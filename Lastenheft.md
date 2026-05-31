# Lastenheft und Forschungskonzept

**Studiengang:** Vertrauenswürdige Systeme **Modul:** IT-Sicherheit **Thema:** Machine Learning zur Erkennung von Cyberangriffen auf Basis des CICIoT2023-Datensatzes

---

## 1. Problemstellung und Motivation

Die Verbreitung von Internet-of-Things (IoT)-Geräten in Haushalten, Industrieanlagen und kritischer Infrastruktur wächst kontinuierlich. Diese Geräte sind strukturell schwach gesichert: begrenzte Rechenleistung, fehlende oder schwache Authentifizierung, selten aktualisierte Firmware. Sie bilden damit eine exponentiell wachsende Angriffsfläche für Bedrohungen wie Distributed-Denial-of-Service (DDoS)-Botnetze, Mirai-Varianten, Spoofing und Brute-Force-Kampagnen.

Klassische Intrusion Detection Systeme (IDS), die auf Signaturvergleich basieren, sind gegenüber neuartigen Angriffsmustern strukturell blind. Sie können Zero-Day-Angriffe nicht erkennen und passen sich nicht an sich verändernde Bedrohungslandschaften an. Machine-Learning (ML)-basierte Ansätze bieten eine datengetriebene Alternative, die Anomalien im Netzwerkverkehr ohne vorherigen Signaturabgleich identifizieren kann.

Das Ausgangspaper von Raturi et al. (2026) liefert in diesem Kontext einen wichtigen empirischen Beitrag: Es vergleicht vierzehn ML-Modelle auf dem CICIoT2023-Datensatz und zeigt, dass baumbasierte Modelle und Ensemble-Methoden die besten Erkennungsleistungen erzielen. Es lässt dabei drei methodische Lücken offen:

**Lücke 1:** Keine Erklärbarkeit der Modellentscheidungen. Die Modelle werden als Black Boxes evaluiert. Sicherheitsanalysten können nicht nachvollziehen, warum ein Paket als Angriff klassifiziert wurde.

**Lücke 2:** Keine Analyse der Fehlerfortpflanzung im zweistufigen Klassifikationsansatz. Ein Fehler in Stufe 1 pflanzt sich unkontrolliert in Stufe 2 fort.

**Lücke 3:** Keine Latenzmessungen. Die Modelle werden nicht auf ihre Einsetzbarkeit in ressourcenbeschränkten IoT-Umgebungen hin bewertet.

Diese Arbeit setzt an Lücke 1 an und erweitert das Forschungsfeld gezielt: Sie verbindet ML-basierte Angriffserkennung auf dem CICIoT2023-Datensatz mit einer integrierten Erklärbarkeitskomponente auf Basis von SHapley Additive Explanations (SHAP). Damit leistet sie einen eigenständigen wissenschaftlichen Beitrag, der über das Ausgangspaper hinausgeht.

---

## 2. Rahmenfrage

Wie kann ein ML-basiertes Intrusion Detection System für IoT-Netzwerke so gestaltet werden, dass es nicht nur leistungsfähig ist, sondern seine Klassifikationsentscheidungen für Sicherheitsanalysten anhand messbarer Explainable-Artificial-Intelligence (XAI)-Kriterien (Faithfulness, Stability, Comprehensibility) nachvollziehbar werden?

---

## 3. Hauptforschungsfrage

Inwieweit ermöglicht eine SHAP-Analyse eines Gradient-Boosting (GB)-Klassifikators auf dem CICIoT2023-Datensatz eine pro-Angriffsklasse nachvollziehbare Zuordnung von Netzwerkmerkmalen zu Klassifikationsentscheidungen, und in welchem Verhältnis steht diese Erklärbarkeit zur erreichten Balanced Accuracy des Modells?

---

## 4. Teilforschungsfragen

### Teilfrage 1: Klassenungleichgewicht und Per-Klassen-Performance

Welche Non-DoS-Angriffsklassen des CICIoT2023-Datensatzes (Mirai, Reconnaissance, Spoofing, Web-Based, Brute-Force, Benign) werden durch das vorhandene Klassenungleichgewicht von einem Gradient-Boosting-Klassifikator systematisch schlechter erkannt, wenn die Bewertung von Accuracy auf Balanced Accuracy und klassenspezifische Recall-Werte umgestellt wird, und in welchem Ausmaß weicht die Per-Klassen-Performance von der aggregierten Balanced Accuracy ab?

