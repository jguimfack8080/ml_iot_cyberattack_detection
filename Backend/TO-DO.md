# TO-DO.md — Backlog Complet du Projet Backend ML IoT IDS
## Dernière mise à jour : 2026-05-30

---

## 🔴 P1 — Bloquant (à résoudre avant tout développement)

[x] Décision sur le format de données : MERGED_CSV retenu (labels présents, 39 features + Label)
[x] Vérifier les features disponibles : 39 features réelles (PCA sera 39→16, pas 46→16)
    → Divergence vs. Lastenheft (qui cite 46) documentée — à mentionner dans le Paper
[x] Valider la liste complète des labels dans MERGED_CSV
    → 34 labels uniques confirmés (scan Merged01-04)
    → Tous en ALL_CAPS : DDOS-*, DOS-*, MIRAI-*, RECON-*, SPOOFING, BRUTE-FORCE, WEB, BENIGN
[x] Validation de la structure du projet Backend/
[x] Décision sur BACKDOOR_MALWARE : DROP — instances filtrées avant entraînement
    → POURQUOI : (1) Absent des 8 catégories définies par Neto et al. (2023) et Raturi et al. (2026)
                 (2) Extrêmement rare : ~4 instances sur 50 000 lignes échantillonnées (< 0,01 %)
                 (3) Une 9e classe avec aussi peu d'instances détruirait la Balanced Accuracy
                 (4) Le scope scientifique de ce travail est explicitement limité aux 8 catégories
    → COMMENT : pd.DataFrame[df['category'] != 'BACKDOOR_MALWARE'] dans label_mapper.py
    → DOCUMENTATION : À mentionner dans Paper/src/methodik.tex (Datenvorbereitung)
[x] Décision sur la stratégie de chargement mémoire (63 fichiers × ~140 MB = ~8,5 GB)
    → DÉCISION : Echantillonnage stratifié sur l'ensemble des 63 fichiers (Best Practice retenu)
    → POURQUOI : (1) Aucune perte d'information — TOUS les 63 fichiers contribuent
                 (2) RAM-safe — on ne charge jamais plus de 1-2 fichiers simultanément
                 (3) Reproductible — random_state=42 à chaque lecture
                 (4) Représentatif — chaque classe est échantillonnée proportionnellement
                 (5) Compatible avec scikit-learn GradientBoosting (pas besoin de partial_fit)
    → COMMENT : Pour chaque fichier Merged_i, lire par chunks, garder N lignes par classe présente
                Concaténer toutes les contributions → DataFrame final de ~500 000 lignes
    → PARAMÈTRE : n_samples_per_class_per_file configurable (défaut : 500 lignes/classe/fichier
                  → ~500 × 34 classes × 63 fichiers ≈ 1 071 000 lignes max, RAM ~400 MB)

---

## 🟠 P2 — Pipeline A : avec PCA (en cours)

[x] src/data/constants.py
    → Source unique vérité : noms colonnes, LABEL_TO_CATEGORY (33 labels), EXCLUDED_LABELS, CATEGORIES
    → N_FEATURES=39, N_PCA_COMPONENTS=16, RANDOM_STATE=42
    → Tests : 100% couverture
[x] src/data/loader.py
    → load_stratified() : lit chaque fichier complètement, sample N lignes/label, gc.collect()
    → Normalisation noms colonnes (Protocol_Type, Tot_sum, Tot_size)
    → Paramètres : data_dir, n_per_class_per_file=500, random_state=42, max_files (test mode)
    → Tests : 5 tests unitaires, 90% couverture
[x] src/data/label_mapper.py
    → apply_label_mapping() : drop BACKDOOR_MALWARE, map 33 labels → 8 catégories, add is_dos_ddos
    → validate_split_labels() : vérifie qu'aucune classe test est absente du train
    → get_stage2_mask() : masque booléen non-DoS/DDoS
    → Tests : 10 tests unitaires, 100% couverture
