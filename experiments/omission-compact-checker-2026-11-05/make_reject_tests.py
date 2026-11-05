#!/usr/bin/env python3
"""Write CompactChecker/Chunk733G4Reject.lean: passing rejection tests for checkF2.

Every test is a theorem `checkF2 ... = false := by decide +kernel` (or a companion
`... = true`) that builds only if the kernel computes that value, so a test never
needs a failing build. The data is leaf node 751 of chunk 733 of tree-62 (the leaf
of least full-load margin in the chunk, 3) with its own context mask, in the
4-entries-per-word encoding of Chunk733G4. Each mutation targets one part of
checkF2 that checkF does not have:

  weight   one weight +1 (as Chunk733G4Corrupt.lean, margin 3 -> 0);
  ovf      c extra entries (row r0, weight K-1), c = 64 (the least count at which
           the test without the guard accepts) and c = 68 (the review's mutation):
           the demand sum passes the leaf base, so the guard `Q / base^n < base`
           must reject; `leafNoGuard` (the test without that guard) accepts;
  oor      the heaviest entry moved to row 4000 (>= m, < 2^12);
  mbound   the genuine leaf checked with m = 3064, so `r < m` drops row 3064;
  drop     the last word (4 entries) removed;
  long     mask ++ [2] (length 253): treeF2 accepts, checkF2's length check rejects;
  short    the weight mutation with mask.take 234: treeF2 accepts a leaf of
           full-load margin 0, checkF2's length check rejects;
  demand0  a one-row catalog whose row has demand 0: checkF2 rejects; the variant
           that keeps demand-0 rows accepts, and its conclusion is false (proved).

All margins and sums in the report and the Lean comments are exact computations
(export_fast2.full_load_margin and a transcription of the Lean tests).
Usage: python3 make_reject_tests.py <balanced-v2-source.json> <tree-62.json.xz> --out .
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import export_fast2 as ex  # noqa: E402

CHUNK, LEAF, PER_WORD = 733, 751, 4


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", type=Path)
    ap.add_argument("tree", type=Path)
    ap.add_argument("--out", type=Path, required=True, help="directory containing CompactChecker/")
    args = ap.parse_args()

    data, cert = ex.read_json(args.source), ex.read_json(args.tree)
    assert cert["source_sha256"] == ex.sha256(args.source), "tree/source hash mismatch"
    n, rows = ex.read_rows(data)
    m = len(rows)
    nodes, budget, root = cert["nodes"], cert["hole_budget"], cert["root"]
    counts, ctx, order = ex.annotate(nodes, root)
    K, k = 1 << 17, PER_WORD
    J = K << m.bit_length()
    base = 1 << 23  # the leaf base of Chunk733G4 (export_fast2 default for tree-62)
    BN = base ** n
    assert LEAF in ex.leaves_under(CHUNK, nodes) and nodes[LEAF]["type"] == "weighted"
    mi, oc = ctx[LEAF]
    cap = nodes[LEAF]["capacity"]
    mask = [0] * n
    for i in mi:
        mask[i] = 1
    for i in oc:
        mask[i] = 2
    ent = ex.normalize(rows, nodes[LEAF], mi)

    def margin(es, mm=m):
        kept = [(r, w) for r, w in es if r < mm and rows[r][1] > 0]
        return ex.full_load_margin(n, rows, budget, mi, oc, cap, kept)

    def words(es):
        return ex.pack_words([r * K + w for r, w in es], k, J)

    def lean_tree_leaf(mk, ws, mm=m, guard=True):
        """Transcription of Fast2.leafF2 (guard=False: leafNoGuard), reading the mask list as given."""
        Q = 0
        for y in ws:
            for _ in range(k):
                e, y = y % J, y // J
                r, w = e // K, e % K
                if r < mm and rows[r][1] > 0:
                    Q += w * (sum(base ** i for i in rows[r][0]) + BN * rows[r][1])
        big = (n + 1) * base
        X, p = 0, Q
        for v in mk:
            c, p = p % base, p // base
            X += c + big if v == 1 else 0 if v == 2 else max(0, c - cap)
        T = Q // BN
        ok = cap * max(0, budget - X // big) + X % big < T
        return (1 < base and T < base and ok) if guard else ok

    def check(mk, ws, mm=m):
        return len(mk) == n and lean_tree_leaf(mk, ws, mm)

    rep = {"chunk": CHUNK, "leaf": LEAF, "capacity": cap, "entries": len(ent), "missing": sorted(mi),
           "occupied": sorted(oc), "leaf_base": base, "K": K, "J": J, "per_word": k, "tests": {}}
    T = rep["tests"]
    ws0 = words(ent)
    T["genuine"] = {"margin": margin(ent), "checkF2": check(mask, ws0),
                    "demand_sum": sum(w * rows[r][1] for r, w in ent)}
    assert T["genuine"]["checkF2"] and T["genuine"]["margin"] == 3

    # weight: first entry whose +1 takes the margin to <= 0 (export_fast2 --corrupt picks the same)
    e = next(e for e in range(len(ent)) if margin(ent[:e] + [(ent[e][0], ent[e][1] + 1)] + ent[e + 1:]) <= 0)
    ent_w = ent[:e] + [(ent[e][0], ent[e][1] + 1)] + ent[e + 1:]
    T["weight"] = {"entry": e, "row": ent[e][0], "old_weight": ent[e][1], "new_weight": ent[e][1] + 1,
                   "margin": margin(ent_w), "checkF2": check(mask, words(ent_w))}

    # ovf: least count of (r0, K-1) entries at which the unguarded test accepts
    r0 = next(r for r in range(m) if rows[r][1] == 1 and not set(rows[r][0]) & set(mi)
              and len(set(rows[r][0]) - set(oc) - set(mi)) >= 3)
    cnt = next(c for c in range(1, 400) if lean_tree_leaf(mask, words(ent + [(r0, K - 1)] * c), guard=False))
    ovf_ent = {}
    for name, c in (("ovf", cnt), ("ovf68", 68)):
        ovf_ent[name] = ent + [(r0, K - 1)] * c
        D = sum(w * rows[r][1] for r, w in ovf_ent[name])
        T[name] = {"row": r0, "support": rows[r0][0], "demand": rows[r0][1], "count": c, "weight": K - 1,
                   "demand_sum": D, "demand_sum_ge_base": D >= base, "margin": margin(ovf_ent[name]),
                   "checkF2": check(mask, words(ovf_ent[name])),
                   "no_guard_test": lean_tree_leaf(mask, words(ovf_ent[name]), guard=False)}

    # oor: heaviest entry (weight * demand) moved to row 4000
    h = max(range(len(ent)), key=lambda i: ent[i][1] * rows[ent[i][0]][1])
    ent_r = ent[:h] + [(4000, ent[h][1])] + ent[h + 1:]
    T["oor"] = {"entry": h, "row": ent[h][0], "weight": ent[h][1], "new_row": 4000,
                "margin_without_entry": margin(ent_r), "checkF2": check(mask, words(ent_r))}

    # mbound: m lowered to the largest row used by the leaf
    mb = max(r for r, _ in ent)
    T["mbound"] = {"m": mb, "row_dropped": mb, "row_demand": rows[mb][1],
                   "entries_of_row": sum(1 for r, _ in ent if r == mb),
                   "margin_without_row": margin(ent, mb), "checkF2": check(mask, ws0, mb)}

    # drop: last word removed
    ws_d = ws0[:-1]
    ent_d = ent[: k * len(ws_d)]
    T["drop"] = {"words": len(ws0), "entries_removed": len(ent) - len(ent_d), "margin": margin(ent_d),
                 "checkF2": check(mask, ws_d)}

    # long / short masks
    T["long"] = {"mask_length": n + 1, "treeF2": lean_tree_leaf(mask + [2], ws0),
                 "checkF2": check(mask + [2], ws0)}
    L = next(L for L in range(n, 0, -1) if lean_tree_leaf(mask[:L], words(ent_w)))
    T["short"] = {"mask_length": L, "dropped_values": sorted(set(mask[L:])), "leaf": "weight mutation",
                  "margin_full_mask": margin(ent_w), "treeF2": lean_tree_leaf(mask[:L], words(ent_w)),
                  "checkF2": check(mask[:L], words(ent_w))}

    for name, t in T.items():
        if name != "genuine":
            assert t["checkF2"] is False, name
    assert T["ovf"]["no_guard_test"] and T["ovf68"]["no_guard_test"] and T["long"]["treeF2"] and T["short"]["treeF2"]

    nl = lambda ws: f"natlits% [{', '.join(map(str, ws))}]"
    P = f"fcat62 {m} {n} {budget} {base} {K} {J} {k}"
    Pm = f"fcat62 {mb} {n} {budget} {base} {K} {J} {k}"
    W, O, O8, R, Dr, S = T["weight"], T["ovf"], T["ovf68"], T["oor"], T["drop"], T["short"]
    lean = f"""import CompactChecker.Fcat62
