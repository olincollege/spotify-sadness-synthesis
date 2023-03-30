import numpy as np
from scipy import stats
import pandas as pd


def get_ranking(song, playlist):
    "takes a row(playlist) from the df and finds the ranking of a song, starting at 1, not 0"

    pass


def make_row_list(row, df):
    row_list = df.loc[row, :].values.flatten().tolist()
    return row_list


def find_percentile(song, playlist, dictionary):

    rank = playlist.index(song) + 1
    length = len(playlist)
    percentile = rank / length
    if song not in dictionary and song != None and song != "":
        dictionary[song] = []
        dictionary[song].append(percentile)

    elif song != None and song != "":
        dictionary[song].append(percentile)
    return dictionary


def find_avg_percent(dictionary):
    for i in dictionary:
        all = sum(dictionary[i])
        length = len(dictionary[i])
        average = all / length
        dictionary[i] = average

    return dictionary


def get_all_ranking(df, num=5):
    percent_dict = {}
    for row in df:
        playlist = make_row_list(row, df)
        for i in playlist:
            percent_dict = find_percentile(i, playlist, percent_dict)

        if row == (len(df) - 1):
            break
    percent_dict = remove_songs(percent_dict, num)

    return percent_dict


def remove_songs(dictionary, num=5):
    removed_dict = {}
    for i in dictionary:
        if len(dictionary[i]) >= num:
            removed_dict[i] = dictionary[i]
    return removed_dict


def get_avg_ranking(df):

    percent_dict = get_all_ranking(df)
    percent_dict = remove_songs(percent_dict, 5)
    avg_percent = find_avg_percent(percent_dict)
    return avg_percent


def find_most_controversial(dictionary, num):
    maxes = {}
    stds_dict = find_std_of_songs(dictionary)

    for i in range(0, num):
        max1 = 0

        maxes[max(stds_dict, key=stds_dict.get)] = stds_dict[
            max(stds_dict, key=stds_dict.get)
        ]

        del stds_dict[max(stds_dict, key=stds_dict.get)]
    return maxes


def find_least_controversial(dictionary, num):
    mins = {}
    stds_dict = find_std_of_songs(dictionary)

    for i in range(0, num):
        max1 = 0

        mins[min(stds_dict, key=stds_dict.get)] = stds_dict[
            min(stds_dict, key=stds_dict.get)
        ]

        del stds_dict[min(stds_dict, key=stds_dict.get)]
    return mins


def find_std_of_songs(dictionary):
    stds = {}
    for i in dictionary:
        stds[i] = np.std(dictionary[i])

    return stds


# def get_one_album(album, df):
#     album_dict = {}
#     for i in df:

#     return


def find_anomalies(playlists, forward_i, backward_i, threshold=0.5):
    """
    Finds playlists that are reversed ordered or appear to be unusually ordered.

    Args:
        playlists: a 2d list of songs, with each inner list being a playlist.
        forward_i: number representing index of a playlist to be used as a model normal order playlist.
        backward_i: number representing index of a playlist to be used as a model reverse order playlist.

    Returns:
        A list of numbers representing the indexes of the playlists that are in ambigious order,
        and a list of numbers representing the indexes of the playlists that are reversed.
    """

    df = pd.DataFrame(playlists)

    forward_series = pd.Series(
        range(len(df.loc[forward_i])), index=df.loc[forward_i].values.flatten().tolist()
    )
    forward_rank = pd.DataFrame(forward_series.rank(), columns=["for_rank"])

    backward_series = pd.Series(
        range(len(df.loc[backward_i])),
        index=df.loc[backward_i].values.flatten().tolist(),
    )
    backward_rank = pd.DataFrame(backward_series.rank(), columns=["back_rank"])

    ambiguous_indexes = []
    reversed_indexes = []

    rows = df.iterrows()
    for row in rows:
        playlist_series = pd.Series(range(len(row[1])), index=row[1])
        playlist_rank = pd.DataFrame(playlist_series.rank(), columns=["curr_rank"])

        merged = forward_rank.join(playlist_rank).join(backward_rank)
        merged = merged.dropna()
        rho, p = stats.spearmanr(
            list(merged[merged.index.notnull()]["for_rank"]),
            list(merged[merged.index.notnull()]["curr_rank"]),
        )
        rho_back, p = stats.spearmanr(
            list(merged[merged.index.notnull()]["back_rank"]),
            list(merged[merged.index.notnull()]["curr_rank"]),
        )

        if abs(rho) + abs(rho_back) < threshold:
            ambiguous_indexes.append(row[0])
        elif rho < 0 and rho_back > 0:
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
    df = pd.DataFrame(playlists)
    for i in indexes:
        playlists[i] = list(reversed(df.loc[i].dropna()))
    return playlists