[x] tests/test_data_loader.py : 10 tests, tous passants ✅
[x] tests/test_data_label_mapper.py : 10 tests, tous passants ✅
    → 20/20 tests passent — coverage global 76% (objectif P4 : >80%)
[x] src/features/preprocessor_a.py
    → sklearn Pipeline(StandardScaler, PCA(n_components=16, random_state=42))
    → build_preprocessor_a() + get_explained_variance_ratio()
    → Tests : 8 tests, 100% coverage
[x] src/models/stage1_classifier.py
    → GradientBoostingClassifier binaire (DoS/DDoS vs. non-DoS)
    → Stage1Config dataclass + build_stage1_classifier() + get_grid_search_space()
    → Tests : 4 tests, 95% coverage
[x] src/models/stage2_classifier.py
    → GradientBoostingClassifier multiclasse (6 classes non-DoS)
    → Stage2Config dataclass + build_stage2_classifier()
    → Tests : 2 tests, 95% coverage
[x] src/models/hierarchical_classifier.py
    → HierarchicalClassifier : fit() / predict() / predict_stage1() / predict_stage2()
    → Validation pré-fit : reject si 0 non-DoS instances ou 1 seule classe
    → SHAP : accéder clf.stage1 et clf.stage2 directement
    → Tests : 8 tests, 95% coverage
[x] src/pipelines/_core.py
    → PipelineConfig dataclass + TrainedPipeline dataclass
    → run_pipeline() : 7 étapes load→map→split→preprocess→train→metrics
    → _compute_basic_metrics() : BA + F1-macro pour Stufe 1 et Stufe 2
    → Tests : couverts via test_pipelines.py, 98% coverage
[x] src/pipelines/pipeline_a.py
    → run_pipeline_a(config) → appelle run_pipeline() avec preprocessor_a
    → Tests : 8 tests, 100% coverage
[x] tests/conftest.py : fixtures communes (sample_df, mapped_df, split_arrays, preprocessed_arrays, fitted_hierarchical)
[x] tests/test_features_preprocessors.py : 13 tests ✅
[x] tests/test_models_hierarchical.py : 12 tests ✅
[x] tests/test_pipelines.py : 10 tests ✅ (Pipeline A + B + comparaison A vs B)
    → Bug corrigé : PyArrow backend pandas incompatible avec sklearn → .to_numpy()

---

## 🟡 P3 — Pipeline B : sans PCA ✅ TERMINÉ (implémenté avec P2)

[x] src/features/preprocessor_b.py
    → sklearn Pipeline(StandardScaler uniquement) — 39 features conservées
    → Tests : 5 tests, 100% coverage
[x] src/pipelines/pipeline_b.py
    → run_pipeline_b(config) → appelle run_pipeline() avec preprocessor_b
    → Tests : 4 tests dans test_pipelines.py + 2 tests comparaison A vs B ✅
[x] Comparaison A vs B : test_a_output_narrower_than_b, test_both_have_same_test_set_size ✅

## Résultats tests globaux (Pipeline A + B + tous modules)
    → 60/60 tests passent ✅
    → Coverage global : 89% (objectif P4 : >80% ✅ déjà atteint)
    → Modules 100% : constants, label_mapper, preprocessor_a, preprocessor_b, pipeline_a, pipeline_b
    → Modules 95-98% : hierarchical_classifier, stage1, stage2, _core

[x] Entraînement Pipeline A sur données réelles (MERGED_CSV, 63 fichiers)
    → Stufe 1 BA=0.9971 F1=0.9969 | Stufe 2 BA=0.5480 F1=0.5784 | 2240s
    → Modèles : preprocessor_A.pkl, stage1_A.pkl, stage2_A.pkl ✅
[x] Entraînement Pipeline B sur données réelles
    → Stufe 1 BA=0.9993 F1=0.9993 | Stufe 2 BA=0.6301 F1=0.6670 | 1657s
    → Modèles : preprocessor_B.pkl, stage1_B.pkl, stage2_B.pkl ✅
