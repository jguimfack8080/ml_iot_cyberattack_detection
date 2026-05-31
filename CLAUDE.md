# CLAUDE.md

## ABSOLUT VERBOTENE REGEL -- KEINE AUSNAHMEN

**Gedankenstriche (-- und ---) sind absolut und ueberall verboten**: in LaTeX-Dateien,
Commit-Nachrichten, Issues, PR-Beschreibungen, Kommentaren und Dokumentation.
Keine einzige Ausnahme. Diese Regel gilt immer und ohne Ausnahme.

**Halluzination ist verboten.** Jede Behauptung im Paper muss direkt auf eine der
10 verifizierten Quellen (mit DOI) oder auf echte Experimentergebnisse zurueckfuehrbar sein.
Bei Unsicherheit: signalisieren und nachfragen.

**Papiersprache: 100% Deutsch.** Alle .tex-Dateien ausschliesslich auf akademischem Deutsch.
Kein Englisch, kein Franzoesisch in den Paper-Dateien.

**Maximale Seitenanzahl: 10 Seiten** im USENIX-Zweispaltenformat. Niemals ueberschreiten.

**Backend-Venv ist obligatorisch.** Immer Backend/.venv/ verwenden, niemals Python-System.

---

## GitHub

Account: jguimfack8080
Repository: https://github.com/jguimfack8080/ml_iot_cyberattack_detection
Issues: Erstellt fuer alle 8 Projektmeilensteine

---

## Projektbeschreibung

Titel: Machine Learning zur Erkennung von Cyberangriffen in IoT-Netzwerken: Entwicklung und Evaluation eines erklaerbaren Gradient-Boosting-Klassifikators mit SHAP-Analyse auf dem CICIoT2023-Datensatz

Autor: Jordan Guimfack Jeuna (Matrikelnummer 38184)
Studiengang: Master Informatik, Vertrauenswuerdige Systeme (IVS), Hochschule Bremerhaven
Modul: IT-Sicherheit, Prof. Dr. Lars Fischer
Typ: Seminararbeit (Hausarbeit, keine Bachelorarbeit)
Datum: 2026-04-29

Das Projekt entwickelt und evaluiert einen erklaerbaren ML-basierten Intrusion Detection Classifier fuer IoT-Netzwerke. Der wissenschaftliche Beitrag besteht in der erstmaligen Kombination von Balanced Accuracy, einer zweistufigen hierarchischen Klassifikationsarchitektur und SHAP-basierter Erklaarbarkeit auf dem CICIoT2023-Datensatz.

---

## Systemarchitektur

### ML-Pipeline

```
CICIoT2023 CSV Daten
        |
        v
Datenvorbereitung (StandardScaler Normalisierung)
        |
   +----+----+
   |         |
Pipeline A  Pipeline B
PCA (46->16) Alle 46 Features
   |         |
   +----+----+
        |
        v
Zweistufiger hierarchischer Klassifikator
        |
     Stufe 1: Binaere Klassifikation
     DoS/DDoS vs. Nicht-DoS-Verkehr
        |
        v
     Stufe 2: Mehrklassenklassifikation
     Mirai / Reconnaissance / Spoofing /
     Brute-Force / Web-based / Benign
        |
        v
Evaluation (Balanced Accuracy, F1-Makro, Konfusionsmatrix)
        |
        v
SHAP-Analyse (Global: Feature-Importance pro Klasse,
              Lokal: Einzelfallanalyse Fehlklassifikationen)
```

### Datensatz: CICIoT2023

- Quelle: Canadian Institute for Cybersecurity (Neto et al., 2023)
- DOI: 10.3390/s23135941
- IoT-Geraete: 105 reale Geraete (Smart-TVs, IP-Kameras, Thermostate, usw.)
- Angriffsbedingungen: 33 spezifische Angriffe
- Angriffen Kategorien (8): DDoS, DoS, Mirai, Reconnaissance, Spoofing, Brute-Force, Web-based Attacks, Benign
- Features: 46 vorextrahierte Netzwerkmerkmale
- Struktur: Separate CSV-Dateien pro Angriffstyp + Benign-Traffic + gemischte Merged-CSVs

