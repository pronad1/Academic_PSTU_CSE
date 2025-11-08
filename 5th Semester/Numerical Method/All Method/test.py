import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)
x=2*np.random.rand(100)
y=4 + 3 * x + np.random.randn(100,1)

def sgd(f,m=0,b=0,lr=0.01,epoch=1000):
    n=len(y)
    for _ in range(epoch):
        for i in range(n):
            xi=x[i]
            yi=y[i]
            y_pred=m*xi + b
            dm =-2 * xi *(yi-y_pred)
            db=-2*(yi-y_pred)
            m -= lr * dm
            b -= lr * db
    return m,b

m,b=sgd(x,y)
print(m,b)
