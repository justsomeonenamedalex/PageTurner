import discord
from discord.ext import commands
import math
import requests
import json
import time
import praw
import asyncio
from PIL import Image, ImageColor, ImageOps, ImageFilter, ImageDraw
from io import BytesIO


async def get_pfp(member: discord.Member):
    """Gets the pfp of the user as a png"""
    img = member.avatar_url_as(format="png")
    img = await img.read()
    return img


async def send_image(image, ctx, filename="image.png"):
    """Converts the pfp into a byte stream? I think? I know it turns it into something PIL can use"""
    # This code was stolen from a friend
    image_b = BytesIO()
    image.save(image_b, format="png")
    image_b.seek(0)
    await ctx.send(file=discord.File(image_b, filename=filename))


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
            if "prompt" in post.link_flair_text.lower() and not post.over_18 and post.score >= 20:
                break
            await asyncio.sleep(0.01)
        e = discord.Embed(title="Writing prompt", description=post.title[4:], url=post.url)
        await ctx.send(embed=e)

    @commands.command(aliases=["profile_picture"])
    async def pfp(self, ctx, user: discord.Member = None):
        """Gets the pfp of the user, or a specified user"""
        if user is None:
            user = ctx.author

        # Send the image as an embed because links don't always expand
        embed = discord.Embed(title=f"Profile picture of {user}")
        embed.set_image(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(alises=["pfp_bw"])
    async def pfp_greyscale(self, ctx, user: discord.Member = None):
        """Creates a greyscale version of the user's pfp"""
        if user is None:
            user = ctx.author

        image = Image.open(BytesIO(await get_pfp(user)))

        out = image.convert('L')
        await send_image(out, ctx)

    @commands.command()
    async def pfp_invert(self, ctx, user: discord.Member = None):
        """Invert's the colours of the user's pfp"""
        if user is None:
            user = ctx.author

        image = Image.open(BytesIO(await get_pfp(user)))

        image = image.convert('RGB')

        out = ImageOps.invert(image)
        await send_image(out, ctx)


def setup(client):
    client.add_cog(Fun(client))
