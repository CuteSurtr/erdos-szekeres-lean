#!/usr/bin/env python3
"""Run tools/trackB/brute_kgon (unchanged, compiled) on every signotope in a compact .sig file.

usage: brute_all.py BRUTE_BIN SIGFILE K TMPDIR OUT.jsonl [workers]

SIGFILE lines: `id tag label hash n signs` (convert.py) or `id ... n signs` with n and signs the
last two fields. Each signotope is written to a temporary `i j k s` file, checked by brute_kgon
(all K-subsets, 4-point test, plus the signotope axiom on every quadruple), and deleted.
Writes one JSON line per set: {id, n, violations, convex}.
"""
import itertools
import json
import os
import re
import subprocess
import sys
from multiprocessing import Pool

BIN = K = TMP = None


def init(b, k, t):
    global BIN, K, TMP
    BIN, K, TMP = b, k, t


def check(line):
    t = line.split()
    sid, n, signs = t[0], int(t[-2]), t[-1]
    path = os.path.join(TMP, f"chk_{os.getpid()}_{sid}.sig")
    with open(path, "w") as f:
        for (i, j, k), c in zip(itertools.combinations(range(1, n + 1), 3), signs):
            f.write(f"{i} {j} {k} {1 if c == '+' else -1}\n")
    out = subprocess.run([BIN, str(n), str(K), path], capture_output=True, text=True)
    os.remove(path)
    m = re.search(r"signotope_violations=(\d+) K-subsets=(\d+) convex_K_subsets=(\d+)", out.stdout)
    if out.returncode != 0 or not m:
        return {"id": sid, "n": n, "error": out.stderr.strip() or out.stdout[-200:]}
    return {"id": sid, "n": n, "violations": int(m.group(1)), "subsets": int(m.group(2)),
            "convex": int(m.group(3))}


def main():
    b, sigfile, k, tmp, out = sys.argv[1:6]
    workers = int(sys.argv[6]) if len(sys.argv) > 6 else os.cpu_count()
    lines = [l for l in open(sigfile) if l.strip()]
    bad = 0
    with Pool(workers, initializer=init, initargs=(os.path.abspath(b), int(k), tmp)) as pool, open(out, "w") as fo:
        for r in pool.imap(check, lines, chunksize=8):
            fo.write(json.dumps(r) + "\n")
            if "error" in r or r["violations"] or r["convex"]:
                bad += 1
    print(json.dumps({"checked": len(lines), "K": int(k), "flagged": bad}))


if __name__ == "__main__":
    main()
