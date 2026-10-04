#!/usr/bin/env python3
"""Move existing points across order-type cells, then try full-plane extension.

This is a bounded exploration of particular realizable configurations. A failed
extension is never reported as a universal Erdős–Szekeres upper bound.
"""
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path
import random
import time

from extend_configuration import run
from search import orient


def signature(points):
    ordered = sorted(map(tuple, points))
    signs = bytes(int(orient(*triple) > 0) for triple in combinations(ordered, 3))
    return hashlib.sha256(signs).hexdigest()


def campaign(source, folder, summary, rounds, seconds, seed):
    folder.mkdir(parents=True, exist_ok=False)
    if summary.exists():
        raise FileExistsError(summary)
    rng = random.Random(seed)
    current = source
    initial = json.loads(source.read_text())
    seen = {signature(initial["coordinates"])}
    result = {"scope": "bounded exploration of realizable fixed configurations; not exhaustive",
              "source": str(source), "seed": seed, "round_limit": rounds,
              "seconds_per_solver_call": seconds, "status": "running", "rounds": []}
    started = time.monotonic()
    for step in range(rounds):
        index = rng.randrange(len(initial["coordinates"]))
        print(f"Mutation round {step + 1}/{rounds}: replace point {index}", flush=True)
        moved_path = folder / f"round-{step:03d}-moved.json"
        moved = run(current, moved_path, seconds, replace_index=index, fast=True)
        entry = {"round": step, "replacement": index, "mutation": moved}
        if moved["status"] == "sat":
            current = moved_path
            sig = signature(moved["coordinates"])
            entry["orientation_signature"] = sig
            entry["previously_seen_signature"] = sig in seen
            if sig not in seen:
                seen.add(sig)
                extended = run(current, folder / f"round-{step:03d}-extension.json", seconds, fast=True)
                entry["extension"] = extended
                if extended["status"] == "sat":
                    result["status"] = "extension_found"
        result["rounds"].append(entry)
        result.update(distinct_signatures=len(seen), seconds=time.monotonic() - started)
        summary.write_text(json.dumps(result, indent=2) + "\n")
        if result["status"] == "extension_found":
            break
    else:
        result["status"] = "bounded_campaign_completed"
    result["last_configuration"] = str(current)
    summary.write_text(json.dumps(result, indent=2) + "\n")
    print(f"Campaign: {result['status']}; {len(seen)} orientation signatures", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--folder", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--rounds", type=int, default=20)
    parser.add_argument("--seconds", type=int, default=60)
    parser.add_argument("--seed", type=int, default=20261004)
    args = parser.parse_args()
    if args.rounds < 1 or args.seconds < 1:
        parser.error("Positive round and time limits required")
    campaign(args.source, args.folder, args.summary, args.rounds, args.seconds, args.seed)
