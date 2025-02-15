import customtkinter as ctk
from classifier import start_classifier_thread
from basketball2 import start_dribbling_thread
import time
import threading
from datetime import datetime, timedelta

class ModeHandler:      
    def __init__(self):
        self.current_mode = "count"
        self.challenge_difficulty = "easy"
        self.custom_time = 120
        self.custom_goal = 30
        self.target = 0
        self.time_limit = 0
        self.start_time = None
        self.paused = False
        self.challenge_active = False


class BellAudioClassifierUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Basketball Training Assistant")
        self.mode = ModeHandler()
        
        self.running = False

        self.made_shots = 0
        self.var = ctk.StringVar()
        self.var.set(str(self.made_shots))

        self.dribblings = 0
        self.var_dribblings = ctk.StringVar()
        self.var_dribblings.set(str(self.dribblings))

        # Initialize widgets here
        self.made_shots_label = None
        self.description_label = None
        self.dribbling_label = None
        self.dribbling_counter_label = None
        self.stop_button = None
        self.quit_button = None
        
        self.main_frame = ctk.CTkFrame(root)
        self.main_frame.pack(fill="both", expand=True)

        self.start_btn = ctk.CTkButton(self.main_frame, 
                                      text="Start Training", 
                                      state="disabled",
                                      command=self.start_training)
        
        self.show_start_page()
        
    def show_start_page(self):
        # Clear existing widgets
        for widget in self.main_frame.winfo_children():
            if widget != self.start_btn:  # Do not destroy self.start_btn
                widget.destroy()

        # Start Page Layout
        self.start_frame = ctk.CTkFrame(self.main_frame)
        self.start_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Mode Selection
        ctk.CTkLabel(self.start_frame, text="Select Mode", font=("Helvetica", 24)).pack(pady=10)
        
        self.mode_selector = ctk.CTkSegmentedButton(self.start_frame, 
                                                   values=["Count Mode", "Challenge Mode"],
                                                   command=self.update_mode_options)
        self.mode_selector.pack(pady=10)
        self.mode_selector.set("Count Mode")

        # Mode Options Container
        self.mode_options_frame = ctk.CTkFrame(self.start_frame)
        self.mode_options_frame.pack(pady=20)

        # Count Mode Options
        self.count_mode_options()
        
        # Start Button
        if not hasattr(self, 'start_btn') or not self.start_btn.winfo_exists():
            self.start_btn = ctk.CTkButton(self.start_frame, 
                                  text="Start Training", 
                                  state="disabled",
                                  command=self.start_training)
        self.start_btn.pack(pady=20)

        # Close Button
        ctk.CTkButton(self.start_frame, 
                     text="Close", 
                     command=self.root.quit).pack(side="bottom", pady=10)

    def update_mode_options(self, selected_mode):
        if selected_mode == "Count Mode":
            self.count_mode_options()
            self.mode.current_mode = "count"
        else:
            self.challenge_mode_options()
            self.mode.current_mode = "challenge"

    def count_mode_options(self):
        # Clear previous options
        for widget in self.mode_options_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.mode_options_frame, text="Count Settings").pack()
        
        """
        # Timer Checkbox
        self.timer_var = ctk.BooleanVar()
        ctk.CTkCheckBox(self.mode_options_frame, 
                       text="Enable Timer", 
                       variable=self.timer_var).pack(pady=5)
        """
        
        # Target Selection
        self.target_var = ctk.StringVar(value="both")
        ctk.CTkLabel(self.mode_options_frame, text="Count:").pack()
        ctk.CTkRadioButton(self.mode_options_frame, 
                          text="Shots Only", 
                          variable=self.target_var, 
                          value="shots").pack()
        ctk.CTkRadioButton(self.mode_options_frame, 
                          text="Dribbles Only", 
                          variable=self.target_var, 
                          value="dribbles").pack()
        ctk.CTkRadioButton(self.mode_options_frame, 
                          text="Both", 
                          variable=self.target_var, 
                          value="both").pack()

        self.start_btn.configure(state="normal")

    def challenge_mode_options(self):
        for widget in self.mode_options_frame.winfo_children():
            widget.destroy()

        # Difficulty Selection
        ctk.CTkLabel(self.mode_options_frame, text="Select Difficulty").pack()
        
        self.diff_var = ctk.StringVar(value="easy")
        difficulties = [
            ("Easy: 30s/30d or 2m/5s", "easy"),
            ("Hard: 1m/120d or 2m/10s", "hard"),
            ("Custom", "custom")
        ]
        
        for text, value in difficulties:
            ctk.CTkRadioButton(self.mode_options_frame,
                              text=text,
                              variable=self.diff_var,
                              value=value).pack(anchor="w", pady=2)
        
        # Custom Settings
        self.custom_frame = ctk.CTkFrame(self.mode_options_frame)
        self.custom_frame.pack(pady=10, fill="x")
        
        ctk.CTkLabel(self.custom_frame, text="Time (sec):").grid(row=0, column=0, padx=5)
        self.time_entry = ctk.CTkEntry(self.custom_frame, width=80)
        self.time_entry.grid(row=0, column=1, padx=5)
        
        ctk.CTkLabel(self.custom_frame, text="Goal:").grid(row=0, column=2, padx=5)
        self.goal_entry = ctk.CTkEntry(self.custom_frame, width=80)
        self.goal_entry.grid(row=0, column=3, padx=5)

        ctk.CTkLabel(self.mode_options_frame, text="Select Target for Challenge", font=("Helvetica", 18)).pack(pady=5)
        self.challenge_target_var = ctk.StringVar(value="dribbles")  # Default selection
        ctk.CTkRadioButton(self.mode_options_frame,
                        text="Shots Only",
                        variable=self.challenge_target_var,
                        value="shots").pack(anchor="w", pady=2)
        ctk.CTkRadioButton(self.mode_options_frame,
                        text="Dribbles Only",
                        variable=self.challenge_target_var,
                        value="dribbles").pack(anchor="w", pady=2)
        
        self.diff_var.trace_add("write", self.validate_challenge_settings)

    def validate_challenge_settings(self, *args):
        if self.diff_var.get() == "custom":
            self.start_btn.configure(state="disabled")  # Start disabled

            time_input = self.time_entry.get().strip()
            goal_input = self.goal_entry.get().strip()

            if time_input.isdigit() and goal_input.isdigit():
                time = int(time_input)
                goal = int(goal_input)

                if 0 < time <= 120 and 0 < goal <= 500:
                    self.start_btn.configure(state="normal")  # Enable only if valid
        else:
            self.start_btn.configure(state="normal")


    def start_training(self):
        self.running = True
        if hasattr(self, 'start_btn') and self.start_btn.winfo_exists():
            self.start_btn.pack_forget() 
        self.setup_training_parameters()
        self.show_run_page()

    def setup_training_parameters(self):
        if self.mode.current_mode == "challenge":
            diff = self.diff_var.get()

            challange_target = self.challenge_target_var.get()
            if diff == "easy":
                self.mode.time_limit = 30 if challange_target == "dribbles" else 120
                self.mode.target = 30 if challange_target == "dribbles" else 5
            elif diff == "hard":
                self.mode.time_limit = 60 if challange_target == "dribbles" else 120
                self.mode.target = 120 if challange_target == "dribbles" else 10
            else:
                self.mode.time_limit = int(self.time_entry.get())
                self.mode.target = int(self.goal_entry.get())

    def show_run_page(self):
        # Clear start page
        self.start_frame.destroy()
        
        # Run Page Layout
        self.run_frame = ctk.CTkFrame(self.main_frame)
        self.run_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        ctk.CTkLabel(self.run_frame, 
                    text="Count Mode" if self.mode.current_mode == "count" else "Challenge Mode",
                    font=("Helvetica", 24, "bold")).pack(pady=10)
        
        # Main Content
        if self.mode.current_mode == "count":
            self.build_count_mode_ui()
            
        else:
            self.build_challenge_mode_ui()
        
        # Control Buttons
        self.build_control_buttons()

    def build_control_buttons(self):
        btn_frame = ctk.CTkFrame(self.run_frame)
        btn_frame.pack(side="bottom", pady=20)
        
        # Back Button
        ctk.CTkButton(btn_frame,
                     text="Back to Main",
                     command=self.stop).pack(side="right", padx=10)

    def build_count_mode_ui(self):
        self.root.after(500, self.start_classifier)
        # Timer Display
        self.timer_var = ctk.StringVar(value="00:00:00")
        ctk.CTkLabel(self.run_frame, 
                    textvariable=self.timer_var,
                    font=("Helvetica", 20)).pack(pady=10)

         # Start the timer
        self.start_time = datetime.now()
        self.update_timer()

        # Counters
        counters_frame = ctk.CTkFrame(self.run_frame)
        counters_frame.pack(pady=20)
        
        if self.target_var.get() in ["shots", "both"]:
            ctk.CTkLabel(counters_frame, text="Shots", font=("Helvetica", 18)).grid(row=0, column=0, padx=20)
            self.made_shots_label = ctk.CTkLabel(counters_frame, textvariable = self.var, font=("Helvetica", 24))
            self.made_shots_label.grid(row=1, column=0, padx=20)
        
        if self.target_var.get() in ["dribbles", "both"]:
            ctk.CTkLabel(counters_frame, text="Dribbles", font=("Helvetica", 18)).grid(row=0, column=1, padx=20)
            self.dribbles_label = ctk.CTkLabel(counters_frame, textvariable=self.var_dribblings, font=("Helvetica", 24))
            self.dribbles_label.grid(row=1, column=1, padx=20)

    
    def update_timer(self):
        if self.running:
            elapsed = datetime.now() - self.start_time
            self.timer_var.set(str(elapsed).split(".")[0])  # Format as HH:MM:SS
            self.root.after(1000, self.update_timer)  # Update every second

    def build_challenge_mode_ui(self):

        challenge_frame = ctk.CTkFrame(self.run_frame)
        challenge_frame.pack(pady=20)
        
        # Goal Display
        ctk.CTkLabel(challenge_frame, text="Goal", font=("Helvetica", 18)).grid(row=0, column=0, padx=20)
        self.goal_label = ctk.CTkLabel(challenge_frame, 
                                      text=str(self.mode.target),
                                      font=("Helvetica", 24))
        self.goal_label.grid(row=1, column=0, padx=20)
        
        # Timer Display
        ctk.CTkLabel(challenge_frame, text="Time Left", font=("Helvetica", 18)).grid(row=0, column=1, padx=20)
        self.time_left_label = ctk.CTkLabel(challenge_frame, 
                                           text=str(timedelta(seconds=self.mode.time_limit)),
                                           font=("Helvetica", 24))
        self.time_left_label.grid(row=1, column=1, padx=20)

        if self.challenge_target_var.get() == "shots":
            ctk.CTkLabel(challenge_frame, text="Shots", font=("Helvetica", 18)).grid(row=2, column=0, padx=20, pady=10)
            self.made_shots_label = ctk.CTkLabel(challenge_frame, textvariable = self.var, font=("Helvetica", 24))
            self.made_shots_label.grid(row=3, column=0, padx=20)
        
        else: #dribbles
            ctk.CTkLabel(challenge_frame, text="Dribbles", font=("Helvetica", 18)).grid(row=2, column=1, padx=20, pady=10)
            self.dribbles_label = ctk.CTkLabel(challenge_frame, textvariable=self.var_dribblings, font=("Helvetica", 24))
            self.dribbles_label.grid(row=3, column=1, padx=20)
        
        # Start/Restart Button
        self.start_challenge_btn = ctk.CTkButton(challenge_frame, 
                                                text="Start Countdown",
                                                command=self.start_challenge)
        self.start_challenge_btn.grid(row=4, columnspan=2, pady=10)


    def start_challenge(self):
        self.mode.challenge_active = True
        self.start_challenge_btn.configure(text="3...", state="disabled")
        self.root.after(1000, lambda: self.start_challenge_btn.configure(text="2..."))
        self.root.after(2000, lambda: self.start_challenge_btn.configure(text="1..."))
        self.root.after(3000, self.begin_challenge)

    def begin_challenge(self):
        self.running = True
        self.mode.start_time = datetime.now()
        self.start_challenge_btn.configure(text="Restart", state="normal")
        self.start_classifier()
        self.update_challenge_timer()

    def update_challenge_timer(self):
        if self.mode.challenge_active:
            elapsed = datetime.now() - self.mode.start_time 
            remaining = self.mode.time_limit - elapsed.seconds
            self.time_left_label.configure(text=str(timedelta(seconds=remaining)))
            
            if remaining <= 0:
                self.end_challenge()
            else:
                self.root.after(1000, self.update_challenge_timer) # Update every second

    def end_challenge(self):
        self.mode.challenge_active = False
        if self.made_shots >= self.mode.target or self.dribblings >= self.mode.target:            
            self.time_left_label.configure(text_color="green")

        else:
            self.time_left_label.configure(text_color="red")
    """
    def refresh_counts(self):
        if self.target_var.get() in ["shots", "both"]:
            self.shots_label.configure(text=str(self.made_shots))
        if self.target_var.get() in ["dribbles", "both"]:
            self.dribbles_label.configure(text=str(self.dribblings))



    def check_challenge_status(self):
        if self.mode.challenge_active:
            remaining = self.mode.time_limit - (datetime.now() - self.mode.start_time).seconds
            self.time_left_label.configure(text=str(timedelta(seconds=remaining)))
            
            if remaining <= 0:
                self.end_challenge()
            else:
                self.root.after(1000, self.check_challenge_status)

    """
        
    def start_classifier(self):
        # Determine which mode is selected: "shots", "dribbles", or "both"
        # (Assuming that self.target_var is a StringVar set in count_mode_options)
        if self.mode.current_mode == "count":
            target = self.target_var.get() if hasattr(self, "target_var") else "both"
        else:
            target = self.challenge_target_var.get()
        
        if target == "shots":
            print("Starting bell classifier thread only...")
            start_classifier_thread(self)
        elif target == "dribbles":
            print("Starting dribbling classifier thread only...")
            start_dribbling_thread(self)
        elif target == "both":
            print("Starting both classifier threads...")
            start_classifier_thread(self)
            start_dribbling_thread(self)
        else:
            print("No valid target selected, defaulting to both threads.")
            start_classifier_thread(self)
            start_dribbling_thread(self)
        
        # Start the listener thread regardless
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
        self.running = False
        for widget in self.main_frame.winfo_children():
            widget.destroy()  
        """
        # Check if widgets exist before calling pack_forget
        if hasattr(self, 'made_shots_label') and self.made_shots_label:
            self.made_shots_label.pack_forget()
        if hasattr(self, 'description_label') and self.description_label:
            self.description_label.pack_forget()
        if hasattr(self, 'dribbling_label') and self.dribbling_label:
            self.dribbling_label.pack_forget()
        if hasattr(self, 'dribbling_counter_label') and self.dribbling_counter_label:
            self.dribbling_counter_label.pack_forget()
        if hasattr(self, 'stop_button') and self.stop_button:
            self.stop_button.pack_forget()
        if hasattr(self, 'quit_button') and self.quit_button:
            self.quit_button.pack_forget()
        """
        
        if hasattr(self, 'start_btn') and self.start_btn.winfo_exists():
            self.start_btn.destroy()
        
        self.start_btn = ctk.CTkButton(self.main_frame, 
                                    text="Start Training", 
                                    state="disabled",
                                    command=self.start_training)
        self.start_btn.pack(side = "bottom", expand=True, padx=20, pady=20)
        
        
        self.made_shots = 0
        self.var.set(str(self.made_shots))
        self.dribblings = 0
        self.var_dribblings.set(str(self.dribblings))
        self.show_start_page()

    def quit(self):
        self.running = False
        self.root.quit()

class App:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.attributes("-topmost", True)
        self.root.minsize(400, 400)
        self.app = BellAudioClassifierUI(self.root)
    
    def run(self):
        self.root.focus()
        self.root.mainloop()

class ListenerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.app = app

    def run(self):
        print("Listener Thread started.")
        while self.app.running:
            self.app.refresh_made_shots()
            self.app.refresh_dribblings()
            time.sleep(1) 

# Set customtkinter appearance mode and color theme
ctk.set_appearance_mode("Dark")  # Options: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

app = App()
