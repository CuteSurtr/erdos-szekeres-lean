# From certificates to the Lean case classes

Written 1 November 2026 (UTC) with `proof.md`. Revised the same day for the referee's findings R1 and R8
(`referee/NOTES.md`) and for the Lean proof of the mirror classes (`SYMLEAN/mirror`). Paths are relative to
`cloud/es7-2026-10-19/results`, except `proof.md`, `perturbation.md` and `referee/`, which are in this directory.
Hashes are SHA-256.

**The Lean reduction.** `SYMLEAN/SymmetricReduction.lean` (`6d5ec90a…252a6e38`) states the case classes as `Prop`s.
They are hypotheses, not axioms. From five of them, `HalfTurn34`, `Threefold33`, `Fivefold35`, `MirrorOneAxis33` and
`MirrorNoAxis34`, it proves `heptagon_of_nontrivial_isometry`: every finite set of at least 33 points in general
position that is mapped into itself by a Euclidean isometry g ≠ id contains 7 points in convex position. The sixth
class, `Fourfold32`, is used only by a variant (end of §1). `SYMLEAN/AffineReduction.lean` proves the same for affine
bijections (`heptagon_of_nontrivial_affineEquiv`). Axioms: `propext`, `Classical.choice`, `Quot.sound`
(`SYMLEAN/logs/`).

**The mirror classes are Lean theorems.** `SYMLEAN/mirror/ReductionThreeClasses.lean` (`0cc83994…`) proves
`MirrorOneAxis33` and `MirrorNoAxis34` (`mirrorOneAxis33_proved`, `mirrorNoAxis34_proved`) from Baek's theorem, with no
SAT input (§2). Its theorems `heptagon_of_nontrivial_isometry_3` and `heptagon_of_nontrivial_affineEquiv_3` assume only
`HalfTurn34`, `Threefold33` and `Fivefold35`. Same axioms (`SYMLEAN/mirror/axioms.out`).

**Where the trust lies.** The step from the classes to the theorem is Lean-checked, and so are the two mirror classes.
For `HalfTurn34`, `Threefold33` and `Fivefold35` the step from the certificates to the class is **not** Lean-checked.
It is the chain of §1: written proofs, certificates accepted by two proof checkers and, for `HalfTurn34` and
`Threefold33`, verdicts recorded at solve time for proofs that were then deleted.

## 1. The classes that rest on certificates

