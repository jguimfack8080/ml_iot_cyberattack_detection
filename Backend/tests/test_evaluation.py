"""Unit tests for src.evaluation.metrics and src.evaluation.confusion_matrix."""
from pathlib import Path
import numpy as np
import pytest

from src.evaluation.metrics import (
    accuracy_vs_balanced_accuracy,
    evaluate_stage1,
    evaluate_stage2,
    full_report,
)


class TestEvaluateStage1:
    def test_returns_expected_keys(self, fitted_hierarchical, preprocessed_arrays) -> None:
        from src.pipelines._core import TrainedPipeline
        from src.pipelines._core import PipelineConfig
        from pathlib import Path

        X_train, X_test, y_bin_train, y_bin_test, y_cat_train, y_cat_test = preprocessed_arrays
        from src.features.preprocessor_a import build_preprocessor_a
        trained = TrainedPipeline(
            pipeline_name="A",
            preprocessor=build_preprocessor_a(),
            classifier=fitted_hierarchical,
            X_test=X_test,
            y_binary_test=y_bin_test,
            y_category_test=y_cat_test,
            feature_names_in=["f"] * 39,
            config=PipelineConfig(data_dir=Path(".")),
        )
        result = evaluate_stage1(trained)
        assert "balanced_accuracy" in result
        assert "f1_macro" in result
        assert "per_class" in result
        assert result["stage"] == 1

    def test_balanced_accuracy_in_range(self, fitted_hierarchical, preprocessed_arrays) -> None:
        from src.pipelines._core import TrainedPipeline, PipelineConfig
        from pathlib import Path
        X_train, X_test, y_bin_train, y_bin_test, y_cat_train, y_cat_test = preprocessed_arrays
        from src.features.preprocessor_a import build_preprocessor_a
        trained = TrainedPipeline(
            pipeline_name="A",
            preprocessor=build_preprocessor_a(),
            classifier=fitted_hierarchical,
            X_test=X_test,
            y_binary_test=y_bin_test,
            y_category_test=y_cat_test,
            feature_names_in=["f"] * 39,
            config=PipelineConfig(data_dir=Path(".")),
        )
        result = evaluate_stage1(trained)
        assert 0.0 <= result["balanced_accuracy"] <= 1.0
        assert 0.0 <= result["accuracy"] <= 1.0

    def test_per_class_has_non_dos_and_dos(self, fitted_hierarchical, preprocessed_arrays) -> None:
        from src.pipelines._core import TrainedPipeline, PipelineConfig
        from pathlib import Path
        X_train, X_test, y_bin_train, y_bin_test, y_cat_train, y_cat_test = preprocessed_arrays
        from src.features.preprocessor_a import build_preprocessor_a
        trained = TrainedPipeline(
            pipeline_name="A",
            preprocessor=build_preprocessor_a(),
            classifier=fitted_hierarchical,
            X_test=X_test,
            y_binary_test=y_bin_test,
            y_category_test=y_cat_test,
            feature_names_in=["f"] * 39,
            config=PipelineConfig(data_dir=Path(".")),
        )
        result = evaluate_stage1(trained)
        assert "non_dos" in result["per_class"]
        assert "dos_ddos" in result["per_class"]


class TestEvaluateStage2:
    def test_returns_expected_keys(self, fitted_hierarchical, preprocessed_arrays) -> None:
        from src.pipelines._core import TrainedPipeline, PipelineConfig
        from pathlib import Path
        X_train, X_test, y_bin_train, y_bin_test, y_cat_train, y_cat_test = preprocessed_arrays
        from src.features.preprocessor_a import build_preprocessor_a
        trained = TrainedPipeline(
            pipeline_name="A",
            preprocessor=build_preprocessor_a(),
            classifier=fitted_hierarchical,
            X_test=X_test,
            y_binary_test=y_bin_test,
            y_category_test=y_cat_test,
            feature_names_in=["f"] * 39,
            config=PipelineConfig(data_dir=Path(".")),
        )
        result = evaluate_stage2(trained)
        assert result["stage"] == 2
        assert "balanced_accuracy" in result
        assert "per_class" in result

    def test_balanced_accuracy_in_range(self, fitted_hierarchical, preprocessed_arrays) -> None:
        from src.pipelines._core import TrainedPipeline, PipelineConfig
        from pathlib import Path
        X_train, X_test, y_bin_train, y_bin_test, y_cat_train, y_cat_test = preprocessed_arrays
        from src.features.preprocessor_a import build_preprocessor_a
        trained = TrainedPipeline(
            pipeline_name="A",
            preprocessor=build_preprocessor_a(),
            classifier=fitted_hierarchical,
            X_test=X_test,
            y_binary_test=y_bin_test,
            y_category_test=y_cat_test,
            feature_names_in=["f"] * 39,
            config=PipelineConfig(data_dir=Path(".")),
        )
        result = evaluate_stage2(trained)
        if "error" not in result:
            assert 0.0 <= result["balanced_accuracy"] <= 1.0


