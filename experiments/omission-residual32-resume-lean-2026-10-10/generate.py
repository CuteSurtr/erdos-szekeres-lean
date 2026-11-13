#!/usr/bin/env python3
"""Export six completed conditional subtrees without asserting a closed root."""
import gzip
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent
ROOT = BUNDLE.parent.parent
RESEARCH = ROOT / "experiments/omission-residual32-resume-2026-10-10"
OLD = ROOT / "experiments/omission-residual32-context-certificates-2026-10-10"
TRANSFER = ROOT / "experiments/omission-residual32-transfer-2026-10-10"
sys.path.insert(0, str(ROOT / "scripts"))
from omission_lean_export import context_term, header, inspect_tree, node_source, node_statement
from omission_row_probe import read_rows

NODES = [492357, 29, 485519, 492355, 485517, 24]
PREFIX = "Residual32ResumeProof"
SHA = "f03eebb1d20eae3bd25dbb5024eaacdfdcc5bcd8ed964d190bdfa59c73aeb909"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def generate():
    source = ROOT / "experiments/omission-residual32-research-2026-10-10/source.json.gz"
    pending = ROOT / "experiments/omission-residual32-research-2026-10-10/pending-contexts.json"
    raw = gzip.decompress(source.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == SHA
    n, rows = read_rows(json.loads(raw))
    assert (n, len(rows)) == (154, 2469)
    contexts = {c["node"]: c for c in json.loads(pending.read_text())["contexts"]}
    spec = importlib.util.spec_from_file_location("resume_replay", RESEARCH / "check.py")
    replay = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(replay)
    old = json.loads((OLD / "manifest.json").read_text())
    assert old["source_uncompressed_sha256"] == SHA and old["base"] == 131072
    modules = BUNDLE / PREFIX
    modules.mkdir(exist_ok=True)
    proofs, files = [], {}
    for original in NODES:
        path = RESEARCH / f"closed-context-{original}.json.gz"
        tree = json.loads(gzip.decompress(path.read_bytes()))
        assert tree["original_node"] == original and tree["source_sha256"] == SHA
        exact = replay.replay(tree, rows, n, contexts[original])
        preorder, postorder, local, counts = inspect_tree(tree["nodes"], tree["root"])
        inherited = {index: (tree["missing"] + m, tree["occupied"] + o)
                     for index, (m, o) in local.items()}
        namespace = f"OmissionResidual32Resume.Context{original}"
        name = f"Context{original}"
        lines = header(["Residual32ContextsProof.Catalog"], namespace)
        lines += ["open OmissionResidual32Contexts",
                  "-- The initial context is inherited from the frozen original tree."]
        for index in postorder:
            node = tree["nodes"][index]
            if node["type"] == "weighted":
                assert sum(w for _, w in node["weights"]) < old["base"]
            lines += node_source(index, n, rows, tree["nodes"], 32, inherited)
        root = tree["root"]
        final = node_statement(root, n, 32, tree["missing"], tree["occupied"])
        final[0] = "theorem excludes_context :"
        lines += final + [f"  exact node{root}", "#print axioms excludes_context", f"end {namespace}"]
        (modules / f"{name}.lean").write_text("\n".join(lines) + "\n")
        proofs.append({"original_node": original, "archive": str(path.relative_to(ROOT)),
                       "archive_sha256": digest(path), "root": root,
                       "missing": tree["missing"], "occupied": tree["occupied"],
                       "module": f"{PREFIX}.{name}",
                       "theorem": namespace + ".excludes_context", "exact_replay": exact})
    lines = header([p["module"] for p in proofs] + ["ContextGeometry"], "OmissionResidual32Resume")
    lines += ["open ErdosSzekeres ErdosSzekeres.Omission OmissionResidual32Transfer"]
    for p in proofs:
        original = p["original_node"]
        m, o = context_term(p["missing"], n), context_term(p["occupied"], n)
        lines += [f"theorem geometric_context{original} {{n : ℕ}} (c : Configuration n)",
                  "    (noCap : ¬ c.HasCap 6)",
                  "    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))",
                  "    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) (hn : 122 ≤ n)",
                  f"    (hm : ∀ i ∈ {m}, i ∉ c.residualOccupied noCap noOctagon noJunction)",
                  f"    (ho : ∀ i ∈ {o}, i ∈ c.residualOccupied noCap noOctagon noJunction) : False := by",
                  f"  exact context_impossible_of_exclusion {m} {o}",
                  f"    Context{original}.excludes_context c noCap noOctagon noJunction hn hm ho",
                  f"#print axioms geometric_context{original}"]
        p["geometric_theorem"] = f"OmissionResidual32Resume.geometric_context{original}"
    lines += ["end OmissionResidual32Resume"]
    (modules / "Geometry.lean").write_text("\n".join(lines) + "\n")
    for path in sorted(modules.glob("*.lean")):
        files[str(path.relative_to(BUNDLE))] = digest(path)
    external = [source, pending, ROOT / "scripts/omission_lean_export.py",
                ROOT / "scripts/omission_row_probe.py", RESEARCH / "check.py", OLD / "manifest.json",
                OLD / "Residual32ContextsProof/Catalog.lean", TRANSFER / "mapping.json",
                TRANSFER / "kernel-check.json", TRANSFER / "ContextGeometry.lean", TRANSFER / "Transfer.lean"]
    manifest = {"scope": "Six complete inherited-context exclusions with explicit literal-row assumptions, plus actual-configuration corollaries. No complete32-hole exclusion or new planar bound.",
                "source_uncompressed_sha256": SHA, "generator_sha256": digest(Path(__file__)),
                "external_inputs": {str(p.relative_to(ROOT)): digest(p) for p in external},
                "proofs": proofs, "files": files}
    (BUNDLE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"contexts": NODES, "modules": len(files),
                      "weighted_leaves": sum(p["exact_replay"]["weighted_leaves"] for p in proofs)}))


if __name__ == "__main__":
    generate()
