#!/usr/bin/env python3
"""Generate the data tables of preprint P1 from the repository records (standard library only).

Run from anywhere:  python3 -I WRITEUP/P1/tools/make_tables.py
Writes WRITEUP/P1/tables/{seeds6,seeds7,cubes6,hashes}.tex and one seed_<set>.tex per point set.

Where the printed values come from (all under cloud/es7-2026-10-19/results):
  * point-set seeds, coefficient sizes and scales: the .pts files themselves (scale from their header line);
  * point-set hashes: computed, and compared with SIX60/sets/SHA256SUMS.txt and PRIMEFOLD/SHA256SUMS;
  * sixfold cube table: solve wall times from C6UPPER/logs/cubes.txt (encoder A) and C6UPPER/logs/encb_cubes.txt
    (encoder B); proof sizes and hashes from C6UPPER/SHA256SUMS.txt; the replayed cubes from the 'sampling' record of
    C6C7REVIEW/replay.json; the phase order of each cube is computed from its label (bit j = sign of the j-th of
    Y(1,3), Y(1,4), Y(2,3), Y(2,4), Y(3,4), with Y(1,2) true, as in C6UPPER/tools/mkcubes.py) and compared with the
    order column of C6UPPER/README.md;
  * hash appendix: C6UPPER/SHA256SUMS.txt, C7UPPER/SHA256SUMS.txt; the Lean file hash is computed and compared with the
    prefix recorded in WRITEUP/note/k8_soundness.tex and, if git is available, with the blob of the commit named there.
The script's own constants are the lists of files and their labels, and the locations of these records.

Checks performed (the script exits with status 1 if any fails):
  * every point-set file has the recorded SHA-256;
  * every point-set file is invariant under multiplication by zeta (a cyclic shift of the coefficient vector, since
    zeta^m = 1): its non-centre rows are distinct and split into orbits of exactly m rows each; the printed seed of an
    orbit is its first row in file order, so the m cyclic shifts of the printed seeds are exactly the non-centre rows;
    files whose rows come in layer blocks (each block of m consecutive rows = the shifts of its first row) are reported;
  * the sevenfold files have exactly one all-zero row (the centre) and the sixfold files none;
  * the cube labels with consistent=True in cubes.txt are exactly the 12 labels whose bits are a transitive order, and
    the computed orders agree with C6UPPER/README.md;
  * the files cited in the hash appendix hash to the values recorded in the SHA256SUMS files.
"""
import hashlib
import itertools
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
P1 = os.path.dirname(HERE)
RES = os.path.dirname(os.path.dirname(P1))          # .../results
OUT = os.path.join(P1, 'tables')
FAIL = []
INFO = []


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def read_sums(path):
    """Map file name -> hash from a 'hash  name' list (other line shapes ignored)."""
    d = {}
    for line in open(path, encoding='utf-8'):
        m = re.match(r'^([0-9a-f]{64})\s+(\S+)\s*$', line)
        if m:
            d[m.group(2)] = m.group(1)
    return d


def read_lrat(path, marker):
    """Rows 'cube raw zst bytes' after the marker line."""
    rows, on = {}, False
    for line in open(path, encoding='utf-8'):
        if line.startswith('#'):
            on = line.startswith(marker)
            continue
        parts = line.split()
        if on and len(parts) == 4 and re.match(r'^c[01]{5}$', parts[0]):
            rows[parts[0]] = (parts[1], int(parts[3]))
    return rows


def rows_of(path):
    out = []
    for line in open(path, encoding='utf-8'):
        line = line.split('#')[0].split()
        if line:
            out.append(tuple(int(x) for x in line))
    return out


def shifts(r, m):
    return [tuple(r[(i - j) % m] for i in range(m)) for j in range(m)]


