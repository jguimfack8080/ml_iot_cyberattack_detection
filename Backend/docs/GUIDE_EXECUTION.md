# Guide d'Exécution — Backend ML IoT IDS
## Projet : CICIoT2023 + Gradient Boosting + SHAP
**Auteur :** Jordan Guimfack Jeuna (38184)
**Module :** IT-Sicherheit, M.Sc. IVS, Hochschule Bremerhaven

---

## Prérequis

- Python 3.10 ou supérieur installé (`python --version`)
- Git (optionnel)
- ~2 GB RAM libre minimum pour les tests
- ~8 GB RAM libre pour l'entraînement complet (63 fichiers MERGED_CSV)
- Le dossier `Dataset/MERGED_CSV/` contenant les 63 fichiers Merged01.csv à Merged63.csv

---

## 1. Activation de l'Environnement Virtuel

**Tout le travail Python se fait exclusivement dans le venv. Ne jamais utiliser le Python système.**

### 1.1 Création du venv (une seule fois)

```bash
# Depuis la racine du projet
cd Backend
python -m venv .venv
```

### 1.2 Activation (à faire à chaque nouvelle session terminal)

**Windows (PowerShell) :**
```powershell
cd Backend
.venv\Scripts\Activate.ps1
```

**Windows (CMD) :**
```cmd
cd Backend
.venv\Scripts\activate.bat
```

**Linux / macOS :**
```bash
cd Backend
source .venv/bin/activate
```

Après activation, le prompt affiche `(.venv)` au début.

### 1.3 Vérification de l'activation

```bash
# Doit afficher le chemin vers .venv/Scripts/python
python -c "import sys; print(sys.executable)"
```

Résultat attendu : `...\Backend\.venv\Scripts\python.exe`

### 1.4 Installation des dépendances

```bash
# Depuis Backend/ avec le venv activé
pip install -r requirements.txt
```

### 1.5 Désactivation

```bash
deactivate
```

---

## 2. Vérification de la Structure du Projet

```bash
# Depuis Backend/
python -c "
from src.data.constants import N_FEATURES, N_PCA_COMPONENTS, RANDOM_STATE, CATEGORIES
print('N_FEATURES      :', N_FEATURES)        # attendu : 39
print('N_PCA_COMPONENTS:', N_PCA_COMPONENTS)  # attendu : 16
print('RANDOM_STATE    :', RANDOM_STATE)       # attendu : 42
print('CATEGORIES      :', CATEGORIES)         # 8 catégories
"
```

---

## 3. Lancement de la Suite de Tests

### 3.1 Tous les tests (recommandé)

```bash
# Depuis Backend/ avec le venv activé
python -m pytest tests/ -v
```

Résultat attendu : **60 passed** en ~50-85 secondes.

### 3.2 Tests avec rapport de couverture

```bash
python -m pytest tests/ -v --cov=src --cov-report=term-missing
```

Couverture attendue : **89%** global, 100% sur les modules clés.

### 3.3 Tests d'un module spécifique

```bash
# Tester uniquement les données
python -m pytest tests/test_data_loader.py tests/test_data_label_mapper.py -v

# Tester uniquement les preprocessors
python -m pytest tests/test_features_preprocessors.py -v

# Tester le classifieur hiérarchique
python -m pytest tests/test_models_hierarchical.py -v

# Tester les pipelines (intégration)
python -m pytest tests/test_pipelines.py -v
```

### 3.4 Tests rapides (sans couverture)

```bash
python -m pytest tests/ -q
```

---

## 4. Vérification du Dataset

```bash
# Depuis Backend/
python -c "
import pandas as pd
from pathlib import Path

data_dir = Path('../Dataset/MERGED_CSV')
files = sorted(data_dir.glob('Merged*.csv'))
print(f'Fichiers MERGED_CSV trouvés : {len(files)}')  # attendu : 63

# Vérification du premier fichier
df = pd.read_csv(files[0], nrows=5)
print(f'Colonnes : {len(df.columns)}')  # attendu : 40 (39 features + Label)
print(f'Sample labels : {df[\"Label\"].tolist()}')
"
```

### 4.1 Vérification du label mapping

```bash
python -c "
from src.data.constants import LABEL_TO_CATEGORY, EXCLUDED_LABELS, CATEGORIES
print(f'Labels mappés       : {len(LABEL_TO_CATEGORY)}/33')
print(f'Labels exclus       : {EXCLUDED_LABELS}')
print(f'Catégories cibles   : {CATEGORIES}')
"
```

