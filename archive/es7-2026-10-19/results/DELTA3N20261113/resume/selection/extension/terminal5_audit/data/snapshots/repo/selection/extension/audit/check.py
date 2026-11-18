#!/usr/bin/env python3
"""Independent general-terminal audit; standard library only.

No encoder/checker imports. A streaming literal/map reconstruction checks
emitted files, while integer hulls and full subset truth tables supply the
real controls. Every invocation is externally limited to 20 seconds.
"""
import argparse
from array import array
from collections import Counter
from itertools import combinations, permutations, product, zip_longest
import hashlib
import json
from pathlib import Path
import resource
import subprocess
import time
import traceback

HERE = Path(__file__).resolve().parent
EXT = HERE.parent
SEL = EXT.parent
COMPACT = SEL.parent / 'compact/compact_cnf.cpp'
DATA = HERE / 'data'
SCRATCH = Path('/home/jay/research/data/delta3-codex-20261113/extension/audit')
BIN = SCRATCH / 'terminal_general'


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def mask(items):
    return sum(1 << i for i in items)


def verts(s):
    return tuple(i for i in range(s.bit_length()) if s >> i & 1)


def subsets(m, k):
    return (mask(t) for t in combinations(range(m), k))


def det(P, a, b, c):
    x, y = P[a]
    u, v = P[b]
    w, z = P[c]
    return (u-x)*(z-y) - (v-y)*(w-x)


def hull(P, S):
    S = tuple(S)
    if len(S) <= 2:
        return S
    lo, hi = [], []
    for order, chain in ((S, lo), (S[::-1], hi)):
        for p in order:
            while len(chain) >= 2 and det(P, chain[-2], chain[-1], p) <= 0:
                chain.pop()
            chain.append(p)
    return tuple(lo[:-1] + hi[:-1])


def upclosure(m, witnesses):
    """Full subset truth table, independent of deletion-child recurrences."""
    out = bytearray(1 << m)
    for s in witnesses:
        out[s] = 1
    for i in range(m):
        bit = 1 << i
        for base in range(0, 1 << m, bit << 1):
            for j in range(bit):
                out[base + bit + j] |= out[base + j]
    return out


class Geometry:
    def __init__(self, P, n):
        self.P, self.n, self.m = P, n, len(P)
        self.full = (1 << self.m) - 1
        assert all(type(a) is int for p in P for a in p)
        assert all(P[i][0] < P[i+1][0] for i in range(self.m-1))
        determinants = {mask(t): det(P, *t) for t in combinations(range(self.m), 3)}
        assert all(determinants.values()), 'not general position'
        self.min_det = min(map(abs, determinants.values()))
        self.sign = {s: d > 0 for s, d in determinants.items()}
        self.caps4 = [s for s in subsets(self.m, 4)
                      if all(not self.sign[mask(t)] for t in combinations(verts(s), 3))]
        ends = {verts(s)[-2:] for s in self.caps4}
        self.bad = [s for s in self.sign if not self.sign[s] and verts(s)[-2:] not in ends]
        self.cap5 = [s for s in subsets(self.m, 5)
                     if all(not self.sign[mask(t)] for t in combinations(verts(s), 3))]
        nonconvex4 = [s for s in subsets(self.m, 4) if len(hull(P, verts(s))) != 4]
        self.nonconvex = upclosure(self.m, nonconvex4)
        self.bad_inside = upclosure(self.m, self.bad)
        self.cap_inside = upclosure(self.m, self.caps4)
        self.targets = [s for s in subsets(self.m, n-1) if len(hull(P, verts(s))) == n-1]
        self.ngons = [s for s in subsets(self.m, n) if len(hull(P, verts(s))) == n]
        for k in (n-1, n):
            for s in subsets(self.m, k):
                assert (not self.nonconvex[s]) == (len(hull(P, verts(s))) == k)
        self.target_inside = upclosure(self.m, self.targets)
        self.good = [s for s in range(self.full+1)
                     if not self.bad_inside[s] and not self.target_inside[self.full ^ s]]
        if not self.cap5:
            assert all(self.bad_inside[s] or not self.cap_inside[s] for s in range(self.full+1))
        self.by_size = dict(sorted(Counter(s.bit_count() for s in self.good).items()))

    def value(self, kind, s):
        if kind == 'orientation':
            return self.sign[s]
        if kind == 'convex':
            return not self.nonconvex[s]
        if kind == 'terminal_fourcap':
            return s in self.capset
        if kind == 'terminal_bad_triple':
            return s in self.badset
        if kind == 'bad_contains':
            return bool(self.bad_inside[s])
        if kind == 'target_contains':
            return bool(self.target_inside[s])
        raise AssertionError(kind)

    def prepare_values(self):
        self.capset, self.badset = set(self.caps4), set(self.bad)

    def report(self):
        return {'m': self.m, 'n': self.n, 'minimum_absolute_determinant': self.min_det,
                'four_caps': len(self.caps4), 'bad_triples': len(self.bad),
                'five_caps': len(self.cap5), 'targets': len(self.targets), 'n_gons': len(self.ngons),
                'terminal_deltas': len(self.good), 'terminal_deltas_by_size': self.by_size,
                'first_terminal_delta': list(verts(self.good[0])) if self.good else None,
                'every_subset_checked': self.full+1}


