"""
Shared pipeline logic for Pipeline A and Pipeline B.

Both pipelines follow the same flow — they differ only in the preprocessor step:
  Pipeline A: StandardScaler → PCA (39 → 16)
  Pipeline B: StandardScaler only (39 features)

This module contains the shared data loading, splitting, training, and evaluation logic
to avoid code duplication (DRY principle).
"""
import logging
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import balanced_accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from src.data.constants import (
    BINARY_COL,
    CATEGORY_COL,
    FEATURE_COLUMNS,
    RANDOM_STATE,
    N_PCA_COMPONENTS,
)
from src.data.label_mapper import apply_label_mapping, validate_split_labels
from src.data.loader import load_stratified
from src.models.hierarchical_classifier import HierarchicalClassifier
from src.models.stage1_classifier import Stage1Config, build_stage1_classifier
from src.models.stage2_classifier import Stage2Config, build_stage2_classifier

logger = logging.getLogger(__name__)


@dataclass
class PipelineConfig:
    """
    Configuration for a complete training pipeline run.

    Attributes:
        data_dir: Path to the MERGED_CSV directory.
        n_per_class_per_file: Rows sampled per label per CSV file.
        test_size: Fraction of data used for test set.
        random_state: Seed for all stochastic operations.
        stage1_config: Hyperparameters for Stage 1 classifier (None = defaults).
        stage2_config: Hyperparameters for Stage 2 classifier (None = defaults).
        n_pca_components: PCA output dimensions (Pipeline A only; ignored by B).
        max_files: Limit files loaded (None = all 63; set to small int for testing).
    """
    data_dir: Path | str
    n_per_class_per_file: int = 500
    test_size: float = 0.2
    random_state: int = RANDOM_STATE
    stage1_config: Stage1Config | None = None
    stage2_config: Stage2Config | None = None
    n_pca_components: int = N_PCA_COMPONENTS
    max_files: int | None = None


@dataclass
class TrainedPipeline:
    """
    Output of a completed pipeline run.

    Contains everything needed for evaluation (P4) and SHAP analysis (P4):
      - Fitted preprocessor and classifier
      - Held-out test data (preprocessed)
      - Ground-truth test labels
      - Training metadata
    """
    pipeline_name: str                    # "A" or "B"
    preprocessor: Pipeline                # Fitted sklearn Pipeline
    classifier: HierarchicalClassifier   # Fitted hierarchical classifier
    X_test: np.ndarray                   # Preprocessed test features
    y_binary_test: np.ndarray            # Binary Stage 1 ground truth
    y_category_test: np.ndarray          # Category ground truth (Stage 2 + DoS/DDoS)
    feature_names_in: list[str]          # Feature names before preprocessing
    config: PipelineConfig
    # Basic metrics logged at training time
    balanced_accuracy_stage1: float = 0.0
    balanced_accuracy_stage2: float = 0.0
    f1_macro_stage1: float = 0.0
    f1_macro_stage2: float = 0.0
    training_time_seconds: float = 0.0


