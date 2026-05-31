"""
Pipeline A: StandardScaler → PCA (39→16) → Hierarchical Gradient Boosting.

Replicates the preprocessing of Raturi et al. (2026, DOI: 10.1002/spy2.70220).
PCA reduces interpretability of SHAP explanations (components are linear combinations
of original features). Compared against Pipeline B in the Ablation Study.
"""
import logging

from src.features.preprocessor_a import build_preprocessor_a
from src.pipelines._core import PipelineConfig, TrainedPipeline, run_pipeline

logger = logging.getLogger(__name__)


def run_pipeline_a(config: PipelineConfig) -> TrainedPipeline:
    """
    Execute Pipeline A end-to-end.

    Flow: MERGED_CSV → label mapping → 80/20 split → StandardScaler + PCA(39→16)
          → HierarchicalClassifier (Stage 1 binary + Stage 2 multiclass)
          → basic metrics (Balanced Accuracy, F1-macro per stage)

    Args:
        config: Pipeline configuration (data_dir, n_per_class_per_file, etc.).

    Returns:
        TrainedPipeline with fitted preprocessor, classifier, and test data.
    """
    preprocessor = build_preprocessor_a(
        n_components=config.n_pca_components,
        random_state=config.random_state,
    )
    return run_pipeline(config, preprocessor, pipeline_name="A")
