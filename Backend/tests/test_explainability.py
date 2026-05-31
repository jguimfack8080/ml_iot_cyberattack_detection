"""
Unit tests for src.explainability.shap_analysis and src.explainability.shap_visualizer.

Uses synthetic data and the fitted_hierarchical fixture from conftest.py.
SHAP computation is limited to very small sample counts to keep tests fast.
"""
import numpy as np
import pytest
from pathlib import Path


# ---------------------------------------------------------------------------
# Helper: build a TrainedPipeline from synthetic conftest fixtures
# ---------------------------------------------------------------------------

def _make_trained_pipeline(fitted_hierarchical, preprocessed_arrays, name="A"):
    from src.pipelines._core import TrainedPipeline, PipelineConfig
    from src.features.preprocessor_a import build_preprocessor_a

    X_train, X_test, y_bin_train, y_bin_test, y_cat_train, y_cat_test = preprocessed_arrays
    return TrainedPipeline(
        pipeline_name=name,
        preprocessor=build_preprocessor_a(),
        classifier=fitted_hierarchical,
        X_test=X_test,
        y_binary_test=y_bin_test,
        y_category_test=y_cat_test,
        feature_names_in=["f"] * 39,
        config=PipelineConfig(data_dir=Path(".")),
        balanced_accuracy_stage1=0.9,
        balanced_accuracy_stage2=0.6,
    )


# ---------------------------------------------------------------------------
# ShapResult structure tests (compute_stage1_shap)
# ---------------------------------------------------------------------------

class TestComputeStage1Shap:
    def test_returns_shap_result(self, fitted_hierarchical, preprocessed_arrays) -> None:
        from src.explainability.shap_analysis import compute_stage1_shap
        trained = _make_trained_pipeline(fitted_hierarchical, preprocessed_arrays)
        result = compute_stage1_shap(trained, max_samples=10)
        assert result.stage == 1
        assert result.pipeline == "A"

    def test_shap_values_shape(self, fitted_hierarchical, preprocessed_arrays) -> None:
        from src.explainability.shap_analysis import compute_stage1_shap
        trained = _make_trained_pipeline(fitted_hierarchical, preprocessed_arrays)
        result = compute_stage1_shap(trained, max_samples=10)
        n_samples = min(10, len(trained.X_test))
        n_features = trained.X_test.shape[1]
        assert result.shap_values.shape == (n_samples, n_features)

    def test_feature_names_count_matches_features(self, fitted_hierarchical, preprocessed_arrays) -> None:
        from src.explainability.shap_analysis import compute_stage1_shap
        trained = _make_trained_pipeline(fitted_hierarchical, preprocessed_arrays)
        result = compute_stage1_shap(trained, max_samples=10)
        assert len(result.feature_names) == trained.X_test.shape[1]

    def test_global_importance_is_dict(self, fitted_hierarchical, preprocessed_arrays) -> None:
        from src.explainability.shap_analysis import compute_stage1_shap
        trained = _make_trained_pipeline(fitted_hierarchical, preprocessed_arrays)
        result = compute_stage1_shap(trained, max_samples=10)
        assert isinstance(result.global_importance, dict)
        assert len(result.global_importance) == trained.X_test.shape[1]

    def test_global_importance_values_non_negative(self, fitted_hierarchical, preprocessed_arrays) -> None:
        from src.explainability.shap_analysis import compute_stage1_shap
        trained = _make_trained_pipeline(fitted_hierarchical, preprocessed_arrays)
        result = compute_stage1_shap(trained, max_samples=10)
        for val in result.global_importance.values():
            assert val >= 0.0

    def test_class_names_binary(self, fitted_hierarchical, preprocessed_arrays) -> None:
        from src.explainability.shap_analysis import compute_stage1_shap
        trained = _make_trained_pipeline(fitted_hierarchical, preprocessed_arrays)
        result = compute_stage1_shap(trained, max_samples=10)
        assert "non-DoS" in result.class_names
        assert "DoS/DDoS" in result.class_names

    def test_misclassified_indices_is_array(self, fitted_hierarchical, preprocessed_arrays) -> None:
        from src.explainability.shap_analysis import compute_stage1_shap
        trained = _make_trained_pipeline(fitted_hierarchical, preprocessed_arrays)
        result = compute_stage1_shap(trained, max_samples=10)
        assert isinstance(result.misclassified_indices, np.ndarray)

    def test_pipeline_b_uses_original_feature_names(
        self, fitted_hierarchical, preprocessed_arrays
    ) -> None:
        from src.explainability.shap_analysis import compute_stage1_shap
        from src.pipelines._core import TrainedPipeline, PipelineConfig
        from src.features.preprocessor_b import build_preprocessor_b
        from src.data.constants import FEATURE_COLUMNS

        X_train, X_test, y_bin_train, y_bin_test, y_cat_train, y_cat_test = preprocessed_arrays

        # Build Pipeline B trained pipeline with correct 39-feature X_test
        preprocessor_b = build_preprocessor_b()
        from tests.conftest import _N_ROWS_PER_LABEL, _REPRESENTATIVE_LABELS
        import pandas as pd
        from src.data.constants import FEATURE_COLUMNS, LABEL_COL, RANDOM_STATE
        from src.data.label_mapper import apply_label_mapping
        from sklearn.model_selection import train_test_split
        from src.models.hierarchical_classifier import HierarchicalClassifier
        from src.models.stage1_classifier import build_stage1_classifier
        from src.models.stage2_classifier import build_stage2_classifier

        rng = np.random.default_rng(RANDOM_STATE)
        rows = []
        for label in _REPRESENTATIVE_LABELS:
            data = {col: rng.random(_N_ROWS_PER_LABEL) for col in FEATURE_COLUMNS}
            data[LABEL_COL] = label
            rows.append(pd.DataFrame(data))
        df = pd.concat(rows, ignore_index=True)
        df = apply_label_mapping(df)

        from src.data.constants import BINARY_COL, CATEGORY_COL
        X = df[list(FEATURE_COLUMNS)].astype(float).to_numpy()
        y_binary = df[BINARY_COL].to_numpy(dtype=int)
        y_category = df[CATEGORY_COL].to_numpy(dtype=str)

        X_tr, X_te, y_b_tr, y_b_te, y_c_tr, y_c_te = train_test_split(
            X, y_binary, y_category, test_size=0.2, stratify=y_category,
            random_state=RANDOM_STATE
        )
        X_tr_prep = preprocessor_b.fit_transform(X_tr)
        X_te_prep = preprocessor_b.transform(X_te)

        clf_b = HierarchicalClassifier(
            stage1=build_stage1_classifier(),
            stage2=build_stage2_classifier(),
        )
        clf_b.fit(X_tr_prep, y_b_tr, y_c_tr)

        trained_b = TrainedPipeline(
            pipeline_name="B",
            preprocessor=preprocessor_b,
            classifier=clf_b,
            X_test=X_te_prep,
            y_binary_test=y_b_te,
            y_category_test=y_c_te,
            feature_names_in=list(FEATURE_COLUMNS),
            config=PipelineConfig(data_dir=Path(".")),
        )
        result = compute_stage1_shap(trained_b, max_samples=10)
        # Pipeline B: feature names must be the original 39 column names (not PC1, PC2...)
        assert not result.feature_names[0].startswith("PC")
        assert result.feature_names[0] in FEATURE_COLUMNS


