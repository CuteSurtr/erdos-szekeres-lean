# FORMAL20261122/fivefold: the fivefold heptagon theorem (RESULTS row C4) in Lean, modulo one cake_lpr verdict

25 Nov 2026, KST. Work directory `~/research/data/formalize-20261122/fivefold` (sources, olean, logs) and
`~/research/data/c4-encb-20261125` (the formula and the kept proof). Not refereed; built and checked inside the
project only.

## 1. Result

Lean-checked (Lean 4.24.0, Mathlib `f897ebcf`, axioms `[propext, Classical.choice, Quot.sound]`) **modulo one verdict**,
which is CERTIFIED in es-research §2's sense (CaDiCaL 2.1.3 LRAT proof, cake_lpr `c14ff498…` `s VERIFIED UNSAT`,
hashes recorded, proof kept):

```
EncB.Geo5.fivefold_heptagon_of_text
  (h : ∀ (nv : ℕ) (G : List (List ℤ)),
      EncB.parseDimacs (EncB.cnfText (EncB.encode 5 7 7) []) = some (nv, G) → ¬EncB.DimacsSatisfiable G)
  (S : Finset ErdosSzekeres.Point) (c : ErdosSzekeres.Point) (hgp : ErdosSzekeres.GeneralPosition S)
  (hinv : ErdosSzekeres.LayerLemma.Invariant (ErdosSzekeres.LayerLemma.rotAbout c (2 * Real.pi / 5)) S)
  (hcard : 32 ≤ S.card) : ErdosSzekeres.HasConvexNGon 7 S
```