def run_pipeline(
    config: PipelineConfig,
    preprocessor: Pipeline,
    pipeline_name: str,
) -> TrainedPipeline:
    """
    Execute the full training pipeline: load → map → split → preprocess → train → evaluate.

    Args:
        config: Pipeline configuration (data dir, sample size, hyperparams, etc.).
        preprocessor: Unfitted sklearn Pipeline (preprocessor_a or preprocessor_b).
        pipeline_name: Label for logging and result identification ("A" or "B").

    Returns:
        TrainedPipeline with fitted components and test data for evaluation.
    """
    logger.info("=" * 60)
    logger.info("Pipeline %s — starting", pipeline_name)
    logger.info("=" * 60)
    t_start = time.perf_counter()

    # ------------------------------------------------------------------
    # Step 1: Load data from MERGED_CSV
    # ------------------------------------------------------------------
    logger.info("[1/7] Loading data from %s ...", config.data_dir)
    df = load_stratified(
        data_dir=config.data_dir,
        n_per_class_per_file=config.n_per_class_per_file,
        random_state=config.random_state,
        max_files=config.max_files,
    )
    logger.info("      %d rows loaded.", len(df))

    # ------------------------------------------------------------------
    # Step 2: Map labels → 8 categories + binary target
    # ------------------------------------------------------------------
    logger.info("[2/7] Applying label mapping...")
    df = apply_label_mapping(df)

    # ------------------------------------------------------------------
    # Step 3: Extract features and targets
    # ------------------------------------------------------------------
    logger.info("[3/7] Extracting features and targets...")
    X = df[list(FEATURE_COLUMNS)].astype(float).to_numpy()
    y_binary = df[BINARY_COL].to_numpy(dtype=int)
    y_category = df[CATEGORY_COL].to_numpy(dtype=str)

    # ------------------------------------------------------------------
    # Step 4: Stratified 80/20 train/test split
    # ------------------------------------------------------------------
    logger.info("[4/7] Splitting 80/20 stratified by category...")
    X_train, X_test, y_bin_train, y_bin_test, y_cat_train, y_cat_test = (
        train_test_split(
            X, y_binary, y_category,
            test_size=config.test_size,
            stratify=y_category,
            random_state=config.random_state,
        )
    )
    validate_split_labels(pd.Series(y_cat_train), pd.Series(y_cat_test))
    logger.info(
        "      Train: %d | Test: %d | Stage-1 pos rate in train: %.1f%%",
        len(X_train),
        len(X_test),
        100 * y_bin_train.mean(),
    )

    # ------------------------------------------------------------------
    # Step 5: Preprocess (fit on train ONLY — no data leakage)
    # ------------------------------------------------------------------
    logger.info("[5/7] Preprocessing (fit on train only)...")
    X_train_prep = preprocessor.fit_transform(X_train)
    X_test_prep = preprocessor.transform(X_test)
    logger.info(
        "      Input shape: %s → Output shape: %s",
        X_train.shape,
        X_train_prep.shape,
    )

    # ------------------------------------------------------------------
    # Step 6: Build and fit hierarchical classifier
    # ------------------------------------------------------------------
    logger.info("[6/7] Training hierarchical classifier (Stage 1 + Stage 2)...")
    clf = HierarchicalClassifier(
        stage1=build_stage1_classifier(config.stage1_config),
        stage2=build_stage2_classifier(config.stage2_config),
    )
    clf.fit(X_train_prep, y_bin_train, y_cat_train)

    # ------------------------------------------------------------------
    # Step 7: Basic metrics (detailed metrics are P4 — evaluation module)
    # ------------------------------------------------------------------
    logger.info("[7/7] Computing basic metrics...")
    ba1, f1_1, ba2, f1_2 = _compute_basic_metrics(
        clf, X_test_prep, y_bin_test, y_cat_test
    )

    t_elapsed = time.perf_counter() - t_start
    logger.info("Pipeline %s complete in %.1f seconds.", pipeline_name, t_elapsed)
    logger.info("  Stage 1 — Balanced Accuracy: %.4f | F1-macro: %.4f", ba1, f1_1)
    logger.info("  Stage 2 — Balanced Accuracy: %.4f | F1-macro: %.4f", ba2, f1_2)

    return TrainedPipeline(
        pipeline_name=pipeline_name,
        preprocessor=preprocessor,
        classifier=clf,
        X_test=X_test_prep,
        y_binary_test=y_bin_test,
        y_category_test=y_cat_test,
        feature_names_in=list(FEATURE_COLUMNS),
        config=config,
        balanced_accuracy_stage1=ba1,
        balanced_accuracy_stage2=ba2,
        f1_macro_stage1=f1_1,
        f1_macro_stage2=f1_2,
        training_time_seconds=t_elapsed,
    )


def _compute_basic_metrics(
    clf: HierarchicalClassifier,
    X_test: np.ndarray,
    y_bin_test: np.ndarray,
    y_cat_test: np.ndarray,
) -> tuple[float, float, float, float]:
    """
    Compute Stage 1 and Stage 2 Balanced Accuracy and F1-macro on the test set.

    Returns:
        (ba_stage1, f1_stage1, ba_stage2, f1_stage2)
    """
    # Stage 1 metrics
    s1_pred = clf.predict_stage1(X_test)
    ba1 = balanced_accuracy_score(y_bin_test, s1_pred)
    f1_1 = f1_score(y_bin_test, s1_pred, average="macro")

    # Stage 2 metrics — evaluate only on true non-DoS instances
    non_dos_mask = y_bin_test == 0
    if non_dos_mask.sum() < 2:
        logger.warning("Too few non-DoS test instances for Stage 2 evaluation.")
        return ba1, f1_1, 0.0, 0.0

    s2_pred = clf.predict_stage2(X_test[non_dos_mask])
    ba2 = balanced_accuracy_score(y_cat_test[non_dos_mask], s2_pred)
    f1_2 = f1_score(y_cat_test[non_dos_mask], s2_pred, average="macro", zero_division=0)

    return ba1, f1_1, ba2, f1_2
