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

    def erkenne_basketball_dribbling(self, schwellenwert_amplitude=0.05, frequenzbereich=(50, 200), record_seconds = 10):
        """
        Prüft, ob eine Audiodatei Basketball-Dribblings enthält.

        :param audio_datei: Pfad zur Audiodatei (z. B. .wav, .mp3).
        :param schwellenwert_amplitude: Mindestlautstärke für Dribbling-Sounds.
        :param frequenzbereich: Typischer Frequenzbereich eines Basketball-Dribblings (Hz).
        :return: Gibt "Dribbling erkannt" aus, wenn ein Basketball-Dribbling erkannt wurde.
        """
        while self.app.running:
            try:
                """
                # Audiodatei laden        
                audio, sr = librosa.load(audio_datei, sr=None)
                
                rec = Recorder(rate=44100, record_seconds=record_seconds, chunksize=1024)

                # Aufnahme vom Mikrofon starten
                audio_buffer = rec.record_buffer()

                # Verarbeite die Audiodaten, die vom Mikrofon aufgenommen wurden
                sr = 44100  # Sample-Rate setzen (kann je nach Mikrofon angepasst werden)"""

                recorder = Recorder(rate=44100, record_seconds=record_seconds, chunksize=1024)
                audio = recorder.record_buffer()  # Audio aufnehmen
                sr = 44100  # Sample-Rate für das Mikrofon

                audio = audio.astype(np.float32) / np.iinfo(np.int16).max

                gefiltertes_signal = bandpass_filter(audio, lowcut=frequenzbereich[0], highcut=frequenzbereich[1], sr=sr)
                
                
                
                #gefiltertes_signal = bandpass_filter(audio, lowcut=50, highcut=200, sr=sr)

                # Kurzzeit-Fourier-Transformation (STFT)
                #print(np.abs(librosa.stft(audio)))
                stft = np.abs(librosa.stft(audio))

                # Berechnung der mittleren Amplitude
                durchschnitt_amplitude = np.mean(stft)

                # Berechnung des Frequenzspektrums
                n_fft = 2048
                frequenzen = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
                amplituden = np.mean(stft, axis=1)

                # Dimensionen überprüfen und anpassen
                if len(frequenzen) != len(amplituden):
                    amplituden = amplituden[:len(frequenzen)]

                # Filtern der relevanten Frequenzen im spezifizierten Bereich
                relevante_frequenzen = frequenzen[(frequenzen >= frequenzbereich[0]) & (frequenzen <= frequenzbereich[1])]
                relevante_amplituden = amplituden[(frequenzen >= frequenzbereich[0]) & (frequenzen <= frequenzbereich[1])]

                # Erkennung von Dribbling-Mustern basierend auf Lautstärke und Frequenzen
                if durchschnitt_amplitude > schwellenwert_amplitude and np.sum(relevante_amplituden) > 0:
                    # Onset-Erkennung für Impulsanalyse
                    onsets = librosa.onset.onset_detect(y=audio, sr=sr, backtrack=True)
                    if len(onsets) > 0:
                        print(f"Basketball-Dribbling erkannt! Anzahl der Dribblings: {len(onsets)}")
                        self.app.increase_dribblings(len(onsets))
                    else:
                        print("Kein Dribbling erkannt (keine Impulsstruktur).")
                else:
                    print("Kein Basketball-Dribbling erkannt.")

            except Exception as e:
                print(f"Fehler bei der Verarbeitung der Datei: {e}")

class DribblingThread(threading.Thread):
    def __init__(self, dribbling_count):
        threading.Thread.__init__(self)
        self.dribbling_count = dribbling_count
    def run(self):
        print("Run Dribbling Classifier")
        self.dribbling_count.erkenne_basketball_dribbling(record_seconds=2)

def start_dribbling_thread(app):
    d = Basketball_Dribbling(app)
    dribblingThread = DribblingThread(d)
    dribblingThread.start()




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
