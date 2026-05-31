# Vortrag: Umsetzungsplan
# Jordan Guimfack Jeuna, IT-Sicherheit, M.Sc. IVS
# Ziel: 4 bis 5 Minuten

Ich moechte jetzt den Umsetzungsplan vorstellen und dabei alle zentralen technischen Entscheidungen begruenden. Der Plan ist kein bloss technisches Dokument. Jedes Arbeitspaket ergibt sich aus einer konkreten wissenschaftlichen Entscheidung.

**Was bereits fertig ist**

Die theoretische Phase ist abgeschlossen. Einleitung, Related Work, Datenbasis und Methodik sind im Paper ausgearbeitet. Zehn verifizierte wissenschaftliche Quellen sind in die Bibliographie aufgenommen. Damit steht das Fundament.

**Erste Entscheidung: Warum Gradient Boosting?**

Wir verwenden Gradient Boosting als Hauptmodell. Die Wahl ist nicht willkuerlich. Raturi et al. aus 2026 evaluieren auf dem CICIoT2023-Datensatz mehrere ML-Algorithmen und zeigen empirisch, dass Gradient Boosting in der Mehrklassenklassifikation die hoechste Balanced Accuracy erzielt. Das ist die staerkste Rechtfertigung fuer eine Modellwahl, die es gibt: ein peer-reviewtes Ergebnis auf dem exakt gleichen Datensatz.

Dazu kommt ein zweiter Grund: Gradient Boosting ist nativ kompatibel mit dem SHAP TreeExplainer. Der TreeExplainer berechnet SHAP-Werte exakt und effizient fuer baumbasierte Modelle, ohne Approximationen. Das ist wichtig, weil die SHAP-Analyse ein zentraler Beitrag dieser Arbeit ist.

**Zweite Entscheidung: Warum eine zweistufige Klassifikationsarchitektur?**

Der CICIoT2023-Datensatz hat ein extremes Klassenungleichgewicht. DoS- und DDoS-Angriffe dominieren den Datensatz massiv. Wenn wir direkt eine Mehrklassenklassifikation durchfuehren, werden die selteneren Klassen wie Brute-Force oder Web-based Attacks systematisch verdraengt. Das Modell lernt, die Mehrheitsklasse zu bevorzugen, weil das rechnerisch besser ist.

Die Loesung von Raturi et al. ist eine zweistufige Hierarchie. In Stufe 1 wird binaer zwischen DoS/DDoS-Verkehr und allem anderen unterschieden. In Stufe 2 klassifiziert ein separates Modell nur noch die Nicht-DoS-Instanzen. So wird das Ungleichgewicht strukturell behandelt, nicht nur statistisch ausgeglichen.

**Dritte Entscheidung: Warum Balanced Accuracy als primaere Metrik?**

Einfache Accuracy ist bei unausgewogenen Datensaetzen irreführend. Hosseini et al. aus 2025 belegen das empirisch: Ein Modell, das alle seltenen Angriffsklassen ignoriert und nur die Mehrheitsklasse korrekt klassifiziert, kann eine Accuracy von ueber 90 Prozent erzielen und waere im praktischen Einsatz dennoch weitgehend wirkungslos.

Die Balanced Accuracy berechnet das arithmetische Mittel der klassenspezifischen Recall-Werte. Jede Klasse zaehlt gleich, unabhaengig davon, wie viele Instanzen sie enthaelt. Das ist die faire Metrik fuer diesen Datensatz.

**Vierte und zentrale Entscheidung: Warum zwei Vorverarbeitungspipelines?**

Das ist die Kernfrage des Umsetzungsplans, und ich moechte sie sorgfaeltig begruenden.

Raturi et al. aus 2026 verwenden PCA zur Dimensionsreduktion. Sie reduzieren die 46 Netzwerkmerkmale auf 16 Hauptkomponenten, bevor sie das Modell trainieren. Alharby aus 2025 macht dasselbe auf dem gleichen Datensatz. Beide berichten verbesserte Trainingszeiten.

Das Problem ist: Niemand hat untersucht, was PCA mit den SHAP-Erklaerungen macht.

