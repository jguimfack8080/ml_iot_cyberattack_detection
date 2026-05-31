"""
Grid Search -- optimisation des hyperparametres de Stufe 1 et Stufe 2.

Strategie :
  1. Chargement d'un sous-ensemble stratifie configurable
     (defaut : max_files=5, n_per_class=50 -> ~8 000 lignes, rapide)
  2. Preprocessing (fit sur train uniquement, pas de data leakage)
  3. GridSearchCV(cv=3, scoring='balanced_accuracy') sur Stufe 1 et Stufe 2 separement
  4. Sauvegarde des meilleurs parametres dans results/metrics/best_params_{pipeline}.json
  5. Optionnel (--retrain) : reentrainement complet sur le dataset reel avec les meilleurs HP

Grille de recherche :
  n_estimators : [100, 200]
  max_depth    : [3, 5]
  learning_rate: [0.05, 0.1]
  subsample    : [0.8, 1.0]
  -> 16 combinaisons x cv=3 x 2 etages = 96 fits par pipeline

Usage (depuis Backend/ avec venv active) :
  .venv/Scripts/python scripts/grid_search.py --pipeline both
  .venv/Scripts/python scripts/grid_search.py --pipeline A --max-files 10 --n-per-class 100
  .venv/Scripts/python scripts/grid_search.py --pipeline both --retrain
"""
import argparse
import json
import logging
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import balanced_accuracy_score

from src.data.constants import (
    BINARY_COL, CATEGORY_COL, FEATURE_COLUMNS, RANDOM_STATE
)
from src.data.label_mapper import apply_label_mapping, validate_split_labels
from src.data.loader import load_stratified
from src.features.preprocessor_a import build_preprocessor_a
from src.features.preprocessor_b import build_preprocessor_b
from src.pipelines._core import PipelineConfig
from src.pipelines.pipeline_a import run_pipeline_a
from src.pipelines.pipeline_b import run_pipeline_b
from src.models.stage1_classifier import Stage1Config
from src.models.stage2_classifier import Stage2Config
from src.utils.logger import setup_training_logger, log_training_complete, log_training_error

_DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "Dataset" / "MERGED_CSV"
_DEFAULT_RESULTS_DIR = Path(__file__).resolve().parent.parent / "results" / "metrics"

PARAM_GRID: dict = {
    "n_estimators": [100, 200],
    "max_depth": [3, 5],
    "learning_rate": [0.05, 0.1],
    "subsample": [0.8, 1.0],
}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Grid Search pour Stufe 1 et Stufe 2 -- Pipelines A et B",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Exemples :\n"
            "  Test rapide (qq minutes) :\n"
            "    .venv/Scripts/python scripts/grid_search.py --pipeline both\n"
            "  Grid Search + reentrainement complet :\n"
            "    .venv/Scripts/python scripts/grid_search.py --pipeline both "
            "--max-files 10 --n-per-class 100 --retrain\n"
            "\nSuivi en temps reel :\n"
            "  Get-Content results/logs/train_latest.log -Wait"
        ),
    )
    p.add_argument("--pipeline", choices=["A", "B", "both"], default="both")
    p.add_argument("--data-dir", type=Path, default=_DEFAULT_DATA_DIR)
    p.add_argument("--results-dir", type=Path, default=_DEFAULT_RESULTS_DIR)
    p.add_argument(
        "--max-files", type=int, default=5,
        help="Nombre de fichiers CSV pour le sous-ensemble Grid Search (defaut: 5)"
    )
    p.add_argument(
        "--n-per-class", type=int, default=50,
        help="Lignes par classe par fichier pour le sous-ensemble (defaut: 50)"
    )
    p.add_argument(
        "--cv", type=int, default=3,
        help="Nombre de folds pour la validation croisee (defaut: 3)"
    )
    p.add_argument(
        "--retrain", action="store_true",
        help="Reentrainer sur le dataset complet avec les meilleurs HP apres Grid Search"
    )
    p.add_argument(
        "--n-per-class-retrain", type=int, default=500,
        help="Lignes par classe par fichier pour le reentrainement complet (defaut: 500)"
    )
    return p.parse_args()


def _load_subset(data_dir: Path, max_files: int, n_per_class: int) -> pd.DataFrame:
    """Charge un sous-ensemble stratifie pour le Grid Search."""
    df = load_stratified(
        data_dir=data_dir,
        n_per_class_per_file=n_per_class,
        max_files=max_files,
        random_state=RANDOM_STATE,
    )
    return apply_label_mapping(df)


