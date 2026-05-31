"""
Label mapping for CICIoT2023 MERGED_CSV.

Maps the 33 raw ALL_CAPS labels to the 8 standard categories defined by
Neto et al. (2023, DOI: 10.3390/s23135941) and adds two derived columns:
  - category    : one of {DDoS, DoS, Mirai, Reconnaissance, Spoofing,
                           Brute-Force, Web-based, Benign}
  - is_dos_ddos : binary Stage-1 target (1 = DoS or DDoS, 0 = other)

BACKDOOR_MALWARE is dropped before mapping.
Decision and justification: Backend/Done.md — Decision P1.5.
"""
import logging

import pandas as pd

from src.data.constants import (
    BINARY_COL,
    CATEGORIES,
    CATEGORY_COL,
    DOS_DDOS_CATEGORIES,
    EXCLUDED_LABELS,
    LABEL_COL,
    LABEL_TO_CATEGORY,
    STAGE2_CATEGORIES,
)

logger = logging.getLogger(__name__)


def apply_label_mapping(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop excluded labels, map raw labels to 8 categories, add binary Stage-1 column.

    Args:
        df: DataFrame with at least a 'Label' column (raw ALL_CAPS labels).

    Returns:
        New DataFrame (copy) with two additional columns:
          - category    : str, one of the 8 standard attack categories
          - is_dos_ddos : int (0 or 1), Stage-1 binary target

    Raises:
        ValueError: If unknown labels are found that are not in LABEL_TO_CATEGORY
                    and not in EXCLUDED_LABELS.
    """
    initial_len = len(df)

    # Step 1: drop excluded labels (BACKDOOR_MALWARE)
    df = df[~df[LABEL_COL].isin(EXCLUDED_LABELS)].copy()
    dropped = initial_len - len(df)
    if dropped > 0:
        logger.info(
            "Dropped %d rows with excluded labels (%s)",
            dropped,
            ", ".join(sorted(EXCLUDED_LABELS)),
        )

    # Step 2: validate — fail fast on unknown labels
    unknown = set(df[LABEL_COL].unique()) - set(LABEL_TO_CATEGORY)
    if unknown:
        raise ValueError(
            f"Unknown labels found (not in LABEL_TO_CATEGORY and not excluded): {sorted(unknown)}"
        )

    # Step 3: map raw label → category
    df[CATEGORY_COL] = df[LABEL_COL].map(LABEL_TO_CATEGORY)

    # Step 4: binary Stage-1 target
    df[BINARY_COL] = df[CATEGORY_COL].isin(DOS_DDOS_CATEGORIES).astype(int)

    _log_distribution(df)
    return df


def _log_distribution(df: pd.DataFrame) -> None:
    """Log per-category and Stage-1 counts for traceability."""
    cat_counts = df[CATEGORY_COL].value_counts()
    dos_count = int(df[BINARY_COL].sum())
    non_dos_count = len(df) - dos_count

    logger.info(
        "Label mapping complete: %d rows | %d categories | "
        "Stage-1: %d DoS/DDoS (%.1f%%) vs %d non-DoS (%.1f%%)",
        len(df),
        df[CATEGORY_COL].nunique(),
        dos_count,
        100 * dos_count / len(df),
        non_dos_count,
        100 * non_dos_count / len(df),
    )
    for cat in CATEGORIES:
        n = cat_counts.get(cat, 0)
        logger.debug("  %-16s : %7d rows (%.2f%%)", cat, n, 100 * n / len(df))


def get_stage2_mask(df: pd.DataFrame) -> pd.Series:
    """Return boolean mask for rows that belong to Stage-2 (non-DoS/DDoS)."""
    return df[BINARY_COL] == 0


def validate_split_labels(y_train: pd.Series, y_test: pd.Series) -> None:
    """
    Assert that all categories present in y_test also appear in y_train.

    Ensures the stratified split did not create unseen classes at test time,
    which would break classifier evaluation. Raises ValueError if violated.
    """
    train_labels = set(y_train.unique())
    test_labels = set(y_test.unique())
    unseen = test_labels - train_labels
    if unseen:
        raise ValueError(
            f"Test set contains {len(unseen)} label(s) not seen during training: {sorted(unseen)}"
        )
