"""Short one-thread controls: hull/subset oracle, negative fixtures, limits, packets.

Run via runner.py controls. This is not an enumeration of conjecture instances.
"""
import itertools
import json
from pathlib import Path
import random
import subprocess
import time

import runner as R


def brute(p, a, n, mode):
    """All subsets; hulls instead of capB+cupB for convexity."""
    m = len(p)
    capB, cupB = [0]*(m*m), [0]*(m*m)
    caps, hits, gons = [], [], []
    maxcap = maxcup = maxgon = min(m, 2)
    for mask in range(1 << m):
        ids = [i for i in range(m) if mask >> i & 1]
        size = len(ids)
        if size < 2:
            continue
        z = ids[0]*m + ids[-1]
        if R.chain(p, ids, -1):
            maxcap = max(maxcap, size); capB[z] = max(capB[z], size)
            if size == a-1:
                caps.append(mask)
        if R.chain(p, ids, 1):
            maxcup = max(maxcup, size); cupB[z] = max(cupB[z], size)
        if len(R.hull([p[i] for i in ids])) == size:
            maxgon = max(maxgon, size)
            if size == n-1:
                gons.append(mask)
                if mode in ('weak', 'strong'):
                    hits.append(mask)
                else:
                    u, v = ids[0], ids[-1]
                    inner = [] if mode == 'ends' else [i for i in ids[1:-1] if R.orient(p[u], p[i], p[v]) * (1 if mode == 'lower' else -1) > 0]
                    hits.append(sum(1 << i for i in [u, *inner, v]))
    models = []
    valid = maxcap < a and maxgon < n
    if valid:
        for d in range(1 << m):
            if any(d & k == k for k in caps) or any(not d & h for h in hits):
                continue
            if mode == 'strong' and any(d & g == g for g in gons):
                continue
            models.append(d)
    return dict(valid=valid, maxcap=maxcap, maxcup=maxcup, maxgon=maxgon, capB=capB, cupB=cupB,
                tau=min(map(int.bit_count, models), default=None), models=models)


