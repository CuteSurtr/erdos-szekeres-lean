#!/usr/bin/env python3
"""Build the cube tree of every case from the wave runs and write it as Lean data.

  gen_trees.py R OUTDIR [LEANDIR]

R is a `results` directory (for example /opt/fin/cloud/es7-2026-10-19/results). LEANDIR
defaults to the `V2L` directory next to this script; the data goes to LEANDIR/Trees/.

* A case that Mii-S closed directly (cases.jsonl status UNSAT_VERIFIED), or for which some wave
  directory closed the empty cube (an UNSAT record, cake_lpr exactly `s VERIFIED UNSAT`, with
  cube [] or "direct"/"whole"), gets the tree `leaf` (leaves [[]]).
* Otherwise: every <vm>/<dir> under WAVE1..WAVE4 with a leaves.jsonl belongs to the case whose
  cnf_sha256 its records carry (case_sha256, or cnf_sha256 of a whole record); a directory whose
  records carry no case hash is assigned by its name, as tree_lib.py does. A directory whose
  records name two cases, or a record naming a case other than the directory's, stops the run.
  From the case's directories: the top cubes (top.icnf lines `a ... 0`, in file order, the
  directories in sorted order, duplicates dropped), the SPLIT records (cube, subs) and the
  closed cubes (UNSAT, cake_lpr exactly `s VERIFIED UNSAT`, by exact literal sequence). A SPLIT
  record without "subs" but with "children" (the W34 driver) is read with children as subs.
  Root children: the top cubes that are not parent + sub of a SPLIT record. A node whose
  sequence was closed is a leaf; otherwise its children are (sub, subtree of parent + sub) in
  the recorded order of its SPLIT record. Stops on an open node, on two different SPLIT records
  of one cube, or if a sibling list fails the Python transcription of Mir.coverCheck.
Writes LEANDIR/Trees/*.lean and OUTDIR/status.json (per case: leaves, split nodes, depth) and
OUTDIR/leaves/<case>.icnf (the tree leaves, as CTree.leaves orders them)."""
import collections, hashlib, json, os, re, sys
sys.setrecursionlimit(100000)
PARTIAL = "--partial" in sys.argv
argv = [a for a in sys.argv if a != "--partial"]
R, OUT = argv[1], argv[2]
HERE = os.path.dirname(os.path.abspath(__file__))
LEAN = argv[3] if len(argv) > 3 else os.path.join(HERE, "..", "V2L")
TD = os.path.join(LEAN, "Trees")
os.makedirs(TD, exist_ok=True); os.makedirs(os.path.join(OUT, "leaves"), exist_ok=True)
VER = "s VERIFIED UNSAT"

def fail(msg):
    print("STOP:", msg); sys.exit(1)

cases = [json.loads(l) for l in open(os.path.join(R, "Mii-S/cases.jsonl")) if l.strip()]
byname = {c["case"]: c for c in cases}
sha2case = {c["cnf_sha256"]: c["case"] for c in cases}
names = sorted(byname, key=len, reverse=True)

# caseSpecs order, read from V2L/Data.lean
data = open(os.path.join(HERE, "..", "V2L", "Data.lean")).read()
blk = data[data.index("def caseSpecs"):]
blk = blk[blk.index(":= [") + 4: blk.index("\n\n")]
specs = [(json.loads(a), json.loads(b)) for a, b in re.findall(r"\((\[[0-9, ]*\]), (\[[0-9, ]*\])\)", blk)]
assert len(specs) == 450, len(specs)
spec2case = {(tuple(c["U"]), tuple(c["L"])): c["case"] for c in cases}
order = [spec2case[(tuple(u), tuple(l))] for u, l in specs]
assert len(set(order)) == 450

def byname_case(base):
    for n in names:
        rest = base[len(n):]
        if base == n or (base.startswith(n) and not rest[:1].isdigit() and not (rest[:1] == "-" and rest[1:2].isdigit())):
            return n
    return None
