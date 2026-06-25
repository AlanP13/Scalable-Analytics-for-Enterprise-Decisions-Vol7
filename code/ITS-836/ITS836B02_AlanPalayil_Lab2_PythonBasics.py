"""
Week 2 Assignment: Tuples, Lists, Sets, and Functions
Author: Alan Palayil
Course: Data Science & Big Data Analytics (ITS836B02)
Instructor: Dr. Charles Edeki
Description: This script demonstrates operations with tuples, lists, sets,
and functions per the assignment. Each section includes explanatory comments
and prints sample outputs so results are visible when executed.
"""
from functools import reduce
from typing import Iterable, List, Tuple

print("="*100)
print("Part 1: Tuples")
print("="*100)

# 1. Create and Access
# a) Define a tuple with at least 5 numerical values.
print("1.a)")
nums_tuple = (10, 20, 30, 40, 50)
print(f"Tuple: {nums_tuple}")

# b) Print the third item in the tuple (0-based indexing -> index 2)
print("1.b)")
print(f"Third item (index 2): {nums_tuple[2]}")

# 2. Tuple Modification (Workaround)
# a) Since tuples are immutable, demonstrate how to remove an item by converting the tuple to a list, removing an item, and converting it back. 
print("2.a)")
temp_list = list(nums_tuple)
removed_item = temp_list.pop(1)  # remove the second item (value 20)
modified_tuple = tuple(temp_list)
print(f"Removed item from tuple via list conversion: {removed_item}")
print(f"Modified tuple: {modified_tuple}")

# 3. Tuple Unpacking
# a) Unpack a tuple into individual variables and print each variable. 
print("3.a)")
person_tuple = ("Alan", "Biju", "Palayil", 13, "August",2000)
first_name, middle_name,last_name,birth_day,birth_month,birth_year = person_tuple
print(f" Person details: {person_tuple}")
print("Unpacking a tuple into individual variables and print each variable:")
print(f" First name: {first_name}")
print(f" Middle name: {middle_name}")
print(f" Last  name: {last_name}")
print(f" Birth day: {birth_day}")
print(f" Birth month: {birth_month}")
print(f" Birth year: {birth_year}")

# 4. Tuple to String
# a) Convert a tuple of characters into a single string and print it. 
print("4.a)")
char_tuple = ('A', 'a', 'B', 'b', 'C', 'c', 'D', 'd', 'E', 'e')
joined_string = ''.join(char_tuple)
print(f"Tuple {char_tuple} -> String: {joined_string}")

# 5. Find Duplicates
# a) Given a tuple with repeated elements, identify and print the duplicate values. 
print("5.a)")
dup_tuple = (1, 2, 3, 2, 4, 3, 5, 3, 6, 1, 7, 8, 8, 9, 2)
seen = set()
duplicates = set(x for x in dup_tuple if (x in seen) or seen.add(x))
print(f"Original tuple: {dup_tuple}")
print(f"Duplicate values: {sorted(duplicates)}")

# 6. Reverse Tuple using slicing
# a) Print the tuple in reverse order using slicing. 
print("6.a)")
print(f"Original tuple: {nums_tuple}")
reversed_tuple = nums_tuple[::-1]
print(f"Reversed tuple: {reversed_tuple}")

print("\n" + "="*100)
print("Part 2: Lists")
print("="*100)

# 7. Sum of List
# a) Write code to sum all the items in a list of numbers. 
print("7.a)")
num_list = [1, 3, 5, 7, 9, 11, 13, 15]
print(f"List: {num_list}")
print(f"Sum of list: {sum(num_list)}")

# 8. Remove Duplicates while maintaining order
# a) Remove duplicate values from a list while maintaining the original order. 
print("8.a)")
list_with_dups = [1, 2, 3, 2, 4, 3, 5, 3, 6, 1, 7, 8, 8, 9, 2]
seen = set()
deduped = [x for x in list_with_dups if not (x in seen or seen.add(x))]
print(f"Original list with duplicates: {list_with_dups}")
print(f"De-duplicated (order preserved): {deduped}")

# 9. Clone a List (three ways)
# a) Show three different ways to copy a list.
print("9.a)")
original = [12, 13, 11, 14, 10, 15]
clone_via_slice = original[:]
clone_via_list = list(original)
clone_via_copy = original.copy()
print(f"Original list: {original}")
print(f"Clone via slicing: {clone_via_slice}")
print(f"Clone via list():  {clone_via_list}")
print(f"Clone via copy():  {clone_via_copy}")

# 10. Combine Lists
# a) Create two separate lists and append one to the other. Print the combined result.
print("10.a)")
a = ["Mazda", "Honda", "Toyota"]
b = ["RAV4", "CX-5", "CR-V", "Highlander", "Pilot", "Mazda3"]
combined = a.copy()
combined.extend(b)  # append list b into a
print(f"List A: {a}")
print(f"List B: {b}")
print(f"Combined (A + B): {combined}")

