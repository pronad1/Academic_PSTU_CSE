import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x**3 - 4 * x + 1

def df(x):
    return 3 * x**2 - 4

def newton_raphson(f,df,x,tol=1e-5,max_iter=100):
    for i in range(max_iter):
        x_new = x - f(x) / df(x)
        if abs(x_new - x) < tol:
            return x_new
        x = x_new
    raise ValueError("Newton-Raphson method did not converge")

x=0.5
root = newton_raphson(f, df, x)
n=np.arange(-10,10,0.1)

plt.plot(n,f(n),label='f(x) = x^3 - 4x + 1')
plt.scatter(root,f(root),color='blue')
plt.axvline(root,color='red',linestyle='--',label=f'Root at x={root:.5f}')

plt.axhline(0,color='black',linestyle='--')
plt.axvline(0,color='black',linestyle='--')

plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('Newton-Raphson Method Root Finding')
plt.legend()
plt.grid()  
plt.show()
