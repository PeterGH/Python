import numpy
import numpy.linalg
import numpy.random
import matplotlib.pyplot as fig

def GetSamples(N):
    x = numpy.linspace(0, 1, num=N)
    y = numpy.sin(2 * numpy.pi * x) + 0.3 * numpy.random.randn(N)
    return x, y

def GetSampleMatrix(x, M):
    """
    Duplicate x for 1+M rows
    0   x[1] x[2] ... x[N]
    1   x[1] x[2] ... x[N]
    2   x[1] x[2] ... x[N]
        ...
    M   x[1] x[2] ... x[N]
    """
    N = len(x)
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

    return X

def GetRegularizationMatrix(M, l):
    """
    Regularization matrix
    0   0 0 0 ... 0
    1   0 l 0 ... 0
    2   0 0 l ... 0
        ...
    M   0 0 0 ... l
    """
    L = numpy.eye(1+M) * l
    L[0,0] = 0

    return L

def GetError(X, y, w, l):
    """
    X   sample matrix
    y   target variables
    w   model coefficients
    l   regularization parameter
    """

    P = numpy.dot(w, X) - y
    V = w.copy()
    V[0] = 0
    e = numpy.sqrt(numpy.dot(P, P.T) + l * numpy.dot(V, V.T)) / len(y)
    return e

def GetModel(x, y, M, l):
    """
    Polynomial model
        w[0] + w[1]x + w[2]x^2 + ... + w[M]x^M
    Regularization parameter
        l
    """

    X = GetSampleMatrix(x, M)
    L = GetRegularizationMatrix(M, l)

    # Solve XX * w = XY
    XX = numpy.dot(X, X.T) + L
    XY = numpy.dot(X, y)
    w = numpy.linalg.solve(XX, XY)

    e = GetError(X, y, w, l)

    return w, e

def TestRegularization(N, M):
    x, y = GetSamples(N)
    fig.plot(x, y, '+')

    u = numpy.linspace(0,1, 1000)
    t = numpy.sin(2 * numpy.pi * u)
    fig.plot(u, t, label='$\sin(2 \pi x)$')

    for l in numpy.linspace(0, 0.01, num=3):
        w, e = GetModel(x, y, M, l)
        p = numpy.poly1d(w[::-1])
        print(p)

        v = p(u)
        fig.plot(u, v, label='$\lambda$={0}, $e$={1:.3f}'.format(l, e))

    fig.legend()
    fig.show()

if __name__ == "__main__":
    import sys
    TestRegularization(int(sys.argv[1]), int(sys.argv[2]))
