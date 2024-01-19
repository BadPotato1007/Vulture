import pynput
import time

def set_timer(seconds):
    print(f"Timer set for {seconds} seconds.")
    time.sleep(seconds)
    print("Timer expired!")

# Disable mouse and keyboard events
mouse_listener = pynput.mouse.Listener(suppress=True)
mouse_listener.start()
keyboard_listener = pynput.keyboard.Listener(suppress=True)
keyboard_listener.start()

# Set the timer for 5 seconds
set_timer(5)

# Enable mouse and keyboard events
mouse_listener.stop()
keyboard_listener.stop()