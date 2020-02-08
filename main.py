from random import randint
from sys import getsizeof

etat = {
'black':
{
(1, 7): 'P', (2, 7): 'P', (3, 7): 'P', (4, 7): 'P',
(5, 7): 'P', (6, 7): 'P', (7, 7): 'P', (8, 7): 'P',
(1, 8): 'T', (8, 8): 'T', (7, 8): 'C', (2, 8): 'C',
(3, 8): 'F', (6, 8): 'F', (5, 8): 'K', (4, 8): 'Q'
},
'white':
{
(1, 2): 'P', (2, 2): 'P', (3, 2): 'P', (4, 2): 'P',
(5, 2): 'P', (6, 2): 'P', (7, 2): 'P', (8, 2): 'P',
(1, 1): 'T', (8, 1): 'T', (2, 1): 'C', (7, 1): 'C',
(3, 1): 'F', (6, 1): 'F', (5, 1): 'K', (4, 1): 'Q'
}
}
infinity = 999_999_999_999
pieces = ['BP', 'BQ', 'BK', 'BF', 'BT', 'BC', 'WP', 'WQ', 'WK', 'WF', 'WT', 'WC']
table = {(x, y): {piece: randint(0, infinity) for piece in pieces} for x in range(1, 9) for y in range(1, 9)}
print(table)
colorDico = {'black': 'B', 'white': 'W'}

nums = [table[position][f"{colorDico[color]}"+piece] for color, pieces in etat.items() for position, piece in pieces.items()]
code = nums[0]
for num in nums[1:]:
    code ^= num

print(code)
