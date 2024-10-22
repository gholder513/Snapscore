import keyboard

def on_key_event(e):
    print(f'Key {e.name} {"pressed" if e.event_type == "down" else "released"}')
    if e.name == "enter" and e.event_type == "down":
        print("Enter key pressed")
    if e.name == "esc" and e.event_type == "down":
        quit()

keyboard.hook(on_key_event)
keyboard.wait()  # Wait for a key event to stop the listener
