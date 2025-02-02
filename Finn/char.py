import librosa
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

# Lade die Audiodatei
y, sr = librosa.load('Aufzeichnung.wav')

# Berechne die Fourier-Transformation
N = len(y)
T = 1.0 / sr
yf = fft(y)
xf = fftfreq(N, T)[:N//2]

# Plotten des Frequenzspektrums
plt.plot(xf, 2.0/N * np.abs(yf[0:N//2]))
plt.title('Frequenzspektrum eines Basketballdribblings')
plt.xlabel('Frequenz (Hz)')
plt.ylabel('Amplitude')
plt.grid()
plt.show()