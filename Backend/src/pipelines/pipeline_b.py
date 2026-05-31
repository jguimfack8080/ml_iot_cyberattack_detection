"""
Pipeline B: StandardScaler only → Hierarchical Gradient Boosting (all 39 features).

No dimensionality reduction. SHAP values map directly to named network features
(Rate, syn_flag_number, Number, etc.), enabling semantic validation against known
IoT attack signatures (Neto et al. 2023, DOI: 10.3390/s23135941).

Key difference from Pipeline A: absence of PCA preserves feature interpretability.
The Ablation Study compares A vs. B to quantify PCA's impact on:
  (a) Balanced Accuracy (performance metric)
  (b) SHAP feature importance stability (explainability metric)
"""
import logging

from src.features.preprocessor_b import build_preprocessor_b
from src.pipelines._core import PipelineConfig, TrainedPipeline, run_pipeline

logger = logging.getLogger(__name__)


def run_pipeline_b(config: PipelineConfig) -> TrainedPipeline:
    """
    Execute Pipeline B end-to-end.

    Flow: MERGED_CSV → label mapping → 80/20 split → StandardScaler (no PCA, 39 features)
          → HierarchicalClassifier (Stage 1 binary + Stage 2 multiclass)
          → basic metrics (Balanced Accuracy, F1-macro per stage)

    Args:
        config: Pipeline configuration (data_dir, n_per_class_per_file, etc.).
            Note: config.n_pca_components is ignored for Pipeline B.

    Returns:
        TrainedPipeline with fitted preprocessor, classifier, and test data.
    """
    preprocessor = build_preprocessor_b(random_state=config.random_state)
    return run_pipeline(config, preprocessor, pipeline_name="B")
