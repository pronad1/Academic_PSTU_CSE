# Important about Cholesky
# Works only if the matrix is:
# Square
# Symmetric
# Positive definite (all eigenvalues > 0)

import numpy as np

# Get matrix size from user
n = int(input("Enter the size of the square matrix (n x n): "))

# Initialize an empty list to store rows
A_list = []

# Take matrix input row by row
print(f"Enter the {n}x{n} symmetric positive definite matrix values row by row:")
for i in range(n):
    row = list(map(float, input(f"Row {i+1}: ").split()))
    if len(row) != n:
        raise ValueError("Row length must match matrix size!")
    A_list.append(row)

# Convert to NumPy array
A = np.array(A_list)

# Check if matrix is symmetric
if not np.allclose(A, A.T):
    raise ValueError("Matrix is not symmetric. Cholesky decomposition requires symmetry.")

# Perform Cholesky decomposition
L = np.linalg.cholesky(A)

# Display results
print("\nOriginal matrix A:")
print(A)

print("\nLower triangular matrix L:")
print(L)

print("\nL * L^T:")
print(L @ L.T)
