import asyncio
import os
from dotenv import load_dotenv

def send_message(msg):
    import discord
    load_dotenv()
    TOKEN = os.getenv('DISCORD_TOKEN')
    GUILD = os.getenv('DISCORD_GUILD')
    CHANNEL = os.getenv('DISCORD_CHANNEL')

    client = discord.Client()

    @client.event
    async def on_ready():
        for guild in client.guilds:
            if guild.name == GUILD:
                break
        for channel in guild.channels:
            if channel.name == CHANNEL:
                break

        await channel.send(msg)
        print(f'{channel.name} (id: {channel.id})')
        print(f'{client.user} has connected to Discord!')
        print(f'{guild.name} (id: {guild.id})')
        await client.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(client.start(TOKEN))
