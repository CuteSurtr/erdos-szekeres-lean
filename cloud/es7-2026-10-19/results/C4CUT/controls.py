"""Controls for c4cut.py's certificate search: GP identity signs, realizable sets (no certificate), minimal12 (certificate)."""
import json, random, sys
from fractions import Fraction
C, MIN12 = sys.argv[1], sys.argv[2]
sys.argv = ["c4cut.py", C, "unused", "0"]
src = open(C + "/c4cut.py").read().split("cuts = [json.loads")[0]
exec(src)
det = lambda P, a, b, c: (P[b][0]-P[a][0])*(P[c][1]-P[a][1]) - (P[b][1]-P[a][1])*(P[c][0]-P[a][0])
# 1. GP identity with the code's term signs
rnd = random.Random(1)
for _ in range(2000):
    P = {i: (rnd.randint(-10**6, 10**6), rnd.randint(-10**6, 10**6)) for i in range(5)}
    a, b, c, d, e = range(5)
    assert det(P,a,b,c)*det(P,a,d,e) - det(P,a,b,d)*det(P,a,c,e) + det(P,a,b,e)*det(P,a,c,d) == 0
print("1. GP identity [abc][ade] - [abd][ace] + [abe][acd] = 0: 2000/2000 random integer checks")
# 2. realizable sets: no certificate
def use_points(P):
    global chi_of
    sgn = lambda x: (x > 0) - (x < 0)
    g = globals(); g["chi_of"] = lambda model, a, b, c: sgn(det(P, a, b, c))
found = 0
for trial in range(20):
    P = {i: (rnd.randint(-10**4, 10**4), rnd.randint(-10**4, 10**4)) for i in range(12)}
    use_points(P)
    try:
        cert, n = certificate(None, list(range(12)))
    except ValueError:
        continue
    found += cert is not None
print(f"2. random real 12-point sets: certificate found in {found}/20 (must be 0)")
# 3. minimal12: sign table from the four deletion coordinate columns
m = json.load(open(MIN12))
cols = [{lab: (x, y) for lab, x, y in w["points"]} for w in m["deletion_witnesses"]]
def chi12(model, a, b, c):
    for col in cols:
        if a in col and b in col and c in col:
            x = det(col, a, b, c); return (x > 0) - (x < 0)
    raise KeyError
globals()["chi_of"] = chi12
cert, n = certificate(None, m["labels"])
ok = cert is not None and not isinstance(cert, str)
if ok: verify(None, cert)
print(f"3. minimal12 (known nonrealizable): certificate {'found, ' + str(len(cert)) + ' rows, exact re-check passed' if ok else 'NOT found'}")