Diese Frage hat einen eigenständigen wissenschaftlichen Wert: Raturi et al. (2026) führen Balanced Accuracy zwar als fairere Metrik ein, berichten sie jedoch nur aggregiert. Die klassenspezifische Aufschlüsselung speziell für Gradient Boosting fehlt und ist für die Gestaltung zukünftiger IDS-Evaluierungen relevant.

### Teilfrage 2: Einfluss der Dimensionsreduktion auf Performance und Erklärungsstabilität

Welchen messbaren Einfluss hat die Principal Component Analysis (PCA)-basierte Dimensionsreduktion von 46 auf 16 Merkmale auf (a) die Balanced Accuracy des Gradient-Boosting-Modells und (b) die Stabilität sowie Interpretierbarkeit der SHAP-Erklärungen, wenn die Ergebnisse mit einer Pipeline ohne PCA unter Verwendung aller 46 Originalmerkmale verglichen werden?

Diese Frage geht über das Ausgangspaper hinaus: Raturi et al. wenden PCA an, ohne diesen Schritt zu analysieren. Die PCA-Vorverarbeitung wird hier selbst zum Untersuchungsgegenstand gemacht und in einer kontrollierten Ablation Study geprüft.

### Teilfrage 3: Semantische Validierung der SHAP-Erklärungen

Welche Netzwerkmerkmale des CICIoT2023-Datensatzes haben gemäß SHAP den größten Einfluss auf die Klassifikation der einzelnen Angriffstypen, und stimmen diese Merkmale mit den in der CIC-Dokumentation des Datensatzes sowie in etablierten IDS-Referenzwerken beschriebenen charakteristischen Netzwerksignaturen der jeweiligen Angriffe überein?

Diese Frage erzeugt einen direkten wissenschaftlichen Mehrwert: Sie verbindet die statistischen SHAP-Werte mit dem fachlichen Wissen über Angriffsmuster und bewertet damit die semantische Qualität der Erklärungen. Der Vergleichsrahmen wird bewusst auf die offizielle CIC-Dokumentation und etablierte IDS-Referenzwerke begrenzt, um den Abgleich nachvollziehbar zu halten.

---

## 5. Projektziel

Das Ziel dieser Arbeit ist die Entwicklung eines ML-basierten Angriffserkennungssystems für IoT-Netzwerke, das zwei Eigenschaften vereint, die in der bestehenden Literatur bisher nicht gemeinsam auf dem CICIoT2023-Datensatz untersucht wurden: hohe Erkennungsleistung gemessen an der Balanced Accuracy und interpretierbare Entscheidungsgrundlagen durch SHAP.

Ein einziges baumbasiertes Modell wird als Kernbeitrag vollständig implementiert, evaluiert und durch SHAP analysiert. Falls die verfügbare Zeit es erlaubt, kann ein zweites Modell als Vergleichspunkt hinzugefügt werden. Ein solcher Vergleich ist jedoch keine Pflichtanforderung, sondern eine mögliche Erweiterung, die den wissenschaftlichen Mehrwert zusätzlich verstärken würde.

Der wissenschaftliche Mehrwert liegt nicht in der Anzahl der implementierten Modelle, sondern in drei konkreten Beiträgen:

**Beitrag 1: Erklärbare IDS auf CICIoT2023.** Erstmalige Integration von SHAP in ein baumbasiertes Klassifikationsexperiment auf dem CICIoT2023-Datensatz mit Balanced Accuracy als primärer Bewertungsmetrik und klassenspezifischer Per-Class-Analyse.

**Beitrag 2: PCA-Einflussanalyse.** Quantitative Analyse des Einflusses der PCA-Dimensionsreduktion auf Modellleistung und SHAP-Erklärungsstabilität, die im Ausgangspaper fehlt.

**Beitrag 3: Semantische Erklärungsvalidierung.** Bewertung der SHAP-Ergebnisse im Licht des dokumentierten Fachwissens über IoT-Angriffsmuster, um zu prüfen, ob das Modell tatsächlich sicherheitsrelevante Signale lernt oder Artefakte des Datensatzes.

---

## 6. Datenbasis

