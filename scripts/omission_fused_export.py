#!/usr/bin/env python3
"""Export omission trees with a single packed arithmetic proof per leaf.

The original exporter and all old exports remain unchanged. This wrapper uses
its exact tree replay, catalog, partition, and branch proofs, then replaces the
two-step leaf proof by a generic composition of the same soundness theorems.
The helper is embedded in the new Catalog, preserving the existing checker's
Catalog/Part/Root source and dependency contract.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

import omission_lean_export as original


FUSED_HELPER = """theorem fused_sparse_packed_excludes {ρ : Type*} (base : ℕ) (cs : List ℕ)
    (support : ρ → Finset (Fin cs.length)) (demand code : ρ → ℕ)
    (entries : List (ρ × ℕ)) (missing occupied : Finset (Fin cs.length))
    (capacity budget : ℕ) (hcode : ∀ r, code r = rowCode base (support r))
    (checks : 1 < base ∧ sparseSum (fun _ => 1) entries < base ∧
      cs.all (fun c => decide (c < base)) = true ∧
      packList base cs = sparseSum code entries ∧
      capacity * (budget - missing.card) +
        (cs.map (fun c => c - capacity)).sum + ∑ i ∈ missing, cs.get i <
      sparseSum demand entries + ∑ i ∈ missing ∪ occupied, (cs.get i - capacity)) :
    ¬ ∃ holes : Fin cs.length → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧ (∑ i, holes i) ≤ budget ∧
      (∀ i ∈ missing, holes i = 1) ∧ (∀ i ∈ occupied, holes i = 0) := by
  rcases checks with ⟨hb, hw, hc, heq, hm⟩
  exact sparse_list_conditioned_excludes cs support demand entries missing occupied capacity budget
    (load_eq_of_sparse_packed base cs support code entries hcode hb hw hc heq) hm
"""


def fuse_source(source):
    """Replace only the original exporter's recognized weighted-leaf shape."""
    expected = len(re.findall(r"^theorem loads\d+ :", source, re.MULTILINE))
    result, removed = re.subn(r"theorem loads(\d+) :.*?(?=theorem node\1 :)",
                             "", source, flags=re.DOTALL)
    result, applications = re.subn(
        r"apply sparse_list_conditioned_excludes (cs\d+) support demand",
        r"apply fused_sparse_packed_excludes base \1 support demand code", result)
    result, arguments = re.subn(r" loads\d+\n", " code_correct\n", result)
    if (removed, applications, arguments) != (expected, expected, expected):
        raise ValueError("Original weighted-leaf shape changed; refusing a partial rewrite")
    if re.search(r"\bloads\d+\b|sparse_list_conditioned_excludes", result):
        raise ValueError("Unexpected leftover weighted-leaf proof")
    return result, expected


def export(source, tree, output, namespace="OmissionFusedExport", leaf_limit=64,
           subtree=None, module_prefix=""):
    report = original.export(source, tree, output, namespace, leaf_limit, subtree, module_prefix)
    source_dir = output / module_prefix if module_prefix else output
    catalog_path = source_dir / "Catalog.lean"
    catalog = catalog_path.read_text()
    ending = f"end {namespace}\n"
    if not catalog.endswith(ending):
        raise ValueError("Unexpected catalog namespace boundary")
    catalog_path.write_text(catalog[:-len(ending)] + "\n" + FUSED_HELPER + "\n" + ending)
    weighted_leaves = 0
    for path in sorted(source_dir.glob("*.lean")):
        if path == catalog_path:
            continue
        fused, count = fuse_source(path.read_text())
        weighted_leaves += count
        path.write_text(fused)
    report["base_exporter_sha256"] = report["exporter_sha256"]
    report["exporter_sha256"] = original.sha256(Path(__file__))
    report["proof_style"] = "fused_sparse_packed_v1"
    report["fused_helper_sha256"] = hashlib.sha256(FUSED_HELPER.encode()).hexdigest()
    report["fused_weighted_leaves"] = weighted_leaves
    report["files"] = {str(path.relative_to(output)): original.sha256(path)
                       for path in sorted(source_dir.glob("*.lean"))}
    (output / "export.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("tree", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--namespace", default="OmissionFusedExport")
    parser.add_argument("--leaf-limit", type=int, default=64)
    parser.add_argument("--subtree", type=int)
    parser.add_argument("--module-prefix", default="")
    args = parser.parse_args()
    result = export(args.source, args.tree, args.output, args.namespace, args.leaf_limit,
                    args.subtree, args.module_prefix)
    print(json.dumps({key: result[key] for key in ["states", "rows", "budget", "base",
                     "exported_leaves", "exported_parts", "proof_style", "lean_checked"]}))
