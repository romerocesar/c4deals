import os
import logging

import discord

logging.basicConfig(level=logging.DEBUG)


BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
TARGET_USER = os.getenv('DISCORD_USER')

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    user = await client.fetch_user(TARGET_USER)
    deal = 'fake test deal! it sucks... '
    await user.send(f'do you approve this {deal=}')

client.run(BOT_TOKEN)
