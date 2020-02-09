from itertools import product

b = list(product([-1, 1], [-2, 2])) + list(product([-2, 2], [-1, 1]))
print(b)

