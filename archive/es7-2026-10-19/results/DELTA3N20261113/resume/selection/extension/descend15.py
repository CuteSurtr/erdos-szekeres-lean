#!/usr/bin/env python3
"""Exact n6 checks on complements of the four smallest n7 weak Deltas."""
import hashlib
import importlib.util
from itertools import combinations as C
import json
from pathlib import Path
import resource

H = Path(__file__).resolve().parent
W = Path('/home/jay/research/data/delta3-codex-20261113/extension/descend15-a')
resource.setrlimit(resource.RLIMIT_AS, (150 << 20, 150 << 20))
W.mkdir(exist_ok=False)
spec = importlib.util.spec_from_file_location('geometry', H.parent / 'boundary/check_envelope.py')
G = importlib.util.module_from_spec(spec)
spec.loader.exec_module(G)
source = H / 'terminal15/data/balanced.json'
original = json.loads(source.read_text())['P']
removed_sets = [[2,3,7], [2,3,11], [4,11,12], [4,11,13]]


def convex(P, q):
    def chain(order):
        out = []
        for i in order:
            while len(out) > 1 and G.det(P, out[-2], out[-1], i) <= 0:
                out.pop()
            out.append(i)
        return out
    return len(chain(q)) + len(chain(reversed(q))) - 2 == len(q)


def upwards(m, family):
    values = bytearray(1 << m)
    for item in family:
        values[sum(1 << i for i in item)] = 1
    for i in range(m):
        bit = 1 << i
        for mask in range(1 << m):
            if mask & bit:
                values[mask] |= values[mask ^ bit]
    return values


results = []
for case, removed in enumerate(removed_sets):
    indices = [i for i in range(15) if i not in removed]
    P = [original[i] for i in indices]
    m = len(P)
    assert G.maxima(P, range(m))[0] < 5 and G.maxima(P, range(m))[2] < 6
    cap = lambda q: all(G.det(P, *t) < 0 for t in C(q, 3))
    caps = [q for q in C(range(m), 4) if cap(q)]
    tails = {q[-2:] for q in caps}
    bad = [q for q in C(range(m), 3) if cap(q) and q[-2:] not in tails]
    targets = [q for q in C(range(m), 5) if convex(P, q)]
    ca, ba, ta = [upwards(m, family) for family in [caps, bad, targets]]
    weak, terminal = [], []
    for mask in range(1 << m):
        if ca[mask] or ta[((1 << m) - 1) ^ mask]:
            continue
        weak.append(mask)
        if not ba[mask]:
            terminal.append(mask)
    directory = W / str(case)
    directory.mkdir()
    (directory / 'points.txt').write_text(f'{m} 6\n' + ''.join(f'{x} {y}\n' for x, y in P))
    rows = [[-i - 1 for i in q] for q in caps + bad] + [[i + 1 for i in q] for q in targets]
    (directory / 'terminal.cnf').write_text(f'p cnf {m} {len(rows)}\n' + ''.join(
        ' '.join(map(str, row)) + ' 0\n' for row in rows))
    best = min(terminal, key=lambda z: (z.bit_count(), z)) if terminal else None
    result = {'label': 'COMPUTED exact fixed-instance enumeration', 'case': case,
              'removed_original_indices': removed, 'local_to_original': indices, 'P': P, 'n': 6,
              'maxima_cap_cup_gon': G.maxima(P, range(m)), 'fourcaps': len(caps),
              'bad_triples': len(bad), 'pentagons': len(targets),
              'assignments_checked': 1 << m, 'weak_delta_count': len(weak),
              'terminal_delta_count': len(terminal),
              'minimum_weak_size': min(map(int.bit_count, weak)) if weak else None,
              'minimum_terminal_size': best.bit_count() if best is not None else None,
              'terminal_witness': [i for i in range(m) if best >> i & 1] if best is not None else None,
              'cnf_sha256': hashlib.sha256((directory / 'terminal.cnf').read_bytes()).hexdigest()}
    (directory / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    results.append(result)
receipt = {'label': 'COMPUTED four exact restrictions, not a universal theorem',
           'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
           'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
           'cases': results}
(W / 'DONE.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps([{k: r[k] for k in ['case', 'weak_delta_count', 'terminal_delta_count', 'minimum_terminal_size']} for r in results]))