**Feature-Uebersicht (aus rohen CSVs, 39 Spalten sichtbar):**
Header_Length, Protocol_Type, Time_To_Live, Rate, fin_flag_number, syn_flag_number,
rst_flag_number, psh_flag_number, ack_flag_number, ece_flag_number, cwr_flag_number,
ack_count, syn_count, fin_count, rst_count, HTTP, HTTPS, DNS, Telnet, SMTP, SSH, IRC,
TCP, UDP, DHCP, ARP, ICMP, IGMP, IPv, LLC, Tot_sum, Min, Max, AVG, Std, Tot_size,
IAT, Number, Variance

**Verzeichnisstruktur Datensatz:**
- Dataset/CSV/: Rohe CSV-Dateien pro Angriffskategorie (34 Unterordner inkl. Benign)
- Dataset/MERGED_CSV/: Gemischte CSVs (Merged01.csv bis Merged63.csv)

**Angriffsklassen im Dataset/CSV/:**
Backdoor_Malware, Benign_Final, BrowserHijacking, CommandInjection,
DDoS-ACK_Fragmentation, DDoS-HTTP_Flood, DDoS-ICMP_Flood, DDoS-ICMP_Fragmentation,
DDoS-PSHACK_FLOOD, DDoS-RSTFINFLOOD, DDoS-SlowLoris, DDoS-SYN_Flood,
DDoS-SynonymousIP_Flood, DDoS-TCP_Flood, DDoS-UDP_Flood, DDoS-UDP_Fragmentation,
DictionaryBruteForce, DNS_Spoofing, DoS-HTTP_Flood, DoS-SYN_Flood, DoS-TCP_Flood,
DoS-UDP_Flood, Mirai-greeth_flood, Mirai-greip_flood, Mirai-udpplain,
MITM-ArpSpoofing, Recon-HostDiscovery, Recon-OSScan, Recon-PingSweep,
Recon-PortScan, SqlInjection, Uploading_Attack, VulnerabilityScan, XSS

---

## Modellarchitektur und Trainingsstrategie

### Hauptmodell: Gradient Boosting

Begruendung: Raturi et al. (2026) zeigen empirisch, dass Gradient Boosting auf dem CICIoT2023-Datensatz eine Balanced Accuracy von 0,952 in der Mehrklassenklassifikation erzielt und vollstaendig SHAP-kompatibel ueber den TreeExplainer ist.

Bibliothek: scikit-learn GradientBoostingClassifier oder XGBoost (SHAP-Kompatibilitaet beider bestaetigt).

### Zweistufige Hierarchie (nach Raturi et al., 2026)

Stufe 1: Binaerer Klassifikator, separiert DoS/DDoS von allen anderen Klassen. Adressiert das extreme Klassenungleichgewicht strukturell.

Stufe 2: Mehrklassen-Klassifikator auf Nicht-DoS-Instanzen. Klassifiziert Mirai, Reconnaissance, Spoofing, Brute-Force, Web-based, Benign.

### Ablation Study

Zwei parallele Preprocessing-Pipelines werden verglichen:

- Pipeline A: PCA-Reduktion von 46 auf 16 Hauptkomponenten (Replikation aus Raturi et al., 2026)
- Pipeline B: Alle 46 originalen Features (Kontrollbedingung)

Ziel: Quantifizierung des PCA-Einflusses auf Balanced Accuracy und SHAP-Feature-Importance-Ranglisten.

### Hyperparameter-Optimierung

Grid Search ueber relevante Hyperparameter (n_estimators, max_depth, learning_rate, subsample). Ergebnisse in Ablation Study integriert.

---

## Evaluation und Metriken

### Primaere Metrik: Balanced Accuracy

Definition: arithmetisches Mittel der klassenspezifischen Recall-Werte (Sensitivitaet pro Klasse).
Begruendung: Robust gegenueber Klassenungleichgewicht. Ein Modell, das seltene Angriffsklassen ignoriert, erzielt trotz hoher Accuracy eine niedrige Balanced Accuracy.

### Sekundaere Metriken

- F1-Score (makro-gemittelt)
- Precision und Recall pro Klasse
- Konfusionsmatrizen (Stufe 1 und Stufe 2 separat)

