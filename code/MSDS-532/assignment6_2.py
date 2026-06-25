"""
Assignment 6 Problem 2 – Ghost Word Game
Purpose: Two-player Ghost word game
June 2026
Alan Biju Palayil
"""

from pathlib import Path

wordlist_file = Path(__file__).resolve().parent / "words.txt"

def import_wordlist():
    print("Loading word list from file...")

    with open(wordlist_file, encoding="utf-8") as f:
        wordlist = [word.lower() for word in f.read().splitlines()]

    print(len(wordlist), "words loaded")
    return wordlist

def import_wordlist():
    with open(wordlist_file) as f:
        return [word.lower() for word in f.read().splitlines()]


def valid_fragment(fragment, word_list):
    for word in word_list:
        if word.startswith(fragment):
            return True
    return False


def play_ghost():
    word_list = import_wordlist()

    fragment = ""
    player = 1

    while True:
        print(f"\nCurrent fragment: {fragment}")
        letter = input(
            f"Player {player}, enter a letter: "
        ).lower()

        if len(letter) != 1 or not letter.isalpha():
            print("Enter one valid letter.")
            continue

        fragment += letter

        if len(fragment) >= 4 and fragment in word_list:
            print(f"\n{fragment} is a complete word.")
            print(f"Player {player} loses.")
            break

        if not valid_fragment(fragment, word_list):
            print(f"\nNo word begins with '{fragment}'.")
            print(f"Player {player} loses.")
            break

        player = 2 if player == 1 else 1


if __name__ == "__main__":
    play_ghost()