def _prepare_arrays(df: pd.DataFrame, test_size: float = 0.2):
    """Extrait les arrays numpy et effectue le split train/test."""
    X = df[list(FEATURE_COLUMNS)].astype(float).to_numpy()
    y_binary = df[BINARY_COL].to_numpy(dtype=int)
    y_category = df[CATEGORY_COL].to_numpy(dtype=str)

    X_train, X_test, y_bin_train, y_bin_test, y_cat_train, y_cat_test = (
        train_test_split(
            X, y_binary, y_category,
            test_size=test_size,
            stratify=y_category,
            random_state=RANDOM_STATE,
        )
    )
    validate_split_labels(pd.Series(y_cat_train), pd.Series(y_cat_test))
    return X_train, X_test, y_bin_train, y_bin_test, y_cat_train, y_cat_test


def _run_grid_search_for_pipeline(
    pipeline_name: str,
    df: pd.DataFrame,
    cv: int,
    results_dir: Path,
) -> dict:
    """
    Lance GridSearchCV sur Stufe 1 et Stufe 2 pour une pipeline donnee.
    Retourne les meilleurs parametres pour chaque etage.
    """
    logger = logging.getLogger(__name__)
    logger.info("Grid Search Pipeline %s -- %d lignes", pipeline_name, len(df))

    X_train, X_test, y_bin_train, y_bin_test, y_cat_train, y_cat_test = _prepare_arrays(df)

    # Preprocessing (fit sur train uniquement)
    if pipeline_name == "A":
        preprocessor = build_preprocessor_a()
    else:
        preprocessor = build_preprocessor_b()

    X_train_prep = preprocessor.fit_transform(X_train)
    X_test_prep = preprocessor.transform(X_test)

    # -------------------------------------------------------------------
    # Stufe 1 : Grid Search binaire (DoS/DDoS vs. non-DoS)
    # -------------------------------------------------------------------
    logger.info(
        "[%s] Stufe 1 Grid Search -- %d combinaisons x cv=%d x %d instances...",
        pipeline_name, len(_expand_grid(PARAM_GRID)), cv, len(X_train_prep)
    )
    t0 = time.perf_counter()
    gs1 = GridSearchCV(
        GradientBoostingClassifier(random_state=RANDOM_STATE),
        PARAM_GRID,
        cv=cv,
        scoring="balanced_accuracy",
        n_jobs=-1,
        verbose=1,
        refit=True,
    )
    gs1.fit(X_train_prep, y_bin_train)
    t1 = time.perf_counter()

    best_params_1 = gs1.best_params_
    best_ba_1_cv = gs1.best_score_
    ba1_test = balanced_accuracy_score(y_bin_test, gs1.best_estimator_.predict(X_test_prep))
    logger.info(
        "[%s] Stufe 1 -- Meilleure BA (CV): %.4f | BA (test): %.4f | Duree: %.1fs",
        pipeline_name, best_ba_1_cv, ba1_test, t1 - t0
    )
    logger.info("[%s] Stufe 1 -- Meilleurs HP: %s", pipeline_name, best_params_1)

    # -------------------------------------------------------------------
    # Stufe 2 : Grid Search multiclasse (non-DoS uniquement)
    # -------------------------------------------------------------------
    non_dos_train = y_bin_train == 0
    non_dos_test = y_bin_test == 0

    logger.info(
        "[%s] Stufe 2 Grid Search -- %d combinaisons x cv=%d x %d instances non-DoS...",
        pipeline_name, len(_expand_grid(PARAM_GRID)), cv, non_dos_train.sum()
    )
    t0 = time.perf_counter()
    gs2 = GridSearchCV(
        GradientBoostingClassifier(random_state=RANDOM_STATE),
        PARAM_GRID,
        cv=cv,
        scoring="balanced_accuracy",
        n_jobs=-1,
        verbose=1,
        refit=True,
    )
    gs2.fit(X_train_prep[non_dos_train], y_cat_train[non_dos_train])
    t1 = time.perf_counter()

    best_params_2 = gs2.best_params_
    best_ba_2_cv = gs2.best_score_
    ba2_test = balanced_accuracy_score(
        y_cat_test[non_dos_test],
        gs2.best_estimator_.predict(X_test_prep[non_dos_test]),
    )
    logger.info(
        "[%s] Stufe 2 -- Meilleure BA (CV): %.4f | BA (test): %.4f | Duree: %.1fs",
        pipeline_name, best_ba_2_cv, ba2_test, t1 - t0
    )
    logger.info("[%s] Stufe 2 -- Meilleurs HP: %s", pipeline_name, best_params_2)

    # -------------------------------------------------------------------
    # Sauvegarde des resultats
    # -------------------------------------------------------------------
    results_dir.mkdir(parents=True, exist_ok=True)
    result = {
        "pipeline": pipeline_name,
        "grid_search_subset": {
            "max_files": "variable",
            "n_per_class_per_file": "variable",
            "n_train": int(len(X_train_prep)),
            "n_test": int(len(X_test_prep)),
        },
        "param_grid": {k: list(v) for k, v in PARAM_GRID.items()},
        "cv_folds": cv,
        "stage1": {
            "best_params": best_params_1,
            "best_balanced_accuracy_cv": round(best_ba_1_cv, 6),
            "balanced_accuracy_test": round(ba1_test, 6),
        },
        "stage2": {
            "best_params": best_params_2,
            "best_balanced_accuracy_cv": round(best_ba_2_cv, 6),
            "balanced_accuracy_test": round(ba2_test, 6),
        },
    }
    out_path = results_dir / f"best_params_{pipeline_name}.json"
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    logger.info("[%s] Resultats Grid Search sauvegardes : %s", pipeline_name, out_path)
    return result


