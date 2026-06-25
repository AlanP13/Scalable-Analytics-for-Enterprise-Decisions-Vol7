"""
Assignment 4 Problem 2: Collect substring match indices
Purpose: This program creates a function that returns the starting indices of all substring matches.
May 31, 2026
Alan Biju Palayil
"""

from string import *


def allMatchesIndices(srch_str, sub_str):
    """
    Finds all starting index positions where sub_str appears inside srch_str.
    Both arguments should be strings. The function returns a tuple of integer indices.
    Overlapping matches are included.
    """
    if sub_str == "":
        return ()

    matches = ()
    start = 0

    while True:
        match_index = srch_str.find(sub_str, start)

        if match_index == -1:
            break

        matches = matches + (match_index,)
        start = match_index + 1

    return matches


# Testing code:
print(allMatchesIndices("atatattta", "ata"))
print(allMatchesIndices("atatatatta", "ata"))
print(allMatchesIndices("atattatta", "Python"))