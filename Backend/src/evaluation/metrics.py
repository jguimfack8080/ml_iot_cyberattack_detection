"""
Evaluation metrics for the hierarchical classifier.

Computes Balanced Accuracy, F1-macro, per-class Precision/Recall/F1,
and demonstrates the accuracy vs. Balanced Accuracy divergence on imbalanced data.

Scientific basis:
  - Balanced Accuracy as primary metric: Raturi et al. (2026, DOI: 10.1002/spy2.70220)
  - Imbalance problem: Hosseini et al. (2025, DOI: 10.3390/electronics14010069)
"""
import logging

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    f1_score,
    precision_recall_fscore_support,
)

from src.pipelines._core import TrainedPipeline

logger = logging.getLogger(__name__)


def evaluate_stage1(trained: TrainedPipeline) -> dict:
    """
    Compute Stage 1 (binary) metrics on the held-out test set.

    Returns dict with: accuracy, balanced_accuracy, f1_macro, f1_binary,
    precision_per_class, recall_per_class, f1_per_class, support_per_class.
    """
    y_pred = trained.classifier.predict_stage1(trained.X_test)
    y_true = trained.y_binary_test

    acc = accuracy_score(y_true, y_pred)
    ba = balanced_accuracy_score(y_true, y_pred)
    f1_mac = f1_score(y_true, y_pred, average="macro")
    f1_bin = f1_score(y_true, y_pred, average="binary")

    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=[0, 1], zero_division=0
    )

    result = {
        "stage": 1,
        "pipeline": trained.pipeline_name,
        "accuracy": round(float(acc), 6),
        "balanced_accuracy": round(float(ba), 6),
        "f1_macro": round(float(f1_mac), 6),
        "f1_binary": round(float(f1_bin), 6),
        "per_class": {
            "non_dos": {
                "precision": round(float(precision[0]), 6),
                "recall": round(float(recall[0]), 6),
                "f1": round(float(f1[0]), 6),
                "support": int(support[0]),
            },
            "dos_ddos": {
                "precision": round(float(precision[1]), 6),
                "recall": round(float(recall[1]), 6),
                "f1": round(float(f1[1]), 6),
                "support": int(support[1]),
            },
        },
    }
    _log_stage1_results(result)
    return result


def evaluate_stage2(trained: TrainedPipeline) -> dict:
    """
    Compute Stage 2 (multiclass) metrics on the non-DoS test instances.

    Evaluates on TRUE non-DoS instances only to isolate Stage 2 performance
    from Stage 1 errors (same approach as training).

    Returns dict with: accuracy, balanced_accuracy, f1_macro, per_class metrics.
    """
    non_dos_mask = trained.y_binary_test == 0
    X_test_stage2 = trained.X_test[non_dos_mask]
    y_true = trained.y_category_test[non_dos_mask]

    if len(y_true) == 0:
        logger.warning("No non-DoS test instances found for Stage 2 evaluation.")
        return {"stage": 2, "error": "no_non_dos_instances"}

    y_pred = trained.classifier.predict_stage2(X_test_stage2)
    labels = sorted(np.unique(y_true))

    acc = accuracy_score(y_true, y_pred)
    ba = balanced_accuracy_score(y_true, y_pred)
    f1_mac = f1_score(y_true, y_pred, average="macro", zero_division=0)

    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=labels, zero_division=0
    )

    per_class = {
        str(label): {
            "precision": round(float(p), 6),
            "recall": round(float(r), 6),
            "f1": round(float(f), 6),
            "support": int(s),
        }
        for label, p, r, f, s in zip(labels, precision, recall, f1, support)
    }

    result = {
        "stage": 2,
        "pipeline": trained.pipeline_name,
        "n_test_instances": int(len(y_true)),
        "accuracy": round(float(acc), 6),
        "balanced_accuracy": round(float(ba), 6),
        "f1_macro": round(float(f1_mac), 6),
        "per_class": per_class,
    }
    _log_stage2_results(result)
    return result


def accuracy_vs_balanced_accuracy(trained: TrainedPipeline) -> dict:
    """
    Demonstrate the divergence between accuracy and Balanced Accuracy.

    Hosseini et al. (2025) show that accuracy misleads on imbalanced IDS datasets.
    This function quantifies the gap for Stage 1 and Stage 2.

    Returns dict with stage1 and stage2 comparisons.
    """
    s1_pred = trained.classifier.predict_stage1(trained.X_test)
    s1_acc = accuracy_score(trained.y_binary_test, s1_pred)
    s1_ba = balanced_accuracy_score(trained.y_binary_test, s1_pred)

    non_dos_mask = trained.y_binary_test == 0
    s2_pred = trained.classifier.predict_stage2(trained.X_test[non_dos_mask])
    s2_acc = accuracy_score(trained.y_category_test[non_dos_mask], s2_pred)
    s2_ba = balanced_accuracy_score(trained.y_category_test[non_dos_mask], s2_pred)

    result = {
        "pipeline": trained.pipeline_name,
        "stage1": {
            "accuracy": round(float(s1_acc), 6),
            "balanced_accuracy": round(float(s1_ba), 6),
            "gap": round(float(s1_acc - s1_ba), 6),
        },
        "stage2": {
            "accuracy": round(float(s2_acc), 6),
            "balanced_accuracy": round(float(s2_ba), 6),
            "gap": round(float(s2_acc - s2_ba), 6),
        },
    }
    logger.info(
        "Accuracy vs. BA gap -- Pipeline %s | Stufe1: %.4f | Stufe2: %.4f",
        trained.pipeline_name,
        result["stage1"]["gap"],
        result["stage2"]["gap"],
    )
    return result


def full_report(trained: TrainedPipeline) -> dict:
    """
    Generate the complete evaluation report for both stages.

    Returns dict with stage1, stage2, and accuracy_vs_ba sections.
    """
    return {
        "pipeline": trained.pipeline_name,
        "stage1": evaluate_stage1(trained),
        "stage2": evaluate_stage2(trained),
        "accuracy_vs_balanced_accuracy": accuracy_vs_balanced_accuracy(trained),
    }


def _log_stage1_results(r: dict) -> None:
    logger.info(
        "Stufe 1 [Pipeline %s] | Accuracy=%.4f | BA=%.4f | F1-macro=%.4f",
        r["pipeline"], r["accuracy"], r["balanced_accuracy"], r["f1_macro"],
    )
    for cls, m in r["per_class"].items():
        logger.debug(
            "  %-12s | P=%.4f R=%.4f F1=%.4f support=%d",
            cls, m["precision"], m["recall"], m["f1"], m["support"],
        )


def _log_stage2_results(r: dict) -> None:
    logger.info(
        "Stufe 2 [Pipeline %s] | Accuracy=%.4f | BA=%.4f | F1-macro=%.4f | %d instances",
        r["pipeline"], r["accuracy"], r["balanced_accuracy"], r["f1_macro"],
        r["n_test_instances"],
    )
    for cls, m in r["per_class"].items():
        logger.info(
            "  %-16s | P=%.4f R=%.4f F1=%.4f support=%d",
            cls, m["precision"], m["recall"], m["f1"], m["support"],
        )
