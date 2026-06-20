"""
compute_shap_quality.py

Computes quantitative SHAP explanation-quality metrics (Faithfulness, Stability,
Jaccard top-k) for the final Stage-2 models of both pipelines, using the exact,
documented definitions in src/explainability/quality_metrics.py.

This answers the framing research question (measurable XAI criteria) and the
stability part of sub-question 2 (effect of PCA on explanation stability):
Pipeline A (PCA components) vs Pipeline B (original features).

Deterministic (random_state = 42). SHAP is recomputed with the same
PermutationExplainer setup as the main analysis (Independent masker, predict_proba).

Usage (from Backend/):  .venv/Scripts/python scripts/compute_shap_quality.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import joblib
import shap

from src.explainability.quality_metrics import (
    faithfulness_correlation,
    cosine_similarity,
    jaccard_topk,
    aggregate,
)

_BACKEND = Path(__file__).resolve().parent.parent
_MODELS = _BACKEND / "models_artifacts"
_OUT = _BACKEND / "results" / "metrics" / "shap_quality.json"

SEED = 42
N_FAITH = 50          # instances for faithfulness
N_STAB = 20           # instances for stability / jaccard
N_PERTURB = 4         # perturbations per instance
N_BACKGROUND = 50     # background instances for the masker
SIGMA_REL = 0.1       # perturbation std as fraction of each feature's std
TOP_K = 5             # k for Jaccard top-k


def _explainer(model, background):
    masker = shap.maskers.Independent(background)
    return shap.PermutationExplainer(
        model.predict_proba, masker, max_evals=2 * background.shape[1] + 1
    )


def _pipeline_quality(name: str) -> dict:
    model = joblib.load(_MODELS / f"stage2_{name}.pkl")
    td = np.load(_MODELS / f"test_data_{name}.npz", allow_pickle=True)
    X, yb, yc = td["X_test"], td["y_binary_test"], td["y_category_test"]

    non_dos = yb == 0
    X_nd = X[non_dos].astype(float)
    rng = np.random.default_rng(SEED)

    bg_idx = rng.choice(len(X_nd), min(N_BACKGROUND, len(X_nd)), replace=False)
    background = X_nd[bg_idx]
    baseline = np.median(X_nd, axis=0)
    feat_std = X_nd.std(axis=0)
    classes = list(model.classes_)
    explainer = _explainer(model, background)

    # --- Faithfulness ---
    f_idx = rng.choice(len(X_nd), min(N_FAITH, len(X_nd)), replace=False)
    Xf = X_nd[f_idx]
    sv_f = explainer(Xf).values                      # (n, d, n_classes)
    pred_f = model.predict(Xf)
    pred_idx_f = np.array([classes.index(p) for p in pred_f])
    shap_pred = np.stack([sv_f[i, :, pred_idx_f[i]] for i in range(len(Xf))])
    faith = faithfulness_correlation(
        model.predict_proba, Xf, shap_pred, pred_idx_f, baseline
    )

    # --- Stability (cosine) + Jaccard top-k under small perturbations ---
    s_idx = rng.choice(len(X_nd), min(N_STAB, len(X_nd)), replace=False)
    cos_vals, jac_vals = [], []
    for i in s_idx:
        x = X_nd[i]
        c = classes.index(model.predict(x.reshape(1, -1))[0])
        noise = rng.normal(0.0, SIGMA_REL * feat_std, size=(N_PERTURB, x.shape[0]))
        batch = np.vstack([x, x + noise])            # (1 + M, d)
        sv = explainer(batch).values                 # (1+M, d, n_classes)
        sv_orig = sv[0, :, c]
        for m in range(1, N_PERTURB + 1):
            sv_pert = sv[m, :, c]
            cos_vals.append(cosine_similarity(sv_orig, sv_pert))
            jac_vals.append(jaccard_topk(sv_orig, sv_pert, TOP_K))

    return {
        "pipeline": name,
        "faithfulness": faith,
        "stability_cosine": aggregate(cos_vals),
        "jaccard_topk": aggregate(jac_vals),
        "params": {
            "n_faithfulness": int(N_FAITH), "n_stability": int(N_STAB),
            "n_perturbations": int(N_PERTURB), "sigma_rel": SIGMA_REL,
            "top_k": int(TOP_K), "n_background": int(N_BACKGROUND), "seed": SEED,
        },
    }


def main() -> int:
    result = {}
    for name in ("A", "B"):
        print(f"=== Pipeline {name} ===", flush=True)
        result[name] = _pipeline_quality(name)
        q = result[name]
        print(f"  Faithfulness : {q['faithfulness']['mean']:.4f} "
              f"(std {q['faithfulness']['std']:.4f}, n={q['faithfulness']['n']})")
        print(f"  Stability    : {q['stability_cosine']['mean']:.4f} "
              f"(std {q['stability_cosine']['std']:.4f})")
        print(f"  Jaccard@{TOP_K}   : {q['jaccard_topk']['mean']:.4f} "
              f"(std {q['jaccard_topk']['std']:.4f})")
    _OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"\nGespeichert: {_OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