**Datensatz:** CICIoT2023 **Herkunft:** Canadian Institute for Cybersecurity (CIC), University of New Brunswick (UNB) **Referenz:** Neto et al. (2023), Sensors, 23(13), 5941, DOI: 10.3390/s23135941 **Download:** https://www.unb.ca/cic/datasets/iotdataset-2023.html

Charakteristika des Datensatzes:

- 105 reale IoT-Geräte (Smart-TVs, Webcams, Thermostate, Bewegungsmelder, Smart-Leuchten)
- 33 Angriffsklassen, zusammengefasst in 7 Kategorien plus Benign: Denial of Service (DoS), DDoS, Mirai, Reconnaissance, Spoofing, Brute-Force, Web-based Attacks
- 46 vorextrahierte Netzwerkmerkmale im CSV-Format
- Stark unausgewogen zugunsten von DoS- und DDoS-Angriffen

---

## 7. Methodik

### 7.1 Datenvorbereitung

- Laden des CICIoT2023-Datensatzes in der CSV-Variante
- Reduktion der 33 Angriffsklassen auf 8 übergeordnete Kategorien
- Normalisierung mit StandardScaler
- Train-Test-Aufteilung mit festem Random Seed 42
- Zwei parallele Preprocessing-Pipelines:
    - Pipeline A: Mit PCA (Reduktion von 46 auf 16 Hauptkomponenten)
    - Pipeline B: Ohne PCA, alle 46 Merkmale (Kontrollbedingung für Teilfrage 2)

### 7.2 Klassifikationsansatz

Zweistufige hierarchische Klassifikation als konzeptioneller Rahmen aus Raturi et al. (2026):

- Stufe 1: Binäre Klassifikation DoS/DDoS versus Nicht-DoS
- Stufe 2: Mehrklassenklassifikation der Nicht-DoS-Kategorie

Dieser Rahmen wird übernommen, weil er das Klassenungleichgewichtsproblem strukturell adressiert. Er wird jedoch nicht einfach nachgebaut, sondern um die SHAP-Analyse auf beiden Stufen erweitert.

### 7.3 Implementiertes Modell

Als Hauptmodell wird **Gradient Boosting** implementiert. Diese Wahl begründet sich auf drei Kriterien:

Erstens liefert Gradient Boosting in Raturi et al. (2026) eine Balanced Accuracy von 0,952 in der Mehrklassenklassifikation, was es zu einem der stärksten Kandidaten für den vorliegenden Datensatz macht.

Zweitens ist Gradient Boosting vollständig SHAP-kompatibel über den TreeExplainer, der native und exakte SHAP-Werte ohne Approximationen liefert.

Drittens ist es als einzelnes Modell für eine Einzelperson in realistischer Zeit vollständig implementierbar, evaluierbar und erklärbar.

**Optionale Erweiterung (nur bei ausreichend verfügbarer Zeit):** Ein zweites Modell, etwa ein Decision Tree, könnte als Vergleichspunkt hinzugefügt werden. Der Decision Tree ist ebenfalls SHAP-kompatibel und strukturell einfacher, was einen Vergleich der Erklärungsqualität zwischen einem einfachen und einem komplexen baumbasierten Modell ermöglichen würde. Diese Erweiterung ist kein Pflichtbestandteil der Arbeit.

### 7.4 SHAP-Integration

SHAP wird ausschließlich als post-hoc-Erklärungskomponente eingesetzt, nicht als Preprocessing- oder Feature-Selection-Werkzeug. Die Analyse erfolgt auf zwei Ebenen:

**Globale Ebene:** Feature-Importance-Ranglisten pro Angriffsklasse. Welche der 46 Netzwerkmerkmale (bzw. 16 PCA-Komponenten) treiben die Klassifikation von DDoS, Mirai oder Brute-Force an?

**Lokale Ebene:** Einzelfallanalysen für ausgewählte Klassifikationen, insbesondere für Fehlklassifikationen. Warum wurde ein Mirai-Paket als Benign klassifiziert?

**Semantische Validierung:** Die SHAP-Ranglisten werden mit der CIC-Dokumentation des Datensatzes und etablierten IDS-Referenzwerken über die Netzwerksignaturen der jeweiligen Angriffstypen verglichen, etwa hohe Paketfrequenz bei DoS oder ungewöhnliche Protokollfelder bei Spoofing.

---

## 8. Evaluationsstrategie

### 8.1 Primäre Metrik

