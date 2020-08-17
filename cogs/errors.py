import discord
from discord.ext import commands


class Errors(commands.Cog):
    def __init__(self, client):
        self.client: commands.Bot = client
        self.config = client.config

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You had some missing arguments, here's the help page:")
            await ctx.send_help(ctx.command)

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have permission to run that command")

        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send(f"The bot is missing the following permission:\n{error.missing_perms}")

        else:
            print(f"{ctx.author.mention} had error '{error}' in command '{ctx.message.content}'")


def setup(client):
    client.add_cog(Errors(client))
