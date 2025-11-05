import numpy as np

# Get the number of equations
n = int(input("Enter the number of equations (n): "))

# Initialize matrix A and vector b
A = []
b = []

print(f"Enter the coefficients of the {n} equations row by row:")
for i in range(n):
    row = list(map(float, input(f"Row {i + 1} coefficients: ").split()))
    if len(row) != n:
        raise ValueError("Row length must match number of equations!")
    A.append(row)
    b_val = float(input(f"Enter the constant term for equation {i + 1}: "))
    b.append(b_val)

A = np.array(A, dtype=float)
b = np.array(b, dtype=float)

# Gaussian Elimination (Triangulation)
for i in range(n):
    # Partial pivoting
    max_row = i + np.argmax(abs(A[i:, i]))
    if i != max_row:
        A[[i, max_row]] = A[[max_row, i]]
        b[[i, max_row]] = b[[max_row, i]]

    # Make elements below the pivot zero
    for j in range(i + 1, n):
        factor = A[j, i] / A[i, i]
        A[j, i:] = A[j, i:] - factor * A[i, i:]
        b[j] = b[j] - factor * b[i]

# Back substitution
x = np.zeros(n)
for i in range(n - 1, -1, -1):
    x[i] = (b[i] - np.dot(A[i, i + 1:], x[i + 1:])) / A[i, i]

# Display results
print("\nUpper triangular matrix U:")
print(A)
print("\nModified constants vector b:")
print(b)
print("\nSolution vector x:")
print(x)
