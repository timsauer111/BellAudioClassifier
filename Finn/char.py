import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

# Step 1: Load the audio file
audio_path = "/home/user/BellAudioClassifier/testData/5_regelmaesig.wav"  # Replace with your audio file path
y, sr = librosa.load(audio_path, sr=None)  # y: audio waveform, sr: sample rate

# Step 2: Visualize the waveform
plt.figure(figsize=(12, 6))
librosa.display.waveshow(y, sr=sr)
plt.title("Audio Waveform")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.show()

# Step 3: Compute the Short-Time Fourier Transform (STFT)
D = np.abs(librosa.stft(y))  # STFT magnitude
DB = librosa.amplitude_to_db(D, ref=np.max)  # Convert to decibels

# Step 4: Visualize the spectrogram
plt.figure(figsize=(12, 6))
librosa.display.specshow(DB, sr=sr, x_axis='time', y_axis='log')
plt.colorbar(format="%+2.0f dB")
plt.title("Spectrogram")
plt.show()

# Step 5: Detect onsets
onsets = librosa.onset.onset_detect(y=y, sr=sr, units='time')
print("Onset times (s):", onsets)

# Step 6: Extract features (e.g., MFCCs)
mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
plt.figure(figsize=(12, 6))
librosa.display.specshow(mfccs, x_axis='time')
plt.colorbar()
plt.title("MFCCs")
plt.show()

# Step 7: Apply a bandpass filter (optional)
def apply_bandpass_filter(signal, sr, lowcut=80, highcut=150, order=2):
    nyquist = 0.5 * sr
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return filtfilt(b, a, signal)

y_filtered = apply_bandpass_filter(y, sr)

# Step 8: Visualize the filtered waveform
plt.figure(figsize=(12, 6))
librosa.display.waveshow(y_filtered, sr=sr)
plt.title("Filtered Audio Waveform")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.show()