#!/usr/bin/env python3
"""Emit the literal 2,650-row residual catalog as a packed Lean module.

The generator is untrusted. It reads the frozen search input
`omission-residual32-rank-global-2026-10-10/source-2650.json.gz`, checks its
pinned SHA-256 identities, and writes `Residual32Bridge2650/Catalog.lean` with
the repository's established packed-catalog exporter (`catalog_source` from
`scripts/omission_lean_export.py`, base 2^17 as in the 2,469-row catalog).
Lean itself checks every row code and, in `Matches.lean`, every literal row
against the separately proved geometric families.

The integer cross-checks below only catch mistakes early; they are not part of
the proof. The manifest pins the source, generator, exporter and every Lean
file of this bundle.
"""
import gzip
import hashlib
import json
import re
import sys
from pathlib import Path

BUNDLE = Path(__file__).resolve().parent
ROOT = BUNDLE.parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from omission_lean_export import catalog_source  # noqa: E402
from omission_row_probe import read_rows  # noqa: E402

SOURCE = ROOT / "experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz"
SOURCE_SHA = "e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6"
RESEARCH = ROOT / "experiments/omission-residual32-research-2026-10-10/source.json.gz"
RESEARCH_SHA = "f03eebb1d20eae3bd25dbb5024eaacdfdcc5bcd8ed964d190bdfa59c73aeb909"
ADDED = ROOT / "experiments/omission-residual32-added-rows-2026-10-10/AddedRows.lean"
RELAXED = ROOT / "experiments/omission-residual32-sixth-relaxed-2026-10-10/SixthRelaxedProof/Data.lean"
RANK = ROOT / "experiments/omission-residual32-rank-certificates-2026-10-10"
RANK_NAMES = ("One", "Two", "Three", "Four")
NAMESPACE = "OmissionResidual32Bridge2650"
PREFIX = "Residual32Bridge2650"
BASE = 1 << 17
HANDWRITTEN = ["Matches.lean", "Rows.lean", "Final.lean"]
# Ordered row blocks of the 2,650-row source (zero based, end exclusive).
BLOCKS = [
    {"rows": [0, 2469], "family": "OmissionResidual32Contexts.support/demand",
     "geometry": "OmissionResidual32Transfer.all_rows"},
    {"rows": [2469, 2598], "family": "ErdosSzekeres.Omission.Residual32AddedRows.support",
     "geometry": "ErdosSzekeres.Omission.Residual32AddedRows.all_rows"},
    {"rows": [2598, 2646], "family": "ErdosSzekeres.Omission.CoupledSixthRelaxedVariants.support",
     "geometry": "ErdosSzekeres.Omission.CoupledSixthRelaxedVariants.all_rows"},
    *({"rows": [2646 + k, 2647 + k],
       "family": f"ErdosSzekeres.Omission.CoupledCoreRankSearch{name}.support.toFinset",
       "geometry": f"ErdosSzekeres.Omission.CoupledCoreRankSearch{name}.hole_bound"}
      for k, name in enumerate(RANK_NAMES)),
]

WRAPPER = """
namespace {ns}
/-! Public names for the literal 2,650-row catalog. Row `r` is the zero-based
entry `constraints[r]` of `source-2650.json.gz`; its support is `support` and its
demand is `rhs`. Validity for real point configurations is proved separately in
`Residual32Bridge2650.Rows`, not asserted here. -/

/-- Literal support of row `r` of the 2,650-row residual catalog. -/
def support2650 (r : Fin 2650) : Finset (Fin 154) := support r

/-- Literal demand (`rhs`) of row `r` of the 2,650-row residual catalog. -/
def demand2650 (r : Fin 2650) : ℕ := demand r

theorem support2650_eq (r : Fin 2650) : support2650 r = support r := rfl
theorem demand2650_eq (r : Fin 2650) : demand2650 r = demand r := rfl
end {ns}
"""


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def sha(path):
    return digest(path.read_bytes())


def lean_lists(pattern, text):
    return [[int(x) for x in m.split(",")] for m in re.findall(pattern, text, re.M)]


