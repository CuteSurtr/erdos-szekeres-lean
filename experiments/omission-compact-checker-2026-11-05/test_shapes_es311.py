#!/usr/bin/env python3
"""Negative tests of shapes_es311.py (6 November 2026, review fix).

  test_shapes_es311.py EXPORT_DIR        (a trial export with a Root, e.g. build/es311/trial/R-sub487209-L1000-B64)

Takes the export's first module and its Root, checks that both pass unchanged, then applies one mutation at
a time and checks that each mutated text is refused. Prints a JSON report; exit 1 if any case is misjudged.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shapes_es311 as S  # noqa: E402


def main():
    ex = Path(sys.argv[1])
    man = json.loads(next(ex.glob("manifest-*.json")).read_text())
    sp = S.side_params(man)
    mm = next(m for m in man["modules"] if m["file"])
    chunk = (ex / mm["file"]).read_text()
    root = (ex / man["root"]["file"]).read_text()
    mod, pre = mm["module"], man["prefix"]
    s0 = mm["subtree_roots"][0][0]
    lines = chunk.split("\n")
    first_def = next(i for i, ln in enumerate(lines) if ln.startswith("noncomputable def b"))
    first_split = next(i for i, ln in enumerate(lines) if ln.startswith("  split_pm "))
    first_chk = next(i for i, ln in enumerate(lines) if ln.startswith("theorem chk"))

    def ins(text, after, new):
        ls = text.split("\n")
        ls[after + 1:after + 1] = new if isinstance(new, list) else [new]
        return "\n".join(ls)

    def rep(text, i, new):
        ls = text.split("\n")
        ls[i] = new
        return "\n".join(ls)

    fake = f"#eval IO.println \"'{mod}.ex{s0}' depends on axioms: [propext]\""
    cases = {
        # the reviewer's synthetic module: an axiom, a proof through it, a faked axiom line, no real #print
        "axiom+eval fake axiom line": rep(ins(chunk, first_def - 1, "axiom bad : False"),
                                          first_split + 1, "  bad.elim").replace(f"#print axioms ex{s0}", fake),
        "eval only": ins(chunk, first_def - 1, fake),
        "skipKernelTC option": ins(chunk, 5, "set_option debug.skipKernelTC true"),
        "other option": ins(chunk, 5, "set_option maxHeartbeats 0"),
        "sorry in a block term": chunk.replace("(natlits% [", "(sorry) (natlits% [", 1),
        "identifier in a block term": chunk.replace("(.leaf ", "(.leaf (foo) ", 1),
        "sorry proof": rep(chunk, first_split, "  sorry"),
        "by sorry chk": rep(chunk, first_chk, lines[first_chk].replace("by decide +kernel", "by sorry")),
        "native_decide": rep(chunk, first_chk, lines[first_chk].replace("by decide +kernel", "by native_decide")),
        "decide without +kernel": rep(chunk, first_chk, lines[first_chk].replace("by decide +kernel", "by decide")),
        "macro": ins(chunk, first_def - 1, "macro \"x\" : term => `(1)"),
        "attribute": ins(chunk, first_def - 1, "attribute [simp] CompactChecker.split_pm"),
        "open ... in": ins(chunk, first_def - 1, "open Nat in"),
        "extra import": ins(chunk, 1, "import CompactChecker.Evil"),
        "block comment": ins(chunk, first_def - 1, "/- x -/"),
        "comment after body": ins(chunk, first_def, "-- late comment"),
        "non-ASCII comment": chunk.replace("-- ES(8)", "-- ES(8) ✓", 1),
        "blank line": ins(chunk, first_def, ""),
        "wrong namespace": chunk.replace(f"namespace {mod}", f"namespace {mod}X", 1),
        "other catalog in chk": rep(chunk, first_chk, lines[first_chk].replace(sp["params"], "fcat62 3131 252 62")),
        "budget changed in ex": chunk.replace(f"FFeas {sp['params']}", f"FFeas {sp['params']}0", 1),
        "homoglyph in statement": chunk.replace("¬ ∃ holes", "¬ ∃ hoIes", 1),
        "CRLF": chunk.replace("\n", "\r\n", 1),
        "missing final end": chunk.replace(f"end {mod}\n", ""),
        "private def": chunk.replace("noncomputable def b", "private noncomputable def b", 1),
    }
    rcases = {
        "two roots": root.replace("#print axioms root", "theorem root : True := trivial\n#print axioms root"),
        "root by sorry": re.sub(r"(theorem root : .*) := \S+\n", r"\1 := sorry\n", root),
        "root import outside the export": "import CompactChecker.Path\n" + root,
        "root eval": root.replace("#print axioms root", "#eval 1\n#print axioms root"),
        "root options": root.replace("set_option profiler true", "set_option debug.skipKernelTC true"),
    }
    out = {"chunk": mm["file"], "root": man["root"]["file"],
           "genuine_chunk_errors": S.check_text(chunk, "chunk", mod, sp),
           "genuine_root_errors": S.check_text(root, "root", pre, sp), "cases": {}}
    good = not out["genuine_chunk_errors"] and not out["genuine_root_errors"]
    for name, text in cases.items():
        assert text != chunk, name
        e = S.check_text(text, "chunk", mod, sp)
        out["cases"][name] = {"refused": bool(e), "first_error": e[0] if e else None}
        good &= bool(e)
    for name, text in rcases.items():
        assert text != root, name
        e = S.check_text(text, "root", pre, sp)
        out["cases"][name] = {"refused": bool(e), "first_error": e[0] if e else None}
        good &= bool(e)
    out["PASS"] = good
    print(json.dumps(out, indent=1, ensure_ascii=False))
    sys.exit(0 if good else 1)


if __name__ == "__main__":
    main()
