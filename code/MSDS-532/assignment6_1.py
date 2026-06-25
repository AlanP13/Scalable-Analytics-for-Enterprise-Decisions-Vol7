"""
Assignment 6 Problem 1 – Scrabble-like Word Game
Purpose: Create a one-player word game similar to Scrabble
June 2026
Alan Biju Palayil
"""

import random

vowels = 'aeiou'
not_vowels = 'bcdfghjklmnpqrstvwxyz'
letters_per_hand = 7

points_by_letter = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1,
    'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8,
    'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1,
    'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1,
    'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}
from pathlib import Path

wordlist_file = Path(__file__).resolve().parent / "words.txt"

def import_wordlist():
    print("Loading word list from file...")

    with open(wordlist_file, encoding="utf-8") as f:
        wordlist = [word.lower() for word in f.read().splitlines()]

    print(len(wordlist), "words loaded")
    return wordlist


def into_dictionary(sequence):
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x, 0) + 1
    return freq


def calc_word_score(word, qty):
    score = sum(points_by_letter[c] for c in word)

    if len(word) == qty:
        score += 50

    return score


def show_hand(hand):
    for letter in hand:
        for _ in range(hand[letter]):
            print(letter, end=' ')
    print()


def dealing_hands(qty):
    hand = {}
    num_vowels = qty // 3

    for i in range(num_vowels):
        letter = random.choice(vowels)
        hand[letter] = hand.get(letter, 0) + 1

    for i in range(num_vowels, qty):
        letter = random.choice(not_vowels)
        hand[letter] = hand.get(letter, 0) + 1

    return hand


def hand_update(hand, word):
    updated = hand.copy()

    for letter in word:
        if letter in updated:
            updated[letter] -= 1
            if updated[letter] <= 0:
                del updated[letter]

    return updated


def word_is_valid(word, hand, word_list):
    if word not in word_list:
        return False

    hand_copy = hand.copy()

    for letter in word:
        if hand_copy.get(letter, 0) <= 0:
            return False
        hand_copy[letter] -= 1

    return True


def playing_hands(hand, word_list):
    total_score = 0

    while len(hand) > 0:
        print("Current hand:")
        show_hand(hand)

        word = input(
            "Given the letters in your hand, make a word or enter '.' to end: "
        ).lower()

        if word == ".":
            break

        if not word_is_valid(word, hand, word_list):
            print("Invalid word; please try again.")
        else:
            score = calc_word_score(word, letters_per_hand)
            total_score += score

            print(
                f"The word {word} got you {score} points. Total score: {total_score}"
            )

            hand = hand_update(hand, word)

    print(f"Final score: {total_score}")


def start_game(word_list):
    while True:
        choice = input(
            "Enter n for new hand or e to end game: "
        ).lower()

        if choice == "n":
            hand = dealing_hands(letters_per_hand)
            playing_hands(hand, word_list)

        elif choice == "e":
            print("Thanks for playing!")
            break

        else:
            print("Invalid option.")


if __name__ == "__main__":
    word_list = import_wordlist()
    start_game(word_list)
