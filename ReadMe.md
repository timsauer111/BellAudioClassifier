# BASKETBALL AUDIO CLASSIFIER
#### Author1: Ihr Name / Ihre Matrikelnummer
#### Author2: Tim Sauer / 2171049
#### Video: <URL>
#### Description:

Dieses Projekt, der Basketball Audio Classifier, wird vorwiegend im Basketballtraining eingesetzt. An den Basketballkorb werden Glocken angebracht, sodass Treffer sowie Dribblings akustisch erfasst werden können. Dabei zählt der Classifier jeden Glockenschlag als Treffer und analysiert gleichzeitig typische Dribbling-Geräusche. Dieses System ermöglicht Spielern, ihre eigene Leistung im Wurftraining zu überwachen und sich zu verbessern.

Die Anwendung ist modular aufgebaut und in mehrere Dateien unterteilt, um eine klare Struktur und einfache Erweiterbarkeit zu gewährleisten. 
In tk_ui.py wird die grafische Benutzeroberfläche mit Tkinter realisiert. Hier werden Buttons, Zähler und Labels definiert, die den aktuellen Stand der Treffer und Dribblings anzeigen. 
Die Datei main.py dient als Einstiegspunkt und startet die gesamte Anwendung. 
In classifier.py erfolgt die Erkennung von Glockenschlägen mithilfe von MediaPipe, welches robuste Modelle zur Audioanalyse verwendet. 
Die Aufnahme und Verarbeitung der Audiodaten übernimmt soundReader.py, während basketball2.py spezifisch für die Zählung von Dribbling-Geräuschen zuständig ist.

Die technischen Entscheidungen des Projekts liegen klar auf Einfachheit und Funktionalität. Python wurde als Programmiersprache gewählt, da es eine schnelle Entwicklung und einfache Wartung ermöglicht. Tkinter sorgt mit einer schlanken GUI dafür, dass Nutzer sofortige Rückmeldungen erhalten, ohne dass komplexe Frameworks notwendig sind. Die Nutzung von MediaPipe basiert auf dessen bewährter Zuverlässigkeit bei der Audioanalyse. Durch den Einsatz von Multithreading (beispielsweise ListenerThread und DribblingThread) wird erreicht, dass die Benutzeroberfläche flüssig bleibt, selbst wenn im Hintergrund rechenintensive Audiosignale verarbeitet werden.

Zusammengefasst bietet der Basketball Audio Classifier ein praktisches Tool zur Leistungsüberwachung im Basketballtraining. Die klare Trennung zwischen GUI, Audioaufnahme, -verarbeitung und -analyse ermöglicht eine einfache Anpassung an unterschiedliche Trainingssituationen. Die Entwickler haben bewusst auf unnötige Ausschmückungen verzichtet und sich auf die Kernfunktionalitäten konzentriert, um ein zuverlässiges Echtzeitsystem zu schaffen. Alle Designentscheidungen – von der Wahl der Programmiersprache über die modulare Architektur bis hin zur Verwendung von Multithreading – wurden getroffen, um eine effiziente und benutzerfreundliche Anwendung zu gewährleisten.



