"""
Quantitative quality metrics for SHAP explanations.

These functions operationalise the three explanation-quality dimensions named by
Hermosilla et al. (2025, DOI: 10.3390/app15137329) with standard, clearly defined
measures from the XAI evaluation literature. The exact formulas are stated here so
that the reported numbers are fully reproducible and not based on any assumption.

  Faithfulness (Fidelitaet)
      Does the attribution reflect the model's actual behaviour? For one instance
      and its predicted class c, each feature j is ablated (replaced by the
      background median) and the resulting drop of predict_proba_c is recorded:
          delta_j = f_c(x) - f_c(x | x_j := baseline_j).
      Faithfulness is the Pearson correlation between the SHAP attributions
      (phi_j for class c) and these ablation effects (delta_j), averaged over
      instances. Range [-1, 1]; higher = more faithful.
      (deletion-based faithfulness, cf. Samek et al. 2017; Bhatt et al. 2020)

  Stability (Konsistenz)
      Do similar inputs yield similar explanations? Each instance is perturbed by
      small Gaussian noise scaled to each feature's standard deviation; the SHAP
      vector of the original and of each perturbation (for the original predicted
      class) are compared by cosine similarity. Range [-1, 1]; higher = more stable.
      (local stability, cf. Alvarez-Melis & Jaakkola 2018)

  Jaccard top-k
      Rank stability of the most important features under the same perturbations:
      mean Jaccard overlap of the top-k feature sets of the original and the
      perturbed explanations. Range [0, 1]; higher = more stable ranking.

All metrics are deterministic for a fixed random seed.
"""
import numpy as np


def _pearson(a: np.ndarray, b: np.ndarray) -> float:
    """Pearson correlation; returns NaN if either vector is (near) constant."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.std() < 1e-12 or b.std() < 1e-12:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity of two vectors; NaN if either has (near) zero norm."""
    a = np.asarray(a, dtype=float).ravel()
    b = np.asarray(b, dtype=float).ravel()
    na, nb = np.linalg.norm(a), np.linalg.norm(b)
    if na < 1e-12 or nb < 1e-12:
        return float("nan")
    return float(np.dot(a, b) / (na * nb))


def jaccard_topk(a: np.ndarray, b: np.ndarray, k: int) -> float:
    """Jaccard overlap of the top-k features (by absolute value) of a and b."""
    a = np.asarray(a, dtype=float).ravel()
    b = np.asarray(b, dtype=float).ravel()
    ta = set(np.argsort(np.abs(a))[::-1][:k].tolist())
    tb = set(np.argsort(np.abs(b))[::-1][:k].tolist())
    union = ta | tb
    if not union:
        return float("nan")
    return len(ta & tb) / len(union)


def faithfulness_correlation(
    predict_proba,
    X: np.ndarray,
    shap_pred_class: np.ndarray,
    pred_class_idx: np.ndarray,
    baseline: np.ndarray,
) -> dict:
    """
    Deletion-based faithfulness, averaged over the rows of X.

    Args:
        predict_proba: callable, X_batch -> array (m, n_classes).
        X: preprocessed instances, shape (n, d).
        shap_pred_class: SHAP attributions for each instance's predicted class,
            shape (n, d).
        pred_class_idx: predicted class index per instance, shape (n,).
        baseline: per-feature ablation value (e.g. background median), shape (d,).

    Returns:
        dict with mean, std and n (number of instances with defined correlation).
    """
    X = np.asarray(X, dtype=float)
    baseline = np.asarray(baseline, dtype=float)
    n, d = X.shape
    base_proba = predict_proba(X)
    cors = []
    cols = np.arange(d)
    for i in range(n):
        c = int(pred_class_idx[i])
        # Row j is x with feature j replaced by baseline_j (single-feature ablation).
        Xa = np.tile(X[i], (d, 1))
        Xa[cols, cols] = baseline[cols]
        pa = predict_proba(Xa)[:, c]
        deltas = base_proba[i, c] - pa
        r = _pearson(shap_pred_class[i], deltas)
        if not np.isnan(r):
            cors.append(r)
    cors = np.asarray(cors, dtype=float)
    return {
        "mean": float(cors.mean()) if cors.size else float("nan"),
        "std": float(cors.std()) if cors.size else float("nan"),
        "n": int(cors.size),
    }


def aggregate(values: list[float]) -> dict:
    """Mean/std/count over a list of metric values, ignoring NaNs."""
    arr = np.asarray([v for v in values if not np.isnan(v)], dtype=float)
    return {
        "mean": float(arr.mean()) if arr.size else float("nan"),
        "std": float(arr.std()) if arr.size else float("nan"),
        "n": int(arr.size),
    }
