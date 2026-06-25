"""
Assignment 5 Problem 2: Variable retirement investment growth
Purpose: Use successive approximation to calculate retirement account value
with salary, employee savings rate, and annual variable growth rates.
June 7, 2026
Alan Biju Palayil
"""

def variableInvestor(salary, p_rate, v_rate):
    """
    Calculates the value of a retirement account at the end of each year
    using a list of annual variable growth rates.

    salary: employee annual salary
    p_rate: employee personal investment rate as a decimal
    v_rate: list of annual growth rates as decimals

    Returns a list containing the account value at the end of each year.
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


# Testing code:
print(variableInvestor(50000, 0.05, [0.00, 0.05, 0.04]))