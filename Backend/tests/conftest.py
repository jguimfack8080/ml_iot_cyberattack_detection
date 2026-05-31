"""
Shared pytest fixtures for all tests.

All fixtures use synthetic data — no dependency on the real 8.5 GB dataset.
Fixtures follow the CICIoT2023 structure: 39 float features + Label column.
"""
import matplotlib
matplotlib.use("Agg")  # non-interactive backend for headless test environments

import numpy as np
import pandas as pd
import pytest

from src.data.constants import (
    BINARY_COL,
    CATEGORY_COL,
    FEATURE_COLUMNS,
    LABEL_COL,
    LABEL_TO_CATEGORY,
    RANDOM_STATE,
)
from src.data.label_mapper import apply_label_mapping

# Representative labels covering all 8 categories
_REPRESENTATIVE_LABELS = [
    "DDOS-SYN_FLOOD",       # DDoS
    "DDOS-UDP_FLOOD",       # DDoS
    "DOS-TCP_FLOOD",        # DoS
    "DOS-SYN_FLOOD",        # DoS
    "MIRAI-UDPPLAIN",       # Mirai
    "RECON-PORTSCAN",       # Reconnaissance
    "VULNERABILITYSCAN",    # Reconnaissance
    "MITM-ARPSPOOFING",     # Spoofing
    "DICTIONARYBRUTEFORCE", # Brute-Force
    "XSS",                  # Web-based
    "COMMANDINJECTION",     # Web-based
    "BENIGN",               # Benign
]

_N_ROWS_PER_LABEL = 20  # 12 labels × 20 = 240 rows total — fast enough for tests


@pytest.fixture(scope="session")
def sample_df() -> pd.DataFrame:
    """
    Small DataFrame with all 8 categories and 39 normalized feature columns.
    No dependency on MERGED_CSV — entirely synthetic.
    """
    rng = np.random.default_rng(RANDOM_STATE)
    rows = []
    for label in _REPRESENTATIVE_LABELS:
        data = {col: rng.random(_N_ROWS_PER_LABEL) for col in FEATURE_COLUMNS}
        data[LABEL_COL] = label
        rows.append(pd.DataFrame(data))
    return pd.concat(rows, ignore_index=True)


@pytest.fixture(scope="session")
def mapped_df(sample_df: pd.DataFrame) -> pd.DataFrame:
    """sample_df after apply_label_mapping() — has 'category' and 'is_dos_ddos' columns."""
    return apply_label_mapping(sample_df)


@pytest.fixture(scope="session")
def split_arrays(mapped_df: pd.DataFrame):
    """
    Pre-split arrays for testing classifiers without data loading.
    Returns (X_train, X_test, y_bin_train, y_bin_test, y_cat_train, y_cat_test).
    """
    from sklearn.model_selection import train_test_split

    X = mapped_df[list(FEATURE_COLUMNS)].astype(float).to_numpy()
    y_binary = mapped_df[BINARY_COL].to_numpy(dtype=int)
    y_category = mapped_df[CATEGORY_COL].to_numpy(dtype=str)

    return train_test_split(
        X, y_binary, y_category,
        test_size=0.2,
        stratify=y_category,
        random_state=RANDOM_STATE,
    )


@pytest.fixture(scope="session")
def preprocessed_arrays(split_arrays):
    """
    Pre-split and pre-preprocessed arrays using Preprocessor A.
    Returns (X_train_prep, X_test_prep, y_bin_train, y_bin_test, y_cat_train, y_cat_test).
    """
    from src.features.preprocessor_a import build_preprocessor_a

    X_train, X_test, y_bin_train, y_bin_test, y_cat_train, y_cat_test = split_arrays
    preprocessor = build_preprocessor_a()
    X_train_prep = preprocessor.fit_transform(X_train)
    X_test_prep = preprocessor.transform(X_test)
    return X_train_prep, X_test_prep, y_bin_train, y_bin_test, y_cat_train, y_cat_test


@pytest.fixture(scope="session")
def fitted_hierarchical(preprocessed_arrays):
    """Fitted HierarchicalClassifier on preprocessed synthetic data."""
    from src.models.hierarchical_classifier import HierarchicalClassifier
    from src.models.stage1_classifier import build_stage1_classifier
    from src.models.stage2_classifier import build_stage2_classifier

    X_train, _, y_bin_train, _, y_cat_train, _ = preprocessed_arrays
    clf = HierarchicalClassifier(
        stage1=build_stage1_classifier(),
        stage2=build_stage2_classifier(),
    )
    clf.fit(X_train, y_bin_train, y_cat_train)
    return clf