### 4.2 Test de chargement rapide (5 fichiers)

```bash
python -c "
from src.data.loader import load_stratified
from src.data.label_mapper import apply_label_mapping
from pathlib import Path

df = load_stratified('../Dataset/MERGED_CSV', n_per_class_per_file=100, max_files=5)
df = apply_label_mapping(df)
print('Lignes chargées :', len(df))
print('Colonnes        :', list(df.columns[-3:]))  # [..., category, is_dos_ddos]
print('Distribution    :')
print(df['category'].value_counts())
"
```

---

## 5. Lancement de l'Entraînement

### 5.1 Entraînement complet (Pipeline A + B — données réelles)

```bash
# Depuis Backend/ avec le venv activé
# Durée estimée : 20-40 minutes selon la machine
python scripts/train_pipelines.py --pipeline both --n-per-class 500
```

Ce script :
- Charge les 63 fichiers MERGED_CSV (~841 680 lignes)
- Entraîne Pipeline A (StandardScaler + PCA 39→16) + Pipeline B (StandardScaler seul)
- Sauvegarde les modèles dans `models_artifacts/`
- Sauvegarde les métriques dans `results/metrics/`

### 5.2 Test rapide (3 fichiers seulement — quelques minutes)

```bash
python scripts/train_pipelines.py --pipeline both --n-per-class 200 --max-files 3
```

### 5.3 Pipeline A uniquement

```bash
python scripts/train_pipelines.py --pipeline A --n-per-class 500
```

### 5.4 Vérification des résultats après entraînement

```bash
# Modèles sauvegardés
python -c "
from pathlib import Path
for f in Path('models_artifacts').glob('*.pkl'):
    size_mb = f.stat().st_size / 1024**2
    print(f'{f.name} — {size_mb:.1f} MB')
"

# Métriques JSON
python -c "
import json
from pathlib import Path
for f in Path('results/metrics').glob('*.json'):
    data = json.loads(f.read_text())
    print(f\"\n=== {data['pipeline']} ===\")
    print(f\"  Stage 1 Balanced Accuracy : {data['balanced_accuracy_stage1']:.4f}\")
    print(f\"  Stage 2 Balanced Accuracy : {data['balanced_accuracy_stage2']:.4f}\")
    print(f\"  Stage 1 F1-macro          : {data['f1_macro_stage1']:.4f}\")
    print(f\"  Stage 2 F1-macro          : {data['f1_macro_stage2']:.4f}\")
    print(f\"  Durée entraînement        : {data['training_time_seconds']:.1f}s\")
"
```

---

## 6. Test Manuel des Composants Individuels

### 6.1 Tester le Preprocessor A (StandardScaler + PCA)

```bash
python -c "
import numpy as np
from src.features.preprocessor_a import build_preprocessor_a, get_explained_variance_ratio

X_dummy = np.random.rand(200, 39)
p = build_preprocessor_a()
X_out = p.fit_transform(X_dummy)
print('Input  shape:', X_dummy.shape)   # (200, 39)
print('Output shape:', X_out.shape)     # (200, 16)
print('Explained variance:', f'{get_explained_variance_ratio(p)*100:.1f}%')
"
```

### 6.2 Tester le Preprocessor B (StandardScaler seul)

```bash
python -c "
import numpy as np
from src.features.preprocessor_b import build_preprocessor_b

X_dummy = np.random.rand(200, 39)
p = build_preprocessor_b()
X_out = p.fit_transform(X_dummy)
print('Input  shape:', X_dummy.shape)   # (200, 39)
print('Output shape:', X_out.shape)     # (200, 39) — pas de réduction
print('Standardisé (mean~0):', X_out.mean(axis=0)[:3].round(10))
"
```

### 6.3 Tester le HierarchicalClassifier (données synthétiques)

```bash
python -c "
import numpy as np
from src.models.hierarchical_classifier import HierarchicalClassifier
from src.models.stage1_classifier import build_stage1_classifier
from src.models.stage2_classifier import build_stage2_classifier

rng = np.random.default_rng(42)
X = rng.random((300, 16))
y_bin = np.array([1]*100 + [0]*200)
y_cat = np.array(['DDoS/DDoS']*100 + ['Mirai']*50 + ['Benign']*50 + ['Reconnaissance']*50 + ['Spoofing']*30 + ['Brute-Force']*20)

clf = HierarchicalClassifier(build_stage1_classifier(), build_stage2_classifier())
clf.fit(X, y_bin, y_cat)
preds = clf.predict(X[:5])
print('Prédictions (5 premières):', preds)
print('Stage 1 fitted:', clf.is_fitted)
"
```

