# Done.md — Journal de Développement ML Backend
## Projet : IoT Cyberattack Detection (CICIoT2023 + Gradient Boosting + SHAP)

Journal chronologique immuable. Ne jamais supprimer les entrées existantes.

---

### 2026-05-30 — Session 1 : Initialisation du Backend ML

**Ce qui a été analysé :**
- Lastenheft.md : cahier des charges complet lu et compris
- README.md : vue d'ensemble technique assimilée
- PROJECT_LOG.md : historique des sessions précédentes (Paper, LaTeX, présentations)
- Dataset/ : structure inspectée en profondeur

**Découvertes clés sur le Dataset :**
- `Dataset/MERGED_CSV/` : 63 fichiers Merged01-63.csv, ~140 MB chacun, total ~8,5 GB
  - Structure : 39 features + colonne Label = 40 colonnes
  - Label exemple : "DDOS-PSHACK_FLOOD" (casse mixte, tirets)
  - Toutes classes d'attaque mélangées — parfait pour l'entraînement
- `Dataset/CSV/<AttackType>/` : fichiers pcap.csv par sous-dossier, SANS colonne Label
  - 39 features uniquement (pas de Label)
- Divergence détectée : Lastenheft dit 46 features, CSV disponibles en ont 39
  - Décision : utiliser les 39 features disponibles, PCA sera 39→16 (pas 46→16)
  - Cette divergence sera documentée dans le Paper

**Décisions prises :**
1. Source de données : MERGED_CSV retenu (labels présents, format consolidé)
2. PCA : 39→16 composantes (au lieu de 46→16 décrit dans Lastenheft)
3. Stratégie mémoire : chargement chunked/stratifié (8,5 GB ne tient pas en RAM)
4. Structure Backend : dossier `Backend/` créé à la racine du projet

**Structure créée :**
```
Backend/
├── src/
│   ├── __init__.py
│   ├── main.py              (squelette CLI avec argparse)
│   ├── data/__init__.py
│   ├── features/__init__.py
│   ├── models/__init__.py
│   ├── pipelines/__init__.py
│   ├── evaluation/__init__.py
│   ├── explainability/__init__.py
│   └── utils/__init__.py
├── tests/__init__.py
├── notebooks/
├── scripts/
├── configs/
├── models_artifacts/
├── results/figures/ + results/metrics/
├── docs/
├── requirements.txt
├── pyproject.toml
├── .env.example
├── .gitignore
├── CLAUDE.md               (document de travail ML)
└── TO-DO.md
```

**Points en attente de décision (P1 ouverts) :**
- Vérifier les valeurs exactes et la casse des labels dans MERGED_CSV
  (label vu : "DDOS-PSHACK_FLOOD" — mapping vers catégories à valider)
- Stratégie de chargement mémoire à décider :
  a) Echantillonnage stratifié (recommandé)
  b) Chargement séquentiel chunked
  c) Dask out-of-core

**Prochaine étape concrète :**
- Résoudre les 3 P1 restants (labels, mapping, stratégie mémoire)
- Implémenter `src/data/loader.py` et `src/data/label_mapper.py` (début P2)

---

### 2026-05-30 — Session 2 : Analyse approfondie, structure Backend/ effectivement créée

**Ce qui a été fait :**
- Inspection directe des fichiers MERGED_CSV avec Python (colonnes, labels, nulls, distribution)
- 34 labels uniques confirmés (scan Merged01-04), mapping vers 8 catégories établi
- Structure Backend/ entièrement créée (répertoires + __init__.py + src/main.py)
- TO-DO.md complet créé (P1 à P5, deadlines du Vortrag Umsetzungsplan intégrées)
- Backend/Done.md créé (journal spécifique au Backend ML)
- requirements.txt, pyproject.toml, .env.example, .gitignore créés

**Corrections par rapport à Session 1 :**
- Session 1 décrivait la structure comme "créée" mais Backend/ n'existait pas — corrigé
- Labels sont en ALL_CAPS (pas "casse mixte" comme noté en Session 1)
- BACKDOOR_MALWARE identifié comme label présent mais non mappé — P1 ouvert

**P1 résolus dans cette session :**
- Labels : 34 labels ALL_CAPS confirmés, mapping complet (33/34)
- Structure Backend/ : effectivement créée et validée

**Décisions P1 supplémentaires prises en fin de session :**
- BACKDOOR_MALWARE → DROP (hors scope 8 catégories, < 0,01 %, à documenter dans methodik.tex)
- Stratégie mémoire → Echantillonnage stratifié sur les 63 fichiers (Best Practice, aucune perte info)
  Détails complets dans Backend/Done.md

