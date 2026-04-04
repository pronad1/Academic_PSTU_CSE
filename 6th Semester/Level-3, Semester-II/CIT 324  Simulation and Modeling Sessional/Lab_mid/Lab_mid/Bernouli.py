import numpy as np
import matplotlib.pyplot as plt

# Parameters
p = 0.6
n_samples = 1000

bernoulli_samples = np.random.binomial(1, p, n_samples)

print("Bernoulli First 10 Samples:", bernoulli_samples[:10])
print("Bernoulli Empirical Mean:", np.mean(bernoulli_samples))
print("Bernoulli Theoretical Mean:", p)

# Plot Bernoulli
plt.hist(bernoulli_samples, bins=2, edgecolor='black', rwidth=0.8)
plt.title("Bernoulli Distribution (n=1)")
plt.xticks([0, 1])
plt.show()