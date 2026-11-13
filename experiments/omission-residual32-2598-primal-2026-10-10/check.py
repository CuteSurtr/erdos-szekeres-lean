#!/usr/bin/env python3
"""Standard-library replay of the frozen catalog and inconclusive search evidence.

This checks identities and integer row counts. It does not execute Lean, trust an
LP objective as a proof, or infer infeasibility from a search timeout.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
BASE_SHA = "f03eebb1d20eae3bd25dbb5024eaacdfdcc5bcd8ed964d190bdfa59c73aeb909"
SOURCE_SHA = "01d4fde13ae0ca43427540a3d529e7e29b875936332af2cc4ef7d423edee469b"
SIXTH = [25, 43, 53, 65, 74, 85, 89, 91, 96, 107, 110, 111, 125]
AXIOMS = {"Classical.choice", "Quot.sound", "propext"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read_json(path):
    return json.loads(path.read_text())


def validate_catalog(base, middle, source, family, bindings):
    """Check row semantics and the exact append order, independently of hashes."""
    require(len(base["constraints"]) == 2469, "base row count")
    require(len(middle["constraints"]) == 2471, "middle row count")
    require(len(source["constraints"]) == 2598, "final row count")
    require(len(source["states"]) == 154, "state count")
    require(base["states"] == middle["states"] == source["states"], "state identity")
    require(middle["constraints"][:2469] == base["constraints"], "base prefix")
    require(source["constraints"][:2471] == middle["constraints"], "middle prefix")
    for row in source["constraints"]:
        support, rhs = row["support"], row["rhs"]
        require(isinstance(support, list), "support type")
        require(all(type(i) is int and 0 <= i < 154 for i in support), "state range")
        require(len(support) == len(set(support)), "support duplicates")
        require(type(rhs) is int and 0 <= rhs <= len(support), "demand range")
    require(source["constraints"][2469] == {"support": SIXTH, "rhs": 1}, "Sixth row")
    require(len(family["rows"]) == len(bindings) == 128, "Fourth count")
    require(len({tuple(r["support"]) for r in family["rows"]}) == 128, "Fourth uniqueness")
    for k, (row, binding) in enumerate(zip(family["rows"], bindings)):
        require(row["row"] == k, "Fourth local order")
        require(len(row["mapping"]) == len(set(row["mapping"])) == 13, "Fourth injection")
        require(sorted(row["mapping"]) == row["support"], "Fourth mapping image")
        require(row["rhs"] == 1, "Fourth demand")
        require(source["constraints"][2470 + k] == {"support": row["support"], "rhs": 1}, "Fourth source order")
        require(binding == {"family_row": k, "source_row": 2470 + k,
                            "support": row["support"], "rhs": 1,
                            "ordered_mapping": row["mapping"]}, "Fourth manifest mapping")
    require(source["research_fourth_family_binding"] == bindings, "embedded family binding")


def replay_candidate(rows, candidate):
    holes = candidate["holes"]
    require(isinstance(holes, list) and all(type(i) is int for i in holes), "hole type")
    require(holes == sorted(set(holes)) and len(holes) == 32, "32 distinct holes")
    require(all(0 <= i < 154 for i in holes), "hole range")
    require(0 not in holes and 43 not in holes, "occupied anchor states")
    hs = set(holes)
    bits = sum(1 << i for i in holes)
    violations = []
    for i, row in enumerate(rows):
        count = sum(j in hs for j in row["support"])
        # Independent representation: integer bit masks, no solver or tolerance.
        bit_count = (bits & sum(1 << j for j in row["support"])).bit_count()
        require(count == bit_count, "set/bitset disagreement")
        if count < row["rhs"]:
            violations.append({"row": i, "count": count, "rhs": row["rhs"],
                               "deficit": row["rhs"] - count})
    require(violations == candidate["expected_violations"], "candidate violations")
    require(all(v["row"] >= candidate["valid_for_prefix_rows"] for v in violations), "prefix witness")
    return violations


def replay_two_exchange(rows, record):
    """Replay the recorded local neighborhood, keeping states 0 and 43 occupied.

    A repair must add a hole in the first violated row. After adding it and
    removing two old holes, all remaining deficient rows constrain the second
    addition by intersection. This exhausts exactly two removals/additions.
    It says nothing about longer paths or other initial assignments.
    """
    holes = record["parent_candidate"]
    bits = sum(1 << i for i in holes)
    masks = [sum(1 << i for i in r["support"]) for r in rows]
    violations = [i for i, (r, m) in enumerate(zip(rows, masks))
                  if (bits & m).bit_count() < r["rhs"]]
    require(violations == record["parent_violated_rows"], "local-repair parent")
    trials = 0
    for added in rows[violations[0]]["support"]:
        if added in holes or added in (0, 43):
            continue
        for first, second in itertools.combinations(holes, 2):
            partial = (bits ^ (1 << first) ^ (1 << second)) | (1 << added)
            available = ((1 << 154) - 1) & ~bits & ~(1 << added) & ~1 & ~(1 << 43)
            trials += 1
            for row, mask in zip(rows, masks):
                deficit = row["rhs"] - (partial & mask).bit_count()
                if deficit > 1:
                    available = 0
                    break
                if deficit == 1:
                    available &= mask
                    if not available:
                        break
            require(available == 0, "unexpected local repair")
    require(trials == record["two_exchange_trials"], "local-repair trial count")
    require(record["witness_found"] is False and record["holes"] is None, "local-repair claim")
    return trials


def check(directory=HERE, repo=ROOT):
    manifest = read_json(directory / "manifest.json")
    for name, expected in manifest["files"].items():
        require(digest((directory / name).read_bytes()) == expected, "file identity: " + name)
    for name, expected in manifest["external_inputs"].items():
        require(digest((repo / name).read_bytes()) == expected, "external identity: " + name)
    base_raw = gzip.decompress((repo / "experiments/omission-residual32-research-2026-10-10/source.json.gz").read_bytes())
    require(digest(base_raw) == BASE_SHA == manifest["base_source_uncompressed_sha256"], "base source hash")
    base = json.loads(base_raw)
    sources = {}
    for name, expected in manifest["source_uncompressed_sha256"].items():
        raw = gzip.decompress((directory / name).read_bytes())
        require(digest(raw) == expected, "decompressed identity: " + name)
        sources[name] = json.loads(raw)
    require(manifest["source_uncompressed_sha256"]["source-2598.json.gz"] == SOURCE_SHA, "frozen final source")
    source = sources["source-2598.json.gz"]
    family = read_json(directory / "fourth-row-bindings.json")
    bindings = read_json(directory / "family-source-manifest.json")["bindings"]
    validate_catalog(base, sources["source-2471.json.gz"], source, family, bindings)
    require(family == read_json(repo / manifest["lean_bindings"]["fourth"]["row_bindings"]), "Lean Fourth binding")
    require(read_json(repo / manifest["lean_bindings"]["sixth"]["support_data"])["support"] == SIXTH, "Lean Sixth binding")
    # These bind saved records to checked source identities. Re-run the sibling
    # Lean checkers for a fresh kernel run; this Python program is not Lean.
    for binding in manifest["lean_bindings"].values():
        record = read_json(repo / binding["kernel_record"])
        require(record["complete"] is True, "incomplete Lean record")
        audited = {name: axioms for module in record.get("modules", {}).values()
                   for name, axioms in module["axioms"].items()}
        audited.update(record.get("axioms", {}))
        require(binding["theorem"] in audited, "missing theorem audit")
        require(set(audited[binding["theorem"]]) <= AXIOMS, "extra theorem axiom")
        if "literal_binding_theorem" in binding:
            theorem = binding["literal_binding_theorem"]
            require(theorem in audited and set(audited[theorem]) <= AXIOMS, "literal binding audit")
            bridge = read_json(repo / binding["manifest"])
            require(bridge["source_uncompressed_sha256"] == SOURCE_SHA, "bridge source")
            require(bridge["new_rows"] == 129 and bridge["prefix_rows"] == 2469, "bridge sizes")
            require(bridge["bindings"] == [
                {"local_row": k, "source_row": 2469 + k,
                 "support": row["support"], "rhs": row["rhs"]}
                for k, row in enumerate(source["constraints"][2469:])], "bridge ordered rows")
    archive = json.loads(gzip.decompress((directory / "research-sources.json.gz").read_bytes()))
    for name, entry in archive["files"].items():
        require(digest(entry["text"].encode()) == entry["sha256"], "script archive: " + name)
    for result_name, script_name in (("family-witness-search.json", "family_mip.py"),
                                     ("tabu-result.json", "tabu.py")):
        result = read_json(directory / result_name)
        script = archive["files"][".cache/residual32-sixth-primal-2026-10-10/" + script_name]
        require(result["script_sha256"] == script["sha256"], "result script identity")
    evidence = read_json(directory / "candidates.json")
    require(evidence["source_sha256"] == SOURCE_SHA, "candidate source")
    rows = source["constraints"]
    results = {c["name"]: replay_candidate(rows, c) for c in evidence["candidates"]}
    require([v["row"] for v in results["original2469_witness"]] == [2469, 2470, 2471, 2472], "old witness strengthening")
    require(results["best_tabu_candidate"] == [{"row": 205, "count": 0, "rhs": 1, "deficit": 1}], "best candidate status")
    tabu = read_json(directory / "tabu-result.json")
    require(tabu["source_sha256"] == SOURCE_SHA and tabu["target_witness_found"] is False, "tabu status")
    require(tabu["best_candidate_holes"] == evidence["candidates"][2]["holes"], "tabu candidate identity")
    require(tabu["best_total_deficit"] == 1, "tabu deficit")
    repairs = {name: replay_two_exchange(rows, read_json(directory / name))
               for name in ("repair-best.json", "repair-best-final.json")}
    for name in ("witness-search.json", "family-witness-search.json"):
        record = read_json(directory / name)
        require(record["status"] == "timelimit" and record["witness_found"] is False, "solver claim")
    lp = read_json(directory / "lp-probe.json")
    require(lp["source_sha256"] == SOURCE_SHA and len(lp["results"]) == 8, "LP source or count")
    require(all(r["exact_contradiction"] is None for r in lp["results"]), "unsupported exact LP claim")
    return {"complete": True, "scope": "Exact catalog identities and integer diagnostics; no global infeasibility proof",
            "source_sha256": SOURCE_SHA, "rows": len(rows), "added_rows": 129,
            "candidate_violations": results, "local_repair_trials": repairs,
            "lean_kernel_executed_by_this_checker": False, "global_32_hole_exclusion": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = check()
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    print(text, end="")
