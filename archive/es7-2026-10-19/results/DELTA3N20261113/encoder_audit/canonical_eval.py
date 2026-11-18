#!/usr/bin/env python3
"""Evaluate the emitted Delta CNF at an independent exact semantic assignment.

No SAT solver, no encoder/check_model imports, no external dependencies or writes.
The C++ variable *allocation order* is reconstructed; semantic values come from
all-triple chains, exact convex hulls (coordinates), and full subset transforms.
Only unconditioned sym=none, non-base formulas are supported. This is a COMPUTED
fixture check, not an UNSAT certificate. The parent schedules substantial runs.
"""
import argparse
from collections import Counter, defaultdict
from hashlib import sha256
from itertools import combinations
import json
from math import comb
from pathlib import Path
import resource
import time


SOURCE_SHA256 = 'b953e14fc7d0840712bbf63f502e00c7342cbd1cdb9ef3ed548759e8ae8aa12c'
PHASES = ('signotope', 'no5cap', 'no_ngon', 'fourcap', 'cap_lattice',
          'endpoint_support', 'target_seeds', 'target_lattice', 'forall_delta')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    h = sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def mask(s):
    return sum(1 << x for x in s)


def vertices(s):
    out = []
    while s:
        bit = s & -s
        out.append(bit.bit_length() - 1)
        s ^= bit
    return out


def upwards(m, seeds):
    # All m coordinate directions, not the bounded deletion recurrence.
    out = bytearray(1 << m)
    for s in seeds:
        out[s] = 1
    for p in range(m):
        bit = 1 << p
        for block in range(0, 1 << m, bit * 2):
            for offset in range(bit):
                out[block + bit + offset] |= out[block + offset]
    return out


def load_fixture(path, m, indices):
    raw = path.read_text()
    points = signs = None
    if raw.lstrip().startswith(('{', '[')):
        data = json.loads(raw)
        if isinstance(data, list):
            points = data
        else:
            points, signs = data.get('P'), data.get('signs')
            if points is None:
                require(data.get('m', m) == m, 'sign fixture m differs')
    else:
        words = raw.split()
        if len(words) == 1 and set(words[0]) <= {'+', '-'}:
            signs = words[0]
        else:
            total = int(words[0])
            require(len(words) == 1 + 2 * total, 'expected count then x y rows')
            points = [[int(words[i]), int(words[i + 1])]
                      for i in range(1, len(words), 2)]
    if indices is not None:
        require(points is not None, '--indices requires coordinates')
        require(len(set(indices)) == len(indices) and indices == sorted(indices),
                'indices must be distinct and increasing')
        require(all(0 <= i < len(points) for i in indices), 'index outside fixture')
        points, signs = [points[i] for i in indices], None
    if points is not None:
        require(len(points) == m, 'point count differs; use explicit --indices')
        require(all(len(p) == 2 and all(type(x) is int for x in p) for p in points),
                'exact integer coordinates required')
        require(all(points[i][0] < points[i + 1][0] for i in range(m - 1)),
                'points must already be in strictly increasing x order')
        values = []
        for i, j, k in combinations(range(m), 3):
            a, b, c = points[i], points[j], points[k]
            det = ((b[0] - a[0]) * (c[1] - a[1]) -
                   (b[1] - a[1]) * (c[0] - a[0]))
            require(det != 0, f'collinear triple {(i, j, k)}')
            values.append('+' if det > 0 else '-')
        actual = ''.join(values)
        require(signs is None or signs == actual, 'coordinate/sign disagreement')
        signs = actual
    require(isinstance(signs, str) and len(signs) == comb(m, 3) and
            set(signs) <= {'+', '-'}, 'bad sign string')
    return points, signs


