"""
Collection of functions to process playlist data.
"""

import numpy as np
from scipy import stats
import pandas as pd


def find_percentile(song, playlist, dictionary):
    """
    Finds the percentile rank of a song in a single playlist

    Args: song: a string representing the exact song title.
    playlist: a list of the song titles in the order that the spotify
    user ranked them. dicionary: a dictionary containing the percentiles
    of songs in playlists that have already been found using this
    function. The song titles are keys and the values are lists of
    percentiles. This function will add the new percentile found to list of
    the correct song in the dictionary.

    Return: dictionary, the same dictionary as the argument dictionary,
    but with the percentile of song added to the list of percentiles for
    that song. If that song did not already exist in the dictionary, it
    is added, and the list for the value is created with the percentile
    as the first item

    Notes: This function is made to be used within the get_all_ranking
    function which iterates through every song in every row to call this
    function in order to find the percentile of a songs ranking in every
    playlist it appears in.

    """

    rank = playlist.index(song) + 1
    length = len(playlist)
    percentile = rank / length
    if song not in dictionary and song not in (None, ""):
        dictionary[song] = []
        dictionary[song].append(percentile)

    elif song is not None and song != "":
        dictionary[song].append(percentile)
    return dictionary


def find_avg_percent(dictionary):
    """
    Finds the average percentile of a song

    Args: dictionary: a dictionary
    with song titles as values, and lists of percentiles as the
    value. This function accesses the list of percenties and uses
    each value in the list to calculate an average percentile,
    which replaces the list as the value of a song title

    Returns: dictionary, the dictionary after it's been edited to
    hold the averages as the values, instead of lists of each
    percentile
    """
    for i in dictionary:
        total = sum(dictionary[i])
        length = len(dictionary[i])
        average = total / length
        dictionary[i] = average

    return dictionary


def get_all_ranking(data, cutoff=5):
    """
    Gets the ranking in percentiles of every song in every playlist

    Takes a data frame and converts rows(playlists) into lists,
    then iterates through each list to find the percentile ranking
    of each song on that list, then removes songs that appear in
    less playlists than the cutoff number, cutoff

    Args: data, a dataframe, each row representing a playlist with
    songs in ranked order. cutoff: an int, representing the value to be
    passed to the remove_songs function, aka the cut off number of
    times a song appears in playlists in order to not be removed
    from the dictionary for not having enough data points.

    Returns: percent_dict, a dictionary containing song titles as keys
    and lists of percentiles as the values.

    """
    percent_dict = {}
    for row in data:
        playlist = data.loc[row, :].values.flatten().tolist()
        for i in playlist:
            percent_dict = find_percentile(i, playlist, percent_dict)

        if row == (len(data) - 1):
            break
    percent_dict = remove_songs(percent_dict, cutoff)

    return percent_dict


def remove_songs(dictionary, cutoff=5):
    """
    Removes songs from a dictionary that appear less then num times

    Args: dictionary, a dictionary of songs and their percentiles or
    avg percentiles. cutoff, an int representing the cut off number of
    playlists a song appears in.

    Returns: removed_dict, a dictionary the same as 'dictionary',
    but without songs that appeared in less playlists than the cutoff
    number

    """
    removed_dict = {}
    for i in dictionary:
        if len(dictionary[i]) >= cutoff:
            removed_dict[i] = dictionary[i]
    return removed_dict


def get_avg_ranking(data, cutoff):
    """
    Gets the average rank percentile of each song across each playlist

    Uses get_all_ranking function to create a dictionaty with song title
    keys and list of percentile values. Then uses remove_songs to
    remove songs that appear less than the cutoff number. Then uses
    avg_percentage to create dictionary with song title keys and avg
    percentile values.

    Args: data, a dataframe of songs, where each row represents a playlist
    in order. cutoff, an int representing the cut off number of
    times a song appears in playlists in order to not be removed
    from the dictionary

    Returns: avg_percent, a dictionary of song title keys and avg
    percentile values
    """

    percent_dict = get_all_ranking(data, cutoff)
    percent_dict = remove_songs(percent_dict, cutoff)
    avg_percent = find_avg_percent(percent_dict)
    return avg_percent


def find_most_controversial(dictionary, num):
    """
    Finds the songs with the largest standard deviations

    Uses function find_stds_of_songs to get standard deviation of
    each song based on the dictionary values, which are lists of
    rank percentiles from each playlist the song appeared on

    Args: dictionary, a dictionary with song title keys and list of
    percentiles values. num, an int representing the number of most
    controversial songs to return. if num = 5, this function will
    return the top 5 most controversial songs.

    Return: maxes, a dictionary of song title keys and
    list of percentiles values, with only the num most controversial
    songs in the dictionary.

    Note: Most controversial is defined as having the highest
    standard deviation

    """
    maxes = {}
    new_dict = {}
    stds_dict = find_std_of_songs(dictionary)

    for _ in range(0, num):
        maxes[max(stds_dict, key=stds_dict.get)] = stds_dict[
            max(stds_dict, key=stds_dict.get)
        ]

        del stds_dict[max(stds_dict, key=stds_dict.get)]

    for song in maxes:
        new_dict[song] = dictionary[song]

    return new_dict


