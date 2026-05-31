"""
experiment_class_weight.py

Experience rapide : mesure l'effet de sample_weight='balanced' sur la Balanced Accuracy
de Stufe 2 (classes rares Web-based, Brute-Force).

GradientBoostingClassifier ne supporte pas class_weight, mais accepte sample_weight
dans fit(). On utilise compute_sample_weight('balanced', y) pour ponderer inversement
a la frequence des classes.

Teste sur un sous-ensemble (rapide) Pipeline B (meilleure pipeline) :
  - Stufe 2 sans sample_weight (baseline)
  - Stufe 2 avec sample_weight='balanced'

Si la BA s'ameliore significativement, un reentrainement complet est justifie.

Usage (depuis Backend/ avec venv) :
  .venv\\Scripts\\python scripts\\experiment_class_weight.py --max-files 15 --n-per-class 300
"""
import argparse
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import balanced_accuracy_score, f1_score, recall_score
from sklearn.utils.class_weight import compute_sample_weight

from src.data.constants import BINARY_COL, CATEGORY_COL, FEATURE_COLUMNS, RANDOM_STATE
from src.data.label_mapper import apply_label_mapping
from src.data.loader import load_stratified
from src.features.preprocessor_b import build_preprocessor_b

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "Dataset" / "MERGED_CSV"

# Best HP Pipeline B Stufe 2 (from grid search)
_BEST_HP = {"n_estimators": 200, "max_depth": 3, "learning_rate": 0.05, "subsample": 0.8}


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Experience sample_weight balanced Stufe 2")
    p.add_argument("--max-files", type=int, default=15)
    p.add_argument("--n-per-class", type=int, default=300)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    logger.info("Chargement sous-ensemble (max_files=%d, n_per_class=%d)...",
                args.max_files, args.n_per_class)
    df = load_stratified(_DATA_DIR, n_per_class_per_file=args.n_per_class,
                         max_files=args.max_files, random_state=RANDOM_STATE)
    df = apply_label_mapping(df)

    X = df[list(FEATURE_COLUMNS)].astype(float).to_numpy()
    y_bin = df[BINARY_COL].to_numpy(dtype=int)
    y_cat = df[CATEGORY_COL].to_numpy(dtype=str)

    X_tr, X_te, y_bin_tr, y_bin_te, y_cat_tr, y_cat_te = train_test_split(
        X, y_bin, y_cat, test_size=0.2, stratify=y_cat, random_state=RANDOM_STATE)

    prep = build_preprocessor_b()
    X_tr_p = prep.fit_transform(X_tr)
    X_te_p = prep.transform(X_te)

    # Stufe 2 : non-DoS uniquement
    non_dos_tr = y_bin_tr == 0
    non_dos_te = y_bin_te == 0
    Xtr2, ytr2 = X_tr_p[non_dos_tr], y_cat_tr[non_dos_tr]
    Xte2, yte2 = X_te_p[non_dos_te], y_cat_te[non_dos_te]

    logger.info("Stufe 2 train: %d instances, test: %d instances", len(ytr2), len(yte2))
    labels = sorted(np.unique(yte2))

    # --- Baseline : sans sample_weight ---
    logger.info("=" * 60)
    logger.info("BASELINE (sans sample_weight)")
    clf_base = GradientBoostingClassifier(random_state=RANDOM_STATE, **_BEST_HP)
    clf_base.fit(Xtr2, ytr2)
    pred_base = clf_base.predict(Xte2)
    ba_base = balanced_accuracy_score(yte2, pred_base)
    f1_base = f1_score(yte2, pred_base, average="macro", zero_division=0)
    logger.info("Baseline BA=%.4f F1=%.4f", ba_base, f1_base)

    # --- Avec sample_weight='balanced' ---
    logger.info("=" * 60)
    logger.info("AVEC sample_weight='balanced'")
    sw = compute_sample_weight(class_weight="balanced", y=ytr2)
    clf_bal = GradientBoostingClassifier(random_state=RANDOM_STATE, **_BEST_HP)
    clf_bal.fit(Xtr2, ytr2, sample_weight=sw)
    pred_bal = clf_bal.predict(Xte2)
    ba_bal = balanced_accuracy_score(yte2, pred_bal)
    f1_bal = f1_score(yte2, pred_bal, average="macro", zero_division=0)
    logger.info("Balanced BA=%.4f F1=%.4f", ba_bal, f1_bal)

    # --- Recall par classe (focus classes rares) ---
    logger.info("=" * 60)
    logger.info("RECALL PAR CLASSE (baseline -> balanced)")
    rec_base = recall_score(yte2, pred_base, labels=labels, average=None, zero_division=0)
    rec_bal = recall_score(yte2, pred_bal, labels=labels, average=None, zero_division=0)
    for lab, rb, rl in zip(labels, rec_base, rec_bal):
        flag = " <-- amelioration" if rl > rb + 0.02 else (" <-- degradation" if rl < rb - 0.02 else "")
        logger.info("  %-16s : %.4f -> %.4f%s", lab, rb, rl, flag)

    logger.info("=" * 60)
    logger.info("RESUME : BA %.4f -> %.4f (delta %+.4f)", ba_base, ba_bal, ba_bal - ba_base)
    if ba_bal > ba_base + 0.01:
        logger.info("==> sample_weight AMELIORE la BA. Reentrainement complet justifie.")
    else:
        logger.info("==> sample_weight n'ameliore pas significativement. Documenter le constat.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