def icnf(path):
    if not os.path.exists(path): return []
    return [tuple(map(int, l.split()[1:-1])) for l in open(path) if l.startswith("a ")]
def aslist(v):
    if isinstance(v, str): v = json.loads(v)
    return v

per = collections.defaultdict(lambda: {"top": [], "topset": set(), "closed": set(), "subs": {}, "whole": [], "dirs": []})
skipped, byname_dirs, children_key = [], [], []
for w in ["WAVE1", "WAVE2", "WAVE3", "WAVE4"]:
    wd = os.path.join(R, w)
    if not os.path.isdir(wd): continue
    for vm in sorted(os.listdir(wd)):
        vp = os.path.join(wd, vm)
        if not os.path.isdir(vp) or vm == "tasks": continue
        for d in sorted(os.listdir(vp)):
            dp = os.path.join(vp, d)
            rel = os.path.join(w, vm, d)
            if not os.path.isdir(dp): continue
            lj = os.path.join(dp, "leaves.jsonl")
            if not os.path.exists(lj): skipped.append(rel); continue
            recs = []
            for l in open(lj):
                l = l.strip()
                if l.startswith("{"):
                    try: recs.append(json.loads(l))
                    except ValueError: pass
            hs = {sha2case[h] for r in recs for h in (r.get("case_sha256"), r.get("cnf_sha256")) if h in sha2case}
            if len(hs) > 1: fail("%s names cases %s" % (rel, sorted(hs)))
            if hs: case = hs.pop()
            else:
                case = byname_case(d)
                if case is None: skipped.append(rel); continue
                byname_dirs.append(rel)
            for r in recs:
                if r.get("top") and "case_sha256" in r and r["case_sha256"] != byname[case]["cnf_sha256"]:
                    fail("%s: top record hash is not %s's" % (rel, case))
            P = per[case]; P["dirs"].append(rel)
            for t in icnf(os.path.join(dp, "top.icnf")):
                if t not in P["topset"]: P["topset"].add(t); P["top"].append(t)
            for r in recs:
                st = r.get("status")
                if st == "UNSAT" and r.get("cake_lpr") == VER:
                    if r.get("direct") or r.get("whole"):
                        h = r.get("case_sha256", r.get("cnf_sha256"))
                        if h is not None and h != byname[case]["cnf_sha256"]: fail("%s: whole record of another case" % rel)
                        c = aslist(r.get("cube", []))
                        if c: fail("%s: whole record with a nonempty cube" % rel)
                        P["whole"].append(rel); P["closed"].add(()); continue
                    c = aslist(r.get("cube"))
                    if not isinstance(c, list): continue
                    if not c: P["whole"].append(rel)
                    P["closed"].add(tuple(c))
                elif st == "SPLIT" and ("subs" in r or "children" in r):
                    # W34's driver names the list "children" (relative cubes, as "subs"; the
                    # leaves under it are recorded as cube + child); counted in status.json
                    c = aslist(r.get("cube"))
                    subs = tuple(tuple(s) for s in aslist(r["subs"] if "subs" in r else r["children"]))
                    c = tuple(c)
                    if "subs" not in r:
                        children_key.append(rel)
                        if any(s[:len(c)] == c for s in subs): fail("%s: SPLIT children of %s look absolute" % (rel, list(c)))
                    if c in P["subs"] and P["subs"][c] != subs: fail("%s: two SPLIT records of %s differ" % (rel, list(c)))
                    P["subs"].setdefault(c, subs)

class OpenCube(Exception): pass
def restrict(z, cs): return [[l for l in c if l != z] for c in cs if -z not in c]
def cover(cs):
    if any(len(c) == 0 for c in cs): return True
    if not cs: return False
    z = cs[0][0]
    return z != 0 and cover(restrict(z, cs)) and cover(restrict(-z, cs))

