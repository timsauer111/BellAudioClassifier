# Description: Main file to run the application

import urllib
from IPython.display import Audio, display
import numpy as np

from mediapipe.tasks import python
from mediapipe.tasks.python.components import containers
from mediapipe.tasks.python import audio
from scipy.io import wavfile

from soundReader import Recorder

from ui import app

if __name__ == "__main__":
    webapp = app.create_app()
    webapp.run(debug=True)