def run(binary, out):
    started = time.monotonic()
    log, serial = [], 0
    def native(p, a=5, n=7, mode='lower', extra=(), packet=False, command='check'):
        nonlocal serial
        serial += 1
        folder = out/f'case-{serial:03d}'
        folder.mkdir()
        inp = folder/'input.points'
        R.write_points(inp, p)
        cmd = [str(binary), command, '--input', str(inp), '--a', str(a), '--n', str(n), '--mode', mode,
               '--time-ms', '1000', '--detail'] + list(extra)
        if packet:
            cmd += ['--out', str(folder)]
        proc = subprocess.run(cmd, capture_output=True, text=True, env=R.ENV, timeout=3,
                              preexec_fn=R.child_limit(1024))
        (folder/'stdout.jsonl').write_text(proc.stdout)
        (folder/'stderr.log').write_text(proc.stderr)
        if proc.returncode not in (0, 10, 11, 20, 30, 31):
            raise AssertionError((proc.returncode, proc.stderr, cmd))
        r = json.loads(proc.stdout.splitlines()[-1])
        expected_rc = {'OK': 0, 'NO_DELTA_COMPUTED': 10, 'NO_DELTA_WITHIN_BOUND': 11,
                       'UNKNOWN': 20, 'INVALID': 30, 'INVALID_INPUT': 31}[r['status']]
        if command == 'check':
            assert proc.returncode == expected_rc
        log.append({k: r[k] for k in ('status', 'm', 'a', 'n', 'mode', 'nodes', 'milliseconds', 'tau_lower', 'tau_upper', 'tau_exact')})
        if packet and r['status'] in ('OK', 'NO_DELTA_COMPUTED'):
            R.audit_packet(folder/('minimized.json' if command == 'minimize' else 'check.json'))
        return r, folder

    fix = json.loads((R.HERE/'fixtures.json').read_text())
    known = [('E4', 6, 'strong', 'NO_DELTA_COMPUTED'), ('E4', 6, 'weak', 'OK'),
             ('E4', 6, 'lower', 'OK'), ('upper11', 6, 'upper', 'NO_DELTA_COMPUTED'),
             ('upper11', 6, 'lower', 'OK'), ('ends9', 6, 'ends', 'NO_DELTA_COMPUTED'),
             ('ends9', 6, 'lower', 'OK'), ('etv26', 7, 'lower', 'OK'), ('etv42', 8, 'lower', 'OK')]
    fixture_paths = {}
    for name, n, mode, expected in known:
        p = R.normalize(fix[name]['P'])
        r, folder = native(p, n=n, mode=mode, packet=True)
        assert r['status'] == expected, (name, r)
        fixture_paths[name+'_'+mode] = str(folder/'check.json')
        if name == 'E4':
            assert (r['maxcap'], r['maxgon']) == (4, 5)
        if name == 'etv42':
            assert r['saturated'] == 191

    if 'parent16' in fix:
        r, folder = native(R.normalize(fix['parent16']['P']), extra=['--min-delta', '--private-witnesses'], packet=True)
        assert r['status'] == 'OK' and r['tau_exact'] and r['tau_lower'] == r['tau_upper'] == 5
        assert r['private_complete'] and len(r['private_points']) == 5
        fixture_paths['parent16_lower'] = str(folder/'check.json')

    rnd = random.Random(20261113)
    random_cases = valid_cases = 0
    for trial in range(36):
        m = 5 + trial % 5
        while True:
            xs = sorted(rnd.sample(range(-100, 101), m))
            p = [(x, rnd.randrange(-1000, 1001)) for x in xs]
            if all(R.orient(*t) for t in itertools.combinations(p, 3)):
                break
        a, n = [(4, 5), (4, 6), (5, 6), (5, 7), (5, 8), (6, 6)][trial % 6]
        mode = ['lower', 'upper', 'ends', 'weak', 'strong'][trial % 5]
        expected = brute(p, a, n, mode)
        r, _ = native(p, a, n, mode, ['--min-delta'])
        assert (r['maxcap'], r['maxcup'], r['maxgon']) == tuple(expected[k] for k in ('maxcap', 'maxcup', 'maxgon'))
        assert r['capB'] == expected['capB'] and r['cupB'] == expected['cupB']
        assert (r['status'] != 'INVALID') == expected['valid']
        if expected['valid']:
            valid_cases += 1
            assert (r['status'] == 'OK') == bool(expected['models'])
            if r['status'] == 'OK':
                mask = sum(1 << i for i in r['Delta'])
                assert mask in expected['models']
                assert r['tau_exact'] and r['tau_lower'] == r['tau_upper'] == expected['tau']
        random_cases += 1

    # Near the explicit coordinate bound, differences/products exceed int64.
    p = [(-R.BOUND, R.BOUND-1), (-R.BOUND+2, -R.BOUND), (-7, 11),
         (5, -13), (R.BOUND-3, R.BOUND), (R.BOUND, -R.BOUND+1)]
    expected = brute(p, 5, 8, 'lower')
    r, _ = native(p, n=8)
    assert r['capB'] == expected['capB'] and r['cupB'] == expected['cupB']
    # m=64 hits bit 63 and the full-universe special case; an obvious invalid cup.
    r, _ = native([(i, i*i) for i in range(64)], n=8)
    assert r['status'] == 'INVALID' and r['maxcup'] == r['maxgon'] == 64
    for p in ([], [(0, 1)], [(0, 0), (1, 1)]):
        r, _ = native(p, extra=['--min-delta'])
        assert r['status'] == 'OK' and r['tau_exact'] and r['tau_upper'] == 0
    for p, reason in [([(0, 0), (0, 1)], 'duplicate_x'), ([(0, 0), (1, 1), (2, 2)], 'collinear_triple'),
                      ([(0, 0), (R.BOUND+1, 1)], 'coordinate_bound')]:
        r, _ = native(p)
        assert r['status'] == 'INVALID_INPUT' and r['reason'] == reason
    for option, reason in [('--node-limit', 'node_limit'), ('--round-limit', 'round_limit'),
                           ('--time-ms', 'time_limit'), ('--clause-limit', 'clause_limit')]:
        r, _ = native(R.normalize(fix['E4']['P']), n=6, extra=[option, '0'])
        assert r['status'] == 'UNKNOWN' and r['reason'] == reason and r['Delta'] is None
    p = R.normalize(fix['ends9']['P'])
    r, _ = native(p, n=6, extra=['--max-delta', '0'])
    assert r['status'] == 'NO_DELTA_WITHIN_BOUND'
    r, folder = native(p, n=6, mode='ends', extra=['--minimize-ms', '1000'], packet=True, command='minimize')
    assert r['status'] == 'NO_DELTA_COMPUTED' and r['one_deletion_minimal']
    for i in range(len(r['P'])):
        assert brute(r['P'][:i]+r['P'][i+1:], 5, 6, 'ends')['models']
    assert R.cake_verdict('c log\ns VERIFIED UNSAT\n')
    for text in ('', 's UNSATISFIABLE\n', 's VERIFIED UNSAT extra\n', ' s VERIFIED UNSAT\n'):
        assert not R.cake_verdict(text)
    # Reject a corrupted packet even if its claimed status says exhaustive UNSAT.
    original = Path(fixture_paths['upper11_upper'])
    packet = json.loads(original.read_text())
    packet['witness_clauses'][0]['clause'] = []
    bad = out/'corrupt.json'; bad.write_text(json.dumps(packet))
    bad.with_suffix('.cnf').write_text(original.with_suffix('.cnf').read_text())
    try:
        R.audit_packet(bad)
    except ValueError:
        pass
    else:
        raise AssertionError('corrupt packet accepted')
    result = {'label': 'COMPUTED', 'status': 'PASS', 'native_invocations': serial,
              'small_hull_subset_cases': random_cases, 'small_valid_cases': valid_cases,
              'fixture_packets': fixture_paths, 'seconds': time.monotonic()-started,
              'max_child_rss_kb': __import__('resource').getrusage(__import__('resource').RUSAGE_CHILDREN).ru_maxrss}
    (out/'results.json').write_text(json.dumps(result, indent=2)+'\n')
    (out/'checks.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in log))
    print(json.dumps(result))
    return 0
