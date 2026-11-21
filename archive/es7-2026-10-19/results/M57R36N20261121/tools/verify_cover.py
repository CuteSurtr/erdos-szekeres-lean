#!/usr/bin/env python3
"""verify_cover.py -- independent check of the rung N = 36 cube campaign (stdlib only).

For each case (A = run/c36_rle13.cnf, B = run/c36_tle22.cnf):
  1. the base CNF has the recorded SHA-256 (aba65111... / 08b8ea9c...);
  2. every leaf counted as verified has a cake_lpr output file containing the exact line
     's VERIFIED UNSAT', and its archived proof cubes/<id>.lrat.zst decompresses to the SHA-256
     recorded at check time (results.tsv);
  3. the leaf CNF regenerated here from base + unit clauses (own code, not drive.py's) has the
     SHA-256 recorded at check time;
  4. the verified leaves cover every assignment of the occupancy variables they mention: for the
     union V of their literal variables, each of the 2^|V| sign patterns satisfies all literals of
     at least one verified leaf.
A case whose monolithic CNF has its own accepted certificate counts as covered: run/<base>.cake holds the exact line
and run/<base>.cake.meta (written before cake_lpr ran) names the base CNF with its recorded SHA-256.
Leaves are read from cubes/, cubes_b/ (B-only driver) and cubes2/ (drive2.py) results.tsv.
Usage: verify_cover.py [--no-regen]
"""
import hashlib, itertools, json, os, subprocess, sys

D = os.path.dirname(os.path.abspath(__file__))
BASE = {'A': ('run/c36_rle13.cnf', 'aba65111d42151131a55e7596043721bd86fe94d05c8fea0b2750212d2808bbe'),
        'B': ('run/c36_tle22.cnf', '08b8ea9c9c588aa242485163a3d4836a0c79f8bd91c61ac25357010dc2bd9339')}
OCC0 = 32759


def sha_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    return h.hexdigest()


def sha_cube(base, units):
    """SHA-256 of base CNF with the clause count raised by len(units) and the unit clauses appended."""
    h = hashlib.sha256()
    with open(base, 'rb') as f:
        head = b''
        while True:
            line = f.readline()
            if line.startswith(b'p cnf'):
                p = line.split()
                h.update(head)
                h.update(b'p cnf %s %d\n' % (p[2], int(p[3]) + len(units)))
                break
            head += line
        for b in iter(lambda: f.read(1 << 22), b''):
            h.update(b)
    for u in units:
        h.update(b'%d 0\n' % u)
    return h.hexdigest()


def verified_line(path):
    try:
        return any(l.strip() == 's VERIFIED UNSAT' for l in open(path, errors='replace'))
    except FileNotFoundError:
        return False


def main():
    regen = '--no-regen' not in sys.argv
    rows = {}
    for sub in ('cubes', 'cubes_b', 'cubes2'):
        res = os.path.join(D, sub, 'results.tsv')
        if not os.path.exists(res):
            continue
        for line in open(res):
            f = line.rstrip('\n').split('\t')
            if len(f) >= 11 and f[3] == 'verified':
                rows[sub + '/' + f[0]] = {'case': f[1], 'units': [int(x) for x in f[2].split()], 'cnf_sha': f[6],
                                          'lrat_bytes': f[7], 'lrat_sha': f[8], 'cake': f[9], 'dir': sub, 'id': f[0]}
    ok_all = True
    for case, (base, want) in BASE.items():
        bp = os.path.join(D, base)
        got = sha_file(bp)
        print(f'case {case}: base {base} sha {got[:16]}... {"OK" if got == want else "MISMATCH"}')
        ok = got == want
        mono = os.path.join(D, base.replace('.cnf', '.cake'))
        meta = mono + '.meta'
        if verified_line(mono) and os.path.exists(meta):
            m = open(meta).read()
            tied = (want + '  ' + base) in m
            print(f'case {case}: monolithic certificate {os.path.basename(mono)}: exact line yes; '
                  f'meta names the base CNF hash: {"yes" if tied else "NO"}; base hash: {"OK" if ok else "MISMATCH"}')
            okm = ok and tied
            ok_all = ok_all and okm
            print(f'case {case}: {"COVERED (monolithic)" if okm else "NOT COVERED"}')
            continue
        leaves = {k: v for k, v in rows.items() if v['case'] == case}
        bad = 0
        for jid, r in sorted(leaves.items()):
            cake = os.path.join(D, r['dir'], r['id'] + '.cake')
            if not verified_line(cake):
                print('  no exact cake line:', jid); bad += 1; continue
            z = os.path.join(D, r['dir'], r['id'] + '.lrat.zst')
            if os.path.exists(z):
                d = subprocess.run('zstd -dc "%s" | shasum -a 256' % z, shell=True, capture_output=True,
                                   text=True).stdout.split()[0]
                if d != r['lrat_sha']:
                    print('  proof hash mismatch:', jid); bad += 1; continue
            else:
                print('  archived proof missing:', jid); bad += 1; continue
            if regen and sha_cube(bp, r['units']) != r['cnf_sha']:
                print('  cube CNF hash mismatch:', jid); bad += 1; continue
        V = sorted({abs(u) for r in leaves.values() for u in r['units']})
        uncovered = 0
        lits = [set(r['units']) for r in leaves.values()]
        for signs in itertools.product((1, -1), repeat=len(V)):
            a = {s * v for s, v in zip(signs, V)}
            if not any(L <= a for L in lits):
                uncovered += 1
        print(f'case {case}: {len(leaves)} verified leaves, {bad} bad, variables {[v - OCC0 for v in V]}, '
              f'uncovered patterns {uncovered} of {2 ** len(V)}')
        ok = ok and bad == 0 and uncovered == 0 and len(leaves) > 0
        ok_all = ok_all and ok
        print(f'case {case}: {"COVERED" if ok else "NOT COVERED"}')
    print('RUNG 36:', 'BOTH CASES COVERED' if ok_all else 'NOT COMPLETE')


if __name__ == '__main__':
    main()