def _expand_grid(grid: dict) -> list:
    """Retourne la liste de toutes les combinaisons de la grille."""
    import itertools
    keys = list(grid.keys())
    values = list(grid.values())
    return [dict(zip(keys, v)) for v in itertools.product(*values)]


def main() -> int:
    args = parse_args()
    root_logger, log_path = setup_training_logger("grid_search")
    logger = logging.getLogger(__name__)

    if not args.data_dir.is_dir():
        logger.error("Dossier MERGED_CSV introuvable : %s", args.data_dir)
        log_training_error(root_logger, FileNotFoundError(str(args.data_dir)))
        return 1

    n_combinations = len(_expand_grid(PARAM_GRID))
    logger.info(
        "Grid Search -- Pipeline=%s | %d combinaisons | cv=%d | "
        "sous-ensemble: max_files=%d, n_per_class=%d",
        args.pipeline, n_combinations, args.cv, args.max_files, args.n_per_class
    )
    logger.info(
        "Duree estimee par pipeline : ~%.0f min",
        n_combinations * args.cv * 2 * 10 / 60
    )

    try:
        # Chargement du sous-ensemble (partage entre A et B)
        logger.info("Chargement du sous-ensemble pour Grid Search...")
        df = _load_subset(args.data_dir, args.max_files, args.n_per_class)
        logger.info("Sous-ensemble charge : %d lignes", len(df))

        gs_results = {}

        if args.pipeline in ("A", "both"):
            gs_results["A"] = _run_grid_search_for_pipeline("A", df, args.cv, args.results_dir)

        if args.pipeline in ("B", "both"):
            gs_results["B"] = _run_grid_search_for_pipeline("B", df, args.cv, args.results_dir)

        # Resume
        logger.info("=" * 60)
        logger.info("RESUME GRID SEARCH")
        logger.info("=" * 60)
        for name, res in gs_results.items():
            logger.info(
                "Pipeline %s | Stufe1 BA(test)=%.4f | Stufe2 BA(test)=%.4f",
                name,
                res["stage1"]["balanced_accuracy_test"],
                res["stage2"]["balanced_accuracy_test"],
            )
            logger.info("  Stufe1 best HP : %s", res["stage1"]["best_params"])
            logger.info("  Stufe2 best HP : %s", res["stage2"]["best_params"])

        # Reentrainement optionnel sur le dataset complet
        if args.retrain:
            logger.info("=" * 60)
            logger.info("REENTRAINEMENT COMPLET avec les meilleurs hyperparametres")
            logger.info("=" * 60)
            for name, res in gs_results.items():
                s1 = res["stage1"]["best_params"]
                s2 = res["stage2"]["best_params"]
                config = PipelineConfig(
                    data_dir=args.data_dir,
                    n_per_class_per_file=args.n_per_class_retrain,
                    stage1_config=Stage1Config(**s1),
                    stage2_config=Stage2Config(**s2),
                )
                logger.info("Reentrainement Pipeline %s...", name)
                if name == "A":
                    result = run_pipeline_a(config)
                else:
                    result = run_pipeline_b(config)
                logger.info(
                    "Pipeline %s (retrain) | Stufe1 BA=%.4f | Stufe2 BA=%.4f | %.1fs",
                    name,
                    result.balanced_accuracy_stage1,
                    result.balanced_accuracy_stage2,
                    result.training_time_seconds,
                )

        logger.info("Fichier log : %s", log_path)
        log_training_complete(root_logger)

    except Exception as exc:
        log_training_error(root_logger, exc)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
