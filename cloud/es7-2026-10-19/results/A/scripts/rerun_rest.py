#!/usr/bin/env python3
"""Re-deal the unanswered jobs of an interrupted ext_solve pool over fresh workers.

usage: rerun_rest.py WORKDIR NBDIR OUTDIR CONFLICT_LIMIT [workers]
Reads NBDIR/w*.jobs and NBDIR/w*.out; every (label, tag) job without an R line is re-run, one
block per S label, with the same base CNF and options (lucky=0). Results go to OUTDIR.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sigutil import parse_outputs  # noqa: E402
from run_ext import run_pool  # noqa: E402


def main():
    wd, nbdir, outdir, climit = sys.argv[1:5]
    workers = int(sys.argv[5]) if len(sys.argv) > 5 else 15
    done = {(r[1], r[2]) for r in parse_outputs(nbdir) if r[0] == 'R'}
    blocks = []
    for fn in sorted(os.listdir(nbdir)):
        if not fn.endswith('.jobs'):
            continue
        cur, pend = None, []
        for line in open(os.path.join(nbdir, fn)):
            t = line.split()
            if t[0] == 'S':
                if cur and pend:
                    blocks.append(cur + ''.join(pend))
                cur, lab, pend = line, t[1], []
            elif t[0] == 'J' and (lab, t[1]) not in done:
                pend.append(line)
        if cur and pend:
            blocks.append(cur + ''.join(pend))
    n = sum(b.count('\nJ ') for b in blocks)
    # spread single heavy blocks: split each block into per-job blocks so all workers share them
    fine = []
    for b in blocks:
        lines = b.splitlines(keepends=True)
        for j in lines[1:]:
            fine.append(lines[0] + j)
    print({"pending_jobs": n, "blocks": len(fine)})
    print(run_pool(os.path.join(wd, 'ext_solve'), os.path.join(wd, 'n33k7.cnf'), 33, climit, fine, outdir,
                   workers, opts=['lucky=0']))


if __name__ == '__main__':
    main()
