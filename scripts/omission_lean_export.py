#!/usr/bin/env python3
"""Export exact omission trees as kernel-checkable Lean modules.

Contexts are emitted with explicit Finset type ascriptions so that empty and
singleton contexts elaborate without stuck typeclass problems.

The exporter is untrusted: each emitted leaf checks its packed columns and
strict integer margin in Lean, and branch proofs cover both Boolean values.
Catalog rows are literal source data; their geometric necessity is separate.
"""
import argparse
import gzip
import hashlib
import json
import re
from pathlib import Path

from omission_row_probe import read_rows
from omission_tree import check_tree


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path):
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix == ".gz" else raw)


def context_term(values, n):
    result = "∅"
    for i in values:
        result = f"(insert {i} {result})"
    return f"({result} : Finset (Fin {n}))"


def inspect_tree(nodes, root):
    """Return preorder, postorder, and ordered branch contexts."""
    preorder, postorder, contexts, counts = [], [], {}, {}

    def visit(index, missing, occupied):
        preorder.append(index)
        contexts[index] = missing, occupied
        node = nodes[index]
        if node["type"] == "branch":
            i = node["vertex"]
            visit(node["zero"], missing, occupied + [i])
            visit(node["one"], missing + [i], occupied)
            counts[index] = counts[node["zero"]] + counts[node["one"]]
        else:
            counts[index] = 1
        postorder.append(index)

    visit(root, [], [])
    return preorder, postorder, contexts, counts


def normalize_leaf(n, rows, node, missing):
    """Discard satisfied rows and compute the full, unconditioned columns."""
    missing = set(missing)
    entries = [(r, w) for r, w in node["weights"]
               if w and rows[r][1] > len(set(rows[r][0]) & missing)]
    columns = [0] * n
    for r, w in entries:
        for i in rows[r][0]:
            columns[i] += w
    return entries, columns


def header(imports, namespace):
    return [*(f"import {name}" for name in imports),
            "open scoped BigOperators",
            "open ErdosSzekeres.OmissionCertificates",
            f"namespace {namespace}",
            "set_option maxRecDepth 100000",
            "set_option maxHeartbeats 100000000"]


def catalog_source(n, rows, base, namespace, source_hash, chunk_size=128):
    lines = header(["ErdosSzekeres.OmissionPacking"], namespace)
    lines += [f"-- Literal omission rows; source SHA-256: {source_hash}",
              "-- Row necessity for planar configurations is not asserted here.",
              f"def base : ℕ := {base}"]
    names = []
    for start in range(0, len(rows), chunk_size):
        name = f"rows{start}"
        names.append(name)
        lines.append(f"def {name} : Array (Finset (Fin {n}) × ℕ × ℕ) := #[")
        for r, (support, demand) in enumerate(rows[start:start + chunk_size], start):
            literal = "{" + ", ".join(map(str, support)) + "}" if support else "∅"
            code = sum(base ** i for i in support)
            comma = "," if r + 1 < min(start + chunk_size, len(rows)) else ""
            lines.append(f"  ({literal}, {demand}, {code}){comma}")
        lines.append("]")
        lines += [f"theorem checked{start} : {name}.all (fun row => decide",
                  "    (row.2.2 = rowCode base row.1)) = true := by",
                  "  decide +kernel"]
    lines += ["def rowChunks := #[" + ", ".join(names) + "]",
              f"def row (r : Fin {len(rows)}) := (rowChunks[r.val / {chunk_size}]!)[r.val % {chunk_size}]!",
              f"def support (r : Fin {len(rows)}) : Finset (Fin {n}) := (row r).1",
              f"def demand (r : Fin {len(rows)}) : ℕ := (row r).2.1",
              f"def code (r : Fin {len(rows)}) : ℕ := (row r).2.2",
              "theorem checked : rowChunks.all (fun chunk => chunk.all",
              "    (fun row => decide (row.2.2 = rowCode base row.1))) = true := by",
              "  apply Array.all_eq_true.mpr",
              "  intro i hi",
              f"  have hlt : i < {len(names)} := by simpa [rowChunks] using hi",
              "  interval_cases i",
              *(f"  · exact checked{start}" for start in range(0, len(rows), chunk_size)),
              "theorem code_correct : ∀ r, code r = rowCode base (support r) := by",
              "  intro r",
              "  have hc := array_all_getElem! rowChunks _ checked (by rfl)",
              f"    (r.val / {chunk_size})",
              "  have hd : decide (0 = rowCode base (∅ : Finset (Fin " + str(n) + "))) = true := by",
              "    simp [rowCode]",
              "  have h := array_all_getElem! _ _ hc hd",
              f"    (r.val % {chunk_size})",
              "  simpa only [code, support, row] using of_decide_eq_true h",
              "#print axioms code_correct", f"end {namespace}"]
    return "\n".join(lines) + "\n"


def node_statement(index, n, budget, missing, occupied):
    return [f"theorem node{index} :",
            f"    ¬ ∃ holes : Fin {n} → ℕ, (∀ i, holes i ≤ 1) ∧",
            "      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧",
            f"      (∑ i, holes i) ≤ {budget} ∧",
            f"      (∀ i ∈ {context_term(missing, n)}, holes i = 1) ∧",
            f"      (∀ i ∈ {context_term(occupied, n)}, holes i = 0) := by"]


