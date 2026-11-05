#!/usr/bin/env python3
"""Strict line-shape check of the Lean sources that export_es311.py writes (6 November 2026, review fix).

  shapes_es311.py EXPORT_DIR            (every manifest-*.json there: module files and Root)

Why: drive_es311.py reads a chunk's verdict from the compile log, so a source that printed a fake
"'X' depends on axioms: [...]" line (with #eval), declared an axiom, or switched off a kernel check
(set_option debug.skipKernelTC) could pass the per-chunk check. This check admits only the lines the
exporter writes, in its order, with the side's fixed catalog parameters:

  chunk  import CompactChecker.<Fcat62|Fcat2650> / import CompactChecker.Path / open CompactChecker /
         set_option maxRecDepth 100000 / set_option Elab.async false / set_option linter.all false /
         [set_option profiler true] / namespace <module> / header comments "-- ..." / then blocks
           noncomputable def b<k> : PTree := <term of .split, .leaf, natlits% and .overBudget>
           theorem chk<k> : checkF2 <cat m n budget> <4 numerals> b<k> (pmask (zerosF n) <path>) = true := by decide +kernel
           theorem ex<k> : <FFeas statement> :=
             checkF2_feas <cat m n budget base0> <4 numerals> <cat>_wf b<k> _ chk<k>
         and combinations
           theorem ex<u> : <FFeas statement> :=
             split_pm <cat m n budget> (zerosF n) <path> <numeral> ex<a> ex<b>
         and "#print axioms ex<s>" lines; last line "end <module>".
  Root   import <prefix>.C<digits> ... / the same open and options / namespace <prefix> / comments /
         split_pm combinations whose references may be <prefix>.C<digits>.ex<a> / one
         "theorem root : <FFeas statement> := <reference>" / "#print axioms root" / "end <prefix>".

No other command, identifier, attribute, option, string, or non-ASCII character outside the fixed
statement text can occur. This is a syntactic gate in front of Lean, not a proof: Lean decides
correctness, and E311.Final's own #print axioms (a fixed template, never generated) stays the final
gate on the axioms of the whole chain.
"""
import argparse
import json
import re
import sys
from pathlib import Path

PATH = r"\[(?:\(\d+, [12]\)(?:, \(\d+, [12]\))*)?\]"
NUM = r"(?:0|[1-9]\d*)"
TERM = re.compile(r"(?:\(\.split " + NUM + r" |\(\.leaf " + NUM + r" \(natlits% \[" + NUM + r"(?:, " + NUM
                  + r")*\]\)\)|\.overBudget|\)| )+")
COMMENT = re.compile(r"-- [ -~]*")
CATALOGS = {"CompactChecker.Fcat62": "fcat62", "CompactChecker.Fcat2650": "fcat2650"}


def side_params(man):
    """The fixed parameters of a manifest's side; a catalog outside CATALOGS is refused."""
    if man["catalog"] not in CATALOGS:
        raise ValueError(f"unknown catalog {man['catalog']!r}")
    cat = CATALOGS[man["catalog"]]
    return {"catmod": man["catalog"], "cat": cat, "params": f"{cat} {int(man['rows'])} {int(man['states'])} "
            f"{int(man['budget'])}", "n": int(man["states"]), "base0": int(man["catalog_base"]),
            "prefix": man["prefix"]}


def patterns(sp, kind, name):
    p, n, cat, pre = re.escape(sp["params"]), sp["n"], sp["cat"], re.escape(sp["prefix"])
    feas = rf"¬ ∃ holes : Fin {n} → ℕ, FFeas {p} \(pmask \(zerosF {n}\) {PATH}\) holes"
    ref = rf"(?:{pre}\.C\d+\.)?ex({NUM})" if kind == "root" else rf"ex({NUM})"
    return {
        "def": re.compile(rf"noncomputable def b({NUM}) : PTree := (.*)"),
        "chk": re.compile(rf"theorem chk({NUM}) : checkF2 {p} {NUM} {NUM} {NUM} {NUM} b({NUM}) \(pmask \(zerosF {n}\) "
                          rf"{PATH}\) = true := by decide \+kernel"),
        "ex": re.compile(rf"theorem ex({NUM}) : {feas} :="),
        "feasproof": re.compile(rf"  checkF2_feas {p} {sp['base0']} {NUM} {NUM} {NUM} {NUM} {cat}_wf b({NUM}) _ "
                                rf"chk({NUM})"),
        "splitproof": re.compile(rf"  split_pm {p} \(zerosF {n}\) {PATH} {NUM} {ref} {ref}"),
        "root": re.compile(rf"theorem root : {feas} := {ref}"),
        "print": re.compile(r"#print axioms root" if kind == "root" else rf"#print axioms ex{NUM}"),
    }


