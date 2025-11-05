import numpy as np
from  scipy.linalg import lu

# Get matrix size from user
n=int(input("Enter the size of the square matrix (n x n): "))

#Initialize an empty list to store rows
A_list=[]

# Take matrix input row by row
print(f"Enter the {n}x{n} matrix values row by row: ")
for i in range(n):
    row=list(map(float,input(f"Row {i+1}: ").split()))
    if len(row)!=n:
        raise ValueError("Row length must match matrix size!")
    A_list.append(row)


# Convert to Numpy array
A=np.array(A_list)

# Perform LU factorization
P,L,U=lu(A)


# Display results
print("\nOriginal matrix A:")
print(A)

print("\nPermutation matrix P:")
print(P)

print("\nLower triangular matrix L:")
print(L)

print("\nUpper triangular matrix U:")
print(U)