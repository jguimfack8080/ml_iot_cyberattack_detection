"""
Stage 2 multiclass classifier for non-DoS/DDoS attack categories.

Target classes: {Mirai, Reconnaissance, Spoofing, Brute-Force, Web-based, Benign}.
Trained exclusively on instances that Stage 1 identifies as non-DoS/DDoS (TRUE labels,
not Stage 1 predictions — avoids train-time error propagation).
"""
import logging
from dataclasses import dataclass

from sklearn.ensemble import GradientBoostingClassifier

from src.data.constants import RANDOM_STATE, STAGE2_CATEGORIES

logger = logging.getLogger(__name__)

_GRID_SEARCH_SPACE: dict = {
    "stage2__n_estimators": [100, 200],
    "stage2__max_depth": [3, 5],
    "stage2__learning_rate": [0.05, 0.1],
    "stage2__subsample": [0.8, 1.0],
}


@dataclass
class Stage2Config:
    """Hyperparameters for the Stage 2 multiclass GradientBoostingClassifier."""
    n_estimators: int = 100
    max_depth: int = 3
    learning_rate: float = 0.1
    subsample: float = 1.0
    random_state: int = RANDOM_STATE


def build_stage2_classifier(config: Stage2Config | None = None) -> GradientBoostingClassifier:
    """
    Build a Stage 2 multiclass GradientBoostingClassifier.

    Target: category labels for non-DoS/DDoS instances (6 classes).
    scikit-learn uses one-vs-rest strategy automatically for multiclass GB.
    Compatible with SHAP TreeExplainer for per-class feature importance.

    Args:
        config: Hyperparameter configuration (uses defaults if None).

    Returns:
        Unfitted GradientBoostingClassifier.
    """
    cfg = config or Stage2Config()
    clf = GradientBoostingClassifier(
        n_estimators=cfg.n_estimators,
        max_depth=cfg.max_depth,
        learning_rate=cfg.learning_rate,
        subsample=cfg.subsample,
        random_state=cfg.random_state,
    )
    logger.debug(
        "Stage 2 classifier built (target classes: %s): %s",
        STAGE2_CATEGORIES,
        clf.get_params(),
    )
    return clf


def get_grid_search_space() -> dict:
    """Return the hyperparameter grid for Grid Search on Stage 2."""
    return _GRID_SEARCH_SPACE.copy()