# tree: None for leaf, else list of (sub, tree)
def build(P, c, depth, stats):
    stats["depth"] = max(stats["depth"], depth)
    if c in P["closed"]: stats["leaves"] += 1; return None
    if c not in P["subs"]:
        if PARTIAL: raise OpenCube(list(c))
        fail("open cube %s" % list(c))
    subs = P["subs"][c]
    if not cover([list(s) for s in subs]): fail("subs of %s are not a cover" % list(c))
    stats["split"] += 1
    return [(s, build(P, c + s, depth + 1, stats)) for s in subs]
def leaves(t):
    if t is None: return [()]
    return [s + l for s, k in t for l in leaves(k)]

def enc(z):
    assert z != 0
    d = 2 * z if z > 0 else 2 * (-z) + 1
    assert d < 1 << 20
    return d
def pk(c): return "%d %s" % (len(c), ("0x" + "".join("%05x" % enc(z) for z in c)) if c else "0")
def term(t, ind):
    """Lean list of children."""
    items = []
    for s, k in t:
        if k is None: items.append("lf %s" % pk(s))
        else: items.append("nd %s %s" % (pk(s), term(k, ind + 1)))
    return "[" + ", ".join(items) + "]"
def natlist(xs): return "[" + ", ".join(map(str, xs)) + "]"

rows, modules = [], []
for k, name in enumerate(order):
    c = byname[name]; P = per.get(name)
    row = {"k": k, "case": name, "U": c["U"], "L": c["L"]}
    if c["status"] == "UNSAT_VERIFIED":
        row.update(tree="leaf", source="Mii-S direct", leaves=1, split=0, depth=0); rows.append(row); continue
    if P is None: fail("%s: no wave directory" % name)
    row["dirs"] = P["dirs"]
    if () in P["closed"]:
        row.update(tree="leaf", source="wave empty cube", whole_dirs=sorted(set(P["whole"])), leaves=1, split=0, depth=0)
        rows.append(row); continue
    children = {p + s for p, subs in P["subs"].items() for s in subs}
    roots = [t for t in P["top"] if t not in children]
    if not roots: fail("%s: no root cubes" % name)
    if not cover([list(r) for r in roots]): fail("%s: root cubes are not a cover" % name)
    stats = collections.Counter(depth=0)
    try: tree = [(r, build(P, r, 1, stats)) for r in roots]
    except OpenCube as e:
        row.update(tree="open", open_cube=e.args[0], leaves=0, split=0, depth=0); rows.append(row); continue
    lv = leaves(tree)
    assert len(lv) == stats["leaves"] and all(l in P["closed"] for l in lv)
    if len(set(lv)) != len(lv): fail("%s: repeated leaf" % name)
    with open(os.path.join(OUT, "leaves", name + ".icnf"), "w") as f:
        f.writelines("a " + " ".join(map(str, l)) + " 0\n" for l in lv)
    row.update(tree="node", roots=len(roots), leaves=stats["leaves"], split=stats["split"],
               depth=stats["depth"], closed_records=len(P["closed"]),
               closed_unused=len(P["closed"] - set(lv)))
    rows.append(row)
    # data module: one def per sibling list (node), numbered in preorder (CTree.sibLists order)
    nodes = []          # preorder: list of items (strings)
    def emit(t):
        j = len(nodes); nodes.append(None)
        items = []
        for sub, kid in t:
            if kid is None: items.append("lf %s" % pk(sub))
            else: items.append("nd %s n%03d_%d" % (pk(sub), k, emit(kid)))
        nodes[j] = items
        return j
    emit(tree)
    defs = ["def n%03d_%d : List (List Int × CTree) := [%s]\n" % (k, j, ", ".join(nodes[j])) for j in reversed(range(len(nodes)))]
    row["nodes"] = len(nodes)
    mod = "V2L.Trees.T%03d" % k; modules.append((k, mod, len(nodes)))
    src = ("import V2L.TreeData\n\n/-! Cube tree of case %s (U = %s, L = %s), generated by `scripts/gen_trees.py`;\n"
           "do not edit by hand. %d root cubes, %d leaves, %d split nodes, depth %d. `n%03d_j` is the\n"
           "j-th sibling list in preorder (`n%03d_0` the root cubes). -/\n\n"
           "namespace V2L.Trees\n\nset_option maxRecDepth 100000\n\n%s\n"
           "/-- The cube tree of case %s. -/\ndef tree%03d : CTree := .node n%03d_0\n\nend V2L.Trees\n") % (
        name, c["U"], c["L"], len(roots), stats["leaves"], stats["split"], stats["depth"], k, k,
        "".join(defs), name, k, k)
    open(os.path.join(TD, "T%03d.lean" % k), "w").write(src)

