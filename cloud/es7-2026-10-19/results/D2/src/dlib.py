"""Shared helpers for the Task D scripts (exact integer arithmetic only)."""
import os, subprocess, json, random, itertools
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.environ.get("DBIN", os.path.join(HERE, "..", "bin"))


def b(name):
    return os.path.join(BIN, name)


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def sgn(v):
    return (v > 0) - (v < 0)


def orient_signs(P):
    n = len(P)
    return [sgn(orient(P[i], P[j], P[k])) for i, j, k in itertools.combinations(range(n), 3)]


def write_pts(path, P):
    with open(path, "w") as f:
        for x, y in P:
            f.write(f"{x} {y}\n")


def read_pts(path):
    P = []
    for line in open(path):
        f = line.split()
        if len(f) >= 2:
            P.append((int(f[0]), int(f[1])))
    return P


def parse_line_pts(fields, nfield_index):
    """fields[nfield_index] = n, followed by n (x,y) pairs"""
    n = int(fields[nfield_index])
    v = fields[nfield_index + 1: nfield_index + 1 + 2 * n]
    return [(int(v[2 * i]), int(v[2 * i + 1])) for i in range(n)]


def integerize(P, target_bits=26, max_bits=29):
    """integer points with exactly the same orientation signs as the exact points P
    (Fractions), centred, extent about 2^target_bits; tries finer scales up to
    2^max_bits.  Returns (Q, scale_exponent) or (None, None)."""
    xs = [p[0] for p in P]; ys = [p[1] for p in P]
    cx = (max(xs) + min(xs)) / 2; cy = (max(ys) + min(ys)) / 2
    ext = max(max(xs) - min(xs), max(ys) - min(ys))
    ref = orient_signs(P)
    for bits in range(target_bits, max_bits + 1):
        s = Fraction(2 ** bits) / ext  # half-extent ~ 2^(bits-1)
        Q = [(round((x - cx) * s), round((y - cy) * s)) for x, y in P]
        if max(max(abs(x), abs(y)) for x, y in Q) >= 2 ** max_bits:
            break
        if orient_signs(Q) == ref:
            return Q, bits
    return None, None


def run(args, inp=None, timeout=None):
    r = subprocess.run(args, input=inp, capture_output=True, text=True, timeout=timeout)
    return r


def cgon_count(P, K):
    inp = "".join(f"{x} {y}\n" for x, y in P)
    r = run([b("cgon"), "count", str(K)], inp)
    out = r.stdout.strip()
    if out.startswith("NOT_GENERAL"):
        return None
    d = {}
    for tok in out.split():
        if tok.startswith("c") and "=" in tok:
            k, v = tok[1:].split("=")
            d[int(k)] = int(v)
    return d


def canon(sets):
    """list of point lists -> list of (canon, canonm) hex strings"""
    inp = "".join(str(len(P)) + " " + " ".join(f"{x} {y}" for x, y in P) + "\n" for P in sets)
    r = run([b("canon")], inp)
    res = []
    for line in r.stdout.splitlines():
        f = line.split()
        res.append((f[0], f[1]) if len(f) == 2 else (None, None))
    return res


def satcount_sweep(path, K, facesout="-", emit=1, cap=3):
    r = run([b("satcount"), "sweep", path, str(K), facesout, str(emit), str(cap)])
    if r.returncode not in (0, 4):
        raise RuntimeError("satcount failed: " + r.stderr[-500:])
    return json.loads(r.stdout.strip().splitlines()[-1])


def read_faces(path):
    """faces file -> list of dicts"""
    res = []
    for line in open(path):
        a, hx, ins = line.split("|")
        f = a.split()
        d = {"m": int(f[0]), "tag": f[1], "t1": int(f[2]), "t2": int(f[3]),
             "ok": int(f[9]), "px": int(f[10]), "py": int(f[11]), "area": float(f[12])}
        d["hex"] = [int(x) for x in hx.split()]
        d["ins"] = int(ins)
        res.append(d)
    return res
