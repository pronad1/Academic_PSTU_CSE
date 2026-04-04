import numpy as np
import matplotlib.pyplot as plt

# Parameters
lambda_param = 0.1     
num_samples = 10000     

U = np.random.uniform(0, 1, num_samples)

X = -np.log(U) / lambda_param

plt.hist(X, bins=50, density=True, alpha=0.6, color='skyblue', edgecolor='black')
plt.title("Exponential Random Variates using Inverse Transform")
plt.xlabel("Value")
plt.ylabel("Density")
plt.show()

print("First 10 generated random variates:", X[:10])