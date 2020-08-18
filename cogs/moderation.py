import discord
from discord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = client.config

    @commands.command()
    async def verify(self, ctx: commands.Context, member: discord.Member):
        unverified_role = ctx.guild.get_role(self.config["unverified_role"])
        member_role = ctx.guild.get_role(self.config["member_role"])
        await member.remove_roles(unverified_role)
        await member.add_roles(member_role)

        welcome_channel = ctx.guild.get_channel(self.config["welcome_channel"])
        message = f"Welcome {member.mention} to the server.\nMake sure to get some roles from <#743068757190115399> , " \ 
                  f"<#744588765888118835> and <#743089463038836778> and introduce yourself in <#743088854004662342> ! "

        await welcome_channel.send(message)


def setup(client):
    client.add_cog(Moderation(client))
