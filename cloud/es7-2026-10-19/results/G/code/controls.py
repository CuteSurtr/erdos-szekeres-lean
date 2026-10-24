#!/usr/bin/env python3
"""Positive/negative controls for the hull-size split with concrete point sets.

For a point set P (general position): put it in the hull frame (point 1 = lowest point, the
others sorted counterclockwise around it), compute the signotope X with exact arithmetic,
compute the geometric hull size (monotone chain, exact), run verify_sig (brute force over the
signotope: axioms, convex K-subsets, chirotope hull size), and test every hull case CNF with
all X literals as assumptions (cnc_worker "A" jobs). Expected: a heptagon-free (K-gon-free)
set is accepted by exactly the case m = hull_size - 3 (or ge:M if hull_size >= M+3) and
rejected by every other case; a set with a K-gon is rejected by every case.

usage: controls.py N K worker verify_sig case1.cnf[:label] ... -- source
  source: k6 (built-in 16/17-point sets), file:<path>[@sample] (lines 'label tag hash N x1 y1 ...'),
          ae:<json> (AlphaEvolve 33-point set), random:<count>:<seed>
"""
import itertools
import json
import os
import random
import subprocess
import sys
import tempfile
from fractions import Fraction as F


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def hull_frame(P):
    """Return points relabelled: index 0 = lowest (then leftmost) point, others CCW around it."""
    i0 = min(range(len(P)), key=lambda i: (P[i][1], P[i][0]))
    p = P[i0]
    rest = [P[i] for i in range(len(P)) if i != i0]
    import functools

    def cmp(a, b):
        o = orient(p, a, b)
        assert o != 0, 'collinear triple through the pivot'
        return -1 if o > 0 else 1
    rest.sort(key=functools.cmp_to_key(cmp))
    return [p] + rest


def signotope_lits(Q):
    N = len(Q)
    lits = []
    v = 0
    for i, j, k in itertools.combinations(range(N), 3):
        v += 1
        o = orient(Q[i], Q[j], Q[k])
        assert o != 0, 'collinear triple'
        lits.append(v if o > 0 else -v)
    return lits


def geo_hull_size(P):
    pts = sorted(set(P))
    assert len(pts) == len(P)

    def half(seq):
        h = []
        for q in seq:
            while len(h) >= 2 and orient(h[-2], h[-1], q) <= 0:
                h.pop()
            h.append(q)
        return h
    lower = half(pts)
    upper = half(list(reversed(pts)))
    return len(lower) + len(upper) - 2


class Worker:
    def __init__(self, exe, cnf, nX):
        self.p = subprocess.Popen([exe, cnf, str(nX), tempfile.gettempdir()], stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, text=True, bufsize=1)
        line = self.p.stdout.readline()
        assert line.startswith('READY'), line
        self.n = 0

    def accepts(self, lits):
        self.n += 1
        self.p.stdin.write('A %d %s 0\n' % (self.n, ' '.join(map(str, lits))))
        self.p.stdin.flush()
        r = self.p.stdout.readline().split()
        assert r[0] in ('AU', 'AS'), r
        return r[0] == 'AS'


def k6_sets():
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'tools', 'decomp'))
    here = os.getcwd()
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'tools', 'decomp'))
    sys.path.insert(0, os.getcwd())
    import sets  # noqa: E402  (published / classical 16-point sets)
    os.chdir(here)
    out = [('ES6_classical', [(F(x), F(y)) for x, y in sets.ES(6)])]
    # 'four' and 'five' are float coordinates; convert exactly from their float values
    out.append(('four_fold', [(F(x), F(y)) for x, y in sets.four]))
    out.append(('five_fold', [(F(x), F(y)) for x, y in sets.five]))
    return out


