def f(t):
    return 20*t - 4.9*t**2

def secant_method(t0, t1, tol=1e-6, max_iter=100):
    print("Iter |   t")
    print("-----------------")
    for i in range(max_iter):
        if f(t1) - f(t0) == 0:
            print("Division by zero")
            return None
        t2 = t1 - f(t1)*(t1 - t0)/(f(t1) - f(t0))
        print(f"{i+1:3d}  | {t2:.6f}")
        if abs(t2 - t1) < tol:
            print("\nConverged in", i+1, "iterations.")
            return t2
        t0, t1 = t1, t2
    print("\nDid not converge within max iterations.")
    return None

t0 = 2
t1 = 5
solution = secant_method(t0, t1)
print("\nTime when ball hits the ground =", round(solution, 2), "seconds")
