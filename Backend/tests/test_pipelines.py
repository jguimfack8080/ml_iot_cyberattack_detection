"""
Integration tests for Pipeline A and Pipeline B.

These tests use synthetic in-memory data (no dependency on MERGED_CSV).
They test the full pipeline flow: mapping → splitting → preprocessing → training → metrics.
"""
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from src.data.constants import FEATURE_COLUMNS, LABEL_COL, RANDOM_STATE
from src.pipelines._core import PipelineConfig, TrainedPipeline
from src.pipelines.pipeline_a import run_pipeline_a
from src.pipelines.pipeline_b import run_pipeline_b


def _write_synthetic_merged_csv(path: Path, n_per_label: int = 30) -> None:
    """Write a synthetic MERGED_CSV-like file covering all 8 categories."""
    labels = [
        "DDOS-SYN_FLOOD", "DDOS-UDP_FLOOD",    # DDoS
        "DOS-TCP_FLOOD", "DOS-SYN_FLOOD",        # DoS
        "MIRAI-UDPPLAIN",                         # Mirai
        "RECON-PORTSCAN",                         # Reconnaissance
        "MITM-ARPSPOOFING",                       # Spoofing
        "DICTIONARYBRUTEFORCE",                   # Brute-Force
        "XSS",                                    # Web-based
        "BENIGN",                                 # Benign
    ]
    rng = np.random.default_rng(RANDOM_STATE)
    rows = []
    for label in labels:
        data = {col: rng.random(n_per_label) for col in FEATURE_COLUMNS}
        data[LABEL_COL] = label
        rows.append(pd.DataFrame(data))
    pd.concat(rows, ignore_index=True).to_csv(path, index=False)


@pytest.fixture(scope="module")
def synthetic_data_dir(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """Create 3 synthetic MERGED_CSV-like files in a temp directory."""
    d = tmp_path_factory.mktemp("merged_csv")
    for i in range(1, 4):
        _write_synthetic_merged_csv(d / f"Merged0{i}.csv", n_per_label=30)
    return d


@pytest.fixture(scope="module")
def minimal_config(synthetic_data_dir: Path) -> PipelineConfig:
    """Minimal PipelineConfig for integration tests (tiny data, fast training)."""
    return PipelineConfig(
        data_dir=synthetic_data_dir,
        n_per_class_per_file=30,
        test_size=0.2,
        random_state=RANDOM_STATE,
        max_files=3,
    )


class TestPipelineA:
    def test_returns_trained_pipeline(self, minimal_config: PipelineConfig) -> None:
        result = run_pipeline_a(minimal_config)
        assert isinstance(result, TrainedPipeline)

    def test_pipeline_name_is_a(self, minimal_config: PipelineConfig) -> None:
        result = run_pipeline_a(minimal_config)
        assert result.pipeline_name == "A"

    def test_x_test_has_pca_dimensions(self, minimal_config: PipelineConfig) -> None:
        result = run_pipeline_a(minimal_config)
        assert result.X_test.shape[1] == minimal_config.n_pca_components

    def test_balanced_accuracy_stage1_in_valid_range(self, minimal_config: PipelineConfig) -> None:
        result = run_pipeline_a(minimal_config)
        assert 0.0 <= result.balanced_accuracy_stage1 <= 1.0

    def test_balanced_accuracy_stage2_in_valid_range(self, minimal_config: PipelineConfig) -> None:
        result = run_pipeline_a(minimal_config)
        assert 0.0 <= result.balanced_accuracy_stage2 <= 1.0

    def test_classifier_is_fitted(self, minimal_config: PipelineConfig) -> None:
        result = run_pipeline_a(minimal_config)
        assert result.classifier.is_fitted

    def test_feature_names_in_has_39_entries(self, minimal_config: PipelineConfig) -> None:
        result = run_pipeline_a(minimal_config)
        assert len(result.feature_names_in) == 39

    def test_training_time_positive(self, minimal_config: PipelineConfig) -> None:
        result = run_pipeline_a(minimal_config)
        assert result.training_time_seconds > 0.0


class TestPipelineB:
    def test_returns_trained_pipeline(self, minimal_config: PipelineConfig) -> None:
        result = run_pipeline_b(minimal_config)
        assert isinstance(result, TrainedPipeline)

    def test_pipeline_name_is_b(self, minimal_config: PipelineConfig) -> None:
        result = run_pipeline_b(minimal_config)
        assert result.pipeline_name == "B"

    def test_x_test_has_all_39_features(self, minimal_config: PipelineConfig) -> None:
        result = run_pipeline_b(minimal_config)
        assert result.X_test.shape[1] == 39

    def test_balanced_accuracy_in_valid_range(self, minimal_config: PipelineConfig) -> None:
        result = run_pipeline_b(minimal_config)
        assert 0.0 <= result.balanced_accuracy_stage1 <= 1.0
        assert 0.0 <= result.balanced_accuracy_stage2 <= 1.0


class TestPipelineAvsB:
    def test_a_output_narrower_than_b(self, minimal_config: PipelineConfig) -> None:
        """Pipeline A compresses features via PCA; Pipeline B keeps all 39."""
        result_a = run_pipeline_a(minimal_config)
        result_b = run_pipeline_b(minimal_config)
        assert result_a.X_test.shape[1] < result_b.X_test.shape[1]

    def test_both_have_same_test_set_size(self, minimal_config: PipelineConfig) -> None:
        """Both pipelines use the same data split (same random_state)."""
        result_a = run_pipeline_a(minimal_config)
        result_b = run_pipeline_b(minimal_config)
        assert len(result_a.y_binary_test) == len(result_b.y_binary_test)