PCA-Komponenten sind lineare Kombinationen aller 46 Originalmerkmale. Hauptkomponente 1 bedeutet nichts fuer einen Sicherheitsanalysten. Er weiss nicht, was dahinter steckt. Wenn wir SHAP auf PCA-transformierten Daten anwenden, erhalten wir die Wichtigkeit von Hauptkomponente 1, Hauptkomponente 2 und so weiter. Das ist mathematisch korrekt, aber semantisch bedeutungslos.

Pipeline A repliziert den Ansatz von Raturi et al.: 46 Merkmale, PCA auf 16 Hauptkomponenten, dann Training und SHAP. Das ist die Vergleichsbedingung.

Pipeline B verwendet alle 46 Originalmerkmale ohne PCA. SHAP arbeitet direkt auf den echten Netzwerkmerkmalen wie Rate, syn_flag_number oder Number. Der Sicherheitsanalyst sieht: "Dieses Paket wurde als DDoS klassifiziert, weil die Paketrate extrem hoch war und die SYN-Flag-Anzahl anomal ist." Das ist eine verwertbare Erklaerung.

Der Vergleich beider Pipelines quantifiziert genau das: Wie stark veraendert PCA die Modellleistung? Und wie stark beeintraechtigt PCA die semantische Interpretierbarkeit der SHAP-Erklaerungen? Das ist die Ablation Study, und das ist der eigenstaendige wissenschaftliche Beitrag dieser Arbeit gegenueber Raturi et al.

**Fuenfte Entscheidung: Warum SHAP?**

Ogunseyi et al. aus 2026 analysieren 129 XAI-IDS-Studien und stellen fest, dass SHAP in der grossen Mehrheit der Studien eingesetzt wird, ohne die Erkennungsgenauigkeit zu beeintraechtigen. Mohale und Obagbuwa aus 2025 liefern die konkrete methodische Vorlage fuer globale und lokale SHAP-Analysen in IDS-Experimenten. Hermosilla et al. aus 2025 stellen Metriken bereit, um die Qualitaet der SHAP-Erklaerungen zu messen: Fidelitaet, Konsistenz und Jaccard-Aehnlichkeit. Alle drei Entscheidungen sind literaturgeprueft.

**Der Zeitplan**

Phase 2 ist abgeschlossen. Der naechste Schritt beginnt ab heute.

Vom 18. bis 25. Mai: Vorbereitung der Datenbasis und Implementierung der Vorverarbeitungspipeline. Vom 25. Mai bis 1. Juni: Implementierung des Klassifikators und Hyperparameteroptimierung.

Am 1. Juni findet das Motivationsreview statt. Zu diesem Termin muessen erste Implementierungsergebnisse vorzeigbar sein.

Vom 1. bis 8. Juni: Experimentdurchfuehrung beider Pipelines und SHAP-Analyse. Am 8. Juni ist Ergebnisfeststellung. Vom 8. bis 15. Juni: Datenauswertung, Visualisierungen, Ausarbeitung Methodik und Ergebnisse. Am 15. Juni ist das Kernkapitel abzugeben.

Vom 15. bis 22. Juni: Diskussion, Einleitung, Fazit, Abstract und Schlusskorrektur. Am 22. Juni wird die Reviewversion eingereicht. Vom 22. bis 29. Juni: Peer-Reviews lesen und die eigene Arbeit ueberarbeiten. Am 29. Juni werden die Reviews vorgestellt.

Vom 29. Juni bis 13. Juli: Vortragsvorbereitung und finale Korrekturen. Am 13. Juli halte ich den Vortrag als Pruefungsleistung. Anschliessend folgt die Camera-Ready-Ueberarbeitung. Die endgueltige Abgabe ist der 27. Juli 2026.

**Abschluss**

Jede Entscheidung in diesem Plan ist durch Literatur begruendet. Die zwei Pipelines sind kein Zufall, sie sind der Kern des wissenschaftlichen Beitrags. Ohne diesen Vergleich gibt es keine Ablation Study, und ohne die Ablation Study gibt es keinen Beitrag ueber Raturi et al. hinaus.