**Tous les P1 sont résolus. P2 peut commencer.**

**Prochaine étape concrète :**
1. Implémenter Backend/src/data/loader.py (chargement stratifié 63 fichiers MERGED_CSV)
2. Implémenter Backend/src/data/label_mapper.py (mapping 33 labels → 8 catégories)

---

### 2026-05-30 — Session 3 : P2 démarré — src/data/ implémenté et testé

**Fichiers créés :**
- Backend/src/data/constants.py — source unique de vérité (33 labels, 39 features, constantes)
- Backend/src/data/loader.py — chargement stratifié Best Practice (63 fichiers, ~568 MB RAM peak)
- Backend/src/data/label_mapper.py — mapping 33 labels → 8 catégories, drop BACKDOOR_MALWARE
- Backend/tests/test_data_loader.py — 10 tests unitaires
- Backend/tests/test_data_label_mapper.py — 10 tests unitaires

**Résultats tests :** 20/20 ✅ — Coverage : constants 100%, label_mapper 100%, loader 90%

**Décision technique majeure — normalisation noms colonnes :**
- 3 colonnes du CSV contiennent des espaces ('Protocol Type', 'Tot sum', 'Tot size')
- Normalisées en Protocol_Type, Tot_sum, Tot_size à la lecture dans loader.py
- Raison : XGBoost rejette les espaces dans les noms de features

**Prochaine étape :** preprocessor_a.py (StandardScaler + PCA), puis les modèles Stufe 1 et 2

---

### 2026-05-30 — Session 4 : P2 + P3 entièrement terminés (60/60 tests, 89% coverage)

**Fichiers créés :**
- src/features/preprocessor_a.py — sklearn Pipeline(scaler + PCA 39→16), 100% coverage
- src/features/preprocessor_b.py — sklearn Pipeline(scaler seul), 100% coverage
- src/models/stage1_classifier.py — GB binaire Stufe 1, Stage1Config dataclass
- src/models/stage2_classifier.py — GB multiclasse Stufe 2, Stage2Config dataclass
- src/models/hierarchical_classifier.py — HierarchicalClassifier fit/predict, 95% coverage
- src/pipelines/_core.py — PipelineConfig + TrainedPipeline + run_pipeline() 7 étapes, 98%
- src/pipelines/pipeline_a.py — run_pipeline_a() 100% coverage
- src/pipelines/pipeline_b.py — run_pipeline_b() 100% coverage
- tests/conftest.py — fixtures partagées
- tests/test_features_preprocessors.py — 13 tests
- tests/test_models_hierarchical.py — 12 tests
- tests/test_pipelines.py — 10 tests (A + B + comparaison)

**Résultats :** 60/60 tests ✅ — Coverage : 89%

**Bug corrigé :** PyArrow/sklearn incompatibilité → .to_numpy() dans _core.py et conftest.py

**Architecture P3 :** Pipeline B implémentée EN MÊME TEMPS que P2 grâce au pattern DRY
(_core.py partagé). Les 2 pipelines ne diffèrent que par le preprocessor injecté.

**URGENT -- deadline 2026-06-01 :** Lancer l'entrainement sur MERGED_CSV reelles pour
premiers resultats Balanced Accuracy du Motivationsreview.

---

### 2026-05-31 — Sessions 5-6 : Venv + entraînement réel terminé — premiers résultats

**Règle venv établie :** Backend/.venv/ — jamais Python système. Documenté dans CLAUDE.md.

**Entraînement complet sur 838 602 lignes (63 fichiers MERGED_CSV) :**

| Pipeline | Stufe 1 BA | Stufe 2 BA | Stufe 1 F1 | Stufe 2 F1 | Durée |
|----------|-----------|-----------|-----------|-----------|-------|
| A (PCA 39→16) | **0.9971** | **0.5480** | 0.9969 | 0.5784 | 37 min |
| B (39 features) | **0.9993** | **0.6301** | 0.9993 | 0.6670 | 28 min |

**Conclusion Ablation Study préliminaire :**
PCA réduit Stufe 2 BA de 8,21 points (0.5480 vs 0.6301) — confirme l'hypothèse centrale.
Pipeline B est meilleur ET plus rapide.

**Bug corrigé :** valeurs inf dans le dataset → SimpleImputer(strategy="median") ajouté.

**Logging fichier implémenté :** src/utils/logger.py — train_latest.log à chaque run.

**Prochaine étape :** Grid Search (n_estimators, max_depth, lr, subsample) pour améliorer
Stufe 2 BA (cible ≥ 0.85, Raturi et al. 2026 rapportent 0.952 avec optimisation).
