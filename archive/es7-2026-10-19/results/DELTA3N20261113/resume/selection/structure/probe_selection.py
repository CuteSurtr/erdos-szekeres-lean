#!/usr/bin/env python3
"""Tiny exact controls for rank/lexicographic selection candidates; no solver."""
import hashlib
import itertools as it
import json
from pathlib import Path
import resource
import sys
import time

resource.setrlimit(resource.RLIMIT_AS, (384 * 1024**2,) * 2)
resource.setrlimit(resource.RLIMIT_CPU, (18, 18))
START = time.monotonic()
HERE = Path(__file__).resolve().parent
R = HERE.parents[1]
SCRATCH = Path('/home/jay/research/data/delta3-codex-20261113/selection/structure')


def det(P, a, b, c):
    ax, ay = P[a]; bx, by = P[b]; cx, cy = P[c]
    return (bx-ax)*(cy-ay)-(by-ay)*(cx-ax)


def mask(vs):
    return sum(1 << v for v in vs)


def vs(a):
    return [i for i in range(a.bit_length()) if a >> i & 1]


def hull(P, ids):
    lo, hi = [], []
    for seq, order in ((lo, ids), (hi, reversed(ids))):
        for p in order:
            while len(seq) >= 2 and det(P, seq[-2], seq[-1], p) <= 0:
                seq.pop()
            seq.append(p)
    return lo[:-1] + hi[:-1]


def geometry(P, n):
    m = len(P)
    assert all(P[i][0] < P[i+1][0] for i in range(m-1))
    signs = {q: det(P, *q) for q in it.combinations(range(m), 3)}
    assert all(signs.values())
    def cap(ids):
        return all(signs[q] < 0 for q in it.combinations(ids, 3))
    caps = {j: [mask(q) for q in it.combinations(range(m), j) if cap(q)]
            for j in (3, 4, 5)}
    gons = {j: [mask(q) for q in it.combinations(range(m), j)
                if len(hull(P, q)) == j] for j in (n-1, n)}
    assert not caps[5] and not gons[n]
    beta = [1] * m
    edges = {}
    for b in range(m):
        for a in range(b):
            edges[a, b] = max([2] + [edges[t, a]+1 for t in range(a)
                                         if signs[t, a, b] > 0])
            beta[b] = max(beta[b], edges[a, b])
    tails = {tuple(vs(q)[-2:]) for q in caps[4]}
    bad = [q for q in caps[3] if tuple(vs(q)[-2:]) not in tails]
    assert all(beta[vs(q)[0]] < beta[vs(q)[1]] for q in bad)
    return caps, gons, beta, bad


def analyze(P, n, tag):
    caps, gons, beta, bad = geometry(P, n)
    m = len(P)
    anti_forbidden = [mask((i,j)) for j in range(m) for i in range(j)
                      if beta[i] < beta[j]]
    anti = []
    for a in range(1 << m):
        if any(a & q == q for q in anti_forbidden):
            continue
        assert not any(a & q == q for q in caps[4] + bad)
        if all(a & h for h in gons[n-1]):
            anti.append(a)
    single_levels = [lev for lev in range(1, max(beta)+1)
                     if all(any(beta[p] == lev for p in vs(h)) for h in gons[n-1])]
    r = m-1
    old4 = [q for q in caps[4] if not q >> r & 1]
    oldH = [h for h in gons[n-1] if not h >> r & 1]
    deltas = [a for a in range(1 << r)
              if not any(a & q == q for q in old4) and all(a & h for h in oldH)]
    minimum = min(a.bit_count() for a in deltas)
    minima = sorted((a for a in deltas if a.bit_count() == minimum), key=vs)
    unsafe_minima = [a for a in minima if any((a | 1 << r) & q == q for q in caps[4])]
    lex = {}
    for t in sorted({a.bit_count() for a in deltas}):
        a = min((a for a in deltas if a.bit_count() == t), key=vs)
        blocks = [vs(q) for q in caps[4] if (a | 1 << r) & q == q]
        if blocks:
            lex[str(t)] = dict(A=vs(a), blocks=blocks,
                              missed_full=[vs(h) for h in gons[n-1] if not a & h])
    return dict(tag=tag, n=n, P=P, m=m, beta=beta, caps4=len(caps[4]),
                targets=len(gons[n-1]), rank3_triples=len(bad),
                antichain_deltas=len(anti), antichain_example=vs(min(anti, key=lambda a:(a.bit_count(),vs(a)))) if anti else None,
                common_rank_levels=single_levels, old_minimum=minimum,
                old_minima=len(minima), unsafe_minima=[vs(a) for a in unsafe_minima],
                lex_at_minimum=vs(minima[0]), lex_failures_by_size=lex)


def main():
    sources = [
        R / 'weak_theory/findings.json',
        R.parent.parent / 'DELTA2N20261113/data/cex/restr_ends_weak_a5_n7_m12_real.json',
        R.parent.parent / 'DELTA2N20261113/data/cex/restr_ends_weak_a5_n8_m13_real.json',
        R.parent / 'hypergraph/four_state_obstruction_small.json',
        Path('/home/jay/research/data/delta3-codex-20261113/coordinator/minimized/counterexample/witness.json'),
    ]
    out = dict(label='COMPUTED', scope='five fixed source files; not a universal search',
               source_hashes={}, results=[])
    SCRATCH.mkdir(parents=True, exist_ok=True)
    for src in sources:
        data = json.loads(src.read_text())
        out['source_hashes'][str(src)] = hashlib.sha256(src.read_bytes()).hexdigest()
        records = data.get('obstructions', [data])
        for j, rec in enumerate(records):
            if time.monotonic()-START > 15:
                out['stopped'] = 'internal wall cutoff'; break
            out['results'].append(analyze(rec['P'], rec['n'], src.stem+f'-{j}'))
            (SCRATCH / 'probe_selection.json').write_text(json.dumps(out, indent=2)+'\n')
    out['seconds'] = time.monotonic()-START
    out['max_rss_KiB'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    (SCRATCH / 'probe_selection.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
