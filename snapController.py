import pyautogui
import tkinter as tk
from tkinter import ttk
import webbrowser
import time
import threading
import configparser
import os
import keyboard
import sys

version = "2.5"

config = configparser.ConfigParser()

targetSnapValue = 0


file_path = "Config.ini"
check_file = os.path.isfile(file_path)
Full_path = os.path.abspath(file_path)

if check_file:
    print("[UPDATE] File Exists At Path: %s" % Full_path)
else:
    print("[WARNING] Config File Not Found. Creating Now...")
    config.add_section('HotKeys')
    config.set('HotKeys', 'record', 'f')
    config.set('HotKeys', 'start', 'r')
    config.set('HotKeys', 'stop', 'd')

    time.sleep(1)

    print("[UPDATE] Config File Created At: %s" % Full_path)

    with open(file_path, "w+") as ConfigFile:
        config.write(ConfigFile)

config.read(file_path)
HotKeyOBJ = config["HotKeys"]
RecordHotkey = HotKeyOBJ["record"]
StartHotkey = HotKeyOBJ["start"]
StopHotkey = HotKeyOBJ["stop"]

class SnapBot:
    def __init__(self):
        self.running = False
        self.recording = False  # Track if recording mode is on
        self.click_positions = []
        self.delay = 0.1  # Default delay of 0.1 seconds
        self.auto_clicker_thread = None
        self.recording_thread = None  # Thread for global mouse click recording

    def start_auto_clicker_thread(self, numOfIterations):
        self.auto_clicker_thread = threading.Thread(target=self.start, args=(numOfIterations,))
        self.auto_clicker_thread.start()

    def start(self, numOfIterations):
        self.running = True
        # If the user specifies the number of iterations, then run the auto-clicker that many times
        if numOfIterations != 0:
            print(f"[INFO] Running auto-clicker for {numOfIterations} iterations...")
            for i in range(numOfIterations):
                for pos in self.click_positions:
                    pyautogui.moveTo(pos)
                    pyautogui.click(pos)
                    time.sleep(self.delay)
                    if not self.running:
                        break
        # If the user doesn't specify the number of iterations, then run the auto-clicker indefinitely
        else:
            while self.running:
                for pos in self.click_positions:
                    pyautogui.moveTo(pos)
                    pyautogui.click(pos)
                    time.sleep(self.delay)
                    if not self.running:
                        break

    def stop(self):
        self.running = False
        if self.auto_clicker_thread and self.auto_clicker_thread.is_alive():
            self.auto_clicker_thread.join()

    def toggle_recording(self):
        if not self.recording:
            self.recording = True
            print("[INFO] Now recording mouse clicks globally...")
            self.start_recording_thread()
        else:
            self.recording = False
            print("[INFO] Stopped recording mouse clicks globally...")

    def start_recording_thread(self):
        self.recording_thread = threading.Thread(target=self.record_global_clicks)
        self.recording_thread.start()

    def record_global_clicks(self):
                pos = pyautogui.position()  # Get the current global mouse position
                self.click_positions.append(pos)
                update_positions_text()
                
