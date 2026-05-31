#!/usr/bin/env bash
# wait_and_evaluate.sh
# Attend la fin du reentrainement (TRAINING COMPLETE dans train_latest.log),
# puis lance evaluate_and_explain.py automatiquement.
#
# Usage (depuis Backend/ avec venv active, dans un terminal separe) :
#   bash scripts/wait_and_evaluate.sh
#
# Suivi en temps reel :
#   cat results/logs/train_latest.log | tail -5

set -euo pipefail

LOG_FILE="results/logs/train_latest.log"
SENTINEL="TRAINING COMPLETE"
POLL_INTERVAL=30  # secondes entre chaque verification

echo "[wait_and_evaluate] Attente de la fin du reentrainement..."
echo "[wait_and_evaluate] Surveillance de: $LOG_FILE"
echo "[wait_and_evaluate] Sentinelle recherchee: '$SENTINEL'"
echo "[wait_and_evaluate] Intervalle de poll: ${POLL_INTERVAL}s"

while true; do
    if grep -q "$SENTINEL" "$LOG_FILE" 2>/dev/null; then
        echo "[wait_and_evaluate] Reentrainement termine! $(date)"
        break
    fi
    echo "[wait_and_evaluate] En attente... $(date '+%H:%M:%S')"
    sleep "$POLL_INTERVAL"
done

echo "[wait_and_evaluate] Lancement de evaluate_and_explain.py..."
.venv/Scripts/python scripts/evaluate_and_explain.py \
    --pipeline both \
    --shap-samples 500 \
    --waterfall-top-k 3

echo "[wait_and_evaluate] Evaluation et SHAP termines!"
echo "[wait_and_evaluate] Voir les resultats dans:"
echo "  results/metrics/ (JSON)"
echo "  results/figures/ (PNG)"
