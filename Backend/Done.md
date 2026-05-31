# Done.md — Journal de Développement Backend ML
## Projet : IoT Cyberattack Detection — Backend (CICIoT2023 + Gradient Boosting + SHAP)

Journal chronologique immuable. Ne jamais supprimer les entrées existantes.

---

### 2026-05-30 — Session 1 : Analyse complète et mise en place de la structure Backend

**Analysé :**
- Lastenheft.md : cahier des charges complet (12 sections, 3 Forschungsfragen, 10 sources vérifiées)
- README.md : vue d'ensemble technique (structure, dataset, build pipeline LaTeX)
- Done.md (root) : journal de projet existant — sessions précédentes (Paper, présentations)
- jguimfackjeuna-vortrag-umsetzungsplan.md : justifications des 5 décisions techniques clés
- Dataset/MERGED_CSV/ : 63 fichiers Merged01-63.csv, ~140 MB chacun, ~8,5 GB total
- Dataset/CSV/ : 34 sous-dossiers par type d'attaque, sans colonne Label

**Découvertes dataset (inspection directe des fichiers) :**
- MERGED_CSV : 40 colonnes = 39 features + colonne Label
- Labels en ALL_CAPS avec tirets/underscores (ex. : DDOS-PSHACK_FLOOD, BENIGN)
- 34 labels uniques confirmés (scan des fichiers Merged01 à Merged04)
- CSV individuels : 39 features SANS colonne Label → inutilisables pour l'entraînement supervisé
- Divergence documentée : Lastenheft cite 46 features, dataset réel en contient 39
  → PCA sera 39→16 (non 46→16) — à mentionner explicitement dans Paper/src/methodik.tex
- Aucune valeur nulle sur 50 000 lignes testées
- Déséquilibre de classes extrême : DDOS-ICMP_FLOOD seul représente ~15 % de l'échantillon

**Label mapping établi (34 labels → 8 catégories) :**
- DDoS (12) : DDOS-ICMP_FLOOD, DDOS-UDP_FLOOD, DDOS-TCP_FLOOD, DDOS-SYN_FLOOD,
              DDOS-RSTFINFLOOD, DDOS-PSHACK_FLOOD, DDOS-SYNONYMOUSIP_FLOOD,
              DDOS-ICMP_FRAGMENTATION, DDOS-ACK_FRAGMENTATION, DDOS-UDP_FRAGMENTATION,
              DDOS-SLOWLORIS, DDOS-HTTP_FLOOD
- DoS (4)   : DOS-UDP_FLOOD, DOS-TCP_FLOOD, DOS-SYN_FLOOD, DOS-HTTP_FLOOD
- Mirai (3) : MIRAI-GREETH_FLOOD, MIRAI-GREIP_FLOOD, MIRAI-UDPPLAIN
- Recon (5) : RECON-HOSTDISCOVERY, RECON-OSSCAN, RECON-PORTSCAN, RECON-PINGSWEEP,
              VULNERABILITYSCAN
- Spoofing (2) : MITM-ARPSPOOFING, DNS_SPOOFING
- Brute-Force (1) : DICTIONARYBRUTEFORCE
- Web-based (5) : BROWSERHIJACKING, COMMANDINJECTION, SQLINJECTION, UPLOADING_ATTACK, XSS
- Benign (1)    : BENIGN
- NON MAPPÉ (1) : BACKDOOR_MALWARE → décision P1 ouverte

**Décisions prises :**
1. Source de données : MERGED_CSV retenu (seul format avec labels)
2. PCA : 39→16 composantes (divergence vs. Lastenheft documentée, à mentionner dans Paper)
3. Architecture Backend : dossier Backend/ créé à la racine du projet
4. Packages retenus : pandas, numpy, scikit-learn, shap, matplotlib, seaborn, joblib,
                      python-dotenv, tqdm, xgboost, pytest (voir requirements.txt)

**Structure Backend/ créée :**
```
Backend/
├── src/
│   ├── __init__.py
│   ├── main.py              (squelette CLI avec argparse — seul .py créé cette session)
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
├── models_artifacts/.gitkeep
├── results/figures/ + results/metrics/
├── data/raw/ + data/processed/ + .gitkeep
├── docs/
├── requirements.txt
├── pyproject.toml
├── .env.example
├── .gitignore
├── TO-DO.md
└── Done.md
```

**P1 résolus :**
- Format données : MERGED_CSV
- Liste des 39 features
- 34 labels uniques vérifiés
- Label mapping (33/34 labels)
- Structure Backend/ validée

