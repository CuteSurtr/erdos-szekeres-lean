#!/usr/bin/env python3
"""Independent exact audit. Imports no encoder, finder, or earlier checker."""
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations as C, permutations
import json
from pathlib import Path
import resource
import subprocess
import time

HERE = Path(__file__).resolve().parent
SCRATCH = Path('/home/jay/research/data/delta3-codex-20261113/boundary')


def digest(p):
    h = sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def mask(s):
    return sum(1 << i for i in s)


def vertices(s):
    return tuple(i for i in range(s.bit_length()) if s >> i & 1)


def det(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])


class Geometry:
    def __init__(self, points):
        self.p = tuple(map(tuple, points))
        self.m = len(self.p)
        assert all(self.p[i][0] < self.p[i+1][0] for i in range(self.m-1))
        self.d = {t: det(*(self.p[i] for i in t)) for t in C(range(self.m), 3)}
        assert all(self.d.values()), 'collinear triple'

    def cup(self, s):
        return all(self.d[t] > 0 for t in C(s, 3))

    def cap(self, s):
        return all(self.d[t] < 0 for t in C(s, 3))

    def chains(self, s):
        # Independent monotone hull; the encoder uses four-point recurrences.
        lower, upper = [], []
        for i in s:
            for chain, sign in ((lower, 1), (upper, -1)):
                while len(chain) >= 2 and sign*det(self.p[chain[-2]], self.p[chain[-1]], self.p[i]) <= 0:
                    chain.pop()
                chain.append(i)
        return tuple(lower), tuple(upper)

    def convex(self, s):
        if len(s) < 3:
            return True
        lo, hi = self.chains(s)
        return len(lo)+len(hi)-2 == len(s)

    def convex_by_triangles(self, s):
        for t in C(s, 3):
            for i in set(s)-set(t):
                ds = [det(self.p[t[j]], self.p[t[(j+1)%3]], self.p[i]) for j in range(3)]
                if all(x > 0 for x in ds) or all(x < 0 for x in ds):
                    return False
        return True

    def maxcup(self):
        best = min(2, self.m)
        for k in range(3, self.m+1):
            if not any(self.cup(t) for t in C(range(self.m), k)):
                break
            best = k
        return best

    def ranks(self):
        end, start = [1]*self.m, [1]*self.m
        h = {t: 2 for t in C(range(self.m), 2)}
        for k in range(2, self.m+1):
            for t in C(range(self.m), k):
                if self.cup(t):
                    end[t[-1]] = max(end[t[-1]], k)
                    start[t[0]] = max(start[t[0]], k)
                if self.cap(t):
                    h[t[-2:]] = max(h[t[-2:]], k)
        return end, start, h

    def weak(self, A, n):
        return (not any(self.cap(t) for t in C(sorted(A), 4)) and
                all(set(t) & set(A) for t in C(range(self.m), n-1) if self.convex(t)))


def bounded(g, n):
    assert g.m <= 2*n-3
    u = Geometry(g.p[:-1])
    cup = next((t for t in C(range(u.m), n-2) if u.cup(t)), None)
    if cup is not None:
        a, branch = cup, 'cup'
    else:
        a = tuple(sorted({t[-1] for t in C(range(u.m), n-1) if u.convex(t)}))
        branch = 'endpoint'
    assert u.weak(a, n) and g.weak(tuple(a)+(g.m-1,), n)
    cap4 = [t for t in C(range(u.m), 4) if u.cap(t)]
    assert all(any(q[-2:] == t[-2:] for q in cap4) for t in C(a, 3) if u.cap(t))
    return dict(branch=branch, selected_old=a, nonempty=bool(a))


