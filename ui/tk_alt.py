import tkinter as tk
from classifier import start_classifier_thread
from basketball2 import start_dribbling_thread
import time
import threading

class BellAudioClassifierUI:
    """
    A Tkinter-based user interface for controlling the audio classifier
    and displaying classification results.

    :param root: The root Tk window for the UI.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Bell Audio Classifier")
        
        self.running = False

        self.made_shots = 0
        self.var = tk.StringVar()
        self.var.set(str(self.made_shots))

        self.dribblings = 0
        self.var_dribblings = tk.StringVar()
        self.var_dribblings.set(str(self.dribblings))
        
        self.start_button = tk.Button(root, text="Start", font=("Helvetica", 24), command=self.start)
        self.start_button.pack(expand=True)
        
    def start(self):
        """
        Initializes and displays UI elements, then starts the classification process.
        """
        self.running = True
        self.start_button.pack_forget()
        
        self.description_label = tk.Label(self.root, text="Made Shots", font=("Helvetica", 48))
        self.description_label.pack(expand=True)
        self.made_shots_label = tk.Label(self.root, textvariable=self.var, font=("Helvetica", 48))
        self.made_shots_label.pack(expand=True)

        self.dribbling_label = tk.Label(self.root, text="Dribblings", font=("Helvetica", 48))
        self.dribbling_label.pack(expand=True)
        self.dribbling_counter_label = tk.Label(self.root, textvariable=self.var_dribblings, font=("Helvetica", 48))
        self.dribbling_counter_label.pack(expand=True)
        
        self.stop_button = tk.Button(self.root, text="Stop", font=("Helvetica", 18), command=self.stop)
        self.stop_button.pack(side=tk.LEFT, expand=True)
        
        self.quit_button = tk.Button(self.root, text="Quit", font=("Helvetica", 18), command=self.quit)
        self.quit_button.pack(side=tk.RIGHT, expand=True)


        self.root.after(500, self.start_classifier)
    
    def start_classifier(self):
        start_classifier_thread(self)
        start_dribbling_thread(self)
        listener = ListenerThread(self)
        listener.start()

    def increase_made_shots(self):
        """
        Increments the made_shots counter when a bell sound is detected.
        """
        self.made_shots += 1

    def increase_dribblings(self, dribblings = 1):
        """
        Increments the dribblings counter by a specified amount.

        :param dribblings: Number of dribbles to add.
        """
        self.dribblings += dribblings

    def refresh_made_shots(self):
        """
        Updates the displayed made_shots counter in the UI.
        """
        self.var.set(str(self.made_shots))
        self.root.update_idletasks()

    def refresh_dribblings(self):
        """
        Updates the displayed dribblings counter in the UI.
        """
        self.var_dribblings.set(str(self.dribblings))
        self.root.update_idletasks()

    def stop(self):
        """
        Stops the classification process, resets counters, and shows the start button again.
        """
        self.running = False
        self.made_shots_label.pack_forget()
        self.description_label.pack_forget()
        self.dribbling_label.pack_forget()
        self.dribbling_counter_label.pack_forget()
        self.stop_button.pack_forget()
        self.quit_button.pack_forget()
        self.start_button.pack(expand=True)
        self.made_shots = 0
        self.var.set(str(self.made_shots))
        self.dribblings = 0
        self.var_dribblings.set(str(self.dribblings))

    def quit(self):
        """
        Quits the application by terminating the Tkinter main loop.
        """
        self.running = False
        self.root.quit()

class App:
    """
    Manages the root window and initializes the BellAudioClassifierUI.
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-topmost", True)
        self.root.minsize(400, 400)
        self.app = BellAudioClassifierUI(self.root)
    
    def run(self):
        self.root.focus()
        self.root.mainloop()

class ListenerThread(threading.Thread):
    """
    Periodically refreshes the UI counters in a separate thread.
    """
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.app = app

    def run(self):
        """
        Continuously updates the made_shots and dribblings counters while the app is running.
        """
        print("Listener Thread started.")
        while self.app.running:
            self.app.refresh_made_shots()
            self.app.refresh_dribblings()
            time.sleep(1)

app = App()
