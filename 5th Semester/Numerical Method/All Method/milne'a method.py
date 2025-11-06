import numpy as np
import matplotlib.pyplot as plt

def f(x, y):
    return x + y  

x0=0
y0=1
h=0.1
xn=10

x_values=[x0]
y_values=[y0]

n=0

while x0<xn:
    x0 +=h
    k1=h*f(x0,y0)
    k2=h*f(x0+h/2,y0+k1/2)
    k3=h*f(x0+h/2,y0+k2/2)
    k4=h*f(x0+h,y0+k3)

    y0 += (k1+2*k2+2*k3+k4)/6

    x_values.append(x0)
    y_values.append(y0)
    n +=1


x0, y0 = x_values[0], y_values[0]
x1, y1 = x_values[1], y_values[1]
x2, y2 = x_values[2], y_values[2]
x3, y3 = x_values[3], y_values[3]

def milne_method(x0, y0, x1, y1, x2, y2, x3, y3, x4, h=x1-x0):
    # Predictor
    y4_pred = y0 + (4 * h / 3) * (2 * f(x3, y3) - f(x2, y2) + 2 * f(x1, y1))
    # Corrector
    y4_corr = y2 + (h / 3) * (f(x2, y2) + 4 * f(x3, y3) + f(x4, y4_pred))
    return y4_corr

y4_milne = milne_method(x0, y0, x1, y1, x2, y2, x3, y3, x4=x3 + (x1 - x0))
print(f"y4 from Milne's method: {y4_milne}")
