# Vortrag: ML zur Erkennung von Cyberangriffen in IoT-Netzwerken
# Jordan Guimfack Jeuna, IT-Sicherheit, M.Sc. IVS
# Ziel: max. 4 Minuten

Mein Projekt befasst sich mit Machine Learning zur Erkennung von Cyberangriffen in IoT-Netzwerken. Konkret: ein erklaerbarer Gradient-Boosting-Klassifikator auf dem CICIoT2023-Datensatz.

**Warum dieses Thema?**

IoT-Geraete sind ueberall: in Haushalten, in Fabriken, in kritischer Infrastruktur. Sie sind oft schlecht gesichert und selten aktualisiert, und damit ein attraktives Angriffsziel. Klassische Intrusion Detection Systeme stoessen hier an ihre Grenzen, weil sie auf festen Signaturen basieren und neue Angriffe nicht erkennen.

Machine Learning bietet eine Alternative. Das Modell lernt statistische Muster im Netzwerkverkehr, ohne auf vordefinierte Signaturen angewiesen zu sein. Und auf dem CICIoT2023-Datensatz zeigt Raturi et al. aus 2026, dass Gradient Boosting dabei die hoechste Balanced Accuracy erreicht.

**Drei Probleme in der bestehenden Literatur:**

Erstens: Der CICIoT2023-Datensatz ist stark unausgewogen. DoS- und DDoS-Angriffe dominieren massiv. Einfache Accuracy ist als Metrik ungeeignet, weil ein Modell, das seltene Angriffsklassen ignoriert, trotzdem einen hohen Wert erreichen kann.

Zweitens: Die Modelle sind Black Boxes. Sicherheitsanalysten sehen das Klassifikationsergebnis, aber nicht den Grund. Das ist in sicherheitskritischen Systemen nicht akzeptabel.

Drittens: Raturi et al. verwenden PCA zur Dimensionsreduktion, ohne zu untersuchen, welchen Einfluss das auf Modellleistung und Erklaerbarkeit hat.

**Mein Ansatz:**

Ich behalte Gradient Boosting und fuege drei Elemente hinzu.

Erstens SHAP, also SHapley Additive Explanations, als post-hoc-Erklaerungskomponente. SHAP erklaert pro Klasse, welche Netzwerkmerkmale die Entscheidung getrieben haben.

Zweitens Balanced Accuracy als primaere Metrik. Sie bildet das arithmetische Mittel der klassenspezifischen Recall-Werte und ist damit fair gegenueber seltenen Klassen.

Drittens eine Ablation Study, die zwei Pipelines vergleicht: eine mit PCA auf 16 Komponenten, eine mit allen 46 Originalmerkmalen. Verglichen werden sowohl Modellleistung als auch die Qualitaet der SHAP-Erklaerungen.

**Aktueller Stand:**

Einleitung, Related Work, Datenbasis und Methodik sind im Paper ausgearbeitet und mit zehn verifizierten wissenschaftlichen Quellen belegt. Der theoretische Rahmen steht vollstaendig.

Die naechsten Schritte sind: Implementierung der Vorverarbeitungspipeline, Training des Klassifikators, SHAP-Analyse und Auswertung der Ergebnisse. Geplante Abgabe ist der 15. Juni 2026.

**Zum Abschluss:**

Das Besondere an diesem Projekt ist nicht nur die Erkennungsleistung, sondern die Erklaerbarkeit. Ein IDS, dessen Entscheidungen Sicherheitsanalysten nachvollziehen koennen, ist vertrauenswuerdiger und im Einsatz besser steuerbar. Das ist der eigentliche Beitrag dieser Arbeit.