def cross_check(rows, states):
    """Untrusted integer comparison with the Lean literal families."""
    research_raw = gzip.decompress(RESEARCH.read_bytes())
    assert digest(research_raw) == RESEARCH_SHA
    research = json.loads(research_raw)
    n, old = read_rows(research)
    assert n == 154 and len(old) == 2469 and research["states"] == states
    assert [list(r) for r in rows[:2469]] == [list(r) for r in old], "prefix differs"
    assert all(d == 1 for _, d in rows[2469:]), "suffix demand differs from one"
    added = lean_lists(r"^\s*\[([0-9, ]+)\]\.toFinset,?$", ADDED.read_text())
    assert len(added) == 129
    assert all(set(a) == set(rows[2469 + k][0]) for k, a in enumerate(added))
    data = RELAXED.read_text()
    maps = {k: [int(x) for x in v.split(",")] for k, v in
            re.findall(r"def state(\d+) : Fin 13 → Fin 154 := !\[([0-9, ]+)\]", data)}
    order = re.search(r"def maps : Fin 48 → Fin 13 → Fin 154 := !\[([^\]]*)\]", data).group(1)
    names = [m.strip().removeprefix("state") for m in order.split(",")]
    assert len(names) == 48
    assert all(set(maps[m]) == set(rows[2598 + k][0]) for k, m in enumerate(names))
    for k, name in enumerate(RANK_NAMES):
        text = (RANK / f"RankCore{name}.lean").read_text()
        support = lean_lists(r"^def support : List \(Fin 154\) := \[([0-9, ]+)\]$", text)
        assert len(support) == 1 and set(support[0]) == set(rows[2646 + k][0])


def load_source():
    """Read the frozen source after checking its pinned uncompressed identity."""
    archive = SOURCE.read_bytes()
    raw = gzip.decompress(archive)
    if digest(raw) != SOURCE_SHA:
        raise ValueError("source-2650.json.gz differs from its pinned identity")
    data = json.loads(raw)
    n, rows = read_rows(data)
    if (n, len(rows)) != (154, 2650) or data["states"][0] != [0, 0, 0, 0, 0]:
        raise ValueError("Unexpected catalog dimensions or state zero")
    return archive, data, n, rows


def catalog_text(n, rows):
    return catalog_source(n, rows, BASE, NAMESPACE, SOURCE_SHA) + WRAPPER.format(ns=NAMESPACE)


def generate():
    archive, data, n, rows = load_source()
    cross_check(rows, data["states"])
    modules = BUNDLE / PREFIX
    modules.mkdir(exist_ok=True)
    (modules / "Catalog.lean").write_text(catalog_text(n, rows))
    missing = [name for name in HANDWRITTEN if not (modules / name).is_file()]
    if missing:
        raise FileNotFoundError(f"Missing handwritten modules: {missing}")
    manifest = {
        "scope": ("Literal 2,650-row residual catalog and its conditional bridge. "
                  "ES(8) <= 313 is NOT proved: it follows only from Excludes2650Zero 32."),
        "source_reference": str(SOURCE.relative_to(ROOT)),
        "source_archive_sha256": digest(archive),
        "source_uncompressed_sha256": SOURCE_SHA,
        "research_prefix_reference": str(RESEARCH.relative_to(ROOT)),
        "research_prefix_uncompressed_sha256": RESEARCH_SHA,
        "exporter": "scripts/omission_lean_export.py",
        "exporter_sha256": sha(ROOT / "scripts/omission_lean_export.py"),
        "row_reader_sha256": sha(ROOT / "scripts/omission_row_probe.py"),
        "generator_sha256": sha(Path(__file__)),
        "namespace": NAMESPACE, "module_prefix": PREFIX,
        "states": n, "rows": len(rows), "base": BASE, "chunk_size": 128,
        "row_blocks": BLOCKS,
        "files": {f"{PREFIX}/{p.name}": sha(p) for p in sorted(modules.glob("*.lean"))},
    }
    (BUNDLE / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"rows": len(rows), "states": n, "base": BASE,
                      "catalog_sha256": manifest["files"][f"{PREFIX}/Catalog.lean"]}))


if __name__ == "__main__":
    generate()
