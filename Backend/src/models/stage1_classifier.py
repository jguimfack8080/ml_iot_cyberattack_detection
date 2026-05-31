"""
Stage 1 binary classifier: DoS/DDoS (1) vs. non-DoS/DDoS (0).

Trained on ALL instances. Separates the dominant DoS/DDoS traffic from minority classes,
structurally addressing the extreme class imbalance of CICIoT2023 without resampling.
Basis: Raturi et al. (2026, DOI: 10.1002/spy2.70220), two-stage hierarchical approach.
"""
import logging
from dataclasses import dataclass

from sklearn.ensemble import GradientBoostingClassifier

from src.data.constants import RANDOM_STATE

logger = logging.getLogger(__name__)

# Default hyperparameters — Grid Search will optimize these (see TO-DO.md P2)
# Grid: n_estimators [100, 200], max_depth [3, 5], learning_rate [0.05, 0.1], subsample [0.8, 1.0]
_GRID_SEARCH_SPACE: dict = {
    "stage1__n_estimators": [100, 200],
    "stage1__max_depth": [3, 5],
    "stage1__learning_rate": [0.05, 0.1],
    "stage1__subsample": [0.8, 1.0],
}


@dataclass
class Stage1Config:
    """Hyperparameters for the Stage 1 binary GradientBoostingClassifier."""
    n_estimators: int = 100
    max_depth: int = 3
    learning_rate: float = 0.1
    subsample: float = 1.0
    random_state: int = RANDOM_STATE


def build_stage1_classifier(config: Stage1Config | None = None) -> GradientBoostingClassifier:
    """
    Build a Stage 1 binary GradientBoostingClassifier.

    Target: is_dos_ddos (0 = non-DoS, 1 = DoS/DDoS)
    The classifier is compatible with SHAP TreeExplainer for post-hoc explanation.

    Args:
        config: Hyperparameter configuration (uses defaults if None).

    Returns:
        Unfitted GradientBoostingClassifier.
    """
    cfg = config or Stage1Config()
    clf = GradientBoostingClassifier(
        n_estimators=cfg.n_estimators,
        max_depth=cfg.max_depth,
        learning_rate=cfg.learning_rate,
        subsample=cfg.subsample,
        random_state=cfg.random_state,
    )
    logger.debug("Stage 1 classifier built: %s", clf.get_params())
    return clf


def get_grid_search_space() -> dict:
    """Return the hyperparameter grid for Grid Search on Stage 1."""
    return _GRID_SEARCH_SPACE.copy()
