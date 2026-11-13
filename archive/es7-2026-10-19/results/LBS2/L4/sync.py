#!/usr/bin/env python3
"""Copy the lines of live/*.jsonl and live/*sets*.txt that are not yet under data/ into new
gzipped chunk files data/<name>.partNNN.gz (append-only, so git never rewrites a big file).
Also copies any live/ALERT_* and live/STOP."""
import glob, gzip, os, re, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
data = os.path.join(HERE, "data"); os.makedirs(data, exist_ok=True)
for f in sorted(glob.glob(os.path.join(HERE, "live", "e*.jsonl")) + glob.glob(os.path.join(HERE, "live", "e*_sets_*.txt"))):
    name = os.path.basename(f)
    parts = sorted(glob.glob(os.path.join(data, name + ".part*.gz")))
    done = sum(sum(1 for _ in gzip.open(p, "rt")) for p in parts)
    lines = open(f).readlines()
    lines = [l for l in lines if l.endswith("\n")]
    if len(lines) > done:
        with gzip.open(os.path.join(data, f"{name}.part{len(parts):03d}.gz"), "wt") as g:
            g.writelines(lines[done:])
for f in glob.glob(os.path.join(HERE, "live", "ALERT_*")) + glob.glob(os.path.join(HERE, "live", "STOP")):
    shutil.copy(f, data)
