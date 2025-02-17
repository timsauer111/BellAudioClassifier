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

def erkenne_dribbling(audio_datei, schwellenwert_amplitude=0.10, frequenzbereich=(50, 200)):
    print("Starte Dribbling-Erkennung...")  # Debug-Startpunkt
    try:
        # Audiodatei prüfen
        print(f"Prüfe, ob die Datei existiert: {audio_datei}")
        if not os.path.exists(audio_datei):
            print(f"Datei nicht gefunden: {audio_datei}")
            return

        print("Lade Audiodatei...")
        audio, sr = librosa.load(audio_datei, sr=None, duration=5)
        print(f"Audiodatei geladen: Länge = {len(audio)}, Samplingrate = {sr}")

        # Bereinigen
        if not np.all(np.isfinite(audio)):
            print("Ungültige Werte gefunden. Bereinige...")
            audio = np.nan_to_num(audio, nan=0.0, posinf=0.0, neginf=0.0)

        print("Starte Visualisierung...")
        plt.figure(figsize=(10, 4))
        librosa.display.waveshow(audio, sr=sr)
        plt.title("Audiodatei - Zeitverlauf")
        plt.xlabel("Zeit (s)")
        plt.ylabel("Amplitude")


        plt.savefig("plot.png")
        print("Plot wurde als plot.png gespeichert.")


        print("Wende Bandpass-Filter an...")
        audio = bandpass_filter(audio, lowcut=frequenzbereich[0], highcut=frequenzbereich[1], sr=sr)

        print("Berechne STFT...")
        stft = np.abs(librosa.stft(audio))

        print("Berechne durchschnittliche Amplitude...")
        durchschnitt_amplitude = np.mean(stft)
        print(f"Durchschnittliche Amplitude: {durchschnitt_amplitude}")

        print("Berechne Frequenzspektrum...")
        n_fft = 2048
        frequenzen = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
        amplituden = np.mean(stft, axis=1)

        print("Filtere relevante Frequenzen...")
        if len(frequenzen) != len(amplituden):
            amplituden = amplituden[:len(frequenzen)]
        relevante_frequenzen = frequenzen[(frequenzen >= frequenzbereich[0]) & (frequenzen <= frequenzbereich[1])]
        relevante_amplituden = amplituden[(frequenzen >= frequenzbereich[0]) & (frequenzen <= frequenzbereich[1])]

        print(f"Summe relevanter Amplituden: {np.sum(relevante_amplituden)}")

        print("Erkenne Dribblings...")
        if durchschnitt_amplitude > schwellenwert_amplitude and np.sum(relevante_amplituden) > 0:
            onsets = librosa.onset.onset_detect(y=audio, sr=sr, backtrack=True, pre_max=10, post_max=10, delta=0.1)
            print(f"Onsets: {onsets}")
            if len(onsets) > 0:
                print(f"Basketball-Dribbling erkannt! Anzahl der Dribblings: {len(onsets)}")
            else:
                print("Kein Dribbling erkannt (keine Impulsstruktur).")
        else:
            print("Kein Basketball-Dribbling erkannt.")

    except Exception as e:
        print(f"Fehler bei der Verarbeitung der Datei: {e}")


# Beispielaufruf
audio_datei_pfad = "Finn/dribbling.wav"
erkenne_dribbling(audio_datei_pfad)




