"""Unit tests for src.features.preprocessor_a and preprocessor_b."""
import numpy as np
import pytest
from sklearn.pipeline import Pipeline

from src.data.constants import N_FEATURES, N_PCA_COMPONENTS
from src.features.preprocessor_a import build_preprocessor_a, get_explained_variance_ratio
from src.features.preprocessor_b import build_preprocessor_b


class TestPreprocessorA:
    def test_returns_sklearn_pipeline(self) -> None:
        p = build_preprocessor_a()
        assert isinstance(p, Pipeline)

    def test_pipeline_has_scaler_and_pca(self) -> None:
        p = build_preprocessor_a()
        assert "scaler" in p.named_steps
        assert "pca" in p.named_steps

    def test_output_shape_after_fit_transform(self, split_arrays) -> None:
        X_train, X_test, *_ = split_arrays
        p = build_preprocessor_a()
        X_train_out = p.fit_transform(X_train)
        assert X_train_out.shape == (len(X_train), N_PCA_COMPONENTS)

    def test_transform_test_has_same_n_components(self, split_arrays) -> None:
        X_train, X_test, *_ = split_arrays
        p = build_preprocessor_a()
        p.fit_transform(X_train)
        X_test_out = p.transform(X_test)
        assert X_test_out.shape[1] == N_PCA_COMPONENTS

    def test_custom_n_components(self, split_arrays) -> None:
        X_train, *_ = split_arrays
        p = build_preprocessor_a(n_components=8)
        out = p.fit_transform(X_train)
        assert out.shape[1] == 8

    def test_explained_variance_ratio_between_0_and_1(self, split_arrays) -> None:
        X_train, *_ = split_arrays
        p = build_preprocessor_a()
        p.fit_transform(X_train)
        ratio = get_explained_variance_ratio(p)
        assert 0.0 < ratio <= 1.0

    def test_reproducible_with_same_seed(self, split_arrays) -> None:
        X_train, *_ = split_arrays
        p1 = build_preprocessor_a(random_state=42)
        p2 = build_preprocessor_a(random_state=42)
        out1 = p1.fit_transform(X_train)
        out2 = p2.fit_transform(X_train)
        np.testing.assert_array_almost_equal(out1, out2)

    def test_scaler_fitted_after_fit_transform(self, split_arrays) -> None:
        X_train, *_ = split_arrays
        p = build_preprocessor_a()
        p.fit_transform(X_train)
        # StandardScaler fitted → has mean_ attribute
        assert hasattr(p.named_steps["scaler"], "mean_")


class TestPreprocessorB:
    def test_returns_sklearn_pipeline(self) -> None:
        p = build_preprocessor_b()
        assert isinstance(p, Pipeline)

    def test_pipeline_has_only_scaler(self) -> None:
        p = build_preprocessor_b()
        assert "scaler" in p.named_steps
        assert "pca" not in p.named_steps

    def test_output_shape_preserves_all_features(self, split_arrays) -> None:
        X_train, X_test, *_ = split_arrays
        p = build_preprocessor_b()
        X_out = p.fit_transform(X_train)
        assert X_out.shape == (len(X_train), N_FEATURES)

    def test_values_are_standardized(self, split_arrays) -> None:
        X_train, *_ = split_arrays
        p = build_preprocessor_b()
        X_out = p.fit_transform(X_train)
        # Standardized data has mean ~0 and std ~1 per column
        np.testing.assert_allclose(X_out.mean(axis=0), 0.0, atol=1e-10)
        np.testing.assert_allclose(X_out.std(axis=0), 1.0, atol=1e-10)

    def test_b_output_wider_than_a(self, split_arrays) -> None:
        X_train, *_ = split_arrays
        pa = build_preprocessor_a()
        pb = build_preprocessor_b()
        out_a = pa.fit_transform(X_train)
        out_b = pb.fit_transform(X_train)
        assert out_b.shape[1] > out_a.shape[1]
