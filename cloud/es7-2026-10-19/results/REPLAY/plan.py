#!/usr/bin/env python3
"""Per-entry resource plan for a full replay, from manifest.json (recorded values only).

Columns: id, group, default, proof GB (disk), cake_lpr heap ladder (MiB), cake footprint GB for the first and the
largest heap (heap*1.048576 + 0.4), recorded cake_lpr max RSS GB (archived log, where one exists), recorded
lrat-check footprint GB, recorded lrat-check s, recorded cake_lpr s, estimated wall s for one replay
(decompress at ~1.2 GB/s + CNF ~3 s + lrat-check + cake_lpr; recorded times, or 25 s/GB lrat and 45 s/GB cake when
unrecorded). Group totals are printed at the end.
usage: plan.py MANIFEST OUT_TSV
"""
import json, sys
from collections import defaultdict

man = json.load(open(sys.argv[1]))
MIB_GB = 1048576 / 1e9
rows, tot = [], defaultdict(lambda: [0, 0.0, 0.0, 0.0])
for e in man["entries"]:
    rec, lad = e["recorded"], e["heap_ladder_mb"]
    gb = e["proof"]["bytes"] / 1e9
    cl, ll = rec.get("cake_lpr_log") or {}, rec.get("lrat_check_log") or {}
    lrat_s = rec.get("lrat_check_s") or ll.get("wall_s") or round(25 * gb, 1)
    cake_s = rec.get("cake_s") or cl.get("wall_s") or round(45 * gb, 1)
    est = round(gb / 1.2 + 3 + lrat_s + cake_s)
    r = {"id": e["id"], "group": e["group"], "default": e["default"], "proof_gb": round(gb, 2),
         "heap_ladder_mb": ",".join(map(str, lad)), "cake_gb_first": round(lad[0] * MIB_GB + 0.4, 1),
         "cake_gb_max": round(max(lad) * MIB_GB + 0.4, 1),
         "rec_cake_rss_gb": round(cl["max_rss_bytes"] / 1e9, 1) if cl.get("max_rss_bytes") else "",
         "rec_lrat_gb": round(ll["peak_footprint_bytes"] / 1e9, 2) if ll.get("peak_footprint_bytes") else "",
         "rec_lrat_s": lrat_s, "rec_cake_s": cake_s, "est_wall_s": est}
    rows.append(r)
    t = tot[e["group"]]; t[0] += 1; t[1] += gb; t[2] += est; t[3] = max(t[3], r["cake_gb_first"])
cols = list(rows[0])
with open(sys.argv[2], "w") as g:
    g.write("\t".join(cols) + "\n")
    for r in rows:
        g.write("\t".join(str(r[c]) for c in cols) + "\n")
print(f"{'group':26} {'n':>4} {'proof GB':>9} {'est h':>6} {'max cake GB (first heap)':>25}")
for k, (n, gb, s, mx) in tot.items():
    print(f"{k:26} {n:4d} {gb:9.1f} {s / 3600:6.2f} {mx:25.1f}")
d = [r for r in rows if r["default"]]
print(f"default selection: {len(d)} entries, {sum(r['est_wall_s'] for r in d) / 3600:.2f} h sequential, "
      f"largest footprint {max(r['cake_gb_max'] for r in d):.1f} GB")