class Geometry:
    def __init__(self, points, signs, m, n, mode):
        self.points, self.m, self.n = points, m, n
        self.t = dict(zip(combinations(range(m), 3), (s == '+' for s in signs)))
        self.range = range(m)
        for q in combinations(self.range, 4):
            seq = [self.t[t] for t in combinations(q, 3)]
            require(sum(a != b for a, b in zip(seq, seq[1:])) <= 1,
                    f'not a signotope at {q}')
        self.caps = {mask(s) for s in combinations(self.range, 4)
                     if self.chain(s, False)}
        self.cap5 = sum(self.chain(s, False) for s in combinations(self.range, 5))
        self.ngons = sum(self.convex(s) for s in combinations(self.range, n))
        require(self.cap5 == self.ngons == 0,
                f'invalid fixture: fivecaps={self.cap5}, convex_ngons={self.ngons}')
        self.targets = set()
        self.polygon_count = 0
        for g in combinations(self.range, n - 1):
            if not self.convex(g):
                continue
            self.polygon_count += 1
            if mode == 'weak':
                target = g
            elif points is not None:
                lo, hi = self.hull_chains(g)
                target = lo if mode == 'cup' else hi
            else:
                u, v = g[0], g[-1]
                target = [u] + [p for p in g[1:-1]
                                if self.t[u, p, v] == (mode == 'cup')] + [v]
            self.targets.add(mask(target))
        self.a = upwards(m, self.caps)
        self.b = upwards(m, self.targets)

    def chain(self, s, positive):
        # Deliberately use every triple, not the encoder's consecutive triples.
        return all(self.t[q] == positive for q in combinations(s, 3))

    def hull_chains(self, s):
        def det(i, j, k):
            a, b, c = self.points[i], self.points[j], self.points[k]
            return ((b[0] - a[0]) * (c[1] - a[1]) -
                    (b[1] - a[1]) * (c[0] - a[0]))
        def build(order):
            out = []
            for v in order:
                while len(out) >= 2 and det(out[-2], out[-1], v) <= 0:
                    out.pop()
                out.append(v)
            return out
        return build(s), list(reversed(build(reversed(s))))

    def convex(self, s):
        if self.points is not None:
            lo, hi = self.hull_chains(s)
            return len(lo) + len(hi) - 2 == len(s)
        return all(self.t[a, b, c] == self.t[a, b, d] and
                   self.t[a, c, d] == self.t[b, c, d]
                   for a, b, c, d in combinations(s, 4))