### Vergleich Accuracy vs. Balanced Accuracy

Expliziter Nachweis des Verzerrungspotenzials einfacher Accuracy auf diesem Datensatz, wie von Hosseini et al. (2025) beschrieben.

---

## SHAP-Analyse

### Globale Ebene

Feature-Importance-Ranglisten pro Angriffsklasse, basierend auf mittleren absoluten SHAP-Werten ueber alle Testinstanzen. Zeigt, welche der 46 Netzwerkmerkmale die Klassifikation von DDoS, Mirai, Brute-Force am staerksten bestimmen.

### Lokale Ebene

Einzelfallanalysen ausgewaehlter Fehlklassifikationen. SHAP Waterfall Plots oder Force Plots fuer einzelne Instanzen.

### Semantische Validierung

Vergleich der SHAP-Feature-Importance gegen bekannte Netzwerksignaturen der Angriffstypen:
- DoS/DDoS: Paketrate (Rate), Verbindungsfrequenz (Number), TCP-Flags (syn_flag_number)
- Spoofing: Protokollfelder, Quell-Adressen korrelierte Features
- Brute-Force: Verbindungsanzahl, Authentifizierungsmerkmale

Grundlage fuer die Qualitaetsbewertung der SHAP-Erklaerungen: Hermosilla et al. (2025) fuhren Fidelitaet, Konsistenz und Jaccard-Aehnlichkeit als Metriken zur Bewertung von SHAP-Erklaerungsqualitaet ein (DOI: 10.3390/app15137329).

### Ablation SHAP

Vergleich der Feature-Importance-Ranglisten zwischen Pipeline A (PCA) und Pipeline B (Original-Features). Hypothese: PCA reduziert die semantische Interpretierbarkeit, da Hauptkomponenten lineare Kombinationen sind.

---

## Paper-Struktur (LaTeX)

**Hauptverzeichnis:** Paper/
**Hauptdatei:** Paper/hauptdatei.tex
**Kompilierung:** LuaLaTeX via Remote-SSH auf Server "hopper"

**Kapitelstruktur (Paper/src/):**
- abstract.tex: Kurzfassung mit Schluesselwoertern
- einleitung.tex: Kontext, Problemformulierung, Beitrag, Struktur
- related_work.tex: 4 Cluster (Datensaetze, ML-Ansaetze, Klassenungleichgewicht, XAI)
- methodik.tex: 4 Phasen (Datenvorbereitung, Klassifikation, Evaluation, SHAP)
- erwartete_ergebnisse.tex: Hypothesen und erwartete Resultate
- diskussion.tex: Beitrag, offene Fragen, Ausblick
- fazit.tex: Zusammenfassung und Schlussfolgerung

**Bibliographie:** Paper/bibtex/hauptdatei.bib (IEEE-Stil, BibLaTeX+Biber)

**Build-Script:** Paper/buildlualatex.sh (Remote-Build via SSH, ControlMaster)

**Zitierte Quellen (alle verifiziert mit DOI):**
1. Neto et al. (2023) - CICIoT2023. Sensors 23(13):5941. DOI: 10.3390/s23135941
2. Raturi et al. (2026) - ML auf CICIoT2023 (Ausgangspaper). Security and Privacy 9:e70220. DOI: 10.1002/spy2.70220
3. Almahaqeri et al. (2026) - Gradient Boosting CICIoT2023. Scientific Reports. DOI: 10.1038/s41598-026-47399-5
4. Alharby (2025) - ML auf CICIoT2023 mit PCA. Scientific Reports 15:39914. DOI: 10.1038/s41598-025-23711-7
5. Ogunseyi et al. (2026) - XAI-IDS PRISMA Review. Sensors 26(2):363. DOI: 10.3390/s26020363
6. Mohale und Obagbuwa (2025) - SHAP in IDS. Frontiers in CS 7:1520741. DOI: 10.3389/fcomp.2025.1520741
7. Hermosilla et al. (2025) - SHAP vs. LIME in IDS (Fidelitaet, Konsistenz, Jaccard). Applied Sciences 15(13):7329. DOI: 10.3390/app15137329
8. Kikissagbe und Adda (2024) - ML-IDS Review. Electronics 13(18):3601. DOI: 10.3390/electronics13183601
9. Hamedani et al. (2025) - IoT Security Survey. Sensors 25(11):3341. DOI: 10.3390/s25113341
10. Hosseini et al. (2025) - Klassenungleichgewicht IDS. Electronics 14(1):69. DOI: 10.3390/electronics14010069

