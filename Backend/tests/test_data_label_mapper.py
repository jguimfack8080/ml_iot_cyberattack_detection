"""Unit tests for src.data.label_mapper."""
import pandas as pd
import pytest

from src.data.constants import (
    BINARY_COL,
    CATEGORIES,
    CATEGORY_COL,
    EXCLUDED_LABELS,
    LABEL_COL,
    LABEL_TO_CATEGORY,
)
from src.data.label_mapper import (
    apply_label_mapping,
    get_stage2_mask,
    validate_split_labels,
)


def _make_df(labels: list[str]) -> pd.DataFrame:
    """Create minimal DataFrame with Label column."""
    import numpy as np
    rng = np.random.default_rng(0)
    return pd.DataFrame({
        "feature_1": rng.random(len(labels)),
        "feature_2": rng.random(len(labels)),
        LABEL_COL: labels,
    })


class TestApplyLabelMapping:
    def test_adds_category_and_binary_columns(self) -> None:
        df = _make_df(["BENIGN", "DDOS-SYN_FLOOD", "DOS-TCP_FLOOD"])
        result = apply_label_mapping(df)
        assert CATEGORY_COL in result.columns
        assert BINARY_COL in result.columns

    def test_all_known_labels_mapped(self) -> None:
        labels = list(LABEL_TO_CATEGORY.keys())
        df = _make_df(labels)
        result = apply_label_mapping(df)
        assert result[CATEGORY_COL].isna().sum() == 0

    def test_drops_excluded_labels(self) -> None:
        labels = ["BENIGN", "BACKDOOR_MALWARE", "DDOS-SYN_FLOOD"]
        df = _make_df(labels)
        result = apply_label_mapping(df)
        assert "BACKDOOR_MALWARE" not in result[LABEL_COL].values
        assert len(result) == 2  # only BENIGN and DDOS-SYN_FLOOD remain

    def test_binary_column_correct_for_dos_ddos(self) -> None:
        df = _make_df(["DDOS-SYN_FLOOD", "DOS-TCP_FLOOD", "BENIGN", "MIRAI-UDPPLAIN"])
        result = apply_label_mapping(df)
        assert result.loc[result[LABEL_COL] == "DDOS-SYN_FLOOD", BINARY_COL].iloc[0] == 1
        assert result.loc[result[LABEL_COL] == "DOS-TCP_FLOOD", BINARY_COL].iloc[0] == 1
        assert result.loc[result[LABEL_COL] == "BENIGN", BINARY_COL].iloc[0] == 0
        assert result.loc[result[LABEL_COL] == "MIRAI-UDPPLAIN", BINARY_COL].iloc[0] == 0

    def test_raises_on_unknown_label(self) -> None:
        df = _make_df(["BENIGN", "UNKNOWN_ATTACK_TYPE"])
        with pytest.raises(ValueError, match="Unknown labels"):
            apply_label_mapping(df)

    def test_does_not_mutate_input(self) -> None:
        df = _make_df(["BENIGN", "DDOS-SYN_FLOOD"])
        original_cols = list(df.columns)
        apply_label_mapping(df)
        assert list(df.columns) == original_cols

    def test_all_8_categories_reachable(self) -> None:
        labels = list(LABEL_TO_CATEGORY.keys())
        df = _make_df(labels)
        result = apply_label_mapping(df)
        found_categories = set(result[CATEGORY_COL].unique())
        assert found_categories == set(CATEGORIES)


class TestGetStage2Mask:
    def test_selects_non_dos_rows(self) -> None:
        df = _make_df(["BENIGN", "DDOS-SYN_FLOOD", "MIRAI-UDPPLAIN"])
        df = apply_label_mapping(df)
        mask = get_stage2_mask(df)
        assert mask.sum() == 2  # BENIGN and MIRAI are non-DoS/DDoS


class TestValidateSplitLabels:
    def test_passes_when_all_test_labels_in_train(self) -> None:
        y_train = pd.Series(["DDoS", "DoS", "Benign", "Mirai"])
        y_test = pd.Series(["DDoS", "Benign"])
        validate_split_labels(y_train, y_test)  # should not raise

    def test_raises_on_unseen_test_label(self) -> None:
        y_train = pd.Series(["DDoS", "Benign"])
        y_test = pd.Series(["DDoS", "Spoofing"])  # Spoofing not in train
        with pytest.raises(ValueError, match="not seen during training"):
            validate_split_labels(y_train, y_test)
