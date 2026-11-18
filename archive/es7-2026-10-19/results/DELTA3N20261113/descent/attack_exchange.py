#!/usr/bin/env python3
"""Find a counterexample A to monotone one-exchange for a fixed real S,D.

This is a bounded local SAT attack, not a certification tool. Default: build
only. A solver run must be explicitly requested, with at most 8 CPU seconds.
UNSAT output is labelled COMPUTED only. All SAT models are rechecked directly.
"""
import argparse
import itertools
import json
import resource
import subprocess
from pathlib import Path

from check_exchange import orient, mask, vertices


def geometry(points, n):
    m = len(points)
    assert m <= 26 and n in (7, 8)
    assert all(points[i][0] < points[i + 1][0] for i in range(m - 1))
    O = {t: orient(*(points[i] for i in t)) for t in itertools.combinations(range(m), 3)}
    assert all(O.values())
    capB, cupB = {}, {}
    for u in range(m):
        C, U = {}, {}
        for v in range(u + 1, m):
            C[u, v], U[u, v] = 2, 2
            for k in range(u + 1, v):
                C[k, v] = max([0] + [C[j, k] + 1 for j in range(u, k) if C[j, k] and O[j, k, v] < 0])
                U[k, v] = max([0] + [U[j, k] + 1 for j in range(u, k) if U[j, k] and O[j, k, v] > 0])
            capB[u, v] = max(C[k, v] for k in range(u, v))
            cupB[u, v] = max(U[k, v] for k in range(u, v))
    assert max(capB.values()) <= 4
    assert max(capB[t] + cupB[t] - 2 for t in capB) < n
    caps = [k for k in itertools.combinations(range(m), 4) if all(O[t] < 0 for t in zip(k, k[1:], k[2:]))]
    cups = []
    for c in (2, 3, 4):
        for d in itertools.combinations(range(m), n + 1 - c):
            if capB[d[0], d[-1]] == c and all(O[t] > 0 for t in zip(d, d[1:], d[2:])):
                cups.append(d)
    return caps, cups, capB, cupB


def attack(points, n, D, output, solve_seconds=0, allow_no_starter=False, fixed_A=None):
    m = len(points)
    caps, cups, capB, cupB = geometry(points, n)
    assert tuple(D) in cups
    assert capB[D[0], D[-1]] in (3, 4)
    if not allow_no_starter:
        assert any(k[0] == D[-1] for k in caps)
    # A_i is variable i+1. Witness definitions are one-directional, which is
    # sufficient because every witness appears positively in the failure clauses.
    count = m
    clauses = [[-i - 1 for i in k] for k in caps]
    clauses += [[i + 1 for i in d] for d in cups if len(d) == n - 1]
    clauses += [[-i - 1] for i in D]
    if fixed_A is not None:
        clauses += [[i + 1 if i in fixed_A else -i - 1] for i in range(m)]
    blocking = {}
    for p in D:
        for k in caps:
            if p in k and len(set(k) & set(D)) == 1:
                count += 1
                blocking[p, k] = count
                clauses += [[-count, i + 1] for i in k if i != p]
    private = {}
    for d in cups:
        for r in d:
            if r in D:
                continue
            count += 1
            private[d, r] = count
            clauses.append([-count, r + 1])
            clauses += [[-count, -i - 1] for i in d if i != r]
    for p in D:
        clauses.append([v for (q, _), v in blocking.items() if q == p])
        for r in set(range(m)) - set(D):
            clauses.append([v for (q, k), v in blocking.items() if q == p and r not in k]
                           + [v for (d, z), v in private.items() if z == r and p not in d])
    output = Path(output)
    cnf = output.with_suffix('.cnf')
    cnf.write_text(f'p cnf {count} {len(clauses)}\n' + ''.join(' '.join(map(str, c)) + ' 0\n' for c in clauses))
    result = {'label': 'COMPUTED', 'P': points, 'n': n, 'D': D, 'cap_type': capB[D[0], D[-1]],
              'variables': count, 'clauses': len(clauses), 'caps4': caps, 'cups': cups,
              'cnf': str(cnf), 'status': 'NOT_RUN'}
    result['require_right_starter'] = not allow_no_starter
    result['fixed_A'] = sorted(fixed_A) if fixed_A is not None else None
    if solve_seconds:
        assert 0 < solve_seconds <= 8
        def limits():
            resource.setrlimit(resource.RLIMIT_AS, (512 * 1024**2, 512 * 1024**2))
        run = subprocess.run(['cadical', '-q', '-t', str(solve_seconds), str(cnf)],
                             capture_output=True, text=True, timeout=solve_seconds + 2,
                             preexec_fn=limits)
        output.with_suffix('.solver.out').write_text(run.stdout + run.stderr)
        lines = run.stdout.splitlines()
        result['solver_status_lines'] = [s for s in lines if s.startswith('s ')]
        if 's SATISFIABLE' in lines:
            model = {int(x) for s in lines if s.startswith('v ') for x in s[2:].split() if int(x) > 0}
            A = {i for i in range(m) if i + 1 in model}
            assert not A & set(D)
            assert not any(set(k) <= A for k in caps)
            assert all(set(d) & A for d in cups if len(d) == n - 1)
            failures = []
            for p in D:
                for r in [None] + sorted(A):
                    B = A | {p} if r is None else (A - {r}) | {p}
                    badcap = next((k for k in caps if set(k) <= B), None)
                    lost = next((d for d in cups if set(d) & A and not set(d) & B), None)
                    assert badcap or lost
                    failures.append({'insert': p, 'remove': r, 'cap': badcap, 'lost_cup': lost})
            result.update(status='SAT_RECHECKED', A=sorted(A), failures=failures)
        elif 's UNSATISFIABLE' in lines:
            result['status'] = 'UNSAT_UNCERTIFIED'
        else:
            result['status'] = 'UNKNOWN'
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ('status', 'cap_type', 'variables', 'clauses')} | {'A': result.get('A')}))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('input')
    p.add_argument('--n', type=int)
    p.add_argument('--cup', required=True, help='comma separated, zero based indices')
    p.add_argument('--out', required=True)
    p.add_argument('--solve-seconds', type=int, default=0)
    p.add_argument('--control-no-starter', action='store_true',
                   help='positive control only: drop E1\'s right-starter hypothesis')
    p.add_argument('--pin-a', help='positive control only: fix A to these comma-separated indices')
    a = p.parse_args()
    data = json.loads(Path(a.input).read_text())
    attack(data['P'], a.n or data['n'], list(map(int, a.cup.split(','))), a.out, a.solve_seconds,
           a.control_no_starter, set(map(int, a.pin_a.split(','))) if a.pin_a else None)


if __name__ == '__main__':
    main()
