import random
import numpy as np
import matplotlib.pyplot as plt

def func(x):
    return x**3

n=0
m=0

for i in range(100):
    rx = random.randint(200,500)
    rx = rx/100
    ry = random.randint(0,150)
    n+=1
    if ry <= func(rx):
        m+=1
        plt.scatter(rx,ry,color = "green")
    else:
        plt.scatter(rx,ry,color = "blue")

x = []
y = []
i=0
h=0.2
while i<10:
    val = i
    x.append(val)
    y.append(func(val))
    i += h
    i = round(i,2)

plt.plot(x,y)
plt.show()

