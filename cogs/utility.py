import discord
from discord.ext import commands


class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = client.config

    @commands.command()
    async def ping(self, ctx):
        """Returns the response time of the bot in ms"""
        await ctx.send(f"Pong! `{round(self.client.latency * 1000)}ms`")

    @commands.command()
    async def poll(self, ctx, title: str, *args):
        """Creates a poll than can be voted upon with reactions"""
        options = args
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


def setup(client):
    client.add_cog(Utility(client))
