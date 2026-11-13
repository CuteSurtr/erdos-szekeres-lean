#!/usr/bin/env python3
"""Export omission trees whose leaves read the catalog through packed lookups.

Profiling a fused export showed that most of the kernel time of a leaf went into
looking up `code r` and `demand r` in the catalog's nested arrays (about 6 ms per
lookup and two hundred lookups per leaf). This wrapper keeps the fused export
unchanged and adds, at the end of the Catalog,

* `fastDemand` and `fastCode`, which read the same numbers out of packed natural
  numbers with shifts and masks, both evaluated by the kernel's GMP arithmetic;
* `fastDemand_eq` and `fastCode_eq`, proving by an exhaustive kernel decision
  that they agree with `demand` and `code` on every row;
* `fused_fast_excludes`, which rewrites a fused leaf check through these
  equalities and reads the margin's coefficients with `List.getD` (the
  `Fin`-indexed `List.get` in the margin sums cost another fifth of a leaf).

Every leaf keeps its exact statement; only its proof changes from
`fused_sparse_packed_excludes ... code_correct` to
`fused_fast_excludes ... code_correct fastCode_eq fastDemand_eq`.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

import omission_fused_export as fused
import omission_lean_export as original

CHUNK = 32

FAST_HELPER = """theorem fused_fast_excludes {ρ : Type*} (base : ℕ) (cs : List ℕ)
    (support : ρ → Finset (Fin cs.length)) (demand code demand' code' : ρ → ℕ)
    (entries : List (ρ × ℕ)) (missing occupied : Finset (Fin cs.length))
    (capacity budget : ℕ) (hcode : ∀ r, code r = rowCode base (support r))
    (hcode' : ∀ r, code' r = code r) (hdemand' : ∀ r, demand' r = demand r)
    (checks : 1 < base ∧ sparseSum (fun _ => 1) entries < base ∧
      cs.all (fun c => decide (c < base)) = true ∧
      packList base cs = sparseSum code' entries ∧
      capacity * (budget - missing.card) +
        (cs.map (fun c => c - capacity)).sum + ∑ i ∈ missing, cs.getD i.val 0 <
      sparseSum demand' entries + ∑ i ∈ missing ∪ occupied, (cs.getD i.val 0 - capacity)) :
    ¬ ∃ holes : Fin cs.length → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧ (∑ i, holes i) ≤ budget ∧
      (∀ i ∈ missing, holes i = 1) ∧ (∀ i ∈ occupied, holes i = 0) := by
  have hget : ∀ i : Fin cs.length, cs.getD i.val 0 = cs.get i := fun i => by
    simp [List.getD_eq_getElem?_getD]
  rw [show code' = code from funext hcode', show demand' = demand from funext hdemand'] at checks
  simp only [hget] at checks
  exact fused_sparse_packed_excludes base cs support demand code entries missing occupied
    capacity budget hcode checks
"""


def lookup_source(rows, states, base):
    """Packed tables, their exhaustive agreement proofs, and the fast leaf lemma."""
    if base & (base - 1) or base < 2:
        raise ValueError("The packing base must be a power of two")
    width = (base.bit_length() - 1) * states
    demand_width = max(1, max(d for _, d in rows).bit_length())
    codes = [sum(base ** i for i in set(support)) for support, _ in rows]
    if any(c >> width for c in codes):
        raise ValueError("A row code does not fit its packed slot")
    demand_pack = sum(d << (demand_width * r) for r, (_, d) in enumerate(rows))
    chunks = [sum(codes[r] << (width * (r - k)) for r in range(k, min(len(rows), k + CHUNK)))
              for k in range(0, len(rows), CHUNK)]
    lines = [f"-- Packed lookups: {len(chunks)} chunks of {CHUNK} codes, {width}-bit slots.",
             f"def demandPack : ℕ := {demand_pack}"]
    lines += [f"def codeChunk{k} : ℕ := {c}" for k, c in enumerate(chunks)]
    lines.append("def codeChunks : List ℕ := [" +
                 ", ".join(f"codeChunk{k}" for k in range(len(chunks))) + "]")
    lines.append(f"def fastDemand (r : Fin {len(rows)}) : ℕ :=\n"
                 f"  (demandPack >>> ({demand_width} * r.val)) &&& (2 ^ {demand_width} - 1)")
    lines.append(f"def fastCode (r : Fin {len(rows)}) : ℕ :=\n"
                 f"  (codeChunks.getD (r.val / {CHUNK}) 0 >>> ({width} * (r.val % {CHUNK}))) &&&\n"
                 f"    (2 ^ {width} - 1)")
    lines.append(f"theorem fastDemand_eq : ∀ r : Fin {len(rows)}, fastDemand r = demand r := by\n"
                 "  decide +kernel")
    lines.append(f"theorem fastCode_eq : ∀ r : Fin {len(rows)}, fastCode r = code r := by\n"
                 "  decide +kernel")
    return "\n".join(lines) + "\n" + FAST_HELPER


def fast_source(source):
    """Rewrite exactly the fused weighted-leaf shape."""
    expected = len(re.findall(r"^  apply fused_sparse_packed_excludes ", source, re.MULTILINE))
    result, applications = re.subn(
        r"^  apply fused_sparse_packed_excludes base (cs\d+) support demand code\n",
        r"  apply fused_fast_excludes base \1 support demand code fastDemand fastCode\n",
        source, flags=re.MULTILINE)
    result, arguments = re.subn(r" code_correct\n  decide \+kernel\n",
                                " code_correct fastCode_eq fastDemand_eq\n  decide +kernel\n", result)
    if (applications, arguments) != (expected, expected):
        raise ValueError("Fused weighted-leaf shape changed; refusing a partial rewrite")
    if "fused_sparse_packed_excludes" in result:
        raise ValueError("Unexpected leftover fused leaf proof")
    return result, expected


def export(source, tree, output, namespace="OmissionFastExport", leaf_limit=64,
           subtree=None, module_prefix=""):
    report = fused.export(source, tree, output, namespace, leaf_limit, subtree, module_prefix)
    data = json.loads(Path(source).read_text())
    rows = [(r["support"], r["rhs"]) for r in data["constraints"]]
    if len(rows) != report["rows"] or len(data["states"]) != report["states"]:
        raise ValueError("Catalog size differs from the fused export")
    source_dir = output / module_prefix if module_prefix else output
    catalog_path = source_dir / "Catalog.lean"
    catalog = catalog_path.read_text()
    ending = f"end {namespace}\n"
    if not catalog.endswith(ending) or "theorem fused_sparse_packed_excludes" not in catalog:
        raise ValueError("Unexpected fused catalog")
    helper = lookup_source(rows, report["states"], report["base"])
    catalog_path.write_text(catalog[:-len(ending)] + "\n" + helper + "\n" + ending)
    leaves = 0
    for path in sorted(source_dir.glob("Part*.lean")):
        text, count = fast_source(path.read_text())
        leaves += count
        path.write_text(text)
    if leaves != report["fused_weighted_leaves"]:
        raise ValueError("Not every fused leaf was rewritten")
    report["fused_exporter_sha256"] = report["exporter_sha256"]
    report["exporter_sha256"] = original.sha256(Path(__file__))
    report["proof_style"] = "fast_packed_lookup_v2"
    report["fast_helper_sha256"] = hashlib.sha256(helper.encode()).hexdigest()
    report["fast_weighted_leaves"] = leaves
    report["files"] = {str(path.relative_to(output)): original.sha256(path)
                       for path in sorted(source_dir.glob("*.lean"))}
    (output / "export.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


if __name__ == "__main__":
    sys.set_int_max_str_digits(0)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("tree", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--namespace", default="OmissionFastExport")
    parser.add_argument("--leaf-limit", type=int, default=64)
    parser.add_argument("--subtree", type=int)
    parser.add_argument("--module-prefix", default="")
    args = parser.parse_args()
    result = export(args.source, args.tree, args.output, args.namespace, args.leaf_limit,
                    args.subtree, args.module_prefix)
    print(json.dumps({key: result[key] for key in ["states", "rows", "budget", "base",
                     "exported_leaves", "exported_parts", "proof_style", "fast_weighted_leaves"]}))
