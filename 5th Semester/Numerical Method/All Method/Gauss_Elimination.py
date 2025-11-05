import numpy as np

A=np.array(eval(input("Enter matrix A (nested lists): ")),float)
b=np.array(eval(input("Enter vector b (list): ")),float)
n=len(b)

# Forward Elimination
for i in range(n):
    for j in range(i+1,n):
        factor=A[j,i]/A[i,i]
        A[j]=A[j]-factor*A[i]
        b[j]=b[j]-factor*b[i]
print(A)
print()

# Back Substitution (Easy Version)
x = np.zeros(n)
for i in range(n-1, -1, -1):
    sum_val = b[i]
    for j in range(i+1, n):
        sum_val -= A[i][j] * x[j]
    x[i] = sum_val / A[i][i]


print("Solution:", x)

# [[2,1,-1],[-3,-1,2],[-2,1,2]]
# [8,-11,-3]