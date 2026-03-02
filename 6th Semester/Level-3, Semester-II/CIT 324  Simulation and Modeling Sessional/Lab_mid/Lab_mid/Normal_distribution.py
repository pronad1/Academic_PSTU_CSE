import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Part 1: Unimodal Normal Curve

mu = 100
sigma = 20

x = np.linspace(0, 200, 500)
y = norm.pdf(x, mu, sigma)

plt.figure()
plt.plot(x, y)
plt.title("Unimodal Normal Distribution (Mean=100, SD=20)")
plt.xlabel("X")
plt.ylabel("Density")
plt.show()


# Part 2: Multimodal Curve

mu1, sigma1 = 80, 15
mu2, sigma2 = 120, 15

y1 = norm.pdf(x, mu1, sigma1)
y2 = norm.pdf(x, mu2, sigma2)

plt.figure()
plt.plot(x, y1 + y2)
plt.title("Multimodal Distribution (Mixture of Two Normals)")
plt.xlabel("X")
plt.ylabel("Density")
plt.show()


# Part 3: Random Sample (n=200)


sample = np.random.normal(100, 20, 200)

print("First 10 samples:", sample[:10])
print("Sample Mean:", np.mean(sample))
print("Sample Std Dev:", np.std(sample))


plt.figure()
plt.hist(sample, bins=15, density=True, edgecolor='black', alpha=0.6)

x_sample = np.linspace(min(sample), max(sample), 500)
y_sample = norm.pdf(x_sample, 100, 20)

plt.plot(x_sample, y_sample)
plt.title("Histogram of Random Sample (Mean=100, SD=20)")
plt.xlabel("X")
plt.ylabel("Density")
plt.show()


# Part 4: Blood Pressure Histogram


bp_sample = np.random.normal(80, 20, 200)

plt.figure()
plt.hist(bp_sample, bins=15, density=True, edgecolor='black', alpha=0.6)
x_bp = np.linspace(min(bp_sample), max(bp_sample), 500)
y_bp = norm.pdf(x_bp, 80, 20)
plt.plot(x_bp, y_bp)
plt.title("Histogram of Diastolic Blood Pressure (Mean=80, SD=20)")
plt.xlabel("Blood Pressure")
plt.ylabel("Density")
plt.show()