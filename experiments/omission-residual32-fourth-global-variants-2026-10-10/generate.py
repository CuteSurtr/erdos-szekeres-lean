#!/usr/bin/env python3
"""Export128 distinct new Fourth-compatible maps in16-row kernel chunks."""
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
NS = "ErdosSzekeres.Omission.CoupledFourthGlobalVariants"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    candidates = [json.loads((HERE / name).read_text()) for name in ["variants.json", "variants-all-states.json"]]
    source = ROOT / candidates[0]["source_archive"]
    raw = gzip.decompress(source.read_bytes())
    source_hash = hashlib.sha256(raw).hexdigest()
    assert source_hash == candidates[0]["source_uncompressed_sha256"] == candidates[1]["source_uncompressed_sha256"]
    old = {frozenset(r["support"]) for r in json.loads(raw)["constraints"] if r["rhs"] > 0}
    maps, seen = [], set()
    for candidate in candidates:
        for support in candidate["supports"]:
            key = frozenset(support)
            assert len(key) == len(support) == 13 and all(0 <= x < 154 for x in support)
            assert key not in old
            if key not in seen and len(maps) < 128:
                seen.add(key)
                maps.append(support)
    assert len(maps) == 128
    out = HERE / "FourthGlobalProof"
    out.mkdir(exist_ok=True)
    head = f"namespace {NS}\nopen CoupledTemplateFourth\nset_option maxRecDepth 100000\nset_option maxHeartbeats 100000000\n\n"
    data = "import ErdosSzekeres.Omission.CoupledTemplateFourthGeometry\nimport ErdosSzekeres.Omission.CoupledTemplateFourthCheck\n\n" + head
    for i, support in enumerate(maps):
        data += f"def state{i:03d} : Fin 13 → Fin 154 := ![" + ", ".join(map(str, support)) + "]\n"
    for part in range(8):
        data += f"def states{part:02d} : Array (Fin 13 → Fin 154) := #[" + ", ".join(f"state{i:03d}" for i in range(part*16,part*16+16)) + "]\n"
    data += "def blocks := #[" + ", ".join(f"states{i:02d}" for i in range(8)) + "]\n"
    data += "def maps (r : Fin 128) : Fin 13 → Fin 154 := (blocks[r.val / 16]!)[r.val % 16]!\n"
    data += "def support (r : Fin 128) : Finset (Fin 154) := Finset.univ.image (maps r)\n"
    data += f"end {NS}\n"
    (out / "Data.lean").write_text(data)
    for part in range(8):
        text = "import FourthGlobalProof.Data\n\n" + head + f"namespace Part{part:02d}\n"
        for i in range(part*16, part*16+16):
            text += f"private theorem checked{i:03d} : Function.Injective state{i:03d} ∧ Compatible state{i:03d} := by\n"
            text += "  exact ⟨by decide +kernel, check_sound _ (by decide +kernel)⟩\n\n"
        text += f"theorem checked : ∀ r : Fin 16, Function.Injective (maps ⟨{part*16} + r.val, by omega⟩) ∧\n"
        text += f"    Compatible (maps ⟨{part*16} + r.val, by omega⟩) := by\n  intro r\n  fin_cases r\n"
        text += "".join(f"  · exact checked{i:03d}\n" for i in range(part*16, part*16+16))
        text += f"#print axioms checked\nend Part{part:02d}\nend {NS}\n"
        (out / f"Part{part:02d}.lean").write_text(text)
    text = "".join(f"import FourthGlobalProof.Part{part:02d}\n" for part in range(8)) + "\n" + head
    text += "theorem checked : ∀ r : Fin 128, Function.Injective (maps r) ∧ Compatible (maps r) := by\n  intro r\n  fin_cases r\n"
    text += "".join(f"  · exact Part{i//16:02d}.checked {i%16}\n" for i in range(128))
    text += """
/-- Every literal row has demand one in an actual residual configuration. -/
theorem all_rows {n : ℕ} (c : Configuration n)
    (noCap : ¬ c.HasCap 6)
    (noOctagon : ¬ HasConvexNGon 8 (Finset.univ.image c.point))
    (noJunction : Subsets.NoJunctionOn c.cup (Finset.range n)) :
    ∀ r : Fin 128, 1 ≤ (support r \\ c.residualOccupied noCap noOctagon noJunction).card := by
  intro r
  exact CoupledTemplateFourth.hole_bound (maps r) (checked r).1 (checked r).2
    c noCap noOctagon noJunction
#print axioms checked
#print axioms all_rows
""" + f"end {NS}\n"
    (out / "Root.lean").write_text(text)
    bindings = {"scope": "128 prospective literal geometric rows; read kernel-check.json for validation status",
                "namespace": NS, "rows": [{"row": i, "support": sorted(s), "rhs": 1, "mapping": s} for i,s in enumerate(maps)]}
    (HERE / "row-bindings.json").write_text(json.dumps(bindings, indent=2) + "\n")
    external = [source, ROOT / candidates[0]["witness"], ROOT / candidates[0]["template"],
                ROOT / "ErdosSzekeres/Omission/CoupledTemplateFourthCheck.lean",
                ROOT / "ErdosSzekeres/Omission/CoupledTemplateFourthGeometry.lean"]
    manifest = {"scope": "128 distinct additional Fourth-template rows; no standalone planar bound",
                "namespace": NS, "source_uncompressed_sha256": source_hash,
                "generator_sha256": sha(Path(__file__)),
                "external_inputs": {str(p.relative_to(ROOT)): sha(p) for p in external},
                "inputs": {name: sha(HERE/name) for name in ["variants.json", "variants-all-states.json", "row-bindings.json"]},
                "files": {str(p.relative_to(HERE)): sha(p) for p in sorted(out.glob("*.lean"))},
                "modules": ["Data"] + [f"Part{i:02d}" for i in range(8)] + ["Root"],
                "rows": 128, "part_size": 16}
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"rows": len(maps), "modules": manifest["modules"]}))


if __name__ == "__main__":
    main()
