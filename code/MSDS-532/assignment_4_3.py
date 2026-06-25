"""
Assignment 4 Problem 3: Fuzzy matching substring positions
Purpose: This program creates a function that identifies fuzzy matches using substring index tuples.
May 31, 2026
Alan Biju Palayil
"""

from string import *


def fuzzyMatching(subOne, subTwo, subOneLength):
    """
    Finds fuzzy match starting positions based on two tuples of substring match indices.
    subOne is a tuple of starting indices for the first substring.
    subTwo is a tuple of starting indices for the second substring.
    subOneLength is the length of the first substring.
    The function returns a tuple containing starting positions where the two substrings
    are separated by one wildcard character.
    """
    fuzzy_matches = ()

    for start_position in subOne:
        expected_second_position = start_position + subOneLength + 1

        if expected_second_position in subTwo:
            fuzzy_matches = fuzzy_matches + (start_position,)

    return fuzzy_matches


# Testing code:
print(fuzzyMatching((0, 7, 9), (2,), len("a")))