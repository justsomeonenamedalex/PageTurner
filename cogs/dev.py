import discord
from discord.ext import commands
import ast


class Dev(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.config = client.config

    def insert_returns(self, body):
        # insert return stmt if the last expression is a expression statement
        if isinstance(body[-1], ast.Expr):
            body[-1] = ast.Return(body[-1].value)
            ast.fix_missing_locations(body[-1])

        # for if statements, we insert returns into the body and the orelse
        if isinstance(body[-1], ast.If):
            self.insert_returns(body[-1].body)
            self.insert_returns(body[-1].orelse)

        # for with blocks, again we insert returns into the body
        if isinstance(body[-1], ast.With):
            self.insert_returns(body[-1].body)

    @commands.is_owner()
    @commands.command(hidden=True)
    async def load(self, ctx, extension: str):
        """Loads a cog"""
        try:
            self.client.load_extension(f"cogs.{extension}")
            await ctx.send(f"{extension} loaded.")

        except commands.NoEntryPointError as e:
            # Runs if the cog has no entry point
            # Not sure if I need this but I might as well cover everything
            await ctx.send(f"Extension {e.name} has no entry point.")

        except commands.ExtensionFailed as e:
            # Runs if there is an error in the code
            await ctx.send(f"Failed to load extension {e.name}, due to a code error:\n`{e.original}`")

        except commands.ExtensionAlreadyLoaded as e:
            await ctx.send(f"Extension {e.name} is already loaded.")

        except commands.ExtensionNotFound as e:
            await ctx.send(f"Extension {e.name} not found.")

    @commands.is_owner()
    @commands.command(hidden=True)
    async def unload(self, ctx, extension: str):
        """Unloads a cog"""
        try:
            self.client.unload_extension(f"cogs.{extension}")
            await ctx.send(f"{extension} unloaded.")

        except commands.ExtensionFailed as e:
            # Runs if there is an error in the code
            await ctx.send(f"Failed to unload extension {e.name}, due to a code error:\n`{e.original}`")

        except commands.ExtensionNotLoaded as e:
            await ctx.send(f"Extension {e.name} is not loaded")

        except commands.ExtensionNotFound as e:
            await ctx.send(f"Extension {e.name} not found.")

    @commands.is_owner()
    @commands.command(hidden=True)
    async def reload(self, ctx, extension: str):
        """Unloads, then loads a cog"""
        # Unload the cog
        try:
            self.client.unload_extension(f"cogs.{extension}")
            await ctx.send(f"{extension} unloaded.")

        except commands.ExtensionFailed as e:
            await ctx.send(f"Failed to unload extension {e.name}, due to a code error:\n`{e.original}`")

        except commands.ExtensionNotLoaded as e:
            await ctx.send(f"Extension {e.name} is not loaded")

        except commands.ExtensionNotFound as e:
            await ctx.send(f"Extension {e.name} not found.")

        # Load the cog
        try:
            self.client.load_extension(f"cogs.{extension}")
            await ctx.send(f"{extension} loaded.")

        except commands.NoEntryPointError as e:
            # Not sure if I need this but I might as well cover everything
            await ctx.send(f"Extension {e.name} has no entry point.")

        except commands.ExtensionFailed as e:
            await ctx.send(f"Failed to load extension {e.name}, due to a code error:\n`{e.original}`")

    @commands.is_owner()
    @commands.command(hidden=True)
    async def activity(self, ctx, *, text):
        """Sets the activity of the bot manually"""
        await self.client.change_presence(activity=discord.Game(text))
        await ctx.send(f"Activity set to {text}")

    @commands.is_owner()
    @commands.command(aliases=["shutdown", "off"], hidden=True)
    async def goodnight(self, ctx):
        """Safely shuts down the bot"""
        await ctx.send("Bot shutting down")

        await self.client.change_presence(status=discord.Status.offline)
        await self.client.logout()

    @commands.is_owner()
    @commands.command(aliases=["inv"], hidden=True)
    async def invite(self, ctx):
        """Sends the link used to add the bot to servers"""
        await ctx.send(self.config["invite"])

    @commands.command(hidden=True)
    async def server(self, ctx):
        """Gets info on the server"""
        guild = ctx.guild
        e = discord.Embed(title="Server Info", description=guild.description, color=discord.Color.blue())
        e.set_author(name=guild.name, icon_url=guild.icon_url_as(format="png"))
        e.add_field(name="Owner", value=guild.owner.mention, inline=False)
        e.add_field(name="Members", value=len(guild.members), inline=False)
        e.add_field(name="Created at", value=guild.created_at, inline=False)
        await ctx.send(embed=e)

    @commands.command(hidden=True)
    async def whois(self, ctx, member: discord.Member = None):
        """Gets info on a particular user"""
        if member is None:
            member = ctx.author

        e = discord.Embed(title="Member info", color=member.color)
        e.set_author(name=member.display_name, icon_url=member.avatar_url_as(format="png"))
        e.add_field(name="Joined at", value=member.joined_at, inline=False)
        e.add_field(name="Created at", value=member.created_at, inline=False)
        e.add_field(name="ID", value=member.id, inline=False)
        await ctx.send(embed=e)

    @commands.command(hidden=True)
    async def server_icon(self, ctx):
        embed = discord.Embed(title=f"Server icon for {ctx.guild.name}")
        embed.set_image(url=ctx.guild.icon_url_as(format="png"))
        await ctx.send(embed=embed)

    @commands.is_owner()
    @commands.command(hidden=True)
    async def run(self, ctx, *, cmd):
        """Evaluates input.

        Input is interpreted as newline seperated statements.
        If the last statement is an expression, that is the return value.

        Usable globals:
          - `bot`: the bot instance
          - `discord`: the discord module
          - `commands`: the discord.ext.commands module
          - `ctx`: the invokation context
          - `__import__`: the builtin `__import__` function

        Such that `>eval 1 + 1` gives `2` as the result.

        The following invokation will cause the bot to send the text '9'
        to the channel of invokation and return '3' as the result of evaluating

        >eval
        a = 1 + 2
        b = a * 2
        await ctx.send(a + b)
        a
        """
        fn_name = "_eval_expr"

        cmd = cmd.strip("` ")

        # add a layer of indentation
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

        # wrap in async def body
        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        self.insert_returns(body)

        env = {
            'bot': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        try:
            result = (await eval(f"{fn_name}()", env))
            await ctx.send(f"```\n{result}\n```")
        except Exception as e:
            await ctx.send(f"```\nException:\n{e}\n```")


def setup(client):
    client.add_cog(Dev(client))