class Layout:
    def __init__(self, g, mode, pool):
        m, n = g.m, g.n
        full = (1 << m) - 1
        self.values = [False]  # ID zero is a false sentinel, never a literal.
        self.counts = Counter()
        self.aliases = self.absent_nodes = self.missing_seeds = 0
        self.seed_sizes = Counter()

        def alloc(value):
            self.values.append(bool(value))
            return len(self.values) - 1

        for t in combinations(range(m), 3):
            alloc(g.t[t])
        lower = n - 1 if mode == 'weak' else n - 3 if mode == 'cup' else 2
        upper = 4 if mode == 'cap' else n - 1
        A, B, seed, H = {}, {}, {}, {}
        for s in range(full + 1):
            if s.bit_count() == 4 or (pool == 'lattice' and s.bit_count() > 4):
                A[s] = alloc(g.a[s])
        self.counts['signotope'] = 8 * comb(m, 4)
        self.counts['no5cap'] = comb(m, 5)
        self.counts['no_ngon'] = comb(m, n) * (1 + (n - 2) + comb(n - 2, 2))
        self.counts['fourcap'] = 2 * comb(m, 4)
        if pool == 'lattice':
            self.counts['cap_lattice'] = sum(comb(m, k) for k in range(5, m + 1))
        if mode == 'cup':
            cap_ends = {(vertices(s)[0], vertices(s)[-1]) for s in g.caps}
            for u in range(m):
                for v in range(u + 2, m):
                    H[u, v, 3] = alloc(any(not g.t[u, x, v] for x in range(u + 1, v)))
                    self.counts['endpoint_support'] += 1
                    if v - u >= 3:
                        H[u, v, 4] = alloc((u, v) in cap_ends)
                        self.counts['endpoint_support'] += 1
        elif mode == 'cap':
            supports = defaultdict(list)
            for k in range(n - 3, n):
                for s in combinations(range(m), k):
                    z = alloc(g.chain(s, True))
                    self.counts['endpoint_support'] += k - 2
                    supports[s[0], s[-1], k].append(z)
            # C++ std::map keys use lexicographic order.
            for key in sorted(supports):
                H[key] = alloc(any(self.values[z] for z in supports[key]))
                self.counts['endpoint_support'] += 1
        if mode == 'weak':
            for s in combinations(range(m), 4):
                alloc(g.convex(s))
                self.counts['target_seeds'] += 4
            for s in combinations(range(m), n - 1):
                sm = mask(s)
                seed[sm] = alloc(sm in g.targets)
                self.seed_sizes[n - 1] += 1
                self.counts['target_seeds'] += comb(n - 1, 4)
        else:
            for k in range(lower, upper + 1):
                for s in combinations(range(m), k):
                    sm, u, v, other = mask(s), s[0], s[-1], n + 1 - k
                    h = 0 if other == 2 else H.get((u, v, other), 0)
                    if v - u + 1 < n - 1 or (other != 2 and not h):
                        self.missing_seeds += 1
                        require(sm not in g.targets, f'pruned actual target {s}')
                        continue
                    semantic = sm in g.targets
                    endpoint_test = g.chain(s, mode == 'cup') and (other == 2 or self.values[h])
                    require(semantic == endpoint_test,
                            f'endpoint/convex-target disagreement at {s}')
                    seed[sm] = alloc(semantic)
                    self.seed_sizes[k] += 1
                    self.counts['target_seeds'] += k - 2 + int(bool(h))
        require(g.targets <= seed.keys(), 'actual target missing from allocated seeds')
        if pool == 'lattice':
            for s in range(full + 1):
                if s.bit_count() < lower:
                    require(not g.b[s], f'target below lower bound: {s}')
                    continue
                rhs = [seed[s]] if s in seed else []
                for p in vertices(s)[:upper + 1]:
                    child = B.get(s ^ (1 << p), 0)
                    if child:
                        rhs.append(child)
                # Values are from full transforms, not the recurrence being audited.
                if not rhs:
                    require(not g.b[s], f'false sentinel loses a target at {s}')
                    B[s] = 0
                    self.absent_nodes += 1
                elif len(rhs) == 1:
                    require(self.values[rhs[0]] == bool(g.b[s]),
                            f'alias has incompatible semantic value at {s}')
                    B[s] = rhs[0]
                    self.aliases += 1
                else:
                    B[s] = alloc(g.b[s])
                    self.counts['target_lattice'] += 1
        self.counts['forall_delta'] = 1 << m


