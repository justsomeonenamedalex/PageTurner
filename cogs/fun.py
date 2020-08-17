import discord
from discord.ext import commands
import math
import requests
import json
import time
import praw
import asyncio


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = client.config

    @commands.command(aliases=["poggers"])
    async def pog(self, ctx):
        """Poggers!"""
        await ctx.send("poggers")

    @commands.command(aliases=["moonphase", "moon_phase"])
    async def moon(self, ctx):
        """Gets the current phase of the moon"""
        # This api is the most random thing i've found for this bot, so I wouldn't be surprised if it goes down
        # TODO: read up on how the api works and recreate it in python
        # https://github.com/FarmSense/Astro-Widget/blob/master/astro_widget.js
        date = math.floor(time.time())
        url = f"http://api.farmsense.net/v1/moonphases/?d={date}&callback=window.randName.f.moonPhase.parseRequest"
        page = requests.get(url)
        # TODO: do this with regex, even if it hurts my soul to do so
        page_split_one = page.text.split("(")[1]
        page_split_two = page_split_one.split(")")[0]
        page = page_split_two[1:-1]
        if page:
            data = json.loads(page)
            await ctx.send(f"The current phase of the moon is `{data['Phase']}`")
        else:
            await ctx.send("Page could not be found")

    @commands.command(aliases=["wp", "prompt"])
    async def writing_prompt(self, ctx):
        """Gets a random prompt from r/WritingPrompts"""
        reddit_username = self.config["reddit_username"]
        # reddit_password = self.config["reddit_password"]
        reddit_id = self.config["reddit_id"]
        reddit_secret = self.config["reddit_secret"]

        reddit = praw.Reddit(client_id=reddit_id, client_secret=reddit_secret, user_agent=reddit_username)

        while True:
            post = reddit.subreddit("WritingPrompts").random()
            if "prompt" in post.link_flair_text.lower():
                break
            await asyncio.sleep(0.01)
        e = discord.Embed(title="Writing prompt", description=post.title[4:], url=post.url)
        await ctx.send(embed=e)


def setup(client):
    client.add_cog(Fun(client))
