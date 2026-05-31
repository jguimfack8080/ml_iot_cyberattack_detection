"""
Training script — runs Pipeline A and/or B on the real CICIoT2023 MERGED_CSV data.

Usage (from Backend/ with venv activated):
    .venv\\Scripts\\python scripts\\train_pipelines.py --pipeline both

Watch progress in real-time (PowerShell, ouvrir un 2e terminal) :
    Get-Content results\\logs\\train_latest.log -Wait

Vérifier si c'est terminé :
    Get-Content results\\logs\\train_latest.log -Tail 5
    → Chercher la dernière ligne : "=== TRAINING COMPLETE" ou "=== TRAINING FAILED"
"""
import argparse
import json
import logging
import sys
from pathlib import Path

# Ensure src/ is importable when running as a script
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import joblib

from src.models.stage1_classifier import Stage1Config
from src.models.stage2_classifier import Stage2Config
from src.pipelines._core import PipelineConfig
from src.pipelines.pipeline_a import run_pipeline_a
from src.pipelines.pipeline_b import run_pipeline_b
from src.utils.logger import (
    log_training_complete,
    log_training_error,
    setup_training_logger,
)

_DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "Dataset" / "MERGED_CSV"
_DEFAULT_MODELS_DIR = Path(__file__).resolve().parent.parent / "models_artifacts"
_DEFAULT_RESULTS_DIR = Path(__file__).resolve().parent.parent / "results" / "metrics"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Train Pipeline A and/or B on CICIoT2023 MERGED_CSV",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Exemples :\n"
            "  Entraînement complet  : python scripts/train_pipelines.py --pipeline both\n"
            "  Test rapide (5 files) : python scripts/train_pipelines.py --pipeline both "
            "--max-files 5 --n-per-class 200\n"
            "  Pipeline A seule      : python scripts/train_pipelines.py --pipeline A\n"
            "\nSuivi en temps réel (PowerShell) :\n"
            "  Get-Content results\\\\logs\\\\train_latest.log -Wait"
        ),
    )
    p.add_argument("--data-dir", type=Path, default=_DEFAULT_DATA_DIR,
                   help="Chemin vers le dossier MERGED_CSV")
    p.add_argument("--models-dir", type=Path, default=_DEFAULT_MODELS_DIR,
                   help="Dossier de sortie des modèles .pkl")
    p.add_argument("--results-dir", type=Path, default=_DEFAULT_RESULTS_DIR,
                   help="Dossier de sortie des métriques JSON")
    p.add_argument("--pipeline", choices=["A", "B", "both"], default="both",
                   help="Quelle(s) pipeline(s) entraîner (défaut: both)")
    p.add_argument("--n-per-class", type=int, default=500,
                   help="Lignes échantillonnées par classe par fichier CSV (défaut: 500)")
    p.add_argument("--max-files", type=int, default=None,
                   help="Limiter le nombre de fichiers CSV (None = tous les 63)")
    p.add_argument(
        "--best-params-dir", type=Path, default=None,
        help=(
            "Charger les meilleurs hyperparametres depuis best_params_A.json "
            "et best_params_B.json dans ce dossier (produit par grid_search.py)"
        ),
    )
    return p.parse_args()


def _load_best_params(params_dir: Path, pipeline: str) -> tuple[Stage1Config, Stage2Config]:
    """Charge les meilleurs HP depuis best_params_{pipeline}.json."""
    path = params_dir / f"best_params_{pipeline}.json"
    if not path.exists():
        raise FileNotFoundError(
            f"best_params_{pipeline}.json introuvable dans {params_dir}. "
            "Lancer grid_search.py d'abord."
        )
    data = json.loads(path.read_text(encoding="utf-8"))
    s1 = Stage1Config(**data["stage1"]["best_params"])
    s2 = Stage2Config(**data["stage2"]["best_params"])
    logging.getLogger(__name__).info(
        "Pipeline %s -- best HP charges : Stufe1=%s | Stufe2=%s",
        pipeline, data["stage1"]["best_params"], data["stage2"]["best_params"],
    )
    return s1, s2