def fixture(path):
    doc = json.loads(path.read_text())
    n = doc['n']
    assert all(type(x) is int for p in doc['P'] for x in p)
    g = Geometry(doc['P'])
    u = Geometry(g.p[:-1])
    assert g.m == 2*n-2 and u.m == 2*n-3
    signs = ''.join('+' if g.d[t] > 0 else '-' for t in C(range(g.m), 3))
    assert signs == doc['signs']
    assert not any(g.cap(t) for t in C(range(g.m), 5))
    assert not any(g.convex(t) for t in C(range(g.m), n))
    assert u.maxcup() == n-2
    cups = [t for t in C(range(u.m), n-2) if u.cup(t)]
    chain_counts = Counter()
    for t in cups:
        b = tuple(i for i in range(u.m) if i not in t)
        assert u.convex(b) and u.convex_by_triangles(b)
        lo, hi = u.chains(b)
        chain_counts[f'{len(hi)},{len(lo)}'] += 1
        assert (len(hi), len(lo)) in ((3, n-2), (4, n-3))
    fullmax = g.maxcup()
    if 'refined' in path.name:
        assert fullmax == n-2
    else:
        assert fullmax >= n-1
    bound_right = bounded(u, n)
    bound_left = bounded(Geometry(tuple((-x, y) for x, y in reversed(u.p))), n)
    # Exact rational sign check for the displayed projective normalization.
    xr, yr = g.p[-1]
    q = [(Fraction(x-xr+1), Fraction(y-yr)) for x, y in u.p]
    image = [(x/(1-x), y/(1-x)) for x, y in q]
    for t in C(range(u.m), 3):
        assert det(*(image[i] for i in t)) == det(*(q[i] for i in t))/__import__('math').prod(1-q[i][0] for i in t)
    for a, b in C(range(u.m), 2):
        d = det(q[a], q[b], (1, 0))
        assert image[b][1]-image[a][1] == -d/((1-q[a][0])*(1-q[b][0]))
    return dict(path=str(path), sha256=digest(path), n=n, m=g.m,
                minimum_absolute_determinant=min(map(abs, g.d.values())),
                max_old_cup=n-2, max_full_cup=fullmax, maximum_cups=len(cups),
                complementary_upper_lower=dict(chain_counts), signs_match=True,
                no5cap=True, no_ngon=True, all_complements_convex=True,
                bounded_prefix_right=bound_right, bounded_prefix_left_reflected=bound_left)


def small_controls():
    counts = Counter()
    mutations = {}
    for ys in permutations(range(6)):
        points = tuple(enumerate(ys))
        if any(det(*(points[i] for i in t)) == 0 for t in C(range(6), 3)):
            continue
        g = Geometry(points)
        beta, start, h = g.ranks()
        mirror = Geometry(tuple((-x, y) for x, y in reversed(points)))
        mbeta, mstart, _ = mirror.ranks()
        assert beta == list(reversed(mstart)) and start == list(reversed(mbeta))
        counts['general_position_six_point_permutations'] += 1
        for t, d in g.d.items():
            assert d == mirror.d[tuple(5-i for i in reversed(t))]
            counts['reflected_triples'] += 1
            a, b, c = t
            if d < 0 and beta[a] >= beta[b]:
                assert h[(b, c)] >= 4
                counts['rank_lemma_premises'] += 1
            if d < 0 and h[(b, c)] == 3:
                assert beta[a] < beta[b]
                counts['rank_three_triples'] += 1
            if d < 0 and beta[a] <= beta[b] and h[(b, c)] < 4:
                mutations.setdefault('reversed_rank_inequality', dict(points=points, triple=t, beta=beta, rank=h[(b, c)]))
        if beta != list(reversed(mbeta)):
            mutations.setdefault('ending_rank_does_not_reflect_to_ending_rank', dict(points=points, beta=beta, mirror_beta=mbeta))
        no5 = not any(g.cap(t) for t in C(range(6), 5))
        if no5:
            b = bounded(g, 6)
            counts['bounded_'+b['branch']] += 1
            if b['branch'] == 'endpoint' and b['nonempty']:
                counts['nonvacuous_bounded_endpoint'] += 1
            for bits in range(1 << 6):
                a = vertices(bits)
                if any(beta[x] < beta[y] for x, y in zip(a, a[1:])):
                    continue
                assert not any(g.cap(t) for t in C(a, 4))
                assert all(h[t[1:]] >= 4 for t in C(a, 3) if g.cap(t))
                counts['nonincreasing_rank_selections'] += 1
        for t in C(range(6), 4):
            assert g.convex(t) == g.convex_by_triangles(t)
            assert g.cup(t) == all(g.d[t[i:i+3]] > 0 for i in range(2))
            assert g.cap(t) == all(g.d[t[i:i+3]] < 0 for i in range(2))
            counts['fourpoint_cross_checks'] += 1
    assert len(mutations) == 2 and counts['rank_lemma_premises'] > 0
    return dict(counts=dict(counts), rejected_mutations=mutations)


