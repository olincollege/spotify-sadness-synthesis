"""
Spotify api functions to get necessary data.
"""
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy


def login():
    """
    Sets up spotify api access.
    """

    with open("secrets.txt", "r") as f:
        cid = f.readline().strip()
        secret = f.readline().strip()

    client_credentials_manager = SpotifyClientCredentials(
        client_id=cid, client_secret=secret
    )
    global sp
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_tracks(url):
    """
    get tracks
    """

    playlist_URI = url.split("/")[-1].split("?")[0]

    return [
        track["track"]["name"] for track in sp.playlist_tracks(playlist_URI)["items"]
    ]


def get_all_playlists(path):
    """
    gets tracks in all playlists
    """
    with open(path, "r") as f:
        playlists = [get_tracks(url.strip()) for url in f]

    return playlists


def get_albums(url):

    data = sp.album_tracks(url)
    return [track["name"] for track in data["items"]]


def get_all_albums():
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
    return [
        laurel_hell,
        be_the_cowboy,
        puberty_2,
        bury_me_at_makeout_creek,
        retired_from_sad,
        lush,
        stranger_in_the_alps,
        punisher,
    ]
