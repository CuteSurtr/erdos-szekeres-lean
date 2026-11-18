"""Bounded exact controls of the rightmost-point T_n lemma, no solver.

All determinants, convex hulls and chain lengths use integer arithmetic.
No producer, frozen checker or solver is imported. Named coordinate
families reproduce standard cup/cap recursive constructions locally.
"""
from itertools import combinations, product
from collections import Counter
from pathlib import Path
import argparse
import hashlib
import json
import resource
import time
import traceback


def det(p, a, b, c):
    x, y = p[a]; u, v = p[b]; w, z = p[c]
    return x * (v-z) + u * (z-y) + w * (y-v)


def hull(p, ids):
    if len(ids) <= 2:
        return list(ids)
    out = []
    for order in (ids, list(reversed(ids))):
        chain = []
        for v in order:
            while len(chain) >= 2 and det(p, chain[-2], chain[-1], v) <= 0:
                chain.pop()
            chain.append(v)
        out.extend(chain[:-1])
    return out


def ranks(s, ids, sign=1):
    result = {v: 1 for v in ids}; edges = {}
    for j, b in enumerate(ids):
        for i, a in enumerate(ids[:j]):
            edges[a, b] = max([2] + [edges[z, a]+1 for z in ids[:i]
                                              if s[z, a, b]*sign > 0])
            result[b] = max(result[b], edges[a, b])
    return result


def maxgon(s, ids):
    """Largest upper+lower hull with fixed common endpoints."""
    result = min(len(ids), 2)
    for start_index, start in enumerate(ids):
        endpoint = {}
        for sign in (1, -1):
            edges = {}
            for j in range(start_index+1, len(ids)):
                b = ids[j]
                for i in range(start_index, j):
                    a = ids[i]
                    candidates = [2] if a == start else [0]
                    candidates += [edges[z, a]+1 for z in ids[start_index:i]
                                   if edges[z, a] and s[z, a, b]*sign > 0]
                    edges[a, b] = max(candidates)
                endpoint[sign, b] = max(edges[a, b] for a in ids[start_index:j])
        for b in ids[start_index+1:]:
            result = max(result, endpoint[1, b]+endpoint[-1, b]-2)
    return result


