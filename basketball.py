import librosa
import numpy as np
from scipy.signal import butter, lfilter
from soundReader import Recorder  # Deine Recorder-Klasse importieren

def bandpass_filter(signal, lowcut, highcut, sr, order=5):
    nyquist = 0.5 * sr
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, signal)

def erkenne_basketball_dribbling(schwellenwert_amplitude=0.2, frequenzbereich=(50, 200), record_seconds=10):
    """
    Prüft, ob eine Audiodatei Basketball-Dribblings enthält.

    :param schwellenwert_amplitude: Mindestlautstärke für Dribbling-Sounds.
    :param frequenzbereich: Typischer Frequenzbereich eines Basketball-Dribblings (Hz).
    :param record_seconds: Länge der Audioaufnahme in Sekunden.
    :return: Gibt aus, ob Dribbling erkannt wurde.
    """
    
    # Audio aufnehmen
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

    

# Aufnahme starten (2 Sekunden)
erkenne_basketball_dribbling()
