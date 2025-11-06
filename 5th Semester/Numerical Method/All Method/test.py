import numpy as np
import matplotlib.pyplot as plt

def f(x,y):
    return x+y

x0=0
y0=1
h=0.1
xn=10

x_val=[x0]
y_val=[y0]

n=0
while x0<xn:
    x0 +=h
    k1=h*f(x0,y0)
    k2=h*f(x0+h/2,y0+k1/2)
    k3=h*f(x0+h/2,y0+k2/2)
    k4=h*f(x0+h,y0+k3)
    y0 += (k1+2*k2+2*k3+k4)/6

    x_val.append(x0)
    y_val.append(y0)
    n+=1

plt.plot(x_val,y_val,label='RK4')
plt.scatter(x_val,y_val)
plt.title("soaif")
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.legend()
plt.show()