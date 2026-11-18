"""Independent exact replay: imports no finder or prior envelope code.

Uses expanded 3x3 determinants, monotone adjacent slopes for caps, and
explicit line certificates. All finite geometry is exhaustively checked.
"""
import argparse
from fractions import Fraction as F
from itertools import combinations
import hashlib
import json
from pathlib import Path
import resource
import time


def determinant(a, b, c):
    return (a[0]*b[1]+b[0]*c[1]+c[0]*a[1]
            - a[1]*b[0]-b[1]*c[0]-c[1]*a[0])


def slope(a, b):
    return F(b[1]-a[1], b[0]-a[0])


def is_cap(p, ids):
    slopes = [slope(p[a], p[b]) for a, b in zip(ids, ids[1:])]
    return all(a > b for a, b in zip(slopes, slopes[1:]))


def terminal_line(p, pair):
    a, b = (p[i] for i in pair)
    s = slope(a, b)
    return s, a[1]+s*(p[-1][0]-a[0])


def check_geometry(p, expected):
    assert all(p[i][0] < p[i+1][0] for i in range(len(p)-1))
    dets = {t: determinant(*(p[i] for i in t)) for t in combinations(range(len(p)), 3)}
    assert all(v != 0 for v in dets.values())
    caps = {k: [t for t in combinations(range(len(p)), k) if is_cap(p, t)] for k in (3,4,5)}
    assert caps[4] == [tuple(t) for t in expected]
    assert not caps[5]
    # Cross-check the adjacent-slope characterization against all turns.
    for k in (3,4,5):
        for t in combinations(range(len(p)), k):
            assert is_cap(p, t) == all(dets[u] < 0 for u in combinations(t,3))
    ambient = {t[-2:]: terminal_line(p,t[-2:]) for t in caps[4]}
    return dets, caps, ambient


def encode(obj):
    if isinstance(obj, F):
        return str(obj)
    if isinstance(obj, dict):
        return {str(k): encode(v) for k,v in obj.items()}
    if isinstance(obj, (list,tuple)):
        return [encode(v) for v in obj]
    return obj


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists(), 'refuse to overwrite output'
    start = time.monotonic()
    data = json.loads(args.input.read_text())
    p = data['safe_two_supports']
    q = data['same_orientations_exposed']
    dp, cp, lp = check_geometry(p, data['ambient_four_caps'])
    dq, cq, lq = check_geometry(q, data['ambient_four_caps'])
    assert all((dp[t] > 0) == (dq[t] > 0) for t in dp)
    triple = tuple(data['target_cap_triple'])
    assert triple in cp[3] and triple in cq[3]
    target = terminal_line(p, triple[-2:])
    assert target == terminal_line(q, triple[-2:]) == (F(-2), F(-4))
    assert lp == {(2,4):(F(-3,2),F(-15,2)), (5,6):(F(-12),F(-14)), (5,7):(F(-5,2),F(5))}
    assert lq == {(2,4):(F(-3,2),F(-15,2)), (5,6):(F(-12),F(-14)), (5,7):(F(-7,2),F(3))}
    for lines in (lp,lq):
        assert all(u < target[0] or w < target[1] for u,w in lines.values())
    supports = [tuple(t) for t in data['safe_support_pairs']]
    weights = [F(w) for w in data['safe_support_weights']]
    assert sum(weights) == 1 and all(w > 0 for w in weights)
    combination = tuple(sum(w*lp[pair][c] for w,pair in zip(weights,supports)) for c in (0,1))
    assert combination == (F(-2), F(-5,4))
    assert combination[1]-target[1] == F(11,4)
    t = F(data['exposed_t_witness'])
    line_values = {ab:u*t+w for ab,(u,w) in lq.items()}
    target_value = target[0]*t+target[1]
    assert t == 6 and target_value == -16
    assert max(line_values.values()) == F(-33,2) < target_value
    differences = {ab:(target[0]-u,target[1]-w) for ab,(u,w) in lq.items()}
    assert differences == {(2,4):(F(-1,2),F(7,2)), (5,6):(F(10),F(10)), (5,7):(F(3,2),F(-7))}
    interval = [F(x) for x in data['exposed_t_interval']]
    assert interval == [F(14,3),F(7)] and interval[0] < t < interval[1]
    insertion = tuple(F(x) for x in data['exposed_insertion'])
    augmented = [tuple(F(v) for v in pt) for pt in q] + [insertion]
    assert insertion[0] == q[-1][0]+t
    assert max(line_values.values()) < insertion[1] < target_value
    assert all(determinant(*(augmented[i] for i in ids)) != 0 for ids in combinations(range(9),3))
    assert not any(is_cap(augmented, ids) for ids in combinations(range(9),5))
    assert is_cap(augmented, (*triple,8))
    # Exact positive/negative tests of the endpoint h and affine-family formula.
    family_samples = []
    for h in (F(3),F(7,2),F(34,9),F(4),F(5)):
        ps = [tuple(F(v) for v in point) for point in p]
        ps[-1] = (F(7),h)
        ds, cs, ls = check_geometry(ps, data['ambient_four_caps'])
        assert all((ds[tri] > 0) == (dp[tri] > 0) for tri in ds)
        weight = 1/(7-h)
        combined = tuple(weight*ls[5,7][c]+(1-weight)*ls[2,4][c] for c in (0,1))
        surplus = (9*h-34)/(2*(7-h))
        assert combined[0] == target[0] and combined[1]-target[1] == surplus
        lower = 2*(h+4)/(6-h)
        assert (lower >= 7) == (surplus >= 0)
        family_samples.append(dict(h=h,low_support_weight=weight,surplus=surplus,exposure_lower=lower,safe=surplus>=0))
    output = dict(status='PASS', label='COMPUTED exact independent-code replay within this track',
                  input_sha256=hashlib.sha256(args.input.read_bytes()).hexdigest(),
                  checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  determinant_count=len(dp),determinants_safe=dp,determinants_exposed=dq,
                  minimum_absolute_determinant_safe=min(map(abs,dp.values())),
                  minimum_absolute_determinant_exposed=min(map(abs,dq.values())),
                  all_orientations_equal=True,cap_triples=cp[3],cap4=cp[4],cap5=cp[5],
                  target_line=target,ambient_safe=lp,ambient_exposed=lq,
                  no_single_support_both=True,weights=weights,convex_combination=combination,
                  surplus=F(11,4),exposure_interval=interval,exposure_witness_t=t,
                  exposure_target_value=target_value,exposure_ambient_values=line_values,
                  exposure_line_differences=differences,
                  five_cap_free_insertion=insertion,created_four_cap=(*triple,8),
                  family_samples=family_samples,elapsed_seconds=time.monotonic()-start,
                  peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(encode(output),indent=2)+'\n')
    print(json.dumps(encode({k:v for k,v in output.items() if not k.startswith('determinants_') and k!='cap_triples'})))


if __name__ == '__main__':
    main()
