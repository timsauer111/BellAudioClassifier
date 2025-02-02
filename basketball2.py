import librosa
import numpy as np
import os
from scipy.signal import butter, lfilter
from soundReader import Recorder
import threading

def bandpass_filter(signal, lowcut, highcut, sr, order=5):
    nyquist = 0.5 * sr
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, signal)


class Basketball_Dribbling:
    def __init__(self, app):
        self.app = app

    def erkenne_basketball_dribbling(self, schwellenwert_amplitude=0.05, frequenzbereich=(50, 200), record_seconds = 2):
        """
        Prüft, ob eine Audiodatei Basketball-Dribblings enthält.

        :param audio_datei: Pfad zur Audiodatei (z. B. .wav, .mp3).
        :param schwellenwert_amplitude: Mindestlautstärke für Dribbling-Sounds.
        :param frequenzbereich: Typischer Frequenzbereich eines Basketball-Dribblings (Hz).
        :return: Gibt "Dribbling erkannt" aus, wenn ein Basketball-Dribbling erkannt wurde.
        """
        while self.app.running:
            
            recorder = Recorder(rate=44100, record_seconds=record_seconds, chunksize=1024)
            audio = recorder.record_buffer()
            sr = 44100  # Sample-Rate für das Mikrofon
            recorder.close()

            # Falls `audio` nicht bereits `float32` ist, konvertieren
            audio = audio.astype(np.float32) / np.iinfo(np.int16).max

            print(f"Überprüfe das geladene Signal auf ungültige Werte...")
            if np.any(np.isnan(audio)):
                print("Das Audio-Signal enthält NaN-Werte!")
            if np.any(np.isinf(audio)):
                print("Das Audio-Signal enthält unendliche Werte!")
            
            # Bandpass-Filter anwenden
            #audio = bandpass_filter(audio, lowcut=frequenzbereich[0], highcut=frequenzbereich[1], sr=sr)

            # Kurzzeit-Fourier-Transformation (STFT)
            print("Berechne STFT...")
            stft = np.abs(librosa.stft(audio))
            
            # Berechne durchschnittliche Amplitude
            durchschnitt_amplitude = np.mean(stft)
            print(f"Durchschnittliche Amplitude: {durchschnitt_amplitude}")

            # Berechne Frequenzspektrum
            n_fft = 2048
            frequenzen = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
            amplituden = np.mean(stft, axis=1)

            # Dimensionen anpassen
            if len(frequenzen) != len(amplituden):
                amplituden = amplituden[:len(frequenzen)]

            # Filtere relevante Frequenzen
            relevante_frequenzen = frequenzen[(frequenzen >= frequenzbereich[0]) & (frequenzen <= frequenzbereich[1])]
            relevante_amplituden = amplituden[(frequenzen >= frequenzbereich[0]) & (frequenzen <= frequenzbereich[1])]

            print(f"Summe relevanter Amplituden: {np.sum(relevante_amplituden)}")

            # Erkenne Dribbling
            print("Erkenne Dribbling...")
            if durchschnitt_amplitude > schwellenwert_amplitude and np.sum(relevante_amplituden) > 0:
                onsets = librosa.onset.onset_detect(y=audio, sr=sr, backtrack=True, pre_max=10, post_max=10, delta=0.2)
                if len(onsets) > 0:
                    print(f"Basketball-Dribbling erkannt! Anzahl der Dribblings: {len(onsets)}")

                else:
                    print("Kein Dribbling erkannt (keine Impulsstruktur).")
            else:
                print("Kein Basketball-Dribbling erkannt.")


class DribblingThread(threading.Thread):
    def __init__(self, dribbling_count):
        threading.Thread.__init__(self)
        self.dribbling_count = dribbling_count
    def run(self):
        self.dribbling_count.erkenne_basketball_dribbling(record_seconds=2)

def start_dribbling_thread(app):
    d = Basketball_Dribbling(app)
    dribblingThread = DribblingThread(d)
    dribblingThread.start()
    print("Dribbling Thread started.")




# Beispielaufruf der Funktion zur Mikrofonaufnahme
 # 2 Sekunden Aufnahme

# Beispielaufruf mit Dateiprüfung
"""
audio_datei_pfad = "//workspaces//185091470//dribbling.wav"  # Ersetze mit dem korrekten Pfad
if os.path.exists(audio_datei_pfad):
erkenne_basketball_dribbling(audio_datei_pfad)
else:
print(f"Datei nicht gefunden: {audio_datei_pfad}")
"""
