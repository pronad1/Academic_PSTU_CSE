import numpy as np
import matplotlib.pyplot as plt
import math

# Case 1: λ = 5 calls per hour

lam1 = 5
k_values = np.arange(0, 11)   # 0 to 10 calls

pmf1 = [(math.exp(-lam1) * lam1**k) / math.factorial(k) for k in k_values]

print("Probabilities for λ = 5")
for k, p in zip(k_values, pmf1):
    print(f"P(X = {k}) = {p:.5f}")

# Plot PMF for λ = 5
plt.figure()
plt.stem(k_values, pmf1)
plt.xlabel("Number of Calls per Hour")
plt.ylabel("Probability")
plt.title("Poisson PMF (λ = 5)")
plt.show()

# Case 2: λ = 10 calls per hour

lam2 = 10
k_values2 = np.arange(0, 21)

pmf2 = [(math.exp(-lam2) * lam2**k) / math.factorial(k) for k in k_values2]

plt.figure()
plt.stem(k_values2, pmf2)
plt.xlabel("Number of Calls per Hour")
plt.ylabel("Probability")
plt.title("Poisson PMF (λ = 10)")
plt.show()

# Case 3: λ = 15 calls per hour
lam3 = 15
k_values3 = np.arange(0, 31)

pmf3 = [(math.exp(-lam3) * lam3**k) / math.factorial(k) for k in k_values3]

plt.figure()
plt.stem(k_values3, pmf3)
plt.xlabel("Number of Calls per Hour")
plt.ylabel("Probability")
plt.title("Poisson PMF (λ = 15)")
plt.show()