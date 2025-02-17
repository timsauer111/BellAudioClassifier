import numpy as np
import pyaudio
import scipy.io.wavfile as wav
import time

class Recorder:
    """
    This class handles audio recording using PyAudio and provides methods
    to record audio data into a buffer or save the recorded data as a WAV file.
    """

    def __init__(self, rate, record_seconds, chunksize):
        """
        Initializes the Recorder object.

        :param rate: Capture sample rate in Hertz.
        :param record_seconds: Total duration to record, in seconds.
        :param chunksize: Number of frames per buffer read.
        """
        # Initialize PyAudio and open an input stream
        self.rate = rate
        self.record_seconds = record_seconds
        self.chunksize = chunksize
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunksize
        )

    def record_buffer(self):
        """
        Records audio data by reading from the configured PyAudio stream.

        :return: A NumPy array containing the recorded audio samples.
        """
        print(f'Recording for {self.record_seconds} seconds...')
        frames = []
        for _ in range(0, int(self.rate / self.chunksize * self.record_seconds)):
            try:
                data = self.stream.read(self.chunksize)
                frames.append(np.frombuffer(data, dtype=np.int16))
            except OSError as e:
                time.sleep(self.record_seconds)
                break
        try:
            numpydata = np.hstack(frames)  # Combine buffers into one NumPy array
            return numpydata
        except ValueError as e:
            return np.array([])
        
    def safe_wav(self, filename):
        """
        Records audio data and saves it as a WAV file.

        :param filename: The destination file path for the WAV output.
        """
        numpydata = self.record_buffer()
        print(f'Saving to {filename}...')
        wav.write(filename, self.rate, numpydata)  # Write recorded data to WAV
        print('Save complete.')

    def close(self):
        """
        Stops the recording stream and releases all associated resources.
        """
        try:
            self.stream.stop_stream()
            self.stream.close()
            self.p.terminate()
        except OSError as e:
            pass
        print("Stopped Recording.")

