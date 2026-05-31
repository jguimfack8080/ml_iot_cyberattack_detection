# TO-DO.md -- Taches restantes sur le Paper
## Derniere mise a jour : 2026-05-31 (Session 12)

---

## P1 -- Blocage (avant toute redaction finale)

[x] Structure repertoire paper-usenix-template-jguimfackjeuna/ creee
[x] Sections migrees et corrigees (46->39 features)
[x] Premiers resultats experimentaux dans evaluation.tex (BA Pipeline A + B)
[x] Grid Search termine (Backend) -- resultats dans best_params_A.json + best_params_B.json
[x] Reentrainement Pipeline A avec best HP (BA1=0.9985 BA2=0.5364) -- 2026-05-31
[x] Reentrainement Pipeline B avec best HP (COMPLETE 2026-05-31 : BA1=0.9992 BA2=0.6285)
[x] SHAP analyse complete (Backend, Session 8 : 30 PNG + JSON generes, update_paper_results.py execute)

---

## P2 -- Redaction principale (deadline 2026-06-15 Kernkapitel)

[x] jguimfackjeuna-abstract.tex
    [x] Resultats numeriques concrets (8.21 pts PCA, BA valeurs experimentales)
[x] jguimfackjeuna-methodik.tex
    [x] PermutationExplainer pour Stufe 2 documente (ADR-005)
    [x] Ablation Study PCA correctement decrite
[x] jguimfackjeuna-evaluation.tex -- COMPLETE
    [x] Tableau 4 configs : Standard, GS-Subset, Best HP, Balanced
    [x] Pipeline A retrain : BA1=0.9985 BA2=0.5364 | Pipeline B retrain : BA1=0.9992 BA2=0.6285
    [x] Klassengewichtung balanced : BA2 Pipeline B 0.6285 -> 0.7261 (+9.76 pts)
    [x] Section SHAP-Analyse complete (Explainer-Wahl, global, local, ablation)
    [x] tab:shap_top5 rempli avec features reelles modele balanced
    [x] Figures reelles incluses (confusion matrix B, SHAP global A+B)
    [x] tab:perclass_b : tradeoff Recall Best HP vs Balanced
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

## P3 -- Verification et mise en forme (deadline 2026-06-22 Reviewversion) -- COMPLET (Session 11)

[x] Verifier absence de tirets cadratins (-- et ---) dans tous les .tex (Session 8+9)
    [x] Toutes occurrences corrigees, scan final OK (hors commentaires LaTeX %---)
[x] Verifier longueur totale < 10 pages : **9 pages** confirmees (Session 9)
[x] Verifier toutes les citations : 10 cles citees = 10 sources BibTeX (Session 9)
[x] Verifier biblio complete : 10 sources, 10 DOIs (Session 9)
[x] Corriger erreurs LaTeX : aucune ref/citation non resolue ; 1 Overfull mineur 19.6pt
[x] Test de compilation : build.sh local (WSL pdflatex) reussi -- 9 pages (Session 9)
[x] Compilation lualatex locale reussie -- 9 pages (Session 9bis)
    [x] Fix portabilite : microtype[kerning,spacing] conditionne a pdftex (iftex) dans .sty
    [x] Paper compile maintenant avec pdflatex ET lualatex (moteur de buildlualatex.sh)
[x] SimpleImputer reference : citation incorrecte \cite{neto} retiree (Session 9)
[x] Review anti-hallucination complet (Session 11) : 0 hallucination, 0 inconsistance interne
    [x] Toutes valeurs numeriques verifiees contre Backend JSON (100% correct)
    [x] discussion.tex : erreur "Pipeline B resultats en attente" corrigee (resultat reel: BA2=0.6285)
    [x] conclusion.tex Ausblick : erreur "SHAP sind naechste Schritte" corrigee (SHAP est complet)
[x] Corrections review (Session 12, branche fix/paper-review-vollstaendig, Issue #13)
    [x] introduction.tex : Forschungsfragen explizit formuliert (Hauptfrage + TF1-3)
    [x] evaluation.tex : \cite{hosseini2025imbalance} pour Klassengewichtung
    [x] discussion.tex : mapping Faithfulness/Stability/Comprehensibility explicit
[x] Compilation papier verifiee : 9 pages, 0 erreur, abstract = "Abstract" (Session 12)
    [x] main.tex : \addto\captionsngerman pour Abstract (pas Zusammenfassung)
    [x] discussion.tex §5.1 : \cite{hosseini2025imbalance} supprime (fausse attribution GS)
    [x] discussion.tex §5.3 : redondance supprimee, Pipeline B ajoutee, ref tab:ergebnisse
[ ] PR branch fix/paper-review-vollstaendig -> main (apres validation visuelle du PDF)

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
| Reentrainement Pipeline B | evaluation.tex tab:ergebnisse Best HP | [x] FAIT (Session 8) |
| SHAP global feature importance | evaluation.tex tab:shap_top5 | [x] FAIT (Session 9bis) |
| Figures confusion matrix PNG | evaluation.tex \includegraphics | [x] FAIT (Session 8) |
| Figures SHAP PNG | evaluation.tex \includegraphics | [x] FAIT (Session 8) |
| Divergence 39 vs 46 features | methodik.tex | [x] FAIT |
| BACKDOOR_MALWARE droppe | methodik.tex | [x] FAIT |
| PermutationExplainer ADR-005 | methodik.tex | [x] FAIT |
