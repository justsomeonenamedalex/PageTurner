import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class Spotify:
    def __init__(self, client_id: str, client_secret):
        # Create spotify thingy
        self.sp = spotipy.Spotify(client_credentials_manager=(
            SpotifyClientCredentials(client_id=client_id,
                                     client_secret=client_secret)))

    def search_songs(self, search: str, num_of_songs: int = 1) -> list:
        results = self.sp.search(search, type="track")
        links = []
        for i in range(num_of_songs):
            try:
                links.append(results["tracks"]["items"][i]["external_urls"]["spotify"])
            except IndexError:
                continue
            except KeyError:
                return None
        return links

    def search_artists(self, search: str, num_of_artists: int = 1) -> list:
        results = self.sp.search(search, type="artist")
        links = []

        for i in range(num_of_artists):
            try:
                links.append(results["artists"]["items"][i]["external_urls"]["spotify"])
            except IndexError:
                continue
            except KeyError as e:
                print(results)
                return None
        return links

    def search_albums(self, search: str, num_of_albums: int = 1) -> list:
        results = self.sp.search(search, type="album")
        links = []

        for i in range(num_of_albums):
            try:
                links.append(results["albums"]["items"][i]["external_urls"]["spotify"])
            except IndexError:
                continue
            except KeyError as e:
                print(results)
                return None
        return links