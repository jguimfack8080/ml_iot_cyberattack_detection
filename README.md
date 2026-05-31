---
title: ml_iot_cyberattack_detection
last_updated: 2026-04-29
---

# ml_iot_cyberattack_detection

Machine Learning zur Erkennung von Cyberangriffen in IoT-Netzwerken.
Seminararbeit im Modul IT-Sicherheit, M.Sc. Informatik IVS, Hochschule Bremerhaven.

Autor: Jordan Guimfack Jeuna (38184)
Betreuer: Prof. Dr. Lars Fischer

---

## Forschungsbeitrag

Erstmalige Kombination auf dem CICIoT2023-Datensatz:

1. Erklaerbarer Gradient-Boosting-Klassifikator mit SHAP-Integration
2. Balanced Accuracy als primaere Bewertungsmetrik
3. Quantitative Ablation Study zum Einfluss von PCA auf Modellleistung und SHAP-Feature-Importance

Ausgangspaper: Raturi et al. (2026), DOI: 10.1002/spy2.70220

---

## Projektstruktur

```
ml_iot_cyberattack_detection/
├── CLAUDE.md               Vollstaendige Projektdokumentation (Architektur, Richtlinien)
├── README.md               Dieses Dokument
├── PROJECT_LOG.md          Aenderungsprotokoll
├── Dataset/
│   ├── CSV/                Rohe CSV-Dateien pro Angriffstyp (34 Kategorien)
│   └── MERGED_CSV/         Gemischte CSVs (Merged01.csv bis Merged63.csv)
└── Paper/
    ├── hauptdatei.tex      LaTeX Hauptdatei
    ├── hauptdatei.pdf      Erzeugtes PDF (nach Build)
    ├── buildlualatex.sh    Remote-Build-Script (SSH nach hopper)
    ├── quickbuild.sh       Schnellbuild-Script
    ├── bibtex/
    │   └── hauptdatei.bib  BibLaTeX-Bibliographie (9 Quellen, alle mit DOI)
    ├── src/
    │   ├── abstract.tex
    │   ├── einleitung.tex
    │   ├── related_work.tex
    │   ├── methodik.tex
    │   ├── erwartete_ergebnisse.tex
    │   ├── diskussion.tex
    │   ├── fazit.tex
    │   └── basic_structure/
    │       ├── deckblatt.tex
    │       ├── abkuerzungen.tex
    │       ├── erklaerung.tex
    │       └── trennung.tex
    └── log/                LaTeX Build-Ausgabedateien
```

---

## Datensatz: CICIoT2023

- Quelle: Canadian Institute for Cybersecurity
- Referenz: Neto et al. (2023), Sensors 23(13):5941, DOI: 10.3390/s23135941
- 105 reale IoT-Geraete, 33 Angriffsbedingungen
- 46 vorextrahierte Netzwerkmerkmale
- 8 Angrifffskategorien: DDoS, DoS, Mirai, Reconnaissance, Spoofing, Brute-Force, Web-based Attacks, Benign

Angriffsklassen in Dataset/CSV/:
Backdoor_Malware, Benign_Final, BrowserHijacking, CommandInjection,
DDoS-ACK_Fragmentation, DDoS-HTTP_Flood, DDoS-ICMP_Flood, DDoS-ICMP_Fragmentation,
DDoS-PSHACK_FLOOD, DDoS-RSTFINFLOOD, DDoS-SlowLoris, DDoS-SYN_Flood,
DDoS-SynonymousIP_Flood, DDoS-TCP_Flood, DDoS-UDP_Flood, DDoS-UDP_Fragmentation,
DictionaryBruteForce, DNS_Spoofing, DoS-HTTP_Flood, DoS-SYN_Flood, DoS-TCP_Flood,
DoS-UDP_Flood, Mirai-greeth_flood, Mirai-greip_flood, Mirai-udpplain,
MITM-ArpSpoofing, Recon-HostDiscovery, Recon-OSScan, Recon-PingSweep,
Recon-PortScan, SqlInjection, Uploading_Attack, VulnerabilityScan, XSS

---

## Paper Build (Remote SSH)

LaTeX wird auf dem Remote-Server (hopper) ausgefuehrt. Das lokale Paper-Verzeichnis wird
in ein temporaeres Verzeichnis auf dem Server kopiert, dort gebaut, und die erzeugte
PDF wird zurueckkopiert. Lokal wird nur SSH benoetigt.

```bash
cd Paper
bash ./buildlualatex.sh
```

Ausgabe: Paper/<tex-main-basename>.pdf (lokal) + /var/www/html/$USER/<tex-main-basename>.pdf (Server)

### Professor-Vorlage (Related Work Abgabe)

