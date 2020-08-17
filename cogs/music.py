from discord.ext import commands

from util import spotify as spotify_util


class Music(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.config = client.config
        self.spotify = spotify_util.Spotify(client_id=self.config["spotify_id"], client_secret=self.config["spotify_secret"])
        self.spotipy_client = self.spotify.sp

    @commands.command()
    async def song(self, ctx, *, song_name):
        """Gets the open spotify link for the first song result of the given search"""
        links = self.spotify.search_songs(song_name)

        if links is None:
            await ctx.send("Something went wrong, sorry")

        if links:
            await ctx.send(links[0])
        else:
            await ctx.send("Sorry, the song wasn't found")

    @commands.command()
    async def album(self, ctx, *, album_name):
        """Gets the open spotify link for the first album result of the given search"""
        links = self.spotify.search_albums(album_name)

        if links is None:
            await ctx.send("Something went wrong, sorry")

        if links:
            await ctx.send(links[0])
        else:
            await ctx.send("Sorry, the album wasn't found")

    @commands.command()
    async def artist(self, ctx, *, artist_name):
        """Gets the open spotify link for the first artist result of the given search"""
        links = self.spotify.search_artists(artist_name)

        if links is None:
            await ctx.send("Something went wrong, sorry")

        if links:
            await ctx.send(links[0])
        else:
            await ctx.send("Sorry, the artist wasn't found")


def setup(client):
    client.add_cog(Music(client))
