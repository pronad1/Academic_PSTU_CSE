import numpy as np
import matplotlib.pyplot as plt

# Picard Approximations
def y1(x):
    return 1 + x + x**2 / 2

def y2(x):
    return 1 + x + x**2 / 2 + x**3 / 3 + x**4 / 8

def y3(x):
    return 1 + x + x**2 / 2 + x**3 / 3 + x**4 / 8 + x**5 / 15 + x**6 / 48

# Generate x values
x_vals = np.linspace(0, 1, 100)

# Plot Picard Approximations
plt.plot(x_vals, y1(x_vals), label="1st Approx (y1)")
plt.plot(x_vals, y2(x_vals), label="2nd Approx (y2)")
plt.plot(x_vals, y3(x_vals), label="3rd Approx (y3)")

# Graph formatting
plt.title("Picard's Method Approximations")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.legend()
plt.show()
