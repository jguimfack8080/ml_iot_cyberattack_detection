# Backend ML -- IoT Cyberattack Detection
## CICIoT2023 + Gradient Boosting + SHAP

Seminararbeit IT-Sicherheit, M.Sc. IVS, Hochschule Bremerhaven
Autor : Jordan Guimfack Jeuna (38184)

---

## Vue d'ensemble

Ce backend implemente un classifieur hierarchique a deux etages sur le dataset CICIoT2023 :

- **Stufe 1** : Classification binaire DoS/DDoS vs. non-DoS (Balanced Accuracy 0.9993)
- **Stufe 2** : Classification multiclasse des 6 categories non-DoS (BA 0.6479 avec Grid Search)
- **Ablation Study** : Pipeline A (StandardScaler + PCA 39 -> 16) vs. Pipeline B (39 features)
- **SHAP** : Analyse d'explicabilite globale et locale (a venir)

---

## Resultats actuels

| Pipeline | Stufe 1 BA | Stufe 2 BA | Stufe 2 BA (Grid Search) |
|----------|-----------|-----------|--------------------------|
| A (PCA 39->16) | 0.9971 | 0.5480 | 0.5384 (subset) |
| B (39 features) | 0.9993 | 0.6301 | **0.6479** (subset) |

Grid Search sur sous-ensemble (8 045 lignes). Reentrainement complet avec best HP prevu.

---

## Prerequis

- Python 3.10 ou superieur
- Dataset CICIoT2023 : `Dataset/MERGED_CSV/` (63 fichiers, ~8.5 GB) -- non versionne

---

## Installation

```bash
# Depuis le repertoire Backend/
python -m venv .venv

# Activer l'environnement (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Activer l'environnement (Linux/WSL/macOS)
source .venv/bin/activate

# Installer les dependances
pip install -r requirements.txt
```

**Verifier l'installation :**
```bash
python -c "import sklearn, shap, pandas; print('OK')"
```

---

## Lancer les tests

```bash
# Tous les tests (60 tests, ~85 secondes)
python -m pytest tests/ -v

# Avec rapport de couverture
python -m pytest tests/ -v --cov=src --cov-report=term-missing

# Tests d'un module specifique
python -m pytest tests/test_data_loader.py -v
python -m pytest tests/test_pipelines.py -v
```

Resultat attendu : **60/60 tests, 89% coverage**

---

## Entrainement des pipelines

### Entrainement complet (Pipeline A + B, ~65 min)

```bash
python scripts/train_pipelines.py --pipeline both --n-per-class 500
```

### Test rapide (3-5 minutes)

```bash
python scripts/train_pipelines.py --pipeline both --max-files 3 --n-per-class 200
```

### Suivi en temps reel (second terminal)

```bash
# Windows PowerShell
Get-Content results\logs\train_latest.log -Wait

# Linux/WSL
tail -f results/logs/train_latest.log
```

### Verifier la fin de l'entrainement

```bash
# Affiche "=== TRAINING COMPLETE" si termine avec succes
Get-Content results\logs\train_latest.log -Tail 3
```

---

## Grid Search (optimisation des hyperparametres)

### Test rapide (subset, ~15 min)

```bash
python scripts/grid_search.py --pipeline both --max-files 5 --n-per-class 50
```

### Grid Search + reentrainement complet

```bash
python scripts/grid_search.py --pipeline both --max-files 10 --n-per-class 200 --retrain
```

### Resultats Grid Search

```bash
python -c "
import json
from pathlib import Path
for n in ['A', 'B']:
    p = Path(f'results/metrics/best_params_{n}.json')
    if p.exists():
        d = json.loads(p.read_text())
        print(f'Pipeline {n}: Stufe2 BA={d[\"stage2\"][\"balanced_accuracy_test\"]:.4f}')
        print(f'  Stufe1 HP: {d[\"stage1\"][\"best_params\"]}')
        print(f'  Stufe2 HP: {d[\"stage2\"][\"best_params\"]}')
"
```

---

## Consulter les resultats d'entrainement

```bash
# Metriques Pipeline A
Get-Content results\metrics\metrics_pipeline_A.json

# Metriques Pipeline B
Get-Content results\metrics\metrics_pipeline_B.json

# Meilleurs hyperparametres (apres Grid Search)
Get-Content results\metrics\best_params_A.json
Get-Content results\metrics\best_params_B.json
```

---

## Structure du projet

```
Backend/
  src/
    data/
      constants.py       Source unique de verite (39 features, 33 labels -> 8 categories)
      loader.py          Chargement stratifie des 63 fichiers MERGED_CSV
      label_mapper.py    Mapping labels -> 8 categories + label binaire Stufe 1
    features/
      preprocessor_a.py  Pipeline A : SimpleImputer + StandardScaler + PCA (39->16)
      preprocessor_b.py  Pipeline B : SimpleImputer + StandardScaler (39 features)
    models/
      stage1_classifier.py       GradientBoosting binaire (DoS/DDoS vs. non-DoS)
      stage2_classifier.py       GradientBoosting multiclasse (6 classes non-DoS)
      hierarchical_classifier.py Orchestration Stufe 1 + Stufe 2
    pipelines/
      _core.py       Logique partagee (PipelineConfig, TrainedPipeline, run_pipeline)
      pipeline_a.py  Pipeline A complete
      pipeline_b.py  Pipeline B complete
    evaluation/        (P4 -- a implementer)
    explainability/    (P4 -- a implementer)
    utils/
      logger.py      Logging fichier (train_latest.log + archives horodatees)
  tests/             60 tests unitaires, 89% coverage
  scripts/
    train_pipelines.py   Entrainement complet Pipeline A et/ou B
    grid_search.py       GridSearchCV Stufe 1 + Stufe 2
  results/
    metrics/             JSON : metriques, best_params
    logs/                Logs d'entrainement (train_latest.log)
    figures/             Graphiques (SHAP, confusion matrix -- a venir)
  models_artifacts/      Modeles serialises (.pkl)
  docs/
    GUIDE_EXECUTION.md   Guide complet d'execution
  .venv/               Environnement virtuel Python (jamais commite)
  requirements.txt
  pyproject.toml
  Done.md              Journal de developpement (immuable)
  TO-DO.md             Backlog des taches par priorite
```

---

## Commandes essentielles

| Action | Commande |
|--------|---------|
| Activer le venv (Windows) | `.venv\Scripts\Activate.ps1` |
| Installer les deps | `pip install -r requirements.txt` |
| Lancer les tests | `python -m pytest tests/ -v` |
| Entrainement complet | `python scripts/train_pipelines.py --pipeline both` |
| Grid Search | `python scripts/grid_search.py --pipeline both` |
| Voir les metriques | `Get-Content results/metrics/metrics_pipeline_B.json` |
| Suivre l'avancement | `Get-Content results/logs/train_latest.log -Wait` |

---

## Regles absolues

- **Jamais Python systeme** : toujours `.venv/Scripts/python` (Windows)
- **Jamais `pip install` hors du venv** pour ce projet
- **Done.md est immuable** : ajouter uniquement en bas, ne jamais modifier les entrees existantes
- **random_state=42** pour tous les composants stochastiques
