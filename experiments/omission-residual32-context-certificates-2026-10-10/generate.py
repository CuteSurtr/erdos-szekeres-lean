#!/usr/bin/env python3
"""Deterministically emit five conditional Lean exclusions from frozen inputs.

The generator is untrusted. Lean checks all row encodings, exact column loads,
and strict margins. Geometric necessity of the literal rows is an assumption.
"""
import gzip
import hashlib
import json
import sys
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent
ROOT = BUNDLE.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from omission_lean_export import catalog_source, header, node_source, normalize_leaf
from omission_row_probe import read_rows


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def generate():
    source = ROOT / "experiments/omission-residual32-research-2026-10-10/source.json.gz"
    diagnostic = ROOT / "experiments/omission-residual32-three-row-probe-2026-10-10/diagnostic.json"
    pending = ROOT / "experiments/omission-residual32-research-2026-10-10/pending-contexts.json"
    raw = gzip.decompress(source.read_bytes())
    probe = json.loads(diagnostic.read_text())
    assert digest(raw) == probe["source_sha256"]
    assert digest(pending.read_bytes()) == probe["pending_contexts_sha256"]
    n, rows = read_rows(json.loads(raw))
    assert (n, len(rows)) == (154, 2469)
    cuts = probe["cuts_for_original_source"]
    assert [c["exact_integer_margin"] for c in cuts] == [11, 1, 159, 13, 21]
    frozen_contexts = {c["node"]: c for c in json.loads(pending.read_text())["contexts"]}
    for cut in cuts:
        assert cut["missing"] == frozen_contexts[cut["node"]]["missing"]
        assert cut["occupied"] == frozen_contexts[cut["node"]]["occupied"]
        assert not (set(cut["missing"]) & set(cut["occupied"]))
        assert all(0 <= r < len(rows) and w > 0 for r, w in cut["leaf"]["weights"])
    contexts = {c["node"]: (c["missing"], c["occupied"]) for c in cuts}
    nodes = {c["node"]: c["leaf"] for c in cuts}
    base = 1 << max(sum(w for _, w in c["leaf"]["weights"]) for c in cuts).bit_length()
    prefix, namespace = "Residual32ContextsProof", "OmissionResidual32Contexts"
    modules = BUNDLE / prefix
    modules.mkdir(exist_ok=True)
    (modules / "Catalog.lean").write_text(catalog_source(n, rows, base, namespace, digest(raw)))
    reports = []
    for cut in cuts:
        index = cut["node"]
        entries, columns = normalize_leaf(n, rows, cut["leaf"], cut["missing"])
        missing, occupied = map(set, (cut["missing"], cut["occupied"]))
        capacity = cut["leaf"]["capacity"]
        lhs = capacity * (32 - len(missing)) + sum(max(c-capacity, 0) for c in columns) + sum(columns[i] for i in missing)
        rhs = sum(w * rows[r][1] for r, w in entries) + sum(max(columns[i]-capacity, 0) for i in missing | occupied)
        assert rhs - lhs == cut["exact_integer_margin"]
        lines = header([prefix + ".Catalog"], namespace)
        lines += ["-- Conditional arithmetic exclusion; geometric row validity is explicit."]
        lines += node_source(index, n, rows, nodes, 32, contexts)
        lines += [f"#print axioms node{index}", f"end {namespace}"]
        module = f"Node{index}"
        (modules / (module + ".lean")).write_text("\n".join(lines) + "\n")
        reports.append({"node": index, "theorem": f"{namespace}.node{index}",
                        "module": f"{prefix}.{module}", "missing": sorted(missing),
                        "occupied": sorted(occupied), "capacity": capacity,
                        "weighted_rows": len(entries), "integer_margin": rhs - lhs,
                        "margin_lhs": lhs, "margin_rhs": rhs})
    lines = header([r["module"] for r in reports], namespace)
    lines += ["-- This audit imports five independent contextual exclusions, not a closed tree."]
    lines += [f"#print axioms node{c['node']}" for c in cuts]
    lines += [f"end {namespace}"]
    (modules / "Audit.lean").write_text("\n".join(lines) + "\n")
    report = {
        "scope": "Five conditioned arithmetic exclusions for a literal 2469-row Boolean system; all row inequalities are explicit assumptions. No geometric transfer or complete 32-hole exclusion.",
        "source_reference": str(source.relative_to(ROOT)),
        "source_archive_sha256": digest(source.read_bytes()),
        "source_uncompressed_sha256": digest(raw),
        "diagnostic_reference": str(diagnostic.relative_to(ROOT)),
        "diagnostic_sha256": digest(diagnostic.read_bytes()),
        "pending_contexts_reference": str(pending.relative_to(ROOT)),
        "pending_contexts_sha256": digest(pending.read_bytes()),
        "exporter_sha256": digest((ROOT / "scripts/omission_lean_export.py").read_bytes()),
        "generator_sha256": digest(Path(__file__).read_bytes()),
        "states": n, "rows": len(rows), "budget": 32, "base": base,
        "contexts": reports,
        "files": {str(p.relative_to(BUNDLE)): digest(p.read_bytes()) for p in sorted(modules.glob("*.lean"))},
    }
    (BUNDLE / "manifest.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"modules": len(report["files"]), "base": base, "margins": [r["integer_margin"] for r in reports]}))


if __name__ == "__main__":
    generate()