def seeds(path, m, centre):
    """Return (seeds in file order, number of rows, layer-block order?, largest number of decimal digits)."""
    rows = rows_of(path)
    if any(len(r) != m for r in rows):
        FAIL.append(f'{path}: a row does not have {m} coefficients')
        return [], len(rows), False, 0
    zero = [r for r in rows if not any(r)]
    if len(zero) != (1 if centre else 0):
        FAIL.append(f'{path}: {len(zero)} zero rows')
    body = [r for r in rows if any(r)]
    if len(set(body)) != len(body):
        FAIL.append(f'{path}: repeated rows')
    if len(body) % m:
        FAIL.append(f'{path}: {len(body)} non-centre rows')
    bodyset, seen, out = set(body), set(), []
    for r in body:
        if r in seen:
            continue
        orb = shifts(r, m)
        if len(set(orb)) != m:
            FAIL.append(f'{path}: orbit of {r} has fewer than {m} points')
        for s in orb:
            if s not in bodyset:
                FAIL.append(f'{path}: cyclic shift {s} of {r} missing (not {m}-fold invariant)')
        seen.update(orb)
        out.append(r)
    blocks = all(body[o * m:(o + 1) * m] == shifts(body[o * m], m) for o in range(len(body) // m))
    digits = max(len(str(abs(x))) for r in rows for x in r)
    return out, len(rows), blocks, digits


def header_scale(path):
    """The scale field of the header line, as TeX: 2^k or 10^k when exact, else the number."""
    first = open(path, encoding='utf-8').readline()
    m = re.search(r'scale=([0-9.e+^]+)', first)
    if not m:
        return None
    s = m.group(1)
    if '^' in s:
        b, e = s.split('^')
        return f'{b}^{{{e}}}'
    v = int(float(s))
    for b in (2, 10):
        k = 0
        while b ** k < v:
            k += 1
        if b ** k == v:
            return f'{b}^{{{k}}}'
    return str(v)


def fmt_seed(r):
    nz = max(i for i, x in enumerate(r) if x) if any(r) else 0
    if nz <= 1:
        return f'({r[0]},{r[1]})'
    return '(' + r',\allowbreak '.join(str(x) for x in r[:nz + 1]) + ')'


def order_of(bits):
    """Phase order of psi_1..psi_4 from Y(1,2)=1 and bits for Y(1,3),Y(1,4),Y(2,3),Y(2,4),Y(3,4); None if intransitive."""
    less = {(1, 2): True}
    for (i, j), b in zip([(1, 3), (1, 4), (2, 3), (2, 4), (3, 4)], bits):
        less[(i, j)] = bool(b)
    for perm in itertools.permutations([1, 2, 3, 4]):
        pos = {v: k for k, v in enumerate(perm)}
        if all((pos[i] < pos[j]) == v for (i, j), v in less.items()):
            return '<'.join(map(str, perm))
    return None


def read_times(path, phase_flag):
    """Final solve wall time per cube label from a runner log ('HH:MM:SS cXXXXX [consistent=..] UNSAT 123.4s')."""
    times, cons = {}, {}
    for line in open(path, encoding='utf-8'):
        m = re.match(r'^\S+ (c[01]{5})(?: consistent=(True|False))? UNSAT ([0-9.]+)s\s*$', line)
        if m:
            times[m.group(1)] = float(m.group(3))
            if m.group(2):
                cons[m.group(1)] = m.group(2) == 'True'
    if phase_flag and len(cons) != 32:
        FAIL.append(f'{path}: {len(cons)} cubes with a consistent= flag')
    return times, cons


def main():
    os.makedirs(OUT, exist_ok=True)

    # ---------------- sixfold sets ----------------
    six = read_sums(os.path.join(RES, 'SIX60/sets/SHA256SUMS.txt'))
    names6 = [('A', 'c6_60pts_A.pts'), ('B', 'c6_60pts_B.pts'), ('C', 'c6_60pts_C.pts'),
              ("C$'$", 'c6_60pts_C2.pts'), ('D', 'c6_60pts_D.pts')]
    lines = ['% generated by tools/make_tables.py -- do not edit']
    for lab, fn in names6:
        p = os.path.join(RES, 'SIX60/sets', fn)
        h = sha(p)
        if six.get(fn) != h:
            FAIL.append(f'{fn}: hash {h} differs from record')
        s, n, blocks, dig = seeds(p, 6, centre=False)
        if n != 60 or len(s) != 10:
            FAIL.append(f'{fn}: n={n}, orbits={len(s)}')
        if not blocks:
            FAIL.append(f'{fn}: rows are not in layer blocks')
        scale = header_scale(p)
        if scale is None:
            FAIL.append(f'{fn}: no scale in header')
        item = (r'\item[' + lab + r'] \dirn{SIX60/sets/' + fn + r'} (SHA-256 \texttt{' + h[:16] +
                r'\dots}; scale $' + str(scale) + r'$): ' + ', '.join('$' + fmt_seed(r) + '$' for r in s) + '.')
        lines.append(item)
        INFO.append(f'{fn}: 60 rows, 10 orbits, layer blocks, scale {scale}, coefficients up to {dig} digits')
        open(os.path.join(OUT, 'seed_' + fn.replace('.pts', '') + '.tex'), 'w').write(
            '% generated by tools/make_tables.py -- do not edit\n' + item + '\n')
    open(os.path.join(OUT, 'seeds6.tex'), 'w').write('\n'.join(lines) + '\n')

    # ---------------- sevenfold sets (all eight files) ----------------
    pf = read_sums(os.path.join(RES, 'PRIMEFOLD/SHA256SUMS'))
    names7 = ['c7_64pts_small.pts', 'c7_64pts_9layers_centre.pts', 'c7_64_own_s1000.pts',
              'c7_64pts_9layers_centre_own.pts', 'p7_compound_64.pts', 'p7_two_orbit_64.pts',
              'rule_p7_64pts.pts', 'm7_x2_G9s_centre.pts']
    listed = sorted(k for k in pf if k.startswith('sets/k8/'))
    if sorted('sets/k8/' + f for f in names7) != listed:
        FAIL.append(f'PRIMEFOLD/SHA256SUMS lists {listed}, not the eight files of the paper')
    lines = ['% generated by tools/make_tables.py -- do not edit']
    for fn in names7:
        p = os.path.join(RES, 'PRIMEFOLD/sets/k8', fn)
        h = sha(p)
        if pf.get('sets/k8/' + fn) != h:
            FAIL.append(f'{fn}: hash {h} differs from record')
        s, n, blocks, dig = seeds(p, 7, centre=True)
        if n != 64 or len(s) != 9:
            FAIL.append(f'{fn}: n={n}, orbits={len(s)}')
        item = (r'\item[\dirn{' + fn.replace('.pts', '') + r'}] (SHA-256 \texttt{' + h[:16] +
                r'\dots}; coefficients of at most ' + str(dig) + r' digits' +
                ('' if blocks else r'; rows not in layer order') + r'): the centre and ' +
                ', '.join('$' + fmt_seed(r) + '$' for r in s) + '.')
        lines.append(item)
        INFO.append(f'{fn}: 64 rows, centre + 9 orbits, layer blocks: {blocks}, coefficients up to {dig} digits')
        open(os.path.join(OUT, 'seed_' + fn.replace('.pts', '') + '.tex'), 'w').write(
            '% generated by tools/make_tables.py -- do not edit\n' + item + '\n')
    open(os.path.join(OUT, 'seeds7.tex'), 'w').write('\n'.join(lines) + '\n')

    # ---------------- sixfold cube table ----------------
    tA, consA = read_times(os.path.join(RES, 'C6UPPER/logs/cubes.txt'), True)
    tB, _ = read_times(os.path.join(RES, 'C6UPPER/logs/encb_cubes.txt'), False)
    labels = ['c' + ''.join(map(str, b)) for b in itertools.product((1, 0), repeat=5)]
    orders = {c: order_of([int(x) for x in c[1:]]) for c in labels}
    phase = sorted(c for c in labels if orders[c])
    if len(phase) != 12 or set(phase) != {c for c, v in consA.items() if v}:
        FAIL.append('phase-order cubes: computed set differs from consistent=True in cubes.txt')
    if set(tA) != set(labels) or set(tB) != set(labels):
        FAIL.append(f'cube logs: {len(tA)} / {len(tB)} cubes with a time')
    readme = open(os.path.join(RES, 'C6UPPER/README.md'), encoding='utf-8').read()
    for line in readme.splitlines():
        m = re.match(r'^\| (c[01]{5}) \| ([0-9<]+) \|', line)
        if m and orders.get(m.group(1)) != m.group(2):
            FAIL.append(f'{m.group(1)}: README order {m.group(2)} != computed {orders.get(m.group(1))}')
    contra_A = [tA[c] for c in labels if not orders[c]]
    contra_B = [tB[c] for c in labels if not orders[c]]
    INFO.append(f'contradictory cubes: A {min(contra_A)}-{max(contra_A)} s, B {min(contra_B)}-{max(contra_B)} s (wall)')
    INFO.append(f'phase-order cubes: A {min(tA[c] for c in phase)}-{max(tA[c] for c in phase)} s, '
                f'B {min(tB[c] for c in phase)}-{max(tB[c] for c in phase)} s (wall)')
    sums6 = os.path.join(RES, 'C6UPPER/SHA256SUMS.txt')
    lA = read_lrat(sums6, '# LRAT proofs')
    lB = read_lrat(sums6, '# encoder-B LRAT')
    if set(lA) != set(labels) or set(lB) != set(labels):
        FAIL.append(f'LRAT records: {len(lA)} / {len(lB)} cubes')
    c6 = read_sums(sums6)
    rep = json.load(open(os.path.join(RES, 'C6C7REVIEW/replay.json'), encoding='utf-8'))
    replayed_A, replayed_B = set(rep['sampling']['A']), set(rep['sampling']['B'])
    # the replayed cube CNFs and proofs must be the recorded ones
    byhash = {v: k for k, v in c6.items()}
    for pr in rep['proofs']:
        name = pr['name']
        if name.startswith(('A6_', 'B6_')):
            enc, cube = name[0], name[3:]
            want = cube + '.cnf' if enc == 'A' else 'B/' + cube + '.cnf'
            if byhash.get(pr['cnf_sha256']) != want:
                FAIL.append(f'replay {name}: CNF hash not the recorded {want}')
            rec = (lA if enc == 'A' else lB)[cube][0]
            if pr['raw_sha256'] != rec:
                FAIL.append(f'replay {name}: proof hash differs from record')
            if cube not in (replayed_A if enc == 'A' else replayed_B):
                FAIL.append(f'replay {name}: not in the sampling record')
    INFO.append(f'replayed (C6C7REVIEW/replay.json): A {sorted(replayed_A)}, B {sorted(replayed_B)}')
    lines = ['% generated by tools/make_tables.py -- do not edit']
    totA = totB = 0
    for cube in phase:
        hA, bA = lA[cube]
        hB, bB = lB[cube]
        totA += bA
        totB += bB
        dA = r'$^\dagger$' if cube in replayed_A else ''
        dB = r'$^\dagger$' if cube in replayed_B else ''
        ordtex = '$' + orders[cube].replace('<', '{<}') + '$'
        lines.append(rf'\texttt{{{cube}}} & {ordtex} & {tA[cube]:,.0f} & {bA / 1e9:.2f} & \texttt{{{hA[:12]}}}{dA}'
                     rf' & {tB[cube]:,.0f} & {bB / 1e9:.2f} & \texttt{{{hB[:12]}}}{dB} \\')
    lines.append(r'\midrule')
    lines.append(rf'\multicolumn{{3}}{{@{{}}l}}{{total, 12 phase orders}} & {totA / 1e9:.1f} & & & {totB / 1e9:.1f} & \\')
    open(os.path.join(OUT, 'cubes6.tex'), 'w').write('\n'.join(lines) + '\n')
    allA = sum(b for _, b in lA.values())
    allB = sum(b for _, b in lB.values())
    INFO.append(f'LRAT bytes: A {totA} (12) / {allA} (32); B {totB} (12) / {allB} (32)')

    # ---------------- hash appendix ----------------
    c7 = read_sums(os.path.join(RES, 'C7UPPER/SHA256SUMS.txt'))
    lean = os.path.join(RES, 'LAYERLEAN/LayerLemma.lean')
    lean_h = sha(lean)
    note = open(os.path.join(RES, 'WRITEUP/note/k8_soundness.tex'), encoding='utf-8').read()
    m = re.search(r'LayerLemma\.lean\}\s*\(SHA-256\s*\\texttt\{([0-9a-f]+)\\dots\}, the file as committed in\s*'
                  r'\\texttt\{([0-9a-f]+)\}', note)
    if not m or not lean_h.startswith(m.group(1)):
        FAIL.append(f'LayerLemma.lean: {lean_h} does not match the prefix recorded in WRITEUP/note/k8_soundness.tex')
    else:
        try:
            blob = subprocess.run(['git', 'show', m.group(2) + ':cloud/es7-2026-10-19/results/LAYERLEAN/LayerLemma.lean'],
                                  cwd=RES, capture_output=True, check=True).stdout
            if hashlib.sha256(blob).hexdigest() != lean_h:
                FAIL.append(f'LayerLemma.lean differs from the blob of commit {m.group(2)}')
            else:
                INFO.append(f'LayerLemma.lean = blob of commit {m.group(2)} ({lean_h[:16]}...)')
        except (OSError, subprocess.CalledProcessError):
            INFO.append('git not available: LayerLemma.lean checked against the recorded prefix only')
    items = [
        ('LAYERLEAN/LayerLemma.lean', 'LAYERLEAN/LayerLemma.lean', lean_h),
        ('C7UPPER/gen.py (encoder A)', 'C7UPPER/gen.py', c7['gen.py']),
        ('C7UPPER/gen\\_b.py (encoder B, odd $m$)', 'C7UPPER/gen_b.py', c7['gen_b.py']),
        ('C6UPPER/encb/gen\\_b2.py (encoder B)', 'C6UPPER/encb/gen_b2.py', c6['encb/gen_b2.py']),
        ('C7UPPER/addunits.py', 'C7UPPER/addunits.py', c7['addunits.py']),
        ('C6UPPER/tools/mkcubes.py', 'C6UPPER/tools/mkcubes.py', c6['tools/mkcubes.py']),
        ('C6UPPER/tools/verify\\_cover.py', 'C6UPPER/tools/verify_cover.py', c6['tools/verify_cover.py']),
        ('A, $(6,8,11)$: \\texttt{m6K8t11.cnf}', None, c6['m6K8t11.cnf']),
        ('A, $(6,8,11)+Y(1,2)$: \\texttt{full\\_Y12.cnf}', None, c6['full_Y12.cnf']),
        ('B, $(6,8,11)$: \\texttt{B\\_m6K8t11.cnf}', None, c6['B_m6K8t11.cnf']),
        ('B, $(6,8,11)+Y(1,2)$: \\texttt{B/full\\_Y12.cnf}', None, c6['B/full_Y12.cnf']),
        ('A, $(7,8,10)$: \\texttt{cnf/m7K8t10.cnf}', None, c7['cnf/m7K8t10.cnf']),
        ('A, $(7,8,10)+H(1)$: \\texttt{cnf/m7K8t10\\_H1.cnf}', None, c7['cnf/m7K8t10_H1.cnf']),
        ('B, $(7,8,10)$: \\texttt{cnfb/m7K8t10.cnf}', None, c7['cnfb/m7K8t10.cnf']),
        ('LRAT, A $(7,8,10)+H(1)$', None, c7['proofs/m7K8t10_H1.lrat']),
        ('LRAT, B $(7,8,10)$', None, c7['proofs/B_full_m7K8t10.lrat']),
    ]
    lines = ['% generated by tools/make_tables.py -- do not edit']
    for label, path, h in items:
        if path is not None:
            got = sha(os.path.join(RES, path))
            if got != h:
                FAIL.append(f'{path}: {got} != recorded {h}')
        lines.append(label + r' & \texttt{' + h + r'} \\')
    open(os.path.join(OUT, 'hashes.tex'), 'w').write('\n'.join(lines) + '\n')

    print('\n'.join(INFO))
    if FAIL:
        print('FAIL'); print('\n'.join(FAIL)); sys.exit(1)
    print('PASS: tables written to', OUT)


if __name__ == '__main__':
    main()
