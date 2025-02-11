# main.py
import pyttsx3
import speech_recognition as sr
import time
import gui  # Import the tkinter application
import commands  # Import commands from commands.py
import web_commands  # Import commands from web_commands.py

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Initialize speech recognition
rcgnz = sr.Recognizer()

# Function to speak a message
def speak(message):
    engine.say(message)
    engine.runAndWait()
    gui.log_event('Function Call', 'speak')  # Log the function call
    gui.update_gui(f"Output: {message}")  # Display the output in the GUI

# Function to simulate robot actions (just examples, you can add more)
def move_forward():
    speak("Moving forward")
    gui.log_event('Function Call', 'move_forward')  # Log the function call

def turn_left():
    speak("Turning left")
    gui.log_event('Function Call', 'turn_left')  # Log the function call

def extend_arm():
    speak("Extending arm")
    gui.log_event('Function Call', 'extend_arm')  # Log the function call

# Function to handle voice input and process commands
def process_input():
    speak("Listening for your command...")
    
    with sr.Microphone() as source:
        audio = rcgnz.listen(source)
        
    try:
        command = rcgnz.recognize_google(audio)
        gui.update_gui(f"Input: {command}")  # Display the input in the GUI
        
        # Log the command being processed
        gui.log_event('Command Accessed', command)
        
        # Process the command and call corresponding functions
        if "move forward" in command:
            move_forward()
        elif "turn left" in command:
            turn_left()
        elif "extend arm" in command:
            extend_arm()
        else:
            speak("Command not recognized")
            
    except sr.UnknownValueError:
        speak("Sorry, I couldn't understand your input. Can you please repeat?")
    except sr.RequestError:
        speak("Sorry, there was an issue with the speech recognition service.")

# Start the Tkinter GUI directly in the main thread
gui.run_gui()

# Main loop that processes voice input
while True:
    process_input()
    time.sleep(1)  # Add a small delay to simulate periodic listening

