# commands.py
import gui  # Import the gui module to log events

# Example command function in commands.py
def move_forward():
    # Function logic for moving forward
    gui.log_event('Function Call', 'move_forward')  # Log the function call

def access_some_file():
    # Simulate accessing a file (e.g., reading a file, processing data)
    gui.log_event('File Accessed', 'some_file.txt')  # Log the file access

