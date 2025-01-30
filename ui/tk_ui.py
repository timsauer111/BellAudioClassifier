import tkinter as tk
from classifier import Classifier
import time


class BellAudioClassifierUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bell Audio Classifier")
        
        self.running = False
        self.made_shots = 0
        self.var = tk.StringVar()
        self.var.set(str(self.made_shots))
        
        self.start_button = tk.Button(root, text="Start", font=("Helvetica", 24), command=self.start)
        self.start_button.pack(expand=True)
        
    def start(self):
        self.running = True
        self.start_button.pack_forget()
        
        self.description_label = tk.Label(self.root, text="Made Shots", font=("Helvetica", 48))
        self.description_label.pack(expand=True)
        self.made_shots_label = tk.Label(self.root, textvariable=self.var, font=("Helvetica", 48))
        self.made_shots_label.pack(expand=True)
        
        self.stop_button = tk.Button(self.root, text="Stop", font=("Helvetica", 18), command=self.stop)
        self.stop_button.pack(side=tk.LEFT, expand=True)
        
        self.quit_button = tk.Button(self.root, text="Quit", font=("Helvetica", 18), command=self.root.quit)
        self.quit_button.pack(side=tk.RIGHT, expand=True)

        self.root.after(500, self.start_classifier)

    def start_classifier(self):
        self.classifier_instance = c.AudioClassifier.create_from_options(c.options)
        self.classify_audio()

    def classify_audio(self):
        if not self.running:
            self.classifier_instance.close()
            return
        results = c.classify_input_audio(self.classifier_instance)
        if c.classfication_set.intersection(results):
            self.increase_made_shots()
            print(c.classify_input_audio(self.classifier_instance))
            self.root.after(2000, self.classify_audio)
        else:
            print(c.classify_input_audio(self.classifier_instance))
            self.root.after(0, self.classify_audio)
        

    
    def increase_made_shots(self):
        self.made_shots += 1
        self.var.set(str(self.made_shots))
        #self.made_shots_label.config(text=str(self.made_shots))
        self.root.update_idletasks()

    def stop(self):
        self.running = False
        self.made_shots_label.pack_forget()
        self.description_label.pack_forget()
        self.stop_button.pack_forget()
        self.quit_button.pack_forget()
        self.start_button.pack(expand=True)
        self.made_shots = 0
        self.var.set(str(self.made_shots))

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-topmost", True)
        self.root.minsize(400, 400)
        self.app = BellAudioClassifierUI(self.root)
    
    def run(self):
        self.root.focus()
        self.root.mainloop()

app = App()
c = Classifier(app)
