import numpy as np

def cramer_rule(A, b):
    det_A = np.linalg.det(A)
    if det_A == 0:
        print("Determinant is zero, system has no unique solution!")
        return None

    n = A.shape[0]
    x = np.zeros(n)
    for i in range(n):
        Ai = A.copy()
        Ai[:, i] = b # replace column i with b
        x[i] = np.linalg.det(Ai) / det_A
    return x

A = np.array(eval(input("Enter matrix A (use nested lists): ")), dtype=float)
b = np.array(eval(input("Enter vector b (use list): ")), dtype=float)

solution = cramer_rule(A, b)

if solution is not None:
    print("The solution is:", solution)
