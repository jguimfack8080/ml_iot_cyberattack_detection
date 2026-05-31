"""
Stratified sampler for CICIoT2023 MERGED_CSV files.

Strategy: read each of the 63 files completely (one at a time, ~140 MB each),
sample up to N rows per label, then discard the full file from memory.
This guarantees:
  - Every row in every file is seen before sampling (no information loss)
  - RAM usage stays bounded: ~235 MB per file + growing sample accumulator
  - Full reproducibility via random_state=42

Memory budget (worst case):
  one file (~235 MB) + accumulated samples (~333 MB) ≈ 570 MB peak.
"""
import gc
import logging
from pathlib import Path
from typing import Optional

import pandas as pd
from tqdm import tqdm

from src.data.constants import (
    FEATURE_COLUMNS,
    FEATURE_COLUMNS_RAW,
    LABEL_COL,
    RANDOM_STATE,
)

logger = logging.getLogger(__name__)

# Default: 500 rows per label per file
# 500 × 33 labels × 63 files ≈ 1 039 500 rows total, ~333 MB RAM
_DEFAULT_N_PER_CLASS: int = 500
_FILE_GLOB: str = "Merged*.csv"

# Map raw column names (with spaces) to normalized names (underscores)
_COLUMN_RENAME: dict[str, str] = {
    raw: norm
    for raw, norm in zip(FEATURE_COLUMNS_RAW, FEATURE_COLUMNS)
    if raw != norm
}


def load_stratified(
    data_dir: str | Path,
    n_per_class_per_file: int = _DEFAULT_N_PER_CLASS,
    random_state: int = RANDOM_STATE,
    file_glob: str = _FILE_GLOB,
    max_files: Optional[int] = None,
) -> pd.DataFrame:
    """
    Load a stratified sample from all MERGED_CSV files.

    Reads every file in sorted order, samples up to n_per_class_per_file rows
    per label from each file, then frees the file from memory before proceeding.
    Column names containing spaces are normalized to underscores.

    Args:
        data_dir: Path to the MERGED_CSV directory.
        n_per_class_per_file: Max rows sampled per label per file.
        random_state: Seed for pandas .sample() — ensures reproducibility.
        file_glob: Glob pattern to match CSV files inside data_dir.
        max_files: If set, process only the first N files (useful for quick testing).

    Returns:
        DataFrame with normalized feature columns + Label column.

    Raises:
        FileNotFoundError: If data_dir does not exist or no matching files found.
        ValueError: If a file has no Label column.
    """
    data_dir = Path(data_dir)
    if not data_dir.is_dir():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    csv_files = sorted(data_dir.glob(file_glob))
    if not csv_files:
        raise FileNotFoundError(
            f"No files matching '{file_glob}' found in {data_dir}"
        )
    if max_files is not None:
        csv_files = csv_files[:max_files]

    logger.info(
        "Starting stratified load: %d files, %d rows/class/file, random_state=%d",
        len(csv_files),
        n_per_class_per_file,
        random_state,
    )

    file_samples: list[pd.DataFrame] = []
    total_rows_seen = 0

    for path in tqdm(csv_files, desc="Loading MERGED_CSV", unit="file"):
        sample = _sample_one_file(path, n_per_class_per_file, random_state)
        if sample is not None:
            total_rows_seen += len(sample)
            file_samples.append(sample)
        gc.collect()

    if not file_samples:
        raise ValueError("No data could be loaded from any file.")

    result = pd.concat(file_samples, ignore_index=True)
    logger.info(
        "Loaded %d rows from %d files (%d labels, %d features)",
        len(result),
        len(csv_files),
        result[LABEL_COL].nunique(),
        len(FEATURE_COLUMNS),
    )
    return result


def _sample_one_file(
    path: Path,
    n_per_class: int,
    random_state: int,
) -> pd.DataFrame | None:
    """
    Read one CSV file completely, sample up to n_per_class rows per label.

    Reads the full file into memory (~235 MB for a 140 MB CSV), groups by Label,
    and takes a deterministic sample from each group. The full DataFrame is freed
    after sampling; only the sample (~16 500 rows) is returned.

    Returns None if the file has no Label column or is empty.
    """
    try:
        df = pd.read_csv(path, low_memory=False)
    except Exception as exc:
        logger.warning("Could not read %s: %s — skipping", path.name, exc)
        return None

    if LABEL_COL not in df.columns:
        logger.warning("No '%s' column in %s — skipping", LABEL_COL, path.name)
        return None

    if df.empty:
        logger.warning("Empty file: %s — skipping", path.name)
        return None

    # Normalize column names: 'Protocol Type' → 'Protocol_Type', etc.
    if _COLUMN_RENAME:
        df = df.rename(columns=_COLUMN_RENAME)

    # Replace inf/-inf with NaN — real CICIoT2023 data contains inf values
    # (imputation with median is done in the preprocessor, fit on train only)
    df = df.replace([float("inf"), float("-inf")], float("nan"))

    # Sample up to n_per_class rows per label (deterministic)
    sampled_parts: list[pd.DataFrame] = []
    for label, group in df.groupby(LABEL_COL, sort=False):
        n = min(n_per_class, len(group))
        sampled_parts.append(
            group.sample(n=n, random_state=random_state, replace=False)
        )

    del df  # free full file from memory immediately
    gc.collect()

    return pd.concat(sampled_parts, ignore_index=True)


def get_feature_columns(df: pd.DataFrame) -> list[str]:
    """Return the feature column names present in df (excludes Label and derived columns)."""
    exclude = {LABEL_COL, "category", "is_dos_ddos"}
    return [c for c in df.columns if c not in exclude]
