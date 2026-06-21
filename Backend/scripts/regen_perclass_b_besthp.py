"""
regen_perclass_b_besthp.py

Regeneriert die deterministischen Per-Klassen-Metriken (Precision/Recall/F1) der
Stufe 2 fuer Pipeline B mit Best-HP OHNE Klassengewichtung (nobalanced).

Hintergrund: rerun_all.sh ueberschreibt das Best-HP-B-Modell mit dem
klassengewichteten finalen B-Modell. Fuer die Vergleichsspalte "R (Best HP)" in
tab:perclass_b werden die Per-Klassen-Recalls des nobalanced-Modells benoetigt.
Diese sind deterministisch (GradientBoosting predict, random_state=42) und werden
hier reproduziert und als JSON gesichert.

Ausfuehrung (aus Backend/):  .venv/Scripts/python scripts/regen_perclass_b_besthp.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
import numpy as np
from sklearn.metrics import (
    recall_score, precision_score, f1_score,
    balanced_accuracy_score, accuracy_score,
)

from src.models.stage1_classifier import Stage1Config
from src.models.stage2_classifier import Stage2Config
from src.pipelines._core import PipelineConfig
from src.pipelines.pipeline_b import run_pipeline_b

_BACKEND = Path(__file__).resolve().parent.parent
_DATA = _BACKEND.parent / "Dataset" / "MERGED_CSV"
_OUT = _BACKEND / "results" / "metrics" / "perclass_B_besthp_nobalanced.json"


def main() -> int:
    bp = json.loads((_BACKEND / "results" / "metrics" / "best_params_B.json").read_text(encoding="utf-8"))
    s1 = Stage1Config(**bp["stage1"]["best_params"])
    s2 = Stage2Config(**bp["stage2"]["best_params"])
    cfg = PipelineConfig(
        data_dir=_DATA, n_per_class_per_file=500,
        stage1_config=s1, stage2_config=s2, balanced_stage2=False,
    )
    r = run_pipeline_b(cfg)

    mask = r.y_binary_test == 0
    Xt = r.X_test[mask]
    yt = r.y_category_test[mask]
    pred = r.classifier.stage2.predict(Xt)
    labels = sorted(np.unique(yt))

    rec = recall_score(yt, pred, labels=labels, average=None, zero_division=0)
    prec = precision_score(yt, pred, labels=labels, average=None, zero_division=0)
    f1 = f1_score(yt, pred, labels=labels, average=None, zero_division=0)

    out = {
        "_meta": "Pipeline B Best-HP (nobalanced) Stufe 2 per-class",
        "balanced_accuracy": float(balanced_accuracy_score(yt, pred)),
        "accuracy": float(accuracy_score(yt, pred)),
        "f1_macro": float(f1_score(yt, pred, average="macro", zero_division=0)),
        "per_class": {
            lab: {"precision": float(p), "recall": float(rc), "f1": float(fc)}
            for lab, p, rc, fc in zip(labels, prec, rec, f1)
        },
    }
    _OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