def main():
    a = sys.argv[1:]
    N, K = int(a[0]), int(a[1])
    wexe, vexe = a[2], a[3]
    sep = a.index('--')
    cases = a[4:sep]
    source = a[sep + 1]
    nX = N * (N - 1) * (N - 2) // 6
    sets_ = []
    if source == 'k6':
        sets_ = k6_sets()
        rng = random.Random(1)
        # 16-point controls: delete one point from random 17-point sets is not useful (they contain
        # hexagons); use random sets as negative controls instead
        for t in range(20):
            sets_.append((f'random16_{t}', [(F(rng.randint(-10**6, 10**6)), F(rng.randint(-10**6, 10**6))) for _ in range(N)]))
    elif source.startswith('file:'):
        path, *rest = source[5:].split('@')
        limit = int(rest[0]) if rest else None
        lines = open(path).read().split('\n')
        rng = random.Random(7)
        lines = [l for l in lines if l.strip()]
        if limit:
            lines = rng.sample(lines, min(limit, len(lines)))
        for l in lines:
            t = l.split()
            # 'label tag hash N x1 y1 ...' (inputs/distinct_K7*.txt) or 'label hash N x1 y1 ...'
            off = 3 if len(t) == 4 + 2 * int(t[3] if t[3].lstrip('-').isdigit() else -1) else 2
            n = int(t[off])
            xs = list(map(int, t[off + 1:off + 1 + 2 * n]))
            assert len(xs) == 2 * n
            sets_.append((':'.join(t[:off - 1]) + ':' + t[off - 1][:8], [(F(xs[2 * i]), F(xs[2 * i + 1])) for i in range(n)]))
    elif source.startswith('ae:'):
        d = json.load(open(source[3:]))
        P = d['points_7']
        sets_.append(('alphaevolve33', [(F(x), F(y)) for x, y in P]))
    elif source.startswith('random:'):
        _, cnt, seed = source.split(':')
        rng = random.Random(int(seed))
        for t in range(int(cnt)):
            sets_.append((f'random{N}_{t}', [(F(rng.randint(-10**6, 10**6)), F(rng.randint(-10**6, 10**6))) for _ in range(N)]))
    workers = []
    for c in cases:
        path, label = (c.split(':') + [None])[:2]
        workers.append((label or path, Worker(wexe, path, nX)))
    results = []
    bad = 0
    for name, P in sets_:
        assert len(P) == N, (name, len(P))
        try:
            Q = hull_frame(P)
            lits = signotope_lits(Q)
        except AssertionError as e:
            results.append({'set': name, 'skipped': str(e)})
            continue
        gh = geo_hull_size(P)
        with tempfile.NamedTemporaryFile('w', suffix='.lits', delete=False) as f:
            f.write(' '.join(map(str, lits)) + '\n')
            lp = f.name
        vr = json.loads(subprocess.check_output([vexe, str(N), str(K), lp], text=True))
        os.unlink(lp)
        acc = {lab: w.accepts(lits) for lab, w in workers}
        # expected acceptance
        exp = {}
        for lab, _ in workers:
            case = lab.split('=')[-1]
            if vr['convex_K'] > 0:
                exp[lab] = False
            elif case.startswith('ge'):
                exp[lab] = gh - 3 >= int(case[2:])
            else:
                exp[lab] = gh - 3 == int(case)
        ok = (vr['axiom_violations'] == 0 and vr['hull_frame_ok'] and vr['hull_size'] == gh and acc == exp)
        bad += not ok
        results.append({'set': name, 'geo_hull': gh, 'sig_hull': vr['hull_size'], 'convex_K': vr['convex_K'],
                        'axiom_violations': vr['axiom_violations'], 'accepted': [l for l in acc if acc[l]], 'ok': ok})
    summary = {'N': N, 'K': K, 'source': source, 'sets': len(results), 'failures': bad,
               'skipped': sum('skipped' in r for r in results),
               'hull_hist': {}, 'kgon_free': sum(r.get('convex_K', 1) == 0 for r in results)}
    for r in results:
        if 'geo_hull' in r and r['convex_K'] == 0:
            summary['hull_hist'][str(r['geo_hull'])] = summary['hull_hist'].get(str(r['geo_hull']), 0) + 1
    print(json.dumps(summary))
    for r in results:
        print(json.dumps(r))


if __name__ == '__main__':
    main()