# 11. Sort by Last Element in Tuple
# a) Given a list of non-empty tuples, sort the list in increasing order based on the last element of each tuple. 
print("11.a)")
tuple_list = [(1, 3), (3, 2), (2, 1), (5, 0), (4, 4)]
sorted_tuple_list = sorted(tuple_list, key=lambda t: t[-1])
print(f"Original tuple list: {tuple_list}")
print(f"Sorted by last element: {sorted_tuple_list}")

# 12. List Slicing
# a) Create a list with names of 10 people. Use slicing to print the first 4 names. 
print("12.a)")
people = ["Alan", "Bebe", "Chacko", "Daniel", "Edwyn", "Fayaz", "Gyan", "Harrison", "Ira", "John"]
print(f"People: {people}")
print(f"First 4 names (slicing): {people[:4]}")

print("\n" + "="*100)
print("Part 3: Sets")
print("="*100)

# 13. Create a Set
# a) Create a set of at least 5 elements and print it. 
print("13.a)")
techs = {"RAV4", "CX-5", "CR-V", "Highlander", "Pilot", "Mazda3"}
print(f"Created set: {techs}")

# 14. Set Intersection
# a) Create two sets with some common elements. Find and print their intersection. 
print("14.a)")
set_a = {"RAV4", "CX-5", "CR-V", "Highlander"}
set_b = {"Highlander", "Pilot", "Mazda3", "CR-V"}
print(f"Set A: {set_a}")
print(f"Set B: {set_b}")
print(f"Intersection: {set_a & set_b}")

# 15. Set Union
# a) Print the union of the same two sets. 
print("15.a)")
print(f"Set A: {set_a}")
print(f"Set B: {set_b}")
print(f"Union: {set_a | set_b}")

print("\n" + "="*100)
print("Part 4: Functions")
print("="*100)

# 16. Multiply List Elements
# a) Define a function that takes a list of numbers and returns the product of all numbers.
print("16.a)")
def product(numbers: Iterable[int]) -> int:
    """Return the product of all numbers in an iterable.
    Uses functools.reduce for clarity and explicitness.
    """
    return reduce(lambda a, b: a * b, numbers, 1)
sample_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(f"Numbers to multiply: {sample_numbers}")
print(f"Product: {product(sample_numbers)}")

# 17. Statistics Function
# a) Generate a list of test scores.  
print("17.a)")
def stats(scores: List[float]) -> Tuple[float, float, float]:
    """Return (min, max, average) of a list of scores."""
    if not scores:
        raise ValueError("scores list cannot be empty")
    return (min(scores), max(scores), sum(scores)/len(scores))
test_scores = [88, 92, 76, 81, 95, 89]
print(f"Test scores: {test_scores}")
# b) Write a function that returns the minimum, maximum, and average of the list. 
print("17.b)")
mn, mx, avg = stats(test_scores)
print(f"Min: {mn}, Max: {mx}, Avg: {avg:.2f}")

# 18. Check Range Membership
# a) Write a function that checks if a given number is within a specified range.
print("18.a)")
def in_range(x: float, low: float, high: float, inclusive: bool = True) -> bool:
    """Check if x is within [low, high] if inclusive else (low, high)."""
    return (low <= x <= high) if inclusive else (low < x < high)
print(f"Is 10 in [5, 15]? {in_range(10, 5, 15)}")
print(f"Is 5 in (5, 15)?  {in_range(5, 5, 15, inclusive=False)}")

# 19. Dog Speed Analyzer
# a) Create a nested list, each item containing a dog breed and its max running speed (e.g., ["Greyhound", 45]). 
print("19.a)")
dogs = [
    ["Greyhound", 45],
    ["Saluki", 42],
    ["German Shepherd", 30],
    ["Whippet", 35],
    ["Border Collie", 30],
    ["Dachshund", 15]
]
print(f"Dogs: {dogs}")
# b) Write a function to determine which dog breed is the fastest and which is the slowest. 
print("19.b)")
def dog_speed_extremes(dog_speeds: List[List]) -> Tuple[List, List]:
    """Return (fastest_dog, slowest_dog) from a nested [breed, speed] list."""
    if not dog_speeds:
        raise ValueError("dog_speeds cannot be empty")
    fastest = max(dog_speeds, key=lambda x: x[1])
    slowest = min(dog_speeds, key=lambda x: x[1])
    return fastest, slowest

fastest, slowest = dog_speed_extremes(dogs)
print(f"Fastest: {fastest[0]} ({fastest[1]} mph)")
print(f"Slowest: {slowest[0]} ({slowest[1]} mph)")

print("\n" + "="*100)
print("All tasks complete.")
print("="*100)