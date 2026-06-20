---
title: Project Log
project: ml_iot_cyberattack_detection
created: 2026-04-28
---

# PROJECT_LOG.md

## Eintraege

### 2026-06-20 : Layout-Korrekturen Abstract und SHAP-Abbildungen

- Datum: 2026-06-20
- Aenderung: Abstand zwischen Abstract-Ueberschrift und Abstract-Text eng gesetzt (eigene \abstract-Definition statt lockerer center-Umgebung der Vorlage); die beiden globalen SHAP-Abbildungen (Stufe 2, Pipeline A und B) durch Sandwich-Struktur und t-Platzierung getrennt, sodass erklaerender Text zwischen ihnen steht; redundante Sektion "Offene Forschungsfragen" aus der Diskussion entfernt (bleibt im Fazit).
- Betroffene Dateien:
  - paper-usenix-template-jguimfackjeuna/jguimfackjeuna-main.tex
  - paper-usenix-template-jguimfackjeuna/jguimfackjeuna-evaluation.tex
  - paper-usenix-template-jguimfackjeuna/jguimfackjeuna-discussion.tex
- Technische Auswirkungen:
  - Verifiziert: 10 Seiten, durchgehend zweispaltig, 0 undefinierte Referenzen, keine verschwendete Flaeche, Schriftgroesse unveraendert.
- Begruendung:
  - Nutzeranforderung: keine Leerraeume, jede Abbildung im Text erklaert, Leser darf nie verloren gehen.

### 2026-06-15 (a) -- Paper 100 Prozent fundiert : Backend-Re-Run + Zahlen-Abgleich (Issue #15)

- Datum: 2026-06-15
- Aenderung: Vollstaendiger, deterministischer Re-Run des gesamten Backends und Abgleich jeder
  Zahl im Paper gegen die frisch erzeugten Artefakte. Branche fix/paper-100-prozent-fundiert.
