#!/usr/bin/env python3
"""Reproduce augmented catalogs and Lean proofs from exact cover-cut DAGs.

The original row order is preserved. Every added row is replayed with unbounded
integer arithmetic before any output is written. The Lean proof rechecks each
strict margin and derives its row from earlier rows, so this exporter is outside
the trusted kernel. Existing output directories are never overwritten.

The pinned balanced/residual source catalogs are from Schroeder's release,
DOI 10.5281/zenodo.22842891 (data CC BY 4.0). The arithmetic rounding lemma is
ErdosSzekeres.OmissionCertificates.rounded_cover_cut.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re

from check_omission_cover_cuts import check
from omission_row_probe import read_rows


FAMILIES = {
    "residual": {
        "source_sha256": "bccd12477064d8a490bbe863ae49dbc8d9dfececf7a65426ba36f7537c66293a",
        "module": "ResidualCoverCuts", "catalog_module": "Catalog",
        "catalog_namespace": "OmissionResidual",
        "note": "Lean transfer is pending.",
    },
    "balanced": {
        "source_sha256": "23363c9e341a7edf4de28b6bf21970983cc6d4cafa6f2bdef54ce3d25b1c5a94",
        "module": "BalancedCoverCuts", "catalog_module": "BalancedProof.Catalog",
        "catalog_namespace": "OmissionBalanced",
        "note": "Lean transfer pending.",
    },
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def vector(items):
    return "![" + ", ".join(items) + "]"


def cases(items):
    result = "(fun i => Fin.elim0 i)"
    for item in reversed(items):
        result = f"(Fin.cases ({item}) {result})"
    return result


def augmented_data(source, certificate, family, source_hash, certificate_hash):
    """Return the original rows followed by the replayed topological cut DAG."""
    check(source, certificate)
    _, original = read_rows(source)
    rows = (copy.deepcopy(source["constraints"]) if "constraints" in source else
            [{"support": support, "rhs": demand} for support, demand in original])
    rows += [{"support": cut["support"], "rhs": cut["rhs"],
              "kind": "exact_arithmetic_cover_cut", "derivation_row": cut["row"]}
             for cut in certificate["proofs"]]
    return {
        "schema": f"exact-cover-augmented-{family}-v1",
        "states": source["states"], "constraints": rows,
        "base_source_sha256": source_hash,
        "cover_certificate_sha256": certificate_hash,
        "note": ("Original rows: Schroeder DOI10.5281/zenodo.22842891, CC-BY4.0. "
                 "Added rows are exact arithmetic consequences; " + FAMILIES[family]["note"]),
    }


def render_module(source, certificate, module, catalog_module, catalog_namespace):
    """Emit one ordinary proof per cut and a universal all_rows theorem."""
    check(source, certificate)
    for name in (module, catalog_namespace):
        if re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", name) is None:
            raise ValueError("Invalid Lean namespace")
    if re.fullmatch(r"(?:[A-Za-z][A-Za-z0-9_]*\.)?Catalog", catalog_module) is None:
        raise ValueError("Invalid original catalog module")
    n, original = read_rows(source)
    base = len(original)
    proofs = certificate["proofs"]
    lines = [f"import {catalog_module}", "import ErdosSzekeres.Omission.CoverCuts",
             "open scoped BigOperators", "open ErdosSzekeres.OmissionCertificates",
             f"namespace {module}", "set_option maxRecDepth 100000",
             "set_option maxHeartbeats 100000000",
             f'-- Original catalog SHA-256: {certificate["source_sha256"]}',
             "-- Each derived row is proved from original rows by a strict integer margin."]
    for index, cut in enumerate(proofs):
        support = "{" + ", ".join(map(str, cut["support"])) + "}" if cut["support"] else "∅"
        lines.append(f"def support{index} : Finset (Fin {n}) := {support}")
        supports, demands, weights, hypotheses = [], [], [], []
        for row, weight in cut["weights"]:
            if row < base:
                supports.append(f"{catalog_namespace}.support {row}")
                demands.append(f"{catalog_namespace}.demand {row}")
                hypotheses.append(f"hrows {row}")
            else:
                previous = row - base
                supports.append(f"support{previous}")
                demands.append(str(proofs[previous]["rhs"]))
                hypotheses.append(f"cut{previous} holes hbool hrows")
            weights.append(str(weight))
        lines += [
            f"theorem cut{index} (holes : Fin {n} → ℕ) (hbool : ∀ i, holes i ≤ 1)",
            f"    (hrows : ∀ r : Fin {base}, {catalog_namespace}.demand r ≤",
            f"      ∑ i ∈ {catalog_namespace}.support r, holes i) :",
            f'    {cut["rhs"]} ≤ ∑ i ∈ support{index}, holes i := by',
            f"  apply rounded_cover_cut {vector(supports)} {vector(demands)} {vector(weights)}",
            f'    support{index} {cut["capacity"]} {cut["rhs"]} (by decide +kernel) holes hbool',
            f"  exact {cases(hypotheses)}",
        ]
        if index % 25 == 0:
            lines.append(f"#print axioms cut{index}")
    lines += [
        f"def support : Fin {len(proofs)} → Finset (Fin {n}) := " +
        vector([f"support{i}" for i in range(len(proofs))]),
        f"def demand : Fin {len(proofs)} → ℕ := " +
        vector([str(cut["rhs"]) for cut in proofs]),
        f"theorem all_rows (holes : Fin {n} → ℕ) (hbool : ∀ i, holes i ≤ 1)",
        f"    (hrows : ∀ r : Fin {base}, {catalog_namespace}.demand r ≤",
        f"      ∑ i ∈ {catalog_namespace}.support r, holes i) :",
        "    ∀ r, demand r ≤ ∑ i ∈ support r, holes i := by",
        "  unfold support demand",
        "  exact " + cases([f"cut{i} holes hbool hrows" for i in range(len(proofs))]),
        "#print axioms all_rows", f"end {module}",
    ]
    return "\n".join(lines) + "\n"


def export(source_path, certificate_path, output, family, module=None):
    if output.exists():
        raise FileExistsError(output)
    configuration = FAMILIES[family]
    source_hash, certificate_hash = digest(source_path), digest(certificate_path)
    if source_hash != configuration["source_sha256"]:
        raise ValueError("Source does not match the pinned original catalog")
    source = json.loads(source_path.read_text())
    certificate = json.loads(certificate_path.read_text())
    if certificate.get("source_sha256") != source_hash:
        raise ValueError("Certificate and original source hashes differ")
    replay = check(source, certificate)
    augmented = augmented_data(source, certificate, family, source_hash, certificate_hash)
    module = configuration["module"] if module is None else module
    lean_source = render_module(source, certificate, module,
                                configuration["catalog_module"], configuration["catalog_namespace"])
    output.mkdir(parents=True)
    (output / "source.json").write_text(json.dumps(augmented, separators=(",", ":")) + "\n")
    (output / "cover-certificate.json").write_bytes(certificate_path.read_bytes())
    lean_path = output / (module + ".lean")
    lean_path.write_text(lean_source)
    manifest = {
        "scope": "Exact arithmetic consequences of the original omission rows; no new geometric hypotheses",
        "module": module, "namespace": module,
        "catalog_module": configuration["catalog_module"],
        "catalog_namespace": configuration["catalog_namespace"],
        "states": replay["states"], "original_rows": replay["original_rows"],
        "derived_rows": replay["derived_rows"],
        "source": str(source_path.resolve()), "source_sha256": source_hash,
        "certificate": str((output / "cover-certificate.json").resolve()),
        "certificate_sha256": certificate_hash,
        "augmented_source": "source.json", "augmented_source_sha256": digest(output / "source.json"),
        "generator_sha256": digest(Path(__file__)),
        "files": {lean_path.name: digest(lean_path)}, "python_replay": replay,
        "lean_checked": False,
    }
    (output / "export.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--family", required=True, choices=FAMILIES)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--module", help="Distinct module/namespace for a different cut DAG")
    args = parser.parse_args()
    result = export(args.source, args.certificate, args.output, args.family, args.module)
    print(json.dumps({key: result[key] for key in
                      ("module", "states", "original_rows", "derived_rows", "lean_checked")}))
