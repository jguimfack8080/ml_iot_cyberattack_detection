"""
update_paper_results.py

Lit les resultats generes par evaluate_and_explain.py et :
1. Copie les figures PNG vers paper-usenix-template-jguimfackjeuna/figures/
2. Affiche les valeurs a inserer dans evaluation.tex (Tabelle + SHAP Top-5)

Usage (depuis Backend/ apres avoir lance evaluate_and_explain.py) :
    .venv\\Scripts\\python scripts\\update_paper_results.py

Ne modifie PAS automatiquement les fichiers .tex -- affiche seulement ce qu'il faut
inserer manuellement, pour respecter la regle de non-hallucination.
"""
import json
import shutil
import sys
from pathlib import Path

_BACKEND_DIR = Path(__file__).resolve().parent.parent
_RESULTS_DIR = _BACKEND_DIR / "results"
_FIGURES_SRC  = _RESULTS_DIR / "figures"
_METRICS_DIR  = _RESULTS_DIR / "metrics"

_PAPER_DIR    = _BACKEND_DIR.parent / "paper-usenix-template-jguimfackjeuna"
_FIGURES_DST  = _PAPER_DIR / "figures"


def copy_figures() -> list[str]:
    """Copie les figures pertinentes vers paper/figures/."""
    _FIGURES_DST.mkdir(parents=True, exist_ok=True)
    copied = []
    wanted = [
        "confusion_matrix_stage2_pipelineB.png",
        "confusion_matrix_stage2_pipelineA.png",
        "confusion_matrix_stage1_pipelineB.png",
        "shap_global_stage2_pipelineB.png",
        "shap_global_stage1_pipelineB.png",
        "shap_summary_stage1_pipelineB.png",
    ]
    for fname in wanted:
        src = _FIGURES_SRC / fname
        if src.exists():
            dst = _FIGURES_DST / fname
            shutil.copy2(src, dst)
            copied.append(fname)
            print(f"  [OK] Copie: {fname}")
        else:
            print(f"  [--] Non trouve: {fname}")
    return copied


def print_metrics_summary() -> None:
    """Affiche les metriques finales pour les deux pipelines."""
    print("\n=== METRIQUES FINALES (a inserer dans evaluation.tex) ===\n")
    for pipeline in ("A", "B"):
        metrics_path = _METRICS_DIR / f"metrics_pipeline_{pipeline}.json"
        if not metrics_path.exists():
            print(f"Pipeline {pipeline}: fichier metriques non trouve ({metrics_path})")
            continue
        data = json.loads(metrics_path.read_text(encoding="utf-8"))
        print(f"Pipeline {pipeline}:")
        print(f"  BA Stufe 1 = {data.get('balanced_accuracy_stage1', 'n.v.'):.4f}")
        print(f"  F1 Stufe 1 = {data.get('f1_macro_stage1', 'n.v.'):.4f}")
        print(f"  BA Stufe 2 = {data.get('balanced_accuracy_stage2', 'n.v.'):.4f}")
        print(f"  F1 Stufe 2 = {data.get('f1_macro_stage2', 'n.v.'):.4f}")
        print(f"  Trainingszeit = {data.get('training_time_seconds', 0):.0f}s")
        print()


def print_shap_top5() -> None:
    """Affiche les Top-5 SHAP Features par classe pour Pipeline B (Stufe 2)."""
    shap_path = _METRICS_DIR / "shap_global_stage2_pipelineB.json"
    if not shap_path.exists():
        print("Fichier SHAP non trouve:", shap_path)
        return

    data = json.loads(shap_path.read_text(encoding="utf-8"))

    print("=== TOP-5 SHAP FEATURES PAR CLASSE -- PIPELINE B STUFE 2 ===")
    print("(a inserer dans le tableau tab:shap_top5 de evaluation.tex)\n")

    for cls_name, importance in data.items():
        top5 = list(importance.items())[:5]
        feature_str = ", ".join(
            f"\\texttt{{{f.replace('_', r'\_')}}}" for f, v in top5
        )
        print(f"  {cls_name:<18} & {feature_str} \\\\")

    print()


def print_full_report_per_class() -> None:
    """Affiche le rapport par classe Stufe 2 Pipeline B."""
    report_path = _METRICS_DIR / "full_report_pipeline_B.json"
    if not report_path.exists():
        print("Rapport non trouve:", report_path)
        return

    data = json.loads(report_path.read_text(encoding="utf-8"))
    stage2 = data.get("stage2", {})
    per_class = stage2.get("per_class", {})

    print("=== RAPPORT PAR CLASSE -- PIPELINE B STUFE 2 ===\n")
    print(f"{'Klasse':<18} {'Precision':>10} {'Recall':>8} {'F1':>8} {'Support':>10}")
    print("-" * 60)
    for cls_name, m in per_class.items():
        print(
            f"{cls_name:<18} {m['precision']:>10.4f} {m['recall']:>8.4f} "
            f"{m['f1']:>8.4f} {m['support']:>10}"
        )
    print()
    print(f"  Gesamt BA:  {stage2.get('balanced_accuracy', 'n.v.'):.4f}")
    print(f"  Gesamt F1:  {stage2.get('f1_macro', 'n.v.'):.4f}")


def main() -> int:
    print("=== update_paper_results.py ===\n")

    print("1. Kopiere Figures nach paper/figures/...")
    copied = copy_figures()
    print(f"   {len(copied)} Figures kopiert.\n")

    print("2. Metriken-Zusammenfassung:")
    print_metrics_summary()

    print("3. SHAP Top-5 Features:")
    print_shap_top5()

    print("4. Rapport par classe Stufe 2 Pipeline B:")
    print_full_report_per_class()

    print("=== Fertig. Werte manuell in evaluation.tex eintragen. ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
