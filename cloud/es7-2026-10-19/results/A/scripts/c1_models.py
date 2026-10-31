#!/usr/bin/env python3
"""Realizer calibration input: the SAT models of control C1 (31-point pool subsets extended to 32
points). usage: c1_models.py WORKDIR OUT.jsonl
Old points = the pool set's x-sorted points without point q; new = [p]."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sigutil import parse_outputs, parse_tag_new  # noqa: E402


def main():
    wd, out = sys.argv[1:3]
    pts = {}
    for l in open(os.path.join(wd, 'pool.pts')):
        t = l.split()
        v = list(map(int, t[2:]))
        pts[t[0]] = [(v[2 * a], v[2 * a + 1]) for a in range(int(t[1]))]
    n = 0
    with open(out, 'w') as f:
        for rec in parse_outputs(os.path.join(wd, 'ctl_c1')):
            if rec[0] != 'W':
                continue
            lab, tag, model = rec[1], rec[2], rec[3]
            _, sid, q = lab.split('_')
            q = int(q[1:])
            old = [p for a, p in enumerate(pts[sid], 1) if a != q]
            f.write(json.dumps({"label": lab, "tag": tag, "M": 32, "model": model, "old_pts": old,
                                "new": parse_tag_new(tag), "own_position": parse_tag_new(tag) == [q]}) + "\n")
            n += 1
    # guaranteed-realizable calibration: the original 32-point signotope, point q treated as new
    sig = {}
    for l in open(os.path.join(wd, 'pool.sig')):
        t = l.split()
        sig[t[0]] = t[-1]
    labs = sorted({rec[1] for rec in parse_outputs(os.path.join(wd, 'ctl_c1')) if rec[0] == 'R'})
    with open(out.replace('.jsonl', '_orig.jsonl'), 'w') as f:
        for lab in labs:
            _, sid, q = lab.split('_')
            q = int(q[1:])
            old = [p for a, p in enumerate(pts[sid], 1) if a != q]
            f.write(json.dumps({"label": lab + "_orig", "tag": f"p{q}", "M": 32, "model": sig[sid],
                                "old_pts": old, "new": [q]}) + "\n")
    print(n, len(labs))


if __name__ == '__main__':
    main()
