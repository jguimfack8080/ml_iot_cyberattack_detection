"""
Evaluation et analyse SHAP sur les modeles sauvegardes sur disque.

Ce script charge les modeles (preprocesseur + Stufe1 + Stufe2) et les donnees
de test depuis models_artifacts/, puis produit :
  1. Rapport d'evaluation complet (JSON) : BA, F1-macro, Precision/Recall par classe
  2. Matrice de confusion Stufe 1 (2x2) et Stufe 2 (6x6) -> PNG
  3. Comparaison Accuracy vs. Balanced Accuracy -> JSON
  4. Analyse SHAP globale (mean |SHAP|) -> JSON + barplot PNG
  5. Summary plot SHAP par classe (Stufe 2) -> PNG par classe
  6. Waterfall plot pour les top-k instances mal classees -> PNG

Usage (depuis Backend/ avec venv active) :
  .venv\\Scripts\\python scripts\\evaluate_and_explain.py --pipeline both
  .venv\\Scripts\\python scripts\\evaluate_and_explain.py --pipeline B --shap-samples 200

Scientific basis:
  - Balanced Accuracy: Raturi et al. (2026, DOI: 10.1002/spy2.70220)
  - Imbalance: Hosseini et al. (2025, DOI: 10.3390/electronics14010069)
  - SHAP TreeExplainer: Mohale & Obagbuwa (2025, DOI: 10.3389/fcomp.2025.1520741)
  - SHAP quality: Hermosilla et al. (2025, DOI: 10.3390/app15137329)
"""
import argparse
import json
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import joblib
import numpy as np

from src.evaluation.metrics import full_report
from src.evaluation.confusion_matrix import plot_both
from src.explainability.shap_analysis import compute_stage1_shap, compute_stage2_shap, get_misclassified_instances
from src.explainability.shap_visualizer import (
    plot_bar_global_importance,
    plot_summary_stage1,
    plot_summary_stage2_per_class,
    plot_waterfall_misclassified,
)
from src.models.hierarchical_classifier import HierarchicalClassifier
from src.pipelines._core import PipelineConfig, TrainedPipeline
from src.utils.logger import setup_training_logger, log_training_complete, log_training_error

_DEFAULT_MODELS_DIR = Path(__file__).resolve().parent.parent / "models_artifacts"
_DEFAULT_RESULTS_DIR = Path(__file__).resolve().parent.parent / "results"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Evaluation et SHAP sur modeles sauvegardes (models_artifacts/)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Exemples :\n"
            "  Tout evaluer : .venv\\\\Scripts\\\\python scripts\\\\evaluate_and_explain.py --pipeline both\n"
            "  Pipeline B seule : .venv\\\\Scripts\\\\python scripts\\\\evaluate_and_explain.py --pipeline B\n"
            "  SHAP rapide (100 samples) : ...--pipeline B --shap-samples 100\n"
        ),
    )
    p.add_argument("--pipeline", choices=["A", "B", "both"], default="both")
    p.add_argument("--models-dir", type=Path, default=_DEFAULT_MODELS_DIR)
    p.add_argument("--results-dir", type=Path, default=_DEFAULT_RESULTS_DIR)
    p.add_argument(
        "--shap-samples", type=int, default=500,
        help="Nombre d'instances pour le calcul SHAP (defaut: 500)"
    )
    p.add_argument(
        "--waterfall-top-k", type=int, default=3,
        help="Nombre de Waterfall plots par pipeline/stage (defaut: 3)"
    )
    p.add_argument(
        "--skip-shap", action="store_true",
        help="Ignorer l'analyse SHAP (evaluation seule)"
    )
    return p.parse_args()


