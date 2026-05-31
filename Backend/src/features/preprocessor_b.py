"""
Pipeline B preprocessor: StandardScaler only, all 39 original features retained.

No dimensionality reduction — SHAP values map directly to interpretable network features
(Rate, syn_flag_number, Number, etc.), enabling semantic validation against known
attack signatures (Neto et al. 2023, DOI: 10.3390/s23135941).

CRITICAL: always call fit_transform(X_train), then transform(X_test).
"""
import logging

from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.data.constants import RANDOM_STATE

logger = logging.getLogger(__name__)


def build_preprocessor_b(random_state: int = RANDOM_STATE) -> Pipeline:
    """
    Build an unfitted Pipeline B preprocessor (StandardScaler only).

    Usage:
        preprocessor = build_preprocessor_b()
        X_train_prep = preprocessor.fit_transform(X_train)
        X_test_prep  = preprocessor.transform(X_test)

    Args:
        random_state: Kept for API symmetry with build_preprocessor_a; not used by StandardScaler.

    Returns:
        Unfitted sklearn Pipeline with step [scaler].
    """
    preprocessor = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])
    logger.debug("Preprocessor B built: StandardScaler (no PCA, 39 features retained)")
    return preprocessor