def clauses(path):
    phase = None
    with Path(path).open() as f:
        first = f.readline().split()
        assert first[:2] == ['p', 'cnf']
        for line in f:
            fields = line.split()
            if not fields:
                continue
            if fields[:2] == ['c', 'phase']:
                assert len(fields) == 3
                phase = fields[2]
                continue
            assert fields[0] != 'c', fields
            row = tuple(map(int, fields))
            assert row[-1] == 0 and 0 not in row[:-1] and phase is not None
            yield phase, row[:-1]


class Reconstruction:
    """Reconstruct from the written families, with independently allocated IDs."""
    def __init__(self, m, n, map_path=None, geometry=None):
        self.m, self.n, self.k = m, n, m-n+2
        self.full, self.nv = (1 << m)-1, 0
        self.Q, self.D, self.T, self.F = (array('i', [0]) * (1 << m) for _ in range(4))
        self.tri = {}
        self.map_reader = None
        if map_path:
            self.map_file = Path(map_path).open()
            self.map_reader = (line.split() for line in self.map_file if not line.startswith('#'))
        self.geometry = geometry
        self.assignment = bytearray([0]) if geometry else None
        if geometry:
            geometry.prepare_values()
        for s in subsets(m, 3):
            self.tri[s] = self.fresh('orientation', s)

    def fresh(self, kind, s):
        self.nv += 1
        if self.map_reader is not None:
            row = next(self.map_reader, None)
            assert row == [str(self.nv), kind, str(s)], (self.nv, kind, s, row)
        if self.geometry:
            self.assignment.append(int(self.geometry.value(kind, s)))
        return self.nv

    def conj(self, z, terms):
        for t in terms:
            yield (-z, t)
        yield (z, *(-t for t in terms))

    def rows(self, fixed=None):
        for s in subsets(self.m, 4):
            ids = [self.tri[mask(t)] for t in combinations(verts(s), 3)]
            for a, b, c in combinations(ids, 3):
                yield 'signotope', (-a, b, -c)
                yield 'signotope', (a, -b, c)
        for s in subsets(self.m, 5):
            v = verts(s)
            yield 'no5cap', tuple(self.tri[mask(v[j:j+3])] for j in range(3))
        for s in subsets(self.m, 4):
            z = self.Q[s] = self.fresh('convex', s)
            a, b, c, d = (self.tri[mask(t)] for t in combinations(verts(s), 3))
            for row in ((-z,-a,b),(-z,a,-b),(-z,-c,d),(-z,c,-d),
                        (z,a,d),(z,-a,-d),(z,b,-c),(z,-b,c)):
                yield 'convex4_equivalence', row
        for k in range(5, self.n):
            for s in subsets(self.m, k):
                z = self.Q[s] = self.fresh('convex', s)
                terms = [self.Q[s ^ (1 << i)] for i in verts(s)[:5]]
                assert all(terms)
                for row in self.conj(z, terms):
                    yield 'convex_larger_equivalence', row
        for s in subsets(self.m, self.n):
            row = tuple(-self.Q[s ^ (1 << i)] for i in verts(s)[:5])
            assert all(row)
            yield 'no_ngon', row
        for s in subsets(self.m, 4):
            z = self.F[s] = self.fresh('terminal_fourcap', s)
            terms = [-self.tri[mask(t)] for t in combinations(verts(s), 3)]
            for row in self.conj(z, terms):
                yield 'terminal_fourcap_equivalence', row
        for s in subsets(self.m, 3):
            a, b, c = verts(s)
            z = self.fresh('terminal_bad_triple', s)
            if self.k >= 3:
                self.D[s] = z
            terms = [-self.tri[s]] + [-self.F[mask((u,v,b,c))]
                                      for u,v in combinations(range(b),2)]
            assert all(terms)
            for row in self.conj(z, terms):
                yield 'terminal_bad_triple_equivalence', row
        for s in range(self.full+1):
            if 4 <= s.bit_count() <= self.k:
                z = self.D[s] = self.fresh('bad_contains', s)
                terms = tuple(self.D[s ^ (1 << i)] for i in verts(s)[:4])
                assert all(terms)
                yield 'bad_triple_containment', (-z, *terms)
        for s in range(self.full+1):
            if s.bit_count() == self.n-1:
                self.T[s] = self.Q[s]
            elif s.bit_count() >= self.n:
                z = self.T[s] = self.fresh('target_contains', s)
                terms = tuple(self.T[s ^ (1 << i)] for i in verts(s)[:self.n])
                assert all(terms)
                yield 'target_containment', (-z, *terms)
        for s in range(self.full+1):
            if s.bit_count() <= self.k:
                yield 'forall_terminal_delta', tuple(i for i in (self.D[s],self.T[self.full^s]) if i)
        if fixed is not None:
            assert len(fixed) == len(self.tri)
            for i, sign in enumerate(fixed, 1):
                assert sign in '+-'
                yield 'fixed_signs', (i if sign == '+' else -i,)
        if self.map_reader is not None:
            assert next(self.map_reader, None) is None, 'extra map entries'
            self.map_file.close()