def save_result(result, models_dir: Path, results_dir: Path) -> None:
    """Sauvegarde les modèles (.pkl) et les métriques (.json) sur disque."""
    models_dir.mkdir(parents=True, exist_ok=True)
    results_dir.mkdir(parents=True, exist_ok=True)

    name = result.pipeline_name
    logger = logging.getLogger(__name__)

    # Sérialisation des modèles
    joblib.dump(result.preprocessor,       models_dir / f"preprocessor_{name}.pkl")
    joblib.dump(result.classifier.stage1,  models_dir / f"stage1_{name}.pkl")
    joblib.dump(result.classifier.stage2,  models_dir / f"stage2_{name}.pkl")

    # Métriques JSON
    metrics = {
        "pipeline":                    name,
        "balanced_accuracy_stage1":    round(result.balanced_accuracy_stage1, 6),
        "balanced_accuracy_stage2":    round(result.balanced_accuracy_stage2, 6),
        "f1_macro_stage1":             round(result.f1_macro_stage1, 6),
        "f1_macro_stage2":             round(result.f1_macro_stage2, 6),
        "training_time_seconds":       round(result.training_time_seconds, 2),
        "n_train_samples":             int(result.X_test.shape[0]),
        "n_test_samples":              int(result.X_test.shape[0]),
        "n_features_in":               len(result.feature_names_in),
        "x_test_shape":                list(result.X_test.shape),
    }
    metrics_path = results_dir / f"metrics_pipeline_{name}.json"
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    logger.info("Pipeline %s — modèles sauvegardés : %s", name, models_dir)
    logger.info("Pipeline %s — métriques sauvegardées : %s", name, metrics_path)


def main() -> int:
    args = parse_args()

    # --- Logging vers fichier dès le départ ---
    root_logger, log_path = setup_training_logger()
    logger = logging.getLogger(__name__)

    logger.info("Commande : python scripts/train_pipelines.py --pipeline %s "
                "--n-per-class %d --max-files %s",
                args.pipeline, args.n_per_class, args.max_files)

    if not args.data_dir.is_dir():
        logger.error("Dossier MERGED_CSV introuvable : %s", args.data_dir)
        log_training_error(root_logger, FileNotFoundError(str(args.data_dir)))
        return 1

    # Chargement des best HP si --best-params-dir fourni
    stage1_cfg_a = stage2_cfg_a = stage1_cfg_b = stage2_cfg_b = None
    if args.best_params_dir is not None:
        if args.pipeline in ("A", "both"):
            stage1_cfg_a, stage2_cfg_a = _load_best_params(args.best_params_dir, "A")
        if args.pipeline in ("B", "both"):
            stage1_cfg_b, stage2_cfg_b = _load_best_params(args.best_params_dir, "B")
        logger.info("Mode : reentrainement avec hyperparametres optimises (Grid Search)")
    else:
        logger.info("Mode : entrainement avec hyperparametres par defaut")

    config_a = PipelineConfig(
        data_dir=args.data_dir,
        n_per_class_per_file=args.n_per_class,
        max_files=args.max_files,
        stage1_config=stage1_cfg_a,
        stage2_config=stage2_cfg_a,
    )
    config_b = PipelineConfig(
        data_dir=args.data_dir,
        n_per_class_per_file=args.n_per_class,
        max_files=args.max_files,
        stage1_config=stage1_cfg_b,
        stage2_config=stage2_cfg_b,
    )

    results = []

    try:
        if args.pipeline in ("A", "both"):
            logger.info(">>> Démarrage Pipeline A (StandardScaler + PCA 39->16)")
            result_a = run_pipeline_a(config_a)
            save_result(result_a, args.models_dir, args.results_dir)
            results.append(result_a)

        if args.pipeline in ("B", "both"):
            logger.info(">>> Démarrage Pipeline B (StandardScaler, 39 features)")
            result_b = run_pipeline_b(config_b)
            save_result(result_b, args.models_dir, args.results_dir)
            results.append(result_b)

    except Exception as exc:
        log_training_error(root_logger, exc)
        return 1

    # --- Résumé final ---
    logger.info("=" * 60)
    logger.info("RÉSUMÉ DE L'ENTRAÎNEMENT")
    logger.info("=" * 60)
    for r in results:
        logger.info(
            "Pipeline %s | Stufe1 BA=%.4f F1=%.4f | Stufe2 BA=%.4f F1=%.4f | %.1f s",
            r.pipeline_name,
            r.balanced_accuracy_stage1, r.f1_macro_stage1,
            r.balanced_accuracy_stage2, r.f1_macro_stage2,
            r.training_time_seconds,
        )
    logger.info("Fichier log complet : %s", log_path)

    log_training_complete(root_logger)
    return 0


if __name__ == "__main__":
    sys.exit(main())
