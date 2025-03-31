import os
import datetime
import subprocess
import sys
import requests
from tkinter import messagebox

# Function to check and install required modules
def install_and_import(package):
    try:
        __import__(package)
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"{package} installed successfully.")

# Ensure customtkinter is installed
install_and_import("customtkinter")
install_and_import("requests")

import customtkinter as ctk

# Set up main application window
ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("CardSaverV2 - By qrexotwy")
app.geometry("400x325")

# CardSaver directory setup
card_saver_hub = os.path.join(os.path.expanduser("~"), "Downloads", "CardSaverV2-HUB")
card_saver_info = os.path.join(card_saver_hub, "CardSaverInfo")
os.makedirs(card_saver_hub, exist_ok=True)
os.makedirs(card_saver_info, exist_ok=True)

changelog_path = os.path.join(card_saver_info, "changelog.txt")

# Fetch changelog from GitHub
def fetch_changelog():
    url = "https://raw.githubusercontent.com/qrexotwy/CardSaverV2/main/Changelog/Changelog.txt"
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(changelog_path, "w") as log:
            log.write(response.text)
        print("Changelog updated successfully.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch changelog: {e}")

# Update changelog on startup
fetch_changelog()

# Input fields
labels = ["Card Type", "Card Number", "Card Holder's Name", "Expiration Date (MM/YYYY)", "Security Code"]
entries = {}

for label in labels:
    frame = ctk.CTkFrame(app)
    frame.pack(pady=5, fill='x', padx=20)
    ctk.CTkLabel(frame, text=label).pack(side="left", padx=10)
    entry = ctk.CTkEntry(frame)
    entry.pack(side="right", fill='x', expand=True, padx=10)
    entries[label] = entry

# File name entry
file_frame = ctk.CTkFrame(app)
file_frame.pack(pady=10, fill='x', padx=20)
ctk.CTkLabel(file_frame, text="File Name (without .txt)").pack(side="left", padx=10)
file_entry = ctk.CTkEntry(file_frame)
file_entry.pack(side="right", fill='x', expand=True, padx=10)

def save_details():
    file_name = file_entry.get().strip()
    if not file_name:
        messagebox.showerror("Error", "Please enter a file name!")
        return
    
    file_path = os.path.join(card_saver_hub, f"{file_name}.txt")
    
    # Get current date and time
    formatted_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Save data to file
    with open(file_path, "w") as f:
        for label, entry in entries.items():
            f.write(f"{label}: {entry.get()}\n")
        f.write("\nMade By: CardSaverV2\n")
        f.write("CardSaverV2 Author: @qrexotwy\n")
        f.write(f"Created On: {formatted_date}\n")
    
    # Clear all input fields
    for entry in entries.values():
        entry.delete(0, 'end')
    file_entry.delete(0, 'end')
    
    messagebox.showinfo("Success", f"Responses saved successfully in {file_path}")

# Save button
save_button = ctk.CTkButton(app, text="Save Details", command=save_details)
save_button.pack(pady=20)

app.mainloop()