def load_cnf(case):
    maps = {}
    for line in (case/'input.cnf.map').read_text().splitlines():
        if line and not line.startswith('#'):
            v, kind, bits = line.split()
            maps[int(v)] = (kind, vertices(int(bits)))
    phases = {}
    header = None
    for line in (case/'input.cnf').read_text().splitlines():
        if line.startswith('p '):
            _, _, nv, nc = line.split()
            header = int(nv), int(nc)
        elif line.startswith('c phase '):
            phase = line.split()[-1]
            assert phase not in phases
            phases[phase] = []
        elif line and not line.startswith('c'):
            row = tuple(map(int, line.split()))
            assert row[-1] == 0 and 0 not in row[:-1]
            phases[phase].append(row[:-1])
    assert header == (len(maps), sum(map(len, phases.values())))
    assert set(maps) == set(range(1, header[0]+1))
    assert all(abs(x) in maps for rows in phases.values() for row in rows for x in row)
    return maps, phases


def independent_rows(n, maps, phases):
    by = {value: key for key, value in maps.items()}
    m = 2*n-3
    orient = lambda t: by['orientation', tuple(t)]
    expected = {}
    def equiv(z, literals, rows):
        rows.extend([(-z, x) for x in literals])
        rows.append(tuple([z]+[-x for x in literals]))
    cups = list(C(range(m), n-2))
    rows = []
    for t in cups:
        equiv(by['cup', t], [orient(q) for q in C(t, 3)], rows)
    expected['cup_equivalence'] = rows
    expected['some_long_cup'] = [tuple(by['cup', t] for t in cups)]
    expected['no_longer_cup'] = [tuple(-orient(q) for q in C(t, 3)) for t in C(range(m), n-1)]
    expected['convex_complements'] = [(-by['cup', t], by['convex', tuple(i for i in range(m) if i not in t)]) for t in cups]
    if 'no_full_longer_cup' in phases:
        expected['no_full_longer_cup'] = [tuple(-orient(q) for q in C(t+(m,), 3)) for t in C(range(m), n-2)]
    if 'terminal_fourcap_equivalence' in phases:
        rows = []
        fours = list(C(range(m), 4))
        for q in fours:
            equiv(by['boundary_fourcap', q], [-orient(t) for t in C(q, 3)], rows)
        expected['terminal_fourcap_equivalence'] = rows
        rows = []
        for t in C(range(m), 3):
            witnesses = [q for q in fours if q[-2:] == t[-2:]]
            equiv(by['boundary_bad_triple', t], [-orient(t)]+[-by['boundary_fourcap', q] for q in witnesses], rows)
        expected['terminal_bad_triple_equivalence'] = rows
        rows = []
        for bits in range(1 << m):
            a = vertices(bits)
            if len(a) > m-n+2:
                continue
            b = tuple(i for i in range(m) if not (bits >> i & 1))
            rows.append(tuple([by['boundary_bad_triple', t] for t in C(a, 3)]+[by['convex', t] for t in C(b, n-1)]))
        expected['forall_terminal_safe_delta'] = rows
    for name, rows in expected.items():
        assert Counter(map(tuple, rows)) == Counter(phases[name]), name
    return {name: len(rows) for name, rows in expected.items()}


def canonical(g, maps):
    cap4 = [t for t in C(range(g.m), 4) if g.cap(t)]
    vals = {}
    for v, (kind, t) in maps.items():
        if kind == 'orientation':
            vals[v] = g.d[t] > 0
        elif kind == 'convex':
            vals[v] = g.convex(t)
        elif kind == 'cup':
            vals[v] = g.cup(t)
        elif kind == 'boundary_fourcap':
            vals[v] = g.cap(t)
        elif kind == 'boundary_bad_triple':
            vals[v] = g.cap(t) and not any(q[-2:] == t[-2:] for q in cap4)
        else:
            raise AssertionError(kind)
    return vals


def violations(phases, vals):
    return {p: sum(not any(vals[abs(x)] == (x > 0) for x in row) for row in rows) for p, rows in phases.items()}


