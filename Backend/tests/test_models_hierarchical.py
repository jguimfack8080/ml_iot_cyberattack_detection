"""Unit tests for Stage 1, Stage 2, and HierarchicalClassifier."""
import numpy as np
import pytest

from src.models.hierarchical_classifier import HierarchicalClassifier
from src.models.stage1_classifier import Stage1Config, build_stage1_classifier
from src.models.stage2_classifier import Stage2Config, build_stage2_classifier


class TestStage1Classifier:
    def test_build_returns_gradient_boosting(self) -> None:
        from sklearn.ensemble import GradientBoostingClassifier
        clf = build_stage1_classifier()
        assert isinstance(clf, GradientBoostingClassifier)

    def test_default_random_state_is_42(self) -> None:
        clf = build_stage1_classifier()
        assert clf.get_params()["random_state"] == 42

    def test_custom_config_applied(self) -> None:
        cfg = Stage1Config(n_estimators=50, max_depth=2)
        clf = build_stage1_classifier(cfg)
        assert clf.get_params()["n_estimators"] == 50
        assert clf.get_params()["max_depth"] == 2

    def test_fits_and_predicts_binary(self, preprocessed_arrays) -> None:
        X_train, X_test, y_bin_train, y_bin_test, *_ = preprocessed_arrays
        clf = build_stage1_classifier()
        clf.fit(X_train, y_bin_train)
        preds = clf.predict(X_test)
        assert set(preds).issubset({0, 1})
        assert len(preds) == len(X_test)


class TestStage2Classifier:
    def test_build_returns_gradient_boosting(self) -> None:
        from sklearn.ensemble import GradientBoostingClassifier
        clf = build_stage2_classifier()
        assert isinstance(clf, GradientBoostingClassifier)

    def test_fits_on_non_dos_instances(self, preprocessed_arrays) -> None:
        X_train, X_test, y_bin_train, y_bin_test, y_cat_train, y_cat_test = preprocessed_arrays
        non_dos = y_bin_train == 0
        clf = build_stage2_classifier()
        clf.fit(X_train[non_dos], y_cat_train[non_dos])
        preds = clf.predict(X_test[y_bin_test == 0])
        assert len(preds) > 0


class TestHierarchicalClassifier:
    def test_fit_sets_is_fitted(self, preprocessed_arrays) -> None:
        X_train, _, y_bin_train, _, y_cat_train, _ = preprocessed_arrays
        clf = HierarchicalClassifier(
            stage1=build_stage1_classifier(),
            stage2=build_stage2_classifier(),
        )
        assert not clf.is_fitted
        clf.fit(X_train, y_bin_train, y_cat_train)
        assert clf.is_fitted

    def test_predict_returns_correct_length(self, fitted_hierarchical, preprocessed_arrays) -> None:
        _, X_test, *_ = preprocessed_arrays
        preds = fitted_hierarchical.predict(X_test)
        assert len(preds) == len(X_test)

    def test_predict_dos_ddos_label_for_stage1_positives(
        self, fitted_hierarchical, preprocessed_arrays
    ) -> None:
        _, X_test, _, y_bin_test, *_ = preprocessed_arrays
        preds = fitted_hierarchical.predict(X_test)
        stage1_pred = fitted_hierarchical.predict_stage1(X_test)
        dos_mask = stage1_pred == 1
        # All Stage 1 positives must get "DoS/DDoS" label
        if dos_mask.any():
            assert all(p == "DoS/DDoS" for p in preds[dos_mask])

    def test_predict_stage2_not_dos_ddos(self, fitted_hierarchical, preprocessed_arrays) -> None:
        _, X_test, _, y_bin_test, *_ = preprocessed_arrays
        non_dos_mask = y_bin_test == 0
        if non_dos_mask.sum() > 0:
            preds = fitted_hierarchical.predict_stage2(X_test[non_dos_mask])
            assert "DoS/DDoS" not in preds

    def test_raises_if_no_non_dos_data(self) -> None:
        rng = np.random.default_rng(0)
        X = rng.random((50, 16))
        y_binary = np.ones(50, dtype=int)   # all DoS/DDoS — no Stage 2 data
        y_cat = np.array(["DDoS"] * 50)
        clf = HierarchicalClassifier(
            stage1=build_stage1_classifier(),
            stage2=build_stage2_classifier(),
        )
        with pytest.raises(ValueError, match="Stage 2 cannot be trained"):
            clf.fit(X, y_binary, y_cat)

    def test_predict_stage1_binary_output(self, fitted_hierarchical, preprocessed_arrays) -> None:
        _, X_test, *_ = preprocessed_arrays
        preds = fitted_hierarchical.predict_stage1(X_test)
        assert set(preds).issubset({0, 1})

    def test_predict_proba_stage1_shape(self, fitted_hierarchical, preprocessed_arrays) -> None:
        _, X_test, *_ = preprocessed_arrays
        proba = fitted_hierarchical.predict_proba_stage1(X_test)
        assert proba.shape == (len(X_test), 2)
        np.testing.assert_allclose(proba.sum(axis=1), 1.0, atol=1e-6)
