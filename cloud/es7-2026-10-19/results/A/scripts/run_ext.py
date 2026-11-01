#!/usr/bin/env python3
"""Process-pool driver for ext_solve.

usage: run_ext.py EXT_SOLVE BASE.cnf M CONFLICT_LIMIT SIGFILE OUTDIR [workers] [option=value ...]
  One-point abstract extension of every signotope in SIGFILE (lines ending `n signs`, first field
  = set id): jobs P 1 .. P M with M = n+1.

As a library: run_pool(exe, cnf, M, climit, blocks, outdir, workers), where every block is a
self-contained job text (an S line followed by P/J lines). Blocks are dealt round-robin to the
workers; each worker is one ext_solve process that loads the base CNF once. Raw outputs go to
OUTDIR/w<k>.out (R and W lines) and OUTDIR/w<k>.err.
"""
import os
import subprocess
import sys
import time


def run_pool(exe, cnf, M, climit, blocks, outdir, workers, opts=()):
    os.makedirs(outdir, exist_ok=True)
    workers = max(1, min(workers, len(blocks)))
    jobs = [[] for _ in range(workers)]
    for idx, b in enumerate(blocks):
        jobs[idx % workers].append(b)
    t0 = time.time()
    procs = []
    for w in range(workers):
        jf = os.path.join(outdir, f"w{w}.jobs")
        with open(jf, "w") as f:
            f.writelines(jobs[w])
        fo = open(os.path.join(outdir, f"w{w}.out"), "w")
        fe = open(os.path.join(outdir, f"w{w}.err"), "w")
        procs.append(subprocess.Popen([exe, cnf, str(M), str(climit)] + list(opts), stdin=open(jf), stdout=fo,
                                      stderr=fe))
    codes = [p.wait() for p in procs]
    return {"workers": workers, "blocks": len(blocks), "exit_codes": sorted(set(codes)), "solver_options": list(opts),
            "wall_s": round(time.time() - t0, 1)}


def ext_blocks(sigfile, M):
    blocks = []
    for l in open(sigfile):
        t = l.split()
        if not t:
            continue
        sid, n, signs = t[0], int(t[-2]), t[-1]
        assert n + 1 == M
        blocks.append("".join([f"S {sid} {n} {signs}\n"] + [f"P {p}\n" for p in range(1, M + 1)]))
    return blocks


def main():
    exe, cnf, M, climit, sigfile, outdir = sys.argv[1:7]
    workers = int(sys.argv[7]) if len(sys.argv) > 7 else os.cpu_count()
    opts = sys.argv[8:]  # CaDiCaL options, e.g. lucky=0
    M = int(M)
    print(run_pool(exe, cnf, M, climit, ext_blocks(sigfile, M), outdir, workers, opts))


if __name__ == "__main__":
    main()
