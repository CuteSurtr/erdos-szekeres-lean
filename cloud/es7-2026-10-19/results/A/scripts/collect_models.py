#!/usr/bin/env python3
"""Verify every SAT model in ext_solve output directories and prepare realization jobs.

usage: collect_models.py WORKDIR OUT.jsonl OUTDIR [OUTDIR ...]

For each W line: rebuild the old signotope (main run: label = set id, all 32 points old;
neighbourhood: label N<id>_<kind>_<D>, old = the set minus D), then check_model (old triples as
assumed, Python signotope axiom check, brute_kgon violations and convex 7-subsets on the 33-point
model). Writes one JSON line per model with the check results and the realization job fields
(old_pts = x-sorted original coordinates of the old points, new = new indices).
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sigutil import parse_outputs, check_model, parse_tag_new, triples  # noqa: E402


def main():
    wd, out = sys.argv[1:3]
    dirs = sys.argv[3:]
    sig, pts = {}, {}
    for fn in ('pool.sig', os.path.join('extra', 'ae.sig')):
        for l in open(os.path.join(wd, fn)):
            t = l.split()
            sig[t[0]] = t[-1]
    for fn in ('pool.pts', os.path.join('extra', 'ae.pts')):
        for l in open(os.path.join(wd, fn)):
            t = l.split()
            v = list(map(int, t[2:]))
            pts[t[0]] = [(v[2 * a], v[2 * a + 1]) for a in range(int(t[1]))]
    T32 = triples(32)
    n = 0
    with open(out, 'w') as f:
        for d in dirs:
            for rec in parse_outputs(d):
                if rec[0] != 'W':
                    continue
                lab, tag, model = rec[1], rec[2], rec[3]
                if lab.startswith('N') and '_' in lab:
                    sid, kind, D = lab[1:].split('_')
                    D = [int(v) for v in D.split('-')]
                else:
                    sid, kind, D = lab, 'one', []
                keep = [a for a in range(1, 33) if a not in D]
                ks = set(keep)
                old = ''.join(c for t, c in zip(T32, sig[sid]) if t[0] in ks and t[1] in ks and t[2] in ks)
                chk = check_model(os.path.join(wd, 'brute_kgon'), 33, model, len(keep), old, tag,
                                  os.path.join(wd, 'tmp'))
                job = {"label": lab, "tag": tag, "set": sid, "kind": kind, "D": D, "M": 33, "model": model,
                       "old_pts": [pts[sid][a - 1] for a in keep], "new": parse_tag_new(tag), "check": chk,
                       "verified": chk["old_triples_agree"] and chk["py_signotope"] and chk["brute_violations"] == 0
                       and chk["brute_convex"] == 0}
                f.write(json.dumps(job) + "\n")
                n += 1
    print(json.dumps({"models": n}))


if __name__ == '__main__':
    main()
