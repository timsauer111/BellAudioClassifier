from IPython.display import Audio, display
import numpy as np

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python.components import containers
from mediapipe.tasks.python import audio
from scipy.io import wavfile

from soundReader import Recorder

AudioClassifier = mp.tasks.audio.AudioClassifier
AudioClassifierOptions = mp.tasks.audio.AudioClassifierOptions
AudioClassifierResult = mp.tasks.audio.AudioClassifierResult
AudioRunningMode = mp.tasks.audio.RunningMode
BaseOptions = mp.tasks.BaseOptions
model_path = 'model/yamnet.tflite' # Path to the model file

def print_result(result, timestamp_ms: int):
    print(f"Timestamp: {timestamp_ms}\n Result: {result}\n\n")

options = AudioClassifierOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=AudioRunningMode.AUDIO_STREAM,
    max_results=5,
    result_callback=print_result)

with AudioClassifier.create_from_options(options) as classifier:
    AudioData = mp.tasks.components.containers.AudioData
    print("Opening Recorder...")
    rec = Recorder(rate=44100, record_seconds=2, chunksize=1024)
    buffer = rec.record_buffer()
    print("Transferring buffer to AudioData...")
    audio_data = AudioData.create_from_array(buffer.astype(float) / np.iinfo(np.int16).max, rec.rate)

    for timestamp_ms in [500, 1000, 1500]:
        classifier.classify_async(audio_data, timestamp_ms)
        # Wait for the result.
    
    rec.close()

    

  