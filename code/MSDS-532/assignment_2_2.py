"""
Assignment 2.2: Sum of Logarithms of Prime Numbers
Purpose: This program evaluates whether the sum of the logarithms of prime numbers
between 2 and n converges toward n by printing the sum, n, and the ratio.
May 17, 2026
Alan Biju Palayil
"""

from math import *


# This function tests whether a number is prime.
def is_prime(number):
    if number == 2:
        return True

    if number < 2 or number % 2 == 0:
        return False

    divisor = 3

    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 2

    return True


# This function calculates the sum of the natural logarithms
# of all prime numbers from 2 through n.
def sum_prime_logs(n):
    total = 0

    for number in range(2, n + 1):
        if is_prime(number):
            total += log(number)

    return total


# Multiple values of n are used to demonstrate that the ratio
# of the sum of prime logarithms to n moves closer to 1.
n_values = [50, 500, 5000, 50000]

for n in n_values:
    log_sum = sum_prime_logs(n)
    ratio = log_sum / n

    print(f"For n = {n}:")
    print(f"Sum of logarithms of prime numbers = {log_sum}")
    print(f"Ratio of sum to n = {ratio}")
    print()