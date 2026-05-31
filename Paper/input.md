# Wissenschaftlicher Inhalt für das LaTeX-Dokument

**Autor:** Jordan Guimfack Jeuna
**Modul:** IT-Sicherheit
**Studiengang:** Master Informatik – Vertrauenswürdige Systeme (IVS)

---

## 1. Titel

**Machine Learning zur Erkennung von Cyberangriffen in IoT-Netzwerken: Entwicklung und Evaluation eines erklärbaren Gradient-Boosting-Klassifikators mit SHAP-Analyse auf dem CICIoT2023-Datensatz**

---

## 2. Einleitung

Die fortschreitende Vernetzung alltäglicher Gegenstände im Rahmen des Internet of Things (IoT) hat zu einer tiefgreifenden Transformation moderner Infrastrukturen geführt. Gleichzeitig hat diese Entwicklung eine erheblich vergrößerte und strukturell schwach gesicherte Angriffsfläche geschaffen, die Sicherheitsverantwortliche vor neue Herausforderungen stellt. IoT-Geräte wie Smart-TVs, IP-Kameras, Thermostate und Bewegungsmelder verfügen in der Regel über begrenzte Rechenressourcen, unzureichende Authentifizierungsmechanismen und selten aktualisierte Firmware. Diese strukturellen Schwächen machen sie zu attraktiven Zielen für Angriffe wie Distributed Denial of Service (DDoS), Mirai-Botnetze, Spoofing und Brute-Force-Kampagnen.

Klassische Intrusion Detection Systeme (IDS), die auf dem Abgleich von Netzwerkpaketen mit bekannten Angriffssignaturen basieren, sind gegenüber neuartigen und sich verändernden Angriffsmethoden grundsätzlich unzureichend. Sie können sogenannte Zero-Day-Angriffe nicht erkennen und besitzen keine Fähigkeit zur adaptiven Anpassung an neue Bedrohungsszenarien. Maschinelles Lernen (ML) bietet in diesem Kontext eine datengetriebene Alternative: Durch das Erlernen statistischer Muster im Netzwerkverkehr können ML-Modelle Anomalien identifizieren, ohne auf vordefinierten Signaturen angewiesen zu sein.

Eine wegweisende Arbeit in diesem Forschungsfeld ist die Studie von Raturi, Aryan und Pranav (2026), die verschiedene ML-Algorithmen auf dem CICIoT2023-Datensatz des Canadian Institute for Cybersecurity evaluiert. Die Autoren zeigen, dass baumbasierte Modelle und Ensemble-Methoden wie Gradient Boosting die höchsten Erkennungsleistungen erzielen. Gleichzeitig identifizieren sie eine wesentliche methodische Lücke: Die untersuchten Modelle werden als nicht transparente Black Boxes evaluiert. Sicherheitsanalysten erhalten keinerlei Einblick in die Entscheidungsgrundlagen des Klassifikators und können damit weder die Zuverlässigkeit einzelner Klassifikationsentscheidungen beurteilen noch sicherheitsrelevante Muster extrahieren.

Die vorliegende Arbeit setzt an dieser Forschungslücke an. Sie verbindet die ML-basierte Angriffserkennung auf dem CICIoT2023-Datensatz mit einer integrierten Erklärbarkeitskomponente auf Basis von SHAP (SHapley Additive Explanations) und leistet damit einen eigenständigen wissenschaftlichen Beitrag, der über das Ausgangspaper hinausgeht.

---

## 3. Problemstellung

Die IoT-Sicherheitsforschung steht vor zwei sich gegenseitig verstärkenden Herausforderungen, die in ihrer Kombination bislang unzureichend adressiert wurden.

Die erste Herausforderung betrifft die Leistungsbewertung von ML-Modellen unter realistischen Datenbedingungen. Der CICIoT2023-Datensatz, der als Benchmark für diese Arbeit dient, weist ein starkes Klassenungleichgewicht auf: DoS- und DDoS-Angriffe dominieren das Datenmaterial erheblich, während Klassen wie Brute-Force oder Web-based Attacks stark unterrepräsentiert sind. Dieses Ungleichgewicht führt dazu, dass die klassische Accuracy als Bewertungsmetrik ein verfälschtes Bild der Modellleistung liefert. Ein Modell, das sämtliche seltenen Angriffsklassen ignoriert und ausschließlich die Mehrheitsklasse korrekt klassifiziert, kann rechnerisch eine Accuracy von über 90 Prozent erzielen und wäre im praktischen Einsatz dennoch weitgehend wirkungslos. Raturi et al. (2026) schlagen die Balanced Accuracy als fairere Bewertungsgrundlage vor, ohne jedoch deren Einfluss auf die Ergebnisinterpretation systematisch zu untersuchen.

