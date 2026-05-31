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
