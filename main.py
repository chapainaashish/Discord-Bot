# await is used to suspends the execution of the sorrounding coroutine until the execution of each coroutine has finished

import random
import discord
from api_requests import *
from word_list import *
from config import *
from dialogflow_agent import *

# making instance of Client class which interacts with Discord Api(handles events, tracks state)
client = discord.Client()


@client.event
async def on_ready():
    """Handles the connection and prepare response"""
    global guild
    for guild in client.guilds:
        if guild.name == "GUILD":
            break
    # client.user represents to bot
    print(f"{client.user} is here!")
    # printing server name
    print(guild.name)


@client.event
async def on_member_join(member):
    """Handles new member join event"""
    await member.create_dm()
    await member.dm_channel.send(f"Let's welcome {member.name}, Welcome to the {guild.name}!")


@client.event
async def on_message(message):
    """Handles message event"""
    # Prevention for replying own message, i.e. "bot" message
    if message.author == client.user:
        return

    # Sending motivational quotes if any hints found
    if any(word in message.content for word in quotes_hint):
        await message.channel.send(get_quote())

    # Cheering up if any hints found
    if any(word in message.content for word in sad_words):
        await message.channel.send(random.choice(cheer_ups))

    # Wishing birthday if any hints found
    if any(word in message.content for word in birthday_hint):
        await message.channel.send(random.choice(birthday_ups))

    # Sending today news if news related cordinates found
    if any(word in message.content for word in news):
        for desc_news in news_search():
            await message.channel.send(desc_news)

    # Completing query of sender
    if any(word in message.content for word in weby):
        await message.channel.send(query_find(message.content))

    # Completing query through dialogflow
    else:
        await message.channel.send(dialogflow_request(message.content))

client.run(DISCORD)
