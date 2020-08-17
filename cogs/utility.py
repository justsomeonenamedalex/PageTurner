import discord
from discord.ext import commands
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


class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = client.config

    @commands.command()
    async def ping(self, ctx):
        """Returns the response time of the bot in ms"""
        await ctx.send(f"Pong! `{round(self.client.latency * 1000)}ms`")

    @commands.command()
    async def poll(self, ctx, title: str, *options):
        """Creates a poll than can be voted upon with reactions"""
        emojis = ["1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣"]
        lines = []

        if len(options) > 9:
            await ctx.send("Sorry, there is a maximum of 9 options")
            return None

        # Generates the description based on the number if options
        for x, i in enumerate(options):
            lines.append(f"{emojis[x]} : `{i}`")

        desc = "\n".join(lines)
        embed = discord.Embed(title=title, description=desc)
        poll_message = await ctx.send(embed=embed)

        # Adds a reaction for each option
        for x, i in enumerate(options):
            await poll_message.add_reaction(emojis[x])

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
    client.add_cog(Utility(client))