def high_join(left, right):
    dx = max(x for x, _ in left)-min(x for x, _ in right)+1
    p = left + [(x+dx, y) for x, y in right]; cut = len(left)
    height = 0
    for a, b in combinations(range(cut), 2):
        for c in range(cut, len(p)):
            height = max(height, (-det(p, a, b, c))//(p[b][0]-p[a][0])+1)
    for a in range(cut):
        for b, c in combinations(range(cut, len(p)), 2):
            height = max(height, det(p, a, b, c)//(p[c][0]-p[b][0])+1)
    return left + [(x+dx, y+height) for x, y in right]


def extremal(cup, cap):
    if cup == 2:
        return [(i, -i*i) for i in range(cap)]
    if cap == 2:
        return [(i, i*i) for i in range(cup)]
    return high_join(extremal(cup-1, cap), extremal(cup, cap-1))


def check(p, n):
    assert p and all(p[i][0] < p[i+1][0] for i in range(len(p)-1))
    ids = list(range(len(p))); prefix = ids[:-1]; root = ids[-1]; k = n-1
    signs = {t: det(p, *t) for t in combinations(ids, 3)}
    assert all(signs.values())
    beta = ranks(signs, ids); alpha = ranks(signs, ids, -1)
    bp = ranks(signs, prefix)
    assert max(alpha.values()) <= 3
    assert max(bp.values(), default=0) <= k-1
    end3 = {c for (a, b, c), v in signs.items() if v < 0}
    targets = [t for t in combinations(ids, k) if len(hull(p, t)) == k]
    old = [t for t in targets if root not in t]
    endpoints = sorted({t[-1] for t in old})
    if root in end3:
        branch = 'root_End3'; selected = sorted(set(endpoints+[root]))
    else:
        branch = 'root_not_End3'; selected = [v for v in prefix if bp[v] == k-1]
    assert all(signs[t] > 0 for t in combinations(selected, 3))
    assert all(v in end3 for v in selected[1:])
    assert all(set(t).intersection(selected) for t in targets)
    complement = [v for v in ids if v not in selected]
    assert maxgon(signs, complement) < k
    gon = maxgon(signs, ids)
    if len(ids) <= 8:
        brute = max([min(len(ids), 2)] + [q for q in range(3, len(ids)+1)
                    for t in combinations(ids, q) if len(hull(p, t)) == q])
        assert gon == brute
    return dict(n=n, points=p, size=len(p), branch=branch, selected=selected,
                selected_first_lacks_End3=bool(selected and selected[0] not in end3),
                End3=sorted(end3), prefix_target_endpoints=endpoints,
                prefix_beta=[bp[v] for v in prefix],
                maxima=dict(cup=max(beta.values()), cap=max(alpha.values()), gon=gon),
                prefix_cup=max(bp.values(), default=0), targets=len(targets),
                old_targets=len(old), targets_using_root=len(targets)-len(old),
                admissible=gon < n, complement_maxgon=maxgon(signs, complement))


def named():
    result = {}
    for n in (5, 6, 7, 8):
        k = n-1
        result[f'n{n}_pure_long_cup'] = check([(i, i*i) for i in range(k)], n)
        target = [(i, (k+2)**3 if i == (k-1)//2 else i*i) for i in range(k)]
        result[f'n{n}_upper_three_target'] = check(target, n)
        base = extremal(n-2, 3)
        result[f'n{n}_extremal'] = check(base, n)
        result[f'n{n}_extremal_plus_high_root'] = check(high_join(base, [(0, 0)]), n)
    assert all(r['admissible'] for r in result.values())
    return dict(status='PASS', cases=result)


def grid():
    counts = Counter(); examples = {}; started = time.monotonic()
    for m in range(1, 8):
        tails = [()] if m <= 2 else product(range(-3, 4), repeat=m-2)
        for ys in tails:
            if time.monotonic()-started > 15:
                return dict(status='PARTIAL_TIME_BOUND', counts=dict(counts), examples=examples)
            counts['attempted'] += 1
            p = list(enumerate(([0, 0]+list(ys))[:m])); ids = list(range(m))
            s = {t: det(p, *t) for t in combinations(ids, 3)}
            if not all(s.values()):
                continue
            counts['GP'] += 1
            if max(ranks(s, ids, -1).values()) > 3:
                continue
            counts['no_four_cap'] += 1
            if max(ranks(s, ids[:-1]).values(), default=0) >= 4:
                continue
            r = check(p, 5); counts['checked'] += 1; counts[r['branch']] += 1
            counts['admissible'] += r['admissible']
            counts['long_cup_present'] += r['maxima']['cup'] >= 4
            counts['first_exception'] += r['selected_first_lacks_End3']
            key = r['branch'] + ('_longcup' if r['maxima']['cup'] >= 4 else '_shortcup')
            examples.setdefault(key, r)
    return dict(status='PASS_COMPLETE_GRID', counts=dict(counts), examples=examples,
                scope='n5; m1..7; x_i=i; y0=y1=0 when present; remaining y_i in [-3,3]; not all order types')


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--mode', choices=['named', 'grid'], required=True)
    ap.add_argument('--out', type=Path, required=True); args = ap.parse_args()
    assert not args.out.exists(); start = time.monotonic(); result = {}
    try:
        result = named() if args.mode == 'named' else grid()
    except BaseException:
        result.update(status='FAIL', traceback=traceback.format_exc())
        raise
    finally:
        result['elapsed_seconds'] = time.monotonic()-start
        result['peak_rss_kib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        result['source_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open('x') as f:
            json.dump(result, f, indent=2); f.write('\n')
        print(json.dumps({k: v for k, v in result.items() if k not in ('cases', 'examples')}))


if __name__ == '__main__':
    main()
