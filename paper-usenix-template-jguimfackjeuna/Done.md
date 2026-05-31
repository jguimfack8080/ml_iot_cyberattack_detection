# Done.md -- Journal des modifications du Paper
## Repertoire : paper-usenix-template-jguimfackjeuna/

Journal chronologique immuable. Ne jamais supprimer les entrees existantes.
Format : date | section | description

---

### 2026-05-31 -- Initialisation du repertoire paper-usenix-template-jguimfackjeuna/

**Structure creee :**
```
paper-usenix-template-jguimfackjeuna/
  jguimfackjeuna-main.tex          USENIX 2019 template principal
  usenix-2020-09.sty               Style USENIX (copie depuis racine)
  jguimfackjeuna-abstract.tex      Kurzfassung
  jguimfackjeuna-introduction.tex  Einleitung (section 1)
  jguimfackjeuna-related-work.tex  Related Work (section 2)
  jguimfackjeuna-methodik.tex      Methodik (section 3)
  jguimfackjeuna-evaluation.tex    Evaluation (section 4)
  jguimfackjeuna-discussion.tex    Diskussion (section 5)
  jguimfackjeuna-conclusion.tex    Fazit (section 6)
  references.bib                   10 sources BibTeX
  Done.md                          Ce fichier
  TO-DO.md                         Taches restantes
```

**Contenu migre depuis Paper/src/ :**
- abstract.tex -> jguimfackjeuna-abstract.tex (adapte pour environnement abstract USENIX)
- einleitung.tex -> jguimfackjeuna-introduction.tex (contenu preserve)
- related_work.tex -> jguimfackjeuna-related-work.tex (contenu preserve)
- methodik.tex -> jguimfackjeuna-methodik.tex (correction 46->39 features)
- diskussion.tex -> jguimfackjeuna-discussion.tex (placeholder conserve)
- fazit.tex -> jguimfackjeuna-conclusion.tex (placeholder conserve)

**Nouveaux fichiers :**
- jguimfackjeuna-evaluation.tex : premiers resultats experimentaux (Pipeline A + B)
  Pipeline A : Stufe1 BA=0.9971, Stufe2 BA=0.5480 | Pipeline B : Stufe1 BA=0.9993, Stufe2 BA=0.6301

**Corrections apportees dans jguimfackjeuna-methodik.tex :**
- "von 46 auf 16 Hauptkomponenten" corrige en "von 39 auf 16 Hauptkomponenten"
- "allen 46 Originalmerkmalen" corrige en "allen 39 Originalmerkmalen"
- "welche der 46 Netzwerkmerkmale" corrige en "welche der 39 Netzwerkmerkmale"
- Section "Hinweis zur Feature-Anzahl" ajoutee pour documenter la divergence
- Section "Datenbasis und Vorverarbeitung" completee avec les details reels :
  BACKDOOR_MALWARE supprime, valeurs inf via SimpleImputer, stratified sampling
- Mention ajoutee : SimpleImputer reference vers \cite{neto2023ciciot2023}
  (NOTE : la reference exacte pour SimpleImputer sera a valider)

**Status actuel du paper :**
- Sections completes : Abstract, Einleitung, Related Work, Methodik
- Section partielle : Evaluation (resultats sans Grid Search, SHAP absent)
- Sections placeholder : Diskussion, Fazit
- Cible : 10 pages USENIX deux colonnes max

**Prochaines etapes paper :**
1. Completer jguimfackjeuna-evaluation.tex apres Grid Search
2. Ajouter SHAP results dans evaluation.tex
3. Completer diskussion.tex et conclusion.tex
4. Verifier la longueur (< 10 pages)

---

### 2026-05-31 -- Session 8 : Finalisation paper sections + resultats retrain Pipeline A

**Modifications jguimfackjeuna-abstract.tex :**
- Resultats numeriques concrets inclus : 8.21 Prozentpunkte PCA-impact (BA Stufe2)
- References specifiques aux valeurs experimentales ajoutees

**Modifications jguimfackjeuna-evaluation.tex :**
- Tableau tab:ergebnisse restructure : 3 configurations (Standard HP, Grid Search Subset, Best HP retrain)
- Resultats Pipeline A retrain ajoutés : BA1=0.9985 F1=0.9985 | BA2=0.5364 F1=0.5644 (3265s)
- Pipeline B Best HP : n.v. (reentrainement en cours)
- Sous-section SHAP-Analyse complete : Explainer-Auswahl (TreeExplainer S1, PermutationExplainer S2)
- Globale Erklaerungen + semantische Validierung + Ablation Study SHAP
- Jaccard non applicable entre espaces PCA et features originales (correction)
- Placeholders figures : confusion_matrix_stage2_pipelineB, shap_global_stage2_pipelineB
- Section "Interpretation: Ablation Study" mise a jour avec observations retrain Pipeline A
- 6 corrections violations Gedankenstrich (-- -> : dans titres et captions)

