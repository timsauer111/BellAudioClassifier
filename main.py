import urllib
from IPython.display import Audio, display
import numpy as np

from mediapipe.tasks import python
from mediapipe.tasks.python.components import containers
from mediapipe.tasks.python import audio
from scipy.io import wavfile

#audio_file_name = 'speech_16000_hz_mono.wav'
#url = f'https://storage.googleapis.com/mediapipe-assets/{audio_file_name}'
#urllib.request.urlretrieve(url, audio_file_name)


file_name = 'data/bell-ringing-01c.wav'
#file_name = 'speech_16000_hz_mono.wav'
#display(Audio(file_name, autoplay=False))
model_path = '/model/yamnet.tflite'

# Customize and associate model for Classifier
base_options = python.BaseOptions(model_asset_path=model_path)
options = audio.AudioClassifierOptions(
    base_options=base_options, max_results=4)

# Create classifier, segment audio clips, and classify
with audio.AudioClassifier.create_from_options(options) as classifier:
  sample_rate, wav_data = wavfile.read(file_name)
  audio_clip = containers.AudioData.create_from_array(
      wav_data.astype(float) / np.iinfo(np.int16).max, sample_rate)
  classification_result_list = classifier.classify(audio_clip)

  #assert(len(classification_result_list) == 5)
detected_categories = []

# Iterate through clips to display classifications
for idx, timestamp in enumerate([1000, 2000, 3000, 4000, 5000, 6000]):    #enumerate([0, 975, 1950, 2925]):
    classification_result = classification_result_list[idx]
    top_category = classification_result.classifications[0].categories[0]
    detected_categories.append(top_category.category_name)
    print(f'Timestamp {timestamp}: {top_category.category_name} ({top_category.score:.2f})')