Die zweite Herausforderung betrifft die Interpretierbarkeit der Modellentscheidungen. In sicherheitskritischen Anwendungen ist es nicht ausreichend, dass ein Modell korrekte Klassifikationen produziert. Sicherheitsanalysten müssen verstehen können, auf welcher Grundlage ein Netzwerkpaket als Angriff eingestuft wurde, um Fehlalarme zu beurteilen, Angriffsmuster zu verstehen und das Vertrauen in das System aufzubauen. Die bestehende Literatur zu ML-basierten IDS auf dem CICIoT2023-Datensatz, einschließlich der Arbeit von Raturi et al. (2026) und Almahaqeri et al. (2026), behandelt Modelle durchgängig als Black Boxes und verzichtet auf jede Form der Erklärbarkeitsanalyse.

Hinzu kommt eine dritte, methodische Lücke: Der Einfluss der PCA-basierten Dimensionsreduktion, die von Raturi et al. (2026) ohne weitere Analyse eingesetzt wird, ist für den CICIoT2023-Datensatz empirisch nicht untersucht. Es ist ungeklärt, ob die Reduktion von 46 auf 16 Hauptkomponenten die Klassifikationsleistung und insbesondere die SHAP-Erklärungen verändert.

Diese drei Problemdimensionen bilden den Ausgangspunkt der vorliegenden Arbeit.

---

## 4. Zielsetzung

Das übergeordnete Ziel dieser Arbeit ist die Entwicklung und Evaluation eines erklärbaren ML-basierten Intrusion Detection Systems für IoT-Netzwerke, das auf dem CICIoT2023-Datensatz trainiert und bewertet wird. Das System soll zwei Eigenschaften vereinen, die in der bestehenden Literatur bislang nicht gemeinsam auf diesem Datensatz untersucht wurden: eine hohe Erkennungsleistung gemessen an der Balanced Accuracy sowie interpretierbare Entscheidungsgrundlagen durch SHAP.

Daraus ergeben sich drei konkrete wissenschaftliche Beiträge:

Der erste Beitrag besteht in der erstmaligen Integration von SHAP in ein baumbasiertes Klassifikationsexperiment auf dem CICIoT2023-Datensatz, evaluiert anhand der Balanced Accuracy als primärer Bewertungsmetrik. Diese Kombination existiert in der Literatur bisher nicht und stellt eine direkt belegbare Forschungslücke dar.

Der zweite Beitrag besteht in einer quantitativen Ablation Study, die den Einfluss der PCA-Dimensionsreduktion auf Modellleistung und SHAP-Feature-Importance systematisch untersucht. Diese Analyse fehlt im Ausgangspaper vollständig.

Der dritte Beitrag besteht in einer semantischen Validierung der SHAP-Erklärungen. Die identifizierten Feature-Importance-Ranglisten werden mit dem fachlichen Wissen über die Netzwerksignaturen der jeweiligen Angriffstypen verglichen, um zu prüfen, ob das Modell tatsächlich sicherheitsrelevante Merkmale lernt oder statistische Artefakte des Datensatzes.

Die drei Forschungsfragen, die diese Ziele operationalisieren, lauten wie folgt:

Kann ein Gradient-Boosting-Klassifikator auf dem CICIoT2023-Datensatz eine hohe Balanced Accuracy bei der Erkennung von Cyberangriffen erzielen, und lassen sich seine Entscheidungen durch SHAP so erklären, dass die relevanten Netzwerkmerkmale pro Angriffsklasse für Sicherheitsanalysten nachvollziehbar werden?

Inwiefern verändert sich die Modellbewertung, wenn statt der einfachen Accuracy die Balanced Accuracy als primäre Metrik eingesetzt wird, und welche Angriffsklassen werden durch das Klassenungleichgewicht systematisch schlechter erkannt?

Welchen messbaren Einfluss hat die PCA-basierte Dimensionsreduktion auf die Balanced Accuracy und die SHAP-Erklärungen, und welche Netzwerkmerkmale sind gemäß SHAP für die Klassifikation der einzelnen Angriffstypen entscheidend?

---

## 5. Methodische Vorgehensweise

Die methodische Vorgehensweise gliedert sich in vier aufeinander aufbauende Phasen.

**Phase 1: Datenvorbereitung**

