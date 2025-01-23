import tkinter as tk
from app import BellAudioClassifierWebUI

class BellAudioClassifierUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bell Audio Classifier")
        
        self.running = BellAudioClassifierUI.running
        self.made_shots = BellAudioClassifierUI.made_shots
        
        self.start_button = tk.Button(root, text="Start", font=("Helvetica", 24), command=self.start)
        self.start_button.pack(expand=True)
        
    def start(self):
        self.running = True
        self.start_button.pack_forget()
        
        self.made_shots_label = tk.Label(self.root, text=str(self.made_shots), font=("Helvetica", 48))
        self.made_shots_label.pack(expand=True)
        
        self.stop_button = tk.Button(self.root, text="Stop", font=("Helvetica", 18), command=self.stop)
        self.stop_button.pack(side=tk.LEFT, expand=True)
        
        self.quit_button = tk.Button(self.root, text="Quit", font=("Helvetica", 18), command=self.root.quit)
        self.quit_button.pack(side=tk.RIGHT, expand=True)
        
    def stop(self):
        self.running = False
        self.made_shots_label.pack_forget()
        self.stop_button.pack_forget()
        self.quit_button.pack_forget()
        self.start_button.pack(expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = BellAudioClassifierUI(root)
    root.mainloop()