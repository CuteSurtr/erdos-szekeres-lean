#!/usr/bin/env python3
"""archive_r36.py -- move the proofs of all certified leaves to proof-archives/es7-r36-20261121/.

Run after verify_cover.py.  Reads summary.json (summarize_r36.py) for the certified leaves; for each, moves
<dir>/<id>.lrat.zst to <archive>/<dir>/, then writes <archive>/SHA256SUMS (SHA-256 of every .zst file, recomputed
after the move) and <archive>/lrat_sha256.tsv (id, case, units, CNF SHA-256, raw LRAT SHA-256 and bytes, heap, from
the results.tsv rows that certified the leaf).  Also copies the case CNF hashes and a README.
"""
import hashlib, json, os, shutil, sys
D = os.path.dirname(os.path.abspath(__file__))
ARC = '<mac-repo>/proof-archives/es7-r36-20261121'
os.makedirs(ARC, exist_ok=True)
summ = json.load(open(os.path.join(D, 'summary.json')))
rows = {}
for sub in ('cubes', 'cubes_b', 'cubes2'):
    res = os.path.join(D, sub, 'results.tsv')
    if os.path.exists(res):
        for line in open(res):
            f = line.rstrip('\n').split('\t')
            if len(f) >= 11 and f[3] == 'verified':
                rows[f[0]] = (sub, f)
out = []
for case in ('A', 'B'):
    for jid in summ[case]['certified']:
        sub, f = rows[jid]
        src = os.path.join(D, sub, jid + '.lrat.zst')
        dst_dir = os.path.join(ARC, sub)
        os.makedirs(dst_dir, exist_ok=True)
        dst = os.path.join(dst_dir, jid + '.lrat.zst')
        if os.path.exists(src):
            shutil.move(src, dst)
        if not os.path.exists(dst):
            print('MISSING', jid); continue
        out.append((sub, jid, f))
sums = []
for sub, jid, f in out:
    p = os.path.join(ARC, sub, jid + '.lrat.zst')
    h = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    sums.append('%s  %s/%s.lrat.zst' % (h, sub, jid))
open(os.path.join(ARC, 'SHA256SUMS'), 'w').write('\n'.join(sums) + '\n')
with open(os.path.join(ARC, 'lrat_sha256.tsv'), 'w') as g:
    g.write('dir\tid\tcase\tunits\tcnf_sha256\tlrat_sha256\tlrat_bytes\tcake_heap_mb\n')
    for sub, jid, f in out:
        g.write('\t'.join([sub, jid, f[1], f[2], f[6], f[8], f[7], f[11] if len(f) > 11 else '']) + '\n')
open(os.path.join(ARC, 'README.txt'), 'w').write(
    'Rung N = 36 of the M(5;7) owner model (record M57R36N20261121), 21 Nov 2026.\n'
    'Each file is the zstd-compressed LRAT proof (CaDiCaL 3.0.1, accepted by cake_lpr) of one cube leaf:\n'
    'base CNF (case A run/c36_rle13.cnf aba65111..., case B run/c36_tle22.cnf 08b8ea9c...) plus the unit clauses\n'
    'in lrat_sha256.tsv.  Regenerate a leaf CNF: copy the base with the clause count raised by the number of units,\n'
    'append one line "u 0" per unit.  Check: zstd -dc FILE > x.lrat; cake_lpr --CML_HEAP_SIZE=6000 leaf.cnf x.lrat\n')
print('archived', len(out), 'proofs to', ARC)