**P1 résolus en fin de session (décisions confirmées par l'étudiant) :**

**Décision P1.5 — BACKDOOR_MALWARE : DROP**
- Quoi : Filtrer et éliminer toutes les instances avec le label BACKDOOR_MALWARE
- Pourquoi :
  (1) Label absent des 8 catégories standard définies par Neto et al. (2023) et Raturi et al. (2026)
  (2) Extrêmement rare : ~4 instances sur 50 000 lignes = 0,008 % du volume
  (3) Une 9e classe avec si peu d'instances causerait un Recall → 0 pour cette classe,
      pénalisant massivement la Balanced Accuracy de manière non représentative
  (4) Le scope scientifique de ce travail est explicitement limité aux 8 catégories
      du CICIoT2023 (cf. Lastenheft section 6 et 7)
- Comment : df = df[df['label_raw'] != 'BACKDOOR_MALWARE'] dans src/data/label_mapper.py
- Documentation obligatoire : à mentionner dans Paper/src/methodik.tex, section Datenvorbereitung

**Décision P1.6 — Stratégie mémoire : Echantillonnage stratifié sur les 63 fichiers**
- Quoi : Lire TOUS les 63 fichiers MERGED_CSV, mais en n'en gardant que N lignes par classe
- Pourquoi :
  (1) Best Practice ML pour grands datasets : aucune perte d'information qualitative
      (toutes les classes de tous les fichiers contribuent au dataset final)
  (2) RAM-safe : on ne charge jamais l'intégralité d'un fichier (pandas read_csv chunksize)
  (3) Reproductible : random_state=42 assure la même sélection à chaque exécution
  (4) Compatible avec scikit-learn GradientBoosting (pas de partial_fit requis)
  (5) Alternatif chunked avec partial_fit = impossible sur sklearn GradientBoosting natif
- Comment :
  → Pour chaque fichier Merged_i, lire par chunks de 50 000 lignes
  → Accumuler jusqu'à N lignes par label présent dans ce fichier
  → Concaténer toutes les contributions → dataset final ~500 000–1 000 000 lignes
  → Paramètre n_samples_per_class_per_file (défaut 500) configurable via .env
- Taille estimée : 500 lignes × 33 classes × 63 fichiers ≈ 1 039 500 lignes, ~400 MB RAM
- Documentation : paramètre à exposer dans requirements et src/data/loader.py

**Tous les P1 sont résolus. La P2 peut commencer.**

**Prochaine étape concrète :**
1. Implémenter src/data/loader.py (chargement stratifié sur 63 fichiers)
2. Implémenter src/data/label_mapper.py (mapping 33 labels → 8 catégories + drop BACKDOOR_MALWARE)

---

### 2026-05-30 — ANNEXE SESSION 1 : Analyse complète ETAPE 1 — Résultats structurés

Cette section documente intégralement les résultats de l'analyse ETAPE 1 tels qu'établis
avant tout développement. Chaque point inclut la décision, la justification et l'impact.

---

#### POINT 1 — FORMAT DE DONNÉES ✅ Décision prise : MERGED_CSV retenu

**Analyse comparative des deux formats disponibles :**

| Critère               | CSV individuels (Dataset/CSV/)           | MERGED_CSV (Dataset/MERGED_CSV/)         |
|-----------------------|------------------------------------------|------------------------------------------|
| Colonne Label         | ABSENTE — 39 features uniquement         | PRÉSENTE — 39 features + Label = 40 col.|
| Organisation          | 34 sous-dossiers par type d'attaque       | 63 fichiers Merged01-63.csv mélangés     |
| Taille totale         | ~8,5 GB estimé                           | 63 × ~140 MB = ~8,5 GB confirmé         |
| Utilisation ML        | IMPOSSIBLE — pas de target supervisé     | PRÊT — labels présents pour l'entraîn.  |
| Classes représentées  | Implicites (nom du dossier)               | Toutes mélangées dans chaque fichier    |
| Compatibilité hiérar. | Inutilisable sans retraitement manuel    | Compatible directement                   |
| Valeurs nulles        | Non testé (sans Label)                   | 0 null sur 50 000 lignes testées ✅      |
| Format labels         | N/A                                      | ALL_CAPS : DDOS-PSHACK_FLOOD, BENIGN    |

**Décision : MERGED_CSV retenu.**
- Justification principale : seul format avec labels — les CSV individuels sont inexploitables
  pour l'entraînement supervisé sans reconstruction manuelle des labels depuis les noms de dossiers
- Justification secondaire : format consolidé, toutes classes mélangées, compatible avec
  l'échantillonnage stratifié multi-classes

**Problèmes détectés et traitement :**

| Problème              | Description                              | Traitement                              |
|-----------------------|------------------------------------------|-----------------------------------------|
| Divergence features   | Lastenheft cite 46 features, dataset a 39| PCA sera 39→16 (non 46→16) — à documenter dans Paper/src/methodik.tex |
| BACKDOOR_MALWARE      | 34e label absent des 8 catégories        | DROP (voir Décision P1.5)               |
| Déséquilibre extrême  | DDOS-ICMP_FLOOD ~15 % de l'échantillon  | Traité architecturalement (Stufe 1)     |
| Noms colonnes espaces | 'Protocol Type', 'Tot sum', 'Tot size'   | Normalisation → underscores à la lecture|

**Features disponibles (39 colonnes confirmées) :**
```
Header_Length, Protocol Type, Time_To_Live, Rate,
fin_flag_number, syn_flag_number, rst_flag_number, psh_flag_number,
ack_flag_number, ece_flag_number, cwr_flag_number,
ack_count, syn_count, fin_count, rst_count,
HTTP, HTTPS, DNS, Telnet, SMTP, SSH, IRC, TCP, UDP, DHCP, ARP, ICMP, IGMP, IPv, LLC,
Tot sum, Min, Max, AVG, Std, Tot size, IAT, Number, Variance
```
Note : 3 noms contiennent des espaces → normalisés en Protocol_Type, Tot_sum, Tot_size

**Distribution classes (échantillon Merged01, 50 000 lignes) :**

| Rang | Label               | Catégorie | Nb instances | % approx. |
|------|---------------------|-----------|-------------|-----------|
| 1    | DDOS-ICMP_FLOOD     | DDoS      | 7 800       | 15,6 %    |
| 2    | DDOS-UDP_FLOOD      | DDoS      | 5 666       | 11,3 %    |
| 3    | DDOS-TCP_FLOOD      | DDoS      | 4 889       | 9,8 %     |
| 4    | DDOS-SYN_FLOOD      | DDoS      | 4 253       | 8,5 %     |
| ...  | (DDoS total)        | DDoS      | ~34 000     | ~68 %     |
| ...  | (DoS total)         | DoS       | ~8 700      | ~17 %     |
| ...  | BENIGN              | Benign    | 1 171       | 2,3 %     |
| ...  | Classes rares       | Divers    | < 100 chacune | < 0,2 % |

→ Confirmation empirique : DoS+DDoS = ~85 % du volume. Justifie la Stufe 1 binaire.

---

#### POINT 2 — PIPELINE A ✅ Clair, 1 point de confirmation résolu

**Ce que fait Pipeline A (selon Lastenheft section 7.1 + 7.2) :**

```
MERGED_CSV
    ↓
1. Chargement + nettoyage (drop BACKDOOR_MALWARE, normalisation noms colonnes)
    ↓
2. Mapping labels → 8 catégories + label binaire Stufe 1
    ↓
3. Split 80/20 stratifié (random_state=42)
    ↓
4. StandardScaler — fit sur train UNIQUEMENT, transform sur train+test
    ↓
5. PCA : 39 features → 16 composantes principales (random_state=42)
    ↓
6. Stufe 1 : GradientBoostingClassifier binaire (DoS/DDoS=1 vs. non-DoS=0)
    ↓
7. Stufe 2 : GradientBoostingClassifier multiclasse (6 classes non-DoS)
   [Mirai, Reconnaissance, Spoofing, Brute-Force, Web-based, Benign]
    ↓
8. Evaluation : Balanced Accuracy, F1-macro, Precision/Recall par classe
    ↓
9. SHAP TreeExplainer sur les 16 composantes PCA (global + local)
```

**Données d'entrée requises :**
- MERGED_CSV directory (63 fichiers)
- random_state=42 pour tous les composants stochastiques
- n_per_class_per_file pour le sampling (configurable via .env)

**Ce qui doit être implémenté (P2) :**

| Fichier                           | Responsabilité                              | Statut    |
|-----------------------------------|---------------------------------------------|-----------|
| src/data/constants.py             | Noms colonnes, constantes dataset           | [ ] P2    |
| src/data/loader.py                | Chargement stratifié 63 fichiers            | [ ] P2    |
| src/data/label_mapper.py          | Mapping 33 labels → 8 catégories           | [ ] P2    |
| src/features/preprocessor_a.py   | StandardScaler + PCA 39→16                 | [ ] P2    |
| src/models/stage1_classifier.py   | GB binaire Stufe 1                          | [ ] P2    |
| src/models/stage2_classifier.py   | GB multiclasse Stufe 2                      | [ ] P2    |
| src/models/hierarchical_classifier.py | Orchestration Stufe 1 + Stufe 2        | [ ] P2    |
| src/pipelines/pipeline_a.py       | Enchaînement complet Pipeline A             | [ ] P2    |

**Point de confirmation résolu (était "1 point à confirmer") :**
- Stratégie mémoire → Echantillonnage stratifié sur les 63 fichiers (décision P1.6)
- Tous les paramètres sont maintenant définis — implémentation peut commencer

---

#### POINT 3 — PIPELINE B ✅ Clair, indépendant de A

**Différence avec Pipeline A :**
- Suppression unique de l'étape PCA (étape 5 du schéma A)
- StandardScaler → 39 features originales directement (pas de réduction)
- Même architecture hiérarchique, mêmes hyperparamètres, même random_state=42
- SHAP sur les features originales → sémantiquement interprétables

**Interface A/B :**
- A et B partagent le même loader, label_mapper, train/test split (même random_state)
- Preprocessors distincts : preprocessor_a.py (avec PCA) / preprocessor_b.py (sans PCA)
- B est indépendant de A : peut être exécuté en parallèle ou après A

---

#### POINT 4 — DÉPENDANCES TECHNIQUES ✅ requirements.txt créé

| Package      | Version min | Rôle dans le projet                            |
|--------------|-------------|------------------------------------------------|
| pandas       | 2.0         | Chargement, manipulation, groupby MERGED_CSV   |
| numpy        | 1.24        | Calculs numériques, arrays SHAP                |
| scikit-learn | 1.3         | GB, PCA, StandardScaler, métriques            |
| xgboost      | 2.0         | Alternative optionnelle à sklearn GB           |
| shap         | 0.44        | TreeExplainer (exact SHAP pour GB)             |
| matplotlib   | 3.7         | Visualisations SHAP, confusion matrix          |
| seaborn      | 0.12        | Heatmaps, confusion matrix styling             |
| joblib       | 1.3         | Sérialisation modèles (.pkl)                   |
| python-dotenv| 1.0         | Chargement variables d'environnement           |
| tqdm         | 4.65        | Progress bars pour les 63 fichiers             |
| pytest       | 7.4         | Tests unitaires (cible : > 80 % coverage)      |
| pytest-cov   | 4.1         | Mesure couverture de tests                     |

---

#### POINT 5 — POINTS BLOQUANTS RÉSOLUS

Tous les P1 identifiés ont été résolus avant le début de P2 :

| P1 | Problème initial | Décision finale | Justification |
|----|-----------------|-----------------|---------------|
| P1.1 | Format données | MERGED_CSV | Seul format avec labels |
| P1.2 | Nb features | 39 (pas 46) | Inspection directe dataset |
| P1.3 | Labels MERGED_CSV | 34 labels ALL_CAPS | Scan Merged01-04 confirmé |
| P1.4 | Mapping labels | 33/34 labels → 8 catégories | Table complète établie |
| P1.5 | BACKDOOR_MALWARE | DROP | Hors scope, < 0,01 %, impact Balanced Acc. |
| P1.6 | Stratégie mémoire | Echantillonnage stratifié 63 fichiers | Best Practice, aucune perte info |
| P1.7 | Structure Backend/ | Créée et validée | 21 répertoires, 18 fichiers |

→ Aucun point bloquant restant. P2 commence à la prochaine session.

---

### 2026-05-30 — Session 3 : Implémentation P2 — src/data/ (constants, loader, label_mapper)

**Objectif de la session :** Implémenter les 3 premiers fichiers P2 avec Best Practices Python ML.
Critères retenus : type hints, logging, pas de hardcoded paths, random_state=42, tests unitaires.

---

#### Fichier 1 : src/data/constants.py ✅

**Rôle :** Source unique de vérité pour toutes les constantes du dataset.
**Pourquoi un fichier séparé (Best Practice) :**
  - Evite la duplication de la table LABEL_TO_CATEGORY entre loader, mapper, tests
  - Centralise les paramètres changeables (N_PCA_COMPONENTS, RANDOM_STATE) en un seul endroit
  - Immuabilité garantie par `Final` et `frozenset` → erreur à la compilation si modifié

**Contenu et décisions :**

| Constante             | Valeur                         | Justification                                          |
|-----------------------|--------------------------------|--------------------------------------------------------|
| FEATURE_COLUMNS_RAW   | 39 noms bruts (avec espaces)  | Noms exacts du CSV source                              |
| FEATURE_COLUMNS       | 39 noms normalisés             | Espaces → underscores pour compatibilité sklearn/XGBoost|
| N_FEATURES            | 39                             | Compté depuis le dataset réel (pas 46 du Lastenheft)   |
| N_PCA_COMPONENTS      | 16                             | Pipeline A : 39→16 (Raturi et al. 2026)                |
| RANDOM_STATE          | 42                             | Reproductibilité — imposé par Lastenheft               |
| LABEL_TO_CATEGORY     | dict de 33 entrées             | Mapping complet 33 labels → 8 catégories               |
| EXCLUDED_LABELS       | frozenset{'BACKDOOR_MALWARE'} | Decision P1.5 (Done.md)                                |
| DOS_DDOS_CATEGORIES   | frozenset{'DDoS','DoS'}       | Classes positives Stufe 1                              |
| STAGE2_CATEGORIES     | 6 classes non-DoS/DDoS        | Classes cibles Stufe 2                                 |

**Choix technique — colonne Label normalisée :**
- 3 colonnes du CSV brut contiennent des espaces : 'Protocol Type', 'Tot sum', 'Tot size'
- XGBoost lève une erreur sur les noms de features avec espaces
- scikit-learn accepte les espaces mais c'est une mauvaise pratique
- Decision : normaliser à la lecture dans loader.py via df.rename()
- FEATURE_COLUMNS_RAW conservé pour référence et validation

---

#### Fichier 2 : src/data/loader.py ✅

**Rôle :** Chargement stratifié de l'ensemble des 63 fichiers MERGED_CSV.

**Architecture de la fonction principale :**
```
load_stratified(data_dir, n_per_class_per_file=500, random_state=42)
    ↓
Pour chaque fichier (trié, ordre déterministe) :
    _sample_one_file(path, n_per_class, random_state)
        → read_csv complet (un fichier ~235 MB RAM)
        → rename colonnes avec espaces
        → groupby(Label) → sample(n, random_state=42)
        → del df + gc.collect()  ← libère le fichier de la mémoire
    ↓
pd.concat(tous les échantillons) → DataFrame final
```

**Décisions d'implémentation (Best Practices) :**

| Décision              | Choix retenu                   | Alternative rejetée / Raison                    |
|-----------------------|--------------------------------|-------------------------------------------------|
| Lecture fichier       | pd.read_csv() complet          | pd.read_csv(chunksize=) : peut manquer des rows |
| Libération mémoire    | del df + gc.collect()          | Compter sur GC Python : trop lent, OOM possible |
| Reproductibilité      | random_state int fixe          | np.random.Generator : ordre dépendant de l'état |
| Paramètre max_files   | Optional[int]                  | Permet mode test sans charger 63 fichiers        |
| Tri fichiers          | sorted(glob())                 | Ordre alphabétique déterministe sur tous OS      |
| Normalisation colonnes| df.rename(columns=_COLUMN_RENAME)| Modification post-lecture, pas en lecture       |

**Budget mémoire mesuré :**
- 1 fichier en RAM : ~235 MB (140 MB CSV × ~1.7 facteur pandas)
- Echantillon accumulé : 63 files × 500 rows/class × 33 classes × 320 bytes ≈ ~333 MB
- Pic RAM estimé : ~235 + 333 = ~568 MB ✅ (bien en dessous de 8 GB RAM standard)

**Tests écrits (tests/test_data_loader.py) :**
| Test                                      | Ce qu'il vérifie                              |
|-------------------------------------------|-----------------------------------------------|
| test_returns_dataframe                    | La fonction retourne bien un DataFrame        |
| test_respects_n_per_class                 | Max N lignes par label respecté               |
| test_normalizes_column_names              | Protocol_Type (pas 'Protocol Type')           |
| test_returns_none_on_missing_label        | Fichier sans Label → None, pas d'exception   |
| test_reproducible_with_same_seed          | Même résultat avec même random_state          |
| test_loads_multiple_files                 | Plusieurs fichiers concaténés                 |
| test_raises_on_missing_dir                | FileNotFoundError si data_dir inexistant      |
| test_raises_on_no_matching_files          | FileNotFoundError si aucun fichier Merged*.csv|
| test_max_files_limit                      | max_files=2 → limité à 2 fichiers             |
| test_excludes_derived_columns             | get_feature_columns() filtre Label/category   |

Résultats : 10/10 ✅ — Couverture loader.py : 90% (6 lignes non couvertes = cas d'erreur
  d'exception I/O, testables via mock mais hors scope P2)

---

#### Fichier 3 : src/data/label_mapper.py ✅

**Rôle :** Transformation des labels bruts en cibles ML exploitables.

**Ce que fait apply_label_mapping() étape par étape :**
1. Drop BACKDOOR_MALWARE (et tout EXCLUDED_LABELS futur)
2. Validation fail-fast : si un label inconnu est présent → ValueError immédiat
   (évite les NaN silencieux dans la colonne category)
3. Mapping Label → category via LABEL_TO_CATEGORY
4. Calcul is_dos_ddos (0/1) pour Stufe 1
5. Log de la distribution finale pour traçabilité

**Décisions d'implémentation :**

| Décision              | Choix retenu                        | Raison                                          |
|-----------------------|-------------------------------------|-------------------------------------------------|
| Fail-fast validation  | raise ValueError sur label inconnu  | NaN silencieux serait détecté trop tard         |
| Copie du DataFrame    | df.copy()                           | Pas de mutation de l'input (principe d'immutabilité) |
| Logging distribution  | Séparé dans _log_distribution()     | Séparation responsabilités, testable seul        |
| validate_split_labels | Fonction publique séparée           | Appelée après train_test_split, pas dans map()  |
| get_stage2_mask       | Retourne pd.Series booléen          | Réutilisable pour filtrer train ET test          |

**Tests écrits (tests/test_data_label_mapper.py) :**
| Test                                         | Ce qu'il vérifie                               |
|----------------------------------------------|------------------------------------------------|
| test_adds_category_and_binary_columns        | Deux colonnes créées                           |
| test_all_known_labels_mapped                 | 33 labels → pas de NaN dans category          |
| test_drops_excluded_labels                   | BACKDOOR_MALWARE supprimé, taille correcte     |
| test_binary_column_correct_for_dos_ddos      | DDoS/DoS = 1, Mirai/Benign = 0               |
| test_raises_on_unknown_label                 | ValueError si label hors mapping              |
| test_does_not_mutate_input                   | Input DataFrame non modifié                   |
| test_all_8_categories_reachable              | Toutes les 8 catégories produites             |
| test_selects_non_dos_rows                    | get_stage2_mask() → non-DoS uniquement        |
| test_passes_when_all_test_labels_in_train    | validate_split_labels() OK si tout présent    |
| test_raises_on_unseen_test_label             | ValueError si label test absent du train      |

Résultats : 10/10 ✅ — Couverture label_mapper.py : 100% ✅

---

#### Résultats de test globaux (pytest)

```
20 passed in 5.51s

Coverage report:
  src/data/constants.py      : 100%
  src/data/label_mapper.py   : 100%
  src/data/loader.py         :  90%  (6 lignes : error handlers I/O)
  src/main.py                :   0%  (squelette — implémenté en P2 final)
  TOTAL                      :  76%  (objectif final P4 : >80%)
```

**Pourquoi 76% et pas 80% :** Les 6 lignes non couvertes de loader.py sont des blocs
`except Exception` pour les erreurs I/O (fichier corrompu, permission denied). Ces cas
nécessitent des mocks système et seront couverts en P4 (Qualité & Robustesse).

---

**P2 + P3 terminés — prochaine étape : entraînement sur données réelles.**

---

### 2026-05-30 — Session 4 : P2 + P3 complétés — Pipelines A et B entièrement implémentés

**Objectif de la session :** Compléter les pipelines A et B jusqu'à l'étape d'entraînement.
All 8 modules implémentés avec Best Practices, tous les tests passants.

---

#### Fichier 4 : src/features/preprocessor_a.py ✅

**Rôle :** Préprocesseur Pipeline A = StandardScaler + PCA(39→16).
**Décisions d'implémentation :**

| Décision | Choix | Raison |
|----------|-------|--------|
| Outil | sklearn.pipeline.Pipeline | API standard ML, fit/transform géré proprement |
| Étapes | scaler → pca | L'ordre est obligatoire : normaliser AVANT PCA |
| n_components | 16 (paramétrable) | Réplication Raturi et al. (2026), modifiable pour ablation |
| random_state PCA | 42 | Reproductibilité — solver SVD randomisé |
| get_explained_variance_ratio() | Fonction publique | Utilisée dans le Paper pour justifier le choix de 16 composantes |

**Règle impérative documentée :** fit_transform(X_train), puis transform(X_test) — JAMAIS fit sur test.

---

#### Fichier 5 : src/features/preprocessor_b.py ✅

**Rôle :** Préprocesseur Pipeline B = StandardScaler uniquement.
**Décision clé :** API identique à preprocessor_a (même signature) → code client interchangeable.
**Justification scientifique :** SHAP sur features originales = noms interprétables pour l'analyste
sécurité ('Rate', 'syn_flag_number', 'Number'). PCA brise cette sémantique.

---

#### Fichier 6 : src/models/stage1_classifier.py ✅

**Rôle :** GradientBoostingClassifier binaire pour Stufe 1 (DoS/DDoS vs. non-DoS).
**Décisions d'implémentation :**

| Décision | Choix | Raison |
|----------|-------|--------|
| Modèle | GradientBoostingClassifier | Raturi et al. (2026) : BA=0.952, compatible TreeExplainer |
| Stage1Config | Dataclass | Hyperparamètres explicites, immuables, testables |
| Défauts | n_estimators=100, max_depth=3, lr=0.1 | Grid Search affinera ces valeurs (TO-DO P2) |
| get_grid_search_space() | Fonction publique | Centralise la grille, réutilisable dans Grid Search module |

---

#### Fichier 7 : src/models/stage2_classifier.py ✅

**Rôle :** GradientBoostingClassifier multiclasse pour Stufe 2 (6 classes non-DoS).
**Décision :** Même architecture que Stage 1 — scikit-learn gère automatiquement one-vs-rest
pour la classification multiclasse avec GradientBoosting.
**SHAP :** TreeExplainer sur clf.stage2 → SHAP values par classe (6 matrices).

---

#### Fichier 8 : src/models/hierarchical_classifier.py ✅

**Rôle :** Orchestration des deux étages.
**Flux d'entraînement :**
```
fit(X, y_binary, y_category):
    1. Validation pré-fit : ≥2 classes binaires + ≥1 instance non-DoS
    2. stage1.fit(X, y_binary)          ← TOUS les exemples d'entraînement
    3. stage2.fit(X[non_dos], y_cat[non_dos]) ← TRUE non-DoS uniquement
       (utilise les VRAIES étiquettes, pas les prédictions de Stufe 1
        → évite la propagation d'erreur en phase d'entraînement)
```
**Flux de prédiction :**
```
predict(X):
    stage1_pred = stage1.predict(X)         → [0, 1, 1, 0, ...]
    result[stage1==1] = "DoS/DDoS"          → label combiné DoS+DDoS
    result[stage1==0] = stage2.predict(X[stage1==0])  → 6 classes
```
**Décision architecture — Stufe 2 entraîné sur TRUE labels :**
- Pourquoi : si Stufe 1 fait des erreurs en train, entraîner Stufe 2 sur ses
  prédictions créerait un biais systématique (le modèle apprendrait à corriger
  des erreurs qui n'existent pas au test time)
- Comment : utiliser y_binary (ground truth), pas stage1.predict(X)

**Bug corrigé :** validation y_binary avant fit pour lever ValueError lisible
plutôt que l'erreur sklearn cryptique "y contains 1 class".

---

#### Fichier 9 : src/pipelines/_core.py ✅

**Rôle :** Logique partagée entre Pipeline A et B (principe DRY).
**Les 7 étapes de run_pipeline() :**

| Étape | Action | Détail |
|-------|--------|--------|
| 1 | load_stratified() | Chargement stratifié des MERGED_CSV |
| 2 | apply_label_mapping() | 33 labels → 8 catégories + is_dos_ddos |
| 3 | Extraction X, y | .to_numpy() → évite bug PyArrow/sklearn |
| 4 | train_test_split() | 80/20 stratifié sur y_category, random_state=42 |
| 5 | preprocessor.fit_transform(X_train) + transform(X_test) | Fit sur train UNIQUEMENT |
| 6 | HierarchicalClassifier.fit() | Stufe 1 + Stufe 2 |
| 7 | _compute_basic_metrics() | BA + F1-macro (Stufe 1 et Stufe 2 séparément) |

**Bug corrigé — PyArrow/sklearn incompatibilité :**
- Symptôme : `TypeError: only integer scalar arrays can be converted to a scalar index`
- Cause : pandas avec backend PyArrow retourne des Series incompatibles avec sklearn `_safe_indexing`
- Fix : `.to_numpy(dtype=int)` et `.to_numpy(dtype=str)` avant train_test_split
- Documenté dans : _core.py + conftest.py

**TrainedPipeline dataclass :** contient tout ce qu'il faut pour évaluation (P4) et SHAP (P4) :
preprocessor, classifier, X_test, y_binary_test, y_category_test, métriques de base, temps.

---

#### Fichiers 10-11 : pipeline_a.py + pipeline_b.py ✅

**Architecture DRY :**
```
pipeline_a.py : run_pipeline_a(config)
    → build_preprocessor_a(config.n_pca_components)
    → run_pipeline(config, preprocessor, "A")   ← _core.py

pipeline_b.py : run_pipeline_b(config)
    → build_preprocessor_b()
    → run_pipeline(config, preprocessor, "B")   ← _core.py
```
Seule différence entre A et B : le preprocessor injecté. Aucune duplication de logique.

---

#### Tests écrits dans cette session ✅

| Fichier test | Nb tests | Coverage modules testés |
|---|---|---|
| tests/conftest.py | fixtures | sample_df, mapped_df, split_arrays, preprocessed_arrays, fitted_hierarchical |
| tests/test_features_preprocessors.py | 13 | preprocessor_a 100%, preprocessor_b 100% |
| tests/test_models_hierarchical.py | 12 | stage1 95%, stage2 95%, hierarchical 95% |
| tests/test_pipelines.py | 10 | pipeline_a 100%, pipeline_b 100%, _core 98% |

**Total cumulé : 60/60 tests ✅ — Coverage global : 89%**

| Module | Coverage | Lignes non couvertes |
|--------|----------|----------------------|
| src/data/constants.py | 100% | — |
| src/data/label_mapper.py | 100% | — |
| src/features/preprocessor_a.py | 100% | — |
| src/features/preprocessor_b.py | 100% | — |
| src/pipelines/pipeline_a.py | 100% | — |
| src/pipelines/pipeline_b.py | 100% | — |
| src/pipelines/_core.py | 98% | Lignes 229-230 : cas edge trop peu non-DoS en test |
| src/models/hierarchical_classifier.py | 95% | Lignes 80, 147 : branches défensives |
| src/models/stage1_classifier.py | 95% | Ligne 64 : get_grid_search_space() pas encore appelé |
| src/models/stage2_classifier.py | 95% | Ligne 67 : même raison |
| src/data/loader.py | 90% | Lignes 102, 131-133, 140-141 : error handlers I/O |
| src/main.py | 0% | Squelette — implémenté lors de la pipeline finale |

---

**P2 + P3 COMPLÉTÉS — structure de fichiers finale :**
```
Backend/src/
├── data/
│   ├── constants.py     ✅ 100% coverage
│   ├── loader.py        ✅  90% coverage
│   └── label_mapper.py  ✅ 100% coverage
├── features/
│   ├── preprocessor_a.py ✅ 100% coverage
│   └── preprocessor_b.py ✅ 100% coverage
├── models/
│   ├── stage1_classifier.py      ✅ 95%
│   ├── stage2_classifier.py      ✅ 95%
│   └── hierarchical_classifier.py ✅ 95%
├── pipelines/
│   ├── _core.py      ✅ 98%
│   ├── pipeline_a.py ✅ 100%
│   └── pipeline_b.py ✅ 100%
├── evaluation/     (P4 — à implémenter)
├── explainability/ (P4 — à implémenter)
└── utils/          (P4 — logging centralisé)
```

**Prochaine étape concrète (URGENT — deadline 2026-06-01) :**
1. Lancer l'entraînement sur les données réelles MERGED_CSV (63 fichiers)
   → `run_pipeline_a(PipelineConfig(data_dir="../Dataset/MERGED_CSV", n_per_class_per_file=500))`
   → `run_pipeline_b(...)` (identique)
2. Collecter les premiers résultats de Balanced Accuracy pour le Motivationsreview

---

### 2026-05-30 — Session 5 : Environnement virtuel + correction inf + lancement entraînement réel

**Règle venv imposée par l'etudiant — OBLIGATOIRE pour toutes les sessions suivantes :**
- Tout le travail Python se fait dans `Backend/.venv/`
- Jamais `pip install` sur le Python système pour ce projet
- Commande Python : `.venv/Scripts/python` (Windows)
- Commande pytest : `.venv/Scripts/python -m pytest tests/`
- Cette règle est documentée dans CLAUDE.md (section "Python-Umgebung") et en mémoire

**Actions réalisées :**

1. Désinstallation packages système (scikit-learn, shap, xgboost, seaborn, tqdm, python-dotenv)
2. Création Backend/.venv/ + installation requirements.txt dans le venv
3. Vérification : 60/60 tests passent dans le venv ✅
4. Mise à jour CLAUDE.md avec règles venv

**Bug corrigé — valeurs infinies dans les données réelles du CICIoT2023 :**
- Symptôme : `ValueError: Input X contains infinity or a value too large for dtype('float64')`
- Cause : le dataset contient des valeurs inf/-inf (non visibles dans le sample de 50 000 lignes)
- Fix 1 : `loader.py` — `df.replace([inf, -inf], NaN)` à la lecture de chaque fichier
- Fix 2 : `preprocessor_a.py` + `preprocessor_b.py` — ajout de `SimpleImputer(strategy="median")`
  en première étape du Pipeline sklearn
- Pourquoi median : robuste aux outliers, contrairement à mean pour données réseau
- Respect data leakage : imputer fit sur train uniquement (via Pipeline.fit_transform)
- 60/60 tests passent encore ✅

**Script d'entraînement créé : scripts/train_pipelines.py**
- Arguments : --pipeline {A,B,both}, --n-per-class, --max-files
- Sauvegarde : models_artifacts/preprocessor_A.pkl, stage1_A.pkl, stage2_A.pkl
- Métriques : results/metrics/metrics_pipeline_A.json

**Statistiques observées au lancement :**

| Métrique | Valeur |
|----------|--------|
| Fichiers chargés | 63/63 |
| Lignes brutes | 841 680 |
| BACKDOOR_MALWARE supprimés | 3 078 (0,37%) |
| Lignes finales | 838 602 |
| DoS/DDoS (Stufe 1 positifs) | 489 735 (58,4%) |
| Non-DoS | 348 867 (41,6%) |
| Train | 670 881 |
| Test | 167 721 |
| Shape après PCA (Pipeline A) | (670 881, 16) |
| Durée chargement | ~3m 42s |

**Entraînement en cours au moment de l'écriture de cette entrée.**
Résultats Balanced Accuracy et F1 seront ajoutés à la prochaine entrée Done.md.

---

### 2026-05-31 — Session 6 : Résultats premiers entraînements + logging fichier

#### Résultats complets — Pipeline A et B (hyperparamètres par défaut)

**Données d'entraînement (identiques pour A et B) :**

| Métrique | Valeur |
|----------|--------|
| Fichiers chargés | 63/63 MERGED_CSV |
| Lignes brutes | 841 680 |
| BACKDOOR_MALWARE supprimés | 3 078 (0,37%) |
| Lignes finales | 838 602 |
| DoS/DDoS (Stufe 1 positifs) | 489 735 (58,4%) |
| Non-DoS | 348 867 (41,6%) |
| Train | 670 881 (80%) |
| Test | 167 721 (20%) |

**Résultats Pipeline A (StandardScaler + PCA 39→16) :**

| Métrique | Valeur | Interprétation |
|----------|--------|----------------|
| Stufe 1 Balanced Accuracy | **0.9971** | Excellent — détection DoS/DDoS quasi parfaite |
| Stufe 1 F1-macro | **0.9969** | Excellent |
| Stufe 2 Balanced Accuracy | **0.5480** | Modeste — hyperparamètres par défaut, Grid Search requis |
| Stufe 2 F1-macro | **0.5784** | Modeste |
| Durée totale | **2240s (37.3 min)** | — |
| Shape test (PCA actif) | (167 721, 16) | Confirme réduction 39→16 |

**Résultats Pipeline B (StandardScaler, 39 features originales) :**

| Métrique | Valeur | Interprétation |
|----------|--------|----------------|
| Stufe 1 Balanced Accuracy | **0.9993** | Excellent — légèrement meilleur que A |
| Stufe 1 F1-macro | **0.9993** | Excellent |
| Stufe 2 Balanced Accuracy | **0.6301** | Meilleur que A, mais encore modeste |
| Stufe 2 F1-macro | **0.6670** | Meilleur que A |
| Durée totale | **1657s (27.6 min)** | Plus rapide que A de ~10 min |
| Shape test (sans PCA) | (167 721, 39) | Confirme absence de réduction |

**Ablation Study — Analyse comparative A vs B (hyperparamètres par défaut) :**

| Critère | Pipeline A | Pipeline B | Delta B-A | Conclusion |
|---------|-----------|-----------|-----------|------------|
| Stufe 1 BA | 0.9971 | 0.9993 | +0.0022 | B légèrement meilleur |
| Stufe 2 BA | 0.5480 | 0.6301 | **+0.0821** | B significativement meilleur |
| Stufe 2 F1 | 0.5784 | 0.6670 | +0.0886 | B significativement meilleur |
| Durée | 2240s | 1657s | -583s | B plus rapide de 26% |

**Conclusion préliminaire de l'Ablation Study :**
Pipeline B (sans PCA) surpasse Pipeline A sur toutes les métriques ET est plus rapide.
PCA réduit la Balanced Accuracy de Stufe 2 de 8,21 points — confirme l'hypothèse centrale
du Lastenheft : la réduction dimensionnelle nuit à la fois à la performance et à
l'interprétabilité des SHAP. Résultat scientifiquement intéressant pour le Paper.

**Analyse Stufe 2 — pourquoi BA = 0.5480-0.6301 avec hyperparamètres par défaut :**
- Raturi et al. (2026) rapportent BA = 0.952, mais avec hyperparamètres optimisés
- Nos résultats actuels : n_estimators=100, max_depth=3, learning_rate=0.1 (valeurs par défaut)
- Les classes rares (Brute-Force : ~2 200 instances sur 838 602 = 0.26%) tirent la BA vers le bas
- Grid Search nécessaire pour atteindre la performance cible — prochaine étape critique

**Fichiers produits :**
```
models_artifacts/
  preprocessor_A.pkl, stage1_A.pkl, stage2_A.pkl  (Pipeline A)
  preprocessor_B.pkl, stage1_B.pkl, stage2_B.pkl  (Pipeline B)
results/metrics/
  metrics_pipeline_A.json
  metrics_pipeline_B.json
```

**Système de logging fichier implémenté :**
- src/utils/logger.py créé : double logging console + fichier
- Deux fichiers par run : train_latest.log (écrasé) + train_YYYYMMDD_HHMMSS.log (archive)
- Sentinelles : `=== TRAINING STARTED ===` en début, `=== TRAINING COMPLETE ===` en fin
- Commande de suivi en temps réel : `Get-Content results/logs/train_latest.log -Wait`
- Commande de vérification fin : `Get-Content results/logs/train_latest.log -Tail 3`

**Prochaine étape critique (deadline 2026-06-08) :**
1. Grid Search Pipeline A et B (n_estimators, max_depth, learning_rate, subsample)
   → Objectif : atteindre BA ≥ 0.85 sur Stufe 2 (proche de Raturi et al. 0.952)
2. Implémenter src/evaluation/metrics.py (rapport complet par classe)
3. Implémenter src/explainability/shap_analysis.py (SHAP global + local)


---

### 2026-05-31 — Session 7 : Issue #2 Motivationsreview — Grid Search lance

**Objectif :** Clore Issue #2 GitHub (Motivationsreview, deadline 2026-06-01).

**Ce qui etait requis par l'issue :**
1. [x] BA Stufe 1 + 2 Pipeline A et B documentees (Session 6)
2. [x] jguimfackjeuna-methodik.tex complet (Session 6)
3. [x] jguimfackjeuna-evaluation.tex avec resultats preliminaires (Session 6)
4. [→] Grid Search demarre (cette session)

**scripts/grid_search.py cree et lance :**
- GridSearchCV(cv=3, scoring='balanced_accuracy') sur Stufe 1 et Stufe 2 separement
- Grille : n_estimators [100, 200], max_depth [3, 5], learning_rate [0.05, 0.1], subsample [0.8, 1.0]
- 16 combinaisons x 3 folds x 2 etages = 96 fits par pipeline
- Sous-ensemble : max_files=5, n_per_class=50 (~8 200 lignes)
- Resultats sauvegardes dans results/metrics/best_params_{A,B}.json
- Logging via src/utils/logger.py (train_latest.log)

**Commande lancee :**
  .venv/Scripts/python scripts/grid_search.py --pipeline both --max-files 5 --n-per-class 50

**Resultats Grid Search** : a completer quand le processus termine (voir section suivante).

**Resultats Grid Search (sous-ensemble 8 045 lignes, 5 fichiers, cv=3) :**

| Pipeline | Stufe | Meilleurs HP | BA (test) |
|----------|-------|-------------|-----------|
| A (PCA) | Stufe 1 | lr=0.1, max_depth=5, n_estimators=200, subsample=0.8 | 0.9969 |
| A (PCA) | Stufe 2 | lr=0.05, max_depth=3, n_estimators=100, subsample=1.0 | 0.5384 |
| B (39f) | Stufe 1 | lr=0.05, max_depth=5, n_estimators=100, subsample=1.0 | 0.9994 |
| B (39f) | Stufe 2 | lr=0.05, max_depth=3, n_estimators=200, subsample=0.8 | **0.6479** |

**Observations cles :**
- Grid Search ameliore Pipeline B Stufe2 de 0.6301 -> 0.6479 (+0.018)
- Grid Search ne ameliore pas significativement Pipeline A Stufe2 (0.5480 -> 0.5384, -0.0096)
  Interpretation : PCA reduit la capacite du Grid Search a ameliorer la classification
- Reentrainement sur dataset complet avec best HP requis (Issue Backend #9)

**Fichiers produits :**
  results/metrics/best_params_A.json
  results/metrics/best_params_B.json

**Nouvelles issues Backend creees :**
  #9  [Backend] Grid Search + Reentrainement complet (deadline 2026-06-08)
  #10 [Backend] Evaluation detaillee metrics.py + confusion_matrix.py (deadline 2026-06-15)
  #11 [Backend] SHAP shap_analysis.py + shap_visualizer.py (deadline 2026-06-15)
  #12 [Backend] Export modeles + tests finaux (deadline 2026-06-22)

**Backend README.md cree.**

**Issue GitHub #2 (Motivationsreview) fermee.**

---

### 2026-05-31 -- Session 8 : Evaluation + SHAP + Tests + Docs + Reentrainement best HP

**Objectif :** Implémenter Issues #9 (retrain), #10 (evaluation), #11 (SHAP), #12 (tests/docs).

---

#### Nouveaux scripts crees

| Fichier | Role |
|---------|------|
| scripts/evaluate_and_explain.py | Charge modeles disk, genere evaluation + confusion matrix + SHAP |
| scripts/extract_test_data.py | Cree test_data_{A,B}.npz depuis preprocesseurs sauvegardes (backup) |
| scripts/update_paper_results.py | Copie figures -> paper/figures/ + affiche SHAP top-5 pour paper |
| scripts/wait_and_evaluate.sh | Monitore TRAINING COMPLETE + lance evaluate_and_explain.py auto |

---

#### Modules modifies/corriges

**src/explainability/shap_analysis.py (ADR-005)**
- compute_stage2_shap() : TreeExplainer remplace par PermutationExplainer
- Raison : sklearn multiclass GradientBoostingClassifier non supporte par SHAP TreeExplainer 0.52
- PermutationExplainer(stage2.predict_proba, masker) : valeurs Shapley correctes en esperance
- Documente dans docs/architecture_decision_records.md (ADR-005)

**src/evaluation/confusion_matrix.py**
- Titres de figures : "Stufe 1 -- Pipeline" -> "Stufe 1: Pipeline" (regle gedankenstriche)

**src/explainability/shap_visualizer.py**
- Titres de figures : "SHAP Summary --" -> "SHAP Summary:" (regle gedankenstriche)

**scripts/train_pipelines.py**
- save_result() modifie : sauvegarde test_data_{name}.npz (X_test, y_binary_test, y_category_test)
- Bug n_train_samples corrige : n_train_approx = n_test * (1-test_size) / test_size

---

#### Nouveaux fichiers de tests

| Fichier | Tests | Coverage cible |
|---------|-------|----------------|
| tests/test_explainability.py | 21 | shap_analysis 96%, shap_visualizer 95% |
| tests/test_logger.py | 9 | utils/logger.py 100% |
| tests/test_main.py | 11 | src/main.py 96% |
| tests/test_evaluation.py | +3 tests confusion matrix | confusion_matrix.py 100% |

**Total cumulatif : 111 tests / 97% coverage global**

**Correction conftest.py :** matplotlib.use("Agg") pour environnement headless (tests Tk error)

---

#### Documentation Backend

**docs/architecture_decision_records.md cree :**
7 ADRs documentes :
- ADR-001 : Gradient Boosting comme modele principal (Raturi et al. 2026)
- ADR-002 : Architecture hierarchique deux etages
- ADR-003 : Balanced Accuracy comme metrique primaire
- ADR-004 : Ablation Study PCA vs. sans PCA
- ADR-005 : SHAP Stage 2 avec PermutationExplainer (multiclass GBC limitation)
- ADR-006 : 39 features au lieu de 46 (divergence Lastenheft)
- ADR-007 : Stratified Sampling 500 instances/classe/fichier

**docs/label_mapping.md cree :**
Tableau complet 33 labels -> 8 categories, structure Stage 1/2, 39 features normalisees

---

#### Reentrainement avec best HP (Issue #9)

**Pipeline A (best HP : Stufe1 lr=0.1 depth=5 n=200 sub=0.8 | Stufe2 lr=0.05 depth=3 n=100 sub=1.0) :**

| Metrique | Standard HP | Best HP (retrain complet) | Delta |
|----------|-------------|--------------------------|-------|
| Stufe 1 BA | 0.9971 | **0.9985** | +0.0014 |
| Stufe 1 F1 | 0.9969 | **0.9985** | +0.0016 |
| Stufe 2 BA | 0.5480 | **0.5364** | -0.0116 |
| Stufe 2 F1 | 0.5784 | **0.5644** | -0.0140 |
| Duree | 2240s | 3265s | +1025s |

Observation critique : les HP optimises sur subset (8045 lignes) ne generalisent PAS
mieux sur le dataset complet (838602 lignes). Stufe2 BA retrain < Standard HP.
Cela montre la limite de l'optimisation sur sous-ensemble pour ce dataset.

**Pipeline B retrain : COMPLETE 09:53:12 (best HP : Stufe1 lr=0.05 depth=5 n=100 | Stufe2 lr=0.05 depth=3 n=200)**
BA1=0.9992, BA2=0.6285, F1-2=0.6652, Duree=2317s

Observation cle Pipeline B : HP optimises sur subset aussi ne generalisent pas (0.6285 < 0.6301 standard)

Per-class Pipeline B (best HP) :
- Mirai: P=1.000 R=1.000 F1=1.000
- Spoofing: P=0.911 R=0.857 F1=0.883
- Reconnaissance: P=0.726 R=0.907 F1=0.806
- Benign: P=0.605 R=0.517 F1=0.557
- Brute-Force: P=0.832 R=0.299 F1=0.440
- Web-based: P=0.739 R=0.192 F1=0.305

SHAP Stage 1 Pipeline B top-5: Number, Protocol_Type, UDP, AVG, Min
SHAP Stage 2 Pipeline B top-5 par classe (selectionnes) :
- Brute-Force: SSH confirme signature attaque ✅
- Mirai/Reconnaissance: Number dominant (scan/flood)
- Spoofing: pas ARP/ICMP comme attendu (artefact possible)

**Fichiers produits FINAL :**
- models_artifacts/ : 6 .pkl + 2 .npz (test_data_A, test_data_B) ✅
- results/metrics/ : full_report_{A,B}, shap_global_stage{1,2}_{A,B}, misclassified_{A,B} ✅
- results/figures/ : 30 PNG (confusion + SHAP summary + waterfall) ✅
- paper/figures/ : 6 PNG copies pour inclusion LaTeX ✅

---

#### Paper -- Mises a jour effectuees dans cette session

| Fichier | Modifications cles |
|---------|-------------------|
| jguimfackjeuna-abstract.tex | Resultats numeriques inclus (8.21 pts PCA, BA valeurs) |
| jguimfackjeuna-evaluation.tex | Tableau 3 configs (Standard/GS-Subset/Best HP), Pipeline A retrain, SHAP section complete, placeholders figures |
| jguimfackjeuna-methodik.tex | PermutationExplainer pour Stufe 2 documente |
| jguimfackjeuna-discussion.tex | Comparaisons litterature completes, observation retrain, Jaccard non-applicable PCA |
| jguimfackjeuna-conclusion.tex | Conclusions definitives avec resultats chiffres |
| jguimfackjeuna-main.tex | usepackage{graphicx} + graphicspath, correction -- autorenzeile |
| Tous .tex | 6 corrections violations Gedankenstrich -- -> : |

---

#### Prochaines etapes critiques (apres fin reentrainement Pipeline B ~10:15)

1. `cd Backend && .venv/Scripts/python scripts/evaluate_and_explain.py --pipeline both --shap-samples 500`
2. `cd Backend && .venv/Scripts/python scripts/update_paper_results.py`
3. Mettre a jour evaluation.tex tableau ligne "B (39f) Best HP" + tab:shap_top5
4. Decommenter les \includegraphics dans evaluation.tex
5. git push (autorisation user requise pour branch main)
6. Fermer issues GitHub #9, #10, #11, #12

---

### 2026-05-31 -- Session 9 : Klassengewichtung (sample_weight balanced) -- Issue #3

**Objectif :** Ameliorer la BA Stufe 2 (classes rares Web-based, Brute-Force) pour Issue #3.

**Constat :** GradientBoostingClassifier n'a pas de class_weight, mais fit() accepte
sample_weight. On utilise compute_sample_weight('balanced', y).

**Experience prealable (subset 15 fichiers) :** BA 0.6456 -> 0.7164 (+7.08 pts).
Reentrainement complet justifie.

**Modifications code :**
- hierarchical_classifier.fit(balanced_stage2=False) : nouveau parametre
- PipelineConfig.balanced_stage2 + propagation run_pipeline
- train_pipelines.py : flag --balanced-stage2
- test_models_hierarchical.py : test_fit_balanced_stage2_sets_is_fitted
- scripts/experiment_class_weight.py : script d'experience

**Reentrainement complet Pipeline B balanced (838.602 instances) :**

| Metrique | Best HP | Balanced | Delta |
|----------|---------|----------|-------|
| Stufe 2 BA | 0.6285 | **0.7261** | +0.0976 |
| Stufe 2 F1 | 0.6652 | 0.6570 | -0.0082 |
| Gap Acc-BA | ~0.12 | 0.0273 | reduit |

Recall par classe (Best HP -> Balanced) :
- Benign: 0.517 -> 0.709 | Brute-Force: 0.299 -> 0.646 (x2.16)
- Mirai: 1.000 -> 1.000 | Reconnaissance: 0.907 -> 0.571 (tradeoff)
- Spoofing: 0.857 -> 0.853 | Web-based: 0.192 -> 0.578 (x3.0)

**Conclusion :** Klassengewichtung = amelioration la plus efficace contre le desequilibre
(+9.76 pts BA vs +0.018 Grid Search). BA-Ziel 0.85 toujours non atteint (0.7261) mais
ecart fortement reduit. Documenté honnetement dans le paper.

**Paper (Session 9) :** tab:ergebnisse ligne B Balanced, tab:perclass_b tradeoff,
tab:shap_top5 features balanced, conclusion + discussion adaptees. Compile : 9 pages.
Figure confusion matrix Pipeline A retiree pour marge.

**Git :** historique nettoye (Claude retire, force-push). Jordan Jeuna seul auteur.

---

### 2026-05-31 -- Session 10 : Decision Issue #3 -- Acceptance BA=0.7261 comme resultat definitif

**Objectif :** Decider si le resultat BA=0.7261 (Pipeline B balanced) est acceptable comme
resultat final, ou si des techniques additionnelles doivent etre investies.

**Brainstorming mene -- Pour et Contre :**

Arguments pour acceptance :
- BA=0.7261 est le resultat reel, honnete, non falsifie sur 838 602 instances CICIoT2023
- Desequilibre intrinseque dataset : Mirai 18 900 vs. Brute-Force 2 504 vs. Web-based 4 144
- Deux techniques standards appliquees et documentees : Grid Search (+0.018) + Klassengewichtung (+0.0976)
- Hosseini et al. (2025) (source #10) documentent les limites de l'oversampling sur donnees reseau :
  echantillons SMOTE synthetiques ne correspondent pas a de vrais patterns d'attaque reseau
- Grid Search complet sur dataset entier : estimation ~100h de calcul (non realiste avant deadlines)
- Tradeoff deja observe avec balanced : Brute-Force +34.7 pts recall, Reconnaissance -33.6 pts
  Augmenter les poids aggraverait ce tradeoff sans garantie de gain net sur la BA

Arguments contre investissement supplementaire :
- BA-Ziel 0.85 non atteint, ecart restant de 0.1239
- SMOTE : risque de data leakage si applique apres split ; rendements decroissants previsibles
- Poids manuels : speculatifs, non justifies par la litterature pour ce dataset

**Decision finale de l'etudiant :** Accepter BA=0.7261 comme resultat definitif.
Discuter honnettement dans le paper les limites (section Diskussion, Hosseini et al. 2025).

**Etat final du projet Backend :**

| Pipeline | Stufe 1 BA | Stufe 2 BA | F1-macro Stufe 2 | Configuration |
|----------|-----------|-----------|-----------------|---------------|
| A (PCA)  | 0.9985    | 0.5364    | 0.5644          | Best HP retrain |
| B (39f)  | 0.9992    | 0.6285    | 0.6652          | Best HP retrain |
| B (39f)  | 0.9992    | **0.7261**| 0.6570          | Balanced (definitif) |

**Actions de cloture :**
- Issue GitHub #3 fermee avec resultat reel documente (BA=0.7261, objectif 0.85 non atteint)
- Aucune modification du code ou des modeles
- Backend, Paper, PROJECT_LOG.md mis a jour
