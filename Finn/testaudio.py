import librosa.display
import matplotlib.pyplot as plt
import os
import librosa.display
import matplotlib.pyplot as plt

# Lade die Datei
audio, sr = librosa.load(audio_datei, sr=None)

# Plotte das Audio-Signal
plt.figure(figsize=(10, 4))
librosa.display.waveshow(audio, sr=sr)
plt.title("Audiodatei - Zeitverlauf")
plt.xlabel("Zeit (s)")
plt.ylabel("Amplitude")
plt.show()



audio_datei_pfad = os.path.join(os.getcwd(), "dribbling.wav")  # Pfad zur Audiodatei
audio_datei = audio_datei_pfad

# Lade die Datei
audio, sr = librosa.load(audio_datei, sr=None)

# Plotte das Audio-Signal
plt.figure(figsize=(10, 4))
librosa.display.waveshow(audio, sr=sr)
plt.title("Audiodatei - Zeitverlauf")
plt.xlabel("Zeit (s)")
plt.ylabel("Amplitude")
plt.show()
