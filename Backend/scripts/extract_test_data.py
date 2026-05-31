"""
extract_test_data.py

Extrait et sauvegarde les donnees de test (X_test + labels) pour les deux pipelines.
A lancer apres train_pipelines.py si test_data_{A,B}.npz sont absents.

Le split train/test est deterministe (random_state=42), donc ce script produit
exactement le meme X_test que l'entrainement original.

Usage (depuis Backend/ avec venv active) :
    .venv\\Scripts\\python scripts\\extract_test_data.py

Temps estime : ~5 minutes (chargement de 63 fichiers CSV)
"""
import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import joblib
import numpy as np
from sklearn.model_selection import train_test_split

from src.data.constants import BINARY_COL, CATEGORY_COL, FEATURE_COLUMNS, RANDOM_STATE
from src.data.label_mapper import apply_label_mapping
from src.data.loader import load_stratified

_DEFAULT_DATA_DIR   = Path(__file__).resolve().parent.parent.parent / "Dataset" / "MERGED_CSV"
_DEFAULT_MODELS_DIR = Path(__file__).resolve().parent.parent / "models_artifacts"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def main() -> int:
    models_dir = _DEFAULT_MODELS_DIR
    data_dir   = _DEFAULT_DATA_DIR

    for pkl_name in ("preprocessor_A.pkl", "preprocessor_B.pkl"):
        if not (models_dir / pkl_name).exists():
            logger.error("Preprocesseur introuvable: %s", models_dir / pkl_name)
            logger.error("Lancer train_pipelines.py d'abord.")
            return 1

    logger.info("Chargement du dataset (meme parametres que l'entrainement)...")
    df = load_stratified(
        data_dir=data_dir,
        n_per_class_per_file=500,
        random_state=RANDOM_STATE,
    )
    logger.info("Dataset charge: %d lignes", len(df))

    df = apply_label_mapping(df)
    logger.info("Label mapping applique: %d lignes restantes", len(df))

    X = df[list(FEATURE_COLUMNS)].astype(float).to_numpy()
    y_bin = df[BINARY_COL].to_numpy(dtype=int)
    y_cat = df[CATEGORY_COL].to_numpy(dtype=str)

    _, X_test_raw, _, y_bin_test, _, y_cat_test = train_test_split(
        X, y_bin, y_cat,
        test_size=0.2,
        stratify=y_cat,
        random_state=RANDOM_STATE,
    )
    logger.info("Test set: %d instances", len(X_test_raw))

    for pipeline_name in ("A", "B"):
        prep_path = models_dir / f"preprocessor_{pipeline_name}.pkl"
        out_path  = models_dir / f"test_data_{pipeline_name}.npz"

        if out_path.exists():
            logger.info("test_data_%s.npz existe deja -- skip", pipeline_name)
            continue

        logger.info("Preprocessing Pipeline %s...", pipeline_name)
        preprocessor = joblib.load(prep_path)
        X_test_prep = preprocessor.transform(X_test_raw)
        logger.info(
            "Pipeline %s: X_test shape %s -> %s",
            pipeline_name, X_test_raw.shape, X_test_prep.shape
        )

        np.savez_compressed(
            out_path,
            X_test=X_test_prep,
            y_binary_test=y_bin_test,
            y_category_test=y_cat_test,
            feature_names_in=np.array(list(FEATURE_COLUMNS)),
        )
        logger.info("Sauvegarde: %s", out_path)

    logger.info("Termine. Lancer evaluate_and_explain.py pour les figures et metriques.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
