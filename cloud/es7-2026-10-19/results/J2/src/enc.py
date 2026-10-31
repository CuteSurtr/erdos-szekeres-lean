"""Lossy multi-scale encoding of planar point sets (task J2).

A set is rotated by a random angle (optionally reflected; neither changes the
number of convex k-gons), scaled so its x-extent is 2^24, and sorted by x.
Each consecutive gap (dx, dy) becomes four tokens: for dx > 0 the integer part
of log2 dx and its fractional part in 256 bins; for dy the sign with the integer
part, then the fractional bin.  Sequence: [BOS_n] ex1 mx1 ey1 my1 ex2 ...
Decoding takes cumulative sums with a random offset inside each quantization
cell.  Some orientation signs still flip (cell width 1/256 octave), so
decoded sets are starting points for exact local search, not exact copies.
"""
import math, random
import numpy as np

MB = 256                          # mantissa bins per octave (8 bits)
EMAX = 31                         # exponents 0..EMAX-1 (integer part of log2)
EX0 = 0                           # dx exponent tokens [0, EMAX)
EY0 = EMAX                        # dy exponent tokens [EMAX, 3*EMAX): +, then -
M0 = 3 * EMAX                     # mantissa tokens [M0, M0+MB)
BOS = {32: M0 + MB, 33: M0 + MB + 1}
VOCAB = M0 + MB + 2
SEQ = 1 + 4 * 32                  # longest sequence (33 points)
# allowed token range per position class (position p >= 1, (p-1) % 4)
RANGES = [(EX0, EX0 + EMAX), (M0, M0 + MB), (EY0, EY0 + 2 * EMAX), (M0, M0 + MB)]


def split(v):
    """v >= 1 -> (exponent, mantissa bin) with log2 v ~ e + (m+0.5)/MB"""
    l = math.log2(max(v, 1.0))
    t = int(l * MB)
    t = min(max(t, 0), EMAX * MB - 1)
    return t // MB, t % MB


def encode(P, rng=random, rotate=True):
    P = np.asarray(P, dtype=np.float64)
    P = P - P.mean(0)
    if rotate:
        th = rng.uniform(0, 2 * math.pi)
        c, s = math.cos(th), math.sin(th)
        P = P @ np.array([[c, -s], [s, c]]).T
        if rng.random() < 0.5:
            P[:, 1] = -P[:, 1]
    P = P[np.argsort(P[:, 0], kind='stable')]
    ext = P[-1, 0] - P[0, 0]
    P = P * (2.0 ** 24 / ext)
    toks = [BOS[len(P)]]
    for i in range(1, len(P)):
        dx = P[i, 0] - P[i - 1, 0]
        dy = P[i, 1] - P[i - 1, 1]
        e, m = split(dx)
        toks += [EX0 + e, M0 + m]
        e, m = split(abs(dy))
        toks += [EY0 + e + (EMAX if dy < 0 else 0), M0 + m]
    return toks


def decode(toks, rng=random):
    x = y = 0.0
    pts = [(0.0, 0.0)]
    body = toks[1:]
    if len(body) % 4:
        return None
    for i in range(0, len(body), 4):
        a, ma, b, mb = body[i:i + 4]
        for t, (lo, hi) in zip((a, ma, b, mb), RANGES):
            if not lo <= t < hi:
                return None
        x += 2.0 ** (a - EX0 + (ma - M0 + rng.random()) / MB)
        bb = b - EY0
        sg = -1.0 if bb >= EMAX else 1.0
        y += sg * 2.0 ** (bb % EMAX + (mb - M0 + rng.random()) / MB)
        pts.append((x, y))
    P = np.array(pts)
    P -= (P.max(0) + P.min(0)) / 2
    m = np.abs(P).max()
    if m > 2.0 ** 25:
        P *= 2.0 ** 25 / m
    return [(int(round(a)), int(round(b))) for a, b in P]


def load_sets(path):
    """lines 'label [label2] [hash] n x1 y1 ...' -> list of integer point lists"""
    out = []
    for line in open(path):
        t = line.split()
        for k in range(1, 4):
            if t[k].isdigit() and int(t[k]) in (32, 33) and len(t) == k + 1 + 2 * int(t[k]):
                n = int(t[k])
                c = list(map(int, t[k + 1:]))
                out.append([(c[2 * i], c[2 * i + 1]) for i in range(n)])
                break
    return out
