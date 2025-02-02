import librosa
import numpy as np
import os
from scipy.signal import butter, lfilter
from soundReader import Recorder
import threading


class Basketball_Dribbling:
    
    def __init__(self, app, schwellenwert_amplitude=0.05, frequenzbereich=(50, 200)):
        """
        :param schwellenwert_amplitude: Mindestlautstärke für Dribbling-Sounds.
        :param frequenzbereich: Typischer Frequenzbereich eines Basketball-Dribblings (Hz).
        """
        
        self.app = app
        self.schwellenwert_amplitude = schwellenwert_amplitude
        self.frequenzbereich = frequenzbereich

    def detect_dribbling(self, audio_data, sr=44100):
        """
        Prüft, ob eine Audiodatei Basketball-Dribblings enthält.        
        :return: Gibt anzahl der erkannten dribblings zurück
        """     
            
        try:
            # Falls `audio` nicht bereits `float32` ist, konvertieren
            audio = audio_data.astype(np.float32) / np.iinfo(np.int16).max
            
            # Bandpass-Filter anwenden
            audio = self._apply_bandpass_filter(audio, sr)

            # Kurzzeit-Fourier-Transformation (STFT)            
            stft = np.abs(librosa.stft(audio))
            
            # Berechne durchschnittliche Amplitude
            durchschnitt_amplitude = np.mean(stft)
            """
            if durchschnitt_amplitude <= self.schwellenwert_amplitude:
                return 0
            
            # Onset Detection
            onsets = librosa.onset.onset_detect(y=audio, sr=sr, backtrack=True, pre_max=10, post_max=10, delta=0.2)
            return len(onsets)
            """
            n_fft = 2048
            frequenzen = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
            amplituden = np.mean(stft, axis=1)

            # Dimensionen anpassen
            if len(frequenzen) != len(amplituden):
                amplituden = amplituden[:len(frequenzen)]

            # Filtere relevante Frequenzen
            relevante_frequenzen = frequenzen[(frequenzen >= self.frequenzbereich[0]) & (frequenzen <= self.frequenzbereich[1])]
            relevante_amplituden = amplituden[(frequenzen >= self.frequenzbereich[0]) & (frequenzen <= self.frequenzbereich[1])]
            """

            """
            # Erkenne Dribbling
            if durchschnitt_amplitude > self.schwellenwert_amplitude and np.sum(relevante_amplituden) > 0:
            
                onsets = librosa.onset.onset_detect(y=audio, sr=sr, backtrack=True, pre_max=10, post_max=10, delta=0.2)
            
                return len(onsets)
            else:
                return 0
            
        
        except Exception as e:
            print(f"Fehler bei der Dribbling-Erkennung: {e}")
            return 0
        
    def _apply_bandpass_filter(self, signal, sr, order=3):
        """Private Hilfsmethode für den Bandpass-Filter"""
        nyquist = 0.5 * sr
        low = self.frequenzbereich[0] / nyquist
        high = self.frequenzbereich[1] / nyquist
        b, a = butter(order, [low, high], btype='band')
        return lfilter(b, a, signal)


    def run_dribbling_detection(self):
        """
        Kontinuierliche Aufnahme & Auswertung.
        """
        while self.app.running:
            try:
                recorder = Recorder(rate=44100, record_seconds=2, chunksize=1024)
                audio = recorder.record_buffer()
                recorder.close()

                dribble_count = self.detect_dribbling(audio)

                if dribble_count > 0:
                    self.app.increase_dribblings(dribble_count)
                    print(f"Dribblings erkannt: {dribble_count}")
            except Exception as e:
                print(f"Fehler in der Hauptschleife: {e}")




class DribblingThread(threading.Thread):
    def __init__(self, dribbling_count):
        threading.Thread.__init__(self)
        self.dribbling_count = dribbling_count

    def run(self):
        self.dribbling_count.run_dribbling_detection()

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