**Balanced Accuracy** als Hauptbewertungsgröße, definiert als Durchschnitt aus Sensitivität (Recall) und Spezifität. Diese Metrik ist robust gegenüber dem starken Klassenungleichgewicht im CICIoT2023-Datensatz und macht sichtbar, wenn ein Modell seltene Angriffsklassen systematisch ignoriert.

### 8.2 Sekundäre Metriken

- F1-Score (makro-gemittelt über alle Klassen)
- Precision und Recall pro Klasse
- Konfusionsmatrix pro Modell und Klassifikationsstufe
- Accuracy (zum Vergleich mit Raturi et al. und anderen Studien)

### 8.3 Ablation Study

Zwei kontrollierte Vergleiche am Hauptmodell mit identischer Modellkonfiguration:

- Mit PCA versus ohne PCA: Einfluss auf Balanced Accuracy, F1 und SHAP-Feature-Importance
- Standardhyperparameter versus optimierte Hyperparameter (Grid Search)

Falls ein zweites Modell implementiert wird, können diese Ablation-Ergebnisse zusätzlich zwischen den beiden Modellen verglichen werden. Dies ist jedoch eine optionale Erweiterung.

### 8.4 XAI-Qualitätsbewertung

Die Qualität der SHAP-Erklärungen wird anhand etablierter XAI-Kriterien bewertet:

- **Faithfulness:** Spiegeln die SHAP-Werte tatsächlich den Einfluss der Merkmale auf die Modellentscheidung wider?
- **Stability:** Liefern SHAP-Werte für ähnliche Instanzen ähnliche Erklärungen?
- **Comprehensibility:** Entsprechen die wichtigsten Features dem fachlichen Erwartungswissen über den jeweiligen Angriffstyp?

---

## 9. Literaturübersicht nach Priorität

### Priorität 1: Unverzichtbar

**Raturi, Aryan und Pranav (2026).** Ausgangspaper der Arbeit. Evaluiert ML-Modelle auf CICIoT2023, führt Balanced Accuracy ein und lässt drei methodische Lücken offen. Die eigene Arbeit adressiert Lücke 1 (fehlende Erklärbarkeit) eigenständig. Konkrete Funktion: Begründung der Forschungslücke und der Modellwahl.

**Neto et al. (2023).** Beschreibt Aufbau, Angriffsklassen und Vorverarbeitungslogik des CICIoT2023-Datensatzes. Konkrete Funktion: Datenbeschreibung, Begründung der Klassenstruktur, Vorverarbeitungsentscheidungen, sowie Referenzdokumentation für die semantische Validierung in Teilfrage 3.

### Priorität 2: Stark und direkt relevant

**Ogunseyi et al. (2026).** PRISMA-Review von 129 Studien (2018–2025). Belegt empirisch, dass SHAP in 98 Prozent aller XAI-IDS-Studien eingesetzt wird, ohne die Erkennungsgenauigkeit zu beeinträchtigen. Konkrete Funktion: Begründung der Methodenwahl SHAP, Argument gegen den Einwand des Genauigkeitsverlusts.

**Mohale und Obagbuwa (2025).** Evaluiert Decision Trees und XGBoost gemeinsam mit SHAP und LIME auf einem IDS-Datensatz. Zeigt konkret, wie globale und lokale SHAP-Analysen in einem Klassifikationsexperiment umgesetzt werden. Konkrete Funktion: Direkte methodische Vorlage für die eigene SHAP-Integration, Vorbild für die Visualisierung der Ergebnisse.

**Hermosilla et al. (2025).** Vergleicht SHAP und LIME auf XGBoost und TabNet im Kontext der Intrusion Detection. Führt konkrete Metriken zur Bewertung der Erklärungsqualität ein: Fidelität, Konsistenz und Jaccard-Ähnlichkeit. Konkrete Funktion: Direkte Grundlage für die XAI-Qualitätsbewertung in Teilfrage 3.

**Almahaqeri et al. (2026).** Verwendet CICIoT2023 mit Gradient Boosting und stratifiziertem Undersampling. Direkt vergleichbar mit dem eigenen Experiment, da gleicher Datensatz und gleiche Modellkategorie. Wählt jedoch eine andere Strategie für das Klassenungleichgewicht. Konkrete Funktion: Vergleichsgrundlage im Diskussionsteil, Begründung der Wahl der hierarchischen Klassifikation gegenüber Undersampling.

