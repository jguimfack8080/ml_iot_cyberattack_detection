# Architecture Decision Records (ADR)

Project: ml_iot_cyberattack_detection
Author: Jordan Guimfack Jeuna (38184)
Module: IT-Sicherheit, M.Sc. IVS, Hochschule Bremerhaven

---

## ADR-001: Gradient Boosting als Hauptmodell

**Status:** Accepted
**Date:** 2026-05-18

**Context:**
Several ML models were evaluated for the CICIoT2023 intrusion detection task.

**Decision:**
Use `sklearn.ensemble.GradientBoostingClassifier` as the primary model for both
Stage 1 and Stage 2.

**Rationale:**
- Raturi et al. (2026, DOI: 10.1002/spy2.70220) demonstrate that Gradient
  Boosting achieves Balanced Accuracy of 0.952 on CICIoT2023, the highest
  among all tested algorithms.
- SHAP's TreeExplainer provides exact Shapley values for tree-based models
  without approximation, enabling the explainability analysis.
- Almahaqeri et al. (2026, DOI: 10.1038/s41598-026-47399-5) independently
  confirm Gradient Boosting superiority on the same dataset.

**Consequences:**
- Stage 1 (binary): TreeExplainer works natively.
- Stage 2 (multiclass, 6 classes): sklearn multiclass GBC is not supported
  by TreeExplainer (see ADR-005). PermutationExplainer is used as fallback.

---

## ADR-002: Zweistufige hierarchische Architektur

**Status:** Accepted
**Date:** 2026-05-18

**Context:**
CICIoT2023 exhibits strong class imbalance: DoS/DDoS traffic accounts for
58.4% of all instances. Standard multiclass classification would systematically
suppress the minority attack classes.

**Decision:**
Adopt the two-stage hierarchical architecture from Raturi et al. (2026):
- Stage 1: Binary classifier (DoS/DDoS vs. non-DoS)
- Stage 2: Multiclass classifier on non-DoS instances only

**Rationale:**
- Structural solution to class imbalance (Hosseini et al. 2025,
  DOI: 10.3390/electronics14010069): the dominant DoS/DDoS class is handled
  separately, so Stage 2 trains on a more balanced subset.
- Stage 2 trains exclusively on TRUE non-DoS training instances. This prevents
  Stage 1 classification errors from propagating into Stage 2 training.

**Consequences:**
- Evaluation: Stage 1 and Stage 2 Balanced Accuracy are reported separately.
- SHAP: Two independent SHAP analyses (Stage 1 binary, Stage 2 multiclass).
- Pipeline code: `HierarchicalClassifier.fit()` enforces the train-on-ground-truth rule.

---

## ADR-003: Balanced Accuracy als primaere Metrik

**Status:** Accepted
**Date:** 2026-05-18

**Context:**
CICIoT2023 is heavily imbalanced. Standard accuracy would favor the majority
class and mask failures on rare attack types.

**Decision:**
Use Balanced Accuracy (arithmetic mean of per-class recall values) as the
primary evaluation metric for both stages.

**Rationale:**
- Raturi et al. (2026) propose Balanced Accuracy as the reference metric for
  CICIoT2023.
- Hosseini et al. (2025) demonstrate empirically that plain accuracy leads to
  systematically biased judgments on IDS datasets. Their study shows cases
  where accuracy reaches 99% while minority classes are entirely ignored.

**Consequences:**
- Grid Search target: `scoring='balanced_accuracy'`.
- Paper: explicit comparison Accuracy vs. Balanced Accuracy is documented.

---

## ADR-004: Ablation Study PCA vs. ohne PCA

**Status:** Accepted
**Date:** 2026-05-18

**Context:**
Raturi et al. (2026) apply PCA (46 -> 16 components) without evaluating its
effect on model explainability.

**Decision:**
Run two parallel preprocessing pipelines:
- Pipeline A: SimpleImputer + StandardScaler + PCA (39 -> 16 components)
- Pipeline B: SimpleImputer + StandardScaler (all 39 features)

**Rationale:**
- Pipeline A replicates the Raturi et al. setup.
- Pipeline B serves as the ablation control condition.
- Filling the explainability gap is the primary scientific contribution of
  this work: PCA components are linear combinations of features and lose
  semantic interpretability.
- Alharby (2025, DOI: 10.1038/s41598-025-23711-7) also uses PCA on
  CICIoT2023 but does not analyse the SHAP impact.

**Consequences:**
- PCA set to 16 components matching Raturi et al. (though actual features
  count is 39 not 46 -- see ADR-006).
- SHAP for Pipeline A: feature names are PC1..PC16 (no semantic meaning).
- SHAP for Pipeline B: feature names are the original 39 network features.

---

## ADR-005: SHAP Stage 2 mit PermutationExplainer

**Status:** Accepted
**Date:** 2026-05-31

**Context:**
SHAP TreeExplainer does not support sklearn's multiclass
`GradientBoostingClassifier` (tested with SHAP 0.52.0).

**Decision:**
Use `shap.PermutationExplainer(clf.stage2.predict_proba, masker)` for Stage 2
SHAP computation. Stage 1 (binary) continues to use TreeExplainer.

**Rationale:**
- PermutationExplainer gives approximate (but correct in expectation) Shapley
  values for any model via predict_proba.
- The scientific value of the SHAP analysis is preserved: feature importance
  rankings and waterfall plots remain interpretable.
- Hermosilla et al. (2025, DOI: 10.3390/app15137329) evaluate SHAP
  explanations by fidelity and Jaccard similarity -- these metrics apply
  regardless of the underlying explainer type.

**Consequences:**
- Stage 2 SHAP computation is slower than TreeExplainer.
- In production, `max_samples=500` and `background_samples=100` are used to
  keep compute time tractable.
- Paper documents this choice explicitly (footnote in Methodik 3.7).

---

## ADR-006: Feature-Anzahl: 39 statt 46

**Status:** Accepted
**Date:** 2026-05-30

**Context:**
CLAUDE.md and referenced papers (Raturi et al. 2026, Alharby 2025) cite 46
features for CICIoT2023. The actual MERGED_CSV files contain 39 features +
1 label column (40 columns total).

**Decision:**
Use the 39 features present in the actual data. PCA reduces 39 -> 16
(not 46 -> 16). Document the discrepancy in the paper.

**Rationale:**
- The discrepancy is acknowledged in the paper (Methodik section).
- Using only available features is scientifically honest and reproducible.
- The PCA ratio (16 components from 39) still captures a similar percentage
  of variance as 16 from 46.

**Consequences:**
- `src/data/constants.py:FEATURE_COLUMNS` defines the 39 exact column names.
- `src/features/preprocessor_a.py`: PCA n_components=16.

---

## ADR-007: Stratifiziertes Sampling (500 Instanzen/Klasse/Datei)

**Status:** Accepted
**Date:** 2026-05-30

**Context:**
63 MERGED_CSV files, ~8.5 GB total. Loading all data exceeds available RAM.

**Decision:**
Load at most 500 rows per class per CSV file using stratified sampling.
This yields approximately 838,602 instances total.

**Rationale:**
- Fits in RAM (~4-8 GB with preprocessing overhead).
- Preserves class distribution (stratified -- no systematic bias).
- All 63 files contribute equally to the training distribution.

**Consequences:**
- `src/data/loader.py:load_stratified()` implements this strategy.
- For Grid Search, the subset is reduced to 5 files x 50/class for speed.
- For final training, all 63 files x 500/class are used.
