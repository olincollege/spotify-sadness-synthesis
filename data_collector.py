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