import CompactChecker.Fast2
import CompactChecker.Chunk733G4
/-!
# Rejection tests for `checkF2` (6 November 2026)

Written by `make_reject_tests.py`; do not edit by hand. Each theorem holds only
if the kernel computes the stated value, so every test here is a passing build.
Data: leaf node {LEAF} of chunk {CHUNK} of `tree-62` (least full-load margin in the
chunk: 3), capacity {cap}, {len(ent)} entries, {k} per word, with the leaf's own
context mask. Margins in the comments are exact computations
(`export_fast2.full_load_margin`); see `export-fast2-64-reject.json`.
-/
open CompactChecker
set_option maxRecDepth 100000
set_option profiler true
namespace CompactChecker.Chunk733G4Reject

/-- Context mask of leaf node {LEAF} (missing {sorted(mi)}, occupied {sorted(oc)}). -/
noncomputable def mask{LEAF} : List ℕ := [{', '.join(map(str, mask))}]
/-- The genuine words of leaf {LEAF}. -/
noncomputable def ws : List ℕ := {nl(ws0)}
/-- Entry {W['entry']} (row {W['row']}): weight {W['old_weight']} → {W['new_weight']}; margin 3 → {W['margin']}. -/
noncomputable def wsWeight : List ℕ := {nl(words(ent_w))}
/-- {O['count']} extra entries (row {O['row']}, weight {O['weight']}); demand sum {O['demand_sum']} ≥ base {base};
margin {O['margin']}. {O['count']} is the least count at which `leafNoGuard` accepts. -/
noncomputable def wsOvf : List ℕ := {nl(words(ovf_ent['ovf']))}
/-- The review's mutation: {O8['count']} extra entries (row {O8['row']}, weight {O8['weight']}); demand sum
{O8['demand_sum']}; margin {O8['margin']}. -/
noncomputable def wsOvf68 : List ℕ := {nl(words(ovf_ent['ovf68']))}
/-- Entry {R['entry']} (row {R['row']}, weight {R['weight']}) moved to row 4000; margin without it {R['margin_without_entry']}. -/
noncomputable def wsOor : List ℕ := {nl(words(ent_r))}
/-- The last word ({Dr['entries_removed']} entries) removed; margin {Dr['margin']}. -/
noncomputable def wsDrop : List ℕ := {nl(ws_d)}

