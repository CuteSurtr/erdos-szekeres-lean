"""Recursive (ES-style) constructions in the simplified classes model:
   cups with all angles < e have <= u[e] points (e=2..h+1), caps with all angles >= s have <= w[s] points (s=1..h).
   Original system: u[e] = min(e,h), w[s] = h+2-s.  Recursion: root at the max (or min) angle of its subtree, in class k;
   max-root: L gets u[e]-1 for e>k, R gets w[s]-1 for s<=k, both confined to classes [lo,k];
   min-root: R gets u[e]-1 for e>k, L gets w[s]-1 for s<=k, both confined to classes [k,hi].
   Returns the best size and a construction."""
import sys, functools
sys.setrecursionlimit(10000)
def solve(h):
    @functools.lru_cache(maxsize=None)
    def N(u, w, lo, hi):
        # u: tuple indexed e=2..h+1 -> u[e-2]; w: tuple indexed s=1..h -> w[s-1]
        if min(u) < 1 or min(w) < 1: return (0, None)
        best = (1, 'o')
        for k in range(lo, hi + 1):
            # root edge is a cup edge for e > k and a cap edge for s <= k
            if any(u[e - 2] < 2 for e in range(k + 1, h + 2)) or any(w[s - 1] < 2 for s in range(1, k + 1)): continue
            uk = tuple(u[e - 2] - (1 if e > k else 0) for e in range(2, h + 2))
            wk = tuple(w[s - 1] - (1 if s <= k else 0) for s in range(1, h + 1))
            a = N(uk, w, lo, k); b = N(u, wk, lo, k)          # max-root: L=(uk,w), R=(u,wk)
            if a[0] and b[0] and a[0] + b[0] > best[0]: best = (a[0] + b[0], ('max', k, a[1], b[1]))
            a = N(u, wk, k, hi); b = N(uk, w, k, hi)          # min-root: L=(u,wk), R=(uk,w)
            if a[0] and b[0] and a[0] + b[0] > best[0]: best = (a[0] + b[0], ('min', k, a[1], b[1]))
        return best
    u0 = tuple(min(e, h) for e in range(2, h + 2)); w0 = tuple(h + 2 - s for s in range(1, h + 1))
    return N(u0, w0, 1, h)
if __name__ == '__main__':
    # optional argument: largest h (default 7; h = 7 needs about 2.3 GB of memory, h <= 6 under 200 MB)
    for h in range(1, (int(sys.argv[1]) if len(sys.argv) > 1 else 7) + 1):
        v, c = solve(h)
        p = 2 * h + 1
        print('h=%d p=%d: recursive max/min construction size %d ; target (2^(p-1)-1)/p = %s' % (h, p, v, (2 ** (p - 1) - 1) / p))
