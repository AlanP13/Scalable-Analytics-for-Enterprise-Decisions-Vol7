"""
Assignment 3 Problem 2: Closest feasible chicken nugget order quantity
Purpose: This program determines whether a requested chicken nugget quantity can be ordered.
If not, it finds the closest feasible alternative quantity and displays available combinations.
May 25, 2026
Alan Biju Palayil
"""

def find_options(order_size):
    options = []

    for six_piece in range(order_size // 6 + 1):
        for nine_piece in range(order_size // 9 + 1):
            for twenty_two_piece in range(order_size // 22 + 1):
                total = (6 * six_piece) + (9 * nine_piece) + (22 * twenty_two_piece)

                if total == order_size:
                    option = {
                        "Six_piece": six_piece,
                        "Nine_piece": nine_piece,
                        "Twenty_two_piece": twenty_two_piece
                    }
                    options.append(option)

    return options


def find_closest_feasible_order(requested_size):
    distance = 1

    while True:
        lower_quantity = requested_size - distance
        upper_quantity = requested_size + distance

        if lower_quantity >= 0:
            lower_options = find_options(lower_quantity)
            if len(lower_options) > 0:
                return lower_quantity, lower_options

        upper_options = find_options(upper_quantity)
        if len(upper_options) > 0:
            return upper_quantity, upper_options

        distance += 1


nuggets_requested = int(input("How many chicken nuggets would you like to order? "))

options = find_options(nuggets_requested)

if len(options) > 0:
    print(f"For an order size of {nuggets_requested}, choose from the following {len(options)} option(s):")
    for option in options:
        print(option)
else:
    closest_quantity, closest_options = find_closest_feasible_order(nuggets_requested)

    print(f"You cannot order exactly {nuggets_requested} chicken nuggets.")
    print(f"The closest feasible order quantity is {closest_quantity}.")
    print(f"For an order size of {closest_quantity}, choose from the following {len(closest_options)} option(s):")

    for option in closest_options:
        print(option)