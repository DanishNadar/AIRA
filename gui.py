import tkinter as tk
from tkinter import scrolledtext
import time
import csv
import sys
import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()
event_log = []
rcgnz = sr.Recognizer()

# Redirects print statements to tkinter GUI
class RedirectText:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.yview(tk.END)

    def flush(self):
        pass

# Function to log any event with timestamp
def log_event(event_type, details):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    event_log.append([event_type, details, timestamp])
    update_gui(f"{event_type}: {details} at {timestamp}")

# Function to update the GUI with logs
def update_gui(text):
    text_display.insert(tk.END, f"{text}\n")
    text_display.yview(tk.END)

# Function to save the event log to CSV
def save_event_log():
    with open('event_log.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Event Type", "Details", "Timestamp"])
        for entry in event_log:
            writer.writerow(entry)
    update_gui("Event log saved to CSV.")

# Function to delete input text in real-time
def delete_text():
    text_display.delete(1.0, tk.END)  # Clears the text in the Text widget

# Function to clear the event log
def clear_log():
    event_log.clear()
    update_gui("Event log cleared.")

# Function to adjust the volume of pyttsx3 engine
def set_volume(value):
    volume = int(value) / 100  # Slider returns 0-100; pyttsx3 expects 0.0 to 1.0
    engine.setProperty('volume', volume)
    update_gui(f"Volume set to {value}%")

# Function to adjust the speech rate of pyttsx3
def set_speech_rate(value):
    rate = int(value)
    engine.setProperty('rate', rate)
    update_gui(f"Speech rate set to {value} words per minute")

# Function to change the voice type (male/female)
def change_voice(choice):
    voices = engine.getProperty('voices')
    if choice == "Male":
        engine.setProperty('voice', voices[0].id)  # Usually male
    else:
        engine.setProperty('voice', voices[1].id)  # Usually female
    update_gui(f"Voice changed to {choice}")

# Function to handle voice input and process commands
def process_input():
    update_gui("Listening for your command...")
    
    with sr.Microphone() as source:
        audio = rcgnz.listen(source)
        
    try:
        command = rcgnz.recognize_google(audio)
        update_gui(f"Input: {command}")  # Display the input in the GUI
        
        # Process the command and call corresponding functions
        if "move forward" in command:
            move_forward()
        elif "turn left" in command:
            turn_left()
        elif "extend arm" in command:
            extend_arm()
        else:
            update_gui("Command not recognized")
            
    except sr.UnknownValueError:
        update_gui("Sorry, I couldn't understand your input. Can you please repeat?")
    except sr.RequestError:
        update_gui("Sorry, there was an issue with the speech recognition service.")

# Function to activate listening when Start button is clicked
def start_listening():
    update_gui("Activating speech recognition...")
    process_input()

# Function to simulate robot actions (just examples)
def move_forward():
    update_gui("Moving forward")

def turn_left():
    update_gui("Turning left")

def extend_arm():
    update_gui("Extending arm")

# Tkinter GUI Setup
root = tk.Tk()
root.title("AIRA - Holographic Assistant")
root.geometry('900x700+200+200')  # Larger window
root.config(bg="#1e1e1e")
root.attributes('-alpha', 0.9)  # Slight transparency

# Create a Text widget for displaying text logs
text_display = tk.Text(root, width=80, height=12, wrap=tk.WORD, font=("Helvetica", 16), fg="#00FF00", bg="#1e1e1e", insertbackground="white", bd=0, relief=tk.FLAT)
text_display.pack(padx=10, pady=10)

# Redirect standard output to the Text widget
redirect_text = RedirectText(text_display)
sys.stdout = redirect_text

# Create buttons for clearing input and logs
clear_button = tk.Button(root, text="Clear Input", font=("Helvetica", 16), command=delete_text, bg="#333333", fg="white", relief=tk.FLAT, width=20, height=2)
clear_button.pack(pady=10)

save_button = tk.Button(root, text="Save Log", font=("Helvetica", 16), command=save_event_log, bg="#333333", fg="white", relief=tk.FLAT, width=20, height=2)
save_button.pack(pady=10)

clear_log_button = tk.Button(root, text="Clear Log", font=("Helvetica", 16), command=clear_log, bg="#333333", fg="white", relief=tk.FLAT, width=20, height=2)
clear_log_button.pack(pady=10)

# Create a Start button to activate voice recognition
start_button = tk.Button(root, text="Start", font=("Helvetica", 20), command=start_listening, bg="#4CAF50", fg="white", relief=tk.FLAT, width=20, height=3)
start_button.pack(pady=20)

# Volume slider
volume_label = tk.Label(root, text="Volume", font=("Helvetica", 16), fg="white", bg="#1e1e1e")
volume_label.pack(pady=10)

volume_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, font=("Helvetica", 14), fg="white", bg="#333333", command=set_volume)
volume_slider.set(50)
volume_slider.pack(pady=10)

# Speech rate slider
rate_label = tk.Label(root, text="Speech Rate", font=("Helvetica", 16), fg="white", bg="#1e1e1e")
rate_label.pack(pady=10)

rate_slider = tk.Scale(root, from_=100, to=250, orient=tk.HORIZONTAL, font=("Helvetica", 14), fg="white", bg="#333333", command=set_speech_rate)
rate_slider.set(150)
rate_slider.pack(pady=10)

# Dropdown menu for voice selection
mode_label = tk.Label(root, text="Select Voice", font=("Helvetica", 16), fg="white", bg="#1e1e1e")
mode_label.pack(pady=10)

voice_var = tk.StringVar()
voice_var.set("Male")
voice_dropdown = tk.OptionMenu(root, voice_var, "Male", "Female", command=change_voice)
voice_dropdown.config(font=("Helvetica", 16), fg="white", bg="#333333", relief=tk.FLAT)
voice_dropdown.pack(pady=10)

# Function to run the GUI in the main thread
def run_gui():
    root.mainloop()

