"""
Assignment 5 Problem 4: Maximum retirement expense
Purpose: Use binary search to estimate the maximum annual retirement expense
that brings the retirement account balance close to zero.
June 7, 2026
Alan Biju Palayil
"""

def variableInvestor(salary, p_rate, v_rate):
    """
    Calculates the value of a retirement account at the end of each year
    using a list of annual variable growth rates.
    """
    yearly_values = []
    account_value = 0

    employer_rate = 0.05
    match_rate = min(p_rate, 0.05)
    yearly_contribution = salary * (p_rate + employer_rate + match_rate)

    for year in range(len(v_rate)):
        if year == 0:
            account_value = yearly_contribution
        else:
            account_value = yearly_contribution + account_value * (1 + v_rate[year])

        yearly_values.append(account_value)

    return yearly_values


def finallyRetired(saved, v_rate, expensed):
    """
    Calculates the remaining retirement account value at the end of each year.
    """
    yearly_values = []
    account_value = saved

    for rate in v_rate:
        account_value = account_value * (1 + rate) - expensed
        yearly_values.append(account_value)

    return yearly_values


def maximumExpensed(salary, p_rate, workRate, retiredRate, epsilon):
    """
    Uses binary search to estimate the annual retirement expense that causes
    the retirement account to end close to zero.

    salary: employee annual salary
    p_rate: employee savings rate as a decimal
    workRate: list of annual return rates while investing
    retiredRate: list of annual return rates while retired
    epsilon: acceptable distance from zero

    Returns the estimated annual expense amount.
    """
    saved_values = variableInvestor(salary, p_rate, workRate)
    saved = saved_values[-1]

    low = 0
    high = saved
    expensed = (low + high) / 2

    remaining_values = finallyRetired(saved, retiredRate, expensed)
    remaining = remaining_values[-1]

    while abs(remaining) > epsilon:
        print(f"Trying an annual expense of ${expensed:.2f}, the remaining value is ${remaining:.2f}.")

        if remaining > 0:
            low = expensed
        else:
            high = expensed

        expensed = (low + high) / 2
        remaining_values = finallyRetired(saved, retiredRate, expensed)
        remaining = remaining_values[-1]

    print(f"Final annual expense estimate is ${expensed:.2f}, leaving ${remaining:.2f}.")
    return expensed


# Testing code:
maximumExpensed(
    50000,
     0.05,
    [0.00, 0.05, 0.04, 0.06, 0.03],
    [0.04, 0.03, 0.03, 0.02, 0.02],
    0.01
)