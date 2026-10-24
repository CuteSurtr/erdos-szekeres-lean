"""summarize run_m11.sh output: usage m11_table.py OUTDIR FILELIST COMMIT SNAPDIR"""
import json, sys
d, fl, commit, snap = sys.argv[1:5]
files = open(fl).read().split()
sp = {}
for f in files:
    for l in open(f"{snap}/{f}"):
        r = json.loads(l)
        if r.get("split") and "node" in r and "cube" not in r:
            sp.setdefault(r["node"], set()).add("sigma" if "sigma_bits" in r else "layer")
R = {n: json.load(open(f"{d}/{n}.json")) for n in ["C3U2", "mine", "C3U2--mirror-h6", "mine--mirror-h6"]}
print(json.dumps({"commit": commit, "files": len(files)}))
for n, j in R.items():
    s = j["summary"]
    print(json.dumps({"composer": n, "covered": j["covered"], "frontier": len(j["frontier"]), "open_depth2": len(j["open_d2"]),
                      "certified_records": s.get("certified_records"), "certified_nodes": s.get("certified_nodes"),
                      "certified_cube_nodes": s.get("certified_cube_nodes"), "sigma_splits_used": s.get("sigma_splits_used"),
                      "sha_checked": s.get("sha_checked")}))
for h in ["", "--mirror-h6"]:
    a, b = R["mine" + h], R["C3U2" + h]
    fa, fb = set(a["frontier"]), set(b["frontier"])
    extra = sorted(fb - fa)
    print(json.dumps({"mirror_h6": bool(h), "covered_equal": a["covered"] == b["covered"],
                      "open_depth2_equal": a["open_d2"] == b["open_d2"], "frontier_only_mine": sorted(fa - fb),
                      "frontier_only_C3U2": len(extra),
                      "only_C3U2_kinds": sorted({"/".join(sorted(sp.get(x, {"none"}))) for x in extra}),
                      "only_C3U2_sample": extra[:5]}))
    print(json.dumps({"mirror_h6": bool(h), "open_depth2": a["open_d2"]}))
