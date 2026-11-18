"""ONLINE version of the Delta-reduction statement as a game (exact minimax, COMPUTED).
The adversary reveals a signotope with no a-cap and no convex n-gon point by point from left to right (each new
point with all its triple signs); the colourer must decide irrevocably, when a point arrives, whether it belongs to
Delta.  The colourer loses as soon as Delta contains an (a-1)-cap or some convex (n-1)-gon misses Delta
(strong form: or Delta contains a convex (n-1)-gon).  The game stops after `depth` points (or when no valid
extension exists).  Output: who wins; if the adversary wins, a winning adversary strategy tree is saved.
usage: online_game.py a n depth weak|strong"""
import sys, itertools, json, time
sys.setrecursionlimit(10000)
comb = itertools.combinations
a, n, depth, form = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
strong = form == 'strong'; b = a - 1; g = n - 1

def tri_index(i, j, k): return k * (k - 1) * (k - 2) // 6 + j * (j - 1) // 2 + i      # colex rank: prefix-stable

def extensions(sig, k):
    """All sign vectors for the triples (i,j,k), i<j<k, extending the signotope sig on points 0..k-1."""
    pairs = [(i, j) for j in range(k) for i in range(j)]          # ordered so that (x,y),(x,z) come before (y,z)
    pairs.sort(key=lambda p: (p[1], p[0]))
    new = {}; out = []
    def ok(y, z):
        for x in range(y):
            s = (sig[tri_index(x, y, z)], new[x, y], new[x, z], new[y, z])
            ch = (s[0] != s[1]) + (s[1] != s[2]) + (s[2] != s[3])
            if ch > 1: return False
        return True
    def rec(t):
        if t == len(pairs): out.append(tuple(new[p] for p in pairs)); return
        y, z = pairs[t]
        for v in (True, False):
            new[y, z] = v
            if ok(y, z): rec(t + 1)
        del new[y, z]
    rec(0)
    return pairs, out

def chains_end(sig, k, pts, cap):
    """longest cap (cap=True) / cup chains inside pts (sorted, last = k) ending with edge (i,k): dict i -> length"""
    E = {}
    for bi in range(len(pts)):
        for ai in range(bi):
            i, j = pts[ai], pts[bi]; best = 2
            for ci in range(ai):
                h = pts[ci]
                if (sig[tri_index(h, i, j)] != cap) and E[h, i] + 1 > best: best = E[h, i] + 1     # sign False = cap
            E[i, j] = best
    return E

def max_gon_at(sig, pts):
    """largest convex polygon with right end pts[-1] inside pts (weak gon = cap + cup with common ends)"""
    k = pts[-1]; best = 0
    for si in range(len(pts) - 1):
        sub = pts[si:]; s = sub[0]
        Dc = {}; Du = {}
        for bi in range(1, len(sub)):
            j = sub[bi]; Dc[s, j] = 2; Du[s, j] = 2
        for bi in range(1, len(sub)):
            for ai in range(1, bi):
                i, j = sub[ai], sub[bi]; bc = bu = 0
                for ci in range(ai):
                    h = sub[ci]
                    if (h, i) not in Dc: continue
                    if not sig[tri_index(h, i, j)]:
                        if Dc[h, i]: bc = max(bc, Dc[h, i] + 1)
                    else:
                        if Du[h, i]: bu = max(bu, Du[h, i] + 1)
                Dc[i, j] = bc; Du[i, j] = bu
        cb = max(Dc.get((i, k), 0) for i in sub[:-1]); ub = max(Du.get((i, k), 0) for i in sub[:-1])
        if cb >= 2 and ub >= 2: best = max(best, cb + ub - 2)
    return best

def valid_ext(sig, k):
    pts = list(range(k + 1))
    E = chains_end(sig, k, pts, True)
    if max([1] + [E[i, k] for i in range(k)]) >= a: return False
    return max_gon_at(sig, pts) < n

memo = {}; stats = {'states': 0}
def colourer_wins(sig, k, col):
    """sig: signs on points 0..k-1 (tuple, colex), col: bitmask of Delta.  True if the colourer survives to `depth`."""
    if k == depth: return True
    key = (sig, col)
    if key in memo: return memo[key]
    stats['states'] += 1
    pairs, exts = extensions(sig, k)
    res = True
    for e in exts:
        sig2 = sig + e                       # colex order: triples with largest element k come last, ordered by (j,i)
        if not valid_ext(sig2, k): continue
        okc = False
        black = [p for p in range(k) if col >> p & 1] + [k]; white = [p for p in range(k) if not col >> p & 1] + [k]
        # option: k in Delta
        Eb = chains_end(sig2, k, black, True)
        if max([1] + [Eb[i, k] for i in black[:-1]]) < b and not (strong and len(black) >= g and max_gon_at(sig2, black) >= g):
            if colourer_wins(sig2, k + 1, col | 1 << k): okc = True
        if not okc:
            if not (len(white) >= g and max_gon_at(sig2, white) >= g):
                if colourer_wins(sig2, k + 1, col): okc = True
        if not okc: res = False; break
    memo[key] = res
    return res

t0 = time.time()
w = colourer_wins((), 0, 0)
print('online game a=%d n=%d %s depth %d: %s wins; states %d; %.1fs' % (a, n, form, depth, 'COLOURER' if w else 'ADVERSARY', stats['states'], time.time() - t0), flush=True)