/-- `leafF2` without its guards `1 < base` and `Q / base ^ n < base`. -/
noncomputable def leafNoGuard (c : FCat) (m n budget base K J k cap : ℕ) (mask ws : List ℕ) : Bool :=
  Nat.blt
    (Nat.add (Nat.mul cap (Nat.sub budget (Nat.div (colLoop base cap (bigF n base) mask
        (leafQ (rowVal c m base (Nat.pow base n)) K J k ws)) (bigF n base))))
      (Nat.mod (colLoop base cap (bigF n base) mask
        (leafQ (rowVal c m base (Nat.pow base n)) K J k ws)) (bigF n base)))
    (Nat.div (leafQ (rowVal c m base (Nat.pow base n)) K J k ws) (Nat.pow base n))

/-- Positive control: the genuine leaf passes. -/
theorem genuine_accepts : checkF2 {P} (.leaf {cap} ws) mask{LEAF} = true := by decide +kernel

/-- One weight +1 (the mutation of `Chunk733G4Corrupt.lean`). -/
theorem weight_rejects : checkF2 {P} (.leaf {cap} wsWeight) mask{LEAF} = false := by decide +kernel

/-- Overflow: the guard `Q / base ^ n < base` rejects ... -/
theorem ovf_rejects : checkF2 {P} (.leaf {cap} wsOvf) mask{LEAF} = false := by decide +kernel
/-- ... and the same test without the guard accepts, although the margin is {O['margin']}. -/
theorem ovf_noGuard_accepts : leafNoGuard {P} {cap} mask{LEAF} wsOvf = true := by decide +kernel
theorem ovf68_rejects : checkF2 {P} (.leaf {cap} wsOvf68) mask{LEAF} = false := by decide +kernel
theorem ovf68_noGuard_accepts : leafNoGuard {P} {cap} mask{LEAF} wsOvf68 = true := by decide +kernel

/-- A row index `≥ m` (4000) contributes nothing. -/
theorem oor_rejects : checkF2 {P} (.leaf {cap} wsOor) mask{LEAF} = false := by decide +kernel
/-- With `m = {mb}`, the bound `r < m` drops row {mb} (demand {T['mbound']['row_demand']}), which exists in the catalog. -/
theorem mbound_row_dropped : rowVal fcat62 {mb} {base} (Nat.pow {base} {n}) {mb} = 0 := by decide +kernel
theorem mbound_row_kept : Nat.blt 0 (rowVal fcat62 {m} {base} (Nat.pow {base} {n}) {mb}) = true := by
  decide +kernel
