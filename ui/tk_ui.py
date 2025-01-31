import tkinter as tk
from classifier import start_classifier_thread
import time
import threading

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
        start_classifier_thread(self)
        listener = ListenerThread(self)
        listener.start()
    
    def increase_made_shots(self):
        self.made_shots += 1

    def refresh_made_shots(self):
        self.var.set(str(self.made_shots))
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

"""
class RunnerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.app = app
        self.target = self.run_app

    def run_app(self):
        print("Running app")
        self.app.run()
"""
class ListenerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.app = app
        self.target = self.setup_ui

    def setup_ui(self):
        while self.app.running:
            self.app.refresh_made_shots()
            time.sleep(1)

app = App()
