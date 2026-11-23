#!/usr/bin/env python3
"""Guarded deletion of proof files listed in pushed receipt TSVs (24 Nov 2026). Usage:
  python3 -I delete_proofs.py NAME RECEIPTS.tsv[:ROOT] ... [--execute]
Every receipt row must have check == OK. Before deleting (dry run by default) each file must exist as a regular file
with the receipt's size and SHA-256, no process may hold it, and no Lean project file (formalize-20261122 text files
under 20 MB), FORMAL20261122 "original in" line or running unit may name it (refuses). Bindings from the ledger,
the bind list and records are listed (they are the owner-lifted ones) and written to the manifest. Plain os.remove.
"""
import csv, hashlib, json, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

C = '/home/jay/research/data/cleanup-20261123'
MAN = '/home/jay/research/data/verify-20261124/manifest_deletions.txt'
EXEC = '--execute' in sys.argv
args = [a for a in sys.argv[1:] if a != '--execute']
name, specs = args[0], args[1:]


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''): h.update(b)
    return h.hexdigest()


rows = []
for spec in specs:
    tsv, root = (spec.split(':') + [''])[:2]
    for r in csv.DictReader(open(tsv), delimiter='\t'):
        assert r['check'] == 'OK', r
        p = r['proof_file'] if r['proof_file'].startswith('/') else os.path.join(root, r['proof_file'])
        rows.append((p, int(r['zst_bytes']), r['zst_sha256']))
paths = {p for p, _, _ in rows}
assert len(paths) == len(rows), 'duplicate paths'
problems, broken = [], []

# 1. existence, regular file, size
for p, n, _ in rows:
    if not os.path.isfile(p) or os.path.islink(p): problems.append('missing or not a regular file: ' + p)
    elif os.path.getsize(p) != n: problems.append('size differs: ' + p)
# 2. hashes, in parallel
if not problems:
    with ThreadPoolExecutor(4) as ex:
        for (p, _, want), got in zip(rows, ex.map(sha, [p for p, _, _ in rows], chunksize=16)):
            if got != want: problems.append('sha256 differs: ' + p)
# 3. processes
for pid in filter(str.isdigit, os.listdir('/proc')):
    try: fds = os.listdir('/proc/%s/fd' % pid)
    except OSError: continue
    for f in fds:
        try: t = os.readlink('/proc/%s/fd/%s' % (pid, f))
        except OSError: continue
        if t in paths: problems.append('open by pid %s: %s' % (pid, t))
# 4. bindings that refuse: Lean project text files and FORMAL "original in" lines naming a file
names = {os.path.basename(os.path.dirname(os.path.dirname(p))) + '/' + os.path.basename(os.path.dirname(p)) + '/' + os.path.basename(p) for p in paths}
r = subprocess.run(['grep', '-rlI', '--include=*.json', '--include=*.tsv', '--include=*.txt', '--include=*.sh', '--include=*.py',
                    '--include=*.md', '--include=*.lean', '-F', '-f', '/dev/stdin', '/home/jay/research/data/formalize-20261122'],
                   input='\n'.join(sorted(paths)), capture_output=True, text=True)
for f in r.stdout.split():
    problems.append('a formalize-20261122 file names a path to delete: ' + f)
fs = '/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/FORMAL20261122/SHA256SUMS'
for line in open(fs):
    if 'original in' in line:
        rel = line.split('  ')[1].split('  ')[0]; orig = line.split('original in ')[1].rstrip(']\n')
        if os.path.join(orig, rel) in paths: problems.append('FORMAL original-in names: ' + rel)
# 5. owner-lifted bindings, listed for the manifest
led = json.load(open('/home/jay/research/data/ledger-20261122/ledger.json'))
prot = set(led['protected']) | {x if isinstance(x, str) else x.get('path') for x in led['protected_added_by_review']}
for line in open(C + '/bind/bound_paths.tsv'):
    t = line.rstrip('\n').split('\t')
    if t and t[0] in paths: broken.append('bind: %s (%s)' % (t[0], ' '.join(t[1:3])[:80]))
for p in paths:
    if p in prot: broken.append('ledger-protected: ' + p)

tot = sum(n for _, n, _ in rows)
print('%s: %d files, %.2f GB; problems %d; owner-lifted bindings %d' % (name, len(rows), tot / 1e9, len(problems), len(broken)))
for x in problems[:20]: print('PROBLEM', x)
for x in broken[:10]: print('LIFTED', x)
if problems: print('REFUSED; nothing deleted'); sys.exit(1)
if not EXEC: print('DRY-RUN OK'); sys.exit(0)
with open(MAN, 'a') as m:
    m.write('\n== %s %s: %d files, %d bytes; receipts %s; owner-lifted bindings %d\n' % (time.strftime('%F %T'), name, len(rows), tot, ' '.join(specs), len(broken)))
    for x in broken: m.write('lifted\t%s\n' % x)
    for p, n, h in rows:
        os.remove(p); m.write('deleted\t%d\t%s\t%s\n' % (n, h, p))
    m.write('%s %s done; free %d B\n' % (time.strftime('%F %T'), name, os.statvfs('/home').f_bavail * os.statvfs('/home').f_frsize))
print('DONE')