theorem mbound_rejects : checkF2 {Pm} (.leaf {cap} ws) mask{LEAF} = false := by decide +kernel

/-- Truncated leaf. -/
theorem drop_rejects : checkF2 {P} (.leaf {cap} wsDrop) mask{LEAF} = false := by decide +kernel

/-- Mask of length {n + 1}: only the length check rejects. -/
theorem long_tree_accepts : treeF2 {P} (.leaf {cap} ws) (mask{LEAF} ++ [2]) = true := by decide +kernel
theorem long_rejects : checkF2 {P} (.leaf {cap} ws) (mask{LEAF} ++ [2]) = false := by decide +kernel
/-- The same on the whole 64-leaf block of `Chunk733G4`. -/
theorem block_long_tree_accepts :
    treeF2 {P} Chunk733G4.b733 (Chunk733G4.mask733 ++ [2]) = true := by decide +kernel
theorem block_long_rejects :
    checkF2 {P} Chunk733G4.b733 (Chunk733G4.mask733 ++ [2]) = false := by decide +kernel

/-- Mask of length {S['mask_length']} (dropped values {S['dropped_values']}): without the length check the leaf of
`weight_rejects` (full-load margin {S['margin_full_mask']}) would pass. -/
theorem short_tree_accepts :
    treeF2 {P} (.leaf {cap} wsWeight) (mask{LEAF}.take {S['mask_length']}) = true := by decide +kernel
theorem short_rejects :
    checkF2 {P} (.leaf {cap} wsWeight) (mask{LEAF}.take {S['mask_length']}) = false := by decide +kernel

/-! ### Demand-0 rows

A one-state catalog whose only row (support `[0]`, code `1`) has demand `0`, leaf
base `2`, budget `0`, one entry of weight `2`. `checkF2` drops the row and rejects.
The variant that keeps demand-0 rows (`rowValKeep0`) accepts, although the
exclusion statement it would certify is false (`cat0_feasible`). -/

noncomputable def cat0 : FCat := .row [0] 0 1

theorem demand0_rejects : checkF2 cat0 1 1 0 2 4 16 1 (.leaf 0 [2]) [0] = false := by decide +kernel

/-- `rowVal` without the test `0 < demand`. -/
noncomputable def rowValKeep0 (c : FCat) (m base BN r : ℕ) : ℕ :=
  Bool.rec 0 (c.getWith (fun s d => Nat.add (codeR base s) (Nat.mul BN d)) r) (Nat.blt r m)

theorem demand0_keep_accepts :
    leafTest 0 2 (Nat.pow 2 1) (bigF 1 2) 0 (leafQ (rowValKeep0 cat0 1 2 (Nat.pow 2 1)) 4 16 1 [2])
      (colLoop 2 0 (bigF 1 2) [0] (leafQ (rowValKeep0 cat0 1 2 (Nat.pow 2 1)) 4 16 1 [2])) = true := by
  decide +kernel

theorem cat0_feasible :
    ∃ holes : Fin 1 → ℕ, (∀ i, holes i ≤ 1) ∧
      (∀ r : Fin 1, cat0.dem r.val ≤ ∑ i ∈ fsupp cat0 1 r.val, holes i) ∧
      (∑ i, holes i) ≤ 0 ∧
      (∀ i ∈ mset 1 [0] 1, holes i = 1) ∧ (∀ i ∈ mset 1 [0] 2, holes i = 0) := by
  refine ⟨fun _ => 0, fun _ => Nat.zero_le _, fun _ => Nat.zero_le _, by simp, ?_, fun _ _ => rfl⟩
  intro i hi
  simp [mset] at hi

#print axioms genuine_accepts
#print axioms weight_rejects
#print axioms ovf_rejects
#print axioms ovf_noGuard_accepts
#print axioms ovf68_rejects
#print axioms ovf68_noGuard_accepts
#print axioms oor_rejects
#print axioms mbound_row_dropped
#print axioms mbound_row_kept
#print axioms mbound_rejects
#print axioms drop_rejects
#print axioms long_tree_accepts
#print axioms long_rejects
#print axioms block_long_tree_accepts
#print axioms block_long_rejects
#print axioms short_tree_accepts
#print axioms short_rejects
#print axioms demand0_rejects
#print axioms demand0_keep_accepts
#print axioms cat0_feasible
end CompactChecker.Chunk733G4Reject
"""
    path = args.out / "CompactChecker" / "Chunk733G4Reject.lean"
    path.write_text(lean)
    rep.update({"file": str(path), "sha256": ex.sha256(path), "generator_sha256": ex.sha256(__file__),
                "source_sha256": ex.sha256(args.source), "tree_sha256": ex.sha256(args.tree)})
    print(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
