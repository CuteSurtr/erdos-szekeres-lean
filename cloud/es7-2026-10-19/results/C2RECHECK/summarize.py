#!/usr/bin/env python3
"""Summarize the re-checks of 1-2 November 2026 from their raw JSON-lines outputs.

usage: summarize.py [OUT.json]
Reads the inputs from the directory of this script, or from the directory in the environment variable RECHECK_DIR:
hexcheck.jsonl, sample_main.jsonl, sample_q3.jsonl, sample_extra.jsonl, pilot_orbits.jsonl, local.jsonl,
lanespot.jsonl, and the unit lists local_units_1.txt, local_units_2.txt, lanespot_units.txt (planned counts).
The sections for c3pieces.jsonl and replay_select.jsonl are written only when those files are present.
OUT defaults to summary.json in the same directory."""
import json, os, sys


def load(p):
    if not os.path.exists(p):
        return []
    return [json.loads(l) for l in open(p) if l.strip()]


def count_lines(paths, default):
    paths = [p for p in paths if os.path.exists(p)]
    return sum(1 for p in paths for l in open(p) if l.strip()) if paths else default


def tally(rs, cert_key="certified"):
    return {
        "units": len(rs),
        "cnf_hash_matches": sum(bool(r.get("cnf_matches_record")) for r in rs),
        "unsat": sum(r.get("status") == "UNSATISFIABLE" for r in rs),
        "certified_both_checkers": sum(bool(r.get(cert_key)) for r in rs),
        "proof_identical_to_record": sum(bool(r.get("proof_reproduces_record")) for r in rs),
        "archive_roundtrip_verified": sum(r.get("roundtrip") == "verified" for r in rs),
        "not_identical": [r["unit"] for r in rs if r.get("status") == "UNSATISFIABLE" and not r.get("proof_reproduces_record")],
        "not_certified": [r.get("unit") for r in rs if not r.get(cert_key)],
    }


D = os.environ.get("RECHECK_DIR") or os.path.dirname(os.path.abspath(__file__))
P = lambda n: os.path.join(D, n)
OUT = sys.argv[1] if len(sys.argv) > 1 else P("summary.json")
out = {}
hx = load(P("hexcheck.jsonl"))
out["hexagonal_hull_cake_recheck"] = {
    "cases": len(hx), "distinct": len({r["case"] for r in hx}),
    "cnf_archive_proof_hashes_match": sum(bool(r["cnf_matches_record"] and r["archive_matches_record"]
                                               and r["proof_matches_record"]) for r in hx),
    "lrat_check_verified": sum(r.get("lrat_check") == "c VERIFIED" for r in hx),
    "cake_lpr_verified": sum(r.get("cake_lpr") == "s VERIFIED UNSAT" for r in hx),
    "certified_both_checkers": sum(r.get("lrat_check") == "c VERIFIED" and r.get("cake_lpr") == "s VERIFIED UNSAT"
                                   for r in hx),
}
out["random_sample_main"] = tally(load(P("sample_main.jsonl")) + load(P("sample_q3.jsonl")))
out["random_sample_extra"] = tally(load(P("sample_extra.jsonl")))
out["p8_pilot_orbits"] = tally(load(P("pilot_orbits.jsonl")))
out["local_only_orbits_and_covers"] = tally(load(P("local.jsonl")))
out["local_only_orbits_and_covers"]["planned"] = count_lines([P("local_units_1.txt"), P("local_units_2.txt")], 65)
ls = load(P("lanespot.jsonl"))
out["lane_spot_check"] = tally(ls)
out["lane_spot_check"]["planned"] = count_lines([P("lanespot_units.txt")], 242)
out["lane_spot_check"]["distinct_lanes"] = len({r.get("record_source") for r in ls})
if os.path.exists(P("c3pieces.jsonl")):
    c3 = load(P("c3pieces.jsonl"))
    out["threefold_indispensable_pieces"] = {
        "records": len(c3), "distinct": len({r.get("piece") or r.get("unit") or r.get("node") for r in c3}),
        "certified": sum(bool(r.get("certified")) for r in c3),
        "cnf_hash_matches": sum(bool(r.get("cnf_matches_record", r.get("cnf_sha256_matches"))) for r in c3),
        "proof_size_equals_record": sum(bool(r.get("proof_bytes_match_record")) for r in c3),
        "records_with_proof_hash": sum(r.get("proof_sha256_match_record") is not None for r in c3),
        "archive_roundtrip_verified": sum(r.get("roundtrip") in ("verified", True, "ok") or r.get("roundtrip_sha256") == r.get("proof_sha256") for r in c3),
    }
if os.path.exists(P("replay_select.jsonl")):
    rp = [r for r in load(P("replay_select.jsonl")) if "id" in r]
    out["replay_selected"] = {r["id"]: r.get("status") for r in rp}
open(OUT, "w").write(json.dumps(out, indent=1) + "\n")
print(json.dumps(out, indent=1))
