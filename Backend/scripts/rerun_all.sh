#!/usr/bin/env bash
#
# rerun_all.sh
#
# Vollstaendige, deterministische Reproduktion ALLER im Paper berichteten
# Kennzahlen aus dem CICIoT2023-Backend (random_state=42).
#
# Erzeugt nacheinander und sichert jede Konfiguration in einer eigenen JSON:
#   1. Standard-Konfiguration (Default-Hyperparameter)  -> metrics_pipeline_{A,B}_standard.json
#   2. Grid Search (Subset 8045)                        -> best_params_{A,B}.json
#   3. Best-HP-Konfiguration (beide Pipelines)          -> metrics_pipeline_A.json (final A)
#                                                          metrics_pipeline_B_nobalanced.json
#   4. Klassengewichtete Konfiguration (Pipeline B)     -> metrics_pipeline_B.json (final B)
#   5. Evaluation + SHAP auf den finalen Modellen       -> full_report_*, shap_global_*, Figuren
#   6. Figuren ins Paper kopieren
#
# Endzustand der Artefakte: stage*_A.pkl = Best-HP A, stage*_B.pkl = Balanced B
# (damit SHAP/Figuren zur finalen Modellwahl des Papers passen).
#
# Ausfuehrung (aus Backend/):  bash scripts/rerun_all.sh
set -u
PY="./.venv/Scripts/python.exe"
M="results/logs/rerun_master.log"
ST="results/metrics/_standard"

step () { echo ""; echo "########## $(date '+%H:%M:%S')  $1 ##########"; }
fail () { echo "!!!!! FEHLER in Schritt: $1 (exit $2). Abbruch. !!!!!"; exit "$2"; }

{
echo "=========================================================="
echo "RERUN ALL gestartet $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================================="

step "1/6 Standard-Konfiguration (Default-HP, beide Pipelines)"
"$PY" scripts/train_pipelines.py --pipeline both \
      --models-dir models_artifacts/_standard --results-dir "$ST" || fail "1-standard" $?
cp "$ST/metrics_pipeline_A.json" results/metrics/metrics_pipeline_A_standard.json
cp "$ST/metrics_pipeline_B.json" results/metrics/metrics_pipeline_B_standard.json
echo ">> Standard-Metriken gesichert."

step "2/6 Grid Search (Subset, beide Pipelines)"
"$PY" scripts/grid_search.py --pipeline both || fail "2-gridsearch" $?

step "3/6 Best-HP-Reentrainement (beide Pipelines, voller Datensatz)"
"$PY" scripts/train_pipelines.py --pipeline both \
      --best-params-dir results/metrics || fail "3-besthp" $?
cp results/metrics/metrics_pipeline_B.json results/metrics/metrics_pipeline_B_nobalanced.json
echo ">> Best-HP A ist finales A-Modell; B-Best-HP-Metriken als _nobalanced gesichert."

step "4/6 Klassengewichtetes Reentrainement (Pipeline B, finales B-Modell)"
"$PY" scripts/train_pipelines.py --pipeline B \
      --best-params-dir results/metrics --balanced-stage2 || fail "4-balanced" $?

step "5/6 Evaluation + SHAP auf finalen Modellen (A=Best-HP, B=Balanced)"
"$PY" scripts/evaluate_and_explain.py --pipeline both || fail "5-eval-shap" $?

step "6/6 Figuren ins Paper kopieren + Zusammenfassung"
"$PY" scripts/update_paper_results.py || fail "6-update" $?

echo ""
echo "=========================================================="
echo "RERUN ALL ABGESCHLOSSEN $(date '+%Y-%m-%d %H:%M:%S')"
echo "=========================================================="
} 2>&1 | tee "$M"
