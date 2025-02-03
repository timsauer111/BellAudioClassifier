#kontinuirliche aufnahme
import librosa
import numpy as np
import os
import noisereduce as nr
from scipy.signal import butter, lfilter
from soundReader import Recorder
import threading
import time
import queue



class Basketball_Dribbling:

    
    def __init__(self, app, schwellenwert_amplitude=0.6, frequenzbereich=(80, 150)):
        """
        :param schwellenwert_amplitude: Mindestlautstärke für Dribbling-Sounds.
        :param frequenzbereich: Typischer Frequenzbereich eines Basketball-Dribblings (Hz).
        """        
        self.app = app
        self.schwellenwert_amplitude = schwellenwert_amplitude
        self.frequenzbereich = frequenzbereich
        self.audio_queue = queue.Queue()  # Speicher für Audio-Daten
        self.running = True


    def detect_dribbling(self, audio_data, sr=44100):
        """
        Prüft, ob eine Audiodatei Basketball-Dribblings enthält.        
        :return: Gibt anzahl der erkannten dribblings zurück
        """                 
        try:
            t0 = time.time()
            
            # Falls `audio` nicht bereits `float32` ist, konvertieren
            audio = audio_data.astype(np.float32) / np.iinfo(np.int16).max
            
            audio = nr.reduce_noise(y=audio, sr=sr, stationary=True, prop_decrease=0.5)

            # Bandpass-Filter anwenden
            #audio = self._apply_bandpass_filter(audio, sr)

            # Kurzzeit-Fourier-Transformation (STFT)            
            stft = np.abs(librosa.stft(audio))
            
            # Berechne durchschnittliche Amplitude
            durchschnitt_amplitude = np.mean(stft)
                         
            n_fft = 2048
            frequenzen = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
            amplituden = np.mean(stft, axis=1)

            # Dimensionen anpassen
            if len(frequenzen) != len(amplituden):
                amplituden = amplituden[:len(frequenzen)]

            # Filtere relevante Frequenzen
            relevante_amplituden = amplituden[(frequenzen >= self.frequenzbereich[0]) & (frequenzen <= self.frequenzbereich[1])]
            print(relevante_amplituden[1])

            
            # Erkenne Dribbling
            if durchschnitt_amplitude > self.schwellenwert_amplitude and np.sum(relevante_amplituden) > 0:
            
                onsets = librosa.onset.onset_detect(y=audio, sr=sr, backtrack=True, pre_max=10, post_max=10, 
                    delta=0.3, units='frames', wait=5)    
                
                t1=time.time()
                total = t1 -t0
                print("berechnung", total)

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
    
    
    def continuous_recording(self):
        """Nimmt permanent auf und speichert Audio in einer Queue"""
        
        recorder = Recorder(rate=44100, record_seconds=2, chunksize=1024)  # Kürzere Aufnahmen

        while self.app.running:
            audio = recorder.record_buffer()
            self.audio_queue.put(audio)  # Speichert die Aufnahme für die Analyse        


    def run_dribbling_detection(self):
        """
        Kontinuierliche Aufnahme & Auswertung.
        """
        while self.app.running:
            try:
                if not self.audio_queue.empty():
                    audio = self.audio_queue.get()
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

    record_thread = threading.Thread(target = d.continuous_recording)
    record_thread.start()

    dribblingThread = DribblingThread(d)
    dribblingThread.start()
    print("Dribbling Thread started.")