---

## Technische Entscheidungen und Begruendungen

### Gradient Boosting als Hauptmodell

Raturi et al. (2026) belegen empirisch 0,952 Balanced Accuracy auf CICIoT2023. TreeExplainer von SHAP unterstuetzt baumbasierte Modelle nativ und ist recheneffizient gegenueber Kernel-basierten SHAP-Varianten.

### Balanced Accuracy als primaere Metrik

Der CICIoT2023-Datensatz ist stark unausgewogen. Hosseini et al. (2025) zeigen, dass einfache Accuracy bei IDS-Datensaetzen zu systematisch verzerrten Urteilen fuehrt. Raturi et al. (2026) zeigen konkret: HMM erreicht Recall 0,999 fuer DoS aber nur 0,13 in der Mehrklassenklassifikation.

### Zweistufige Hierarchie

Strukturelle Adressierung des Klassenungleichgewichts. DoS/DDoS dominieren den CICIoT2023-Datensatz erheblich. Trennung in Stufe 1 verhindert, dass Nicht-DoS-Klassen in der Mehrklassenklassifikation systematisch unterdrueckt werden.

### PCA-Ablation als Forschungsbeitrag

Raturi et al. (2026) setzen PCA (46 auf 16 Komponenten) ohne Analyse des Einflusses auf Erklaerbarkeit ein. Diese Luecke ist direkt adressierbar und stellt einen eigenstaendigen Beitrag dar.

---

## Coding Standards

- Sprache: Python 3.x
- Bibliotheken: scikit-learn, shap, pandas, numpy, matplotlib
- Reproduzierbarkeit: random_state=42 fuer alle stochastischen Komponenten
- Seeds: explizit gesetzt und dokumentiert
- Keine Hardcoded Paths: alle Pfade ueber Konfigurationsvariablen
- Logging: strukturiertes Logging von Metriken und Hyperparametern

## Python-Umgebung — PFLICHTREGELN

**WICHTIG: Immer im virtuellen Environment arbeiten. Niemals Pakete direkt auf dem System-Python installieren.**

### Virtuelles Environment

Pfad: `Backend/.venv/`

Erstellen (einmalig):
```bash
cd Backend
python -m venv .venv
```

Aktivieren (Windows):
```bash
.venv\Scripts\activate
```

Pakete installieren:
```bash
.venv/Scripts/pip install -r requirements.txt
```

Python/pytest ausfuehren (ohne Aktivierung):
```bash
.venv/Scripts/python src/main.py
.venv/Scripts/python -m pytest tests/
```

### Regeln

1. NIEMALS `pip install` ausserhalb des venv fuer dieses Projekt ausfuehren
2. IMMER `.venv/Scripts/python` statt `python` verwenden (Windows)
3. Das Verzeichnis `.venv/` ist in `.gitignore` eingetragen — nicht committen
4. Bei neuen Abhaengigkeiten: zuerst `requirements.txt` aktualisieren, dann im venv installieren
5. Diese Regel gilt fuer alle Sessions — kein Ausnahmen

### Begruendung

Der Nutzer hat explizit verlangt, dass das System-Python sauber bleibt. Alle ML-Abhaengigkeiten
(scikit-learn, shap, xgboost, pandas usw.) existieren ausschliesslich im venv.
Pakete, die versehentlich auf dem System-Python installiert wurden, muessen deinstalliert werden.

---

## Reproduzierbarkeit der Experimente

Folgende Massnahmen sichern die Reproduzierbarkeit:

