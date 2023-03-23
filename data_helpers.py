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
    if song not in dictionary:
        dictionary[song] = []
        dictionary[song].append(percentile)

    else:
        dictionary[song].append(percentile)
    return dictionary


def find_avg_percent(dictionary):
    for i in dictionary:
        all = sum(dictionary[i])
        length = len(dictionary[i])
        average = all / length
        dictionary[i] = average

    return dictionary


def get_avg_ranking(df):

    percent_dict = {}
    for row in df:
        playlist = make_row_list(row, df)
        for i in playlist:
            percent_dict = find_percentile(i, playlist, percent_dict)

        if row == (len(df) - 1):
            break

    avg_percent = find_avg_percent(percent_dict)
    return avg_percent