### 6.4 Charger un modèle sauvegardé et faire une prédiction

```bash
python -c "
import joblib
import numpy as np
from pathlib import Path

models = Path('models_artifacts')
if not list(models.glob('*.pkl')):
    print('Aucun modèle sauvegardé. Lancer scripts/train_pipelines.py d abord.')
else:
    preprocessor = joblib.load(models / 'preprocessor_A.pkl')
    stage1 = joblib.load(models / 'stage1_A.pkl')
    stage2 = joblib.load(models / 'stage2_A.pkl')
    print('Modèles Pipeline A chargés.')
    print('PCA n_components:', preprocessor.named_steps[\"pca\"].n_components_)
    print('Stage1 n_estimators:', stage1.n_estimators)
    print('Stage2 classes:', stage2.classes_)
"
```

---

## 7. Résumé des Commandes Essentielles

| Action | Commande |
|--------|---------|
| Activer le venv | `.venv\Scripts\Activate.ps1` |
| Installer les dépendances | `pip install -r requirements.txt` |
| Lancer tous les tests | `python -m pytest tests/ -v` |
| Tests avec couverture | `python -m pytest tests/ -v --cov=src` |
| Vérifier les constantes | `python -c "from src.data.constants import *; print(N_FEATURES)"` |
| Chargement rapide (5 fichiers) | `python -c "from src.data.loader import load_stratified; ..."` |
| Entraînement complet | `python scripts/train_pipelines.py --pipeline both` |
| Entraînement rapide (test) | `python scripts/train_pipelines.py --pipeline both --max-files 3 --n-per-class 200` |
| Voir les métriques | `cat results/metrics/metrics_pipeline_A.json` |

---

## 8. Structure des Fichiers Produits

Après l'entraînement, les fichiers suivants sont créés :

```
Backend/
├── models_artifacts/
│   ├── preprocessor_A.pkl     # sklearn Pipeline (imputer + scaler + PCA)
│   ├── stage1_A.pkl           # GBClassifier binaire (Stufe 1)
│   ├── stage2_A.pkl           # GBClassifier multiclasse (Stufe 2)
│   ├── preprocessor_B.pkl     # sklearn Pipeline (imputer + scaler)
│   ├── stage1_B.pkl           # GBClassifier binaire Pipeline B
│   └── stage2_B.pkl           # GBClassifier multiclasse Pipeline B
└── results/
    └── metrics/
        ├── metrics_pipeline_A.json   # BA, F1, durée Pipeline A
        └── metrics_pipeline_B.json   # BA, F1, durée Pipeline B
```

---

## 9. Dépannage

### Erreur : `No module named 'sklearn'`
Le venv n'est pas activé. Exécuter `.venv\Scripts\Activate.ps1` d'abord.

### Erreur : `FileNotFoundError: Data directory not found`
Le chemin vers MERGED_CSV est incorrect. Vérifier avec :
```bash
python -c "from pathlib import Path; print(Path('../Dataset/MERGED_CSV').is_dir())"
```

### Erreur : `ValueError: Input X contains infinity`
Normalement résolu par le SimpleImputer dans le preprocessor. Si cela persiste,
vérifier que le venv utilise bien la dernière version de `preprocessor_a.py`.

### Entraînement trop lent
Utiliser `--max-files 5 --n-per-class 200` pour un prototype rapide :
```bash
python scripts/train_pipelines.py --pipeline both --max-files 5 --n-per-class 200
```

### Tests qui échouent
```bash
# Vérifier la version de Python dans le venv
python --version   # doit être 3.10+
pip list | grep scikit  # doit afficher scikit-learn
```

---

## 10. Ordre d'Exécution Recommandé (première fois)

```
1. cd Backend
2. python -m venv .venv                          # créer venv (une fois)
3. .venv\Scripts\Activate.ps1                    # activer venv
4. pip install -r requirements.txt               # installer dépendances
5. python -m pytest tests/ -v                    # vérifier 60/60 tests
6. python scripts/train_pipelines.py \
       --pipeline both \
       --max-files 5 \
       --n-per-class 200                         # entraînement test rapide
7. python scripts/train_pipelines.py \
       --pipeline both \
       --n-per-class 500                         # entraînement complet (~30 min)
```