def check_formula(path, m, n, geometry=None, fixed=None):
    before = {str(p): sha(p) for p in (Path(path), Path(str(path)+'.map'))}
    reconstruction = Reconstruction(m,n,str(path)+'.map',geometry)
    counts, literals, failures = Counter(), Counter(), Counter()
    first_failures = {}
    for lineno, (expected, actual) in enumerate(zip_longest(reconstruction.rows(fixed), clauses(path)),1):
        assert expected == actual, (lineno, expected, actual)
        phase, row = actual
        counts[phase] += 1
        literals[phase] += len(row)
        if geometry and not any(bool(reconstruction.assignment[abs(x)]) == (x > 0) for x in row):
            failures[phase] += 1
            first_failures.setdefault(phase, {'clause':lineno,'row':row})
    header = Path(path).open().readline().split()
    assert (int(header[2]),int(header[3])) == (reconstruction.nv,sum(counts.values()))
    assert before == {str(p): sha(p) for p in (Path(path), Path(str(path)+'.map'))}
    if geometry:
        assert not (set(failures)-{'no5cap','no_ngon','forall_terminal_delta'})
        expected_failures = sum(s.bit_count() <= m-n+2 for s in geometry.good)
        assert failures['forall_terminal_delta'] == expected_failures
        assert failures['no5cap'] == len(geometry.cap5)
        assert failures['no_ngon'] == len(geometry.ngons)
    return {'m':m,'n':n,'variables':reconstruction.nv,'clauses':sum(counts.values()),
            'phases':dict(counts),'literals':sum(literals.values()),'hashes':before,
            'canonical_failed_clauses':dict(failures),'first_failures':first_failures,
            'map_and_all_rows_match':True,'fixed_signs':fixed is not None}