def evaluate(cnf, g, layout, stats=None):
    # Stream clauses from the actual encoder output; do not regenerate clauses.
    values, counts = layout.values, layout.counts
    checked, literal_counts, false_pool = Counter(), Counter(), []
    phases = [(p, counts[p]) for p in PHASES if counts[p]]
    phase_index = local = clause_count = literal_count = max_width = 0
    header = None
    with cnf.open() as file:
        for line_number, line in enumerate(file, 1):
            words = line.split()
            if not words or words[0] == 'c':
                continue
            if words[0] == 'p':
                require(header is None and clause_count == 0 and len(words) == 4 and
                        words[1] == 'cnf', 'bad DIMACS header')
                header = tuple(map(int, words[2:]))
                require(header == (len(values) - 1, sum(counts.values())),
                        f'layout/header mismatch: {header}, expected '
                        f'{(len(values) - 1, sum(counts.values()))}')
                continue
            require(header is not None and phase_index < len(phases),
                    f'unexpected clause at line {line_number}')
            clause = list(map(int, words))
            require(clause[-1] == 0 and all(0 < abs(x) < len(values) for x in clause[:-1]),
                    f'invalid literal/terminator at line {line_number}')
            clause.pop()
            phase, phase_total = phases[phase_index]
            truth = any(values[abs(x)] == (x > 0) for x in clause)
            if phase == 'forall_delta':
                d = local
                expected = bool(g.a[d] or g.b[((1 << g.m) - 1) ^ d])
                require(truth == expected,
                        f'pool mismatch delta={vertices(d)} clause={clause}')
                if not truth:
                    false_pool.append(d)
            else:
                require(truth, f'canonical assignment falsifies {phase} clause '
                        f'{local + 1}, DIMACS line {line_number}: {clause}')
            checked[phase] += 1
            literal_counts[phase] += len(clause)
            literal_count += len(clause)
            max_width = max(max_width, len(clause))
            clause_count += 1
            local += 1
            if local == phase_total:
                phase_index += 1
                local = 0
    require(header is not None and clause_count == header[1], 'truncated CNF')
    if stats is not None:
        require(stats['variables'] == header[0] and stats['clauses'] == clause_count and
                stats['literals'] == literal_count and stats['max_width'] == max_width,
                'encoder totals disagree with actual CNF')
        actual = {p: dict(clauses=checked[p], literals=literal_counts[p]) for p in checked}
        require(stats['phases'] == actual, 'encoder phase statistics differ')
    return dict(variables=header[0], clauses=clause_count, literals=literal_count,
                checked_phases=dict(checked), canonical_nonpool_false=0,
                working_deltas=len(false_pool),
                first_working_delta=vertices(false_pool[0]) if false_pool else None,
                canonical_full_model=(len(false_pool) == 0))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--cnf', type=Path, required=True)
    ap.add_argument('--fixture', type=Path, required=True)
    ap.add_argument('--n', type=int, required=True)
    ap.add_argument('--m', type=int, required=True)
    ap.add_argument('--mode', choices=('weak', 'cup', 'cap'), default='cup')
    ap.add_argument('--pool', choices=('lattice', 'flat'), default='lattice')
    ap.add_argument('--indices', help='explicit comma-separated coordinate indices')
    ap.add_argument('--stats', type=Path, help='encode.log JSON, optional')
    ap.add_argument('--source', type=Path, help='require audited C++ source hash')
    ap.add_argument('--cpu-seconds', type=int, default=45)
    ap.add_argument('--as-mib', type=int, default=384)
    args = ap.parse_args()
    require(4 <= args.m <= 16 and 5 <= args.n <= 8, 'audit guard: 4<=m<=16, 5<=n<=8')
    require(args.cpu_seconds > 0 and args.as_mib > 0, 'positive resource limits required')
    resource.setrlimit(resource.RLIMIT_AS, (args.as_mib << 20, args.as_mib << 20))
    resource.setrlimit(resource.RLIMIT_CPU, (args.cpu_seconds, args.cpu_seconds))
    started = time.monotonic()
    if args.source:
        require(digest(args.source) == SOURCE_SHA256, 'C++ source changed; re-audit first')
    stats = json.loads(args.stats.read_text()) if args.stats else None
    if stats is not None:
        require((stats['m'], stats['n'], stats['mode'], stats['pool']) ==
                (args.m, args.n, args.mode, args.pool), 'stats parameters differ')
        require(stats['sym'] == 'none' and not stats['cube'] and not stats['base_only'] and
                not stats['phases'].get('fixed_signs'), 'conditioned/base formulas unsupported')
    indices = [int(x) for x in args.indices.split(',')] if args.indices is not None else None
    points, signs = load_fixture(args.fixture, args.m, indices)
    g = Geometry(points, signs, args.m, args.n, args.mode)
    layout = Layout(g, args.mode, args.pool)
    report = evaluate(args.cnf, g, layout, stats)
    report.update(label='COMPUTED', status='CANONICAL_FIXTURE_CHECK_PASSED',
                  n=args.n, m=args.m, mode=args.mode, pool=args.pool,
                  geometry='integer_convex_hulls' if points is not None else 'signotope_4_subsets',
                  fixture=str(args.fixture), fixture_sha256=digest(args.fixture),
                  cnf=str(args.cnf), cnf_sha256=digest(args.cnf), indices=indices,
                  source_sha256=SOURCE_SHA256, signs_sha256=sha256(signs.encode()).hexdigest(),
                  fourcaps=len(g.caps), fivecaps=g.cap5, convex_ngons=g.ngons,
                  target_polygons=g.polygon_count, target_seeds=len(g.targets),
                  allocated_seed_sizes=dict(layout.seed_sizes), aliases_checked=layout.aliases,
                  zero_nodes_checked=layout.absent_nodes, pruned_seeds_checked=layout.missing_seeds,
                  wall_seconds=round(time.monotonic() - started, 6))
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
