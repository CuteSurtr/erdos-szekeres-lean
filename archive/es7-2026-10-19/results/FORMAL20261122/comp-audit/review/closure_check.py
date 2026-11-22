#!/usr/bin/env python3
"""lrev closure check (own code, read-only).

pre:  re-hash every module of the worker's closure.tsv on the review LEAN_PATH (11 lake roots, chain311/olean, the
      worker's out/olean): exactly one root must provide the .olean, it must be the root closure.tsv names, and its
      sha256 must equal closure.tsv, the library.json pin (lake/toolchain roots), chain311 build.tsv's last ok row
      (chain311 root) or AUDIT.md's out/olean table (worker root). Also hashes the .olean.server/.olean.private
      companions (recorded only; this also keeps the pages in cache before the unit starts).
post: the 'module ...' lines of review.log must list exactly closure.tsv's modules, in the same order.
usage: closure_check.py pre|post
"""
import csv, hashlib, json, os, re, sys

REPO = '/home/jay/research/lean/erdos-szekeres-lean'
CH = REPO + '/experiments/omission-compact-checker-2026-11-05/build/chain311'
W = '/home/jay/research/data/formalize-20261122/comp-audit'
R = W + '/review'
ROOTS = open(CH + '/lake-lean-path.txt').read().strip().split(':') + [CH + '/olean', W + '/out/olean']
OUT_PINS = {  # AUDIT.md section 10, fresh oleans
    'LemmaZ': 'ef249ba167372ac31f995027299efa1eeddac251ff73e4ef093a990ab02c353c',
    'BalancedBudgetsZ': '38d8f8aed92e5e2fefbd86bf46607f920eea28dc5b757a5a30e26734b0cbe71a',
    'FixedStatesZ': 'fdd1900d9118cab5b013f1957178c160fe938bdc6873000a62755ca33c6e390c',
    'LemmaZStar': '1a741fa05068b4c1f0e09465fe218df793d3e30bbb27e2b99a7ca9a32b555102',
    'BalancedBudgetsZZs': 'c53030beac0b3238982b3b15fd4e11d5f0fa7e8486a870adb848d58e52f01791',
    'BalancedBudgetsZZsN': 'b11c8bd8a0cd19b87e04b8e815bab75402116a77b9acf1bfb5d3eca7d55e4fef',
    'Composition305': '94e5257e170ec2cde931402abfe2d618793834218df044d126398a4ad8f7b2f8',
    'Composition304': '88029bb32ed86adf5801b7a06e3bf4626ac59c5a4008569af11224d81606f6ce',
    'Composition303': 'ae3961f3c767ae83744b9ee3dd9a144f3556a3b658e5bdd3eb825fe155017c20',
    'Composition306': '1cc3daf27a8c670dfdb0bdcfd45623ab90eee5ae24b4ea085226e2e2934fd1e3'}


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def closure_rows():
    with open(W + '/closure.tsv') as f:
        rows = list(csv.reader(f, delimiter='\t'))
    assert rows[0][:3] == ['module', 'root', 'olean_sha256'], rows[0]
    return rows[1:]


def pre():
    lib = json.load(open(CH + '/library.json'))
    lroots = [r.replace('<repo>', REPO).replace('<home>', os.path.expanduser('~')) for r in lib['roots']]
    assert lroots == ROOTS[:11], 'library.json roots differ from lake-lean-path.txt'
    libpin = {m: (lroots[i], h) for m, (i, h) in lib['modules'].items()}
    chainpin = {}
    with open(CH + '/build.tsv') as f:
        for row in csv.DictReader(f, delimiter='\t'):
            if row['verdict'] == 'ok':
                chainpin[row['module']] = row['olean_sha256']  # last ok row wins
    bad, by_root, comp, n = [], {}, hashlib.sha256(), 0
    for m, root, h, *_ in closure_rows():
        rel = m.replace('.', '/')
        prov = [r for r in ROOTS if os.path.isfile(f'{r}/{rel}.olean')]
        got = sha(f'{prov[0]}/{rel}.olean') if len(prov) == 1 else None
        if root == ROOTS[-2]:
            pin = chainpin.get(m)
        elif root == ROOTS[-1]:
            pin = OUT_PINS.get(m)
        else:
            pin = libpin.get(m, (None, None))
            pin = pin[1] if pin[0] == root else None
        if prov != [root] or got != h or pin != h:
            bad.append({'module': m, 'providers': prov, 'tsv_root': root, 'sha': got, 'tsv_sha': h, 'pin': pin})
        by_root[root] = by_root.get(root, 0) + 1
        n += 1
        for ext in ('.olean.server', '.olean.private'):
            p = f'{prov[0]}/{rel}{ext}' if prov else None
            if p and os.path.isfile(p):
                comp.update(f'{m}{ext}\t{sha(p)}\n'.encode())
    res = {'modules': n, 'bad': bad, 'by_root': by_root, 'companions_digest': comp.hexdigest(),
           'lean_path': ':'.join(ROOTS)}
    json.dump(res, open(R + '/closure_pre.json', 'w'), indent=1)
    print(json.dumps({k: (v if k != 'bad' else v[:5]) for k, v in res.items() if k != 'lean_path'}))
    return 0 if not bad and n == 4980 else 1


def post():
    mods = [l[len('module '):].strip() for l in open(R + '/review.log', errors='replace') if l.startswith('module ')]
    tsv = [r[0] for r in closure_rows()]
    res = {'review_modules': len(mods), 'closure_tsv_modules': len(tsv), 'same_list_same_order': mods == tsv,
           'only_in_review': sorted(set(mods) - set(tsv))[:20], 'only_in_tsv': sorted(set(tsv) - set(mods))[:20]}
    json.dump(res, open(R + '/closure_post.json', 'w'), indent=1)
    print(json.dumps(res))
    return 0 if mods == tsv else 1


if __name__ == '__main__':
    sys.exit(pre() if sys.argv[1] == 'pre' else post())
