#!/usr/bin/env python3
"""Collect generated models, verify each by brute force (brute: signotope axioms, max cap, max cup,
largest convex subset), drop duplicates (exact bit-string), and append new verified models to
QUEUE (lines 'id mode bits'), interleaving the two phase modes.  Keeps a seen-hash file.
usage: prep_queue.py GENDIR BRUTE QUEUE SEEN"""
import glob, hashlib, os, subprocess, sys
gendir, brute, queue, seenf = sys.argv[1:5]
seen = set(open(seenf).read().split()) if os.path.exists(seenf) else set()
stats = {"read": 0, "dup": 0, "bad": 0, "new": 0}
new = {"0": [], "1": []}
for f in sorted(glob.glob(os.path.join(gendir, "*.txt"))):
    mode = "0" if os.path.basename(f).startswith(("m0", "b0")) else "1"
    lines = [l.strip() for l in open(f) if len(l.strip()) == 2600]
    if not lines: continue
    out = subprocess.run([brute, "26", "7"], input="\n".join(lines) + "\n", capture_output=True, text=True).stdout.split("\n")
    for l, o in zip(lines, out):
        stats["read"] += 1
        h = hashlib.sha1(l.encode()).hexdigest()[:20]
        if h in seen: stats["dup"] += 1; continue
        _, ax, cap, cup, lcs = map(int, o.split())
        if not (ax == 0 and cap <= 4 and cup <= 6 and lcs <= 6):
            stats["bad"] += 1; continue
        seen.add(h); new[mode].append((h, l))
with open(queue, "a") as q:
    a, b = new["0"], new["1"]
    for i in range(max(len(a), len(b))):
        for m, L in (("0", a), ("1", b)):
            if i < len(L): q.write(f"{L[i][0]} {m} {L[i][1]}\n"); stats["new"] += 1
with open(seenf, "w") as g: g.write("\n".join(sorted(seen)) + "\n")
print(stats, "total distinct verified:", len(seen))
