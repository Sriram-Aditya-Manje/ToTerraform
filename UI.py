import tkinter as tk
from tkinter import filedialog, Text, Scrollbar, messagebox
import json
from main import *



def open_file():
    """Handles file upload and opens a new window to display JSON content."""
    # file_path = filedialog.askopenfilename(
    #     filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
    # )
    file_path = "C:/Users/dell/Desktop/test.json"
    if not file_path:
        return  # User canceled the dialog

    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            parameters = extract_parameters(data)
            show_json_window(parameters)
    except json.JSONDecodeError:
        messagebox.showerror("Error", "Invalid JSON file.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def show_json_window(json_data):
    """Opens a new window to display the JSON content."""
    json_window = tk.Toplevel(root)
    json_window.title("ARM Template Viewer")
    json_window.geometry("800x600")

    # Add a Text widget with a Scrollbar for displaying JSON
    text_frame = tk.Frame(json_window)
    text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    scrollbar = Scrollbar(text_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_widget = Text(text_frame, wrap=tk.NONE, yscrollcommand=scrollbar.set, bg="#f5f5f5")
    text_widget.pack(fill=tk.BOTH, expand=True)

    scrollbar.config(command=text_widget.yview)

    # Insert the formatted JSON content
    text_widget.insert(tk.END, json.dumps(json_data, indent=4))
    text_widget.config(state=tk.DISABLED)  # Make the content read-only

# Create the main Tkinter window
root = tk.Tk()
root.title("Parameters Converter")

# Configure the initial popup size
root.geometry("300x150")

# Add a label and button in the popup
frame = tk.Frame(root)
frame.pack(expand=True)

upload_button = tk.Button(frame, text="Upload ARM Template", command=open_file, width=20)
upload_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