[x] src/utils/logger.py — logging fichier implémenté
    → train_latest.log + train_YYYYMMDD_HHMMSS.log à chaque run
    → Sentinelles TRAINING STARTED / TRAINING COMPLETE / TRAINING FAILED
[ ] Grid Search Pipeline A (URGENT — améliorer Stufe 2 BA de 0.5480 → ≥0.85)
    → Grille : n_estimators [100, 200], max_depth [3, 5], learning_rate [0.05, 0.1], subsample [0.8, 1.0]
    → Utiliser GridSearchCV avec cv=3 sur sous-ensemble (RAM + temps)
[ ] Grid Search Pipeline B (même grille)
[ ] Analyse post-Grid Search : comparer A_optimisé vs B_optimisé (Ablation Study finale)

---

## 🔵 P4 — Qualité & Robustesse (après A et B fonctionnels)

[ ] src/evaluation/metrics.py
    → balanced_accuracy_score, f1_score (macro), classification_report par classe
    → Comparaison Accuracy vs. Balanced Accuracy (démonstration biais)
[ ] src/evaluation/confusion_matrix.py
    → Matrices de confusion séparées : Stufe 1 (binaire) et Stufe 2 (multiclasse)
    → Export en PNG vers results/figures/
[ ] src/explainability/shap_analysis.py
    → SHAP TreeExplainer sur GradientBoosting (Stufe 1 et Stufe 2 séparément)
    → Global : mean(|SHAP|) par feature et par classe
    → Local : top-k instances mal classifiées, SHAP values par instance
[ ] src/explainability/shap_visualizer.py
    → Summary Plot (beeswarm) par classe
    → Waterfall Plot pour instances individuelles (Fehlklassifikationen)
    → Force Plot pour cas locaux sélectionnés
    → Export PNG vers results/figures/
[ ] src/utils/logger.py
    → Logging centralisé : métriques, hyperparamètres, durées, chemins
[ ] Validation sémantique SHAP
    → Comparer les top features SHAP par classe avec les signatures d'attaques documentées
    → DoS/DDoS : Rate, Number, syn_flag_number attendus en tête
    → Spoofing : ARP, ICMP, Protocol_Type
    → Brute-Force : connexions répétées, SSH, Telnet
    → Référence : Neto et al. (2023), DOI 10.3390/s23135941
[ ] Couverture de tests > 80% (pytest --cov=src)

---

## ⚪ P5 — Finalisation (dernière phase)

[ ] Export et sérialisation des modèles (joblib, format .pkl → models_artifacts/)
[ ] Documentation technique dans docs/
    → architecture_decision_records.md
    → label_mapping.md (tableau complet des 34 labels → 8 catégories)
[ ] README.md du Backend/ (instructions d'installation et d'exécution)
[ ] Génération des figures finales pour le Paper (results/figures/)
[ ] Export des métriques finales en JSON/CSV (results/metrics/)
[ ] Intégration des résultats dans Paper/src/methodik.tex et erwartete_ergebnisse.tex

---

## Deadlines (depuis jguimfackjeuna-vortrag-umsetzungsplan.md)

| Date | Jalon |
|------|-------|
| 2026-06-01 | Motivationsreview — premiers résultats Pipeline A visibles |
| 2026-06-08 | Ergebnisfeststellung — Pipelines A+B complètes, SHAP prêt |
| 2026-06-15 | Kernkapitel-Abgabe — Paper Methodik + Résultats rédigés |
| 2026-06-22 | Review-Version eingereicht |
| 2026-07-13 | Vortrag (Prüfungsleistung) |
| 2026-07-27 | Endgültige Abgabe |

---

→ P2 et P3 détaillés — prêts pour implémentation dès résolution des 2 P1 ouverts
→ Ne jamais avancer sur P2 si un P1 reste ouvert