def frozen():
    return json.loads((DATA/'fixtures.json').read_text())


def freeze():
    fixtures = []
    for n in (6,7,8):
        for mode in ('root','refined'):
            p = SEL/f'boundary/audit/data/n{n}-{mode}.json'
            data = json.loads(p.read_text())
            fixtures.append({'name':f'n{n}-{mode}-old','n':n,'P':data['P'][:data['old_m']],
                             'source':str(p),'source_sha256':sha(p),'expect_terminal':True})
    p = SEL/'terminal/data/witness.json'
    data = json.loads(p.read_text())
    fixtures.append({'name':'terminal18','n':7,'P':data['P'],'source':str(p),
                     'source_sha256':sha(p),'expect_terminal':False})
    with (DATA/'fixtures.json').open('x') as f:
        json.dump(fixtures,f,indent=2);f.write('\n')
    return {'frozen_cases':len(fixtures),'sha256':sha(DATA/'fixtures.json')}


def generate(m,n,fixed_fixture=None):
    tag = f'm{m}n{n}' + (f'-{fixed_fixture}' if fixed_fixture else '')
    case = SCRATCH/tag
    case.mkdir(exist_ok=False)
    cmd = [str(BIN),str(m),str(n),str(case/'input.cnf')]
    if fixed_fixture:
        f = next(x for x in frozen() if x['name']==fixed_fixture)
        assert len(f['P'])==m and f['n']==n
        signs = ''.join('+' if det(f['P'],*t)>0 else '-' for t in combinations(range(m),3))
        (case/'signs.txt').write_text(signs+'\n')
        cmd.append(str(case/'signs.txt'))
    with (case/'encode.log').open('w') as err:
        p = subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=err,timeout=18)
    (case/'encode.json').write_text(p.stdout)
    assert p.returncode==0, (p.returncode,case)
    return {'path':str(case/'input.cnf'),'stats':json.loads(p.stdout),'binary_sha256':sha(BIN),
            'source_sha256':sha(EXT/'terminal_general.cpp'),'compact_sha256':sha(COMPACT)}


def algebra():
    packet_valid = 0
    for signs in product((False,True),repeat=4):
        a,b,c,d = signs
        valid = all(not (signs[i]==signs[k]!=signs[j]) for i,j,k in combinations(range(4),3))
        assert valid == (sum(signs[i]!=signs[i+1] for i in range(3)) <= 1)
        if not valid:
            continue
        packet_valid += 1
        actual = (a==b and c==d)
        accepted = []
        for z in (False,True):
            values = {1:a,2:b,3:c,4:d,5:z}
            rows = [(-5,-1,2),(-5,1,-2),(-5,-3,4),(-5,3,-4),
                    (5,1,4),(5,-1,-4),(5,2,-3),(5,-2,3)]
            if all(any(values[abs(t)]==(t>0) for t in row) for row in rows):
                accepted.append(z)
        assert accepted == [actual]
    cover_cases = 0
    for m in range(4,11):
        for size in (3,4,5,6,7):
            if size>=m:
                continue
            deleted = set(range(size+1))
            for witness in combinations(range(m),size):
                assert deleted-set(witness)
                cover_cases += 1
            assert not set(range(size))-set(range(size)), 'impossible'
    # Explicit witnesses show each wrong shorter cover really loses its leaf.
    wrong_covers = []
    for witness_size in (3,4,5,6,7):
        witness = set(range(witness_size))
        good = [i for i in range(witness_size+1) if i not in witness]
        bad = [i for i in range(witness_size) if i not in witness]
        assert good == [witness_size] and not bad
        wrong_covers.append({'witness_size':witness_size,'lost_by_wrong_deletions':list(witness)})
    # Without no-five-cap a later four-cap can contain no bad triple.
    P = [[i,-i*i] for i in range(6)]
    g = Geometry(P,8)
    A = mask((2,3,4,5))
    assert g.cap_inside[A] and not g.bad_inside[A] and g.cap5
    # Safe pairs cannot freely grow to triples in a three-cap ambient set.
    small = Geometry([[0,0],[1,1],[2,0]],5)
    assert not small.bad_inside[3] and small.bad_inside[7]
    return {'one_change_packets':packet_valid,'cover_cases':cover_cases,
            'wrong_cover_controls':wrong_covers,'missing_no5cap_countercontrol':verts(A),
            'unsafe_pair_growth_control':True}


