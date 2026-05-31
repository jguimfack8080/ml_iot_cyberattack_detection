"""
Confusion matrix computation and export for Stage 1 and Stage 2.

Generates PNG figures saved to results/figures/.
"""
import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay, confusion_matrix

from src.pipelines._core import TrainedPipeline

logger = logging.getLogger(__name__)

_FIGURES_DIR = Path(__file__).resolve().parent.parent.parent / "results" / "figures"

_STAGE1_LABELS = ["non-DoS", "DoS/DDoS"]


def plot_and_save_stage1(
    trained: TrainedPipeline,
    output_dir: Path = _FIGURES_DIR,
) -> Path:
    """
    Plot and save the Stage 1 binary confusion matrix.

    Args:
        trained: Fitted TrainedPipeline.
        output_dir: Directory for PNG output.

    Returns:
        Path to the saved PNG file.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    y_pred = trained.classifier.predict_stage1(trained.X_test)
    y_true = trained.y_binary_test

    cm = confusion_matrix(y_true, y_pred, labels=[0, 1])

    fig, ax = plt.subplots(figsize=(5, 4))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=_STAGE1_LABELS)
    disp.plot(ax=ax, colorbar=False, cmap="Blues")
    ax.set_title(
        f"Konfusionsmatrix Stufe 1 -- Pipeline {trained.pipeline_name}\n"
        f"(Balanced Accuracy = {trained.balanced_accuracy_stage1:.4f})"
    )
    fig.tight_layout()

    out_path = output_dir / f"confusion_matrix_stage1_pipeline{trained.pipeline_name}.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info("Stufe 1 confusion matrix saved: %s", out_path)
    return out_path


def plot_and_save_stage2(
    trained: TrainedPipeline,
    output_dir: Path = _FIGURES_DIR,
) -> Path:
    """
    Plot and save the Stage 2 multiclass confusion matrix (non-DoS instances).

    Args:
        trained: Fitted TrainedPipeline.
        output_dir: Directory for PNG output.

    Returns:
        Path to the saved PNG file.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    non_dos_mask = trained.y_binary_test == 0
    X_test_s2 = trained.X_test[non_dos_mask]
    y_true = trained.y_category_test[non_dos_mask]
    y_pred = trained.classifier.predict_stage2(X_test_s2)

    labels = sorted(np.unique(y_true))
    cm = confusion_matrix(y_true, y_pred, labels=labels)

    fig, ax = plt.subplots(figsize=(8, 7))
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(ax=ax, colorbar=False, cmap="Blues", xticks_rotation=45)
    ax.set_title(
        f"Konfusionsmatrix Stufe 2 -- Pipeline {trained.pipeline_name}\n"
        f"(Balanced Accuracy = {trained.balanced_accuracy_stage2:.4f})"
    )
    fig.tight_layout()

    out_path = output_dir / f"confusion_matrix_stage2_pipeline{trained.pipeline_name}.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info("Stufe 2 confusion matrix saved: %s", out_path)
    return out_path


def plot_both(trained: TrainedPipeline, output_dir: Path = _FIGURES_DIR) -> tuple[Path, Path]:
    """Generate and save both confusion matrices for a trained pipeline."""
    p1 = plot_and_save_stage1(trained, output_dir)
    p2 = plot_and_save_stage2(trained, output_dir)
    return p1, p2
