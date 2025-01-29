# Description: Main file to run the application

import urllib
from IPython.display import Audio, display
import numpy as np
import tkinter as tk

from mediapipe.tasks import python
from mediapipe.tasks.python.components import containers
from mediapipe.tasks.python import audio
from scipy.io import wavfile

from ui.tk_ui import app
from classifier import Classifier

if __name__ == "__main__":
    app.run()



    