def f(x):
    return x**3 - 4 * x + 1
def g(x):
    return (x ** 3 + 1 )/ 4

def iteration(g,x,tol=1e-6, max_iter=100):
    for i in range(max_iter):
        x_new=g(x)
        if abs(x_new - x) < tol:
            return x_new
        x = x_new
    raise ValueError("Did not converge within the maximum number of iterations")

root = iteration(g, 1)
print("Approximate root:", root)