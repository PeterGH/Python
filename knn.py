import numpy

model_size = 1000

def GetModel():
    x = numpy.random.multivariate_normal([2,2],[[1,0],[0,1]],model_size)
    y = numpy.random.multivariate_normal([4,4],[[1,0],[0,1]],model_size)
    return x,y

def Categorize(x, y, m):
    # Compute distances
    dx = numpy.sqrt(numpy.sum(numpy.square(x[:,:] - m), axis=1))
    dy = numpy.sqrt(numpy.sum(numpy.square(y[:,:] - m), axis=1))
    # Tag distances with known categorization
    xx = numpy.array([dx,numpy.zeros(model_size)])
    yy = numpy.array([dy,numpy.ones(model_size)])
    # Sort by distances
    zz = numpy.concatenate((xx, yy), axis = 1)
    z0,z1 = zz
    ind = numpy.lexsort((z1,z0))
    s = [(z0[i],z1[i]) for i in ind]
    # Take 101 nearest neighbors to categorize m
    s0,s1 = zip(*s)
    k = 101
    n = numpy.count_nonzero(s1[0:k])
    c = 0
    if n > 50:
        c = 1

    return c

if __name__ == "__main__":
    import matplotlib.pyplot as fig
    x,y = GetModel()
    fig.plot(x[:,0], x[:,1],'b.')
    fig.plot(y[:,0], y[:,1],'b.')
    for i in range(0,1000):
        m = 6 * numpy.random.rand(2)
        c = Categorize(x, y, m)
        if c == 0:
            fig.plot(m[0],m[1],'r.')
        else:
            fig.plot(m[0],m[1],'g.')

    fig.show()

