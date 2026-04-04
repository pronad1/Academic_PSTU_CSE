import numpy as np
import matplotlib.pyplot as plt

# Parameters
n = 10        
p = 0.6      
n_samples = 1000  

samples = np.random.binomial(n, p, n_samples)

print("First 10 Samples:", samples[:10])

print("Empirical Mean:", np.mean(samples))

print("Theoretical Mean:", n * p)

plt.hist(samples, edgecolor='black')
plt.xlabel("Number of Successes")
plt.ylabel("Frequency")
plt.title("Binomial Distribution")
plt.show()