def small():
    counts = Counter()
    for perm in permutations(range(6)):
        P = list(map(list,zip(range(6),perm)))
        if any(det(P,*t)==0 for t in combinations(range(6),3)):
            continue
        counts['general_position_sets'] += 1
        for n in (5,6,7):
            g = Geometry(P,n)
            counts['ambient_cases'] += 1
            if not g.cap5 and not g.ngons:
                counts['valid_premise_cases'] += 1
            e = Reconstruction(6,n,geometry=g)
            failed = Counter()
            for phase,row in e.rows():
                counts['canonical_clauses_evaluated'] += 1
                if not any(bool(e.assignment[abs(x)])==(x>0) for x in row):
                    failed[phase] += 1
            assert not set(failed)-{'no5cap','no_ngon','forall_terminal_delta'}
            assert failed['no5cap']==len(g.cap5) and failed['no_ngon']==len(g.ngons)
            assert failed['forall_terminal_delta']==sum(s.bit_count()<=6-n+2 for s in g.good)
            if not g.cap5:
                for s in range(64):
                    safe = not g.bad_inside[s]
                    assert safe == (not g.cap_inside[s] and not any((b&s)==b for b in g.bad))
                    counts['terminal_equivalences'] += 1
    return dict(counts)


def main():
    resource.setrlimit(resource.RLIMIT_AS,(400<<20,400<<20))
    resource.setrlimit(resource.RLIMIT_CPU,(18,18))
    parser = argparse.ArgumentParser()
    parser.add_argument('mode',choices=['freeze','generate','formula','real','small','algebra'])
    parser.add_argument('--m',type=int)
    parser.add_argument('--n',type=int)
    parser.add_argument('--path',type=Path)
    parser.add_argument('--fixture')
    parser.add_argument('--fixed',action='store_true')
    parser.add_argument('--receipt',required=True)
    args = parser.parse_args()
    start = time.monotonic()
    out = {'label':'COMPUTED','status':'IN_PROGRESS','mode':args.mode,'script_sha256':sha(__file__)}
    try:
        if args.mode=='freeze':
            result = freeze()
        elif args.mode=='generate':
            result = generate(args.m,args.n,args.fixture if args.fixed else None)
        elif args.mode=='algebra':
            result = algebra()
        elif args.mode=='small':
            result = small()
        elif args.mode=='formula':
            result = check_formula(args.path,args.m,args.n)
        else:
            f = next(x for x in frozen() if x['name']==args.fixture)
            g = Geometry(f['P'],f['n'])
            assert not g.cap5 and not g.ngons
            assert bool(g.good)==f['expect_terminal']
            result = g.report()
            if args.path:
                fixed = ''.join('+' if v else '-' for v in g.sign.values()) if args.fixed else None
                result['formula'] = check_formula(args.path,g.m,g.n,g,fixed)
            result['fixture_sha256']=sha(DATA/'fixtures.json')
        out.update(status='PASS',result=result)
    except BaseException:
        out.update(status='FAIL',error=traceback.format_exc())
        raise
    finally:
        out.update(elapsed_seconds=time.monotonic()-start,
                   max_rss_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        with (DATA/args.receipt).open('x') as f:
            json.dump(out,f,indent=2);f.write('\n')
        print(json.dumps(out if out['status']=='FAIL' else {
            'status':out['status'],'mode':out['mode'],'receipt':args.receipt,
            'seconds':round(out['elapsed_seconds'],3),'max_rss_KiB':out['max_rss_KiB']}))


if __name__=='__main__':
    main()
