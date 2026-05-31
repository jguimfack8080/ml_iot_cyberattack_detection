"""
Pipeline A preprocessor: StandardScaler → PCA (39 → 16 components).

Replicates the preprocessing approach of Raturi et al. (2026, DOI: 10.1002/spy2.70220).
CRITICAL: always call fit_transform(X_train), then transform(X_test) — never fit on test data.
"""
import logging

from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.data.constants import N_PCA_COMPONENTS, RANDOM_STATE

logger = logging.getLogger(__name__)


def build_preprocessor_a(
    n_components: int = N_PCA_COMPONENTS,
    random_state: int = RANDOM_STATE,
) -> Pipeline:
    """
    Build an unfitted Pipeline A preprocessor (StandardScaler + PCA).

    Usage:
        preprocessor = build_preprocessor_a()
        X_train_prep = preprocessor.fit_transform(X_train)  # fit on train only
        X_test_prep  = preprocessor.transform(X_test)       # transform only

    Args:
        n_components: Number of PCA output dimensions (default 16 = Raturi et al. 2026).
        random_state: Seed for PCA's SVD randomized solver.

    Returns:
        Unfitted sklearn Pipeline with steps [scaler, pca].
    """
    # SimpleImputer fills NaN/inf (replaced by loader) with column median.
    # Fit on train only — prevents data leakage from test to train.
    preprocessor = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
        ("pca", PCA(n_components=n_components, random_state=random_state)),
    ])
    logger.debug(
        "Preprocessor A built: StandardScaler → PCA(n_components=%d, random_state=%d)",
        n_components,
        random_state,
    )
    return preprocessor


def get_explained_variance_ratio(preprocessor: Pipeline) -> float:
    """
    Return the cumulative explained variance ratio of the fitted PCA step.
    Requires the preprocessor to have been fitted first.
    """
    pca: PCA = preprocessor.named_steps["pca"]
    ratio = float(pca.explained_variance_ratio_.sum())
    logger.info("PCA cumulative explained variance: %.4f (%.1f%%)", ratio, ratio * 100)
    return ratio
