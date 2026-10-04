#!/usr/bin/env python3
"""Try replacing each vertex participating in a verified near-miss polygon.

Every attempt fixes all other coordinates. Failure does not rule out moving
several points together, and does not establish a universal upper bound.
"""
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path

from extend_configuration import run
from search import general_position, hull


def forbidden_subsets(points, k):
    return [indices for indices in combinations(range(len(points)), k)
            if len(hull([points[i] for i in indices])) == k]


def repair(source, folder, summary, seconds):
    if summary.exists():
        raise FileExistsError(summary)
    folder.mkdir(parents=True, exist_ok=False)
    data = json.loads(source.read_text())
    points, k = list(map(tuple, data["coordinates"])), data["gon"]
    if not general_position(points):
        raise ValueError("Input is not in general position")
    forbidden = forbidden_subsets(points, k)
    if not forbidden:
        raise ValueError("Input is not a near miss: it has no forbidden polygon")
    # A single deletion must hit every forbidden polygon.
    candidates = sorted(set.intersection(*(set(s) for s in forbidden)))
    result = {"scope": "fixed-coordinate single-vertex repair; not exhaustive over configurations",
              "source": str(source), "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
              "coordinates": points, "gon": k, "forbidden_subsets": forbidden,
              "candidate_indices": candidates, "status": "running", "attempts": []}
    summary.write_text(json.dumps(result, indent=2) + "\n")
    for index in candidates:
        print(f"Repair vertex {index}", flush=True)
        base = folder / f"delete-{index}.json"
        base.write_text(json.dumps({"coordinates": points[:index] + points[index + 1:], "gon": k}) + "\n")
        extension = run(base, folder / f"repair-{index}.json", seconds, fast=True)
        result["attempts"].append({"deleted_index": index, "extension": extension})
        if extension["status"] == "sat":
            result["status"] = "repair_found"
        summary.write_text(json.dumps(result, indent=2) + "\n")
        if result["status"] == "repair_found":
            break
    else:
        result["status"] = "bounded_campaign_completed"
    summary.write_text(json.dumps(result, indent=2) + "\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--folder", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    parser.add_argument("--seconds", type=int, default=120)
    args = parser.parse_args()
    repair(args.source, args.folder, args.summary, args.seconds)
