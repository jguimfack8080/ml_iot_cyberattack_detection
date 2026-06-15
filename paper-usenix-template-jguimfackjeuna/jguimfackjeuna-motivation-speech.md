# Vortrag: Motivation und Zielsetzung

*Sprechdauer etwa 4 Minuten. In natürlicher, gesprochener Sprache.*

---

Liebe Kommilitoninnen und Kommilitonen, sehr geehrter Herr Professor Fischer,

ich möchte euch heute die Motivation hinter meiner Seminararbeit vorstellen. Es geht um die Erkennung von Cyberangriffen in IoT-Netzwerken mit maschinellem Lernen, und vor allem darum, diese Erkennung nachvollziehbar zu machen.

Fangen wir mit dem Problem an. IoT-Geräte sind heute überall: in Wohnungen, in Fabriken, in kritischer Infrastruktur. Der Datensatz, mit dem ich arbeite, der CICIoT2023, zeigt das sehr konkret. Er erfasst 33 reale Angriffe gegen ein Testnetz aus 105 echten Geräten. Das macht deutlich, wie groß die Angriffsfläche inzwischen geworden ist.

Klassische Intrusion Detection Systeme arbeiten mit Signaturen. Sie erkennen also nur das, was sie schon kennen. Sobald ein Angriff neu ist oder leicht abgewandelt wird, versagt dieser Ansatz. Genau hier setzt maschinelles Lernen an. Statt feste Muster zu hinterlegen, lernt das Modell das Angriffsverhalten direkt aus den Netzwerkmerkmalen. Baumbasierte Verfahren gelten dabei als der etablierte Stand der Forschung, und Gradient Boosting erreicht auf diesem Datensatz die beste Balanced Accuracy unter den verglichenen Modellen.

Jetzt kommt aber der Punkt, der mich eigentlich interessiert. Eine hohe Erkennungsrate allein reicht für den praktischen Einsatz nicht aus. Die vorhandenen Arbeiten behandeln ihr Modell wie eine Black Box. Sie sagen also: das ist ein Angriff. Aber sie sagen nicht, warum. Und für einen Sicherheitsanalysten, der einen Alarm prüft, ist genau das entscheidend. Er muss verstehen können, welches Merkmal die Entscheidung getragen hat, bevor er reagiert.

Daraus ergeben sich drei konkrete Lücken, die ich angehe.

Erstens das Klassenungleichgewicht. Der Datensatz wird von DoS und DDoS Verkehr dominiert. Das heißt, ein Modell kann die seltenen Angriffsklassen komplett übersehen und trotzdem eine hohe Accuracy ausweisen, weil die häufigen Klassen das Ergebnis bestimmen. Deshalb nutze ich nicht die einfache Accuracy, sondern die Balanced Accuracy als Hauptmetrik.

Zweitens die fehlende Interpretierbarkeit. Ohne Einblick in die Entscheidung bleibt unklar, ob das Modell ein echtes Angriffsmerkmal nutzt oder nur einem Zufall im Datensatz folgt. Diese Begründung pro Angriffsklasse liefert bisher keine der Arbeiten.

Und drittens die Dimensionsreduktion. Die Ausgangsstudie reduziert die 46 Merkmale per PCA auf 16 Komponenten, prüft aber nie, wie sich das auf die Erklärbarkeit auswirkt. Und da PCA Komponenten nur Linearkombinationen sind, ist zu erwarten, dass die fachliche Deutbarkeit darunter leidet.

Mein Ziel ist deshalb ein Gradient Boosting Klassifikator, der zwei Dinge gleichzeitig leistet. Zum einen eine hohe Erkennungsleistung, gemessen an der Balanced Accuracy. Zum anderen eine Entscheidung, die pro Angriffsklasse nachvollziehbar ist, und zwar über SHAP.

Mein eigener Beitrag liegt in der Kombination. Ich verbinde SHAP, die Balanced Accuracy und eine messbare Prüfung der Erklärungen auf diesem Datensatz, was in dieser Form so noch nicht gemacht wurde. Dabei nehme ich die Qualität der Erklärungen nicht einfach an, sondern überprüfe sie mit Maßen wie Fidelität, Konsistenz und Jaccard Ähnlichkeit, und vergleiche sie mit den bekannten Signaturen der jeweiligen Angriffstypen. Zusätzlich vergleiche ich in einer Ablation Study die PCA Variante mit allen 46 Originalmerkmalen, um den Preis der Reduktion sichtbar zu machen.

Kurz gesagt: Ich will ein Modell, das nicht nur gut erkennt, sondern auch erklärt, warum. Und genau diese Verbindung aus Leistung und Erklärbarkeit ist der Kern meiner Arbeit.

Vielen Dank. Ich freue mich auf eure Fragen und euer Feedback.
