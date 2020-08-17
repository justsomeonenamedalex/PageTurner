import discord
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = client.config

    @commands.command(aliases=["poggers"])
    async def pog(self, ctx):
        """Poggers!"""
        await ctx.send("poggers")


def setup(client):
    client.add_cog(Fun(client))