def load_trained_pipeline(models_dir: Path, pipeline_name: str) -> TrainedPipeline:
    """
    Reconstruit un TrainedPipeline depuis les fichiers sauvegardes sur disque.

    Charge preprocessor_{name}.pkl, stage1_{name}.pkl, stage2_{name}.pkl,
    et test_data_{name}.npz.
    """
    logger = logging.getLogger(__name__)

    preprocessor_path = models_dir / f"preprocessor_{pipeline_name}.pkl"
    stage1_path       = models_dir / f"stage1_{pipeline_name}.pkl"
    stage2_path       = models_dir / f"stage2_{pipeline_name}.pkl"
    test_data_path    = models_dir / f"test_data_{pipeline_name}.npz"

    for p in (preprocessor_path, stage1_path, stage2_path):
        if not p.exists():
            raise FileNotFoundError(
                f"Modele introuvable : {p}\n"
                "Lancer train_pipelines.py d'abord."
            )

    if not test_data_path.exists():
        raise FileNotFoundError(
            f"Donnees de test introuvables : {test_data_path}\n"
            "Relancer train_pipelines.py (version avec sauvegarde .npz)."
        )

    preprocessor = joblib.load(preprocessor_path)
    stage1        = joblib.load(stage1_path)
    stage2        = joblib.load(stage2_path)

    test_data = np.load(test_data_path, allow_pickle=True)
    X_test           = test_data["X_test"]
    y_binary_test    = test_data["y_binary_test"]
    y_category_test  = test_data["y_category_test"]
    feature_names_in = test_data["feature_names_in"].tolist()

    clf = HierarchicalClassifier(stage1=stage1, stage2=stage2)
    clf._is_fitted = True

    from sklearn.metrics import balanced_accuracy_score, f1_score
    s1_pred = stage1.predict(X_test)
    ba1 = balanced_accuracy_score(y_binary_test, s1_pred)
    f1_1 = f1_score(y_binary_test, s1_pred, average="macro")

    non_dos_mask = y_binary_test == 0
    s2_pred = stage2.predict(X_test[non_dos_mask])
    ba2 = balanced_accuracy_score(y_category_test[non_dos_mask], s2_pred)
    f1_2 = f1_score(y_category_test[non_dos_mask], s2_pred, average="macro", zero_division=0)

    trained = TrainedPipeline(
        pipeline_name=pipeline_name,
        preprocessor=preprocessor,
        classifier=clf,
        X_test=X_test,
        y_binary_test=y_binary_test,
        y_category_test=y_category_test,
        feature_names_in=feature_names_in,
        config=PipelineConfig(data_dir=models_dir),
        balanced_accuracy_stage1=ba1,
        balanced_accuracy_stage2=ba2,
        f1_macro_stage1=f1_1,
        f1_macro_stage2=f1_2,
    )

    logger.info(
        "Pipeline %s charge depuis disque | Stufe1 BA=%.4f | Stufe2 BA=%.4f | test=%d instances",
        pipeline_name, ba1, ba2, len(X_test)
    )
    return trained


def run_evaluation(trained: TrainedPipeline, results_dir: Path) -> dict:
    """Lance l'evaluation complete et sauvegarde le rapport JSON."""
    logger = logging.getLogger(__name__)
    metrics_dir = results_dir / "metrics"
    figures_dir = results_dir / "figures"
    metrics_dir.mkdir(parents=True, exist_ok=True)

    # Rapport complet (BA, F1, precision/recall par classe)
    report = full_report(trained)
    report_path = metrics_dir / f"full_report_pipeline_{trained.pipeline_name}.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    logger.info("Rapport d'evaluation sauvegarde : %s", report_path)

    # Matrices de confusion (PNG)
    p1, p2 = plot_both(trained, figures_dir)
    logger.info("Matrices de confusion sauvegardees : %s | %s", p1, p2)

    return report