# table, checks
imp = "".join("import %s\n" % m for _, m, _ in modules)
ents = []
treek = {k: n for k, _, n in modules}
for r in rows:
    ents.append("  ((%s, %s), %s)" % (natlist(r["U"]), natlist(r["L"]), ("Trees.tree%03d" % r["k"]) if r["k"] in treek else ".node []" if r["tree"] == "open" else ".leaf"))
open(os.path.join(TD, "Table.lean"), "w").write(
    "import V2L.TreeData\n%s\n/-! The table of the 450 case trees (generated by `scripts/gen_trees.py`). -/\n\nnamespace V2L\n\n"
    "/-- Per case `(U, L)`, in `caseSpecs` order, its cube tree. -/\ndef treeTable : List ((List Nat × List Nat) × CTree) := [\n%s]\n\n"
    "/-- The cube tree of a case (`.node []`, which fails `check`, for a case not in the table). -/\n"
    "def treeOf (s : List Nat × List Nat) : CTree :=\n  match treeTable.find? (·.1 == s) with\n  | some p => p.2\n  | none => .node []\n\nend V2L\n"
    % (imp, ",\n".join(ents)))
def spec(r): return "(%s, %s)" % (natlist(r["U"]), natlist(r["L"]))
CH = 10   # sibling lists per kernel-check module
nodemods = {}
for r in rows:
    k = r["k"]
    if k not in treek: continue
    n = treek[k]; nodemods[k] = []
    for c0 in range(0, n, CH):
        m = "N%03d_%d" % (k, c0 // CH); nodemods[k].append(m)
        open(os.path.join(TD, m + ".lean"), "w").write(
            "import V2L.Trees.T%03d\n\n/-! Kernel checks of sibling lists %d..%d of case %s (generated by `scripts/gen_trees.py`). -/\n\n"
            "namespace V2L.Trees\n\nopen Mir\n\nset_option maxHeartbeats 0\n\n" % (k, c0, min(n, c0 + CH) - 1, r["case"])
            + "".join("theorem c%03d_%d : coverCheck (n%03d_%d.map Prod.fst) = true := by decide +kernel\n" % (k, j, k, j) for j in range(c0, min(n, c0 + CH)))
            + "\nend V2L.Trees\n")
    lines = ["  have a%d : AllOf CoverOk ([] : List (List (List Int))) := AllOf.nil" % n]
    for j in reversed(range(n)):
        lines.append("  have a%d := AllOf.cons (P := CoverOk) (a := n%03d_%d.map Prod.fst) c%03d_%d a%d" % (j, k, j, k, j, j + 1))
    open(os.path.join(TD, "Check%03d.lean" % k), "w").write(
        "import V2L.Trees.Table\n" + "".join("import V2L.Trees.%s\n" % m for m in nodemods[k]) +
        "\n/-! The tree check of case %s from its %d per-sibling-list kernel checks (generated by\n`scripts/gen_trees.py`). -/\n\nnamespace V2L.Trees\n\nopen Mir\n\n" % (r["case"], n)
        + "set_option maxRecDepth 100000 in\ntheorem sib%03d : tree%03d.sibLists = [%s] := rfl\n\n" % (k, k, ", ".join("n%03d_%d.map Prod.fst" % (k, j) for j in range(n)))
        + "set_option maxRecDepth 100000 in\ntheorem check%03d : (treeOf %s).check = true := by\n" % (k, spec(r))
        + "  have e : treeOf %s = tree%03d := rfl\n" % (spec(r), k)
        + "\n".join(lines) + "\n  rw [e]\n  exact CTree.check_of_sibLists (by rw [sib%03d]; exact a0.forall)\n\nend V2L.Trees\n" % k)
open(os.path.join(TD, "CheckLeaf.lean"), "w").write(
    "import V2L.Trees.Table\n\n/-! Kernel checks of the cases whose tree is `leaf` (generated by `scripts/gen_trees.py`). -/\n\nnamespace V2L.Trees\n\n"
    + "".join("/-- %s -/\ntheorem check%03d : (treeOf %s).check = true := by decide +kernel\n" % (r["case"], r["k"], spec(r)) for r in rows if r["k"] not in treek and r["tree"] != "open")
    + "\nend V2L.Trees\n")
# build the proof as a flat sequence of `have`s to keep the term shallow
lines = ["  have h450 : AllOf TreeOk ([] : List (List Nat × List Nat)) := AllOf.nil"]
for r in reversed(rows):
    lines.append("  have h%03d := AllOf.cons (P := TreeOk) Trees.check%03d h%03d" % (r["k"], r["k"], r["k"] + 1 if r["k"] < 449 else 450))
if PARTIAL: print("partial run: open cases", [r["case"] for r in rows if r["tree"] == "open"]); open(os.path.join(TD, "Checks.lean"), "w").write("-- partial run, not written\n") if False else None
else: open(os.path.join(TD, "Checks.lean"), "w").write(
    "import V2L.Trees.CheckLeaf\n" + "".join("import V2L.Trees.Check%03d\n" % k for k in sorted(treek)) +
    "\n/-! All 450 tree checks, combined from the per-case kernel checks without re-evaluation\n(generated by `scripts/gen_trees.py`). -/\n\nnamespace V2L\n\n"
    "/-- A case whose tree checks. -/\ndef TreeOk (s : List Nat × List Nat) : Prop := (treeOf s).check = true\n\n"
    "set_option maxRecDepth 100000 in\ntheorem caseSpecs_treeOk : AllOf TreeOk caseSpecs := by\n" + "\n".join(lines) + "\n  exact h000\n\n"
    "/-- **The 450 case trees pass `CTree.check`.** -/\ntheorem treeOf_check : ∀ p ∈ caseTable, (treeOf p.1).check = true := fun p hp =>\n"
    "  caseSpecs_treeOk.forall p.1 (List.of_mem_zip hp).1\n\nend V2L\n")
summary = {"cases": len(rows), "tree_node": len(treek), "tree_leaf": sum(r["tree"] == "leaf" for r in rows), "open": [r["case"] for r in rows if r["tree"] == "open"],
           "leaf_direct": sum(r.get("source") == "Mii-S direct" for r in rows),
           "leaf_wave_empty": sum(r.get("source") == "wave empty cube" for r in rows),
           "leaves_total": sum(r["leaves"] for r in rows),
           "leaves_in_trees": sum(r["leaves"] for r in rows if r["tree"] == "node"),
           "split_nodes": sum(r["split"] for r in rows),
           "max_depth": max(r["depth"] for r in rows),
           "split_records_with_children_key": children_key, "dirs_by_name": byname_dirs, "dirs_skipped": skipped}
json.dump({"R": os.path.abspath(R), "summary": summary, "rows": rows}, open(os.path.join(OUT, "status.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in summary.items() if not k.startswith("dirs")}), "dirs_by_name", len(byname_dirs), "skipped", len(skipped))
