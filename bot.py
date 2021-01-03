import os
import requests

import discord
from dotenv import load_dotenv
from mongo_conn import db

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GUILD = os.getenv('DISCORD_GUILD_NAME')

GS_KEY = os.getenv('GOOGLE_CUSTOM_SEARCH_KEY')
GS_SE_ID = os.getenv('GOOGLE_PROG_SE_ID')
GS_URL = "https://www.googleapis.com/customsearch/v1?q={}&key={}&cx={}"

client = discord.Client()


@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(f"{client.user} is connected to following guild: ")
    print(f"{guild.name}(id: {guild.id})")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == "hi":
        await message.channel.send("what do you say to the god of death?")

    if message.content.startswith("!google"):
        msg = message.content[8:].strip()
        resp = requests.get(GS_URL.format(msg, GS_KEY, GS_SE_ID))
        response_list = [
            discord.Embed(title=res.get('title'), url=res.get('link'), description=res.get('snippet')) for res in resp.json().get('items')[:5]]
        await message.channel.send('Top 5 Search Results are:')
        for resp in response_list:
            await message.channel.send(embed=resp)
        db.search_history.insert_one(
            dict(author_id=message.author.id, search_text=msg))

    if message.content.startswith("!recent"):
        msg = message.content[7:].strip()
        await message.channel.send(f"fetching our search history:")
        history_items = list(db.search_history.find(dict(author_id=message.author.id,
                                                         search_text={'$regex': f'.*{msg}.*', '$options': 'i'})))
        for idx, hi in enumerate(history_items[:5]):
            await message.channel.send(f"{idx}. {hi.get('search_text')}")
        await message.channel.send(f"finished fetching search history")


client.run(TOKEN)
