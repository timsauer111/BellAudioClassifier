import pyaudio
import numpy as np
import scipy.io.wavfile as wav

# Mikrofonaufnahme testen
rate = 44100  # Sample-Rate
duration = 5  # Sekunden
chunksize = 1024

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=rate,
                input=True,
                frames_per_buffer=chunksize)

print("Recording...")
frames = []

for _ in range(0, int(rate / chunksize * duration)):
    data = stream.read(chunksize)
    frames.append(np.frombuffer(data, dtype=np.int16))

print("Recording complete.")

# Daten in eine WAV-Datei speichern
audio_data = np.hstack(frames)
wav.write("test_recording.wav", rate, audio_data)

stream.stop_stream()
stream.close()
p.terminate()