Als Datenbasis dient der CICIoT2023-Datensatz des Canadian Institute for Cybersecurity (Neto et al., 2023). Der Datensatz enthält realen Netzwerkverkehr von 105 IoT-Geräten unter 33 verschiedenen Angriffsbedingungen, die auf 8 übergeordnete Kategorien reduziert werden: DoS, DDoS, Mirai, Reconnaissance, Spoofing, Brute-Force, Web-based Attacks sowie gutartiger Verkehr (Benign). Die 46 vorextrahierten Netzwerkmerkmale werden mittels StandardScaler normalisiert. Es werden zwei parallele Preprocessing-Pipelines aufgebaut: Pipeline A reduziert die Merkmalsdimension mittels PCA von 46 auf 16 Hauptkomponenten, Pipeline B verwendet alle 46 Merkmale als Kontrollbedingung für die Ablation Study.

**Phase 2: Klassifikation**

Als Klassifikationsarchitektur wird der zweistufige hierarchische Ansatz aus Raturi et al. (2026) übernommen, da er das Klassenungleichgewichtsproblem strukturell adressiert. In Stufe 1 wird zwischen DoS/DDoS-Verkehr und Nicht-DoS-Verkehr unterschieden (binäre Klassifikation). In Stufe 2 werden die Nicht-DoS-Instanzen in die verbleibenden Kategorien eingeordnet (Mehrklassenklassifikation). Dieser Rahmen wird nicht reproduziert, sondern um eine vollständige SHAP-Analyse auf beiden Klassifikationsstufen erweitert.

Als Hauptmodell wird Gradient Boosting implementiert, da es in Raturi et al. (2026) die höchste Balanced Accuracy in der Mehrklassenklassifikation erzielt (0,952) und vollständig SHAP-kompatibel über den TreeExplainer ist. Falls die verfügbare Zeit es erlaubt, kann ein Decision Tree als optionaler Vergleichspunkt hinzugefügt werden.

**Phase 3: Evaluation**

Die primäre Bewertungsmetrik ist die Balanced Accuracy, definiert als arithmetisches Mittel aus Sensitivität und Spezifität über alle Klassen. Sie ist robust gegenüber Klassenungleichgewicht und macht sichtbar, wenn ein Modell seltene Angriffsklassen systematisch ignoriert. Als sekundäre Metriken werden F1-Score (makro-gemittelt), Precision und Recall pro Klasse sowie Konfusionsmatrizen erhoben. Eine Ablation Study vergleicht die Modellleistung mit und ohne PCA-Reduktion sowie unter Standard- und optimierten Hyperparametern (Grid Search).

**Phase 4: SHAP-Analyse**

SHAP wird auf zwei Ebenen eingesetzt. Auf globaler Ebene werden Feature-Importance-Ranglisten pro Angriffsklasse erzeugt, die zeigen, welche der 46 Netzwerkmerkmale die Klassifikation von DDoS, Mirai oder Brute-Force am stärksten treiben. Auf lokaler Ebene werden Einzelfallanalysen ausgewählter Fehlklassifikationen durchgeführt. Die SHAP-Ergebnisse werden abschließend semantisch validiert, indem sie mit dem Fachwissen über die Netzwerksignaturen der jeweiligen Angriffstypen verglichen werden.

---

## 6. Abgrenzung des Themas

Die vorliegende Arbeit konzentriert sich bewusst auf einen klar definierten Forschungsbereich und grenzt sich von benachbarten Themenfeldern wie folgt ab.

Es wird kein verpflichtender Modellvergleich durchgeführt. Ein einziges Hauptmodell wird vollständig implementiert, evaluiert und durch SHAP analysiert. Ein zweites Modell ist ausschließlich als optionale Erweiterung vorgesehen, falls die verfügbare Zeit und der Projektumfang es erlauben. Die wissenschaftliche Qualität der Arbeit ist nicht von der Anzahl implementierter Modelle abhängig.

Die Arbeit stellt keine Reproduktion des Ausgangspapers von Raturi et al. (2026) dar. Das Ausgangspaper dient als konzeptioneller Ausgangspunkt und Referenz für die Identifikation der Forschungslücke, nicht als Vorlage zum Nachbauen.

Es werden keine Deep-Learning-Architekturen implementiert. LSTM-Netzwerke, Convolutional Neural Networks, Autoencoder und Transformer-Modelle werden nicht berücksichtigt. Der Fokus liegt auf interpretierbaren baumbasierten Modellen, weil ausschließlich diese native SHAP-Werte über den TreeExplainer ohne Approximationen liefern.

Es wird keine Echtzeit-Implementierung entwickelt. Das System wird als wissenschaftliches Analysewerkzeug konzipiert, nicht als produktionsbereites IDS für den operativen Einsatz.

