#!/usr/bin/env python3
"""s3520-gate (22 Nov 2026): the unit-level (context-level) sub-root module of one exported unit. NOTHING HERE PROVES
ANYTHING: Lean checks every split_pm step (both children must be stated with the right literal path).

  subroot.py OUT UNIT       (OUT = an export directory of slice_export_v3.py; unit UNIT must be exported)

Writes OUT/src/RS<TAG>/U<uuuu>.lean, module RS<TAG>.U<uuuu>: it imports the unit's chunk modules, joins them through
the unit's internal skeleton exactly as res-slices-fv/tools/root_slice.py does (its unit_root, copied below; theorems
ex<(u+1)*10^12 + node>), and states

  RS<TAG>.U<uuuu>.root : ¬ ∃ holes : Fin 154 → ℕ, FFeas fcatS<TAG> <rows> 154 <B> (pmask (zerosF 154) P) holes

with P = skeleton.json tops[u].path (asserted equal to the manifest's base path). The text must pass
shapes_es311.check_text (kind "root", name RS<TAG>.U<uuuu>) before it is written."""
import json
import sys
from pathlib import Path

X = Path("/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-compact-checker-2026-11-05")
sys.path.insert(0, str(X))
import shapes_es311  # noqa: E402
from export_es311 import OPTS, lean_path  # noqa: E402

STRIDE = 10 ** 12


def main():
    out, u = Path(sys.argv[1]), int(sys.argv[2])
    sk = json.loads((out / "skeleton.json").read_text())
    tag, B, m = sk["tag"], sk["budget"], sk["rows"]
    prefix, params, m0 = f"RS{tag}", f"fcatS{tag} {m} 154 {B}", "(zerosF 154)"
    name = f"{prefix}.U{u:04d}"
    top = next(t for t in sk["tops"] if t["unit"] == u)
    man = json.loads((out / "ctx" / f"ctx-{u:04d}.json").read_text())
    assert [list(x) for x in man["base_path"]] == [list(x) for x in top["path"]], u
    assert man["stats"]["leaves"] == top["leaves"] and man["stats"]["lean_test_failures"] == 0, u

    def feas(p):
        return f"¬ ∃ holes : Fin 154 → ℕ, FFeas {params} (pmask {m0} {lean_path(p)}) holes"

    imports = [mm["module"] for mm in man["modules"]]
    lines = [*(f"import {x}" for x in imports), "open CompactChecker", "set_option maxRecDepth 100000", *OPTS,
             f"namespace {name}",
             f"-- s3520-gate (22 Nov 2026): unit {u} of the residual slice check B={B} ({top['leaves']} leaves, "
             f"{len(imports)} modules), joined through its skeleton; Lean checks each step"]

    def unit_root(u, man):                               # = root_slice.py unit_root
        base = [tuple(x) for x in man["base_path"]]
        where = {s: mm["module"] for mm in man["modules"] for s, _ in mm["subtree_roots"]}
        if not man["skeleton"]:
            assert list(where) == [0], (u, where)
            return f"{where[0]}.ex0"
        sk_ = {e["u"]: e for e in man["skeleton"]}
        parent = {}
        for e in man["skeleton"]:
            parent[e["zero"]] = (e["u"], 2)
            parent[e["one"]] = (e["u"], 1)

        def path(x):
            p = []
            while x != 0:
                y, d = parent[x]
                p.append((sk_[y]["vertex"], d))
                x = y
            return p + base

        def ref(x):
            return f"{where[x]}.ex{x}" if x in where else f"ex{(u + 1) * STRIDE + x}"

        for x in sorted(sk_, reverse=True):              # preorder ids: children have larger ids
            e = sk_[x]
            lines.append(f"theorem ex{(u + 1) * STRIDE + x} : {feas(path(x))} :=")
            lines.append(f"  split_pm {params} {m0} {lean_path(path(x))} {e['vertex']} {ref(e['zero'])} {ref(e['one'])}")
        return f"ex{(u + 1) * STRIDE}"

    lines.append(f"theorem root : {feas([tuple(x) for x in top['path']])} := {unit_root(u, man)}")
    lines += ["#print axioms root", f"end {name}"]
    text = "\n".join(lines) + "\n"
    shapes_es311.CATALOGS[f"RS.Cat{tag}"] = f"fcatS{tag}"
    sp = shapes_es311.side_params({"catalog": f"RS.Cat{tag}", "rows": m, "states": 154, "budget": B,
                                   "catalog_base": 131072, "prefix": prefix})
    errs = shapes_es311.check_text(text, "root", name, sp)
    assert not errs, errs
    path = out / "src" / prefix / f"U{u:04d}.lean"
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_text(text)
    tmp.replace(path)
    print(json.dumps({"module": name, "imports": len(imports), "lines": len(lines), "path": top["path"],
                      "leaves": top["leaves"]}))


if __name__ == "__main__":
    main()
