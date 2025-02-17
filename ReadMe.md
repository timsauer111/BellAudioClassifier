# BASKETBALL AUDIO CLASSIFIER
#### Author1: Finn Hennig / 2181633
#### Author2: Tim Sauer / 2171049
#### Video: https://youtu.be/vhjmgrkiWD0
#### GitHub: https://github.com/timsauer111/BellAudioClassifier

## Description

**English Version**

This project, the *Basketball Audio Classifier*, is designed primarily for basketball training. Bells are attached to the hoop to capture made shots and dribbling sounds. The classifier counts each bell sound as a made shot, while dribbling noises are analyzed to monitor ball handling. This quick feedback system helps players improve their shooting and dribbling performance.

### Modular Files
- **tk_ui.py**: Implements the graphical user interface using Tkinter/CustomTkinter. It features two main modes:
  - **Count Mode**: Continuously counts shots and dribbles, allowing users to choose between shots only, dribbles only, or both.
  - **Challenge Mode**: Enables users to set custom targets and time limits for training challenges. A countdown timer and real-time progress updates guide the challenge.
- **main.py**: Serves as the entry point to launch the application.
- **classifier.py**: Detects bell sounds using MediaPipe's robust audio analysis models.
- **soundReader.py**: Handles audio recording and processing.
- **basketball2.py**: Processes dribbling audio signals using techniques such as the Fourier Transform.

### UI Modes
The application offers two selectable modes:
- **Count Mode**: Best suited for regular training sessions, it displays live counts of successful shots and dribbling events.
- **Challenge Mode**: Simulates a competitive scenario with adjustable difficulty. Users can set a target (e.g., number of dribbles or shots) and a time limit. The interface shows a countdown timer and updates the progress continuously.

### Technical Decisions
Python was chosen for its rapid development and ease of maintenance. Tkinter/CustomTkinter provides a lightweight, responsive GUI without the overhead of complex frameworks. MediaPipe was selected for its proven reliability in audio analysis. Multithreading (using ListenerThread and DribblingThread) guarantees that the interface remains smooth during heavy background processing.

In summary, the *Basketball Audio Classifier* is a practical tool for tracking performance in basketball training. Its modular design and selectable modes allow flexible adaptation to various training scenarios. All design decisions—from the programming language to the modular architecture and multithreading—were made to ensure an efficient and user-friendly real-time system.

--------------------------------------------------------------------------------

**Deutsche Version**

Dieses Projekt, der *Basketball Audio Classifier*, wird vorwiegend im Basketballtraining eingesetzt. An den Basketballkorb werden Glocken angebracht, sodass Treffer sowie Dribblings akustisch erfasst werden können. Dabei zählt der Classifier jeden Glockenschlag als Treffer und analysiert gleichzeitig typische Dribbling-Geräusche, um Spielern ein schnelles Feedback zu ermöglichen.

### Modulare Dateien
- **tk_ui.py**: Verantwortlich für die Benutzeroberfläche, die mit Tkinter/CustomTkinter realisiert wird. Enthalten sind zwei Hauptmodi:
  - **Count Mode**: Zählt kontinuierlich Treffer und Dribblings und erlaubt die Auswahl zwischen der Zählung von Treffern, Dribblings oder beidem.
  - **Challenge Mode**: Ermöglicht das Festlegen individueller Ziele und Zeitlimits. Ein Countdown-Timer und Echtzeit-Updates führen den Nutzer durch die Herausforderung.
- **main.py**: Dient als Einstiegspunkt und startet die Anwendung.
- **classifier.py**: Erkennt Glockenschläge mithilfe von MediaPipe, das robuste Modelle zur Audioanalyse bietet.
- **soundReader.py**: Übernimmt die Aufnahme und Verarbeitung der Audiodaten.
- **basketball2.py**: Zählt Dribbling-Geräusche mittels Algorithmen wie der Fourier-Transformation.

### Auswahl der Modi in der UI
Die Anwendung bietet zwei auswählbare Modi:
- **Count Mode**: Ideal für das reguläre Training, da hier Treffer und Dribblings live gezählt werden.
- **Challenge Mode**: Simuliert eine Wettkampfsituation, in der Nutzer Ziele (z. B. Anzahl der Dribblings oder Treffer) und ein Zeitlimit festlegen können. Ein Countdown-Timer und fortlaufende Fortschrittsanzeigen unterstützen den Nutzer während der Challenge.

### Technische Entscheidungen
Python wurde aufgrund seiner schnellen Entwicklung und einfachen Wartbarkeit gewählt. Die Verwendung von Tkinter/CustomTkinter ermöglicht eine schlanke und reaktionsschnelle GUI ohne komplexe Frameworks. MediaPipe überzeugt durch seine Zuverlässigkeit in der Audioanalyse. Der Einsatz von Multithreading (z. B. ListenerThread und DribblingThread) stellt sicher, dass die Oberfläche auch bei intensiver Hintergrundverarbeitung flüssig bleibt.

Zusammenfassend stellt der *Basketball Audio Classifier* ein praktisches Tool zur Leistungsüberwachung im Basketballtraining dar. Die klare Trennung in modulare Dateien und die verschiedenen auswählbaren Modi ermöglichen eine flexible Anpassung an unterschiedliche Trainingssituationen. Alle Designentscheidungen – von der Wahl der Programmiersprache über die modulare Architektur bis hin zur Verwendung von Multithreading – wurden getroffen, um ein effizientes und benutzerfreundliches Echtzeitsystem zu gewährleisten.



