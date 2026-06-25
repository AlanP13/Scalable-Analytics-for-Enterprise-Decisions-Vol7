"""
Assignment 4 Problem 1: Find and count matching strings
Purpose: This program creates iterative and recursive functions to count substring matches.
May 31, 2026
Alan Biju Palayil
"""

from string import *


def countSubstrMatches(srch_str, sub_str):
    """
    Counts the number of times sub_str appears inside srch_str using iteration.
    Both arguments should be strings. The function returns an integer count.
    Overlapping matches are counted.
    """
    if sub_str == "":
        return 0

    count = 0
    start = 0

    while True:
        match_index = srch_str.find(sub_str, start)

        if match_index == -1:
            break

        count += 1
        start = match_index + 1

    return count


def countSubstrRecursive(srch_str, sub_str, start=0):
    """
    Counts the number of times sub_str appears inside srch_str using recursion.
    srch_str and sub_str should be strings. start is an optional integer index.
    The function returns an integer count. Overlapping matches are counted.
    """
    if sub_str == "":
        return 0

    match_index = srch_str.find(sub_str, start)

    if match_index == -1:
        return 0

    return 1 + countSubstrRecursive(srch_str, sub_str, match_index + 1)


# Testing code:
print(countSubstrMatches("atatattta", "ata"))
print(countSubstrRecursive("atatattta", "ata"))
print(countSubstrMatches("python", "Python"))
print(countSubstrRecursive("python", "Python"))