Die Professor-Vorlage ist im Projekt-Root: usenix2019_v3.1.tex. Die abzugebende Related-Work-Datei ist: jguimfackjeuna-related-work.tex und wird in usenix2019_v3.1.tex via \input eingebunden.

Kompilieren der Professor-Vorlage ueber den gleichen Remote-Build:

```bash
cd Paper
TEX_MAIN=../usenix2019_v3.1.tex bash ./buildlualatex.sh
```

Ausgabe: Paper/usenix2019_v3.1.pdf (lokal) + /var/www/html/$USER/usenix2019_v3.1.pdf (Server)

Hinweis: usenix2019_v3.1.tex wird mit pdflatex gebaut (USENIX-Template), hauptdatei.tex mit lualatex.

### Konfiguration (Environment-Variablen)

| Variable         | Default                | Beschreibung                          |
|------------------|------------------------|---------------------------------------|
| REMOTE_HOST      | hopper                 | SSH-Hostname des Build-Servers        |
| REMOTE_TMP_PARENT| /tmp                   | Elternverzeichnis fuer Remote-Temp    |
| TEX_MAIN         | hauptdatei.tex         | LaTeX-Hauptdatei                      |
| OUTDIR           | log                    | Build-Ausgabeverzeichnis (Remote)     |
| PUBLISH_DIR      | /var/www/html/$USER/   | Publish-Zielverzeichnis (Remote)      |
| KEEP_REMOTE      | 0                      | 1 = temporaeres Remote-Dir behalten   |

### Voraussetzungen auf dem Remote-Server

- LuaLaTeX mit latexmk
- biber (BibLaTeX-Backend)
- Python 3 mit Pygments (fuer minted Code-Highlighting)
- tar und mktemp

### Hinweis

Der Build nutzt SSH Connection Multiplexing (ControlMaster). Das Passwort wird
typischerweise nur einmal abgefragt. Build toleriert LaTeX Return Code != 0,
sofern die PDF erzeugt wurde (latexmk gibt bei Warnings Code 1 zurueck).

---

## Paper-Kapitelstruktur

| Datei                    | Inhalt                                               |
|--------------------------|------------------------------------------------------|
| src/abstract.tex         | Abstract und Schluesselwoerter                       |
| src/einleitung.tex       | Kontext, Problem, Beitrag, Struktur                  |
| src/related_work.tex     | 4 Cluster: Datensaetze, ML-IDS, Imbalance, XAI      |
| src/methodik.tex         | 4 Phasen: Daten, Klassifikation, Evaluation, SHAP   |
| src/erwartete_ergebnisse.tex | Hypothesen und erwartete Resultate              |
| src/diskussion.tex       | Beitrag, offene Fragen, Ausblick                     |
| src/fazit.tex            | Zusammenfassung                                      |

---

## Wissenschaftliche Quellen (alle mit DOI verifiziert)

| Schluessel                | Autoren                     | Werk                               | DOI                              |
|--------------------------|-----------------------------|------------------------------------|----------------------------------|
| neto2023ciciot2023        | Neto et al.                | CICIoT2023 Dataset Paper           | 10.3390/s23135941                |
| raturi2026exploratory     | Raturi, Aryan, Pranav      | ML on CICIoT2023 (Ausgangspaper)   | 10.1002/spy2.70220               |
| almahaqeri2026gradient    | Almahaqeri et al.          | Gradient Boosting CICIoT2023       | 10.1038/s41598-026-47399-5       |
| alharby2025ciciot         | Alharby                    | ML auf CICIoT2023 mit PCA          | 10.1038/s41598-025-23711-7       |
| ogunseyi2026xai_review    | Ogunseyi et al.            | XAI-IDS PRISMA Review              | 10.3390/s26020363                |
| mohale2025xai             | Mohale, Obagbuwa           | SHAP in IDS                        | 10.3389/fcomp.2025.1520741       |
| hermosilla2025xai_forensic| Hermosilla et al.          | SHAP vs. LIME in IDS (Fidelitaet)  | 10.3390/app15137329              |
| kikissagbe2024review      | Kikissagbe, Adda           | ML-IDS Review                      | 10.3390/electronics13183601      |
| hamedani2025iotsurvey     | Hamedani et al.            | IoT Security ML Survey             | 10.3390/s25113341                |
| hosseini2025imbalance     | Hosseini et al.            | Klassenungleichgewicht in IDS      | 10.3390/electronics14010069      |

---

## Vollstaendige Projektdokumentation

Alle Architektur-, Design- und Entwicklungsrichtlinien sind in CLAUDE.md dokumentiert.
Alle Aenderungen werden in PROJECT_LOG.md protokolliert.
