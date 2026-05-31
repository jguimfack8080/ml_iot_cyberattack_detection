# TO-DO.md -- Taches restantes sur le Paper
## Derniere mise a jour : 2026-05-31 (Session 8)

---

## P1 -- Blocage (avant toute redaction finale)

[x] Structure repertoire paper-usenix-template-jguimfackjeuna/ creee
[x] Sections migrees et corrigees (46->39 features)
[x] Premiers resultats experimentaux dans evaluation.tex (BA Pipeline A + B)
[x] Grid Search termine (Backend) -- resultats dans best_params_A.json + best_params_B.json
[x] Reentrainement Pipeline A avec best HP (BA1=0.9985 BA2=0.5364) -- 2026-05-31
[ ] Reentrainement Pipeline B avec best HP -- en cours (fin ~09:40 le 2026-05-31)
[ ] SHAP analyse complete (Backend) -- requis pour finaliser section SHAP dans evaluation.tex
    Prerequis : reentrainement Pipeline B complet + evaluate_and_explain.py execute

---

## P2 -- Redaction principale (deadline 2026-06-15 Kernkapitel)

[x] jguimfackjeuna-abstract.tex
    [x] Resultats numeriques concrets (8.21 pts PCA, BA valeurs experimentales)
[x] jguimfackjeuna-methodik.tex
    [x] PermutationExplainer pour Stufe 2 documente (ADR-005)
    [x] Ablation Study PCA correctement decrite
[x] jguimfackjeuna-evaluation.tex -- PARTIELLEMENT COMPLETE
    [x] Tableau 3 configs : Standard HP, Grid Search Subset, Best HP retrain
    [x] Pipeline A retrain : BA1=0.9985 F1=0.9985 | BA2=0.5364 F1=0.5644
    [x] Section SHAP-Analyse methodologie complete (Explainer-Wahl, global, local, ablation)
    [x] Placeholders figures (fbox avec commentaires de remplacement)
    [ ] Tableau ligne B (39f) Best HP : remplir quand reentrainement termine
    [ ] tab:shap_top5 : remplir avec vraies valeurs de update_paper_results.py
    [ ] Decommenter \includegraphics pour figures reelles (confusion matrix + SHAP)
    [ ] Ajouter tableaux de resultats par classe (Precision, Recall, F1 per class Stufe 2)
[x] jguimfackjeuna-discussion.tex -- COMPLETE
    [x] Comparaisons Raturi/Almahaqeri/Alharby
    [x] Observation retrain Pipeline A (HP subset ne generalisent pas)
    [x] Jaccard non applicable PCA vs. features (correction)
    [x] Evaluation SHAP qualite (Fidelitat, Konsistenz) documentee
    [x] Einschraenkungen : Grid Search sur subset, generalisation limitee
    [x] Offene Forschungsfragen : 3 questions documentees
[x] jguimfackjeuna-conclusion.tex -- COMPLETE
    [x] Kernergebnisse avec resultats chiffres (8.21 pts PCA)
    [x] Wissenschaftlicher Beitrag formule contre Raturi et Alharby
    [x] Ausblick : SHAP qualite, Latenz, Generalisierbarkeit

---

## P3 -- Verification et mise en forme (deadline 2026-06-22 Reviewversion)

[x] Verifier absence de tirets cadratins (-- et ---) dans tous les .tex -- FAIT Session 8
    [x] 6 occurrences corrigees (evaluation.tex, discussion.tex, main.tex)
[ ] Verifier longueur totale < 10 pages (USENIX deux colonnes)
    Prerequis : figures reelles incluses pour mesurer la longueur exacte
[ ] Verifier toutes les citations : chaque claim = source BibTeX tracable
[ ] Verifier que SimpleImputer est correctement reference (ou reference supprimee)
[ ] Corriger eventuelles erreurs LaTeX (overfull hbox, undefined refs, etc.)
[ ] Test de compilation complet via buildlualatex.sh
[ ] Compilation test local ou remote pour verifier PDF

---

## P4 -- Finalisation (deadline 2026-07-27 Camera Ready)

[ ] Integrer retours du Peer Review (2026-06-29)
[ ] Relecture finale du paper
[ ] PDF final compile et soumis

---

## Mapping Backend -> Paper (mis a jour 2026-05-31)

| Avancement Backend | Section a mettre a jour | Statut |
|---|---|---|
| Grid Search termine | evaluation.tex tableaux | [x] FAIT |
| Reentrainement Pipeline A | evaluation.tex tab:ergebnisse Best HP | [x] FAIT |
| Reentrainement Pipeline B | evaluation.tex tab:ergebnisse Best HP | [ ] EN ATTENTE |
| SHAP global feature importance | evaluation.tex tab:shap_top5 | [ ] EN ATTENTE |
| Figures confusion matrix PNG | evaluation.tex \includegraphics | [ ] EN ATTENTE |
| Figures SHAP PNG | evaluation.tex \includegraphics | [ ] EN ATTENTE |
| Divergence 39 vs 46 features | methodik.tex | [x] FAIT |
| BACKDOOR_MALWARE droppe | methodik.tex | [x] FAIT |
| PermutationExplainer ADR-005 | methodik.tex | [x] FAIT |