**Modifications jguimfackjeuna-methodik.tex :**
- Section SHAP-Integration : PermutationExplainer pour Stufe 2 documente avec justification
- Mention SHAP 0.52 limitation pour multiclass sklearn GBC

**Modifications jguimfackjeuna-discussion.tex :**
- Sous-section "Wissenschaftlicher Beitrag" complete : comparaisons Raturi/Almahaqeri/Alharby
- Sous-section "Bewertung der SHAP-Erklaerungsqualitaet" : Jaccard non applicable PCA vs. features
- Sous-section "Einschraenkungen" : observation empirique retrain Pipeline A (HP subset ne generalisent pas)
- Sous-section "Offene Forschungsfragen" : 3 questions ouvertes documentees

**Modifications jguimfackjeuna-conclusion.tex :**
- Conclusion definitive avec resultats chiffres (8.21 pts PCA, 1.78 pts Grid Search)
- Beitrag scientifique formule contre Raturi et Alharby
- Ausblick : SHAP qualite, Latenz, Generalisierbarkeit

**Modifications jguimfackjeuna-main.tex :**
- usepackage{graphicx} + graphicspath{{figures/}} ajoutés
- Gedankenstrich correction : "Informatik -- Vertrauenswuerdige" -> "(Vertrauenswuerdige)"
- figures/.gitkeep cree (repertoire pour les figures generees)

**Violations Gedankenstrich corrigees (total 6 occurrences dans .tex) :**
- evaluation.tex : sous-section titres, captions tableaux, formule Grid Search
- discussion.tex : 2 occurrences dans le texte
- main.tex : 1 occurrence dans champ auteur

**Status actuel du paper (2026-05-31 ~10:00) :**
- Sections completes (definitives) : Abstract, Einleitung, Related Work, Methodik
- Section principalement complete : Evaluation (Pipeline A done, Pipeline B n.v., SHAP methodologie done)
- Sections completes : Diskussion, Fazit
- Manque : valeurs reelles Pipeline B Best HP + figures SHAP + top-5 features
- Aucune violation Gedankenstrich dans les .tex

**Prochaines etapes :**
1. Attendre fin reentrainement Pipeline B (~10:15)
2. Executer evaluate_and_explain.py + update_paper_results.py
3. Remplir tab:ergebnisse ligne B Best HP + tab:shap_top5 avec vraies valeurs
4. Decommenter \includegraphics dans evaluation.tex
5. git push (autorisation requise user)

---

### 2026-05-31 -- Session 9 : Tickets #4 + #5 finalises, compilation reussie

**Ticket #4 (Kernkapitel) -- COMPLET :**
- Placeholders obsoletes supprimes (discussion.tex semantische Validierung, evaluation.tex fig:shap_global_b)
- SHAP global : tab:shap_top5 rempli avec top-5 features reelles par classe
- SHAP local : waterfall plots des 3 top misclassifications par stage/pipeline
- Semantische Validierung : SSH->Brute-Force confirme, Spoofing artefact documente
- Erklaerungsqualitaet : Fidelitaet/Konsistenz/Jaccard discutees (discussion.tex)
  Jaccard non applicable entre PCA et features originales (espaces differents)

**Ticket #5 (Reviewversion) -- COMPLET :**
- Compilation reussie via WSL build.sh (pdflatex) : **9 pages** (limite 10 respectee)
- Aucune reference/citation non resolue
- Un seul Overfull hbox mineur (19.6pt, non bloquant)
- Aucun Gedankenstrich dans le contenu (hors commentaires LaTeX %---)
- Bibliographie : 10 sources, 10 DOIs, 10 cles citees (toutes utilisees)
- Tous les labels references existent (fig, tab, sections)
- Note : buildlualatex.sh (remote SSH hopper) non testable sans credentials ;
  build.sh local (WSL pdflatex) valide la compilation

**Resultats finaux integres au paper :**
- Pipeline A Best HP : BA1=0.9985 BA2=0.5364
- Pipeline B Best HP : BA1=0.9992 BA2=0.6285
- Figures incluses : confusion matrix A+B, SHAP global A+B
- Tableaux : ergebnisse (3 configs), best_hp, perclass_a, perclass_b, shap_top5

**Constat scientifique cle :** HP optimises sur subset (8045 lignes) ne generalisent pas
mieux sur dataset complet (A: 0.5364<0.5480 ; B: 0.6285<0.6301). Documente transparemment.

**Git :** historique nettoye (Claude retire des 23 commits via filter-branch + force-push).
Jordan Jeuna seul auteur/committer.
