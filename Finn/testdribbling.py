import librosa
import numpy as np
import os
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt

def bandpass_filter(signal, lowcut, highcut, sr, order=5):
    nyquist = 0.5 * sr
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, signal)

def erkenne_dribbling(audio_datei, schwellenwert_amplitude=0.26, frequenzbereich=(50, 200)):
    """
    Prüft, ob eine Audiodatei Basketball-Dribblings enthält.
    """
    print("Starte Dribbling-Erkennung...")

    try:
        # Audiodatei laden
        if not os.path.exists(audio_datei):
            print(f"Datei nicht gefunden: {audio_datei}")
            return
        print(f"Lade Audiodatei: {audio_datei}")
        audio, sr = librosa.load(audio_datei, sr=None)

        # Überprüfen, ob das Audio-Signal gültig ist
        print(f"Überprüfe das geladene Signal auf ungültige Werte...")
        if np.any(np.isnan(audio)):
            print("Das Audio-Signal enthält NaN-Werte!")
        if np.any(np.isinf(audio)):
            print("Das Audio-Signal enthält unendliche Werte!")

        # Länge und Samplingrate
        print(f"Audiodatei geladen: Länge = {len(audio)}, Samplingrate = {sr}")

        # Visualisierung (nur die ersten 5 Sekunden)
        

        # Bandpass-Filter anwenden
        #print("Wende Bandpass-Filter an...")        
        #audio = bandpass_filter(audio, lowcut = 50, highcut=200, sr=sr)
        
        """
        plt.figure(figsize=(10, 4))
        librosa.display.waveshow(audio, sr=sr)
        plt.title("Audiodatei - Zeitverlauf")
        plt.xlabel("Zeit (s)")
        plt.ylabel("Amplitude")
        plt.show()
        """

        # Berechne STFT
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
                #onset_zeiten = librosa.frames_to_time(onsets, sr=sr)
                print(f"Basketball-Dribbling erkannt! Anzahl der Dribblings: {len(onsets)}")
            else:
                print("Kein Dribbling erkannt (keine Impulsstruktur).")
        else:
            print("Kein Basketball-Dribbling erkannt.")

    except Exception as e:
        print(f"Fehler bei der Verarbeitung der Datei: {e}")

# Beispielaufruf
audio_datei_pfad =  os.path.join(os.getcwd(), "Aufzeichnung.wav")  # Pfad zur Audiodatei
erkenne_dribbling(audio_datei_pfad)
