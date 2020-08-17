import os
import json
import logging

import discord
from discord.ext.commands import Bot

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

with open("config.json", "r") as config_file:
    config = json.load(config_file)

client = Bot(
    command_prefix=config["prefix"],
    allowed_mentions=discord.AllowedMentions(everyone=False, roles=False, users=True),
    status=discord.Status.online,
    activity=discord.Game("Vibing | .help")
)
client.config = config

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        client.load_extension(f"cogs.{name}")

client.run(config["bot_token"])