| Lean class (hypotheses) | encoder and CNF | normal-form lemma | soundness document | certificates | centre perturbation |
|---|---|---|---|---|---|
| **`HalfTurn34`**: \|S\| = 34, general position, `Invariant (halfTurn c) S`, c ∉ S | `SYMZ/zcnf.py` (`13d6c162…`), `rot 17 7 --m 2 --hull`: base `p cnf 838032 16653336`, `b0061e90…fd8ff1`. Unit CNFs: the base plus hull cubes (`C2C34/hullcubes.py` `10612953…`, `C2C34/cubes.txt`) or second-layer cubes (`C2C34/l2cubes.py` `a771dfe0…`, `C2P/cubes/P1..P8_cubes.txt`) as units. Second-layer cover CNFs: the base, the hull cube as units and one clause per subcase | `proof.md` Lemma 4: angular normal form from **any** hull vertex. Covers: `proof.md` Corollary 3 (the hull cover) and Corollary 3′ (each second-layer cover, relative to its hull cube; referee finding R1). Reductions A (P_a ↔ P_{17−a}) and B ((P_a,V) ↦ (P_a,(a−V) mod 17)): `C2C34/README.md` §6, `C2P/review`, `AUDIT3` A5 (checked at the CNF level) | `proof.md` (complete written proof, refereed: `referee/NOTES.md`; specification match, exact tests, mutation tests). Before it: a docstring sketch, `SYMZ/README.md` §1 last paragraph, and `C2C34` §5 (a review of `--no-sb`, without logs) | **Hull cover**: `central34-cover` (cover.cnf `bb60facb…`, proof `3255391a…`, lrat-check and cake_lpr, retained; `WRITEUP/CERTIFICATES.md`). **Hexagonal hulls**: `central34-hull`, 120 cases UNSAT, proofs retained, both checkers (`C2C34/logs/hex_cases.tsv`). **Parallelograms P1–P8** (`C2FINAL`): each case has 560 subcases in 287 orbits under reduction B, so there are 8 × 287 = 2,296 orbit facts, plus 8 second-layer covers. Every orbit has a member, and every cover a record, with status UNSAT and both checkers' verdicts recorded at solve time. Of the 2,492 records, 2,385 are UNSAT; an orbit may have several, so the two counts are not meant to match. The proofs were deleted (**recorded verdicts**), apart from the units re-solved with retained proofs (`C2FINAL` §4–5). All 2,589 recorded unit-CNF hashes rebuild from the base (`C2FINAL` §3). Bookkeeping: `C2FINAL/Central34Orbits.lean` (Lean) | **not needed** (`proof.md` Lemma 3: the only zero triples through c are {c,p,−p}, forced by general position) |
| **`Threefold33`**: \|S\| = 33, general position, `Invariant (rotAbout c (2π/3)) S`, c ∉ S | `C3a/c3cnf.py` (`cf730939…`, chain encoding) through `C3U2/tools/gen_case.py` (`689e9440…`) `11 7 none`: base `p cnf 168399 4154921`, `bf0e502e…6cdd6da`. Pieces: base plus hull/layer clauses (`C3U2/tools/hullcase.py` `2a1ce407…`) plus σ-cubes, one per tree node | `C3-S/soundness.md` Lemmas 1–5: slope order, label 0 on the hull, σ₀ = 0 by the point reflection, H3/H6(a,s), convex layers, mirror reduction below H3. Lemma H6M (`C3AUDIT2`). **Plus** `perturbation.md`: generic centre (Corollary, m = 3) and the frame choice for l (no point on l, no segment parallel to l) | `C3a/README.md` "The encoding" (identities 1–5, chain encoding), `C3b/DERIVATION.md`, `C3-S/soundness.md`; audits `C3AUDIT*` and `AUDIT3` A2 (sound with caveats; A2-F3 and A2-F4 are documentation gaps) | **Composition**: `C3FINAL`, two composers over 116,883 certified records re-derive every piece's CNF hash from the base and cover all 910 depth-2 roots, 0 open. **Lean check of the cover**: `C3LEAN` (`all_roots_covered`: the 73,567 leaves of one explicit cut cover the 910 roots; core Lean, `decide +kernel`; that every leaf names a certified record with a matching CNF hash is checked in Python). **Pieces**: accepted by both checkers at solve time; no proof retained (**recorded verdicts**); 26,436 records carry a proof hash. `C3SPOT`: 2,120 random pieces re-solved, all pass. The 204 indispensable σ-cube pieces were outside that sample; their re-solve, started on 1 November, is reported in `WRITEUP/SYMMETRIC.md` (Theorem 1) | **needed**: `perturbation.md`, Lemma P and Corollary (m = 3) |
| **`Fivefold35`**: \|S\| = 35, general position, `Invariant (rotAbout c (2π/5)) S`, c ∉ S | (a) `SYM5/symcnf.py` (`a8056da0…`) `35 7 5`, angle form: `p cnf 401464 7923909`, `ead55228…5450dbb`. (b) `SYM5/symcnf_layers.py` (`71b2d7e7…`) `35 7 5`, layer form: `p cnf 401464 7924027`, `90dea1cf…c0668a8` | (a) angle normal form, proof in §4 below. (b) layer lemma (`SYM5/README.md` §2; full proof in `AUDIT3`, finding A4-7) | `symcnf.py` docstring, `SYM5/README.md` §1–2; `AUDIT3` A4 (clause-by-clause argument, exact tests of both encoders) | (a) `c5-angle`: proof P1 `eff67c0f…`, lrat-check `c VERIFIED`, cake_lpr `s VERIFIED UNSAT` (heap 30000), retained. (b) `c5-layer`: proof L1 `8625b321…`, both checkers, retained (`WRITEUP/CERTIFICATES.md`). Each alone settles the class; they are two normal forms of one encoder, not independent encodings (`AUDIT3`, A4-3). Prior report: B. C. Dumitru (arXiv:2512.24061, §7, Table 1, row 5^6) reports an UNSAT Kissat run for 33 points with six pentagonal layers, which implies the bound through the layer lemma; no proof files are public, so it is a reported claim (`SYM5/README.md`) | **needed**: the model is uniform on 35 points plus c. `perturbation.md`, Lemma P and Corollary (m = 5) |

**Not used by the main theorem.** `Fourfold32` appears only in the variant `halfTurn_of_symmetric_counterexample`. Its
certificate is `C4CUT` (the c4 base plus six verified cuts, with LRAT). `AUDIT3` (finding A4-6) found it on no critical
path once `HalfTurn34` holds.

