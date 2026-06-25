import numpy as np

# Part 1: Working with Arrays
print("="*100)
print("Part 1: Working with Arrays")
print("="*100)
# 1. Create array 'a' with shape (3, 4)
a = np.array([[3, 8, 15, 2],
              [2, 10, 5, 3],
              [4, 0, 2, 4]])
print("1) Array a:\n", a)
# 2. Print the shape of the array a
print("2) Shape of a:", a.shape)  # (rows, columns)
# 3. Print the number of dimensions (ndim) of the array
print("3) Number of dimensions (ndim):", a.ndim)
# 4. Use len() on a
print("4) len(a):", len(a))  # For 2D arrays, this is the size of the first dimension (number of rows)
# 5. Based on the shape, determine number of dimensions and length. Number of dimensions is len(a.shape). Length is a.shape[0]
print("5) \nFrom shape, number of dimensions:", len(a.shape))
print("From shape, length (first dimension):", a.shape[0])

# Part 2: Array Creation with NumPy
print("="*100)
print("Part 2: Array Creation with NumPy")
print("="*100)
# 6. 1D array with values from 2 to 5 inclusive
arr_6 = np.arange(2, 6)  # 6 is exclusive, so this gives 2,3,4,5
print("6) 1D array from 2 to 5:", arr_6)
# 7. 1D array with 10 equally spaced values between 2 and 5 inclusive
arr_7 = np.linspace(2, 5, 10)
print("7) 10 equally spaced values between 2 and 5:\n", arr_7)
# 8. 4 x 4 array filled with ones
arr_8 = np.ones((4, 4))
print("8) 4x4 array of ones:\n", arr_8)
# 9. 6 x 6 identity matrix
arr_9 = np.eye(6)
print("9) 6x6 identity matrix:\n", arr_9)
# 10. Diagonal matrix [[1,0,0],[0,2,0],[0,0,3]] using a single command
arr_10 = np.diag([1, 2, 3])
print("10) Diagonal matrix:\n", arr_10)
# 11. (3, 5) array with random numbers from standard normal distribution
np.random.seed(0)  # Optional: set seed for reproducible results
arr_11 = np.random.randn(3, 5)
print("11) (3,5) random array from N(0,1):\n", arr_11)

# Part 3: Indexing and Slicing
print("="*100)
print("Part 3: Indexing and Slicing")
print("="*100)
# 12. Create array 'a'
a = np.array([[2, 7, 12, 0],
              [3, 9, 3, 4],
              [4, 0, 1, 3]])
print("Array a:\n", a)
# 13. Retrieve the second row: [3, 9, 3, 4]
second_row = a[1, :]  # row index 1 (0-based)
print("13) Second row:", second_row)
# 14. Retrieve the third column: [12, 3, 1]
third_column = a[:, 2]  # column index 2
print("14) Third column:", third_column)
# 15. Create the two arrays:
# 1) Integer array
int_array = np.array([[1, 1, 1, 1],
                      [1, 1, 1, 1],
                      [1, 1, 1, 2],
                      [1, 6, 1, 1]])
print("15.1) Integer array:\n", int_array)
# 2) Float array
float_array = np.array([[0., 0., 0., 0., 0.],
                        [2., 0., 0., 0., 0.],
                        [0., 3., 0., 0., 0.],
                        [0., 0., 4., 0., 0.],
                        [0., 0., 0., 5., 0.],
                        [0., 0., 0., 0., 6.]])
print("15.2) Float array:\n", float_array)

# Part 4: Boolean Masks and Statistics
print("="*100)
print("Part 4: Boolean Masks and Statistics")
print("="*100)
# 16. Recall array 'a'
a = np.array([[2, 7, 12, 0],
              [3, 9, 3, 4],
              [4, 0, 1, 3]])
print("Array a:\n", a)
# 17. Comparison operation (> 5) to create Boolean mask
mask = a > 5
print("17) Boolean mask (a > 5):\n", mask)
# 18. Use mask to extract all values greater than 5
greater_than_5 = a[mask]
print("18) Values greater than 5:", greater_than_5)
# 19. Modify array in-place: all values > 5 replaced with 5
a[a > 5] = 5
print("19) Array a after replacing values > 5 with 5:\n", a)

# Part 5: Array Aggregation Functions
print("="*100)
print("Part 5: Array Aggregation Functions")
print("="*100)
# Recall modified array 'a'
print("Array a used for aggregation:\n", a)
# 20a. Sum of all values
total_sum = a.sum()
print("20.a) Sum of all values:", total_sum)
# 20b. Sum of each column
col_sum = a.sum(axis=0)
print("20.b) Sum of each column:", col_sum)
# 20c. Sum of each row
row_sum = a.sum(axis=1)
print("20.c) Sum of each row:", row_sum)
# 20d. Mean of all values
mean_val = a.mean()
print("20.d) Mean of all values:", mean_val)
# 20e. Minimum value
min_val = a.min()
print("20.e) Minimum value:", min_val)
# 20f. Maximum value
max_val = a.max()
print("20.f) Maximum value:", max_val)