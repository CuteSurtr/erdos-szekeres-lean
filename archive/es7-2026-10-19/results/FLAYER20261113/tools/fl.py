"""FLAYER core: exact analysis of (6,6;8)-sets (no 6-cap, no 6-cup, no convex octagon) and their
internal states (catalog ETV_A=4, ETV_B=4 of etv_common.py: 70 Young diagrams in the 4x4 box)."""
import os, sys, json
os.environ['ETV_A'] = '4'; os.environ['ETV_B'] = '4'
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import etv_common as ec
from esgeo import Analysis, quick
assert ec.A == 4 and ec.B == 4 and ec.N == 70
STATES = ec.STATES; SINDEX = ec.SINDEX; N = ec.N

def transpose(f):
    """Young diagram transpose (column heights -> row lengths): the state of the y-mirror image."""
    return tuple(sum(1 for x in f if x >= r) for r in range(1, 5))
TR = [SINDEX[transpose(f)] for f in STATES]

def valid(P, capmax=5, cupmax=5, gonmax=7):
    g, mc, mu = quick(P)
    return g >= 0 and g <= gonmax and mc <= capmax and mu <= cupmax

def state_of(capE, cupE, v, A=4):
    f = [0] * A
    for u in range(v):
        a = int(capE[u, v]) - 1; b = int(cupE[u, v]) - 1
        for c in range(min(a, A)):
            if f[c] < b: f[c] = b
    return tuple(f)

class Set66:
    """P: list of integer points.  Raises ValueError if not general / not distinct x.
    in_state[v]  = index of the incoming state I(v)  (labels (capE-1, cupE-1) of pairs (u,v), u<v)
    out_state[v] = index of the outgoing state O(v)  (labels (capS-1, cupS-1) of pairs (v,w), v<w),
                   i.e. the incoming state of v in the x-reversed set."""
    def __init__(self, P):
        self.A = A = Analysis(P); self.P = A.P; n = self.n = A.n
        self.maxcap = int(A.capB.max()) if n >= 2 else 1
        self.maxcup = int(A.cupB.max()) if n >= 2 else 1
        self.gon = int((A.capB + A.cupB).max() - 2) if n >= 2 else n
        self.ok = self.maxcap <= 5 and self.maxcup <= 5 and self.gon <= 7
        if not self.ok: return
        self.in_f = [state_of(A.capE, A.cupE, v) for v in range(n)]
        outf = []
        for v in range(n):
            f = [0] * 4
            for w in range(v + 1, n):
                a = int(A.capS[v, w]) - 1; b = int(A.cupS[v, w]) - 1
                for c in range(a):
                    if f[c] < b: f[c] = b
            outf.append(tuple(f))
        self.out_f = outf
        self.in_state = [SINDEX[f] for f in self.in_f]
        self.out_state = [SINDEX[f] for f in self.out_f]
    def occ(self): return sorted(set(self.in_state))
    def occ_out(self): return sorted(set(self.out_state))

def load_jsonl(fn):
    out = []
    if os.path.exists(fn):
        for line in open(fn):
            line = line.strip()
            if line: out.append(json.loads(line))
    return out