## 2. The mirror classes: Lean-checked from Baek's theorem

**The Lean proof.** `MirrorOdd.mirror_seven_line` (`SYMLEAN/mirror`) proves that a finite set in general position that
is invariant under the reflection in a line and has no 7 points in convex position has at most 32 points. Both classes
follow (`mirrorOneAxis33_proved`, `mirrorNoAxis34_proved`). The argument is the mirror reduction plus Baek's theorem for
n = 7: a set with distinct x-coordinates, no 4-cap and no convex 7-gon has at most C(6,2) + 1 = 16 points. Baek's
theorem enters through the repository's Lean formalization (`ErdosSzekeres/Vendor/ETV` at the repository root). No SAT
certificate is used.

**Credit.** The two mirror classes are consequences of Baek's theorem (J. Baek, Eur. J. Combin. 124 (2025) 104085;
arXiv:2206.04260, Theorem 1.6 in the arXiv numbering) through the elementary mirror reduction
(`SYMLEAN/mirror/README.md` §1; `MIRRORETV`). The value 16 used here, N(7,4,7) in Baek's notation, was reported
earlier by SAT by Balko and Valtr (2015; `MIRRORETV`).

**Independent confirmation by SAT** (`SYMZ`). The certificates below proved the same classes earlier. The main theorem
no longer needs them; they confirm the Lean result by an independent route.

| Lean class (hypotheses) | encoder and CNF | normal form | soundness document | certificate |
|---|---|---|---|---|
| `MirrorOneAxis33`: \|S\| = 33, general position, `Invariant (reflLine a u) S`, exactly one point of S on the mirror | `SYMZ/zcnf.py` (`13d6c162…`) `mirror 16 7 --axis 1`: `p cnf 695928 14080656`, `e45464ed…73739d02` | pairs numbered by decreasing height, axis point separate (`SYMZ/README.md` §1, fact 7); heights are distinct by general position; an orientation-preserving isometry maps the mirror to the y-axis | `SYMZ/README.md` §1 (facts 1–7), `SYMZ/REVIEW.md` (axis-point extension); `AUDIT3` A3 (re-derived, own evaluators, mutation tests; A3-F3: proof terse) | `mirror33`: proof `e1b2689d…`, lrat-check `c VERIFIED`, cake_lpr `s VERIFIED UNSAT`, retained; no independent replay on record (A3-F1). A further Lean chain, `Mir.MirrorExclusionLine` → `mirrorOneAxis33_of_exclusionLine` (`WRITEUP/MIRROR.md`, `SYMLEAN`), rests on about 75,000 recorded verdicts without retained proofs (A3-F9) |
| `MirrorNoAxis34`: \|S\| = 34, general position, `Invariant (reflLine a u) S`, no point of S on the mirror | `SYMZ/zcnf_v1.py` (`8fb8a3ab…`) `mirror 17 7`: `p cnf 838032 16642456`, `b175eac0…09a6c5b` (the final `zcnf.py` writes the same clauses, `1b61bf2f…`) | pairs by decreasing height (as above) | `SYMZ/README.md` §1; two source audits (29 October); `AUDIT3` A3 | `mirror34`: proof `98e4d02a…`, lrat-check `c VERIFIED`, cake_lpr `s VERIFIED UNSAT`, retained; one lrat-check replay by an audit, without a log in the repository (A3-F1) |

Neither confirmation needs a centre perturbation: the zero triples {Z, L_i, R_i} are forced by general position
(`perturbation.md`).

## 3. How each class follows from its row

For `HalfTurn34`, `Threefold33` and `Fivefold35`, and for the SAT confirmations of the mirror classes, the argument has
the same shape. Given S satisfying the Lean hypotheses:

1. **Normalize the frame.** Apply an orientation-preserving isometry, if needed, so that the centre is the origin or the
   mirror is the y-axis. This changes no orientation sign and no convex position.
2. **Make the centre generic (odd orders only).** Replace S by S_θ (`perturbation.md`). This keeps the symmetry, the
   order type and the convex 7-subsets.
3. **Label.** Label the set (perturbed in step 2, for odd orders) in the normal form of the row. The normal-form lemma
   says this is always possible, possibly after choosing among finitely many labellings (a hull vertex, a sector, a
   frame direction).
