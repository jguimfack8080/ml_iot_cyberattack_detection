"""
SHAP analysis for the hierarchical classifier (Stage 1 and Stage 2).

Uses SHAP TreeExplainer which computes exact Shapley values for tree-based
models without approximation (Mohale & Obagbuwa 2025, DOI: 10.3389/fcomp.2025.1520741).

Two levels of analysis:
  Global: mean(|SHAP values|) per feature per class -> feature importance ranking
  Local:  SHAP values for individual misclassified instances

Scientific basis:
  - SHAP method choice: Ogunseyi et al. (2026, DOI: 10.3390/s26020363)
  - Quality metrics (fidelity, stability, Jaccard): Hermosilla et al. (2025, DOI: 10.3390/app15137329)
  - Semantic validation reference: Neto et al. (2023, DOI: 10.3390/s23135941)
"""
import logging
from dataclasses import dataclass, field

import numpy as np
import shap

from src.pipelines._core import TrainedPipeline

logger = logging.getLogger(__name__)


@dataclass
class ShapResult:
    """Container for SHAP analysis results of one classifier stage."""
    stage: int                          # 1 (binary) or 2 (multiclass)
    pipeline: str                       # "A" or "B"
    shap_values: np.ndarray            # shape: (n_samples, n_features) or (n_classes, n_samples, n_features)
    base_values: np.ndarray            # expected value(s)
    feature_names: list[str]           # feature names (original or PCA component names)
    class_names: list[str]             # class labels
    X_test: np.ndarray                 # preprocessed test features used for SHAP
    y_true: np.ndarray                 # ground truth labels
    y_pred: np.ndarray                 # model predictions
    misclassified_indices: np.ndarray  # indices of misclassified instances
    global_importance: dict[str, float] = field(default_factory=dict)  # mean(|SHAP|) per feature


def compute_stage1_shap(
    trained: TrainedPipeline,
    max_samples: int = 500,
    random_state: int = 42,
) -> ShapResult:
    """
    Compute SHAP values for Stage 1 (binary classifier).

    Uses TreeExplainer for exact computation without approximation.
    Subsample to max_samples for speed (SHAP on 167K instances is slow).

    Args:
        trained: Fitted TrainedPipeline.
        max_samples: Max number of test instances to explain.
        random_state: Seed for subsampling reproducibility.

    Returns:
        ShapResult with SHAP values, feature importance, and misclassified instances.
    """
    logger.info(
        "Computing SHAP Stage 1 [Pipeline %s] -- up to %d samples...",
        trained.pipeline_name, max_samples
    )

    explainer = shap.TreeExplainer(trained.classifier.stage1)

    # Subsample for speed
    rng = np.random.default_rng(random_state)
    n = min(max_samples, len(trained.X_test))
    idx = rng.choice(len(trained.X_test), n, replace=False)
    X_sample = trained.X_test[idx]
    y_true_sample = trained.y_binary_test[idx]

    shap_values = explainer.shap_values(X_sample)
    # For binary GradientBoosting, shap_values is shape (n_samples, n_features) for class 1
    if isinstance(shap_values, list):
        shap_values = shap_values[1]  # positive class (DoS/DDoS)

    y_pred_sample = trained.classifier.stage1.predict(X_sample)
    misclassified = np.where(y_pred_sample != y_true_sample)[0]

    feature_names = _get_feature_names(trained, stage=1)
    global_importance = _compute_global_importance(shap_values, feature_names)

    logger.info(
        "Stage 1 SHAP done. Top 5 features: %s",
        list(global_importance.keys())[:5]
    )

    return ShapResult(
        stage=1,
        pipeline=trained.pipeline_name,
        shap_values=shap_values,
        base_values=np.array([explainer.expected_value]
                             if np.isscalar(explainer.expected_value)
                             else explainer.expected_value),
        feature_names=feature_names,
        class_names=["non-DoS", "DoS/DDoS"],
        X_test=X_sample,
        y_true=y_true_sample,
        y_pred=y_pred_sample,
        misclassified_indices=misclassified,
        global_importance=global_importance,
    )