def find_least_controversial(dictionary, num):
    """
    Finds the songs with the largest standard deviations

    Uses function find_stds_of_songs to get standard deviation of
    each song based on the dictionary values, which are lists of
    rank percentiles from each playlist the song appeared on

    Args: dictionary, a dictionary with song title keys and list of
    percentiles values. num, an int representing the number of least
    controversial songs to return. if num = 5, this function will
    return the top 5 least controversial songs.

    Return: mins, a dictionary of song title keys and
    list of percentiles values, with only the num least controversial
    songs in the dictionary.

    Note: least controversial is defined as having the lowest
    standard deviation
    """
    mins = {}
    new_dict = {}
    stds_dict = find_std_of_songs(dictionary)

    for _ in range(0, num):
        mins[min(stds_dict, key=stds_dict.get)] = stds_dict[
            min(stds_dict, key=stds_dict.get)
        ]

        del stds_dict[min(stds_dict, key=stds_dict.get)]
    for song in mins:
        new_dict[song] = dictionary[song]

    return new_dict


def find_std_of_songs(dictionary):
    """
    Finds the standard deviation rank percentiles for each song

    uses numpy std function to calculate the standard deviations
    of a list of percentiles, taken from dictionary

    Args: dictionary, a dictionary of song title keys and list of
    percentiles values

    Return: stds, a dictionary with song title keys and standard
    deviation values
    """
    stds = {}
    for i in dictionary:
        stds[i] = np.std(dictionary[i])

    return stds


def make_dict_one_album(album, all_songs):
    """
    Creates a dictionary with only songs from a given album

    Args: album, a list of song titles from an album,
    all_songs, a dictionary with song title keys, and either
    avg percentile values, or list of percentiles values

    Return: album_dict, a dictionary with the same key and value
    types as all_songs, but only for songs in album


    """
    album_dict = {}
    for i in all_songs:
        if i in album:
            album_dict[i] = all_songs[i]

    return album_dict


# def get_one_album(album, df):
#     album_dict = {}
#     for i in df:

#     return


def find_anomalies(playlists, forward_i, backward_i, threshold=0.5):
    """
    Finds playlists that are reversed ordered or appear to be unusually ordered.

    Args:
        playlists: a 2d list of songs, with each inner list being a playlist.
        forward_i: number representing index of a playlist to be used as a model normal order
        playlist.
        backward_i: number representing index of a playlist to be used as a model reverse order
        playlist.

    Returns:
        A list of numbers representing the indexes of the playlists that are in ambigious order,
        and a list of numbers representing the indexes of the playlists that are reversed.
    """

    data = pd.DataFrame(playlists)

    forward_series = pd.Series(
        range(len(data.loc[forward_i])),
        index=data.loc[forward_i].values.flatten().tolist(),
    )
    forward_rank = pd.DataFrame(forward_series.rank(), columns=["for_rank"])

    backward_series = pd.Series(
        range(len(data.loc[backward_i])),
        index=data.loc[backward_i].values.flatten().tolist(),
    )
    backward_rank = pd.DataFrame(backward_series.rank(), columns=["back_rank"])

    ambiguous_indexes = []
    reversed_indexes = []

    rows = data.iterrows()
    for row in rows:
        playlist_series = pd.Series(range(len(row[1])), index=row[1])
        playlist_rank = pd.DataFrame(playlist_series.rank(), columns=["curr_rank"])

        merged = forward_rank.join(playlist_rank).join(backward_rank)
        merged = merged.dropna()
        rho, _ = stats.spearmanr(
            list(merged[merged.index.notnull()]["for_rank"]),
            list(merged[merged.index.notnull()]["curr_rank"]),
        )
        rho_back, _ = stats.spearmanr(
            list(merged[merged.index.notnull()]["back_rank"]),
            list(merged[merged.index.notnull()]["curr_rank"]),
        )

        if abs(rho) + abs(rho_back) < threshold:
            ambiguous_indexes.append(row[0])
        elif rho_back > 0 > rho:
            reversed_indexes.append(row[0])

    return ambiguous_indexes, reversed_indexes


def reverse_rows(playlists, indexes):
    """
    Reverses the order of the playlists at the given indices.

    Args:
        playlists: a 2d list of songs, with each inner list being a playlist.
        indexes: a list of numbers representing the indexes of playlists to be reversed.

    Returns:
        the modified playlist list
    """
    data = pd.DataFrame(playlists)
    for i in indexes:
        playlists[i] = list(reversed(data.loc[i].dropna()))
    return playlists