Es werden keine Latenzmessungen durchgeführt. Inferenzzeit, CPU-Last und Speicherbedarf für den Einsatz auf ressourcenbeschränkten IoT-Geräten werden nicht gemessen. Diese Limitation wird im Ausblick der Arbeit explizit benannt.

Es werden keine Adversarial Robustness Tests durchgeführt. Die Robustheit der Modelle gegenüber gezielten Angriffen auf das ML-System selbst ist nicht Gegenstand dieser Arbeit.

Es werden ausschließlich die Daten des CICIoT2023-Datensatzes verwendet. Keine eigene Datenerhebung und kein Einsatz weiterer Datensätze sind vorgesehen.

---

## 7. Erwartete Ergebnisse

Auf Grundlage der analysierten Literatur und der gewählten Methodik werden folgende Ergebnisse erwartet:

Das Gradient-Boosting-Modell wird auf dem CICIoT2023-Datensatz eine hohe Balanced Accuracy erzielen, die im Bereich der von Raturi et al. (2026) berichteten Werte von 0,95 liegt, unter der Maßgabe, dass ähnliche Vorverarbeitungsschritte angewendet werden.

Der Vergleich von Accuracy und Balanced Accuracy wird zeigen, dass einfache Accuracy bei diesem stark unausgewogenen Datensatz ein systematisch verzerrtes Bild der Modellleistung liefert. Es wird erwartet, dass bestimmte Angriffsklassen trotz hoher Gesamt-Accuracy eine deutlich geringere klassenspezifische Erkennungsrate aufweisen.

Die Ablation Study wird belegen, dass die PCA-Reduktion von 46 auf 16 Merkmale einen messbaren Einfluss auf die Feature-Importance-Ranglisten der SHAP-Analyse hat, da die Hauptkomponenten lineare Kombinationen der Originalmerkmale darstellen und die semantische Interpretierbarkeit der Erklärungen einschränken.

Die SHAP-Analyse wird zeigen, dass das Gradient-Boosting-Modell tatsächlich sicherheitsrelevante Netzwerkmerkmale lernt, deren Bedeutung mit dem Fachwissen über die jeweiligen Angriffstypen übereinstimmt. Für DoS-Angriffe werden beispielsweise Merkmale wie Paketrate und Verbindungsfrequenz erwartet, für Spoofing-Angriffe hingegen Merkmale im Zusammenhang mit Protokollfeldern und Quell-Adressen.

---

## 8. Vorläufige Gliederung

**1 Einleitung**
1.1 Motivation und Relevanz
1.2 Problemstellung
1.3 Zielsetzung und Forschungsfragen
1.4 Struktur der Arbeit

**2 Theoretische Grundlagen**
2.1 IoT-Sicherheit: Architektur, Schwachstellen und Bedrohungslandschaft
2.2 Klassische versus ML-basierte Intrusion Detection Systeme
2.3 Maschinelles Lernen für IoT-IDS: Supervised Learning und Ensemble-Methoden
2.4 Klassenungleichgewicht in ML-Anwendungen: Ursachen, Auswirkungen und Gegenmaßnahmen
2.5 Dimensionsreduktion mit PCA: Grundlagen und Einsatz in IDS
2.6 Erklärbare Künstliche Intelligenz (XAI): SHAP als post-hoc-Erklärungsverfahren

**3 Verwandte Arbeiten**
3.1 ML-basierte Angriffserkennung auf dem CICIoT2023-Datensatz
3.2 XAI-Ansätze in Intrusion Detection Systemen
3.3 Behandlung von Klassenungleichgewicht in IDS-Studien
3.4 Abgrenzung der eigenen Arbeit vom Stand der Forschung

**4 Datensatz und Vorverarbeitung**
4.1 Beschreibung des CICIoT2023-Datensatzes
4.2 Angriffsklassen und Klassenstruktur
4.3 Klassenungleichgewicht: Analyse und Auswirkungen
4.4 Vorverarbeitungspipeline: Normalisierung und Klassenkondensierung
4.5 PCA-Dimensionsreduktion: Vorgehen und Parameterwahl

**5 Methodik**
5.1 Zweistufiger hierarchischer Klassifikationsansatz
5.2 Gradient-Boosting-Modell: Architektur und Hyperparameteroptimierung
5.3 Evaluationsmetriken: Balanced Accuracy, F1-Score, Konfusionsmatrix
5.4 Ablation Study: PCA versus vollständiger Merkmalsraum
5.5 SHAP-Integration: globale und lokale Erklärungsebene