1. Fixierter Random State (random_state=42) in allen scikit-learn Komponenten
2. Explizit dokumentierte Preprocessing-Reihenfolge (Normalisierung vor PCA, Split vor Fit)
3. Train/Test-Split: 80/20, stratifiziert nach Klasse
4. Alle Hyperparameter werden in der Arbeit angegeben
5. Datensatz CICIoT2023 oeffentlich verfuegbar unter https://www.unb.ca/cic/datasets/iotdataset-2023.html

---

## Dokumentationssystem

Pflichtdateien:
- CLAUDE.md: Dieses Dokument (Projektarchitektur und Richtlinien)
- README.md: Build-Anleitung und Projektueberblick
- PROJECT_LOG.md: Aenderungsprotokoll mit Datum, Dateien, Auswirkungen, Begruendung

Jede Aenderung im Projekt erfordert einen Eintrag in PROJECT_LOG.md mit:
- Datum
- Beschreibung der Aenderung
- Betroffene Dateien
- Technische Auswirkungen
- Begruendung

## ABSOLUT VERBOTENE REGEL -- Done.md und TO-DO.md PFLICHTAKTUALISIERUNG

**Diese Regel ist genauso streng wie die Gedankenstrich-Regel: keine Ausnahmen.**

Am Ende JEDER Session muessen folgende Dateien aktualisiert werden:

1. Backend/Done.md
   - Neue Session-Sektion hinzufuegen (chronologisch, immuabel)
   - Format: ### YYYY-MM-DD -- Session N : Titel
   - Inhalt: implementierte Dateien, Resultate (BA, F1, Trainingszeit), Entscheidungen
   - Alle Testergebnisse (Anzahl Tests, Coverage)

2. Backend/TO-DO.md
   - Erledigte Items: [ ] -> [x] mit Datum
   - Neue Items aus der Session hinzufuegen
   - Datum der letzten Aktualisierung oben aktualisieren

3. paper-usenix-template-jguimfackjeuna/Done.md
   - Gleiche Regel wie Backend/Done.md fuer alle Paper-Aenderungen
   - Jede .tex-Aenderung dokumentieren

4. paper-usenix-template-jguimfackjeuna/TO-DO.md
   - Gleiche Regel wie Backend/TO-DO.md

**Reihenfolge am Sessionende:**
1. Done.md aktualisieren
2. TO-DO.md aktualisieren
3. PROJECT_LOG.md aktualisieren
4. git commit mit allen Aenderungen (inkl. Done.md und TO-DO.md)

**Konsequenz bei Nichteinhaltung:** Dokumentation divergiert vom Code.
Dies ist kritisch fuer die wissenschaftliche Nachvollziehbarkeit der Seminararbeit.

---

## Paper Build (Remote SSH)

```bash
cd Paper
bash ./buildlualatex.sh
```

Environment-Variablen:
- REMOTE_HOST (Default: hopper)
- REMOTE_TMP_PARENT (Default: /tmp)
- TEX_MAIN (Default: hauptdatei.tex)
- OUTDIR (Default: log)
- PUBLISH_DIR (Default: /var/www/html/$USER/)
- KEEP_REMOTE (Default: 0)

Voraussetzungen auf dem Remote-Server:
- LuaLaTeX mit latexmk
- tar und mktemp
- biber (fuer BibLaTeX)
- Python 3 mit Pygments (fuer minted Code-Highlighting)

Ausgabe: Paper/hauptdatei.pdf (lokal) + /var/www/html/$USER/hauptdatei.pdf (Server)

---

## Security Best Practices

- SSH Verbindung ueber ControlMaster fuer reduzierte Passwort-Prompts
- Kein SSH BatchMode: interaktive Passwort-Eingabe moeglich
- Keine Credentials in Skripten oder Konfigurationsdateien
- Temporaere Remote-Verzeichnisse werden nach dem Build bereinigt (KEEP_REMOTE=0)

---

## Bekannte technische Einschraenkungen

- LaTeX PDF-Bookmarks deaktiviert (bookmarks=false in hyperref), um Warning "end occurred inside a group at level 1" zu vermeiden
- Build toleriert LaTeX Return Code != 0 sofern PDF erzeugt wurde (latexmk gibt manchmal Code 1 fuer Warnings)
- Lokale LaTeX-Installation nicht erforderlich (Build erfolgt remote)
