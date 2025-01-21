import numpy as np
import pyaudio
import scipy.io.wavfile as wav

class Recorder:
    def __init__(self, rate, record_seconds, chunksize):
        self.rate = rate
        self.record_seconds = record_seconds
        self.chunksize = chunksize
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=self.rate, input=True, frames_per_buffer=self.chunksize)
        
    def record_buffer(self):
        print(f'Recording for {self.record_seconds} seconds...')
        frames = []
        for _ in range(0, int(self.rate / self.chunksize * self.record_seconds)):
            data = self.stream.read(self.chunksize)
            frames.append(np.frombuffer(data, dtype=np.int16))
        print('Recording complete.')
        print("Converting...")
        numpydata = np.hstack(frames)
        print("Conversion complete.")
        return numpydata
    
    def safe_wav(self, filename):
        numpydata = self.record_buffer()
        print(f'Saving to {filename}...')
        wav.write(filename, self.rate, numpydata)
        print('Save complete.')

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        print("Stopped Recording.")



#Test All Recoder Functions:

#rec = Recorder(rate=44100, record_seconds=5, chunksize=1024)
#rec.record_wav('testData/recordedTest.wav')
#rec.close()