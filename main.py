from itertools import product, chain

x, y = 2, 6
liste = [(x+dx, y+dy) for dx, dy in chain(product((-1, 1), (-2, 2)), product((-2, 2), (-1, 1)))]
print(liste)