def clause_controls(n, kind):
    case = SCRATCH/('terminal' if kind == 'terminal' else 'refined' if kind == 'refined' else 'sweep')/(f'n{n}' if kind == 'terminal' else f'n{n}-{kind if kind in ("old", "root") else "root"}')
    maps, phases = load_cnf(case)
    rebuilt = independent_rows(n, maps, phases)
    base_names = {'signotope', 'no5cap', 'convex4_equivalence', 'convex_larger_equivalence', 'no_ngon'}
    assert set(phases) == base_names | set(rebuilt)
    source_hashes = {}
    if kind in ('old', 'root'):
        generated = SCRATCH/f'audit/n{n}-{kind}.cnf'
        subprocess.run([str(SCRATCH/'audit/complement'), str(n), kind, str(generated)],
                       check=True, stdout=subprocess.DEVNULL, timeout=10)
        assert digest(generated) == digest(case/'input.cnf')
        assert digest(Path(str(generated)+'.map')) == digest(case/'input.cnf.map')
        for src in (HERE.parent/'complement.cpp', HERE.parents[2]/'compact/compact_cnf.cpp'):
            source_hashes[str(src)] = digest(src)
    else:
        parent = SCRATCH/f'sweep/n{n}-{"old" if kind == "terminal" else "root"}'
        oldmaps, oldphases = load_cnf(parent)
        assert all(maps[v] == value for v, value in oldmaps.items())
        assert all(phases[p] == rows for p, rows in oldphases.items())
    m = max(max(t) for _, t in maps.values())+1
    controls = []
    for name in ('root', 'refined'):
        doc = json.loads((HERE/f'data/n{n}-{name}.json').read_text())
        g = Geometry(doc['P'][:m])
        vals = canonical(g, maps)
        bad = violations(phases, vals)
        expected_bad = {'forall_terminal_safe_delta'} if kind == 'terminal' else ({'no_full_longer_cup'} if kind == 'refined' and name == 'root' else set())
        assert {p for p, count in bad.items() if count} == expected_bad, (kind, name, bad)
        controls.append(dict(name=name, false_clauses=bad))
        # Mutate one true and one false cup flag to test both directions.
        mutated_truths = set()
        for v, (flagkind, t) in maps.items():
            if flagkind != 'cup' or vals[v] in mutated_truths:
                continue
            mutant = dict(vals)
            mutant[v] = not vals[v]
            assert violations({'cup_equivalence': phases['cup_equivalence']}, mutant)['cup_equivalence'] > 0
            mutated_truths.add(vals[v])
        assert mutated_truths == {False, True}
    for sign in (1, -1):
        g = Geometry([(i, sign*i*i) for i in range(m)])
        bad = violations(phases, canonical(g, maps))
        assert bad['cup_equivalence'] == 0 and bad['convex_complements'] == 0
        if sign == 1:
            assert bad['no_longer_cup'] > 0 and bad['some_long_cup'] == 0 and bad['no5cap'] == 0
        else:
            assert bad['no5cap'] > 0 and bad['some_long_cup'] == 1 and bad['no_longer_cup'] == 0
        assert bad['no_ngon'] > 0
        controls.append(dict(name=f'parabola_{sign}', false_clauses=bad))
    # A deterministically raised middle point lies strictly inside some
    # complements. The odd displacement avoids all parabolic secant heights.
    mid = m//2
    g = Geometry([(i, 2*i*i+(3 if i == mid else 0)) for i in range(m)])
    bad = violations(phases, canonical(g, maps))
    assert bad['cup_equivalence'] == 0 and bad['convex_complements'] > 0
    assert bad['no5cap'] == 0 and bad['no_longer_cup'] > 0 and bad['no_ngon'] > 0
    controls.append(dict(name='raised_middle_parabola', points=g.p, false_clauses=bad))
    return dict(n=n, kind=kind, cnf_sha256=digest(case/'input.cnf'), map_sha256=digest(case/'input.cnf.map'), source_hashes=source_hashes, rebuilt=rebuilt, controls=controls)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('mode', choices=('fixtures', 'small', 'old', 'root', 'refined', 'terminal'))
    ap.add_argument('--n', type=int, choices=(6, 7, 8))
    a = ap.parse_args()
    begin = time.monotonic()
    if a.mode == 'fixtures':
        result = [fixture(HERE/f'data/n{n}-{name}.json') for n in (6, 7, 8) for name in ('root', 'refined')]
    elif a.mode == 'small':
        result = small_controls()
    else:
        assert a.n
        result = clause_controls(a.n, a.mode)
    report = dict(label='COMPUTED', status='PASS', mode=a.mode, result=result,
                  checker_sha256=digest(__file__), seconds=round(time.monotonic()-begin, 3),
                  maxrss_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    out = HERE/'data'/f'{a.mode}{"-n"+str(a.n) if a.n else ""}.json'
    out.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', output=str(out), seconds=report['seconds'], maxrss_KiB=report['maxrss_KiB'])))


if __name__ == '__main__':
    main()
