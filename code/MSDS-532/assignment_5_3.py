"""
Assignment 5 Problem 3: Retirement account withdrawals
Purpose: Calculate retirement account value over time when the account earns
annual returns and fixed annual payments are expensed to the retiree.
June 7, 2026
Alan Biju Palayil
"""

def finallyRetired(saved, v_rate, expensed):
    """
    Calculates the remaining retirement account value at the end of each year.

    saved: starting retirement account balance
    v_rate: list of annual return rates as decimals
    expensed: annual amount withdrawn from the account

    Returns a list containing the remaining account value at the end of each year.
    """
    yearly_values = []
    account_value = saved

    for rate in v_rate:
        account_value = account_value * (1 + rate) - expensed
        yearly_values.append(account_value)

    return yearly_values


# Testing code:
print(finallyRetired(100000, [0.05, 0.04, 0.03], 10000))