**Alharby (2025).** Evaluiert Gradient Boosting, Decision Tree und weitere ML-Modelle auf CICIoT2023, implementiert PCA als Feature-Selection-Methode und misst zusätzlich Trainings- und Vorhersagezeiten. Konkrete Funktion: Direkte Referenz für den PCA-Einsatz auf CICIoT2023, Vergleichsbasis für die eigene Ablation Study, Begründung warum PCA eine belegte Methode für diesen Datensatz ist.

**Kikissagbe und Adda (2024).** Systematischer Review über supervised, unsupervised und hybride ML-Ansätze für IoT-IDS. Konkrete Funktion: Theoretische Einbettung der Modellwahl, Begründung warum baumbasierte Ensemble-Methoden für IoT-IDS state-of-the-art sind.

### Priorität 3: Ergänzend für den Diskussionsteil

**Hamedani et al. (2025).** Survey über ML-basierte Sicherheitslösungen für IoT-Netzwerke (2020–2024). Kategorisiert ML-Techniken nach ihrer Anwendung in der IoT-Sicherheit und benennt offene Forschungsfragen. Konkrete Funktion: Theoretische Motivation des Forschungsthemas, Einbettung in den breiteren Forschungskontext.

**Hosseini et al. (2025).** Evaluiert ML-Algorithmen unter verschiedenen Graden von Klassenungleichgewicht in IDS-Datensätzen und vergleicht Resampling-Strategien anhand von F1-Score und G-Mean. Konkrete Funktion: Direkte theoretische und empirische Grundlage für Teilfrage 1, Begründung warum Accuracy allein als Metrik unzureichend ist.

---

## 10. Kritische Bewertung der Literatur

### 10.1 Funktion jeder Quelle in der eigenen Arbeit

Jede der zehn Quellen erfüllt eine klar definierte und nicht austauschbare Rolle.

Raturi et al. (2026) begründen die Forschungslücke und die Modellwahl. Ohne diese Quelle gibt es keinen wissenschaftlichen Ausgangspunkt.

Neto et al. (2023) liefern die Datenbeschreibung und dienen als Referenzdokumentation für die semantische Validierung. Ohne diese Quelle fehlt sowohl die wissenschaftliche Grundlage für den Methodenteil als auch der Vergleichsrahmen für Teilfrage 3.

Ogunseyi et al. (2026) rechtfertigen die Wahl von SHAP als XAI-Methode mit 129 empirisch analysierten Studien. Ohne diese Quelle ist die SHAP-Entscheidung eine unbelegte Präferenz.

Mohale und Obagbuwa (2025) zeigen konkret, wie eine globale und lokale SHAP-Analyse in einem IDS-Experiment umgesetzt wird. Diese Quelle ist die methodische Vorlage für die eigene XAI-Komponente.

Hermosilla et al. (2025) führen konkrete Metriken zur Bewertung der Erklärungsqualität ein. Ohne diese Quelle wäre die XAI-Qualitätsbewertung nicht systematisch fundiert.

Almahaqeri et al. (2026) arbeiten auf demselben Datensatz mit derselben Modellkategorie, wählen aber eine andere Strategie für das Klassenungleichgewicht. Diese Quelle ermöglicht einen direkten Vergleich der eigenen Entscheidung im Diskussionsteil.

Alharby (2025) evaluiert Gradient Boosting und PCA auf dem CICIoT2023-Datensatz und misst Laufzeiten. Diese Quelle liefert direkte Vergleichswerte für die eigene Ablation Study und belegt, dass PCA auf diesem Datensatz eine belegte Methode ist.

Kikissagbe und Adda (2024) verankern die Modellwahl im aktuellen Forschungsstand. Ohne diese Quelle fehlt die theoretische Einbettung der Entscheidung für baumbasierte Ensemble-Methoden.

Hamedani et al. (2025) liefern die theoretische Motivation des Forschungsthemas im breiteren IoT-Sicherheitskontext.

Hosseini et al. (2025) liefern die theoretische und empirische Grundlage für die Diskussion des Klassenungleichgewichts in Teilfrage 1.

### 10.2 Was die Literatur insgesamt nicht leistet und warum das wichtig ist

Keine der zehn Quellen kombiniert gleichzeitig alle drei folgenden Elemente:

1. Den CICIoT2023-Datensatz als primäre Datenbasis
2. Balanced Accuracy mit klassenspezifischer Per-Class-Analyse als Hauptbewertungsmetrik
3. SHAP-basierte Erklärbarkeitsanalyse pro Angriffsklasse mit semantischer Validierung

