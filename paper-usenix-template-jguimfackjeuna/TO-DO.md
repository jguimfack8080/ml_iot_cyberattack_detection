# TO-DO.md -- Taches restantes sur le Paper
## Derniere mise a jour : 2026-05-31

---

## P1 -- Blocage (avant toute redaction finale)

[x] Structure repertoire paper-usenix-template-jguimfackjeuna/ creee
[x] Sections migrees et corrigees (46->39 features)
[x] Premiers resultats experimentaux dans evaluation.tex (BA Pipeline A + B)
[ ] Grid Search termine (Backend) -- requis avant de finaliser evaluation.tex
[ ] SHAP analyse complete (Backend) -- requis pour section SHAP dans evaluation.tex

---

## P2 -- Redaction principale (deadline 2026-06-15 Kernkapitel)

[ ] jguimfackjeuna-evaluation.tex
    -- Completer avec resultats Grid Search (BA cible >= 0.85)
    -- Ajouter tableaux de resultats par classe (Precision, Recall, F1 per class)
    -- Ajouter section SHAP : feature importance globale par classe
    -- Ajouter section SHAP : analyse locale (exemples de Fehlklassifikationen)
    -- Verifier : aucune valeur inventee, tout tracable aux resultats experimentaux
[ ] jguimfackjeuna-discussion.tex
    -- Completer les comparaisons avec Raturi et al. (0.9971 vs. 0.952 avec optimisation)
    -- Quantifier impact PCA sur SHAP feature importance (Jaccard-Aehnlichkeit)
    -- Discuter BACKDOOR_MALWARE suppression (justification dans le paper)
    -- Ajouter evaluation SHAP qualite : Fidelitat, Konsistenz (Hermosilla et al. 2025)
[ ] jguimfackjeuna-conclusion.tex
    -- Remplacer placeholder par conclusions definitives apres experimentation complete
    -- Recapituler les 3 contributions (BA, Ablation, SHAP)
    -- Formuler Ausblick (3 questions ouvertes)

---

## P3 -- Verification et mise en forme (deadline 2026-06-22 Reviewversion)

[ ] Verifier longueur totale < 10 pages (USENIX deux colonnes)
[ ] Verifier toutes les citations : chaque claim = source BibTeX tracable
[ ] Verifier absence de tirets cadratins (-- et ---) dans tous les .tex
[ ] Verifier que SimpleImputer est correctement reference (ou reference supprimee)
[ ] Corriger eventuelles erreurs LaTeX (overfull hbox, undefined refs, etc.)
[ ] Test de compilation complet via buildlualatex.sh

---

## P4 -- Finalisation (deadline 2026-07-27 Camera Ready)

[ ] Integrer retours du Peer Review (2026-06-29)
[ ] Relecture finale du paper
[ ] PDF final compile et soumis

---

## Mapping Backend -> Paper

| Avancement Backend | Section a mettre a jour |
|---|---|
| Grid Search termine | evaluation.tex (tableaux resultats) |
| SHAP global feature importance | evaluation.tex (section SHAP) |
| SHAP local / cas individuels | evaluation.tex (section SHAP local) |
| Divergence 39 vs 46 features | methodik.tex (DONE, Hinweis deja ajoute) |
| BACKDOOR_MALWARE droppe | methodik.tex (DONE, documentation deja presente) |
