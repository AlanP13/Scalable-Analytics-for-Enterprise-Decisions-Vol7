"""
Assignment 4 Problem 4: Return fuzzy matches only
Purpose: This program creates a function that returns only fuzzy substring matches
where exactly one character is incorrect.
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


def get_indices_for_part(srch_str, part):
    """
    Returns all matching indices for a substring part.
    If the part is empty, all possible index positions are returned so wildcard
    matching can work at the beginning or end of a substring.
    """
    if part == "":
        return tuple(range(len(srch_str) + 1))

    return allMatchesIndices(srch_str, part)


def fuzzyMatchesOnly(srch_str, sub_str):
    """
    Finds starting positions where sub_str matches srch_str with exactly one incorrect character.
    srch_str and sub_str should be strings. The function returns a tuple of integer indices.
    Exact matches are excluded from the returned tuple.
    """
    if sub_str == "" or len(sub_str) > len(srch_str):
        return ()

    fuzzy_matches = ()
    exact_matches = allMatchesIndices(srch_str, sub_str)

    for wildcard_position in range(len(sub_str)):
        first_part = sub_str[:wildcard_position]
        second_part = sub_str[wildcard_position + 1:]

        first_indices = get_indices_for_part(srch_str, first_part)
        second_indices = get_indices_for_part(srch_str, second_part)

        possible_matches = fuzzyMatching(first_indices, second_indices, len(first_part))

        for match in possible_matches:
            if match <= len(srch_str) - len(sub_str):
                if match not in exact_matches and match not in fuzzy_matches:
                    fuzzy_matches = fuzzy_matches + (match,)

    return fuzzy_matches


# Testing code:
print(fuzzyMatchesOnly("abcdefgabad", "abcd"))
print(fuzzyMatchesOnly("abcd abxd abcd abcd", "abcd"))
print(fuzzyMatchesOnly("atatatatta", "ata"))
print(fuzzyMatchesOnly("python", "Python"))