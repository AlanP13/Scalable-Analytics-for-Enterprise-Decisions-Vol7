"""
Assignment 3 Problem 1: Quantities of chicken nuggets that fit within available order quantities
Purpose: This program determines whether a requested chicken nugget quantity can be ordered
using 6-piece, 9-piece, and 22-piece box combinations.
May 25, 2026
Alan Biju Palayil
"""

nuggets_requested = int(input("How many chicken nuggets would you like to order? (6/9/22 pieces) "))

options = []

for six_piece in range(nuggets_requested // 6 + 1):
    for nine_piece in range(nuggets_requested // 9 + 1):
        for twenty_two_piece in range(nuggets_requested // 22 + 1):
            total = (6 * six_piece) + (9 * nine_piece) + (22 * twenty_two_piece)

            if total == nuggets_requested:
                option = {
                    "Six_piece": six_piece,
                    "Nine_piece": nine_piece,
                    "Twenty_two_piece": twenty_two_piece
                }
                options.append(option)

if len(options) > 0:
    print(f"For an order size of {nuggets_requested}, choose from the following {len(options)} option(s):")
    for option in options:
        print(option)
else:
    print(f"You cannot order exactly {nuggets_requested} chicken nuggets.")