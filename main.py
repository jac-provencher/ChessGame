from more_itertools import take, tail
x, y = 2, 5

vectors = {
'N': (0, 1), 'S': (0, -1), 'O': (-1, 0), 'E': (1, 0),
'NE': (1, 1), 'SE': (1, -1), 'SO': (-1, -1), 'NO': (-1, 1)
}

q = [[(x+i*n, y+j*n) for n in range(1, 9)] for i, j in vectors.values()]
f = [[(x+i*n, y+j*n) for n in range(1, 9)] for i, j in tail(4, vectors.values())]
t = [[(x+i*n, y+j*n) for n in range(1, 9)] for i, j in take(4, vectors.values())]

print(q)
print(f)
print(t)
