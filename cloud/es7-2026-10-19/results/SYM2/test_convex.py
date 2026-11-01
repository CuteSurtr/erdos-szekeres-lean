import random, sys
sys.path.insert(0, ".")
from convex import max_convex, max_convex_brute, collinear_triples
random.seed(1)
bad = 0
for t in range(300):
    n = random.randint(4, 11)
    while True:
        P = [(random.randint(-40, 40), random.randint(-40, 40)) for _ in range(n)]
        if len(set(P)) == n and not collinear_triples(P):
            break
    a, b = max_convex(P), max_convex_brute(P)
    if a != b:
        bad += 1; print("MISMATCH", P, a, b)
print("tests 300, mismatches", bad)
