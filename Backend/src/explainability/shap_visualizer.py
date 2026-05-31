"""
SHAP visualization: Summary Plot, Waterfall Plot, Force Plot.

Saves PNG figures to results/figures/.
"""
import logging
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import shap

from src.explainability.shap_analysis import ShapResult

logger = logging.getLogger(__name__)

_FIGURES_DIR = Path(__file__).resolve().parent.parent.parent / "results" / "figures"


def plot_summary_stage1(
    result: ShapResult,
    output_dir: Path = _FIGURES_DIR,
    max_display: int = 15,
) -> Path:
    """
    Beeswarm summary plot for Stage 1 (binary) SHAP values.

    Shows the distribution and direction of each feature's impact.
    Saved as shap_summary_stage1_pipeline{A|B}.png.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"shap_summary_stage1_pipeline{result.pipeline}.png"

    fig, ax = plt.subplots(figsize=(8, 6))
    shap.summary_plot(
        result.shap_values,
        result.X_test,
        feature_names=result.feature_names,
        max_display=max_display,
        show=False,
        plot_type="dot",
    )
    plt.title(
        f"SHAP Summary: Stufe 1 (Pipeline {result.pipeline})\n"
        "DoS/DDoS vs. non-DoS"
    )
    plt.tight_layout()
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    logger.info("SHAP summary Stage 1 saved: %s", out_path)
    return out_path


def plot_summary_stage2_per_class(
    result: ShapResult,
    output_dir: Path = _FIGURES_DIR,
    max_display: int = 15,
) -> list[Path]:
    """
    Beeswarm summary plots for each Stage 2 class.

    Generates one plot per attack category showing which features drive
    the classification of that specific attack type.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []

    for i, cls_name in enumerate(result.class_names):
        out_path = output_dir / f"shap_summary_stage2_{cls_name.replace('-', '_')}_pipeline{result.pipeline}.png"
        fig, _ = plt.subplots(figsize=(8, 6))
        shap.summary_plot(
            result.shap_values[i],
            result.X_test,
            feature_names=result.feature_names,
            max_display=max_display,
            show=False,
            plot_type="dot",
        )
        plt.title(
            f"SHAP Summary: {cls_name} (Pipeline {result.pipeline})\n"
            "Stufe 2 Feature Importance"
        )
        plt.tight_layout()
        plt.savefig(out_path, dpi=150, bbox_inches="tight")
        plt.close()
        logger.info("SHAP summary %s saved: %s", cls_name, out_path)
        paths.append(out_path)

    return paths


def plot_bar_global_importance(
    result: ShapResult,
    output_dir: Path = _FIGURES_DIR,
    top_k: int = 15,
) -> Path:
    """
    Bar chart of global feature importance (mean |SHAP|) for Stage 1 or Stage 2.

    For Stage 2, aggregates across all classes.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    if result.stage == 1:
        importance = result.global_importance
        title = f"Global SHAP Feature Importance: Stufe 1 (Pipeline {result.pipeline})"
        fname = f"shap_global_stage1_pipeline{result.pipeline}.png"
    else:
        # Aggregate across classes: mean of per-class importances
        all_values: dict[str, list] = {}
        for cls_imp in result.global_importance.values():
            for feat, val in cls_imp.items():
                all_values.setdefault(feat, []).append(val)
        importance = {f: float(np.mean(v)) for f, v in all_values.items()}
        importance = dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))
        title = f"Global SHAP Feature Importance: Stufe 2 (Pipeline {result.pipeline})"
        fname = f"shap_global_stage2_pipeline{result.pipeline}.png"

    features = list(importance.keys())[:top_k]
    values = [importance[f] for f in features]

    fig, ax = plt.subplots(figsize=(8, max(4, len(features) * 0.35)))
    bars = ax.barh(features[::-1], values[::-1], color="steelblue")
    ax.set_xlabel("mean(|SHAP value|)")
    ax.set_title(title)
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()

    out_path = output_dir / fname
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    logger.info("SHAP global importance chart saved: %s", out_path)
    return out_path


def plot_waterfall_misclassified(
    result: ShapResult,
    instance_idx: int,
    output_dir: Path = _FIGURES_DIR,
) -> Path | None:
    """
    Waterfall plot for a single misclassified instance.

    Shows how each feature contributes (positively or negatively) to the
    prediction, starting from the base value (expected model output).
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    if instance_idx >= len(result.X_test):
        logger.warning("Instance index %d out of range.", instance_idx)
        return None

    true_label = result.y_true[instance_idx]
    pred_label = result.y_pred[instance_idx]

    if result.stage == 1:
        sv = result.shap_values[instance_idx]
        base = float(result.base_values[0]) if len(result.base_values) == 1 else float(result.base_values)
        explanation = shap.Explanation(
            values=sv,
            base_values=base,
            data=result.X_test[instance_idx],
            feature_names=result.feature_names,
        )
    else:
        pred_cls_idx = list(result.class_names).index(str(pred_label))
        sv = result.shap_values[pred_cls_idx][instance_idx]
        base = float(result.base_values[pred_cls_idx])
        explanation = shap.Explanation(
            values=sv,
            base_values=base,
            data=result.X_test[instance_idx],
            feature_names=result.feature_names,
        )

    fig, _ = plt.subplots(figsize=(10, 6))
    shap.waterfall_plot(explanation, max_display=15, show=False)
    plt.title(
        f"SHAP Waterfall: Stufe {result.stage} Pipeline {result.pipeline}\n"
        f"True: {true_label}  |  Predicted: {pred_label}"
    )
    plt.tight_layout()

    fname = (
        f"shap_waterfall_stage{result.stage}_pipeline{result.pipeline}"
        f"_idx{instance_idx}.png"
    )
    out_path = output_dir / fname
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    logger.info("SHAP waterfall plot saved: %s", out_path)
    return out_path
