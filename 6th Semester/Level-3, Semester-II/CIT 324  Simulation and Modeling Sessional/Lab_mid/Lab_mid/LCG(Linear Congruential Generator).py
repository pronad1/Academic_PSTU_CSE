import matplotlib.pyplot as plt

# LCG parameters
m = 16         
a = 5          
c = 3        
X0 = 7        
n = 10        

random_numbers = []

Xn = X0
for i in range(n):
    Xn = (a * Xn + c) % m      # LCG formula
    random_numbers.append(Xn)

# normalize to 0-1
U = [x / m for x in random_numbers]

print("Generated LCG numbers:", random_numbers)
print("Normalized numbers (0-1):", U)


plt.figure(figsize=(8,4))


plt.scatter(range(1, n+1), U, color='blue', s=50)
plt.plot(range(1, n+1), U, linestyle='--', color='orange', alpha=0.7)

plt.title("LCG Generated Random Numbers (Normalized 0-1)")
plt.xlabel("Iteration (n)")
plt.ylabel("Random Number U_n")
plt.ylim(0,1)
plt.grid(True)
plt.show()