import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import expon


mean_days = 100 
x = 120         

lambda_param = 1 / mean_days  

prob = np.exp(-lambda_param * x)
print(f"Probability that next wave occurs after 120 days: {prob:.4f}")

rate_params = [0.5, 1.0, 2.0, 4.0]
num_samples = 10000  

plt.figure(figsize=(10,6))
for rate in rate_params:
    samples = np.random.exponential(scale=1/rate, size=num_samples)
    plt.hist(samples, bins=50, alpha=0.5, label=f"rate={rate}")

plt.title("Simulation of Exponential Distribution with Different Rates")
plt.xlabel("Days until next wave")
plt.ylabel("Frequency")
plt.legend()
plt.show()