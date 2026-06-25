"""
Assignment 5 Problem 1: Fixed retirement investment growth
Purpose: Use successive approximation to calculate retirement account value
with salary, employee savings rate, fixed annual growth rate, and years invested.
June 7, 2026
Alan Biju Palayil
"""

def fixedInvestor(salary, p_rate, f_rate, years):
    """
    Calculates the value of a retirement account at the end of each year.

    salary: employee annual salary
    p_rate: employee personal investment rate as a decimal
    f_rate: fixed annual growth rate as a decimal
    years: number of years to evaluate

    Returns a list containing the account value at the end of each year.
    """
    yearly_values = []
    account_value = 0

    employer_rate = 0.05
    match_rate = min(p_rate, 0.05)
    yearly_contribution = salary * (p_rate + employer_rate + match_rate)

    for year in range(years):
        if year == 0:
            account_value = yearly_contribution
        else:
            account_value = yearly_contribution + account_value * (1 + f_rate)

        yearly_values.append(account_value)

    return yearly_values


# Testing code:
print(fixedInvestor(50000, 0.05, 0.05, 3))