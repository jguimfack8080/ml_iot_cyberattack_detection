"""
IoT Cyberattack Detection — Main Entry Point
Hierarchical Gradient Boosting Classifier on CICIoT2023 with SHAP Analysis

Author: Jordan Guimfack Jeuna (38184)
Module: IT-Sicherheit, M.Sc. IVS, Hochschule Bremerhaven
"""
import argparse
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "IoT Cyberattack Detection: Hierarchical Gradient Boosting + SHAP "
            "on the CICIoT2023 dataset"
        )
    )
    parser.add_argument(
        "--pipeline",
        choices=["A", "B", "both"],
        default="both",
        help="Pipeline A (StandardScaler + PCA 39→16) or B (StandardScaler, all 39 features) or both",
    )
    parser.add_argument(
        "--train",
        action="store_true",
        help="Train the hierarchical classifier",
    )
    parser.add_argument(
        "--evaluate",
        action="store_true",
        help="Evaluate the trained model (Balanced Accuracy, F1-macro, confusion matrix)",
    )
    parser.add_argument(
        "--explain",
        action="store_true",
        help="Run SHAP analysis (global feature importance + local instance explanations)",
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default=None,
        help="Path to MERGED_CSV directory (overrides DATA_DIR from .env)",
    )
    parser.add_argument(
        "--results-dir",
        type=str,
        default=None,
        help="Output directory for metrics and figures (overrides RESULTS_DIR from .env)",
    )
    parser.add_argument(
        "--models-dir",
        type=str,
        default=None,
        help="Directory for saved model artifacts (overrides MODELS_DIR from .env)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if not any([args.train, args.evaluate, args.explain]):
        logger.error("No action specified. Use --train, --evaluate, and/or --explain.")
        return 1

    logger.info("IoT Cyberattack Detection Pipeline starting")
    logger.info("Pipeline: %s | train=%s | evaluate=%s | explain=%s",
                args.pipeline, args.train, args.evaluate, args.explain)

    # TODO (P2): implement pipeline orchestration
    # from src.pipelines.pipeline_a import run_pipeline_a
    # from src.pipelines.pipeline_b import run_pipeline_b

    return 0


if __name__ == "__main__":
    sys.exit(main())