def check_text(text, kind, name, sp, max_errors=5):
    """Errors (at most max_errors) of one source text; [] means every line has an admitted shape.
    kind is "chunk" (name = module, e.g. E311R.C00001) or "root" (name = prefix)."""
    errs = []

    def bad(i, why, line):
        errs.append(f"line {i + 1}: {why}: {line[:100]!r}")
        return len(errs) >= max_errors

    if not text.endswith("\n") or "\r" in text or "\t" in text:
        return ["file must end with a newline and contain no CR or tab"]
    lines = text[:-1].split("\n")
    head = ["open CompactChecker", "set_option maxRecDepth 100000", "set_option Elab.async false",
            "set_option linter.all false"]
    i = 0
    if kind == "chunk":
        want = [f"import {sp['catmod']}", "import CompactChecker.Path"]
        if lines[:2] != want:
            return [f"first lines must be {want}"]
        i = 2
    else:
        imp = re.compile(rf"import {re.escape(sp['prefix'])}\.C\d+")
        while i < len(lines) and lines[i].startswith("import "):
            if not imp.fullmatch(lines[i]) and bad(i, "import", lines[i]):
                return errs
            i += 1
        if i == 0:
            return ["a Root imports its chunk modules"]
    if lines[i:i + 4] != head:
        return errs + [f"line {i + 1}: expected the fixed open/option lines"]
    i += 4
    if i < len(lines) and lines[i] == "set_option profiler true":
        i += 1
    if i >= len(lines) or lines[i] != f"namespace {name}":
        return errs + [f"line {i + 1}: expected 'namespace {name}'"]
    i += 1
    while i < len(lines) and lines[i].startswith("--"):
        if not COMMENT.fullmatch(lines[i]) and bad(i, "comment", lines[i]):
            return errs
        i += 1
    if not lines or lines[-1] != f"end {name}":
        return errs + [f"last line must be 'end {name}'"]
    P = patterns(sp, kind, name)
    body, nroot = lines[i:-1], 0
    j = 0
    while j < len(body):
        ln, at = body[j], i + j
        m = P["def"].fullmatch(ln) if kind == "chunk" else None
        if m:
            k = m.group(1)
            if not TERM.fullmatch(m.group(2)):
                if bad(at, "block term", ln):
                    return errs
            mc = P["chk"].fullmatch(body[j + 1]) if j + 1 < len(body) else None
            me = P["ex"].fullmatch(body[j + 2]) if j + 2 < len(body) else None
            mf = P["feasproof"].fullmatch(body[j + 3]) if j + 3 < len(body) else None
            if not (mc and me and mf and mc.group(1) == mc.group(2) == me.group(1) == mf.group(1) == mf.group(2) == k):
                if bad(at, f"block b{k} must be followed by chk{k}, ex{k} and its checkF2_feas proof", ln):
                    return errs
            j += 4
            continue
        m = P["ex"].fullmatch(ln)
        if m:
            if not (j + 1 < len(body) and P["splitproof"].fullmatch(body[j + 1])):
                if bad(at + 1, "a combination ex must be proved by split_pm", body[j + 1] if j + 1 < len(body) else ""):
                    return errs
            j += 2
            continue
        if kind == "root" and P["root"].fullmatch(ln):
            nroot += 1
            j += 1
            continue
        if P["print"].fullmatch(ln):
            j += 1
            continue
        if bad(at, "line of no admitted shape", ln):
            return errs
        j += 1
    if kind == "root" and nroot != 1:
        errs.append(f"a Root states 'theorem root' exactly once (found {nroot})")
    return errs


def check_manifest(ex, man, max_errors=5):
    """[(file, errors)] for every written module file and the Root of one manifest."""
    sp = side_params(man)
    out = []
    for mm in man["modules"]:
        if mm["file"]:
            f = ex / mm["file"]
            out.append((mm["file"], check_text(f.read_text(encoding="utf-8"), "chunk", mm["module"], sp, max_errors)))
    if man.get("root"):
        f = ex / man["root"]["file"]
        out.append((man["root"]["file"], check_text(f.read_text(encoding="utf-8"), "root", man["prefix"], sp,
                                                    max_errors)))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("export", type=Path)
    args = ap.parse_args()
    res, ok = {"export": str(args.export), "manifests": {}}, True
    for mf in sorted(args.export.glob("manifest-*.json")):
        man = json.loads(mf.read_text())
        rows = check_manifest(args.export, man)
        badf = [{"file": f, "errors": e} for f, e in rows if e]
        res["manifests"][mf.name] = {"files": len(rows), "failing": len(badf), "first_failures": badf[:10]}
        ok &= not badf
    res["PASS"] = ok and bool(res["manifests"])
    print(json.dumps(res, indent=1))
    sys.exit(0 if res["PASS"] else 1)


if __name__ == "__main__":
    main()
