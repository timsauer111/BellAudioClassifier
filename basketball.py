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

def erkenne_basketball_dribbling(schwellenwert_amplitude=0.05, frequenzbereich=(50, 200), record_seconds=2):
    """
    Prüft, ob eine Audiodatei Basketball-Dribblings enthält.

    :param schwellenwert_amplitude: Mindestlautstärke für Dribbling-Sounds.
    :param frequenzbereich: Typischer Frequenzbereich eines Basketball-Dribblings (Hz).
    :param record_seconds: Länge der Audioaufnahme in Sekunden.
    :return: Gibt aus, ob Dribbling erkannt wurde.
    """
    try:
        # Audio aufnehmen
        recorder = Recorder(rate=44100, record_seconds=record_seconds, chunksize=1024)
        audio = recorder.record_buffer()
        sr = 44100  # Sample-Rate für das Mikrofon

        # Falls `audio` nicht bereits `float32` ist, konvertieren
        if audio.dtype != np.float32:
            audio = audio.astype(np.float32) / np.iinfo(np.int16).max

        # Bandpass-Filter anwenden
        audio = bandpass_filter(audio, lowcut=frequenzbereich[0], highcut=frequenzbereich[1], sr=sr)

        # Kurzzeit-Fourier-Transformation (STFT)
        stft = np.abs(librosa.stft(audio))

        # Berechnung der mittleren Amplitude
        durchschnitt_amplitude = np.mean(stft)

        # Frequenzspektrum berechnen
        n_fft = 2048
        frequenzen = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
        amplituden = np.mean(stft, axis=1)

        # Relevante Frequenzen filtern
        relevante_mask = (frequenzen >= frequenzbereich[0]) & (frequenzen <= frequenzbereich[1])
        relevante_amplituden = amplituden[relevante_mask]

        # Erkennung von Dribbling-Mustern
        if durchschnitt_amplitude > schwellenwert_amplitude and np.sum(relevante_amplituden) > 0:
            # Onset-Erkennung für Impulsanalyse
            onsets = librosa.onset.onset_detect(y=audio, sr=sr, backtrack=True)
            if len(onsets) > 0:
                print(f"🏀 Basketball-Dribbling erkannt! Anzahl der Dribblings: {len(onsets)}")
            else:
                print("❌ Kein Dribbling erkannt (keine Impulsstruktur).")
        else:
            print("❌ Kein Basketball-Dribbling erkannt.")

    except Exception as e:
        print(f"⚠️ Fehler bei der Verarbeitung: {e}")

# Aufnahme starten (2 Sekunden)
erkenne_basketball_dribbling(record_seconds=2)
