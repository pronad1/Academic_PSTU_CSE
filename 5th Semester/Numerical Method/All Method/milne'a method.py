import numpy as np
import matplotlib.pyplot as plt

def f(x, y):
    return x + y  

h = 0.1
x = np.arange(0, 1+h, h)
y = np.zeros(len(x))

y[0] = 1

def rk4_step(xn, yn, h):
    k1 = h * f(xn, yn)
    k2 = h * f(xn + h/2, yn + k1/2)
    k3 = h * f(xn + h/2, yn + k2/2)
    k4 = h * f(xn + h, yn + k3)
    return yn + (k1 + 2*k2 + 2*k3 + k4)/6

for i in range(3):
    y[i+1] = rk4_step(x[i], y[i], h)

for i in range(3, len(x)-1):
    f0 = f(x[i-3], y[i-3])
    f1 = f(x[i-2], y[i-2])
    f2 = f(x[i-1], y[i-1])
    f3 = f(x[i], y[i])
    
    yp = y[i-3] + (4*h/3)*(2*f3 - f2 + 2*f1)
    
    f4 = f(x[i+1], yp)
    y[i+1] = y[i-1] + (h/3)*(f4 + 4*f3 + f2)

print(y)


h = 0.1
x = np.arange(0, 1+h, h)
y = np.array([1.0, 1.11034167, 1.24280514, 1.39971699,
              1.58364897, 1.79744188, 2.04423710, 2.32750471,
              2.65108129, 3.01920546, 3.43656303])

# Plot
plt.figure(figsize=(8,5))
plt.plot(x, y, 'o-', label="Milne Predictor-Corrector", color='blue')
plt.title("Numerical Solution of y' = x + y using Milne's Method")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.legend()
plt.show()