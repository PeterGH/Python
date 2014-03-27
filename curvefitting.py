import numpy
import numpy.linalg
import numpy.random
import matplotlib.pyplot as fig

# Generate a training set
N = 10
x = numpy.linspace(0, 1, num=N)
y = numpy.sin(2 * numpy.pi * x) + 0.3 * numpy.random.randn(N)
M = 5;

"""
Duplicate x for 1+M rows
0   x[1] x[2] ... x[N]
1   x[1] x[2] ... x[N]
2   x[1] x[2] ... x[N]
    ...
M   x[1] x[2] ... x[N]
"""
X = x * numpy.ones((1+M, N))

"""
Raise row i to the i-th power
0   (x[1])^0 (x[2])^0 ... (x[N])^0
1   (x[1])^1 (x[2])^1 ... (x[N])^1
2   (x[1])^2 (x[2])^2 ... (x[N])^2
    ...
M   (x[1])^M (x[2])^M ... (x[N])^M
"""
n = numpy.arange(1+M).reshape((1+M,1))
X = X ** n

# Solve XX * w = XY
XX = numpy.dot(X, X.T)
XY = numpy.dot(X, y)
w = numpy.linalg.solve(XX, XY)

"""
Polynomial
w[0] + w[1]x + w[2]x^2 + ... + w[M]x^M
"""
p = numpy.poly1d(w[::-1])
print(p)

u = numpy.linspace(0,1, 1000)
v = p(u)
t = numpy.sin(2 * numpy.pi * u)
fig.plot(x, y, '+', u, t, 'b', u, v, 'r')
fig.show()