def node_source(index, n, rows, nodes, budget, contexts):
    node = nodes[index]
    missing, occupied = contexts[index]
    m, z = context_term(missing, n), context_term(occupied, n)
    lines = []
    if node["type"] == "weighted":
        entries, columns = normalize_leaf(n, rows, node, missing)
        pairs = ", ".join(f"({r}, {w})" for r, w in entries)
        lines += [f"def entries{index} : List (Fin {len(rows)} × ℕ) := [{pairs}]",
                  f"def cs{index} : List ℕ := [{', '.join(map(str, columns))}]",
                  f"theorem loads{index} : cs{index}.get =",
                  f"    load (fun i : Fin entries{index}.length => support (entries{index}.get i).1)",
                  f"      (fun i => (entries{index}.get i).2) := by",
                  f"  apply load_eq_of_sparse_packed base cs{index} support code",
                  f"    entries{index} code_correct",
                  "  · decide +kernel", "  · decide +kernel",
                  "  · decide +kernel", "  · decide +kernel"]
    lines += node_statement(index, n, budget, missing, occupied)
    if node["type"] == "weighted":
        lines += [f"  apply sparse_list_conditioned_excludes cs{index} support demand",
                  f"    entries{index} {m} {z} {node['capacity']} {budget} loads{index}",
                  "  decide +kernel"]
    elif node["type"] == "branch":
        lines += [f"  exact split_excludes support demand {budget} {m} {z}",
                  f"    {node['vertex']} node{node['zero']} node{node['one']}"]
    else:
        lines += ["  exact (CertificateTree.overBudget).check_sound support demand",
                  f"    {budget} {m} {z} (by decide +kernel)"]
    return lines


def export(source, tree, output, namespace="OmissionExport", leaf_limit=16, subtree=None):
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", namespace):
        raise ValueError("Use a simple Lean namespace identifier")
    if type(leaf_limit) is not int or leaf_limit < 1:
        raise ValueError("Leaf limit must be positive")
    if output.exists():
        raise FileExistsError(output)
    data, cert = read_json(source), read_json(tree)
    n, rows = read_rows(data)
    if not rows:
        raise ValueError("Empty catalogs are unsupported")
    source_hash = sha256(source)
    if cert.get("source_sha256") != source_hash:
        raise ValueError("Tree and source hashes differ")
    checked = check_tree(n, rows, cert["hole_budget"], cert["nodes"], cert["root"])
    nodes, budget = cert["nodes"], cert["hole_budget"]
    preorder, postorder, contexts, counts = inspect_tree(nodes, cert["root"])
    root = cert["root"] if subtree is None else subtree
    if type(root) is not int or root not in contexts:
        raise ValueError("Invalid subtree root")
    largest = max((sum(w for _, w in node["weights"])
                   for node in nodes if node["type"] == "weighted"), default=0)
    base = 1 << max(1, largest.bit_length())
    parts, remaining = [], []

    def partition(index):
        if counts[index] <= leaf_limit:
            parts.append(index)
        else:
            partition(nodes[index]["zero"])
            partition(nodes[index]["one"])
            remaining.append(index)

    partition(root)
    output.mkdir(parents=True)
    (output / "Catalog.lean").write_text(catalog_source(
        n, rows, base, namespace, source_hash))
    modules = []
    for part, index in enumerate(parts):
        name = f"Part{part:05d}"
        modules.append(name)
        selected = set()

        def collect(j):
            selected.add(j)
            if nodes[j]["type"] == "branch":
                collect(nodes[j]["zero"])
                collect(nodes[j]["one"])

        collect(index)
        lines = header(["Catalog"], namespace)
        for j in postorder:
            if j in selected:
                lines += node_source(j, n, rows, nodes, budget, contexts)
        lines += [f"#print axioms node{index}", f"end {namespace}"]
        (output / f"{name}.lean").write_text("\n".join(lines) + "\n")
    lines = header(modules, namespace)
    for index in remaining:
        lines += node_source(index, n, rows, nodes, budget, contexts)
    if root == cert["root"]:
        lines += ["theorem excludes_budget :",
                  f"    ¬ ∃ holes : Fin {n} → ℕ, (∀ i, holes i ≤ 1) ∧",
                  "      (∀ r, demand r ≤ ∑ i ∈ support r, holes i) ∧",
                  f"      (∑ i, holes i) ≤ {budget} := by",
                  "  rintro ⟨holes, hbool, hrows, hb⟩",
                  f"  exact node{root} ⟨holes, hbool, hrows, hb, by simp, by simp⟩",
                  "#print axioms excludes_budget"]
    else:
        lines += [f"#print axioms node{root}"]
    lines.append(f"end {namespace}")
    (output / "Root.lean").write_text("\n".join(lines) + "\n")
    report = {"scope": "Literal finite row system only; no geometric theorem",
              "source_sha256": source_hash, "tree_sha256": sha256(tree),
              "exporter_sha256": sha256(Path(__file__)),
              "states": n, "rows": len(rows), "budget": budget, "base": base,
              "namespace": namespace, "root": root, "full_tree_root": cert["root"],
              "exported_leaves": counts[root], "exported_parts": len(parts),
              "parts": [{"module": name, "root": index, "leaves": counts[index]}
                        for name, index in zip(modules, parts)],
              "contexts": {"missing": contexts[root][0], "occupied": contexts[root][1]},
              "python_check": checked,
              "lean_checked": False,
              "files": {p.name: sha256(p) for p in sorted(output.glob("*.lean"))}}
    (output / "export.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("tree", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--namespace", default="OmissionExport")
    parser.add_argument("--leaf-limit", type=int, default=16)
    parser.add_argument("--subtree", type=int)
    args = parser.parse_args()
    report = export(args.source, args.tree, args.output, args.namespace,
                    args.leaf_limit, args.subtree)
    print(json.dumps({k: report[k] for k in
                      ("states", "rows", "budget", "base", "exported_leaves", "exported_parts",
                       "lean_checked")}))
