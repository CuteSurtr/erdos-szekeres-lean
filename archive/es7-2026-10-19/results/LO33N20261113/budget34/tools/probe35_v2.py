#!/usr/bin/env python3
"""HEURISTIC discovery for a witness whose pool candidates are exhausted. Nothing here certifies anything.

Method of fastbb-20261113/killtools/probe_vec.py (candidate supports = unions of near-tight rows inside the witness's
occupied set; 30 s CaDiCaL solves of the fast coupled model; greedy shrinking of the refuted ones), run with a
redirected copy of its encoder (W/discovery/coupled.py). Output: a candidate file in the format of
`cut34_v4.py select`, for `cut34_v4.py certify` (full pinned encoder, LRAT, cake_lpr) and the independent batch audit.
Usage: probe35.py WITNESS INPUT_FOLDER OUT.json [minutes] [procs]
"""
from datetime import datetime
import gzip
import hashlib
import itertools
import json
from multiprocessing import Pool
from pathlib import Path
import random
import sys
import time

W = Path('/home/jay/research/data/es308-20261114')
import os, resource  # v2: as a loop child the soft address-space limit is 100 MiB; take the inherited hard limit
for _n in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'): os.environ[_n] = '1'
_soft, _hard = resource.getrlimit(resource.RLIMIT_AS); resource.setrlimit(resource.RLIMIT_AS, (_hard, _hard))
sys.path.insert(0, str(W / 'discovery'))
import coupled  # noqa: E402  (redirected copy; writes only below W/discovery)

sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()


def candidates(holes, rows, rng, n=154, limit=3000):
    O = set(range(n)) - set(holes)
    faces = sorted({tuple(sorted(set(s) & O)) for s, d in rows if len(s) - d == 7 and len(set(s) & O) == 7})
    fm = [sum(1 << i for i in f) for f in faces]
    pool = {}
    for x, y in itertools.combinations(fm, 2):
        m = x | y
        if 10 <= m.bit_count() <= 15 and m not in pool:
            pool[m] = sum(m & f == f for f in fm)
    ranked = sorted(pool, key=lambda m: (-pool[m], m.bit_count(), m))
    out = ranked[:limit // 2]
    for m in ranked[:300]:
        for f in rng.sample(fm, min(40, len(fm))):
            j = m | f
            if 14 <= j.bit_count() <= 17 and j not in pool:
                pool[j] = sum(j & g == g for g in fm)
                out.append(j)
    return [[i for i in range(n) if m >> i & 1] for m in out[:limit]], len(faces)


def test(S):
    return S, coupled.fast_solve(S, seconds=30)


def minimize(S):
    S = list(S); i = 0
    while i < len(S):
        T = S[:i] + S[i + 1:]
        if coupled.fast_solve(T, seconds=30) == 'unsat':
            S = T
        else:
            i += 1
    return S


if __name__ == '__main__':
    wit, inp, out = Path(sys.argv[1]), W / 'inputs' / sys.argv[2], Path(sys.argv[3])
    minutes = float(sys.argv[4]) if len(sys.argv) > 4 else 6
    procs = int(sys.argv[5]) if len(sys.argv) > 5 else 4
    assert not out.exists() and inp.resolve().is_relative_to(W / 'inputs')
    H = json.loads(wit.read_text())['holes']; HS = set(H)
    assert len(H) == len(HS) and len(H) in (34, 35) and 0 not in HS
    raw = gzip.decompress((W / 'inputs/source-2650.json.gz').read_bytes())
    assert hashlib.sha256(raw).hexdigest() == 'e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6'
    base = json.loads(raw)
    extra = json.loads((inp / 'extra.json').read_text())
    t = sum(i in HS for i, s in enumerate(base['states']) if s[0] >= 5)
    assert extra[0]['rhs'] == t and extra[1]['rhs'] == len(H) - t
    rows = [(tuple(r['support']), r['rhs']) for r in base['constraints'] + extra]
    assert all(len(HS.intersection(s)) >= d for s, d in rows), 'witness does not satisfy the input rows'
    have = {tuple(sorted(s)) for s, d in rows if d == 1}
    cands, nfaces = candidates(H, rows, random.Random(1113))
    deadline = time.time() + 60 * minutes
    stats = {'sat': 0, 'unsat': 0, 'unknown': 0}; found = []
    with Pool(procs) as P:
        for S, st in P.imap_unordered(test, cands, chunksize=1):
            stats[st] += 1
            if st == 'unsat':
                found.append(S)
            if time.time() > deadline or len(found) >= 12:
                P.terminate(); break
    chosen = {}
    for S in found:
        core = minimize(S) if time.time() < deadline + 240 else S
        final = tuple(core) if 8 <= len(core) <= 17 else tuple(S)
        if 8 <= len(final) <= 17 and not HS.intersection(final) and final not in have:
            chosen.setdefault(final, {'refuted_support': S, 'core': core})
    result = {'label': 'HEURISTIC candidates (probe35 discovery), not accepted rows',
              'created': datetime.now().astimezone().isoformat(), 'witness_sha256': sha(wit), 'holes': sorted(HS),
              'slice': t, 'budget': len(H), 'exact_row_check': 'PASS', 'rows_checked': len(rows),
              'input_extra_sha256': sha(inp / 'extra.json'), 'input_folder': str(inp),
              'candidate_sources': {'probe35': sha(Path(__file__)), 'coupled_copy': sha(W / 'discovery/coupled.py')},
              'faces': nfaces, 'tested': stats, 'available_candidates': len(chosen),
              'candidates': [{'support': list(s), 'rhs': 1, 'discovery_references': [v]} for s, v in chosen.items()]}
    out.write_text(json.dumps(result, indent=1) + '\n')
    print(json.dumps({k: result[k] for k in ('slice', 'budget', 'faces', 'tested', 'available_candidates')}))
