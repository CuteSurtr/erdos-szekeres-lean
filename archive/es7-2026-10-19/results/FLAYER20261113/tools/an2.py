"""Hole patterns of large sets: in-holes, out-holes (and transposes), classified."""
import sys, json
import fl
from fl import *
def pattern_name(H):
    H = set(H)
    H1 = {i for i, f in enumerate(STATES) if f[0] == 4 and f[3] >= 1}
    H2 = {i for i, f in enumerate(STATES) if f[0] == 4 and f[1] <= 3}
    H3 = {i for i, f in enumerate(STATES) if f[3] == 1}
    for nm, X in (('H1', H1), ('H2', H2), ('H3', H3)):
        if H == X: return nm
    return None
if __name__ == '__main__':
    minn = int(sys.argv[1]); pats = {}
    for fn in sys.argv[2:]:
        for rec in load_jsonl(fn):
            P = [tuple(p) for p in rec['P']]
            if len(P) < minn: continue
            S = Set66(P)
            assert S.ok
            hin = tuple(i for i in range(N) if i not in set(S.in_state))
            hout = tuple(i for i in range(N) if i not in set(S.out_state))
            for h in (hin, hout):
                pats[h] = pats.get(h, 0) + 1
                ht = tuple(sorted(TR[i] for i in h)); pats[ht] = pats.get(ht, 0) + 1
    print('distinct hole patterns (incl. out-states and transposes):', len(pats))
    for h, c in sorted(pats.items(), key=lambda kv: -kv[1]):
        print(c, len(h), pattern_name(h), [''.join(map(str, STATES[i])) for i in h])
