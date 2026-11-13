import random, sys
sys.path.insert(0, '.')
from family import *
rng = random.Random(5)
P = realize(witness_tree(8))
k0 = order_type_key(P)[0]
for trial in range(5):
    Q = P[:]
    rng.shuffle(Q)
    a, b, c, d = [rng.randint(-5, 5) for _ in range(4)]
    while a*d - b*c == 0:
        a, b, c, d = [rng.randint(-5, 5) for _ in range(4)]
    Q = [(a*x + b*y + 7, c*x + d*y - 3) for x, y in Q]   # affine (possibly orientation reversing)
    print('affine det sign', (a*d-b*c > 0), order_type_key(Q)[0] == k0)
# a perturbed set should differ: move one point slightly so one triple flips
Q = P[:]
x, y = Q[10]
print('mirror y', order_type_key([(x, -y) for x, y in P])[0] == k0, 'mirror x', order_type_key([(-x, y) for x, y in P])[0] == k0)
print('xorder key: mirror', xorder_key([(-x, y) for x, y in P]) == xorder_key(P), xorder_key([(x, -y) for x, y in P]) == xorder_key(P))
