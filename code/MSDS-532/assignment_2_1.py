"""
Assignment 2.1: Finding the 450th Prime Number
Purpose: This program uses a generate-and-test approach to find the 450th prime number.
May 17, 2026
Alan Biju Palayil
"""

# This function tests whether a number is prime.
# A prime number is divisible only by 1 and itself.
def is_prime(number):
    if number == 2:
        return True

    if number < 2 or number % 2 == 0:
        return False

    divisor = 3

    # Only test divisors up to the square root of the number.
    # If a number has a divisor larger than its square root,
    # it must also have a matching divisor smaller than its square root.
    while divisor * divisor <= number:
        if number % divisor == 0:
            return False
        divisor += 2

    return True


prime_count = 1
candidate = 3
last_prime = 2

while prime_count < 450:
    if is_prime(candidate):
        prime_count += 1
        last_prime = candidate

        if prime_count % 50 == 0:
            print(f"{prime_count} prime numbers found so far.")

    candidate += 2

print(f"The program was looking for the 450th prime number.")
print(f"The 450th prime number is {last_prime}.")