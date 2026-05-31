"""Unit tests for src.data.loader."""
import tempfile
from pathlib import Path

import pandas as pd
import pytest

from src.data.constants import FEATURE_COLUMNS, LABEL_COL, N_FEATURES
from src.data.loader import _sample_one_file, get_feature_columns, load_stratified


def _make_csv(path: Path, rows: int = 200, labels: list[str] | None = None) -> None:
    """Create a minimal MERGED_CSV-like file with normalized column names."""
    if labels is None:
        labels = ["BENIGN", "DDOS-SYN_FLOOD", "DOS-TCP_FLOOD"]
    import numpy as np

    rng = np.random.default_rng(0)
    data = {col: rng.random(rows) for col in FEATURE_COLUMNS}
    # Simulate spaces in raw column names for 3 special columns
    if "Protocol_Type" in data:
        data["Protocol Type"] = data.pop("Protocol_Type")
    if "Tot_sum" in data:
        data["Tot sum"] = data.pop("Tot_sum")
    if "Tot_size" in data:
        data["Tot size"] = data.pop("Tot_size")
    data[LABEL_COL] = [labels[i % len(labels)] for i in range(rows)]
    pd.DataFrame(data).to_csv(path, index=False)


class TestSampleOneFile:
    def test_returns_dataframe(self, tmp_path: Path) -> None:
        csv = tmp_path / "Merged01.csv"
        _make_csv(csv)
        result = _sample_one_file(csv, n_per_class=50, random_state=42)
        assert isinstance(result, pd.DataFrame)
        assert not result.empty

    def test_respects_n_per_class(self, tmp_path: Path) -> None:
        csv = tmp_path / "Merged01.csv"
        _make_csv(csv, rows=300, labels=["BENIGN", "DDOS-SYN_FLOOD"])
        result = _sample_one_file(csv, n_per_class=10, random_state=42)
        counts = result[LABEL_COL].value_counts()
        assert counts.max() <= 10

    def test_normalizes_column_names(self, tmp_path: Path) -> None:
        csv = tmp_path / "Merged01.csv"
        _make_csv(csv)
        result = _sample_one_file(csv, n_per_class=50, random_state=42)
        assert "Protocol_Type" in result.columns
        assert "Protocol Type" not in result.columns

    def test_returns_none_on_missing_label(self, tmp_path: Path) -> None:
        csv = tmp_path / "bad.csv"
        pd.DataFrame({"A": [1, 2], "B": [3, 4]}).to_csv(csv, index=False)
        result = _sample_one_file(csv, n_per_class=50, random_state=42)
        assert result is None

    def test_reproducible_with_same_seed(self, tmp_path: Path) -> None:
        csv = tmp_path / "Merged01.csv"
        _make_csv(csv, rows=200)
        r1 = _sample_one_file(csv, n_per_class=30, random_state=42)
        r2 = _sample_one_file(csv, n_per_class=30, random_state=42)
        pd.testing.assert_frame_equal(r1.reset_index(drop=True), r2.reset_index(drop=True))


class TestLoadStratified:
    def test_loads_multiple_files(self, tmp_path: Path) -> None:
        for i in range(3):
            _make_csv(tmp_path / f"Merged0{i+1}.csv", rows=150)
        df = load_stratified(tmp_path, n_per_class_per_file=20, random_state=42)
        assert len(df) > 0
        assert LABEL_COL in df.columns

    def test_raises_on_missing_dir(self) -> None:
        with pytest.raises(FileNotFoundError):
            load_stratified("/nonexistent/path")

    def test_raises_on_no_matching_files(self, tmp_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            load_stratified(tmp_path, file_glob="Merged*.csv")

    def test_max_files_limit(self, tmp_path: Path) -> None:
        for i in range(5):
            _make_csv(tmp_path / f"Merged0{i+1}.csv", rows=100)
        df = load_stratified(tmp_path, n_per_class_per_file=10, max_files=2)
        # With 2 files × 3 labels × ≤10 rows = at most 60 rows
        assert len(df) <= 60


class TestGetFeatureColumns:
    def test_excludes_derived_columns(self) -> None:
        df = pd.DataFrame(columns=[*FEATURE_COLUMNS, LABEL_COL, "category", "is_dos_ddos"])
        cols = get_feature_columns(df)
        assert LABEL_COL not in cols
        assert "category" not in cols
        assert "is_dos_ddos" not in cols
        assert len(cols) == N_FEATURES
