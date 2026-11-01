#!/usr/bin/env python3
"""verify_F2: individual necessity of the sigma_cubes.py-only certified nodes for the project's cover.
For each selected sigma-only node n (from count_pop.json), drop ONLY the certified sigma_cubes.py-format
record(s) of n (every other line of every file is kept byte for byte), run the project's C3U2
compose.py unchanged (--mirror-h6 --no-sha, read-only, python -I -B) on the 280 files, and record
class_covered.  n is 'necessary' when the class is no longer covered without it.
usage: necessity.py RESULTS_DIR BASE COUNT_POP_JSON SOURCES(comma list, e.g. C3SIG2,C3W3S) START END OUT.jsonl"""
import json
import os
import subprocess
import sys
import tempfile

RD, BASE, CP, SRCS, START, END, OUT = sys.argv[1:8]
START, END = int(START), int(END)
srcs = set(SRCS.split(","))
PY = sys.executable
files = [l.strip() for l in open(os.path.join(RD, "C3FINAL", "compose_files.txt")) if l.strip()]
sig_only = set(json.load(open(CP))["sig_only_nodes"])


def cname(r):
    return r["node"] + "__" + "-".join(f"{a}s{b}" for a, b in sorted((int(x), int(v)) for x, v in r["cube"].items()))


# where each sigma-only node's certified sigma-format records sit
loc = {}  # node -> {file: [line indices]}
for f in files:
    if f.split("/")[0] not in srcs:
        continue
    for i, l in enumerate(open(os.path.join(RD, f))):
        if not l.strip():
            continue
        r = json.loads(l)
        if "cube" in r and r.get("certified") is True:
            n = cname(r)
            if n in sig_only:
                loc.setdefault(n, {}).setdefault(f, []).append(i)
nodes = sorted(loc)[START:END]
tmp = tempfile.mkdtemp(dir=os.path.dirname(os.path.abspath(OUT)))
with open(OUT, "a") as fo:
    for n in nodes:
        args = []
        for f in files:
            if f in loc[n]:
                drop = set(loc[n][f])
                p = os.path.join(tmp, f.replace("/", "__"))
                with open(os.path.join(RD, f), "rb") as fi, open(p, "wb") as fw:
                    for i, line in enumerate(fi):
                        if i not in drop:
                            fw.write(line)
                args.append(p)
            else:
                args.append(os.path.join(RD, f))
        cp = subprocess.run([PY, "-I", "-B", os.path.join(RD, "C3U2", "tools", "compose.py"), BASE] + args
                            + ["--mirror-h6", "--no-sha"], capture_output=True, text=True)
        try:
            o = json.loads(cp.stdout.strip().splitlines()[-1])
        except Exception:  # noqa: BLE001
            o = {"error": cp.stdout[-300:] + cp.stderr[-300:]}
        rec = {"node": n, "src": sorted({f.split("/")[0] for f in loc[n]}), "dropped_records": sum(len(v) for v in loc[n].values()),
               "class_covered": o.get("class_covered"), "uncovered_frontier_nodes": o.get("uncovered_frontier_nodes"),
               "certified_nodes": o.get("certified_nodes"), "exit": cp.returncode}
        if "error" in o:
            rec["error"] = o["error"]
        fo.write(json.dumps(rec) + "\n")
        fo.flush()
        for f in loc[n]:
            os.remove(os.path.join(tmp, f.replace("/", "__")))
os.rmdir(tmp)
print("done", len(nodes))
