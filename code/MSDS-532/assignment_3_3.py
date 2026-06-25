"""
Assignment 3 Problem 3: Least expensive chicken nugget order option
Purpose: This program determines the lowest cost chicken nugget box combination for a requested
quantity using 6-piece, 9-piece, and 22-piece box options. If the requested quantity is not feasible,
the program finds the closest feasible quantity and provides the lowest cost option for that quantity.
May 24, 2026
Alan Biju Palayil
"""

def find_options(order_size):
    options = []

    for six_piece in range(order_size // 6 + 1):
        for nine_piece in range(order_size // 9 + 1):
            for twenty_two_piece in range(order_size // 22 + 1):
                total = (6 * six_piece) + (9 * nine_piece) + (22 * twenty_two_piece)

                if total == order_size:
                    cost = (3 * six_piece) + (4 * nine_piece) + (9 * twenty_two_piece)

                    option = {
                        "Six_piece": six_piece,
                        "Nine_piece": nine_piece,
                        "Twenty_two_piece": twenty_two_piece,
                        "Total_cost": cost
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


def find_lowest_cost_option(options):
    lowest_cost_option = options[0]

    for option in options:
        if option["Total_cost"] < lowest_cost_option["Total_cost"]:
            lowest_cost_option = option

    return lowest_cost_option


nuggets_requested = int(input("How many chicken nuggets would you like to order? "))

options = find_options(nuggets_requested)

if len(options) > 0:
    best_option = find_lowest_cost_option(options)

    print(f"For an order size of {nuggets_requested}, the lowest cost option is:")
    print(best_option)
    print(f"Total cost: ${best_option['Total_cost']}")
else:
    closest_quantity, closest_options = find_closest_feasible_order(nuggets_requested)
    best_option = find_lowest_cost_option(closest_options)

    print(f"You cannot order exactly {nuggets_requested} chicken nuggets.")
    print(f"The closest feasible order quantity is {closest_quantity}.")
    print("The lowest cost option for this alternative quantity is:")
    print(best_option)
    print(f"Total cost: ${best_option['Total_cost']}")