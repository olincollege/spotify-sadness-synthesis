import numpy as np


def get_ranking(song, playlist):
    "takes a row(playlist) from the df and finds the ranking of a song, starting at 1, not 0"

    pass


def make_row_list(row, df):
    """
    converts a row of a data frame into a list

    Args: row: an int, representing the row of the data fram to be
    converted to a list. df: the data frame containing the row to be
    converted

    Returns: row_list, the row of the data frame as a list
    """
    row_list = df.loc[row, :].values.flatten().tolist()
    return row_list


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


def make_dict_one_album(album, all_songs):
    album_dict = {}
    for i in all_songs:
        if i in album:
            album_dict[i] = all_songs[i]

    return album_dict


# def get_one_album(album, df):
#     album_dict = {}
#     for i in df:

#     return
