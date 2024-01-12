import os

import discord

TOKEN = "MTE5NTMzMTE1NzEwNjEwMjMzNA.G0raSP.WlOJM84SPuuDo9RTgHP1BVts_rn7FymiVTVtjo"

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

    if message.content.startswith('11'):
        await message.channel.send('Hello!')
        print("Hello")
        os.system("python main.py")

client.run(TOKEN)