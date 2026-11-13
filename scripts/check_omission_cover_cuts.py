#!/usr/bin/env python3
"""Replay rounded omission-cover cuts using exact integer arithmetic.

This parser is not a Lean proof. Each accepted row records the finite data needed
by OmissionCertificates.rounded_cover_cut; a separate Lean replay must connect it
to the original row hypotheses. Solver statuses and numerical objectives are
ignored. The source hash and topological parent indices prevent silent reuse of
cuts with another row catalog.
"""
import argparse
import hashlib
import json
from pathlib import Path

from omission_row_probe import read_rows


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(source, certificate):
    n, rows = read_rows(source)
    original_count = len(rows)
    if type(certificate.get("base_rows")) is not int or certificate["base_rows"] != original_count:
        raise ValueError("Wrong number of original rows")
    proofs = certificate.get("proofs")
    if not isinstance(proofs, list):
        raise ValueError("Expected a list of cut proofs")
    depths = [0] * original_count
    margins = []
    for step, proof in enumerate(proofs):
        if (not isinstance(proof, dict) or type(proof.get("row")) is not int or
                proof["row"] != len(rows)):
            raise ValueError("Cut rows must be in topological order")
        support, demand = proof.get("support"), proof.get("rhs")
        read_rows({"states": [None] * n,
                   "constraints": [{"support": support, "rhs": demand}]})
        capacity, weights = proof.get("capacity"), proof.get("weights")
        if type(capacity) is not int or capacity < 0 or not isinstance(weights, list):
            raise ValueError("Invalid capacity or multipliers")
        loads, lower, parents = [0] * n, 0, set()
        for pair in weights:
            if not isinstance(pair, list) or len(pair) != 2:
                raise ValueError("Malformed row multiplier")
            row, weight = pair
            if (type(row) is not int or not 0 <= row < len(rows) or row in parents or
                    type(weight) is not int or weight <= 0):
                raise ValueError("Invalid or repeated parent row")
            parents.add(row)
            lower += weight * rows[row][1]
            for vertex in rows[row][0]:
                loads[vertex] += weight
        if proof.get("parents") != [row for row, _ in weights]:
            raise ValueError("Parent list and multipliers disagree")
        chosen = set(support)
        excess = sum(max(0, loads[i] - (capacity if i in chosen else 0))
                     for i in range(n))
        margin = lower - capacity * max(0, demand - 1) - excess
        if margin <= 0:
            raise ValueError(f"Nonpositive exact cut margin at row {len(rows)}")
        if "exact_margin" in proof and (type(proof["exact_margin"]) is not int or
                                        proof["exact_margin"] != margin):
            raise ValueError("Recorded margin does not match exact replay")
        rows.append((support, demand))
        depths.append(1 + max((depths[row] for row in parents), default=0))
        margins.append(margin)
    return {"states": n, "original_rows": original_count,
            "derived_rows": len(proofs), "total_rows": len(rows),
            "minimum_margin": min(margins, default=None),
            "maximum_derivation_depth": max(depths, default=0),
            "all_integer_margins_positive": True}


def run(source_path, certificate_path, output=None):
    source = json.loads(source_path.read_text())
    certificate = json.loads(certificate_path.read_text())
    if certificate.get("source_sha256") != sha256(source_path):
        raise ValueError("Certificate and source hashes differ")
    result = check(source, certificate)
    result.update(scope="Exact Python replay of arithmetic cuts; not a Lean certificate",
                  source_sha256=sha256(source_path),
                  certificate_sha256=sha256(certificate_path),
                  checker_sha256=sha256(Path(__file__)))
    text = json.dumps(result, indent=2) + "\n"
    if output is not None:
        output.write_text(text)
    print(text, end="")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    run(args.source, args.certificate, args.output)
