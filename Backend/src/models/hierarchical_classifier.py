"""
Two-stage hierarchical classifier for CICIoT2023 IoT intrusion detection.

Architecture (Raturi et al. 2026, DOI: 10.1002/spy2.70220):

  Stage 1 — Binary:     all instances → DoS/DDoS (1) or non-DoS (0)
  Stage 2 — Multiclass: non-DoS instances → {Mirai, Reconnaissance, Spoofing,
                                               Brute-Force, Web-based, Benign}

Training rule:
  Stage 1 is trained on ALL training instances.
  Stage 2 is trained on TRUE non-DoS training instances only (uses ground-truth labels,
  not Stage 1 predictions, to prevent train-time error propagation from Stage 1 mistakes).

Prediction rule:
  - Stage 1 = 1 (DoS/DDoS) → final label "DoS/DDoS"
  - Stage 1 = 0 (non-DoS)  → Stage 2 predicts the specific category

SHAP usage:
  Access clf.stage1 and clf.stage2 directly for TreeExplainer:
    shap.TreeExplainer(clf.stage1)  # binary SHAP
    shap.TreeExplainer(clf.stage2)  # multiclass SHAP
"""
import logging

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier

logger = logging.getLogger(__name__)

_DOS_DDOS_LABEL = "DoS/DDoS"


class HierarchicalClassifier:
    """
    Hierarchical two-stage Gradient Boosting classifier for IoT IDS.

    Attributes:
        stage1: Fitted binary GradientBoostingClassifier (DoS/DDoS vs. non-DoS).
        stage2: Fitted multiclass GradientBoostingClassifier (6 non-DoS categories).
    """

    def __init__(
        self,
        stage1: GradientBoostingClassifier,
        stage2: GradientBoostingClassifier,
    ) -> None:
        self.stage1 = stage1
        self.stage2 = stage2
        self._is_fitted = False

    def fit(
        self,
        X: np.ndarray,
        y_binary: np.ndarray,
        y_category: np.ndarray,
    ) -> "HierarchicalClassifier":
        """
        Fit Stage 1 on all data, Stage 2 on true non-DoS/DDoS instances.

        Args:
            X: Feature matrix (preprocessed), shape (n_samples, n_features).
            y_binary: Binary labels — 1 for DoS/DDoS, 0 for non-DoS (Stage 1 target).
            y_category: Category string labels for Stage 2 non-DoS instances.

        Returns:
            self (fitted).

        Raises:
            ValueError: If no non-DoS/DDoS instances exist for Stage 2 training.
        """
        # --- Pre-flight validation ---
        non_dos_mask = y_binary == 0
        if not non_dos_mask.any():
            raise ValueError(
                "No non-DoS/DDoS instances found in training data. "
                "Stage 2 cannot be trained."
            )
        if len(np.unique(y_binary)) < 2:
            raise ValueError(
                "Stage 1 requires at least 2 classes (0=non-DoS, 1=DoS/DDoS). "
                f"Only class(es) present: {np.unique(y_binary).tolist()}"
            )

        # --- Stage 1: train on all instances ---
        logger.info(
            "Fitting Stage 1 on %d instances (%d DoS/DDoS, %d non-DoS)...",
            len(X),
            int(y_binary.sum()),
            int((y_binary == 0).sum()),
        )
        self.stage1.fit(X, y_binary)

        # --- Stage 2: train on TRUE non-DoS instances ---
        X_stage2 = X[non_dos_mask]
        y_stage2 = y_category[non_dos_mask]
        logger.info(
            "Fitting Stage 2 on %d non-DoS instances (%d unique categories)...",
            len(X_stage2),
            len(np.unique(y_stage2)),
        )
        self.stage2.fit(X_stage2, y_stage2)

        self._is_fitted = True
        logger.info("HierarchicalClassifier fitted successfully.")
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Two-stage prediction: Stage 1 filters DoS/DDoS, Stage 2 classifies the rest.

        Args:
            X: Feature matrix (preprocessed), shape (n_samples, n_features).

        Returns:
            1-D array of predicted category strings.
            DoS/DDoS instances → "DoS/DDoS".
            Non-DoS instances → one of {Mirai, Reconnaissance, Spoofing,
                                         Brute-Force, Web-based, Benign}.
        """
        stage1_pred = self.stage1.predict(X)
        final_pred = np.full(len(X), _DOS_DDOS_LABEL, dtype=object)

        non_dos_mask = stage1_pred == 0
        if non_dos_mask.any():
            final_pred[non_dos_mask] = self.stage2.predict(X[non_dos_mask])

        return final_pred

    def predict_stage1(self, X: np.ndarray) -> np.ndarray:
        """Return binary Stage 1 predictions (1 = DoS/DDoS, 0 = non-DoS)."""
        return self.stage1.predict(X)

    def predict_stage2(self, X_non_dos: np.ndarray) -> np.ndarray:
        """
        Predict Stage 2 categories for instances already known to be non-DoS.
        Caller is responsible for passing only non-DoS instances.
        """
        return self.stage2.predict(X_non_dos)

    def predict_proba_stage1(self, X: np.ndarray) -> np.ndarray:
        """Return Stage 1 class probabilities, shape (n_samples, 2)."""
        return self.stage1.predict_proba(X)

    def predict_proba_stage2(self, X_non_dos: np.ndarray) -> np.ndarray:
        """Return Stage 2 class probabilities for non-DoS instances."""
        return self.stage2.predict_proba(X_non_dos)

    @property
    def is_fitted(self) -> bool:
        return self._is_fitted