class TestAccuracyVsBalancedAccuracy:
    def test_gap_is_float(self, fitted_hierarchical, preprocessed_arrays) -> None:
        from src.pipelines._core import TrainedPipeline, PipelineConfig
        from pathlib import Path
        X_train, X_test, y_bin_train, y_bin_test, y_cat_train, y_cat_test = preprocessed_arrays
        from src.features.preprocessor_a import build_preprocessor_a
        trained = TrainedPipeline(
            pipeline_name="A",
            preprocessor=build_preprocessor_a(),
            classifier=fitted_hierarchical,
            X_test=X_test,
            y_binary_test=y_bin_test,
            y_category_test=y_cat_test,
            feature_names_in=["f"] * 39,
            config=PipelineConfig(data_dir=Path(".")),
        )
        result = accuracy_vs_balanced_accuracy(trained)
        assert isinstance(result["stage1"]["gap"], float)
        assert isinstance(result["stage2"]["gap"], float)


class TestFullReport:
    def test_full_report_structure(self, fitted_hierarchical, preprocessed_arrays) -> None:
        from src.pipelines._core import TrainedPipeline, PipelineConfig
        from pathlib import Path
        X_train, X_test, y_bin_train, y_bin_test, y_cat_train, y_cat_test = preprocessed_arrays
        from src.features.preprocessor_a import build_preprocessor_a
        trained = TrainedPipeline(
            pipeline_name="A",
            preprocessor=build_preprocessor_a(),
            classifier=fitted_hierarchical,
            X_test=X_test,
            y_binary_test=y_bin_test,
            y_category_test=y_cat_test,
            feature_names_in=["f"] * 39,
            config=PipelineConfig(data_dir=Path(".")),
        )
        report = full_report(trained)
        assert "stage1" in report
        assert "stage2" in report
        assert "accuracy_vs_balanced_accuracy" in report
        assert report["pipeline"] == "A"


# ---------------------------------------------------------------------------
# Confusion matrix tests
# ---------------------------------------------------------------------------

def _make_trained_pipeline_for_cm(fitted_hierarchical, preprocessed_arrays):
    from src.pipelines._core import TrainedPipeline, PipelineConfig
    from src.features.preprocessor_a import build_preprocessor_a
    X_train, X_test, y_bin_train, y_bin_test, y_cat_train, y_cat_test = preprocessed_arrays
    return TrainedPipeline(
        pipeline_name="A",
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


class TestConfusionMatrix:
    def test_plot_stage1_returns_existing_png(
        self, fitted_hierarchical, preprocessed_arrays, tmp_path
    ) -> None:
        from src.evaluation.confusion_matrix import plot_and_save_stage1
        trained = _make_trained_pipeline_for_cm(fitted_hierarchical, preprocessed_arrays)
        out_path = plot_and_save_stage1(trained, output_dir=tmp_path)
        assert out_path.exists()
        assert out_path.suffix == ".png"
        assert "stage1" in out_path.name
        assert "pipelineA" in out_path.name

    def test_plot_stage2_returns_existing_png(
        self, fitted_hierarchical, preprocessed_arrays, tmp_path
    ) -> None:
        from src.evaluation.confusion_matrix import plot_and_save_stage2
        trained = _make_trained_pipeline_for_cm(fitted_hierarchical, preprocessed_arrays)
        out_path = plot_and_save_stage2(trained, output_dir=tmp_path)
        assert out_path.exists()
        assert out_path.suffix == ".png"
        assert "stage2" in out_path.name

    def test_plot_both_returns_two_paths(
        self, fitted_hierarchical, preprocessed_arrays, tmp_path
    ) -> None:
        from src.evaluation.confusion_matrix import plot_both
        trained = _make_trained_pipeline_for_cm(fitted_hierarchical, preprocessed_arrays)
        p1, p2 = plot_both(trained, output_dir=tmp_path)
        assert p1.exists()
        assert p2.exists()
        assert p1 != p2
