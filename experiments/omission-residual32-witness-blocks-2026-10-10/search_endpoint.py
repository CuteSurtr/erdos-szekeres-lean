#!/usr/bin/env python3
"""Look for23 occupied states excluding every four-cap label pattern.

The source uses four incoming-column heights. A real four-cap would give
four distinct owners and three strictly increasing cap-label columns, with
the height increasing across each pair at its chosen column. A discovered
support would still require a Lean transfer and finite check.
"""
import gzip
import hashlib
import itertools
import json
import time
from pathlib import Path

import z3
from search import HOLES

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent


def obstructions(states, selected, limit=3000):
    bad = set()
    for x, y, z in itertools.combinations(range(4), 3):
        left = {b: [a for a in selected if states[a][x] < states[b][x]] for b in selected}
        right = {c: [d for d in selected if states[c][z] < states[d][z]] for c in selected}
        for b in selected:
            for c in selected:
                if states[b][y] >= states[c][y]:
                    continue
                for a in left[b]:
                    if a == c:
                        continue
                    for d in right[c]:
                        if d == a or d == b:
                            continue
                        bad.add(tuple(sorted((a, b, c, d))))
                        if len(bad) >= limit:
                            return bad
    return bad


def main():
    source = ROOT / "experiments/omission-residual32-research-2026-10-10/source.json.gz"
    raw = gzip.decompress(source.read_bytes())
    states = json.loads(raw)["states"]
    occupied = [i for i in range(154) if i not in HOLES]
    variables = {i: z3.Bool(f"state_{i}") for i in occupied}
    solver = z3.Solver()
    solver.set(timeout=5000, random_seed=1)
    solver.add(z3.PbEq([(v, 1) for v in variables.values()], 23))
    total, rounds = set(), []
    start = time.monotonic()
    candidate = None
    verdict = "time_limit"
    while time.monotonic() - start < 120:
        status = solver.check()
        if status != z3.sat:
            verdict = str(status)
            break
        model = solver.model()
        selected = [i for i, v in variables.items() if z3.is_true(model.eval(v))]
        bad = obstructions(states, selected)
        rounds.append({"selected": selected, "new_obstructions": len(bad),
                       "elapsed": round(time.monotonic()-start, 3)})
        if not bad:
            candidate = selected
            verdict = "candidate"
            break
        assert not (bad & total)
        total |= bad
        for quad in sorted(bad):
            solver.add(z3.Or([z3.Not(variables[i]) for i in quad]))
        print(len(rounds), len(total), round(time.monotonic()-start, 2), flush=True)
    report = {"scope": "Finite candidate search for an endpoint-dependent four-cap obstruction; no Lean theorem",
              "source_uncompressed_sha256": hashlib.sha256(raw).hexdigest(),
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "holes": HOLES, "solver": "Z3 " + z3.get_version_string(), "status": verdict,
              "candidate": candidate, "rounds": rounds, "obstruction_count": len(total),
              "seconds": round(time.monotonic()-start, 3)}
    (HERE / "endpoint-search.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "rounds"}), flush=True)


if __name__ == "__main__":
    main()
