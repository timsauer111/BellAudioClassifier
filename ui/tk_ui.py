import tkinter as tk
from classifier import Classifier
import time


class BellAudioClassifierUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bell Audio Classifier")
        
        self.running = False
        self.made_shots = 0
        
        self.start_button = tk.Button(root, text="Start", font=("Helvetica", 24), command=self.start)
        self.start_button.pack(expand=True)
        
    def start(self):
        self.running = True
        self.start_button.pack_forget()
        
        self.description_label = tk.Label(self.root, text="Made Shots", font=("Helvetica", 48))
        self.description_label.pack(expand=True)
        self.made_shots_label = tk.Label(self.root, text=str(self.made_shots), font=("Helvetica", 48))
        self.made_shots_label.pack(expand=True)
        
        self.stop_button = tk.Button(self.root, text="Stop", font=("Helvetica", 18), command=self.stop)
        self.stop_button.pack(side=tk.LEFT, expand=True)
        
        self.quit_button = tk.Button(self.root, text="Quit", font=("Helvetica", 18), command=self.root.quit)
        self.quit_button.pack(side=tk.RIGHT, expand=True)

        """
        with c.AudioClassifier.create_from_options(c.options) as classifier:
            i = 0
            while self.running:
                if 'Bell' in c.classify_input_audio(classifier):
                    self.increase_made_shots()
        """
        self.classifier_instance = c.AudioClassifier.create_from_options(c.options)
        self.classify_audio()

    def classify_audio(self):
        if not self.running:
            self.classifier_instance.close()
            return
        if "Bell" in c.classify_input_audio(self.classifier_instance):
            self.increase_made_shots()
            time.sleep(2)
            self.root.after(100, self.classify_audio)
        else:
            time.sleep(0.5)
            self.root.after(0, self.classify_audio)
        
        print(c.classify_input_audio(self.classifier_instance))

    
    def increase_made_shots(self):
        self.made_shots += 1
        self.made_shots_label.config(text=str(self.made_shots))

    def stop(self):
        self.running = False
        self.made_shots_label.pack_forget()
        self.description_label.pack_forget()
        self.stop_button.pack_forget()
        self.quit_button.pack_forget()
        self.start_button.pack(expand=True)

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-topmost", True)
        self.root.minsize(400, 400)
        self.app = BellAudioClassifierUI(self.root)
    
    def run(self):
        self.root.mainloop()

app = App()
c = Classifier(app)