def run_shap_analysis(
    trained: TrainedPipeline,
    results_dir: Path,
    shap_samples: int,
    waterfall_top_k: int,
) -> None:
    """Lance l'analyse SHAP et sauvegarde JSON + figures."""
    logger = logging.getLogger(__name__)
    metrics_dir = results_dir / "metrics"
    figures_dir = results_dir / "figures"
    metrics_dir.mkdir(parents=True, exist_ok=True)

    name = trained.pipeline_name

    # --- Stufe 1 SHAP ---
    logger.info("Calcul SHAP Stufe 1 [Pipeline %s]...", name)
    s1_result = compute_stage1_shap(trained, max_samples=shap_samples)

    # Sauvegarde JSON importance globale
    s1_imp_path = metrics_dir / f"shap_global_stage1_pipeline{name}.json"
    s1_imp_path.write_text(
        json.dumps(s1_result.global_importance, indent=2), encoding="utf-8"
    )

    # Figures Stufe 1
    plot_summary_stage1(s1_result, figures_dir)
    plot_bar_global_importance(s1_result, figures_dir)

    # Waterfall pour les instances mal classees
    misclassified_1 = get_misclassified_instances(s1_result, top_k=waterfall_top_k)
    for inst in misclassified_1:
        plot_waterfall_misclassified(s1_result, inst["index"], figures_dir)
    logger.info("Stufe 1 SHAP : %d misclassifications analysees", len(misclassified_1))

    # --- Stufe 2 SHAP ---
    logger.info("Calcul SHAP Stufe 2 [Pipeline %s]...", name)
    s2_result = compute_stage2_shap(trained, max_samples=shap_samples)

    # Sauvegarde JSON importance globale par classe
    s2_imp_path = metrics_dir / f"shap_global_stage2_pipeline{name}.json"
    s2_imp_path.write_text(
        json.dumps(s2_result.global_importance, indent=2), encoding="utf-8"
    )

    # Figures Stufe 2
    plot_summary_stage2_per_class(s2_result, figures_dir)
    plot_bar_global_importance(s2_result, figures_dir)

    # Waterfall pour les instances mal classees de Stufe 2
    misclassified_2 = get_misclassified_instances(s2_result, top_k=waterfall_top_k)
    for inst in misclassified_2:
        plot_waterfall_misclassified(s2_result, inst["index"], figures_dir)

    # Sauvegarde details des instances mal classees
    misclass_path = metrics_dir / f"misclassified_instances_pipeline{name}.json"
    misclass_path.write_text(
        json.dumps({"stage1": misclassified_1, "stage2": misclassified_2}, indent=2),
        encoding="utf-8"
    )
    logger.info("Stufe 2 SHAP : %d misclassifications analysees", len(misclassified_2))
    logger.info("SHAP Pipeline %s termine.", name)


def main() -> int:
    args = parse_args()
    root_logger, log_path = setup_training_logger("evaluate_and_explain")
    logger = logging.getLogger(__name__)

    pipelines = ["A", "B"] if args.pipeline == "both" else [args.pipeline]

    logger.info(
        "evaluate_and_explain -- pipeline=%s | shap_samples=%d | skip_shap=%s",
        args.pipeline, args.shap_samples, args.skip_shap,
    )

    try:
        all_reports = {}
        for name in pipelines:
            logger.info("=" * 60)
            logger.info("Pipeline %s", name)
            logger.info("=" * 60)

            trained = load_trained_pipeline(args.models_dir, name)
            report = run_evaluation(trained, args.results_dir)
            all_reports[name] = report

            if not args.skip_shap:
                run_shap_analysis(
                    trained, args.results_dir,
                    shap_samples=args.shap_samples,
                    waterfall_top_k=args.waterfall_top_k,
                )

        # Resume final
        logger.info("=" * 60)
        logger.info("RESUME EVALUATION")
        logger.info("=" * 60)
        for name, report in all_reports.items():
            logger.info(
                "Pipeline %s | Stufe1 BA=%.4f F1=%.4f | Stufe2 BA=%.4f F1=%.4f",
                name,
                report["stage1"]["balanced_accuracy"],
                report["stage1"]["f1_macro"],
                report["stage2"].get("balanced_accuracy", 0.0),
                report["stage2"].get("f1_macro", 0.0),
            )

        logger.info("Fichier log : %s", log_path)
        log_training_complete(root_logger)

    except Exception as exc:
        log_training_error(root_logger, exc)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
