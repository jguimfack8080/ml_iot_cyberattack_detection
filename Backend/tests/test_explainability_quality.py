"""Tests for the SHAP explanation-quality metrics."""
import numpy as np

from src.explainability.quality_metrics import (
    cosine_similarity,
    jaccard_topk,
    faithfulness_correlation,
    aggregate,
)


def test_cosine_similarity_bounds():
    assert np.isclose(cosine_similarity([1, 2, 3], [1, 2, 3]), 1.0)
    assert abs(cosine_similarity([1, 0], [0, 1])) < 1e-9          # orthogonal
    assert np.isclose(cosine_similarity([1, 2], [-1, -2]), -1.0)  # opposite
    assert np.isnan(cosine_similarity([0, 0], [1, 1]))           # zero norm


def test_jaccard_topk():
    # top-2 of [3,1,2,0] = {0,2}; of [2.9,0.1,2.1,0] = {0,2} -> identical
    assert jaccard_topk([3, 1, 2, 0], [2.9, 0.1, 2.1, 0], 2) == 1.0
    # top-1 sets disjoint
    assert jaccard_topk([3, 0, 0], [0, 0, 5], 1) == 0.0
    # top-2: {0,1} vs {0,2} -> intersection {0}, union {0,1,2} -> 1/3
    assert abs(jaccard_topk([3, 2, 0], [3, 0, 2], 2) - 1 / 3) < 1e-9


def test_faithfulness_positive_for_consistent_attribution():
    # 2-class logistic model; attribution proportional to w*x should correlate
    # positively with single-feature ablation effects.
    w = np.array([2.0, -1.5, 0.5, 0.0])

    def predict_proba(X):
        X = np.atleast_2d(np.asarray(X, dtype=float))
        z = X @ w
        p1 = 1.0 / (1.0 + np.exp(-z))
        return np.column_stack([1.0 - p1, p1])

    X = np.array([[1.0, 1.0, 1.0, 1.0], [0.5, 2.0, 1.0, 3.0], [2.0, 0.5, 1.5, 0.0]])
    baseline = np.zeros(4)
    pred_idx = np.array([1, 1, 1])
    shap_pred = np.array([w * x for x in X])          # consistent attribution
    out = faithfulness_correlation(predict_proba, X, shap_pred, pred_idx, baseline)
    assert out["n"] == 3
    assert out["mean"] > 0.5                           # clearly positive


def test_aggregate_ignores_nan():
    out = aggregate([1.0, 3.0, float("nan")])
    assert out["n"] == 2
    assert abs(out["mean"] - 2.0) < 1e-9
