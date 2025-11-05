import numpy as np

A = np.array(eval(input("Enter matrix A (nested lists): ")), float)
b = np.array(eval(input("Enter vector b (list): ")), float)
n = len(b)

for i in range(n):
    # Make pivot = 1
    pivot = A[i, i]
    A[i] = A[i] / pivot
    b[i] = b[i] / pivot
    
    for j in range(n):
        if j != i:
            factor = A[j, i]
            A[j] = A[j] - factor * A[i]
            b[j] = b[j] - factor * b[i]

print("Reduced Row Echelon Form of A:")
print(A)
print("\nSolution:", b)