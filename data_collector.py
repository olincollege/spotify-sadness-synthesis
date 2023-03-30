"""
Spotify api functions to get necessary data.
"""
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

SPOTIFY = None


def login():
    """
    Connects to the spotify API with stored credentials.
    """

    with open("secrets.txt", "r", encoding="UTF-8") as file:
        cid = file.readline().strip()
        secret = file.readline().strip()

    client_credentials_manager = SpotifyClientCredentials(
        client_id=cid, client_secret=secret
    )
    global SPOTIFY
    SPOTIFY = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_tracks(url):
    """
    Gets the song names in a playlist.

    args:
        url: a string representing the spotify playlist url
    returns: a list of strings representing the song names, in order.
    """

    playlist_uri = url.split("/")[-1].split("?")[0]

    return [
        track["track"]["name"]
        for track in SPOTIFY.playlist_tracks(playlist_uri)["items"]
    ]


def get_all_playlists(path):
    """
    Gets the songs for all the playlist urls in a text file.

    Args:
        path: a string representing the path to the text file.

    Returns: a 2d list of strings representing song names, with each inner
    list being a playlist
    """
    with open(path, "r", encoding="UTF-8") as file:
        playlists = [get_tracks(url.strip()) for url in file]

    return playlists


def get_albums(url):
    """
    Gets the songs in a given album on spotify.

    Args:
        url: a string representing the url of the album on spotify.

    Returns: a list of strings representing song names.
    """

    data = SPOTIFY.album_tracks(url)
    return [track["name"] for track in data["items"]]


def get_all_albums():
    """
    Gets all the songs in the most popular albums.

    Returns: a 2d list of strings representing song names, with each inner
    list being an album
    """
    laurel_hell = get_albums(
        "https://open.spotify.com/album/4rcinMUHEWOxpIwJo2sf22?si=JDKtk3IFSACxhVdO5b3U_g"
    )
    be_the_cowboy = get_albums(
        "https://open.spotify.com/album/42cH7mrkfljkqkxA2Ip9Xq?si=K1ZiPV-xQH2qC1pB1pBrhw"
    )
    puberty_2 = get_albums(
        "https://open.spotify.com/album/4Coa8Eb9SzjrkwWEom963Q?si=YgaN4NZjSM-s-R3IDfCVjA"
    )
    bury_me_at_makeout_creek = get_albums(
        "https://open.spotify.com/album/3I2KkX13lHXuYqfBjSOopo?si=ttcTCKKYQueCMFmkWVCANQ"
    )
    retired_from_sad = get_albums(
        "https://open.spotify.com/album/7K4SuWzgUEweJScduBcC6f?si=gzQZriBiRdyik-qVWKf-Yg"
    )
    lush = get_albums(
        "https://open.spotify.com/album/22MICAVuz34zzqm4Se5Lga?si=KVn0cj73SzCD0bfrCdJNMA"
    )
    stranger_in_the_alps = get_albums(
        "https://open.spotify.com/album/5rcJ5xCMYYLCgGilFDKRZl?si=569_TrzdQWiHMuatIqRqbw"
    )
    punisher = get_albums(
        "https://open.spotify.com/album/6Pp6qGEywDdofgFC1oFbSH?si=nzWaWIYkS2uW2IDxETQhow"
    )
    boygenius = get_albums(
        "https://open.spotify.com/album/6RjlLIuDFC8Dw91yRAdPz9?si=yvACGcZaSU-fusdU5U-tsQ"
    )
    return [
        laurel_hell,
        be_the_cowboy,
        puberty_2,
        bury_me_at_makeout_creek,
        retired_from_sad,
        lush,
        stranger_in_the_alps,
        punisher,
        boygenius,
    ]
