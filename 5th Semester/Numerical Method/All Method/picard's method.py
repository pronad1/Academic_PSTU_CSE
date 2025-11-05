import sympy as sp

t = sp.symbols('t')
T0 = 90
Ta = 25
k = 0.1

def f(tt, yy):
    return -k * (yy - Ta)

def picard_method(x0, y0, h, iterations=4):
    y_approx = y0
    for _ in range(iterations):
        y_new = y0 + sp.integrate(f(t, y_approx), (t, x0, x0+h))
        y_approx = sp.simplify(y_new)
    return y_approx

y_approx = picard_method(0, T0, 1, iterations=4)
T1_picard = float(y_approx.subs(t, 1))
T1_exact = Ta + (T0 - Ta) * sp.exp(-k*1)

print(round(T1_picard, 4))
print(round(float(T1_exact), 4))
