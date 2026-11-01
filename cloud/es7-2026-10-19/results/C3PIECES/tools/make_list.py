#!/usr/bin/env python3
"""Write the unit list for c3resolve.py from the set of necessary pieces found by indispensable.py.

Inputs: NECESSARY (one piece per line, from indispensable.py), optionally A2's list for comparison.
For every piece: its records in the 280 C3FINAL record files (found with c3resolve.Repo, i.e. exactly as the
runner finds them), the certified reference record, and checks of the assumptions the runner relies on (one
certified record or several with the same cnf_sha256; cadical_opts present; cube bits recorded in ascending
residue order, so that the campaign's unit order equals compose.py's).  Order of the list: recorded solve time,
longest first (so N lanes sharing the list finish close together).
Writes OUTDIR/units.txt (one piece per line), OUTDIR/units.tsv, OUTDIR/units_check.json.
usage: python3 -I -B make_list.py NECESSARY OUTDIR [A2_LIST]"""
import importlib.util
import json
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("c3resolve", os.path.join(HERE, "c3resolve.py"))
c3r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c3r)

NEC, OUT = sys.argv[1:3]
A2 = sys.argv[3] if len(sys.argv) > 3 else None
pieces = [l.strip() for l in open(NEC) if l.strip()]
repo = c3r.Repo(c3r.DEF_RESULTS, os.path.join(OUT, "pycache_prefix_unused"))
recs = repo.records(set(pieces))
rows, issues = [], []
for p in pieces:
    ref, why = c3r.pick_record(recs[p])
    if ref is None:
        issues.append((p, why))
        continue
    r = ref["rec"]
    order = [int(b) for b in r["cube"]]
    rows.append({
        "piece": p, "src": ref["file"].split("/")[0], "record_file": ref["file"], "record_line": ref["line"],
        "parent": r["node"], "cube_bits_recorded_order": order, "ascending": order == sorted(order),
        "bits": len(order), "units": r.get("units"), "cnf_sha256": r.get("cnf_sha256"),
        "proof_sha256": r.get("proof_sha256"), "proof_bytes": r.get("proof_bytes"), "solve_s": r.get("solve_s"),
        "check_s": r.get("check_s"), "cap": r.get("cap"), "cadical_opts": r.get("cadical_opts"),
        "n_records": len(recs[p]), "n_certified": sum(e["certified"] for e in recs[p]),
        "other_statuses": sorted(e["rec"].get("status", "?") for e in recs[p] if e is not ref),
        "sigma_format": "cube" in r})
rows.sort(key=lambda x: (-(x["solve_s"] or 0), x["piece"]))
os.makedirs(OUT, exist_ok=True)
with open(os.path.join(OUT, "units.txt"), "w") as f:
    f.write("".join(x["piece"] + "\n" for x in rows))
cols = ["piece", "src", "record_file", "record_line", "parent", "cube_bits_recorded_order", "units", "cnf_sha256",
        "proof_bytes", "proof_sha256", "solve_s", "check_s", "cap", "cadical_opts", "n_records", "n_certified", "other_statuses"]
with open(os.path.join(OUT, "units.tsv"), "w") as f:
    f.write("idx\t" + "\t".join(cols) + "\n")
    for i, x in enumerate(rows):
        f.write(f"{i}\t" + "\t".join(json.dumps(x[c]) if isinstance(x[c], (list, dict)) or x[c] is None else str(x[c])
                                     for c in cols) + "\n")
chk = {
    "pieces": len(pieces), "rows": len(rows), "issues": issues,
    "all_sigma_format": all(x["sigma_format"] for x in rows),
    "all_cube_bits_ascending": all(x["ascending"] for x in rows),
    "cadical_opts": sorted({json.dumps(x["cadical_opts"]) for x in rows}),
    "caps": sorted({x["cap"] for x in rows}),
    "with_proof_sha256": sum(1 for x in rows if x["proof_sha256"]),
    "with_proof_bytes": sum(1 for x in rows if x["proof_bytes"]),
    "n_certified_hist": {str(k): sum(1 for x in rows if x["n_certified"] == k) for k in sorted({x["n_certified"] for x in rows})},
    "n_records_hist": {str(k): sum(1 for x in rows if x["n_records"] == k) for k in sorted({x["n_records"] for x in rows})},
    "by_src_and_bits": {f"{s}/{b}": sum(1 for x in rows if x["src"] == s and x["bits"] == b)
                        for s, b in sorted({(x["src"], x["bits"]) for x in rows})},
    "by_record_file": {f: sum(1 for x in rows if x["record_file"] == f) for f in sorted({x["record_file"] for x in rows})},
    "parents": len({x["parent"] for x in rows}),
    "recorded_solve_h": round(sum(x["solve_s"] or 0 for x in rows) / 3600, 2),
    "recorded_check_h": round(sum(x["check_s"] or 0 for x in rows) / 3600, 2),
    "recorded_solve_s_min_median_max": [min(x["solve_s"] for x in rows), sorted(x["solve_s"] for x in rows)[len(rows) // 2],
                                        max(x["solve_s"] for x in rows)],
    "recorded_proof_bytes_min_median_max_sum": [min(x["proof_bytes"] for x in rows),
                                                sorted(x["proof_bytes"] for x in rows)[len(rows) // 2],
                                                max(x["proof_bytes"] for x in rows), sum(x["proof_bytes"] for x in rows)],
    "units_txt_sha256": c3r.sha_file(os.path.join(OUT, "units.txt")),
}
if A2:
    a2 = {l.strip() for l in open(A2) if l.strip()}
    chk["equals_A2_list"] = a2 == set(pieces)
    chk["A2_minus_ours"], chk["ours_minus_A2"] = sorted(a2 - set(pieces)), sorted(set(pieces) - a2)
json.dump(chk, open(os.path.join(OUT, "units_check.json"), "w"), indent=1)
print(json.dumps(chk, indent=1))
