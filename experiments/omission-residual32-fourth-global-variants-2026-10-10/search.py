#!/usr/bin/env python3
"""Enumerate injective Fourth-template maps outside the old local component.

Only positive maps are exported; reaching the support/time limit is not an
exhaustiveness claim. Every output still needs an independent Lean check.
"""
import argparse
import ast
import gzip
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

for key in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[key] = "1"
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from omission_cycle_enumeration import pair_boxes, triple_table


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all-states", action="store_true")
    args = parser.parse_args()
    source = ROOT / "experiments/omission-residual32-research-2026-10-10/source.json.gz"
    witness = ROOT / "experiments/omission-residual32-case4-2026-10-10/witness.json"
    template = ROOT / "ErdosSzekeres/Omission/CoupledTemplateFourth.lean"
    raw = gzip.decompress(source.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == "f03eebb1d20eae3bd25dbb5024eaacdfdcc5bcd8ed964d190bdfa59c73aeb909"
    data = json.loads(raw)
    states = data["states"]
    holes = set(json.loads(witness.read_text())["holes"])
    targets = list(range(154)) if args.all_states else sorted(set(range(154)) - holes)
    old_supports = {frozenset(r["support"]) for r in data["constraints"] if r["rhs"] > 0}
    cells = [{(i+1,j) for i,h in enumerate(s[:4]) for j in range(1,h+1)} for s in states]
    P, mn, mx = pair_boxes(states)
    TT = triple_table(P, mn, mx)
    criteria = []
    for name, kind in [("emptyTests", "empty"), ("domainTests", "domain"), ("positiveTests", "positive")]:
        match = re.search(r"def " + name + r" :[^\n]+:= (\[[^\n]*\])", template.read_text())
        assert match, name
        criteria.extend((kind, tuple(item)) for item in ast.literal_eval(match[1]))
    differences = [[cells[b] - cells[a] - {(1,6)} for b in range(154)] for a in range(154)]

    def good(item, S):
        kind, q = item
        a, b = S[q[0]], S[q[1]]
        if kind == "positive":
            return bool(TT[a,b,S[q[2]]])
        return not differences[a][b] if kind == "empty" else (q[2], q[3]) not in differences[a][b]

    scopes = [set(q[:3] if kind == "positive" else q[:2]) for kind,q in criteria]
    checks = [[(c,sc) for c,sc in zip(criteria,scopes) if i in sc] for i in range(13)]
    start = time.monotonic()
    nodes = mappings = 0
    found = {}
    halted = None

    def dfs(S, used, assigned):
        nonlocal nodes, mappings, halted
        nodes += 1
        if len(found) >= 128:
            halted = "128 distinct new supports"
            return
        if time.monotonic() - start > 60:
            halted = "60 second search limit"
            return
        if len(assigned) == 13:
            mappings += 1
            key = frozenset(S)
            assert len(key) == 13
            if not args.all_states:
                assert not (key & holes)
            assert all(good(c, S) for c in criteria)
            if key not in old_supports and key not in found:
                found[key] = S.copy()
            return
        best = None
        for i in sorted(set(range(13)) - assigned):
            ready = [c for c,sc in checks[i] if sc - {i} <= assigned]
            opts = []
            for v in targets:
                if v in used:
                    continue
                S[i] = v
                if all(good(c,S) for c in ready):
                    opts.append(v)
            S[i] = None
            score = (len(opts), -len(ready), -len(checks[i]))
            if best is None or score < best[0]:
                best = (score, i, opts)
            if not opts:
                return
        _, i, opts = best
        for v in opts:
            S[i] = v
            dfs(S, used | {v}, assigned | {i})
            if halted:
                return
        S[i] = None

    dfs([None]*13, set(), set())
    result = {"scope": "Candidate injective Fourth-template substitutions; no completeness claim; Lean check separate",
              "source_archive": str(source.relative_to(ROOT)), "source_archive_sha256": sha(source),
              "source_uncompressed_sha256": hashlib.sha256(raw).hexdigest(),
              "witness": str(witness.relative_to(ROOT)), "witness_sha256": sha(witness),
              "template": str(template.relative_to(ROOT)), "template_sha256": sha(template),
              "script_sha256": sha(Path(__file__)), "criterion_count": len(criteria),
              "holes": sorted(holes), "targets": targets, "recursive_nodes": nodes,
              "completed_injective_maps": mappings, "supports": list(found.values()),
              "new_distinct_supports": len(found),
              "all_violate_witness": all(not(key & holes) for key in found),
              "complete_search": halted is None, "stop_reason": halted,
              "seconds": round(time.monotonic()-start, 3)}
    (HERE / ("variants-all-states.json" if args.all_states else "variants.json")).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ("supports", "targets", "holes")}), flush=True)


if __name__ == "__main__":
    main()