4. **Encode.** The soundness document says that the real chirotope and the real convexity values of this labelling
   satisfy every clause of the encoder's base CNF if S has no 7 points in convex position.
5. **Case split.** The case-split documents say that the labelling falls in some case, after the stated reductions
   (hull and layer cubes, σ-cubes, mirror and relabelling maps). The certificates say that each case CNF is
   unsatisfiable. So S has 7 points in convex position. For `HalfTurn34` the hull cover and the second-layer covers
   need no geometric argument (`proof.md`, Corollaries 3 and 3′).

Each class has its own sizes:

- `HalfTurn34`: 17 pairs.
- `Threefold33`: 11 orbits.
- `Fivefold35`: 7 orbits.
- `MirrorOneAxis33`: 16 pairs and 1 axis point.
- `MirrorNoAxis34`: 17 pairs.

They match the encoder parameters in the rows. The Lean reduction (`case_halfTurn`, `case_odd_prime`, `case_mirror`)
supplies exactly these hypotheses, including whether c, or an axis point, is in S (`AUDIT3`, finding A1-F6).

## 4. Note: the fivefold angle normal form exists

This is the existence argument for row (a), used together with perturbation.md. Let S be 5-fold symmetric about c, with
c ∉ S and a generic centre.

- Choose any point X₀ = (0,0) of S and measure angles at c from the ray c → X₀.
- Every other orbit has its five points at angles β + 72°·k. Exactly one of them lies in the open sector (0°, 72°). It
  cannot lie on a boundary ray: angle 0° means collinear with c and X₀, and angle 72° means collinear with c and R(X₀).
  Genericity excludes both. Call it the representative (o, 0).
- Two representatives have different angles, again by genericity. Sort them by angle.
- The units of `symcnf.py` add_sb then hold:
  - χ(c, X₀, (o,0)) = +, since the angle is in (0°, 180°);
  - χ(c, R(X₀), (o,0)) = −, since the angle relative to the ray c → R(X₀) is in (−72°, 0°);
  - χ(c, (o,0), (o′,0)) = + for o < o′, since the angle difference is in (0°, 72°).

This is the m = 5 analogue of proof.md, Lemma 4.

## 5. Status summary

| class | proof of the class | weakest link today |
|---|---|---|
| `HalfTurn34` | written proof (`proof.md`, refereed) + retained certificates for the hull cover and the 120 hexagons + recorded verdicts for the parallelogram orbits and covers + Lean bookkeeping (`C2FINAL`) | before the re-checks started on 1 November, about 98% of the 2,304 parallelogram orbit and cover facts rested on recorded verdicts of deleted proofs. The completeness review of the audit (`AUDIT3`, A8 §2) found that 60 orbit facts and 5 of the 8 second-layer covers rest only on records of the local Mac lanes, which keep no record of the tools used; the covers have a geometric backup, the 60 facts do not. The re-checks are reported in `C2FINAL` and `WRITEUP/SYMMETRIC.md` (Theorem 4) |
| `Threefold33` | written proofs (`C3a`, `C3-S`, H6M, `perturbation.md`) + recorded verdicts + Lean check of the cover (`C3LEAN`) | no proof of a piece is retained; the 204 indispensable σ-cube pieces were outside the `C3SPOT` sample (their re-solve: `WRITEUP/SYMMETRIC.md`, Theorem 1) |
| `Fivefold35` | written proofs (`symcnf.py`, layer lemma, `perturbation.md`) + two retained certificates | both certificates were accepted by both checkers at solve time; in the follow-up checks of the audit (`AUDIT3` §5 row 1, status at 15:08 UTC on 1 November), only L1 of the two had a replay with hash-bound logs, by lrat-check |
| `MirrorOneAxis33` | **Lean-checked** (`SYMLEAN/mirror`, from Baek's theorem); SAT confirmation: written proof (`SYMZ/README.md` §1, `SYMZ/REVIEW.md`) + one retained certificate | Lean and the class definition (reviewed in `SYMLEAN` §6, shown there not to be vacuous). The SAT confirmation is not needed; it has no independent replay on record (A3-F1) |
| `MirrorNoAxis34` | **Lean-checked** (`SYMLEAN/mirror`, from Baek's theorem); SAT confirmation: written proof (`SYMZ/README.md` §1) + one retained certificate | as for `MirrorOneAxis33`; the audit replay of the SAT certificate has no log in the repository |

None of the encoder soundness arguments is Lean-checked, and neither is the perturbation lemma.