class Link(tk.Label):
    def __init__(self, master=None, link=None, fg='grey', font=('Arial', 10), *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.default_color = fg
        self.color = 'blue'
        self.default_font = font
        self.link = link

        self['fg'] = fg
        self['font'] = font 

        self.bind('<Enter>', self._mouse_on)
        self.bind('<Leave>', self._mouse_out)
        self.bind('<Button-1>', self._callback)

    def _mouse_on(self, *args):
        self['fg'] = self.color
        self['font'] = self.default_font + ('underline', )

    def _mouse_out(self, *args):
        self['fg'] = self.default_color
        self['font'] = self.default_font

    def _callback(self, *args):
        webbrowser.open_new(self.link)

auto_clicker = SnapBot()

def on_key_event(e):
    key_name = e.name if e.name else e.scan_code  # Use scan code if name is None
    print(f'Key {e.name} {"pressed" if e.event_type == "down" else "released"}')
    if key_name == "enter" and e.event_type == "down":
        print("Toggling Mouse Clicks")
        auto_clicker.record_global_clicks()
    # if the character is escape, then stop the auto-clicker
    if key_name == "escape" and e.event_type == "down":
        print("Stopping Auto-Clicker")
        stop_auto_clicker()
    if key_name == "space" and e.event_type == "down":
        print("Running Auto-Clicker")
        start_stop_auto_clicker()
    if key_name == "ctrl" and e.event_type == "down":
        print("Quitting")
        root.quit()  # Stop the Tkinter loop
        sys.exit(1)  # Exit the program
keyboard.hook(on_key_event)

def toggle_auto_clicker():
    if not auto_clicker.recording:
        auto_clicker.toggle_recording()
    else:
        auto_clicker.toggle_recording()

def start_stop_auto_clicker():
    if not auto_clicker.running:
        if auto_clicker.click_positions:
            try:
                numOfIterations = int(targetSnapValue)  # Convert to integer
                auto_clicker.start_auto_clicker_thread(numOfIterations)
            except ValueError:
                print("[ERROR] Please enter a valid number for the iterations.")
                print("Current iterations value: %s" % targetSnapValue)
        else:
            print("[WARNING] Please record at least one position before starting auto-clicker.")
    else:
        auto_clicker.stop()


def stop_auto_clicker():
    print("[UPDATE] Stop auto-clicker function called")
    auto_clicker.stop()

def update_positions_text():
    positions_text.delete(1.0, tk.END)
    for pos in auto_clicker.click_positions:
        positions_text.insert(tk.END, f"({pos[0]}, {pos[1]})\n")

def clear_positions():
    auto_clicker.click_positions = []
    update_positions_text()

def change_hotkeys_window():
    hotkeys_window = tk.Toplevel(root)
    hotkeys_window.title("Change Hotkeys")
    hotkeys_window.geometry("300x200")
    
    record_label = ttk.Label(hotkeys_window, text="")
    record_label.pack()

    record_button = ttk.Button(hotkeys_window, text=f"Change Record Key ({auto_clicker.hotkeys['record']})", command=lambda: change_hotkey('record', record_label))
    record_button.pack(pady=5)

    start_label = ttk.Label(hotkeys_window, text="")
    start_label.pack()

    start_button = ttk.Button(hotkeys_window, text=f"Change Start Key ({auto_clicker.hotkeys['start']})", command=lambda: change_hotkey('start', start_label))
    start_button.pack(pady=5)

    stop_label = ttk.Label(hotkeys_window, text="")
    stop_label.pack()

    stop_button = ttk.Button(hotkeys_window, text=f"Change Stop Key ({auto_clicker.hotkeys['stop']})", command=lambda: change_hotkey('stop', stop_label))
    stop_button.pack(pady=5)

def change_hotkey(action, label):
    print(f"[UPDATE] Change {action} hotkey function called")
    new_hotkey = input(f"Enter new hotkey for {action}: ")
    auto_clicker.hotkeys[action] = new_hotkey
    label.config(text=f"Edited: New hotkey for {action} is {new_hotkey}")
    config.set("HotKeys", action, new_hotkey)

    with open(file_path, "w") as ConfigFile:
        config.write(ConfigFile)

def change_delay(value):
    auto_clicker.delay = float(value)

root = tk.Tk()
root.title("SnapBot")
root.geometry("500x600")
root.configure(bg="#302e2e")

style = ttk.Style()
style.configure("TFrame", background="#302e2e")

frame = ttk.Frame(root, padding="20")
frame.pack(expand=True, fill=tk.BOTH)

# Create labels and entry widgets
label1 = tk.Label(root, text="How many snaps do you want?")
label1.pack()

entry1 = tk.Entry(root)
entry1.pack()

targetSnapValue = entry1.get()
# Function to save and clear the entry
def save_and_clear():
    global targetSnapValue 
    targetSnapValue = entry1.get()  # Save the value
    entry1.delete(0, tk.END)  # Clear the entry
    update_iterations_text()


def update_iterations_text():
    iterations_text.delete(1.0, tk.END)
    iterations_text.insert(tk.END, targetSnapValue)

# Create the button
clear_button = tk.Button(root, text="Save and Clear Entry", font=("Helvetica", 14), command=save_and_clear)
clear_button.pack(pady=20)

positions_label = ttk.Label(frame, text="Click positions:", font=("Arial", 12))
positions_label.grid(row=0, column=0, pady=5, padx=5)

positions_text = tk.Text(frame, height=10, width=20, font=("Arial", 10))
positions_text.grid(row=1, column=0, pady=5, padx=5)

record_button = ttk.Button(frame, text="Record Position (%s)" % RecordHotkey, command=toggle_auto_clicker)
record_button.grid(row=2, column=0, pady=5, padx=5)

start_stop_button = ttk.Button(frame, text="Start/Stop (%s)" % StartHotkey, command=start_stop_auto_clicker)
start_stop_button.grid(row=3, column=0, pady=5, padx=5)

stop_button = ttk.Button(frame, text="Stop (%s)" % StopHotkey, command=stop_auto_clicker)
stop_button.grid(row=4, column=0, pady=5, padx=5)

iterations_label = ttk.Label(frame, text="Number of Iterations:", font=("Arial", 12))
iterations_label.grid(row=0, column=1, pady=5, padx=5)
iterations_text = tk.Text(frame, height=10, width=20, font=("Arial", 10))
iterations_text.grid(row=1, column=1, pady=5, padx=5)

clear_button = ttk.Button(frame, text="Clear Positions", command=clear_positions)
clear_button.grid(row=5, column=0, pady=5, padx=5)

hotkeys_button = ttk.Button(frame, text="Change Hotkeys", command=change_hotkeys_window)
hotkeys_button.grid(row=7, column=0, pady=5, padx=5)

delay_label = ttk.Label(frame, text="Delay (seconds):", font=("Arial", 12))
delay_label.grid(row=8, column=0, pady=5, padx=5)

delay_slider = tk.Scale(frame, from_=0.1, to=3, resolution=0.1, orient=tk.HORIZONTAL, length=200, command=change_delay)
delay_slider.set(0.001)
delay_slider.grid(row=9, column=0, pady=5, padx=5)

root.mainloop()
