"""
Test cases for data helper functions
"""
import pytest
import pandas as pd
from data_helpers import (
    find_percentile,
    find_avg_percent,
    get_all_ranking,
    remove_songs,
    get_avg_ranking,
)


AVG_PERCENT_CASES = [
    # test with one song and one number
    ({"song": [0.5]}, {"song": 0.5}),
    # test with one song and multiple percentiles
    ({"song": [0.5, 0.3]}, {"song": 0.4}),
    # test with multiple songs and multiple percentiles
    ({"song": [0.5, 0.7], "song2": [0.3, 0.4]}, {"song": 0.6, "song2": 0.35}),
]

ALL_RANKING_CASES = [
    # test a single example that includes multiple songs in different and same places in multiple playlists
    (
        pd.DataFrame(
            [["song1", "song2", "song3", "song4"], ["song2", "song1", "song3", "song4"]]
        ),
        {
            "song1": [0.25, 0.5],
            "song2": [0.5, 0.25],
            "song3": [0.75, 0.75],
            "song4": [1, 1],
        },
    )
]

REMOVE_SONGS_CASES = [
    # test with default cutoff
    (
        {
            "song1": [0.25, 0.5, 0.3, 0.4, 0.4, 0.5],
            "song2": [0.5, 0.25, 0.5, 1, 1, 1],
            "song3": [0.75, 0.75],
            "song4": [1, 1],
        },
        None,
        {
            "song1": [0.25, 0.5, 0.3, 0.4, 0.4, 0.5],
            "song2": [0.5, 0.25, 0.5, 1, 1, 1],
        },
    ),
    # test with custom cutoff
    (
        {
            "song1": [0.25, 0.5, 0.3, 0.4, 0.4, 0.5],
            "song2": [0.5, 0.25, 0.5, 1, 1, 1],
            "song3": [0.75, 0.75, 0.5],
            "song4": [1],
        },
        2,
        {
            "song1": [0.25, 0.5, 0.3, 0.4, 0.4, 0.5],
            "song2": [0.5, 0.25, 0.5, 1, 1, 1],
            "song3": [0.75, 0.75, 0.5],
        },
    ),
]

AVG_RANKING_CASES = [
    # test a case that includes averaging multiple numbers and single numbers for multiple songs
    (
        pd.DataFrame(
            [["song1", "song2", "song3", "song4"], ["song2", "song1", "song3", "song4"]]
        ),
        {
            "song1": 0.375,
            "song2": 0.375,
            "song3": 0.75,
            "song4": 1,
        },
    )
]

FIND_PERCENTILE_CASES = [
    # test first song
    ("song1", {}, {"song1": [0.2]}),
    # test last song
    ("song5", {}, {"song5": [1]}),
    # test middle song
    ("song2", {}, {"song2": [0.4]}),
    # test that previous ones in the dict are kept
    ("song5", {"song1": [0.2]}, {"song1": [0.2], "song5": [1]}),
]


@pytest.mark.parametrize("song,input_dict,output_dict", FIND_PERCENTILE_CASES)
def test_find_percentile(song, input_dict, output_dict):
    """
    Test that it finds song percentile in playlist correctly.

    Args:
        song: string, the song to find percentile of
        input_dict: input of previous function run
        output_dict: the same dictionary as the argument dictionary,
            but with the percentile of song added to the list of percentiles for
            that song. If that song did not already exist in the dictionary, it
            is added, and the list for the value is created with the percentile
            as the first item
    """

    example_playlist = ["song1", "song2", "song3", "song4", "song5"]
    assert find_percentile(song, example_playlist, input_dict) == output_dict


@pytest.mark.parametrize("dictionary,output_dict", AVG_PERCENT_CASES)
def test_find_avg_percent(dictionary, output_dict):
    """
    Checking that a dictionary is correctly averaged.

    Args:
        dict: A dictionary of song names correlated with a list of their percentile in all playlists
        output_dict: A dictionary of song names correlated with their avg percentile
    """

    assert find_avg_percent(dictionary) == output_dict


@pytest.mark.parametrize("data,output_dict", ALL_RANKING_CASES)
def test_find_all_ranking(data, output_dict):
    """
    Checking that it gets the percentiles of all songs in each playlist

    Args:
        data: a dataframe, each row representing a playlist with songs in ranked order.
        output_dict: a dictionary containing song titles as keys and lists of percentiles as the values
    """

    assert get_all_ranking(data, 1) == output_dict


@pytest.mark.parametrize("dictionary,cutoff, output_dict", REMOVE_SONGS_CASES)
def test_remove_songs(dictionary, cutoff, output_dict):
    """
    Checking songs that appear in less that cutoff number playlists are removed

    Args:
        dict: A dictionary of song names correlated with a list of their percentile in all playlists
        cutoff: a number representing the number of playlists that a song needs to be in.
        output_dict: A dictionary of song names correlated with their avg percentile, with necessary songs removed.
    """

    if cutoff is not None:
        assert remove_songs(dictionary, cutoff) == output_dict
    else:
        assert remove_songs(dictionary) == output_dict


@pytest.mark.parametrize("data,output_dict", AVG_RANKING_CASES)
def test_get_avg_ranking(data, output_dict):
    """
    Checking that it correctly gets the average rank percentile of each song across each playlist

    Args:
        data: a dataframe of songs, where each row represents a playlist
        in order
        output_dict: a dictionary of song title keys and avg
        percentile values
    """

    assert get_avg_ranking(data, 1) == output_dict
