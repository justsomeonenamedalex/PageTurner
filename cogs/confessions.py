import discord
from discord.ext import commands
import asyncio
import random


class Confessions(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client
        self.config = client.config

    # @commands.Cog.listener()
    # async def on_message(self, message: discord.Message):
    #
    #     if message.author.bot:
    #         return None
    #
    #     if isinstance(message.channel, discord.DMChannel):
    #         await message.channel.send(message.content)
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Deletes messages in void-venting after 5 seconds
        if message.channel.id == 743096503333027861:
            await asyncio.sleep(5)
            try:
                await message.delete()
            except discord.NotFound:
                pass

    @commands.command()
    async def confess(self, ctx: commands.Context, *, text):
        """When sent via dm, used to send an anonymous confession"""
        if not (isinstance(ctx.channel, discord.DMChannel)):
            return
        check_message = await ctx.send(
            f"Is this what you would like to anonymously send:\n```\n{text}\n```React to confirm or deny.")

        await check_message.add_reaction("✅")
        await check_message.add_reaction("❎")

        def check(reaction, user):
            return reaction.message.id == check_message.id and (
                    str(reaction.emoji) == "✅" or str(reaction.emoji) == "❎") and user == ctx.author

        try:
            response_reaction, user = await self.client.wait_for("reaction_add", timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond, so the process was cancelled")
            return

        if str(response_reaction.emoji) == "❎":
            await ctx.send("Ok, process cancelled")
            return

        elif str(response_reaction.emoji) == "✅":
            pass

        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        e = discord.Embed(title=text, color=discord.Color.from_rgb(r, g, b))
        e.set_footer(text="DM me `+confess` followed by your message to send a confession.")

        screening_channel = self.client.get_channel(self.config["confession_check_channel"])
        screening_message = await screening_channel.send(embed=e)

        await screening_message.add_reaction("✅")
        await screening_message.add_reaction("❎")

        def check(reaction, user):
            return reaction.message.id == screening_message.id and (
                    str(reaction.emoji) == "✅" or str(reaction.emoji) == "❎") and not user.bot

        try:
            screening_reaction, user = await self.client.wait_for("reaction_add", timeout=7200.0, check=check)
        except asyncio.TimeoutError:
            await screening_channel.send("You took too long to respond, so the process was cancelled")
            return

        if str(screening_reaction.emoji) == "❎":
            await screening_channel.send("Ok, confession denied")
            return

        elif str(screening_reaction.emoji) == "✅":
            await screening_channel.send("Confession sent")
            confession_channel = self.client.get_channel(self.config["confession_channel"])
            await confession_channel.send(embed=e)


def setup(client):
    client.add_cog(Confessions(client))
