# TO-DO.md — Backlog Complet du Projet Backend ML IoT IDS
## Derniere mise a jour : 2026-06-15 (Re-Run Fundierung Paper)

---

## 2026-06-15 — Re-Run zur Fundierung des Papers (Issue #15)

[x] scripts/rerun_all.sh : vollstaendige deterministische Reproduktion aller Konfigurationen
[x] Standard-Config-Metriken persistiert (metrics_pipeline_{A,B}_standard.json)
[x] scripts/regen_perclass_b_besthp.py : Per-Class B Best-HP nobalanced reproduziert
[x] Endzustand Artefakte : stage*_A=Best-HP, stage*_B=Balanced (passend zu SHAP/Figuren)
[x] Tests gruen : 112 passed, 97% Coverage

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
[x] Grid Search Pipeline A + B (TERMINE)
    → Grille : n_estimators [100, 200], max_depth [3, 5], learning_rate [0.05, 0.1], subsample [0.8, 1.0]
    → 16 combinaisons x cv=3 x 2 etages = 96 fits par pipeline
    → Sous-ensemble : max_files=5, n_per_class=50 (~8 000 lignes) pour test rapide
    → Resultats -> results/metrics/best_params_A.json + best_params_B.json
    → Log -> results/logs/train_latest.log (sentinelle TRAINING COMPLETE)
    → Apres Grid Search : reentrainer sur dataset complet avec --retrain
    → Pipeline A : Stufe1 HP={lr=0.1, max_depth=5, n_estimators=200, subsample=0.8} | BA=0.9969
                   Stufe2 HP={lr=0.05, max_depth=3, n_estimators=100, subsample=1.0} | BA=0.5384
    → Pipeline B : Stufe1 HP={lr=0.05, max_depth=5, n_estimators=100, subsample=1.0} | BA=0.9994
                   Stufe2 HP={lr=0.05, max_depth=3, n_estimators=200, subsample=0.8} | BA=0.6479
    → Resultats sauvegardes : results/metrics/best_params_A.json + best_params_B.json
    → Note : Grid Search sur sous-ensemble (8 045 lignes). Reentrainement complet requis.
[x] Reentrainement complet Pipeline A avec meilleurs HP (2026-05-31)
    → BA1=0.9985 BA2=0.5364 F1=0.5644 | Duree 3265s | Modeles + test_data_A.npz sauvegardes
    → Observation : HP optimises sur subset ne generalisent pas mieux (BA2 retrain < Standard HP)
[x] Reentrainement complet Pipeline B avec meilleurs HP (2026-05-31 09:53:12)
    → BA1=0.9992, BA2=0.6285, F1-2=0.6652, Duree=2317s
    → Modeles + test_data_B.npz sauvegardes ✅