def compute_stage2_shap(
    trained: TrainedPipeline,
    max_samples: int = 500,
    random_state: int = 42,
) -> ShapResult:
    """
    Compute SHAP values for Stage 2 (multiclass classifier).

    Evaluates on TRUE non-DoS test instances to isolate Stage 2 behavior.

    Args:
        trained: Fitted TrainedPipeline.
        max_samples: Max number of test instances to explain.
        random_state: Seed for subsampling reproducibility.

    Returns:
        ShapResult with per-class SHAP values and feature importance.
    """
    logger.info(
        "Computing SHAP Stage 2 [Pipeline %s] -- up to %d samples...",
        trained.pipeline_name, max_samples
    )

    non_dos_mask = trained.y_binary_test == 0
    X_non_dos = trained.X_test[non_dos_mask]
    y_true_non_dos = trained.y_category_test[non_dos_mask]

    # Subsample
    rng = np.random.default_rng(random_state)
    n = min(max_samples, len(X_non_dos))
    idx = rng.choice(len(X_non_dos), n, replace=False)
    X_sample = X_non_dos[idx]
    y_true_sample = y_true_non_dos[idx]

    explainer = shap.TreeExplainer(trained.classifier.stage2)
    shap_values = explainer.shap_values(X_sample)
    # shap_values is list of arrays (one per class) for multiclass GradientBoosting
    shap_array = np.array(shap_values)  # shape: (n_classes, n_samples, n_features)

    y_pred_sample = trained.classifier.stage2.predict(X_sample)
    misclassified = np.where(y_pred_sample != y_true_sample)[0]

    feature_names = _get_feature_names(trained, stage=2)
    class_names = list(trained.classifier.stage2.classes_)
    global_importance = _compute_global_importance_multiclass(
        shap_array, feature_names, class_names
    )

    logger.info(
        "Stage 2 SHAP done. %d misclassifications out of %d.",
        len(misclassified), n
    )

    return ShapResult(
        stage=2,
        pipeline=trained.pipeline_name,
        shap_values=shap_array,
        base_values=np.array(explainer.expected_value),
        feature_names=feature_names,
        class_names=class_names,
        X_test=X_sample,
        y_true=y_true_sample,
        y_pred=y_pred_sample,
        misclassified_indices=misclassified,
        global_importance=global_importance,
    )


def _get_feature_names(trained: TrainedPipeline, stage: int) -> list[str]:
    """
    Return feature names after preprocessing.

    Pipeline A: PCA components (PC1, PC2, ..., PC16) -- not semantically named
    Pipeline B: original 39 feature names -- semantically interpretable
    """
    if trained.pipeline_name == "B":
        return trained.feature_names_in
    else:
        n_out = trained.X_test.shape[1]
        return [f"PC{i+1}" for i in range(n_out)]


def _compute_global_importance(
    shap_values: np.ndarray,
    feature_names: list[str],
) -> dict[str, float]:
    """Global importance: mean(|SHAP values|) per feature, sorted descending."""
    importance = np.abs(shap_values).mean(axis=0)
    return dict(
        sorted(
            zip(feature_names, importance.tolist()),
            key=lambda x: x[1],
            reverse=True,
        )
    )


def _compute_global_importance_multiclass(
    shap_array: np.ndarray,
    feature_names: list[str],
    class_names: list[str],
) -> dict[str, dict[str, float]]:
    """
    Global importance per class for multiclass SHAP.
    Returns {class_name: {feature_name: importance_score}}.
    """
    result = {}
    for i, cls in enumerate(class_names):
        result[cls] = _compute_global_importance(shap_array[i], feature_names)
    return result


def get_misclassified_instances(result: ShapResult, top_k: int = 5) -> list[dict]:
    """
    Return details of the top_k misclassified instances for local SHAP analysis.

    Each entry includes: index, true label, predicted label, top contributing features.
    """
    instances = []
    for i in result.misclassified_indices[:top_k]:
        if result.stage == 1:
            sv = result.shap_values[i]
        else:
            # For multiclass: use the predicted class SHAP values
            pred_cls_idx = list(result.class_names).index(result.y_pred[i])
            sv = result.shap_values[pred_cls_idx][i]

        top_features = sorted(
            zip(result.feature_names, sv.tolist()),
            key=lambda x: abs(x[1]),
            reverse=True,
        )[:5]

        instances.append({
            "index": int(i),
            "true_label": str(result.y_true[i]),
            "predicted_label": str(result.y_pred[i]),
            "top_shap_features": [
                {"feature": f, "shap_value": round(v, 6)} for f, v in top_features
            ],
        })
    return instances
