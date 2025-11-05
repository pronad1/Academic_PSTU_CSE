def g(x):
    return (10000 * 0.10) / (1 - (1.10) ** -5)

def fixed_point_iteration(x0, tol=1e-6, max_iter=100):
    print("Iter |   x")
    print("-----------------")
    for i in range(max_iter):
        x1 = g(x0)
        print(f"{i+1:3d}  | {x1:.6f}")
        if abs(x1 - x0) < tol:
            print("\nConverged in", i+1, "iterations.")
            return x1
        x0 = x1
    print("\nDid not converge within max iterations.")
    return None

x0 = 2000
solution = fixed_point_iteration(x0)
print("\nApproximate yearly installment =", round(solution, 2))