# ---------------------------------------------------------------------------
# compute_stage2_shap tests
# ---------------------------------------------------------------------------

class TestComputeStage2Shap:
    def test_returns_shap_result(self, fitted_hierarchical, preprocessed_arrays) -> None:
        from src.explainability.shap_analysis import compute_stage2_shap
        trained = _make_trained_pipeline(fitted_hierarchical, preprocessed_arrays)
        result = compute_stage2_shap(trained, max_samples=10)
        assert result.stage == 2
        assert result.pipeline == "A"

    def test_shap_array_has_class_dimension(self, fitted_hierarchical, preprocessed_arrays) -> None:
        from src.explainability.shap_analysis import compute_stage2_shap
        trained = _make_trained_pipeline(fitted_hierarchical, preprocessed_arrays)
        result = compute_stage2_shap(trained, max_samples=10)
        # shap_values shape: (n_classes, n_samples, n_features)
        assert result.shap_values.ndim == 3
        assert result.shap_values.shape[0] == len(result.class_names)

    def test_global_importance_per_class(self, fitted_hierarchical, preprocessed_arrays) -> None:
        from src.explainability.shap_analysis import compute_stage2_shap
        trained = _make_trained_pipeline(fitted_hierarchical, preprocessed_arrays)
        result = compute_stage2_shap(trained, max_samples=10)
        assert isinstance(result.global_importance, dict)
        for cls in result.class_names:
            assert cls in result.global_importance

    def test_class_names_match_stage2_classes(self, fitted_hierarchical, preprocessed_arrays) -> None:
        from src.explainability.shap_analysis import compute_stage2_shap
        trained = _make_trained_pipeline(fitted_hierarchical, preprocessed_arrays)
        result = compute_stage2_shap(trained, max_samples=10)
        expected_classes = list(trained.classifier.stage2.classes_)
        assert result.class_names == expected_classes


# ---------------------------------------------------------------------------
# get_misclassified_instances tests
# ---------------------------------------------------------------------------