Diese Kombination ist der Kern des wissenschaftlichen Mehrwerts dieser Arbeit.

---

## 11. Abgrenzung

**Was diese Arbeit nicht tut:**

- Kein Pflicht-Modellvergleich. Es wird ein einziges Hauptmodell vollständig implementiert und analysiert. Ein zweites Modell ist eine optionale Erweiterung, die nur bei ausreichend verfügbarer Zeit hinzugefügt wird. Die wissenschaftliche Qualität der Arbeit hängt nicht von der Anzahl der implementierten Modelle ab.
- Keine Reproduktion von Raturi et al. (2026). Das Ausgangspaper dient als konzeptioneller Startpunkt, nicht als Nachbauziel.
- Kein Deep Learning. Long Short-Term Memory (LSTM), Convolutional Neural Networks (CNN), Autoencoder und Transformer werden nicht implementiert. Der Fokus liegt auf interpretierbaren baumbasierten Modellen, weil nur diese native SHAP-Werte (TreeExplainer) liefern.
- Keine Echtzeit-Implementierung. Das System wird als Analysewerkzeug entwickelt, nicht als produktionsbereites IDS.
- Keine Latenzmessungen. Inferenzzeit und Speicherbedarf für IoT-Deployment werden nicht gemessen. Dies ist eine anerkannte Limitation, die im Ausblick formuliert wird.
- Keine Adversarial-Robustness-Tests. Die Modelle werden nicht gegen gezielte Angriffe auf das ML-System getestet.
- Keine neuen Datensätze. Es wird ausschließlich der CICIoT2023-Datensatz verwendet.

---

## 12. Wissenschaftlicher Mehrwert

Diese Arbeit leistet drei klar abgrenzbare und überprüfbare Beiträge zur bestehenden Forschung:

**Beitrag 1: Erklärbare Angriffserkennung auf CICIoT2023.** Die Integration von SHAP in ein baumbasiertes IDS-Experiment auf dem CICIoT2023-Datensatz mit Balanced Accuracy als primärer Metrik und klassenspezifischer Per-Class-Analyse existiert in der Literatur bisher nicht. Dies ist eine direkt belegbare Forschungslücke.

**Beitrag 2: PCA-Einflussanalyse.** Die systematische Untersuchung, wie PCA-Dimensionsreduktion die Balanced Accuracy und die Stabilität der SHAP-Feature-Importance beeinflusst, fehlt in Raturi et al. (2026) vollständig. Die Ablation Study schließt diese Lücke empirisch.

**Beitrag 3: Semantische Erklärungsvalidierung.** Die Bewertung der SHAP-Ergebnisse im Licht der CIC-Dokumentation und etablierter IDS-Referenzwerke ist ein methodischer Ansatz, der in der IDS-Literatur selten systematisch durchgeführt wird. Er beantwortet die Frage, ob das Modell tatsächlich sicherheitsrelevante Signale lernt oder statistische Artefakte des Datensatzes.

---

## 13. Verifizierte Literaturquellen im BibTeX-Format

Zehn Quellen, alle durch direkten Seitenzugriff auf die Verlagsseiten verifiziert.

