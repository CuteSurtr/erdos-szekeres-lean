#!/usr/bin/env python3
"""Mirror the Lean work dirs of formalize-20261122 into the repo record FORMAL20261122.

Usage: python3 -I sync_record.py <record dir> <project> [<project> ...]

Each named project folder in the record is rebuilt from its work dir; other record paths (README.md, evidence/)
are never touched, and their SHA256SUMS entries are kept. Copied: sources, tools, docs, logs and other small text
files. Hash-only (listed as NOT COPIED): bulk data (descriptor files, large tables) and binaries (printer exes,
loose oleans), which stay in the work dir. Build dirs, olean stores and exports are skipped entirely.
"""
import hashlib, os, shutil, sys

SRC = os.path.dirname(os.path.abspath(__file__))
SKIP_DIRS = {'olean', 'export', '.lake', '__pycache__', 'scratch', 'tmp', 'sbx', 'out_big', 'cnf', 'proofs', 'cake_tmp'}
EXTS = {'.lean', '.py', '.sh', '.md', '.json', '.txt', '.tsv', '.cpp', '.hpp', '.c', '.h', '.diff', '.toml', '.log'}
SMALL = 200_000      # any text file up to this size is copied
LARGE = 3_000_000    # nothing larger is copied


def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def is_text(path):
    with open(path, 'rb') as f:
        return b'\0' not in f.read(8192)


def classify(rel, size, path):
    """'copy', 'bulk' (hash only) or 'binary' (hash only)."""
    segs = rel.split(os.sep)
    ext = os.path.splitext(rel)[1].lower()
    if not is_text(path):
        return 'binary'
    # .lean/.json over 1 MB are generated (exported chunk modules, skeletons): hash only, like the exports
    if size > LARGE or (ext == '.txt' and size > SMALL) or (('desc' in segs or 'ctl' in segs) and size > 50_000) \
            or (ext in ('.lean', '.json') and size > 1_000_000) or '/selftest/ref/' in rel:
        return 'bulk'
    if ext in EXTS or size <= SMALL:
        return 'copy'
    return 'bulk'


def main(dst, projects):
    rows = {}
    old = os.path.join(dst, 'SHA256SUMS')
    if os.path.exists(old):
        for line in open(old):
            parts = line.rstrip('\n').split('  ')
            if len(parts) >= 2 and parts[1].split('/')[0] not in projects:
                rows[parts[1]] = line.rstrip('\n')          # keep entries of untouched paths
    counts = {'copy': 0, 'bulk': 0, 'binary': 0}
    for p in projects:
        assert os.path.isdir(os.path.join(SRC, p)), p
        if os.path.isdir(os.path.join(dst, p)):
            shutil.rmtree(os.path.join(dst, p))
        for root, dirs, files in os.walk(os.path.join(SRC, p)):
            dirs[:] = [d for d in dirs if not (d.startswith('build') or d in SKIP_DIRS)]
            for f in files:
                fp = os.path.join(root, f)
                if os.path.islink(fp):
                    continue
                rel = os.path.relpath(fp, SRC)
                kind = classify(rel, os.path.getsize(fp), fp)
                counts[kind] += 1
                if kind == 'copy':
                    out = os.path.join(dst, rel)
                    os.makedirs(os.path.dirname(out), exist_ok=True)
                    shutil.copy2(fp, out)
                    rows[rel] = f'{sha(out)}  {rel}'
                else:
                    rows[rel] = f'{sha(fp)}  {rel}  [NOT COPIED: {kind}; original in {SRC}]'
    with open(old, 'w') as f:
        f.write('\n'.join(rows[k] for k in sorted(rows)) + '\n')
    print(counts, len(rows), 'entries in SHA256SUMS')


if __name__ == '__main__':
    main(os.path.abspath(sys.argv[1]), sys.argv[2:])
