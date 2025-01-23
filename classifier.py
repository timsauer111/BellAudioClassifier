"""
This script uses MediaPipe's AudioClassifier to record short audio
samples and classify them. The results are printed to the console.
"""

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

  
options = AudioClassifierOptions(
    base_options=BaseOptions(model_asset_path=model_path),
    running_mode=AudioRunningMode.AUDIO_CLIPS,
    max_results=5
)

def start_classifier():
    with AudioClassifier.create_from_options(options) as classifier:
        # The 'classify_input_audio' function handles audio recording and classification.

        def classify_input_audio():
            """
            Records short audio samples, processes them via AudioClassifier, 
            and returns a list of category names.

            :return: A list of string category names recognized for the recorded audio.
            """
            # Start recording using specified sample rate and duration.
            rec = Recorder(rate=44100, record_seconds=2, chunksize=1024)
            # Fetch audio data into a numpy buffer.
            buffer = rec.record_buffer()
            audio_data = mp.tasks.components.containers.AudioData.create_from_array(
                buffer.astype(float)/np.iinfo(np.int16).max, 
                rec.rate
            )
            result = classifier.classify(audio_data)
            
            """
            result = [ClassificationResult(classifications=[Classifications(categories=[Category(index=132, score=0.19921875, display_name='', category_name='Music'), Category(index=133, score=0.08203125, display_name='', category_name='Musical instrument'), Category(index=158, score=0.05859375, display_name='', category_name='Drum machine'), Category(index=500, score=0.05859375, display_name='', category_name='Inside, small room'), Category(index=153, score=0.05859375, display_name='', category_name='Synthesizer')], head_index=0, head_name='scores')], timestamp_ms=0), ClassificationResult(classifications=[Classifications(categories=[Category(index=132, score=0.66796875, display_name='', category_name='Music'), Category(index=159, score=0.19921875, display_name='', category_name='Drum'), Category(index=156, score=0.19921875, display_name='', category_name='Percussion'), Category(index=133, score=0.1484375, display_name='', category_name='Musical instrument'), Category(index=168, score=0.08203125, display_name='', category_name='Wood block')], head_index=0, head_name='scores')], timestamp_ms=975), ClassificationResult(classifications=[Classifications(categories=[Category(index=132, score=0.08203125, display_name='', category_name='Music'), Category(index=494, score=0.05859375, display_name='', category_name='Silence'), Category(index=498, score=0.04296875, display_name='', category_name='Sound effect'), Category(index=0, score=0.01953125, display_name='', category_name='Speech'), Category(index=153, score=0.01171875, display_name='', category_name='Synthesizer')], head_index=0, head_name='scores')], timestamp_ms=1950)]
            -->result is a list of ClasificationResult objects

            ClassificationResult(classifications=[Classifications(categories=[Category(index=132, score=0.19921875, display_name='', category_name='Music'), Category(index=133, score=0.08203125, display_name='', category_name='Musical instrument'), Category(index=158, score=0.05859375, display_name='', category_name='Drum machine'), Category(index=500, score=0.05859375, display_name='', category_name='Inside, small room'), Category(index=153, score=0.05859375, display_name='', category_name='Synthesizer')], head_index=0, head_name='scores')], timestamp_ms=0)
            -->result[n] is a ClassificationResult object with classifications attribute
            --> result[0].classifications is a list of Classifications objects

            Classifications(categories=[Category(index=132, score=0.19921875, display_name='', category_name='Music'), Category(index=133, score=0.08203125, display_name='', category_name='Musical instrument'), Category(index=158, score=0.05859375, display_name='', category_name='Drum machine'), Category(index=500, score=0.05859375, display_name='', category_name='Inside, small room'), Category(index=153, score=0.05859375, display_name='', category_name='Synthesizer')], head_index=0, head_name='scores')
            -->result[0].classifications[0].categories is a list of Category objects

            Category(index=132, score=0.19921875, display_name='', category_name='Music')
            -->result[0].classifications[0].categories[0].category_name is a tuple with timestamp and category name
            """

            # Close the recorder to release resources.
            rec.close()

            # Extract timestamp and corresponding category name from result.
            result_categories = [
                (r.timestamp_ms, cat.category_name)
                for r in result
                if r.classifications
                for classification in r.classifications
                if classification.categories
                for cat in classification.categories
            ]
            return [cat_name for _, cat_name in result_categories]
        
        # Loop for multiple classifications, printing categorization each time.
        for i in range(5):
            print(f"Classification {i+1}:\n{classify_input_audio()}\n\n")

    print("\n\nStopped Classifier. End of Program.")