class TestGetMisclassifiedInstances:
    def test_returns_list(self, fitted_hierarchical, preprocessed_arrays) -> None:
        from src.explainability.shap_analysis import compute_stage1_shap, get_misclassified_instances
        trained = _make_trained_pipeline(fitted_hierarchical, preprocessed_arrays)
        result = compute_stage1_shap(trained, max_samples=20)
        instances = get_misclassified_instances(result, top_k=5)
        assert isinstance(instances, list)

    def test_each_instance_has_required_keys(self, fitted_hierarchical, preprocessed_arrays) -> None:
        from src.explainability.shap_analysis import compute_stage1_shap, get_misclassified_instances
        trained = _make_trained_pipeline(fitted_hierarchical, preprocessed_arrays)
        result = compute_stage1_shap(trained, max_samples=20)
        instances = get_misclassified_instances(result, top_k=5)
        for inst in instances:
            assert "index" in inst
            assert "true_label" in inst
            assert "predicted_label" in inst
            assert "top_shap_features" in inst

    def test_top_shap_features_count(self, fitted_hierarchical, preprocessed_arrays) -> None:
        from src.explainability.shap_analysis import compute_stage1_shap, get_misclassified_instances
        trained = _make_trained_pipeline(fitted_hierarchical, preprocessed_arrays)
        result = compute_stage1_shap(trained, max_samples=20)
        instances = get_misclassified_instances(result, top_k=5)
        for inst in instances:
            assert len(inst["top_shap_features"]) <= 5


# ---------------------------------------------------------------------------
# shap_visualizer tests
# ---------------------------------------------------------------------------

class TestShapVisualizer:
    def test_plot_bar_global_importance_stage1_creates_file(
        self, fitted_hierarchical, preprocessed_arrays, tmp_path
    ) -> None:
        from src.explainability.shap_analysis import compute_stage1_shap
        from src.explainability.shap_visualizer import plot_bar_global_importance
        trained = _make_trained_pipeline(fitted_hierarchical, preprocessed_arrays)
        result = compute_stage1_shap(trained, max_samples=10)
        out_path = plot_bar_global_importance(result, output_dir=tmp_path)
        assert out_path.exists()
        assert out_path.suffix == ".png"

    def test_plot_bar_global_importance_stage2_creates_file(
        self, fitted_hierarchical, preprocessed_arrays, tmp_path
    ) -> None:
        from src.explainability.shap_analysis import compute_stage2_shap
        from src.explainability.shap_visualizer import plot_bar_global_importance
        trained = _make_trained_pipeline(fitted_hierarchical, preprocessed_arrays)
        result = compute_stage2_shap(trained, max_samples=10)
        out_path = plot_bar_global_importance(result, output_dir=tmp_path)
        assert out_path.exists()

    def test_plot_summary_stage1_creates_file(
        self, fitted_hierarchical, preprocessed_arrays, tmp_path
    ) -> None:
        from src.explainability.shap_analysis import compute_stage1_shap
        from src.explainability.shap_visualizer import plot_summary_stage1
        trained = _make_trained_pipeline(fitted_hierarchical, preprocessed_arrays)
        result = compute_stage1_shap(trained, max_samples=10)
        out_path = plot_summary_stage1(result, output_dir=tmp_path)
        assert out_path.exists()

    def test_plot_summary_stage2_per_class_creates_files(
        self, fitted_hierarchical, preprocessed_arrays, tmp_path
    ) -> None:
        from src.explainability.shap_analysis import compute_stage2_shap
        from src.explainability.shap_visualizer import plot_summary_stage2_per_class
        trained = _make_trained_pipeline(fitted_hierarchical, preprocessed_arrays)
        result = compute_stage2_shap(trained, max_samples=10)
        paths = plot_summary_stage2_per_class(result, output_dir=tmp_path)
        assert len(paths) == len(result.class_names)
        for p in paths:
            assert p.exists()

    def test_plot_waterfall_misclassified_returns_path_or_none(
        self, fitted_hierarchical, preprocessed_arrays, tmp_path
    ) -> None:
        from src.explainability.shap_analysis import compute_stage1_shap
        from src.explainability.shap_visualizer import plot_waterfall_misclassified
        trained = _make_trained_pipeline(fitted_hierarchical, preprocessed_arrays)
        result = compute_stage1_shap(trained, max_samples=20)
        if len(result.misclassified_indices) > 0:
            idx = int(result.misclassified_indices[0])
            out_path = plot_waterfall_misclassified(result, instance_idx=idx, output_dir=tmp_path)
            assert out_path is None or out_path.exists()

    def test_plot_waterfall_out_of_range_returns_none(
        self, fitted_hierarchical, preprocessed_arrays, tmp_path
    ) -> None:
        from src.explainability.shap_analysis import compute_stage1_shap
        from src.explainability.shap_visualizer import plot_waterfall_misclassified
        trained = _make_trained_pipeline(fitted_hierarchical, preprocessed_arrays)
        result = compute_stage1_shap(trained, max_samples=5)
        out_path = plot_waterfall_misclassified(result, instance_idx=9999, output_dir=tmp_path)
        assert out_path is None
