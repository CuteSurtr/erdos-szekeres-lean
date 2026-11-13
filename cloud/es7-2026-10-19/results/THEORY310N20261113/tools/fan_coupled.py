#!/usr/bin/env python3
"""Do fan-monotonicity clauses turn October 'necessary-model SAT' supports UNSAT?

Re-runs the frozen rank-search coupled model (model.py, source-cup bound on) on
supports recorded as SAT, with and without the extra exactness clauses
  chronological p<q<r:  cup -> b(p,r) >= b(p,q) and a(p,r) >= a(q,r)
                        cap -> b(p,r) <= b(p,q) and a(p,r) <= a(q,r)
(residual labels (a,b) = (6-F_-, E_+-1); fan at p for E_+, fan at r for F_-).
Discovery evidence only: UNSAT here is not a proof (z3, no certificate).
"""
import gzip, hashlib, itertools, json, sys, time
from pathlib import Path
RS = Path('/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-residual32-rank-search-2026-10-10')
sys.path.insert(0, str(RS))
import model
WORK = Path('/home/jay/research/data/theory310-20261113/coupled'); WORK.mkdir(exist_ok=True)
model.ROOT = WORK
SRC = Path('/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-residual32-sixth-relaxed-2026-10-10/source-2646.json.gz')
raw = gzip.decompress(SRC.read_bytes())
assert hashlib.sha256(raw).hexdigest() == '151ea1bfb175f6507d910521eb96961c82b54add2fb7e49e13b864b87241123e'
data = json.loads(raw); n = 154
model.D = data
P, mn, mx = model.pair_boxes(data['states']); model.TT = model.triple_table(P, mn, mx)
model.cells = [{(i + 1, y) for i, h in enumerate(s[:4]) for y in range(1, h + 1)} for s in data['states']]

def add_fan(m):
    z3 = model.z3; cnt = 0
    for q in itertools.permutations(range(m.n), 3):
        cond = m.condition(q)
        if cond is None:
            continue
        a, b, c = q
        ab = tuple(sorted((a, b))); bc = tuple(sorted((b, c))); ac = tuple(sorted((a, c)))
        cupc = z3.And(m.cup[ac] >= m.cup[ab], m.cap[ac] >= m.cap[bc])
        capc = z3.And(m.cup[ac] <= m.cup[ab], m.cap[ac] <= m.cap[bc])
        m.s.add(z3.Implies(cond, z3.If(m.oriented[q], cupc, capc))); cnt += 1
    return cnt

def run(entry, fan, tl):
    model.occupied = set(range(n)) - set(entry['strict_row_witness_holes'])
    t0 = time.monotonic()
    try:
        m = model.CompactModel(entry['support'], t0 + 60, source_cup_bound=True)
        k = add_fan(m) if fan else 0
        r = m.probe(time.monotonic() + tl)
    except (TimeoutError, model.z3.Z3Exception, MemoryError) as e:
        return {'status': 'unknown', 'reason': str(e)}
    return {'status': r['status'], 'fan_clauses': k, 'seconds': round(time.monotonic() - t0, 2),
            'iterations': r.get('iterations'), 'cuts': r.get('cuts')}

if __name__ == '__main__':
    tl = float(sys.argv[1]); limit = int(sys.argv[2])
    entries = []
    for f in ['discovery-initial.json', 'discovery-continuation.json', 'discovery-survivors.json']:
        d = json.load(open(RS / f))
        for r in d['results']:
            if r.get('status') == 'sat' and isinstance(r.get('strict_row_witness_holes'), list):
                entries.append(r)
    seen = set(); uniq = []
    for e in entries:
        k = tuple(e['support'])
        if k not in seen:
            seen.add(k); uniq.append(e)
    uniq.sort(key=lambda e: len(e['support']))
    print('sat supports', len(uniq), flush=True)
    out = []
    for e in uniq[:limit]:
        r1 = run(e, True, tl)
        rec = {'support': e['support'], 'size': len(e['support']), 'fan': r1}
        if r1['status'] != 'sat':
            rec['base'] = run(e, False, tl)
        print(json.dumps(rec), flush=True)
        out.append(rec)
        json.dump(out, open('fan_coupled_out.json', 'w'), indent=1)
