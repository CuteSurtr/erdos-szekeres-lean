"""Exact bounded real controls for the all-cap-cut written lemma."""
from itertools import combinations
from pathlib import Path
import argparse
import hashlib
import json
import resource
import time
import traceback
from rooted_controls import det, hull, ranks, maxgon


def join(left, right):
    left = [(x-min(t[0] for t in left), y) for x, y in left]
    right = [(x-min(t[0] for t in right), y) for x, y in right]
    gap = 2*(left[-1][0]+right[-1][0]+1)
    p = left+[(x+gap, y) for x, y in right]; cut = len(left)
    weights = [x if i < cut else gap-x for i, (x, y) in enumerate(p)]
    basis = [(x, weights[i]) for i, (x, y) in enumerate(p)]
    amount = 0
    for t in combinations(range(len(p)), 3):
        if t[0] < cut <= t[-1]:
            coefficient = det(basis, *t); assert coefficient < 0
            amount = max(amount, det(p, *t)//(-coefficient)+1)
    return [(x, y+amount*weights[i]) for i, (x, y) in enumerate(p)]


def check(left, right, n, options=None):
    p = join(left, right); cut = len(left); ids = list(range(len(p)))
    L = ids[:cut]; R = ids[cut:]
    s = {t: det(p, *t) for t in combinations(ids, 3)}
    assert all(s.values())
    assert all(v < 0 for t, v in s.items() if t[0] < cut <= t[-1])
    assert max(ranks(s, ids, -1).values()) <= 4 and maxgon(s, ids) < n
    caps = [t for t in combinations(ids, 4) if all(s[q] < 0 for q in combinations(t, 3))]
    ends = {t[-2:]:t for t in caps}
    targets = [t for t in combinations(ids, n-1) if len(hull(p, t)) == n-1]
    if len(L) >= 2 and len(R) >= 2:
        assert all(s[t] > 0 for block in (L, R) for t in combinations(block, 3))
        options = [[l]+R for l in L]
    elif len(L) == 1:
        options = [R]
    else:
        assert options is not None
    tested = []
    for A in options:
        aset = set(A)
        assert not any(aset.issuperset(t) for t in caps)
        selected_caps = [t for t in combinations(A, 3) if s[t] < 0]
        assert all(t[-2:] in ends for t in selected_caps)
        assert all(aset.intersection(t) for t in targets)
        blue = [i for i in ids if i not in aset]
        assert maxgon(s, blue) < n-1
        tested.append(dict(A=A, selected_cap_triples=len(selected_caps),
                           complement_maxgon=maxgon(s, blue),
                           terminal_witnesses={str(t):ends[t[-2:]] for t in selected_caps}))
    kinds = {'left':0, 'right':0, 'mixed':0}
    for t in targets:
        kinds['left' if t[-1] < cut else 'right' if t[0] >= cut else 'mixed'] += 1
    return dict(n=n, points=p, size=len(p), cut=cut, caps4=len(caps), targets=len(targets),
                target_kinds=kinds, maxima=dict(cap=max(ranks(s, ids, -1).values()),
                cup=max(ranks(s, ids).values()), gon=maxgon(s, ids)), selections=tested)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args(); assert not args.out.exists(); start = time.monotonic(); result = {}
    try:
        root = Path(__file__).resolve().parents[1]
        old_path = root/'data/rooted_named.json'; old = json.loads(old_path.read_text())['cases']
        cases = {}
        for n in (5, 6, 7, 8):
            for a, b in ((2, 2), (2, n-1), (n-1, 2), (n-1, n-1)):
                cases[f'n{n}_L{a}_R{b}'] = check([(i, i*i) for i in range(a)],
                                                [(i, i*i) for i in range(b)], n)
            R = [tuple(q) for q in old[f'n{n}_extremal']['points']]
            cases[f'n{n}_singleton_left'] = check([(0, 0)], R, n)
            src = old[f'n{n}_extremal_plus_high_root']
            L = [tuple(q) for q in src['points']]
            cases[f'n{n}_singleton_right'] = check(L, [(0, 0)], n,
                                                   options=[src['selected']+[len(L)]])
        result = dict(status='PASS', cases=cases,
                      selections_checked=sum(len(r['selections']) for r in cases.values()),
                      named_input_sha256=hashlib.sha256(old_path.read_bytes()).hexdigest())
    except BaseException:
        result.update(status='FAIL', traceback=traceback.format_exc()); raise
    finally:
        result['elapsed_seconds'] = time.monotonic()-start
        result['peak_rss_kib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        result['source_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        result['helper_sha256'] = hashlib.sha256(Path(__file__).with_name('rooted_controls.py').read_bytes()).hexdigest()
        with args.out.open('x') as f:
            json.dump(result, f, indent=2); f.write('\n')
        print(json.dumps({k: v for k, v in result.items() if k != 'cases'}))


if __name__ == '__main__':
    main()
