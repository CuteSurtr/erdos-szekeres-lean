"""C3AUDIT4: for every fuzz case file that fuzz.py saved (any disagreement among its composers), re-run two composers
and compare verdict, open depth-1/depth-2 nodes, and the frontier with sigma-split nodes set aside (C3U-family
compose lists a sigma-split node whose route failed; C3AUDIT3 mycompose lists only its missing descendants).
usage: fuzz_pair.py A B CASEFILES...   (file names case_m{m}k{k}_...)"""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
A, B = sys.argv[1], sys.argv[2]
BD = "/tmp/claude-0/-home-user-erdos-szekeres-lean/a2372e58-e319-59b7-94d3-805904fed989/scratchpad/base"
st = {"files": 0, "verdict_diff": [], "open_d2_diff": [], "frontier_diff_beyond_split_nodes": [], "frontier_only_split_nodes": 0}
for f in sys.argv[3:]:
    m, k = re.search(r"case_m(\d+)k(\d+)_", os.path.basename(f)).groups()
    extra = ["--mirror-h6"] if "_h6m" in f or os.environ.get("FUZZ_H6M") == "1" else []
    res = []
    for w in (A, B):
        x = subprocess.run([sys.executable, os.path.join(HERE, "runcomp.py"), w, m, k, f"{BD}/b{m}{k}.cnf", f] + extra, capture_output=True, text=True)
        res.append(json.loads(x.stdout.strip().splitlines()[-1]))
    sp = set()
    for l in open(f):
        r = json.loads(l)
        if r.get("split") and "node" in r and "cube" not in r: sp.add(r["node"])
    st["files"] += 1
    a, b = res
    va = "reject" if a.get("reject") else a["covered"]; vb = "reject" if b.get("reject") else b["covered"]
    if va != vb: st["verdict_diff"].append(os.path.basename(f)); continue
    if va == "reject": continue
    if a["open_d2"] != b["open_d2"] or a["open_d1"] != b["open_d1"]: st["open_d2_diff"].append(os.path.basename(f))
    fa, fb = set(a["frontier"]), set(b["frontier"])
    d = (fa ^ fb)
    if d - sp: st["frontier_diff_beyond_split_nodes"].append((os.path.basename(f), sorted(d - sp)[:3]))
    elif d: st["frontier_only_split_nodes"] += 1
print(json.dumps(st))
