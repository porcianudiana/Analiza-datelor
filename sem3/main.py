import numpy as np

a = np.array([1, 2, 3])
print(a)
print(type(a))
print(type(a[0]))

a = np.array([1, 2, 3], dtype='int16')
print(a)
print(type(a))
print(type(a[0]))

b = np.array([[5.4, 3.2], [7.4, 1.7], [7.7, 3.7]])
print(b)
print(type(b))
print(type(b[0][0]))


print(a.ndim)
print(b.ndim)

print(a.dtype)
print(b.dtype)

print(a.itemsize)
print(b.itemsize)

print(a.size)
print(b.size)

print(a.size * a.itemsize)
print(b.size * b.itemsize)
print(a.nbytes)
print(b.nbytes)

print(a.shape)
print(b.shape)

a = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])
print(a[1][2])
a[1][2] = 20
print(a[1, 2])

print(a[0, 1:-1])
# slicing [startindex:endindex:stepsize]
print(a[0, 1:-1:2])
print(a[0, ::2])
print(a[0, :])
print(a[:, 3])
print(a[:-1, 3])

z = np.zeros((4, 6))
print(z)

o = np.ones((2, 2, 2), dtype='int16')
print(o)

f = np.full((2, 2), 66)
print(f)

r = np.random.rand(2, 2)
print(r)

ri = np.random.randint(-50, 2, size=(3, 3))
print(ri)

i = np.identity(6)
print(i)


a = np.array([[1, 2, 3]])
rep = np.repeat(a, 3, axis=0)
print(rep)

a = np.array([[1, 2, 3]])
b = a
b[0, 0] = 50
print(a)
print(b)

c = a.copy()
c[0, 0] = 10
print(a)
print(b)
print(c)
