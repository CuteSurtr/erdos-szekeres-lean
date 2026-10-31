#!/usr/bin/env python3
"""Signotope-level brute-force checker (independent of the CNF): given chi on all triples of
0..n-1 (True = counter-clockwise = cup triple), check
  * signotope axiom on every 4-subset (monotone sign sequence abc,abd,acd,bcd),
  * mirror rule chi(m-k,m-j,m-i) == chi(i,j,k),
  * no convex k-gon, two ways that must agree:
    (a) exhaustive DFS over subsets in convex position, where 4 points a<b<c<d are in convex
        position iff b is not inside acd (-chi(abc)=chi(abd)=chi(bcd)) and c is not inside
        abd (chi(abc)=chi(acd)=-chi(bcd)), and a set is convex iff all its 4-subsets are;
    (b) exhaustive DFS over cups and caps from each leftmost point p (chains up to k points),
        looking for a cup p..q of s points and a cap p..q of t points with s+t-2 >= k."""
import itertools

def check(n, chi, k, mirror=True):
    res = dict(ok=True)
    for q in itertools.combinations(range(n), 4):
        s = [chi[t] for t in itertools.combinations(q, 3)]
        flips = sum(s[i] != s[i + 1] for i in range(3))
        if flips > 1: res['ok'] = False; res['axiom'] = q; return res
    if mirror:
        m = n - 1
        for (i, j, l), v in chi.items():
            if chi[(m - l, m - j, m - i)] != v: res['ok'] = False; res['mirror'] = (i, j, l); return res
    gon = find_gon(n, chi, k); g4 = find_gon4(n, chi, k)
    if bool(gon) != bool(g4): res['ok'] = False; res['disagree'] = (gon, g4); return res
    if gon: res['ok'] = False; res['gon'] = g4
    return res

def convex4(chi, a, b, c, d):
    x, y, z, w = chi[(a, b, c)], chi[(a, b, d)], chi[(a, c, d)], chi[(b, c, d)]
    return not ((not x) == y == w) and not (x == z == (not w))

def find_gon4(n, chi, k):
    S = []
    def ok(r):
        for a, b, c in itertools.combinations(S, 3):
            if not convex4(chi, a, b, c, r): return False
        return True
    def dfs(frm):
        if len(S) >= k: return list(S)
        for r in range(frm, n):
            if len(S) + (n - r) < k: return None
            if ok(r):
                S.append(r); g = dfs(r + 1); S.pop()
                if g: return g
        return None
    return dfs(0)

def chains(n, chi, p, sign, k):
    """all chains p=c0<c1<...  with every consecutive triple of orientation `sign`;
    yields (chain) — exhaustive."""
    out = {}
    def dfs(ch):
        q = ch[-1]
        out.setdefault(q, []).append(tuple(ch))
        for r in range(q + 1, n):
            if len(ch) < k and (len(ch) < 2 or chi[(ch[-2], q, r)] == sign):
                ch.append(r); dfs(ch); ch.pop()
    dfs([p]); return out

def find_gon(n, chi, k):
    for p in range(n):
        cups = chains(n, chi, p, True, k); caps = chains(n, chi, p, False, k)
        for q in range(p + 1, n):
            su = max((len(c) for c in cups.get(q, [])), default=0)
            sa = max((len(c) for c in caps.get(q, [])), default=0)
            if su + sa - 2 >= k:
                return (p, q, su, sa)
    return None
