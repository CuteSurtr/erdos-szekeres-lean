#!/usr/bin/env python3
"""Extra-row file of slice t (track G2): [h(F) >= t, h(Lo) >= BUDGET - t] + the pool rows in pool order.

Usage: make_slice_extra.py T POOL.json OUT.json [BUDGET=33]
F = the 84 residual states with f1 >= 5, Lo = the other 70 (states of the pinned 2,650-row source).
The two capacity rows come first and the certified rows follow in the stable pool order, so rows certified later
can be APPENDED without moving any index (closed contexts stay valid).
"""
import gzip, hashlib, json, sys

SRC = '/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz'
RAW_SHA = 'e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6'   # sha256 of the decompressed JSON


def main():
    t, pool_path, out = int(sys.argv[1]), sys.argv[2], sys.argv[3]
    budget = int(sys.argv[4]) if len(sys.argv) > 4 else 33
    raw = gzip.decompress(open(SRC, 'rb').read())
    assert hashlib.sha256(raw).hexdigest() == RAW_SHA
    states = json.loads(raw)['states']
    F = [i for i, s in enumerate(states) if s[0] >= 5]
    LO = [i for i, s in enumerate(states) if s[0] <= 4]
    assert len(F) == 84 and len(LO) == 70
    pool = json.load(open(pool_path))
    rows = [{'support': F, 'rhs': t}, {'support': LO, 'rhs': budget - t}]
    seen = set()
    for r in pool:
        s = tuple(sorted(r['support']))
        assert r.get('rhs', 1) == 1 and r.get('cnf_sha256') and s not in seen
        seen.add(s)
        rows.append({'support': list(s), 'rhs': 1})
    json.dump(rows, open(out, 'w'))
    print(json.dumps({'t': t, 'budget': budget, 'rows': len(rows), 'certified': len(rows) - 2, 'out': out,
                      'sha256': hashlib.sha256(open(out, 'rb').read()).hexdigest()}))


if __name__ == '__main__':
    main()