```bibtex
@article{raturi2026exploratory,
  author    = {Raturi, Aayush and Aryan, Raj and Pranav, Prashant},
  title     = {An Exploratory Study on Application of Machine Learning
               in Detecting Cyberattacks},
  journal   = {Security and Privacy},
  volume    = {9},
  pages     = {e70220},
  year      = {2026},
  doi       = {10.1002/spy2.70220},
  url       = {https://onlinelibrary.wiley.com/doi/10.1002/spy2.70220},
  publisher = {Wiley},
  note      = {Ausgangspaper der Arbeit. Konzeptioneller Startpunkt,
               kein Reproduktionsziel. Laesst drei methodische Luecken
               offen: fehlende Erklaerbarkeit, fehlende Fehlerfortpflanzungs-
               analyse, fehlende Latenzmessungen. Die eigene Arbeit
               adressiert Luecke 1 eigenstaendig durch SHAP-Integration.}
}

@article{neto2023ciciot2023,
  author    = {Neto, Euclides Carlos Pinto and Dadkhah, Sajjad
               and Ferreira, Raphael and Zohourian, Alireza
               and Lu, Rongxing and Ghorbani, Ali A.},
  title     = {{CICIoT2023}: A Real-Time Dataset and Benchmark for
               Large-Scale Attacks in {IoT} Environment},
  journal   = {Sensors},
  volume    = {23},
  number    = {13},
  pages     = {5941},
  year      = {2023},
  doi       = {10.3390/s23135941},
  url       = {https://www.mdpi.com/1424-8220/23/13/5941},
  publisher = {MDPI},
  note      = {Wissenschaftliche Grundlage der Datenbeschreibung und
               Referenzdokumentation fuer die semantische Validierung
               in Teilfrage 3. Beantwortet die Frage: Wie wurde der
               CICIoT2023-Datensatz aufgebaut, welche IoT-Geraete und
               Angriffstypen sind enthalten, und welche Netzwerksignaturen
               charakterisieren die jeweiligen Angriffe?}
}

@article{ogunseyi2026xai_review,
  author    = {Ogunseyi, Taiwo Blessing and Thiyagarajan, Gogulakrishan
               and He, Honggang and Bist, Vinay and Du, Zhengcong},
  title     = {Performance Analysis of Explainable Deep Learning-Based
               Intrusion Detection Systems for {IoT} Networks:
               A Systematic Review},
  journal   = {Sensors},
  volume    = {26},
  number    = {2},
  pages     = {363},
  year      = {2026},
  doi       = {10.3390/s26020363},
  url       = {https://www.mdpi.com/1424-8220/26/2/363},
  publisher = {MDPI},
  note      = {PRISMA-Review von 129 Studien (2018--2025). Belegt, dass
               SHAP in 98 Prozent der XAI-IDS-Studien eingesetzt wird
               ohne Genauigkeitseinbussen. Beantwortet die Frage: Ist
               die SHAP-Integration wissenschaftlich begruendet und
               verbreitet in der IDS-Literatur?}
}

@article{mohale2025xai,
  author    = {Mohale, Vincent Zibi and Obagbuwa, Ibidun Christiana},
  title     = {Evaluating Machine Learning-Based Intrusion Detection
               Systems with Explainable {AI}: Enhancing Transparency
               and Interpretability},
  journal   = {Frontiers in Computer Science},
  volume    = {7},
  pages     = {1520741},
  year      = {2025},
  doi       = {10.3389/fcomp.2025.1520741},
  url       = {https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2025.1520741/full},
  publisher = {Frontiers},
  note      = {Direkte methodische Vorlage fuer die SHAP-Integration.
               Zeigt konkret wie globale und lokale SHAP-Analysen in
               einem IDS-Klassifikationsexperiment umgesetzt werden.
               Beantwortet die Frage: Wie sieht eine wissenschaftlich
               fundierte XAI-Analyse in einem IDS-Experiment aus?}
}

@article{hermosilla2025xai_forensic,
  author    = {Hermosilla, Pamela and Berr{\'i}os, Sebasti{\'a}n
               and Allende-Cid, H{\'e}ctor},
  title     = {Explainable {AI} for Forensic Analysis: A Comparative Study
               of {SHAP} and {LIME} in Intrusion Detection Models},
  journal   = {Applied Sciences},
  volume    = {15},
  number    = {13},
  pages     = {7329},
  year      = {2025},
  doi       = {10.3390/app15137329},
  url       = {https://www.mdpi.com/2076-3417/15/13/7329},
  publisher = {MDPI},
  note      = {Vergleicht SHAP und LIME auf XGBoost und TabNet im Kontext
               der Intrusion Detection. Fuehrt konkrete Metriken zur
               Bewertung der Erklaerungsqualitaet ein: Fidelitaet,
               Konsistenz und Jaccard-Aehnlichkeit. Beantwortet die Frage:
               Wie laesst sich die Qualitaet von SHAP-Erklaerungen
               quantitativ und systematisch bewerten? Direkte Grundlage
               fuer die XAI-Qualitaetsbewertung und die semantische
               Validierung in Teilfrage 3.}
}

@article{almahaqeri2026gradient,
  author    = {Almahaqeri, Salah A. and Almourish, Mohammed Hashem
               and Nasser, Adel A. and Elsayed, Amani A. K.
               and Alhejoj, Ali N.},
  title     = {An Optimized Gradient Boosting Framework for {IoT}
               Intrusion Detection: A Comprehensive Evaluation on the
               {CICIoT2023} Dataset},
  journal   = {Scientific Reports},
  year      = {2026},
  doi       = {10.1038/s41598-026-47399-5},
  url       = {https://www.nature.com/articles/s41598-026-47399-5},
  publisher = {Nature Publishing Group},
  note      = {Gleicher Datensatz (CICIoT2023), gleiche Modellkategorie
               (Gradient Boosting), andere Strategie fuer Klassenungleich-
               gewicht (stratifiziertes Undersampling). Beantwortet die
               Frage: Wie unterscheidet sich die eigene hierarchische
               Klassifikation von alternativen Imbalance-Strategien auf
               demselben Datensatz?}
}

@article{hamedani2025iotsurvey,
  author    = {Hamedani, Peyman and others},
  title     = {Machine Learning-Based Security Solutions for {IoT} Networks:
               A Comprehensive Survey},
  journal   = {Sensors},
  volume    = {25},
  number    = {11},
  pages     = {3341},
  year      = {2025},
  doi       = {10.3390/s25113341},
  url       = {https://www.mdpi.com/1424-8220/25/11/3341},
  publisher = {MDPI},
  note      = {Survey ueber ML-basierte Sicherheitsloesungen fuer IoT
               (2020--2024). Beantwortet die Frage: Warum ist ML-basierte
               Angriffserkennung fuer IoT ein relevantes und aktives
               Forschungsfeld, und welche methodischen Luecken bestehen
               noch? Wird im Theorieteil zur Motivation des
               Forschungsthemas verwendet.}
}

@article{hosseini2025imbalance,
  author    = {Hosseini, Seyedeh Somayyeh and others},
  title     = {Addressing Class Imbalance in Intrusion Detection:
               A Comprehensive Evaluation of Machine Learning Approaches},
  journal   = {Electronics},
  volume    = {14},
  number    = {1},
  pages     = {69},
  year      = {2025},
  doi       = {10.3390/electronics14010069},
  url       = {https://www.mdpi.com/2079-9292/14/1/69},
  publisher = {MDPI},
  note      = {Evaluiert ML-Algorithmen unter verschiedenen Graden von
               Klassenungleichgewicht in IDS-Datensaetzen. Beantwortet
               die Frage: Welche messbaren Konsequenzen hat Klassen-
               ungleichgewicht auf die Modellleistung, und warum ist
               Accuracy allein als Metrik ungenuegend? Direkte Grundlage
               fuer Teilfrage 1 der eigenen Arbeit.}
}

@article{alharby2025ciciot,
  author    = {Alharby, Maher},
  title     = {Evaluating Machine Learning Approaches for Multiple Attack
               Classification with Improved Computational Efficiency
               in {IoT} Networks},
  journal   = {Scientific Reports},
  volume    = {15},
  pages     = {39914},
  year      = {2025},
  doi       = {10.1038/s41598-025-23711-7},
  url       = {https://www.nature.com/articles/s41598-025-23711-7},
  publisher = {Nature Publishing Group},
  note      = {Evaluiert Gradient Boosting und Decision Tree auf CICIoT2023
               mit PCA als Dimensionsreduktion und misst Trainings- sowie
               Vorhersagezeiten. Beantwortet die Frage: Wie wirkt sich PCA
               auf die Leistung baumbasierter Modelle auf dem CICIoT2023-
               Datensatz aus, und was sind realistische Vergleichswerte
               fuer die eigene Ablation Study?}
}

@article{kikissagbe2024review,
  author    = {Kikissagbe, Brunel Rolack and Adda, Meddi},
  title     = {Machine Learning-Based Intrusion Detection Methods in
               {IoT} Systems: A Comprehensive Review},
  journal   = {Electronics},
  volume    = {13},
  number    = {18},
  pages     = {3601},
  year      = {2024},
  doi       = {10.3390/electronics13183601},
  url       = {https://www.mdpi.com/2079-9292/13/18/3601},
  publisher = {MDPI},
  note      = {Systematischer Review ueber supervised, unsupervised und
               hybride ML-Ansaetze fuer IoT-IDS. Beantwortet die Frage:
               Welchen Platz nehmen baumbasierte Ensemble-Methoden im
               aktuellen Forschungsstand zu ML-basierten IDS fuer IoT
               ein, und wie wird die eigene Modellwahl theoretisch
               verankert?}
}
```

---