**6 Experimentelle Evaluation**
6.1 Experimentelles Setup und Reproduzierbarkeit
6.2 Ergebnisse der binären Klassifikation (Stufe 1)
6.3 Ergebnisse der Mehrklassenklassifikation (Stufe 2)
6.4 Ergebnisse der Ablation Study
6.5 SHAP-Analyse: Feature-Importance pro Angriffsklasse
6.6 Semantische Validierung der SHAP-Erklärungen

**7 Diskussion**
7.1 Interpretation der Ergebnisse im Licht der Forschungsfragen
7.2 Vergleich mit Raturi et al. (2026) und Almahaqeri et al. (2026)
7.3 Bedeutung der Balanced Accuracy für die IDS-Bewertung
7.4 Grenzen der Arbeit

**8 Fazit und Ausblick**
8.1 Zusammenfassung der Beiträge
8.2 Beantwortung der Forschungsfragen
8.3 Offene Fragen und zukünftige Forschungsrichtungen

**Literaturverzeichnis**

---

## 9. Relevante wissenschaftliche Quellen

Almahaqeri, S. A., Almourish, M. H., Nasser, A. A., Elsayed, A. A. K. & Alhejoj, A. N. (2026). An Optimized Gradient Boosting Framework for IoT Intrusion Detection: A Comprehensive Evaluation on the CICIoT2023 Dataset. Scientific Reports. https://doi.org/10.1038/s41598-026-47399-5

Alharby, M. (2025). Evaluating Machine Learning Approaches for Multiple Attack Classification with Improved Computational Efficiency in IoT Networks. Scientific Reports, 15, 39914. https://doi.org/10.1038/s41598-025-23711-7

Hamedani, P. et al. (2025). Machine Learning-Based Security Solutions for IoT Networks: A Comprehensive Survey. Sensors, 25(11), 3341. https://doi.org/10.3390/s25113341

Hosseini, S. S. et al. (2025). Addressing Class Imbalance in Intrusion Detection: A Comprehensive Evaluation of Machine Learning Approaches. Electronics, 14(1), 69. https://doi.org/10.3390/electronics14010069

Kikissagbe, B. R. & Adda, M. (2024). Machine Learning-Based Intrusion Detection Methods in IoT Systems: A Comprehensive Review. Electronics, 13(18), 3601. https://doi.org/10.3390/electronics13183601

Mohale, V. Z. & Obagbuwa, I. C. (2025). Evaluating Machine Learning-Based Intrusion Detection Systems with Explainable AI: Enhancing Transparency and Interpretability. Frontiers in Computer Science, 7, 1520741. https://doi.org/10.3389/fcomp.2025.1520741

Neto, E. C. P., Dadkhah, S., Ferreira, R., Zohourian, A., Lu, R. & Ghorbani, A. A. (2023). CICIoT2023: A Real-Time Dataset and Benchmark for Large-Scale Attacks in IoT Environment. Sensors, 23(13), 5941. https://doi.org/10.3390/s23135941

Ogunseyi, T. B., Thiyagarajan, G., He, H., Bist, V. & Du, Z. (2026). Performance Analysis of Explainable Deep Learning-Based Intrusion Detection Systems for IoT Networks: A Systematic Review. Sensors, 26(2), 363. https://doi.org/10.3390/s26020363

Raturi, A., Aryan, R. & Pranav, P. (2026). An Exploratory Study on Application of Machine Learning in Detecting Cyberattacks. Security and Privacy, 9, e70220. https://doi.org/10.1002/spy2.70220

---

## 10. Schlüsselbegriffe

Internet of Things (IoT), Intrusion Detection System (IDS), Machine Learning, Gradient Boosting, CICIoT2023, Balanced Accuracy, Klassenungleichgewicht, Explainable Artificial Intelligence (XAI), SHAP (SHapley Additive Explanations), Principal Component Analysis (PCA), Cyberangriffserkennung, Feature Importance, Netzwerksicherheit, Vertrauenswürdige Systeme, Anomalieerkennung

---

## 11. BibTeX-Einträge

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
               kein Reproduktionsziel. Benennt drei methodische Luecken:
               fehlende Erklaerbarkeit, fehlende Fehlerfortpflanzungsanalyse,
               fehlende Latenzmessungen. Die eigene Arbeit adressiert
               Luecke 1 eigenstaendig durch SHAP-Integration.}
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
  note      = {Wissenschaftliche Grundlage der Datenbeschreibung.
               Beantwortet die Frage: Wie wurde der CICIoT2023-Datensatz
               aufgebaut, welche IoT-Geraete und Angriffstypen sind
               enthalten, und warum ist er ein valider Benchmark?}
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
```