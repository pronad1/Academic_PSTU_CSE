import numpy as np
import matplotlib.pyplot as plt

def fun(x):
  return 0.2 + 25 * x - 200 * x**2 + 675 * x**3 - 900 * x**4 + 400 * x**5

def trapezoidal_rule(fun, a, b):
  return (b - a) * (fun(a) + fun(b)) / 2

array = np.arange(-0.01, 0.82, 0.01)

print(trapezoidal_rule(fun, 0, 0.8))
plt.plot(array, fun(array))
plt.plot([0, 0.8], [fun(0), fun(0.8)], color='red')
plt.show()