Also pinned in `src/Geo5/Main5.lean` (13 `#guard_msgs`): `fivefold35_of_text : … → Fivefold35` (`Fivefold35` has
the body of SYMLEAN's `ErdosSzekeres.SymReduction.Fivefold35`: 35 points, centre not in the set),
`fivefold_heptagon_of_centre_not_mem_of_text` (at least 31 points, centre not in the set),
`fivefold_heptagon_order5_of_text` (invariance under any rotation `2πj/5`, `1 ≤ j ≤ 4`), and `text577_iff` (the
hypothesis is equivalent to `¬ DimacsSatisfiable (encB 5 7 7)`, so it is not vacuous).

So every set of at least 32 points in general position that is invariant under a rotation of order 5 contains a
convex heptagon, which is row C4's bound (`N(5-fold) = 31`), now with a Lean-checked encoder.

## 2. Method: nothing new in Lean

Every step is a generic lemma of the sevenfold development (`FORMAL20261122/sevenfold`, itself on ENCBLEAN), used at
`(m, K, t) = (5, 7, 7)` instead of `(7, 8, 10)`:

- `EncB.encB_satisfiable_odd` (odd `m ≥ 2`): a `ModelO m K t` satisfies `encB m K t`;
- `EncB.Geo7.modelO_of_counterexample` (`3 ≤ m`, `4 ≤ K ≤ 2m`): a centre-free set of `m·t` points in general position,
  invariant under the rotation by `2π/m`, with no convex `K`-gon, yields a `ModelO m K t` (here `7 ≤ 10`, `35 = 5·7`);
- `EncB.parseDimacs_cnfText` (generic): the round trip of the printed text;
- `convexNGon_of_layers` (ES8Geo/Capstone2): the corollaries, whose proofs are copied verbatim from
  `LEANEXT/es7corr/ES7Corollaries.lean`; the order-5 lemmas are the sevenfold's with 7 replaced by 5.

The module compiles against the sevenfold build read-only (`tools/lc5.sh`: its `LP_SELF`, Mathlib from ENCBLEAN geo's
checkout, the vendored repository modules from sevenfold's own olean store): 9 s, 2.35 GB, rc 0, no message
(`logs/build.log`). Control `controls/Geo5/Bad5.lean` (the same file with `32 ≤ S.card` weakened to `31`, which is
false since 31-point fivefold sets containing the centre without a heptagon exist, `SYM5/c5_31minus_centre.txt`) fails
to compile with two errors (`logs/bad5.out`).

## 3. Trust items (as ENCBLEAN E1–E6, read for this instance)

- **E1** (emitter): the pinned exe `encb_dimacs` (SHA-256 `3d43fa8b…`, the copy the sevenfold record pins) prints
  `cnfText (encode 5 7 7) []` with `twin-base 5 7 7`: 4,102,383 bytes, `p cnf 11135 189437`, SHA-256
  `326758c67f75aafd80b6e21feae4778da45a983417377211050058ef5b7f8c93`; `base 5 7 7` prints the same bytes. Sanity: the
  same exe's `twin-base 7 8 10` hashes to the sevenfold record's `b4d29017…`. Checked by running compiled code, not
  proved.
- **E2** (verdict): `certify_cnf.sh` on that file: CaDiCaL 2.1.3 exit 20 in 2 s, LRAT 20,871,983 B (SHA-256
  `26a5be67…`), cake_lpr `c14ff498…` (heap 4000) printed `s VERIFIED UNSAT` in 1 s (`data/certify_577.jsonl`,
  `data/encB_577.cake.out`). Proof kept: `~/research/data/c4-encb-20261125/out/encB_577.lrat.zst` (6,292,981 B,
  `05ffe60c…`, `data/files.sha256`).
- **E2, second checker (25 Nov 21:20)**: the same LRAT proof (decompressed, SHA-256 `26a5be67…` = the
  record) is also accepted by **Lean core's verified checker** `Std.Tactic.BVDecide.LRAT.check` (Lean 4.24.0;
  `LRAT.check_sound : check proof cnf = true → cnf.Unsat` is proved in core): `lrat-lean/LeanLrat.lean`, run natively
  with `lean --run` (trust: the Lean compiler and runtime, not the kernel), printed `s VERIFIED UNSAT (...)` in 2 s at
  0.58 GB (`lrat-lean/check_577.out`). Its DIMACS parser is not verified; per file, core's printer
  `Std.Sat.CNF.dimacs` applied to the parsed formula reproduced the input text byte for byte. Controls
  (`lrat-lean/test/`): PHP(4,3) accepted; the satisfiable PHP(4,3) minus one clause, a final step whose hint is a
  missing clause id, and a proof with its first lemma dropped are all rejected (`s NOT VERIFIED`); removing one
  hint of the final step is accepted, correctly, since the remaining hints still give the conflict. So the verdict
  rests on two independently verified checkers (CakeML/HOL4 and Lean).
- **E3** (DIMACS semantics): cake_lpr reads the text as `parseDimacs` does. Tested, not proved: the evidence is
  ENCBLEAN's (`ENCBLEAN/logs/m9_a2_cake_parse.log`) for texts of the same printer `cnfText`; this text has one `p`
  line, no comment line, and ends with `0\n`.
- **E4–E6**: compiler and runtime, kernel/Mathlib/definitions, SHA-256: as ENCBLEAN.

Control on the formula side: `twin-base 5 7 6` (30 points, 6 orbits) is **satisfiable** (CaDiCaL exit 10,
`data/control_576_cadical.out`), as it must be if 30-point fivefold heptagon-free sets exist; so the UNSAT verdict at
`t = 7` is not an artefact of an always-unsatisfiable encoding.

## 4. Relation to the other records

- RESULTS row C4 (CERTIFIED: `symcnf_layers.py` formula `c5_n35L`, re-certified on Linux in RECERT20261125) is a
  different encoding of the same statement, without a Lean encoder. This record adds a second formula whose link to
  the geometry is Lean-checked; the two verdicts are independent solver runs on unrelated formulas.
- **Fourfold (row C5): this route does not work.** `twin-base 4 7 8` (32 points, 8 orbits; SHA-256 `22a67719…`) is
  **satisfiable** (CaDiCaL exit 10, `data/certify_478.jsonl`), like the cut-free formula of C4CUT; C5 still needs the
  six realizability cuts, and their Lean checker does not exist.
- Rows C2/C3 (threefold, half-turn) are out of this route's reach: `modelO_of_counterexample` needs `K ≤ 2m`, and
  `7 > 6` for `m = 3`, `7 > 4` for `m = 2`.
- Not done: a bridge from `EncB.Geo5.Fivefold35` to `ErdosSzekeres.SymReduction.Fivefold35` for SYMLEAN's Theorem A
  (which also needs `HalfTurn34` and `Threefold33`).