[x] Analyse post-reentrainement Pipeline A : HP optimises sous-ensemble ne generalisent pas (BA2 0.5364 < 0.5480)
[x] Analyse post-reentrainement Pipeline B : HP optimises sous-ensemble ne generalisent pas (BA2 0.6285 < 0.6301)
[x] Klassengewichtung sample_weight='balanced' Stufe 2 (Issue #3, 2026-05-31)
    → Code : balanced_stage2 param (hierarchical_classifier, _core, train_pipelines)
    → Pipeline B balanced : BA2 0.6285 -> 0.7261 (+9.76 pts)
    → Recall classes rares : Brute-Force 0.299->0.646, Web-based 0.192->0.578
    → Amelioration la plus efficace contre le desequilibre (vs Grid Search +0.018)
    → BA-Ziel 0.85 toujours non atteint mais ecart fortement reduit (documenté)
[x] Decision Issue #3 (Session 10, 2026-05-31) : BA=0.7261 accepte comme resultat definitif
    → Brainstorming : options SMOTE, poids manuels, Grid Search complet analysees
    → SMOTE : Hosseini et al. (2025) documentent limites oversampling donnees reseau
    → Grid Search complet : ~100h calcul, non realiste avant deadlines
    → Tradeoff balanced deja observe (Reconnaissance -33.6 pts) -- augmenter aggraverait
    → Decision etudiant : honneteté scientifique, 0.7261 defendable, discuter dans Diskussion
    → Issue #3 fermee 2026-05-31 avec resultat reel documente

---

## 🔵 P4 — Qualité et Robustesse (Issue Backend #10 et #11 -- essentiellement termines)

[x] src/evaluation/metrics.py ✅ (Session 7)
    → evaluate_stage1(), evaluate_stage2(), accuracy_vs_balanced_accuracy(), full_report()
    → 7 tests unitaires, 96% coverage
[x] src/evaluation/confusion_matrix.py ✅ (Session 7)
    → plot_and_save_stage1(), plot_and_save_stage2() -- export PNG vers results/figures/
    → Titres corriges (-- -> :) pour respect regle gedankenstriche
[x] src/explainability/shap_analysis.py ✅ (Session 8 : correction ADR-005)
    → compute_stage1_shap() : SHAP TreeExplainer (exact, Stage 1 binaire)
    → compute_stage2_shap() : PermutationExplainer(predict_proba) (Stage 2 multiclass)
    → ShapResult dataclass, get_misclassified_instances()
[x] src/explainability/shap_visualizer.py ✅ (Session 8 : correction titres)
    → plot_summary_stage1/2, plot_bar_global_importance, plot_waterfall_misclassified
    → Export PNG vers results/figures/
[x] src/utils/logger.py ✅ (Session 5)
[x] tests/test_explainability.py ✅ (Session 8 -- 21 tests)
[x] tests/test_logger.py ✅ (Session 8 -- 9 tests, 100% logger coverage)
[x] tests/test_main.py ✅ (Session 8 -- 11 tests, 96% main coverage)
[x] tests/test_evaluation.py -- +3 tests confusion matrix (Session 8)
[x] Couverture de tests > 80% : 97% atteint (111 tests) ✅ (Session 8)
[x] Executer SHAP sur modeles reentraines + generer les figures PNG ✅ (2026-05-31)
    → Pipeline A : evaluate_and_explain.py complete 09:43:29
    → Pipeline B : evaluate_and_explain.py complete ~10:00
    → 30 PNG dans results/figures/ + 6 copies dans paper/figures/
[x] Validation semantique SHAP ✅
    → Brute-Force : SSH en top-5 -- valide signature attaque ✅
    → DoS/DDoS Stufe 1 : Number, Protocol_Type -- consistent avec flut/scan ✅
    → Spoofing : Min/Number/Max au lieu ARP/ICMP -- possible artefact dataset
    → Documente dans paper evaluation.tex section "Semantische Validierung"

---

## ⚪ P5 — Finalisation (Issue Backend #12 -- deadline 2026-06-22)

[x] Export et serialisation des modeles (joblib, format .pkl -> models_artifacts/) ✅ (Session 5+8)
    → preprocessor_{A,B}.pkl, stage1_{A,B}.pkl, stage2_{A,B}.pkl sauvegardes
[x] Documentation technique dans docs/ ✅ (Session 8)
    → docs/architecture_decision_records.md : 7 ADRs
    → docs/label_mapping.md : tableau complet 33 labels + features
[x] README.md du Backend/ (Session 7) ✅
[x] Generation des figures finales pour le Paper ✅
    → confusion_matrix_stage{1,2}_pipeline{A,B}.png ✅
    → shap_global_stage{1,2}_pipeline{A,B}.png ✅
    → shap_summary_stage1_pipeline{A,B}.png ✅
    → shap_summary_stage2_{class}_pipeline{A,B}.png (6 classes x 2 pipelines) ✅
    → shap_waterfall_stage{1,2}_pipeline{A,B}_idx*.png ✅
[x] Figures copiees vers paper/figures/ via update_paper_results.py ✅
[x] Export des metriques finales en JSON (results/metrics/) ✅
    → full_report_pipeline_{A,B}.json ✅
    → shap_global_stage{1,2}_pipeline{A,B}.json ✅
    → misclassified_instances_pipeline{A,B}.json ✅
[x] Integrer resultats dans paper evaluation.tex ✅
    → Tableau B Best HP : BA1=0.9992 BA2=0.6285 F1-2=0.6652
    → tab:shap_top5 rempli avec top-5 features reelles Pipeline B
    → fig:cm_stage2_a, fig:cm_stage2_b, fig:shap_global_a, fig:shap_global_b actives
    → tab:perclass_a, tab:perclass_b avec donnees reelles
[x] Fermer issues GitHub #9, #10, #11, #12 (fermees -- Session 8/9)
[x] Fermer issue GitHub #3 (fermee Session 10, BA=0.7261 resultat definitif accepte)

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