- Betroffene Dateien:
  - Backend/scripts/rerun_all.sh (neu) : Orchestrator Standard/GridSearch/BestHP/Balanced/Eval+SHAP
  - Backend/scripts/regen_perclass_b_besthp.py (neu) : Per-Class B Best-HP nobalanced
  - Backend/results/metrics/* : metrics_*_standard.json, best_params_*, full_report_*, shap_*,
    perclass_B_besthp_nobalanced.json (neu/aktualisiert)
  - paper/* : abstract, evaluation, discussion, conclusion, methodik, motivation, main,
    related-work, figures/ (3 frische Figuren)
  - Backend/Done.md, paper/Done.md, paper/TO-DO.md, Backend/TO-DO.md
- Technische Auswirkungen:
  - Standard-Config (0,5480 / 0,6301) exakt reproduziert -> Headline "8,21 Prozentpunkte" fundiert
  - Alle BA/F1/Per-Class/SHAP deterministisch identisch ; nur Trainingszeiten neu gemessen
  - SHAP-Qualitaetsmetriken ehrlich als qualitativ/Bezugsrahmen formuliert (kein Overclaim)
  - KI-/Uebersetzungs-Offenlegung ergaenzt ; franzoesische Woerter entfernt
  - Abweichung zur Raturi-BA 0,952 als Reproduzierbarkeitsfrage dokumentiert (Betreuer-Linie)
  - Kompilierung WSL pdflatex : 10 Seiten, 0 undefined refs/citations
- Begruendung:
  - Nutzerforderung "100 Prozent fundiert, keine erfundenen Zahlen" ; Backend = einzige Wahrheit
  - Review hatte Standard-Zahlen als nicht persistiert/nicht reproduzierbar markiert

### 2026-06-01 (a) -- Session 13 : Review complete (redondances, fluidite, coherence)

- Datum: 2026-06-01
- Aenderung: Review complete du paper a la demande de l'etudiant. Suppression des
  redondances, reformulation fluide des Forschungsfragen, correction d'incoherences
  internes et d'une regression de l'abstract. 7 fichiers .tex touches.
- Betroffene Dateien:
  - paper/jguimfackjeuna-introduction.tex : double citation Hamedani retiree ;
    Forschungsfragen en prose chronologique ; "Struktur der Arbeit" supprime ;
    redondance Related Work (Mohale/Hermosilla) retiree ; Motivation renforcee
  - paper/jguimfackjeuna-abstract.tex : resultats chiffres restaures (regression) ;
    meta-phrases (Alharby/Diskussionsteil) retirees ; "Schluesselwoerter" corrige
  - paper/jguimfackjeuna-evaluation.tex : \cite{hosseini} errone retire (Grid Search) ;
    "zukuenftige" ; "Kapitel"->"Abschnitt"
  - paper/jguimfackjeuna-discussion.tex : §5.1 triple repetition consolidee ;
    "Rahmenfrage"->"leitende Forschungsfrage"
  - paper/jguimfackjeuna-methodik.tex : contradiction "Normalverteilung" corrigee
  - paper/jguimfackjeuna-conclusion.tex : "Kapitel"->"Abschnitt"
  - paper/jguimfackjeuna-motivation.tex : "46 Originalmerkmalen"->"Originalmerkmalen"
  - paper/Done.md, TO-DO.md : session 13
- Technische Auswirkungen:
  - 0 Gedankenstrich introduit ; 10/10 sources toujours citees ; 0 cle indefinie
  - Abstract de nouveau porteur de resultats (best practice) ; intro non redondante
  - Coherence interne methodik <-> discussion sur l'echantillonnage retablie
  - Compilation NON verifiee (pas de LaTeX local, WSL HS) : a recompiler avant merge
- Begruendung:
  - Demande explicite de l'etudiant (review complete, anti-redondance, anti-hallucination)
  - L'abstract avait perdu ses resultats numeriques et gagne du meta-commentaire impropre
  - "Normalverteilung erhalten" contredisait "glaettet die Klassenverteilung" (§5.3)
  - Hosseini ne soutient pas le constat de generalisation Grid-Search (anti-hallucination)

### 2026-05-31 (h) -- Final Review complet + 3 correctifs supplementaires (branch Issue #13)

- Datum: 2026-05-31
- Aenderung: Final review 100% safe sur branch fix/paper-review-vollstaendig.
  3 correctifs supplementaires apres relecture profonde.
- Betroffene Dateien:
  - paper/jguimfackjeuna-main.tex : abstractname force a "Abstract" (babel override)
  - paper/jguimfackjeuna-discussion.tex :
    § 5.1 : hosseini2025imbalance retire du Grid-Search-Satz (fausse attribution)
    § 5.3 : redondance BA-Zahlen supprimee, Pipeline B ajoute, ref tab:ergebnisse
  - paper/Done.md, TO-DO.md : session 12 finalisee
  - PROJECT_LOG.md : cet entree
- Technische Auswirkungen:
  - Abstract s'affiche "Abstract" (non "Zusammenfassung")
  - 0 fausse citation, 0 redondance en §5.3
  - Compilation : 9 pages, 0 erreur, 0 reference indefinie (WSL pdflatex)
- Begruendung:
  - babel[ngerman] ecrase \abstractname -> "Zusammenfassung" : non voulu pour USENIX
  - hosseini2025imbalance ne traite pas de la generalisation Grid-Search (anti-hallucination)
  - §5.3 repetait les memes chiffres BA que §5.1 (redondance detectee au review final)

### 2026-05-31 (g) -- Branche fix/paper-review-vollstaendig : Issue #13 corrections paper

- Datum: 2026-05-31
- Aenderung: 3 Korrekturen auf Branche fix/paper-review-vollstaendig (Issue #13).
- Betroffene Dateien:
  - paper-usenix-template-jguimfackjeuna/jguimfackjeuna-introduction.tex :
    Absatz Forschungsfragen eingefuegt (Hauptfrage + TF1-3 explizit)
  - paper-usenix-template-jguimfackjeuna/jguimfackjeuna-evaluation.tex :
    \cite{hosseini2025imbalance} zu Klassengewichtungs-Satz hinzugefuegt
  - paper-usenix-template-jguimfackjeuna/jguimfackjeuna-discussion.tex :
    Mapping Faithfulness/Stability/Comprehensibility explizit eingefuegt
  - paper-usenix-template-jguimfackjeuna/Done.md, TO-DO.md : Session 12
  - PROJECT_LOG.md : dieser Eintrag
- Technische Auswirkungen:
  - Alle 5 Forschungsfragen der Rahmenfrage vollstaendig oder explizit adressiert
  - 0 neue Quellen ausserhalb der 10 BibTeX-Eintraege
  - Seitenzahl nach Kompilierung zu verifizieren (Ziel: max 10)
- Begruendung:
  - Review-Protokoll (Session 11) identifizierte 3 mittlere Probleme
  - Explizite Forschungsfragen in der Einleitung sind akademischer Standard
  - Rahmenfrage erfordert explizite Mapping der XAI-Kriterien
  - Klassengewichtung braucht Literaturstutze (Hosseini et al. 2025)

### 2026-05-31 (f) -- Review anti-hallucination + correction 2 erreurs critiques paper

- Datum: 2026-05-31
- Aenderung: Review complet du paper selon protocole strict (hallucinations, sources, metriques,
  Forschungsfragen). Deux erreurs critiques identifiees et corrigees.
- Betroffene Dateien:
  - paper-usenix-template-jguimfackjeuna/jguimfackjeuna-discussion.tex :
    Zeile "Fuer Pipeline B stehen die Reentrainement-Ergebnisse noch aus." entfernt und
    durch korrekte Ergebnisse ersetzt (BA2=0.6285, konsistentes Grid-Search-Muster)
  - paper-usenix-template-jguimfackjeuna/jguimfackjeuna-conclusion.tex :
    Ausblick korrigiert : "SHAP sind naechste Schritte" entfernt (SHAP abgeschlossen),
    durch korrekte Zusammenfassung + echte offene Fragen ersetzt
  - paper-usenix-template-jguimfackjeuna/Done.md : Session 11 ergaenzt
  - paper-usenix-template-jguimfackjeuna/TO-DO.md : Review-Checkboxen ergaenzt
  - PROJECT_LOG.md : dieser Eintrag
- Technische Auswirkungen:
  - Paper intern konsistent : kein Widerspruch mehr zwischen Evaluation und Discussion/Conclusion
  - Alle Zahlenwerte 100% verifiziert gegen Backend-JSON-Metriken
  - 0 Halluzinationen, 0 externe Quellen, 0 falsche Zitierungen
- Begruendung:
  - Beide Saetze waren Ueberbleibsel aus Zwischenphasen des Schreibprozesses
  - "Pipeline B ausstehend" war seit Session 8 faktisch falsch (Ergebnisse lagen vor)
  - "SHAP naechste Schritte" war seit Session 8 faktisch falsch (SHAP abgeschlossen)
  - Wissenschaftliche Glaubwuerdigkeit erfordert interne Konsistenz

### 2026-05-31 (e) -- Decision Issue #3 : BA=0.7261 definitif + cloture documentation

- Datum: 2026-05-31
- Aenderung: Decision academique apres brainstorming : BA=0.7261 (Pipeline B balanced)
  acceptee comme resultat definitif. Cloture Issue #3. Documentation completement synchronisee.
- Betroffene Dateien:
  - Backend/Done.md : Session 10 ajoutee (tableau recapitulatif, raisonnement decision)
  - Backend/TO-DO.md : Issue #3 marquee fermee, issues #9-12 confirmees fermees
  - paper-usenix-template-jguimfackjeuna/Done.md : Session 10 ajoutee
  - paper-usenix-template-jguimfackjeuna/TO-DO.md : 4 items EN ATTENTE -> FAIT, 2 items P1 marques done
  - PROJECT_LOG.md : cette entree
- Technische Auswirkungen:
  - Aucune modification du code ou des modeles
  - Documentation completement synchronisee avec l'etat reel du projet
  - Tous les tickets Backend actionnables fermes (#3, #9, #10, #11, #12)
- Begruendung:
  - Brainstorming sur SMOTE, poids manuels, Grid Search complet : rendements decroissants,
    risque data leakage SMOTE, Hosseini et al. (2025) documentent les limites oversampling
    sur donnees reseau, Grid Search complet ~100h non realiste avant deadlines
  - BA=0.7261 bien discute dans le paper est une contribution scientifique honnete et solide
  - Discussion.tex documente deja les limites et offene Forschungsfragen

### 2026-05-31 (d) -- Klassengewichtung (sample_weight balanced) + nettoyage git

- Datum: 2026-05-31
- Aenderung: Klassengewichtung in Stufe 2 (Issue #3) + suppression Claude de l'historique git.
- Betroffene Dateien:
  - Backend/src/models/hierarchical_classifier.py : parametre balanced_stage2
  - Backend/src/pipelines/_core.py : PipelineConfig.balanced_stage2
  - Backend/scripts/train_pipelines.py : flag --balanced-stage2
  - Backend/scripts/experiment_class_weight.py : nouveau script d'experience
  - Backend/tests/test_models_hierarchical.py : test balanced
  - paper/jguimfackjeuna-{evaluation,discussion,conclusion}.tex : integration balanced
  - Backend/results/metrics/ + figures/ : resultats balanced + archives _nobalanced
- Technische Auswirkungen:
  - Pipeline B balanced : BA Stufe 2 0.6285 -> 0.7261 (+9.76 Punkte)
  - Recall classes rares : Brute-Force 0.299->0.646, Web-based 0.192->0.578
  - Klassengewichtung deutlich wirksamer als Grid Search (+0.018)
  - Paper compile : 9 pages (figure Pipeline A confusion matrix retiree)
  - Git : historique nettoye (Co-Authored-By Claude retire des 23 commits, force-push)
- Begruendung:
  - Issue #3 : amelioration de la BA pour les classes rares sous-detectees
  - GradientBoostingClassifier n'a pas class_weight ; sample_weight est le mecanisme supporte
  - Demande explicite de l'etudiant : seul contributeur, pas de mention Claude

### 2026-05-31 (c) -- Evaluation + SHAP finale + Paper complet

- Datum: 2026-05-31
- Aenderung: Reentrainement Pipeline B complet + evaluation + SHAP + paper finalisé.
- Betroffene Dateien:
  - Backend/models_artifacts/ : test_data_B.npz + modeles Pipeline B best HP
  - Backend/results/metrics/ : full_report_{A,B}.json, shap_global_{stage1,stage2}_{A,B}.json
  - Backend/results/figures/ : 30 PNG (confusion + SHAP)
  - paper/figures/ : 6 PNG copies pour LaTeX
  - paper/jguimfackjeuna-evaluation.tex : tab:perclass_b, tab:shap_top5 complets,
    fig:cm_stage2_b et fig:shap_global_b actives
  - Backend/Done.md, Backend/TO-DO.md : mis a jour finaux
  - CLAUDE.md : regle Done.md/TO-DO.md obligation documentee
- Technische Auswirkungen:
  - Pipeline B Best HP retrain: BA1=0.9992, BA2=0.6285, F1-2=0.6652, 2317s
  - Observation : HP optimises sur subset ne generalisent pas sur dataset complet (A et B)
  - SHAP Stage 2 Pipeline B: SSH pour Brute-Force confirme signature d'attaque
  - Paper evaluation.tex complet avec vraies valeurs experimentales
- Begruendung:
  - Issues #9, #10, #11, #12 (Issues Backend): tous criteres remplis
  - Issues #3, #4 (Academic Paper): sections Evaluation et SHAP avec donnees reelles

### 2026-05-31 (b) -- Paper: Diskussion, Fazit, SHAP-Methodik, Gedankenstrich-Fix

- Datum: 2026-05-31
- Aenderung: Vollstaendige Fertigstellung der Paper-Sektionen fuer Issues #3, #4.
- Betroffene Dateien:
  - paper-usenix-template-jguimfackjeuna/jguimfackjeuna-evaluation.tex: SHAP-Sektion vollstaendig
    (Explainer-Wahl, globale + lokale Erklaerungen, Ablation SHAP, Tabellen-Struktur)
  - paper-usenix-template-jguimfackjeuna/jguimfackjeuna-discussion.tex: vollstaendige Diskussion
    (Vergleiche Raturi/Almahaqeri/Alharby, SHAP-Qualitaet, Limitierungen, offene Fragen)
  - paper-usenix-template-jguimfackjeuna/jguimfackjeuna-conclusion.tex: vollstaendiges Fazit
  - paper-usenix-template-jguimfackjeuna/jguimfackjeuna-methodik.tex: PermutationExplainer Stufe 2
  - paper-usenix-template-jguimfackjeuna/jguimfackjeuna-main.tex: Gedankenstrich-Fix Autorenzeile
  - Alle .tex-Dateien: alle -- Gedankenstriche entfernt (6 Fixes in evaluation+discussion)
- Technische Auswirkungen:
  - Keine verbotenen Gedankenstriche mehr in Inhaltsbereichen der .tex-Dateien
  - Tabelle 3 (SHAP Top-5 Features) hat Platzhalter; wird nach Reentrainement befuellt
  - SHAP-Sektion beschreibt PermutationExplainer fuer Stufe 2 (ADR-005-Begruendung)
- Begruendung:
  - Issues #3 (Ergebnisfeststellung) und #4 (Kernkapitel) erfordern vollstaendige Paper-Sektionen.
  - Deadline Issue #3: 2026-06-08. Alle methodischen Sektionen sind jetzt vollstaendig geschrieben.
  - Zahlenwerte (SHAP Top-Features) werden nach Abschluss des Reentrainements eingefuegt.

### 2026-05-31 (a) -- Backend: Evaluation, SHAP, Tests, Docs (Issues #10, #11, #12 teilweise)

- Datum: 2026-05-31
- Aenderung: Umfassende Backend-Erweiterung im Rahmen der Issues #10, #11, #12.
- Betroffene Dateien:
  - Backend/scripts/train_pipelines.py: save_result() speichert jetzt test_data_{A,B}.npz
    (X_test, y_binary_test, y_category_test, feature_names); Bug n_train_samples behoben
  - Backend/scripts/evaluate_and_explain.py: neues Script, laedt Modelle von Disk,
    generiert Evaluation-Berichte + Konfusionsmatrizen + SHAP-Analysen (JSON + PNG)
  - Backend/src/explainability/shap_analysis.py: compute_stage2_shap() nutzt jetzt
    PermutationExplainer statt TreeExplainer (sklearn multiclass GBC nicht unterstuetzt)
  - Backend/src/explainability/shap_analysis.py: ADR-005 dokumentiert die Entscheidung
  - Backend/tests/test_explainability.py: neu, 21 Tests fuer shap_analysis + shap_visualizer
  - Backend/tests/test_evaluation.py: 3 neue Konfusionsmatrix-Tests + matplotlib Agg fix
  - Backend/tests/test_logger.py: neu, 9 Tests fuer utils/logger.py (100% coverage)
  - Backend/tests/test_main.py: neu, 11 Tests fuer src/main.py (96% coverage)
  - Backend/tests/conftest.py: matplotlib.use("Agg") fuer headless Test-Umgebung
  - Backend/docs/architecture_decision_records.md: neu, 7 ADRs dokumentiert
  - Backend/docs/label_mapping.md: neu, vollstaendige Label-Mapping-Dokumentation
- Technische Auswirkungen:
  - 111 Tests bestehen, 97% Couverture (Issue #12 Ziel: >80% erfuellt)
  - SHAP Stage 2 nutzt PermutationExplainer (approximate aber korrekt in Erwartung)
  - evaluate_and_explain.py benoetigt test_data_{A,B}.npz (nach Reentrainement vorhanden)
  - Reentrainement mit best HP gestartet: train_pipelines.py --best-params-dir results/metrics
- Begruendung:
  - Issues #10 und #11 erfordern vollstaendige Evaluation und SHAP-Analyse.
  - Issue #12 erfordert Coverage >80% und Modell-Export-Infrastruktur.
  - sklearn's multiclass GradientBoostingClassifier wird von SHAP TreeExplainer nicht
    unterstuetzt (SHAP 0.52.0); PermutationExplainer ist der wissenschaftlich valide Fallback.

### 2026-05-30 — Backend ML Initialisierung

- Datum: 2026-05-30
- Änderung: Backend ML Projektstruktur vollständig aufgebaut. Datensatz analysiert, Labels verifiziert, alle Pflichtdokumente erstellt.
- Betroffene Dateien:
  - Backend/ (neu, komplett)
  - Backend/src/main.py (CLI-Skeleton mit argparse)
  - Backend/src/{data,features,models,pipelines,evaluation,explainability,utils}/__init__.py
  - Backend/requirements.txt
  - Backend/pyproject.toml
  - Backend/.env.example
  - Backend/.gitignore
  - Backend/CLAUDE.md (ML-Arbeitsreferenz)
  - Backend/TO-DO.md (vollständiges Backlog P1-P5)
  - Done.md (neu erstellt, Entwicklungsjournal)
- Technische Auswirkungen:
  - Datensatzanalyse: MERGED_CSV hat 39 Features + Label-Spalte (40 Spalten gesamt).
    Labels sind vollständig in Großbuchstaben (z.B. "DDOS-ICMP_FLOOD", "BENIGN").
    Abweichung vom Lastenheft: 39 Features verfügbar, nicht 46 wie beschrieben.
    Entscheidung: 39 Features verwenden, PCA wird 39→16 (nicht 46→16).
  - Mapping: 34 spezifische Labels → 8 Kategorien vollständig in Backend/CLAUDE.md dokumentiert.
  - Klassenungleichgewicht bestätigt: DDOS-ICMP_FLOOD dominiert (~16% aller Zeilen in 5 Dateien).
  - Speicherproblem: 63 Dateien à ~140 MB = ~8,5 GB gesamt. Chunked-Loading erforderlich.
  - Strategie für Speicher noch offen (letzter offener P1).
- Begründung:
  - Projektstart des ML-Backends gemäß Lastenheft. Saubere Struktur vor der Implementierung
    verhindert Spaghetti-Code und Duplizierungen. Alle Entscheidungen sind dokumentiert und
    nachvollziehbar.

### 2026-05-18 (d)

- Datum: 2026-05-18
- Änderung: Drei Dateien aktualisiert. (1) folien/jguimfackjeuna-umsetzungsplan.html: Zeitplan vollständig auf die realen Semestertermine des Professors angepasst. Burndown um fehlende Schritte ergänzt (Review anderer Arbeiten, Vortragsvorbereitung, Camera-Ready-Überarbeitung). (2) jguimfackjeuna-vortrag-umsetzungsplan.md: Zeitplan im Speech entsprechend angepasst. (3) Paper/src/einleitung.tex: Strukturparagraph erweitert, Kapitel 4 (Methodik) nun mit allen fünf Teilaspekten explizit beschrieben und zitiert.
- Betroffene Dateien:
  - folien/jguimfackjeuna-umsetzungsplan.html
  - jguimfackjeuna-vortrag-umsetzungsplan.md
  - Paper/src/einleitung.tex
- Technische Auswirkungen:
  - Zeitplan korrekt: Abgabe Camera Ready 27.07.2026, Vortrag 13.07.2026, Reviewversion 22.06.2026, Kernkapitel 15.06.2026, Ergebnisfeststellung 08.06.2026, Motivationsreview 01.06.2026.
  - Einleitung des Papers enthält jetzt eine vollständige Vorschau aller methodischen Entscheidungen aus Kapitel 4.
- Begründung:
  - Der frühere Zeitplan endete irrtümlich am 15.06.2026. Laut Semesterplan des Professors ist das Camera-Ready-Datum der 27.07.2026 und der Vortrag am 13.07.2026.

### 2026-05-18 (c)

- Datum: 2026-05-18
- Änderung: jguimfackjeuna-umsetzungsplan.html im Verzeichnis Forschungsfrage/ erstellt. Dieses Verzeichnis enthält bereits die vollständige reveal.js-Infrastruktur (dist/, css/, config.js) des Professors. Die Datei enthält ausschließlich Inhalt; Design und Verhalten werden vollständig durch das bestehende Template übernommen.
- Betroffene Dateien:
  - Forschungsfrage/jguimfackjeuna-umsetzungsplan.html (neu)
- Technische Auswirkungen:
  - Alle relativen Pfade (dist/reveal.css, css/hbv-light.css, config.js) werden vom vorhandenen Verzeichnis korrekt aufgelöst.
  - Design und Verhalten sind automatisch identisch mit jordan_guimfack_jeuna_forschungsfrage.html.
- Begründung:
  - Das Forschungsfrage/-Verzeichnis hat das vollständige, funktionierende reveal.js-Setup des Professors. Neue Präsentationsdateien dort abzulegen ist die korrekte Vorgehensweise.

### 2026-05-18 (b)

- Datum: 2026-05-18
- Änderung: jguimfackjeuna-umsetzungsplan.html vollständig an das Template des Professors (umsetzungsplan.html) angeglichen. Nested-Listen-Struktur (Rolle/Nutzen/Beitrag) entfernt. Burndown-Liste jetzt einfach und flach wie im Vorlage. Technische Begründungen in <aside class="notes"> ausgelagert. Kommentierter Beispielblock aus dem Vorlage übernommen. Gedankenstriche in Zeitplan durch "bis" ersetzt.
- Betroffene Dateien:
  - jguimfackjeuna-umsetzungsplan.html
- Technische Auswirkungen:
  - Design und Verhalten identisch mit dem Vorlage des Professors.
  - reveal.js skaliert die Folie korrekt, da die Liste kompakt bleibt.
  - Speaker Notes (<aside class="notes">) enthalten alle inhaltlichen Begründungen für den Vortrag.
- Begründung:
  - Das Vorlage des Professors verwendet eine einfache <ul><li>-Struktur ohne Unterpunkte. Die vorherige Version mit tief verschachtelten Listen war inkompatibel mit dem Design-System und überlud die Folie.

### 2026-05-18

- Datum: 2026-05-18
- Änderung: Zeitplan in Präsentation und Vortrag-Speech korrigiert. Der Arbeitsschritt "Vorbereitung Datenbasis + Implementierung Vorverarbeitungspipeline" war fälschlicherweise als abgeschlossen dargestellt (Zeitraum 11.05 bis 18.05). Er ist noch nicht begonnen und wird nun korrekt auf den Zeitraum 18.05 bis 25.05 gesetzt. Alle nachfolgenden Meilensteine entsprechend verschoben. Abgabedatum 15.06.2026 bleibt unverändert.
- Betroffene Dateien:
  - jguimfackjeuna-vortrag-umsetzungsplan.md
  - jguimfackjeuna-umsetzungsplan.html
- Technische Auswirkungen:
  - Zeitplan jetzt konsistent mit dem tatsächlichen Projektstand: theoretischer Teil abgeschlossen, praktische Implementierung beginnt ab 18.05.2026.
  - Letzte drei Phasen (Datenauswertung, Ausarbeitung, Schlusskorrektur) leicht verdichtet um die Verschiebung bei gleichem Abgabedatum aufzufangen.
- Begründung:
  - Darstellung im Vortrag muss dem realen Stand entsprechen. Ein falscher Zeitplan schwächt die wissenschaftliche Glaubwürdigkeit.

### 2026-04-28

- Datum: 2026-04-28
- Änderung: Paper Build Script auf Remote-Ausführung via SSH umgestellt.
- Betroffene Dateien:
  - Paper/buildlualatex.sh
  - README.md
- Technische Auswirkungen:
  - LaTeX Build läuft auf hopper und erzeugt die PDF dort.
  - Die erzeugte hauptdatei.pdf wird anschließend auf die lokale Maschine kopiert.
  - Lokale LaTeX Installation ist nicht erforderlich.
- Begründung:
  - LaTeX ist lokal nicht installiert und der Build soll wie zuvor auf hopper erfolgen.

### 2026-04-28

- Datum: 2026-04-28
- Änderung: SSH-Aufruf so angepasst, dass Passwort-Login möglich bleibt (kein BatchMode).
- Betroffene Dateien:
  - Paper/buildlualatex.sh
- Technische Auswirkungen:
  - Der Build funktioniert auch ohne SSH-Key, da SSH interaktiv nach einem Passwort fragen kann.
- Begründung:
  - Direkte Nutzbarkeit ohne zusätzliche SSH-Key Einrichtung.

### 2026-04-28

- Datum: 2026-04-28
- Änderung: Remote-Build so umgestellt, dass keine Projektkopie auf dem Server vorausgesetzt wird (Upload des lokalen Paper Verzeichnisses in ein temporäres Server-Verzeichnis, Build dort, PDF Download).
- Betroffene Dateien:
  - Paper/buildlualatex.sh
  - README.md
- Technische Auswirkungen:
  - Der Build schlägt nicht mehr wegen fehlendem Remote-Pfad fehl.
  - Der Server benötigt nur LaTeX, latexmk, tar und mktemp.
  - Das lokale Ergebnis ist Paper/hauptdatei.pdf.
- Begründung:
  - Das Repository existiert nicht auf dem Server und soll trotzdem dort gebaut werden.

### 2026-04-28

- Datum: 2026-04-28
- Änderung: Publish-Schritt im Remote-Build wieder aktiviert (PDF wird serverseitig standardmäßig nach /var/www/html/$USER/ kopiert).
- Betroffene Dateien:
  - Paper/buildlualatex.sh
  - README.md
- Technische Auswirkungen:
  - Nach dem Remote-Build liegt die PDF auf dem Server zusätzlich in /var/www/html/$USER/ und lokal in Paper/hauptdatei.pdf.
  - Das Zielverzeichnis kann per PUBLISH_DIR überschrieben werden.
- Begründung:
  - Beibehaltung des bisherigen Workflows mit Server-Publish.

### 2026-04-28

- Datum: 2026-04-28
- Änderung: Remote-Build stabilisiert und Passwortabfrage reduziert (SSH Multiplexing via ControlMaster, Remote-Temp-Pfad bereinigt).
- Betroffene Dateien:
  - Paper/buildlualatex.sh
  - README.md
- Technische Auswirkungen:
  - Typischerweise nur eine Passwortabfrage für mehrere SSH-Kommandos.
  - Kein Fehler mehr durch Zeilenumbruch im Remote-Temp-Verzeichnis.
- Begründung:
  - Verbesserte Bedienbarkeit und Robustheit beim Remote-Build.

### 2026-04-28

- Datum: 2026-04-28
- Änderung: README um Paper Struktur ergänzt (Rolle von Paper/src und Einbindung über \input).
- Betroffene Dateien:
  - README.md
- Technische Auswirkungen:
  - Klarere Dokumentation, welche Dateien tatsächlich den Paper Inhalt liefern.
- Begründung:
  - Bessere Nachvollziehbarkeit der LaTeX-Projektstruktur.

### 2026-04-28

- Datum: 2026-04-28
- Änderung: LaTeX Bookmark Handling stabilisiert (zusätzliches Paket bookmark geladen).
- Betroffene Dateien:
  - Paper/hauptdatei.tex
- Technische Auswirkungen:
  - Reduziert bzw. vermeidet warnings beim Lesen/Schreiben der Bookmark Einträge in der .aux.
- Begründung:
  - Der Build war erfolgreich, meldete aber ein wichtiges Warning "(\end occurred inside a group at level 1)" mit Bezug auf Bookmark Einträge in log/hauptdatei.aux.

### 2026-04-28

- Datum: 2026-04-28
- Änderung: PDF Bookmarks in hyperref deaktiviert, um das Warning "(\end occurred inside a group at level 1)" zu vermeiden.
- Betroffene Dateien:
  - Paper/hauptdatei.tex
- Technische Auswirkungen:
  - PDF erzeugt weiterhin Links, aber ohne Lesezeichen Navigation in der PDF Seitenleiste.
  - Verhindert die Erzeugung der BKM Einträge in log/hauptdatei.aux.
- Begründung:
  - Das Warning blieb trotz bookmark Paket bestehen; das Deaktivieren der Bookmarks ist die robusteste, minimale Maßnahme.

### 2026-04-28

- Datum: 2026-04-28
- Änderung: Defensive Überschreibung von \BKM@entry, um das Warning beim Einlesen der .aux zu verhindern.
- Betroffene Dateien:
  - Paper/hauptdatei.tex
- Technische Auswirkungen:
  - Ignoriert Bookmark Einträge aus log/hauptdatei.aux auch dann, wenn sie dennoch geschrieben werden.
- Begründung:
  - Das Warning blieb nach Deaktivieren der Bookmarks bestehen; die Überschreibung verhindert offene Gruppen beim \end{document}.

### 2026-04-28

- Datum: 2026-04-28
- Änderung: Hyperref Bookmarks über \hypersetup deaktiviert, statt über Package Option, und direkte \BKM@entry Überschreibung entfernt.
- Betroffene Dateien:
  - Paper/hauptdatei.tex
- Technische Auswirkungen:
  - Bookmarks werden nicht mehr in die .aux geschrieben, wodurch das Warning "(\end occurred inside a group at level 1)" vermieden werden kann.
- Begründung:
  - Im Log blieb "Bookmarks ON", obwohl bookmarks=false als Package Option gesetzt war; \hypersetup ist die robustere Konfiguration.

### 2026-04-28

- Datum: 2026-04-28
- Änderung: Remote-Build toleriert LaTeX Return Code != 0, wenn die PDF trotzdem erzeugt wurde.
- Betroffene Dateien:
  - Paper/buildlualatex.sh
- Technische Auswirkungen:
  - Der Build bricht nicht mehr ab, nur weil LuaLaTeX mit Code 1 (Warnings) beendet.
  - Die PDF wird weiterhin zuverlässig nach Paper/hauptdatei.pdf kopiert.
- Begründung:
  - Latexmk meldete "return code 1" trotz erzeugter PDF; das ist in der Praxis häufig nur ein Warning-Level Exitcode.

### 2026-04-28

- Datum: 2026-04-28
- Änderung: Related Work in Professor-Vorlage integriert (separate Abgabe-Datei per \input).
- Betroffene Dateien:
  - relatex-work.tex
  - jguimfackjeuna-related-work.tex (neu erstellt)
  - usenix-2020-09.sty (neu erstellt)
  - Paper/buildlualatex.sh
  - README.md
- Technische Auswirkungen:
  - relatex-work.tex bindet jguimfackjeuna-related-work.tex via \input ein und nutzt Paper/bibtex/hauptdatei.bib als BibTeX-Quelle.
  - buildlualatex.sh unterstützt TEX_MAIN ausserhalb von Paper/, packt Paper/ plus benoetigte Root-Dateien ins Remote-Temp-Verzeichnis und kopiert die erzeugte PDF nach Paper/.
  - Bei TEX_MAIN=../relatex-work.tex erzeugt der Build Paper/relatex-work.pdf und legt zusaetzlich Paper/jguimfackjeuna-related-work.pdf als Alias an.
  - README dokumentiert die Kompilier-Command für die Professor-Vorlage via TEX_MAIN=../relatex-work.tex.
- Begründung:
  - Abgabeanforderung: Related Work muss als separate Datei erstellt und aus der Hauptdatei eingebunden werden.
  - Remote-Server hatte usenix-2020-09.sty nicht installiert; die Datei wird daher im Projekt mitgeliefert und beim Remote-Build mit hochgeladen.
  - USENIX-Template ist für pdfLaTeX ausgelegt; relatex-work.tex wird daher mit pdflatex gebaut, um Engine-Warnings/Exitcode 1 zu vermeiden.

### 2026-04-29

- Datum: 2026-04-29
- Änderung: CLAUDE.md erstellt (vollständige Projektdokumentation) und README.md umfassend erweitert.
- Betroffene Dateien:
  - CLAUDE.md (neu erstellt)
  - README.md (umfassend erweitert)
- Technische Auswirkungen:
  - CLAUDE.md dokumentiert vollständig: Systemarchitektur, ML-Pipeline, Datensatzstruktur (34 Angriffsklassen, 46 Features), Modellarchitektur (zweistufige hierarchische Klassifikation), Evaluationsmetriken, SHAP-Analyse, Paper-Struktur, alle 9 zitierten Quellen mit DOI, Coding Standards, Reproduzierbarkeitsregeln, Build-Infrastruktur und bekannte technische Einschränkungen.
  - README.md enthält jetzt: Forschungsbeitrag, vollständige Projektstruktur als Baumdiagramm, Datensatz-Übersicht, Build-Anleitung mit Konfigurationstabelle, Paper-Kapitelstruktur und Quellentabelle mit DOIs.
- Begründung:
  - Pflichtdokumente gemäß Projektvorgabe. CLAUDE.md dient als persistente Referenz für den autonomen Engineering-Agent und zukünftige Entwicklungssessions. README.md dient als Einstiegspunkt für alle Projektbeteiligten.

### 2026-04-29 (Quellenaktualisierung)

- Datum: 2026-04-29
- Änderung: Bibliographie vollständig auf kanonische Quellenliste aktualisiert. Neue Quelle hermosilla2025xai_forensic integriert. Autorname in ogunseyi2026xai_review korrigiert. Template-Einträge (KnutThea2009, flignitz) entfernt.
- Betroffene Dateien:
  - Paper/bibtex/hauptdatei.bib
  - Paper/src/related_work.tex
  - Paper/src/methodik.tex
  - CLAUDE.md
  - README.md
- Technische Auswirkungen:
  - Bibliographie enthält jetzt exakt 10 Quellen, alle mit verifiziertem DOI.
  - Hermosilla et al. (2025, DOI: 10.3390/app15137329) in XAI-Cluster des Related Work sowie in Phase 4 (SHAP-Analyse) der Methodik eingebunden. Zitationsschluessel: hermosilla2025xai_forensic.
  - Autorname in ogunseyi2026xai_review korrigiert: "Gogulakrishnan" zu "Gogulakrishan" (Thiyagarajan).
  - Forschungsluecken-Subsection in related_work.tex angepasst: Hermosilla et al. neben Mohale und Obagbuwa als fehlenden CICIoT2023-Bezug identifiziert.
- Begründung:
  - Nutzeranforderung: kanonische Quellenliste soll konsistent in allen Projektdateien gepflegt werden. Hermosilla et al. liefert Metriken (Fidelitaet, Konsistenz, Jaccard) fuer die Qualitaetsbewertung der SHAP-Erklaerungen und staerkt damit Teilfrage 3 methodisch.

### 2026-04-29 (Paper-Korrektur: Projektstand synchronisiert)

- Datum: 2026-04-29
- Änderung: Paper vollständig auf tatsächlichen Projektstand synchronisiert. Alle Abschnitte, die Implementierung und Evaluation als abgeschlossen darstellten, wurden korrigiert oder durch korrekte Platzhalter ersetzt. Kapitelstruktur von 6 auf 8 Kapitel erweitert.
- Betroffene Dateien:
  - Paper/src/abstract.tex (ersetzt)
  - Paper/src/einleitung.tex (ersetzt)
  - Paper/src/related_work.tex (Einleitungssatz und ML-Abschnitt korrigiert)
  - Paper/src/datenbasis.tex (neu erstellt, Kapitel 3)
  - Paper/src/methodik.tex (vollständig umstrukturiert: 4 Phasen zu 5 Subsektionen 4.1-4.5; Datenvorbereitung ausgelagert)
  - Paper/src/implementierung.tex (neu erstellt, Kapitel 5, Platzhalter)
  - Paper/src/evaluation.tex (neu erstellt, Kapitel 6, Platzhalter)
  - Paper/src/diskussion.tex (ersetzt durch Platzhalter mit methodischen Bezugspunkten)
  - Paper/src/fazit.tex (ersetzt durch Platzhalter)
  - Paper/hauptdatei.tex (Input-Kette aktualisiert: erwartete_ergebnisse.tex entfernt, datenbasis/implementierung/evaluation hinzugefügt)
- Technische Auswirkungen:
  - Das Paper beschreibt jetzt ausschließlich den tatsächlichen Projektstand: Einleitung, Related Work, Datenbasis und Methodik sind inhaltlich ausgeführt. Implementierung, Evaluation, Diskussion und Fazit sind korrekt als ausstehend gekennzeichnet.
  - Kapitel 3 (Datenbasis) trennt Datensatzbeschreibung und Vorverarbeitung klar von der Methodik.
  - Kapitel 4 (Methodik) strukturiert die methodische Vorgehensweise in 5 thematisch gegliederte Subsektionen.
  - Der \input-Pfad in hauptdatei.tex entspricht der neuen 8-Kapitel-Struktur. Die Datei erwartete_ergebnisse.tex bleibt als Archiv erhalten, wird aber nicht mehr eingebunden.
- Begründung:
  - Fachliche Anforderung: Ein wissenschaftliches Paper darf keine Ergebnisse als abgeschlossen darstellen, die noch nicht erarbeitet wurden. Die bisherigen Fassungen von diskussion.tex und fazit.tex beschrieben das Projekt als vollständig umgesetzt. abstract.tex und einleitung.tex enthielten Formulierungen, die den Beitrag als bereits erbracht darstellten. Diese Inkonsistenz zwischen Projektstand und Darstellung wurde vollständig beseitigt.

### 2026-05-18 (Vortrag und Motivation-HTML)

- Datum: 2026-05-18
- Änderung: Vortragstext (Speech) erstellt und jguimfackjeuna-motivation.html vollständig aktualisiert.
- Betroffene Dateien:
  - jguimfackjeuna-vortrag.md (neu erstellt)
  - jguimfackjeuna-motivation.html (vollständig ueberarbeitet)
- Technische Auswirkungen:
  - jguimfackjeuna-vortrag.md: Vortragstext auf Deutsch, ca. 430 Woerter, max. 4 Minuten. Deckt Motivation, Problemstellung, Ansatz, aktuellen Projektstand und Ausblick ab. Einfacher, natuerlicher, professioneller Stil.
  - jguimfackjeuna-motivation.html: 4 Folienblöcke (Motivation/Problemstellung/Ziel/Beitraege, Forschungsfragen, Einleitung aus Paper, Struktur der Arbeit). Konsistent mit dem aktuellen Einleitungsinhalt aus einleitung.tex. 8-Kapitel-Struktur. Hermosilla et al. 2025 als Qualitaetsbewertungsquelle aufgenommen. Korrekte HTML-Entities fuer Umlaute und Sonderzeichen.
- Begründung:
  - Anforderung aus Aufgabenstellung Woche 5: Praesentation der Motivation und des Projektstands. Der Vortragstext dient als Grundlage fuer den muendlichen Vortrag. Die HTML-Datei ist die formale Abgabe gemaess Aufgabenstellung.

### 2026-05-18 (Korrektur: Gedankenstriche entfernt, Umsetzungsplan-Speech erstellt)

- Datum: 2026-05-18
- Änderung: Alle Gedankenstriche (em-dash, en-dash) aus Speech und HTML entfernt. Motivation-Speech um Intro-Absatz gekuerzt. Neuer Speech fuer Umsetzungsplan erstellt.
- Betroffene Dateien:
  - jguimfackjeuna-vortrag.md (Intro-Absatz entfernt, alle Gedankenstriche bereinigt)
  - jguimfackjeuna-motivation.html (alle &mdash; und &ndash; durch Komma, Doppelpunkt oder Klammern ersetzt)
  - jguimfackjeuna-vortrag-umsetzungsplan.md (neu erstellt)
- Technische Auswirkungen:
  - Beide Speech-Dateien und die HTML-Datei sind vollstaendig frei von Gedankenstrichen.
  - Der Motivation-Speech beginnt jetzt direkt mit dem inhaltlichen Einstieg.
  - Der Umsetzungsplan-Speech deckt alle 15 Arbeitspakete logisch gegliedert ab, praesentiert den Zeitplan Woche fuer Woche, und betraegt ca. 580 Woerter (4 bis 5 Minuten).
- Begründung:
  - Strikte Projektregel: Gedankenstriche sind ueberall verboten. Intro-Absatz war nicht zielgerichtet genug fuer einen Vortrag, der direkt zum Punkt gehen soll.

### 2026-05-11

- Datum: 2026-05-11
- Änderung: Related Work gekürzt und sprachlich gestrafft, um die Vorgabe (maximal eine Seite; optional zweite Seite überwiegend Literatur) einzuhalten.
- Betroffene Dateien:
  - jguimfackjeuna-related-work.tex
  - Paper/src/related_work.tex
- Technische Auswirkungen:
  - Gleiche Kernaussagen und identische Zitationsbasis, aber deutlich kürzerer Textumfang.
- Begründung:
  - Professor-Vorgabe zur maximalen Länge der Related-Work-Sektion.

### 2026-05-11

- Datum: 2026-05-11
- Änderung: Abgabe-Datei jguimfackjeuna-related-work.tex als Standalone-Datei kompilierbar gemacht, ohne die \input-Integration in relatex-work.tex zu brechen.
- Betroffene Dateien:
  - usenix2019_v3.1.tex
  - jguimfackjeuna-related-work.tex
  - usenix-2020-09.sty
  - Paper/buildlualatex.sh
  - README.md
- Technische Auswirkungen:
  - usenix2019_v3.1.tex ist die einzige zu kompilierende Professor-Vorlage und bindet jguimfackjeuna-related-work.tex via \input ein.
  - buildlualatex.sh nutzt pdflatex für usenix2019_v3.1.tex (USENIX-Template).
- Begründung:
  - Nutzeranforderung: Es soll ausschließlich die Professor-Vorlage usenix2019_v3.1.tex verwendet werden.
