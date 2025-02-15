"""
This script uses MediaPipe's AudioClassifier to record short audio
samples and classify them. The results are returned.
"""

from IPython.display import Audio, display
import numpy as np

import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python.components import containers
from mediapipe.tasks.python import audio
from scipy.io import wavfile

from soundReader import Recorder

import time


import threading


class Classifier():
    """
    This class wraps MediaPipe's AudioClassifier to detect specific bell sounds.
    
    :param app: The main application object controlling the overall flow.
    """
    def __init__(self, app):
        self.AudioClassifier = mp.tasks.audio.AudioClassifier
        self.AudioClassifierOptions = mp.tasks.audio.AudioClassifierOptions
        self.AudioClassifierResult = mp.tasks.audio.AudioClassifierResult
        self.AudioRunningMode = mp.tasks.audio.RunningMode
        self.BaseOptions = mp.tasks.BaseOptions
        self.model_path = 'model/yamnet.tflite' # Path to the model file
        self.app = app


        self.options = self.AudioClassifierOptions(
            base_options=self.BaseOptions(model_asset_path=self.model_path),
            running_mode=self.AudioRunningMode.AUDIO_CLIPS,
            max_results=5,
        )

        # Define, which sounds should trigger the counter
        self.classfication_set = {
                                'Bell', 'Church bell', 'Doorbell', 'Jingle bell', 'Tolling bell', 
                                  'Glockenspiel', 'Tambourine', 'Maraca', 'Sleigh bell', 
                                  'tinkle', 'jingle', 'Ding'
                                  }

    def classify_input_audio(self, classifier):
        """
        Records a short audio sample using the Recorder, classifies it with the given
        AudioClassifier, and returns a list of recognized category names.

        :param classifier: An instantiated AudioClassifier for processing audio data.
        :return: A list of recognized category names (strings).
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
    
    def start_classifier(self):
        """
        Creates the AudioClassifier instance and calls the audio classification loop.
        """
        self.classifier_instance = self.AudioClassifier.create_from_options(self.options)
        self.classify_audio()


    def classify_audio(self):
        """
        Continuously checks for recognized bell sounds while the app is running.
        If any recognized category belongs to classfication_set, increments the counter.
        """
        while self.app.running:
            results = self.classify_input_audio(self.classifier_instance)
            if self.classfication_set.intersection(results):
                print("Bell detected")
                self.app.increase_made_shots()
                print(results)
                time.sleep(2)
                
            else:
                print(results)

        self.classifier_instance.close()
        

class ClassifierThread(threading.Thread):
    """
    A threading class that starts the audio classification in a background thread.

    :param classifier: An instance of the Classifier class to run in this thread.
    """
    def __init__(self, classifier):
        threading.Thread.__init__(self)
        self.classifier = classifier

    def run(self):
        self.classifier.start_classifier()



def start_classifier_thread(app):
    """
    Convenience function to create and start the Classifier in a separate thread.

    :param app: The main application instance.
    """
    c = Classifier(app)
    classifier_thread = ClassifierThread(c)
    classifier_thread.start()
    print("Classifier thread started")



