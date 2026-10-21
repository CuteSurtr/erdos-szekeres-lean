# Mirror-symmetric 33-point sets contain a convex heptagon

All paths are relative to `cloud/es7-2026-10-19/` on branch `es7-cloud` of this repository,
unless they start with `docs/` (main repository). Every number is followed by the file it comes
from. Commit hashes are the hashes after the history rewrite of 2026-10-21; where a source file
cites an older hash, the old one is given in brackets and was translated with
`results/FINAL/COMMIT_MAP.tsv`. Written 2026-10-21 from the files at commit 852bee7 (the commit of
`results/WRITEUP/TASK.md`) and the branch head at the time of writing.

**Terms.** A CNF is a propositional formula in conjunctive normal form, written as a DIMACS
file; UNSAT means unsatisfiable. A cube is a conjunction of literals; F + cube is F with the
cube's literals added as unit clauses (`cubeCnf` in Lean). LRAT is a clausal proof format for
UNSAT; cake_lpr is a checker for such proofs, formally verified in HOL4/CakeML down to x64
(`results/V2-L/README.md` §6), whose verdict on a refuted file is `s VERIFIED UNSAT`. A leaf is
a cube whose CNF has been refuted; a set of leaves covers a case if every assignment satisfying
the case cube satisfies some leaf (`verify/v3/v3_check.py`). A case (U, L) of §4 is named
`U<U>_L<L>` with elements joined by `-`, e.g. U_L7 for U = ∅, L = {7} (`results/Mii-S/scripts/hullsplit.py`, `name`).
Directory names under `results/` are separate cloud runs: H and H3 are the Lean encoding
packages; C and C2 earlier runs on the mirror class; Mi-0..Mi-3 the shard runs of sub-case (i)
(a shard is one machine's share of the cubes); V1-0..V1-3 and V1-L the re-checks and the Lean
side of sub-case (i); Mii-S the case split of sub-case (ii); Haudit its independent audit;
WAVE1–WAVE4 the four rounds of cloud machines that solved the 278 hard cases; V2-L (with its
assembly steps V2F, V2G) the Lean side of sub-case (ii); V3T, V3A–V3E and V3Z the from-scratch
re-solving and checking runs ("acceptance", §5); E and E2 the D_3 runs (§2); C3-S, C3WAVE1,
C3WAVE2 the runs on the 3-fold class. Zf is the commit at which no wave case had an open cube
(§5).

## 1. Statement, and what is and is not claimed

**Theorem (conditional on the trust base of §6).** Let S be a set of 33 points in the plane,
no three on a line, and let ρ be a reflection in a line with ρ(S) = S. Then S contains 7 points
in convex position.

Equivalently: a counterexample to the Erdős–Szekeres conjecture at n = 7, that is a 33-point set
in general position with no convex heptagon (which would show ES(7) > 33 = 2^5 + 1), is not
mirror-symmetric.

The statement is the Lean 4 proposition `Mir.MirrorExclusionLine`
(`results/H3/MirrorEncoding/Line.lean`, namespace `Mir`; `results/H3/README.md` §3):

```lean
def MirrorExclusionLine : Prop :=
  ∀ (S : Finset Point) (a u : Point), u 0 ^ 2 + u 1 ^ 2 = 1 → GeneralPosition S →
    S.card = 33 → (∀ q ∈ S, reflLine a u q ∈ S) → HasConvexNGon 7 S
```

i.e. for an arbitrary line through `a` with unit direction `u`. It is the conclusion of the
Lean theorem `V2L.mirrorExclusionLine_final` (`results/V2-L/README.md` §9.1), whose
hypotheses are 1 + 121 + 1,198 + 74,000 statements of the form "this explicit CNF is
unsatisfiable", each of which is a cake_lpr `s VERIFIED UNSAT` verdict on a file (§5, §6).

**What is claimed.**
- The Lean kernel has checked everything from those CNF facts to the geometric statement: the
  soundness of the two encodings, the geometry of the normal forms, the reduction from an
  arbitrary line to the y-axis, the case split, and that every case's leaf tree covers the case.
  Axioms: `propext`, `Classical.choice`, `Quot.sound` (`results/V2-L/README.md` §9.2).
- Each of the CNF facts has a cake_lpr verdict recorded in the repository; for sub-case (ii) the
  case and leaf facts were in addition re-derived from scratch (every leaf re-solved from a CNF
  rebuilt from F, the sub-case (ii) CNF of §3, every proof checked by cake_lpr, every case cover checked) by the acceptance
  passes V3T, V3A–V3E and V3Z (`results/V3Z/summary.md`).

**What is not claimed.**
- Not ES(7) = 33. Only the mirror-symmetric class is excluded.
- The class of sets invariant under a rotation by 120° (and under no reflection) is **open**.
  `results/C3-S/README.md`: "No top case is closed", 1,956 frontier nodes open, with a cost
  estimate of about 1,500 core-hours "if the H3 tail is mild" (there H3 is the 3-fold top case
  with a triangular hull, not the directory `results/H3`), possibly 10^4–10^5. Later
  waves work on it (`results/C3WAVE1`, 24 machines C00–C23; `results/C3WAVE2/README.md`: a survey
  of the 1,349 of 1,630 depth-2 roots that wave 1 did not touch); the class is not closed.
- No counterexample is known. No SAT record occurs in Mii-S (`results/Mii-S/README.md` §5:
  "No case, cube, product or `G_o` was SAT") or in any leaf or cover file of the acceptance runs
  V3T, V3A–V3E, V3Z (`results/V3Z/README.md`).
- The cake_lpr verdicts are not imported into Lean; they are hypotheses of the Lean theorem
  (§6). The CNF facts are about files; the step from a file to a Lean term is a byte or sha256
  comparison done outside Lean, and for the per-leaf files of sub-case (ii) it rests on the
  drivers' file writing (§6).
- We did not find prior work stating that every reflection-invariant 33-point set in general
  position contains 7 points in convex position (`results/LIT/RELATED.md` §3–§4, searches of
  21 October 2026 listed in `results/LIT/searches.tsv`; the sources there were read from
  abstracts and search snippets only, because direct fetches were blocked; and
  `docs/RELATED_WORK_2026-10-14.md`). The nearest work found concerns rotational symmetry:
  Subercaseaux, Mackey, Qian and Heule (arXiv:2506.00224): for 16 points without a convex
  hexagon the 3-fold formula is UNSAT and the 4- and 5-fold formulas are satisfiable and
  realizable; for 32 points without a convex 7-gon there is no realizable 4-fold symmetric set.
  The 14 Oct survey also records a mention of "axially symmetric sets (18 points force an empty
  hexagon)" in Koshelev–Koshka (arXiv:2604.20120), marked there "should be re-verified"; the
  later search (`results/LIT/RELATED.md` §3) found in that paper's snippets only a 25-point
  3-fold symmetric example for a hexagon-type variant. No priority is claimed.

## 2. Which symmetries a 33-point counterexample can have

Let S be 33 points in general position with no 7 in convex position, and let G be the group
of isometries of the plane that map S to itself. G is finite (S contains three non-collinear
points, and an isometry is determined by their images) and fixes the centroid of S, so by the
classification of finite groups of plane isometries G is cyclic C_s or dihedral D_s, with
rotation subgroup C_s. The point reflection (half-turn) is the rotation of order 2.

**Claim.** s ∈ {1, 3}. Hence G is trivial, generated by one reflection (D_1), C_3, or D_3.

*Proof.* Let r be a rotation of order s ≥ 2 in G, with centre o. Every point other than o
has an r-orbit of exactly s points, and these s points form a regular s-gon centred at o.
- If s ≥ 7, any 7 vertices of such an orbit are in convex position. Since |S| = 33 > 1, some
  point is not o, so this orbit exists. Contradiction.
- If s is even, r^{s/2} is the half-turn about o. Its orbits off o have size 2, and 33 is odd, so
  o ∈ S. Then for any p ∈ S other than o, the points p, o, −p (reflected through o) are three
  collinear points of S. Contradiction.
- If s = 5, then 33 = 5a + c with c ∈ {0, 1} (c = 1 if o ∈ S), and 33 ≡ 3 (mod 5). Contradiction.
- So s = 3, and then 33 = 3a + c forces c = 0: the centre is not in S (11 orbits of size 3).

This is the argument of `plan/es7_structure.md` (C6, "[own, elementary]") and
`plan/es7_methods.md` (Rotations); the s = 5 line is the divisibility check they do not spell out.

**The cases that remain.**
- **D_3.** Under D_3, 33 = 6a + 3b + c, with a orbits of size 6, b orbits of size 3 (on the
  mirror axes) and c ∈ {0, 1} for the centre; c = 0 by the C_3 case. Each orbit of size 3 has one
  point on each of the three axes (the rotation permutes them), so each axis carries b points of
  S; a line carries at most 2 points (general position), so b ≤ 2; 33 = 6a + 3b forces b odd, so
  b = 1 and a = 5: 5 orbits of 6 and one orbit of 3 on the mirror axes
  (`results/E/README.md` §4). This class is excluded by the CNF `n33k7d3` (sha256
  prefix 72ebbae0) and two other constructions of the same class, `n33k7m3refl` (cc329387; the 3-fold CNF plus
  reflection clauses, `c3refl.py`) and `n33k7d3direct` (7796d999; `d3cnf.py` with the direct
  K-gon encoding), all UNSAT (`results/E/README.md`, Summary). `results/E2/README.md`
  re-checked the three proofs with the patched lrat-check and with cake_lpr: all VERIFIED / `s
  VERIFIED UNSAT`. The D_3 encodings are tested, not formally verified (`results/E/README.md`:
  "Nothing in this directory is a theorem"). A D_3-symmetric set is also mirror-symmetric, so it is covered by the
  theorem of this note too, which does not depend on E/E2.
- **D_1 (one reflection):** this note.
- **C_3 (a 3-fold rotation, no reflection):** open (§1).

**Mirror sets have exactly one point on the axis.** The points of S off the axis come in mirror
pairs, so the number on the axis is odd; three points on the axis would be collinear. So S is one
axis point c plus 16 mirror pairs (`results/C/README.md`, opening paragraph; Lean:
`Mir.exists_mirrorSet`, `results/H3/README.md` §2). Either c is a vertex of conv(S) (sub-case
(i)) or c lies in conv(S ∖ {c}) (sub-case (ii)); by general position c is not on the boundary
without being a vertex.

## 3. The encoding and its Lean soundness proof

**Variables.** After a normalization that orders the points 1..33, the variable X(i,j,k), for
i < j < k, is true when the points i, j, k are counter-clockwise; an assignment satisfying the
axioms is a signotope (an abstract order type). The base CNF
(`tools/etv/gen_etv.py 33 7 7 7 --mirror`; in Lean `mirClauses` = `ETV.etvClauses`, the
option-free generator whose soundness is proved in `results/H`, plus hull units and the
identification clauses, `results/H3/README.md` §3) has the signotope axioms and the clauses forbidding 7 points in convex position via
cup and cap auxiliary variables (`results/H3/README.md` §3, "The generator").

**Mirror normalization.** The mirror identification is the orbit substitution
X(i,j,k) = X(34−k, 34−j, 34−i), with sign +, applied to every clause (`results/C/scripts/mirgen.py`,
Lean `Mir.subVar`/`subLit`, `results/H3/README.md` §3). This is the form for sub-case (ii); in
sub-case (i) `mirgen.py` uses m = N + 2, i.e. X(i,j,k) = X(35−k, 35−j, 35−i) on points 2..33
(`mirgen.py` docstring: "m = N+1 (no hull) or N+2 (hull, indices 2..N)"). The sign is + because
the reflection negates every orientation and reversing the order of three indices is an odd
permutation. `results/Haudit/AUDIT.md` NOTE-4 checked
the + sign on all 5,456 triples of each of 15,900 exact sets.

**Sub-case (i), axis point a hull vertex** (`hullCnf 33 7`, file `hm33k7.sub.cnf`, sha256
`bfbc2d6096e4099ba751130d421eca9da18b72559991103cc2d4b4bc0d92757d`, header `p cnf 47002 535454`,
`results/H3/README.md` §3). If c is extreme, all other points are strictly on one side of the
horizontal through c (`extreme_axis_split`). The linear map (x, y) ↦ (−y, x) (`rotA`, c on top)
or (x, y) ↦ (y, x) (`rotB`, c at the bottom; this map is a reflection, not a rotation, and
reverses every orientation, `orient_rotB`) makes c strictly leftmost on the new, horizontal
mirror axis. Sorting the other points by slope from c gives the hull frame (`ETV.HullFrame`;
this is the projective normal form of `results/C`, in which c goes to vertical infinity and the
slope seen from c is x/(y₀ − y)). A hull frame is determined by the set and its first point
(`HullFrame.eq_of_ptSet`), so the mirrored frame is the frame itself, which gives
σ(N−k, N−j, N−i) = σ(i, j, k) for 1 ≤ i in the 0-based indexing of `Frame.lean`
(`results/H3/MirrorEncoding/Frame.lean` header; `results/H3/README.md` §2, "Sub-case (i)").

**Sub-case (ii), axis point interior** (`interiorCnf 33 7`, file `m33k7int.sub.cnf` = F, sha256
`69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d`, header `p cnf 47002 515121`,
`results/H3/README.md` §3; 2,736 free orbits, `results/C/README.md`). The axis is the y-axis;
points are sorted by x, so P_{34−i} = reflX(P_i) and c = P_17. Ties in x between different pairs
are broken by the projective map (x, y) ↦ (x, y)/(1 + εy), which commutes with the reflection
and keeps every orientation sign (`TieBreak.lean`, `exists_eps`). Here reflX(x, y) = (−x, y),
and orient(p, q, r) > 0 means p, q, r counter-clockwise (`results/Mii-S/soundness.md`,
Notation). Two clauses say that c is not extreme: some X(i,17,k) with i < 17 < k is true and
some is false (`AxisInterior`, `mirgen.py --interior`). They hold because some point a of S is
strictly above c and some strictly below, and for a mirror pair a, reflX a with a left of the
axis, orient(a, c, reflX a) = 2·a.x·(c.y − a.y) (`results/H3/README.md` §2). Finally the unit X(1,2,3) breaks the
y-flip (x, y) ↦ (x, −y), which commutes with the reflection, keeps the x-order and complements
every orientation; complementing a signotope keeps the signotope axioms, the mirror symmetry and
the absence of convex 7-gons and swaps the two interior clauses, so X(1,2,3) may be assumed
(`results/H3/README.md` §2, `results/Mii-S/soundness.md` step 1).

**Lean soundness** (`results/H3/README.md` §3, `MirrorEncoding/Sound.lean`, `Interior.lean`,
`TieBreak.lean`, `Frame.lean`, `Line.lean`):

    theorem Mir.hullCnf_satisfiable (hK2 : 2 ≤ K) (hσ : IsSignotope N σ) (hK : ¬HasGon σ N K)
        (hH : HullForm N σ) (hS : MirSym N true σ) : DimacsSatisfiable (hullCnf N K)
    theorem Mir.interiorCnf_satisfiable (hN : 3 ≤ N) (hK2 : 2 ≤ K) (hσ : IsSignotope N σ)
        (hK : ¬HasGon σ N K) (hS : MirSym N false σ) (hI : AxisInterior N σ) :
        DimacsSatisfiable (interiorCnf N K)
    theorem Mir.hasConvexNGon_of_unsat_hull (hunsat : ¬DimacsSatisfiable (hullCnf 33 7)) ...
    theorem Mir.mirrorExclusionLine_of_unsat (h1 : ¬DimacsSatisfiable (hullCnf 33 7))
        (h2 : ¬DimacsSatisfiable (interiorCnf 33 7)) : MirrorExclusionLine

`DimacsSatisfiable` is plain DIMACS semantics (`results/H`). The reduction from an arbitrary line
to the y-axis is the rigid motion p ↦ M(p − a), M = [[u₁, −u₀], [u₀, u₁]] (`Line.lean`).
The Lean generator `Gen.lean` writes both CNFs; its output (string formatting in `Emit.lean`,
unverified) is byte-identical (`cmp`) to the output of the Python generators (`gen_etv.py`,
`mirgen.py`, driven by the shell script `results/C/scripts/make_cnfs.sh`) for both files and for an 84-instance grid of smaller sizes (`results/H3/README.md` §3, table).
`MirrorEncoding/Audit.lean` pins 29 axiom sets with `#guard_msgs`.

## 4. The case split of sub-case (ii)

Source: `results/Mii-S/soundness.md`, `results/Mii-S/README.md` §1, `results/Haudit/AUDIT.md`.

**Cases.** In the normal form of §3, P_1 and P_33 have the least and greatest x and equal y, so
they are hull vertices and the chord P_1P_33 is horizontal. The hull vertex set V is
reflection-invariant and does not contain c (sub-case (ii)), so V ∖ {P_1, P_33} is a union of
mirror pairs, each strictly above the chord (upper chain) or strictly below (lower chain) — a pair
at chord height would put 4 points on a line. V is in convex position, so |V| ≤ 6; |V| is even
and ≥ 3, so |V| ∈ {4, 6}. A case is (U, L): disjoint sets of pair labels in 2..16 (pair a ↔ 34−a)
with 1 ≤ |U| + |L| ≤ 2. That gives 30 cases with a 4-gon hull and 420 with a 6-gon hull,
**450** in all (`results/Mii-S/soundness.md`, "The split"); by |U|: 120 + 225 + 105
(`results/Haudit/AUDIT.md` task 2).

**Cube of a case.** cube(U, L) consists of unit literals: (a) every other point is strictly left
of each ccw hull edge; (b) hull triples are ccw; (c) each upper (lower) vertex is above (below)
every chord P_iP_k that spans it in x. Cubes have 61–535 orbit literals
(`results/Mii-S/README.md` §1; checked on `results/Mii-S/cases.jsonl`, field `nlits`).
`results/Mii-S/soundness.md` proves (a)–(c) for the true orientation assignment of any real
configuration, i.e. that it satisfies the cube of its own case (that it satisfies no other cube
is only tested, and not needed).

**Completeness, certified without geometry (the 122 obligations).** UP(U) is the cube that says
the upper chain starts 1, u_1, …, u_k, 34−u_k: for each edge v→q of this left half (the crossing
edge included), orient(v, q, r) < 0 for every other point r (`results/Mii-S/soundness.md`,
"Certificate argument").
- `root`: F + {¬UP(U) : U ⊆ 2..16, |U| ≤ 2} is UNSAT (121 blocking clauses; 121 = 1 + 15 + 105).
- `up:U`, for each of the 121 values of U: F + UP(U) + {¬cube(U, L) : (U, L) a case} is UNSAT.
- Then any model of F satisfies some UP(U), then some cube(U, L); so if every case CNF
  F + cube(U, L) is UNSAT, F is UNSAT.

This is a statement about models of F (signotopes), not about point sets, so the case split is
complete as a matter of propositional logic once the 122 obligations are UNSAT. The Lean form is
`V2L.not_dimacsSatisfiable_of_clauseCover₂` (`results/V2-L/README.md` §3); the kernel also checks
`casesOf_length_sum` (the lengths of the `casesOf U` sum to 450; with `upSets_nodup` and
`caseSpecs_upper_mem` they partition the 450 cases) and that no cube contains the literal 0 (§4
there: "Only the nonzero facts are used by the proofs"). A flat one-level cover with all 450 blocking clauses did not finish in
1,480 s of CaDiCaL (`results/Mii-S/soundness.md`).

The 122 obligations: all `s VERIFIED UNSAT` in `results/Mii-S/cover_lrat.jsonl` (122 records),
and again from scratch in `results/Haudit/t3_cover_lrat.jsonl` (122 records, every CNF sha256
equal to Mii-S's, `results/Haudit/AUDIT.md` task 3; the auditor's independent construction of
the 122 CNFs agreed with `cover.py`'s, task 2). Their CNFs are byte-identical to the Lean terms
`rootCnf`/`upCnf` (`results/V2-L/README.md` §5: root equal, 121/121 equal).

**Tests of the geometric argument** (not needed for soundness): Mii-S, 2,000 + 1,000 random
sets, 0 failures, 279 distinct cases hit (`results/Mii-S/README.md` §1); Haudit's independent
test, 15,900 exact sets, 0 failures, 394 distinct cases hit = all except the 56 vacuous ones
(`results/Haudit/AUDIT.md` task 4, NOTE-3). The vacuous cases are those with 2 ∈ U, or with
3 ∈ L and 2 ∉ L: their cubes contain ¬X(1,2,3), contradicting F's unit X(1,2,3). NOTE-3 writes
"2 ∈ U or 3 ∈ L", which also takes in the case U = ∅, L = {2, 3} and gives 57; that case is not
vacuous (its lower chain 1, 2, 3 is ccw) and was hit by the tests (`results/Haudit/t4_summary.txt`:
"U2.. or L3.."; recounted from `results/Mii-S/cases.jsonl`).

## 5. Solving and from-scratch acceptance

**Sub-case (i).** The Lean theorem uses the 1,198 leaf cubes of `verify/hull_leaves.icnf`
(sha256 `cc11270a57ebe85ad1d5c83b15da0a3439521cc7ebd50432f16c223a1b2478b6`), from the shard runs
Mi-0..Mi-3; they form a complete binary partition (`verify/README.md`). Every leaf was re-checked
with cake_lpr by V1-0..V1-3 and a backup run in V1-L: 1,198 of 1,198 `s VERIFIED UNSAT`, no gaps
(`results/V1-L/SUMMARY.md`, table: 300 + 300 + 299 + 299; CaDiCaL 26,142 s and cake_lpr 4,608 s
summed over that table's rows). Earlier, H3 had closed the same CNF with a different leaf list of
5,589 cake_lpr-verified leaves (the closed cubes of the earlier run C2, plus C2's 1,048 open
cubes refuted by H3, the last one after a split into 4 sub-cubes) (`results/H3/README.md`); the Lean theorem does
not use that list.

**Sub-case (ii), the 172 direct cases.** 172 cases were UNSAT within 10 s
(`results/Mii-S/README.md` §2), each re-solved with LRAT and cake_lpr-verified
(`results/Mii-S/pass2_lrat.jsonl`: 174 records over 174 cases, 172 with `s VERIFIED UNSAT` and 2
without a cake_lpr field (U_L2-3 and U_L2-4, result UNKNOWN); 443 s CaDiCaL and 331 s cake_lpr
over the 172 verified records), and again from scratch by
the audit (`results/Haudit/t5_all172.jsonl`: 172 of 172 `s VERIFIED UNSAT`, sha256 equal to
`cases.jsonl`, 699 s solve and 445 s check, `results/Haudit/AUDIT.md` task 5).

**Sub-case (ii), the 278 wave cases** were closed by cube-and-conquer (a look-ahead solver,
march_cu from the CnC package at 705b60c6, splits a CNF into cubes, i.e. conjunctions of
literals, and CaDiCaL 3.0.1 solves each cube with a time cap; a cube that times out is split
again, recorded as SPLIT; a leaf counts only with cake_lpr `s VERIFIED UNSAT`). In WAVE1 the six
hardest 4-gon cases were split into march_cu top cubes (`march_cu CASE -d 7`, 128 cubes per top
file, `results/Haudit/AUDIT.md` NOTE-2); the other cases were first given whole to the driver
(`verify/README.md` "Wave 1", `results/Mii-S/README.md` §2). 138 wave cases closed with the empty
cube as their only leaf (`results/V3Z/covers.jsonl`). Four waves of cloud machines:
WAVE1 36 machines (W00–W35), WAVE2 12, WAVE3 26, WAVE4 75 (directory listings of
`results/WAVE1`–`results/WAVE4`). At Zf = 06c1f798cd8b8b066df804282f95e9ec075c4d99 [old
14447d0d56c891a89a07a8141b50eae0ebfd44a7], 2026-10-20T16:20:17Z, no wave case has an open cube
(`results/FINAL/READY.json`: 278 wave cases, 0 open cubes, tool
`results/WAVE4/scripts/gfrontier3.py`).

**Why the wave records were not accepted as they stand.** The 36 WAVE1 machines each ran their
own modified driver (`results/Haudit/AUDIT.md` RISK-3); the drivers of WAVE2–WAVE4 were not
reviewed by the audit. The audit found that the original Mii-S driver counts
a leaf as closed even when cake_lpr rejects it (BUG-1, no effect on committed results), that a
truncated last cube line could be read as a larger cube (RISK-1), and that some drivers used
non-unique scratch names, so a verdict could be recorded for the wrong cube (RISK-3 (b)).

**The from-scratch acceptance (V3).** `verify/v3/` (at 92746acb [old bdf319c]):
- `v3_jsonl_leaves.py` and `v3_manifest.py` build a manifest of all distinct (case, leaf)
  pairs from the wave directories, parsing strictly; at Zf: 73,880 leaves in 278 cases,
  0 problems, sha256 `e01af167266dc044078798355f76f9f8d36c74d1b8843aeab90072b644ea83b5`
  (`results/V3Z/inputs.txt`, equal to `results/FINAL/READY.json`).
- `v3_check.py`, per leaf: rebuild the CNF as F's body + case cube units + the leaf literals not
  already in the cube (both sorted by |literal|); the case part must hash to the case's
  `cnf_sha256` in `results/Mii-S/cases.jsonl`; run CaDiCaL with a text LRAT proof; VERIFIED only
  if cake_lpr prints exactly `s VERIFIED UNSAT`. A leaf that contradicts its case cube is
  recorded VERIFIED without a solver run (`verify/v3/v3_check.py`, `leaf_job`); none of the
  73,880 final leaves is of this kind (`results/V3Z/problems.txt` gives timings for n = 73,880
  solved leaves).
- per case: the cover CNF {case cube units} + {¬leaf : leaf} must be UNSAT with a cake_lpr
  verified proof, or the leaf list must contain the empty cube.
- V3T (`results/V3T/README.md`) reviewed and tested the scripts, found two bugs (shared work
  paths; resume keyed by index alone), fixed them (a89d6de7 [old a3e5d17] and 6664466f [old
  f3b07a7]), and found no failure in 2,655 records. Passes V3A (9 machines), V3B (16), V3C (16),
  V3D (24) and V3E (8) checked the leaves of successive manifests (directory listings;
  `results/V3C/README.md`, `results/V3D/README.md`, `results/V3E/README.md`).
- V3Z (`results/V3Z/README.md`, `summary.md`) checked all 278 covers (`results/V3Z/covers.jsonl`:
  278 VERIFIED, 140 by cake_lpr and 138 with the empty cube as a leaf) and built the table
  `results/V3Z/accepted_final.tsv` with `scripts/aggregate_final.py` over 78 record files at
  branch head 569b763f [old ff29bc68]. It read 75,459 leaf VERIFIED records, 1 leaf REJECTED (U4_L
  `[-1014, -1040, 1065, -1112, 1134, 1155, -1245]` in `results/V3A/V07/out.jsonl`, next to a
  VERIFIED record of the same leaf), 377 cover VERIFIED and 9 cover NOT_COVERED records (for leaf
  lists of older manifests, none equal to a final leaf list).

**Final numbers** (`results/V3Z/summary.md`, `results/V3Z/problems.txt`):
- 278 of 278 wave cases ACCEPTED; 73,880 of 73,880 leaves have a VERIFIED record whose CNF sha256
  matches the CNF rebuilt from F + case cube + leaf; every cover VERIFIED; no SAT record.
- Per solved leaf: solve median 10.9 s, max 730.0 s; check median 3.0 s, max 52.0 s.
- The 172 direct cases and the 278 accepted wave cases are disjoint and are all 450 cases.

## 6. The Lean theorems, axioms and trust base

Lean 4.24.0, Mathlib v4.24.0. Packages `results/H` (`ETVEncoding`), `results/H3`
(`MirrorEncoding`), `results/V1-L` (`V1L`), `results/V2-L` (`V2L`). No `sorry`, `admit`,
`native_decide`, `axiom` declaration, `implemented_by` or `extern` in V2-L (`results/V2-L/README.md`
§9.2, `results/V2-L/logs/tree_grep_forbidden.log`, a grep over V2-L's 517 Lean files);
`results/H`, `results/H3` and `results/V1-L` each state in their README: no `sorry`, `admit`,
`native_decide` or new axiom.

**Sub-case (i)** (`results/V1-L/SUMMARY.md`):

```lean
theorem V1L.hullVertexLine_of_leaves
    (h : ∀ c ∈ hullLeaves, ¬DimacsSatisfiable (cubeCnf (hullCnf 33 7) c)) :
    ∀ (S : Finset Point) (a u c : Point), u 0 ^ 2 + u 1 ^ 2 = 1 → GeneralPosition S →
      S.card = 33 → (∀ q ∈ S, reflLine a u q ∈ S) → c ∈ S → reflLine a u c = c →
      c ∉ convexHull ℝ (↑(S.erase c) : Set Point) → HasConvexNGon 7 S
```

`hullLeaves` is `verify/hull_leaves.icnf` as Lean data; `coverCheck hullLeaves = true` is proved
by `decide +kernel`. Axioms `[propext, Classical.choice, Quot.sound]`.

**Sub-case (ii) and the whole class** (`results/V2-L/README.md` §9.1):

```lean
theorem V2L.mirrorExclusionLine_final
    (h1 : ∀ c ∈ V1L.hullLeaves, ¬DimacsSatisfiable (cubeCnf (hullCnf 33 7) c))
    (hroot : RootCertificate) (hup : UpCertificates)
    (hleaves : ∀ p ∈ caseTable, ∀ l ∈ (treeOf p.1).leaves,
      ¬DimacsSatisfiable (cubeCnf (cubeCnf (interiorCnf 33 7) p.2) l)) :
    MirrorExclusionLine
```

with `RootCertificate := ¬DimacsSatisfiable (interiorCnf 33 7 ++ upCubes.map negClause)` and
`UpCertificates := ∀ p ∈ upTable, ¬DimacsSatisfiable (cubeCnf (interiorCnf 33 7) p.2 ++ (casesOf p.1).map negClause)`
(§3 there). `V2L.axisInteriorLine_final` is sub-case (ii) alone. Axioms of both:
`[propext, Classical.choice, Quot.sound]`, pinned by `#guard_msgs` in `V2L/Audit.lean`.

**Tree certificates** (§9 there). `CTree` is `leaf | node (List (List Int × CTree))`;
`CTree.check` is `coverCheck` of every sibling list; `CTree.covers_of_check` proves that a checked
tree's leaves cover all assignments. `treeOf` gives one tree per case, generated from the wave
records at Zf (`scripts/gen_trees.py`): 310 cases get the tree `leaf` (172 direct, 138 whose empty
cube has a verified record), the other 140 have 73,690 leaves and 910 split nodes, depth ≤ 7,
1,050 sibling lists. `V2L.treeOf_check` (axioms: `propext`) proves every tree checks; each
sibling list is its own `decide +kernel` theorem, in 220 modules, 2,230 s CPU, 694 s wall, peak
2.98 GB per process. Hypothesis `hleaves` has 172 + 138 + 73,690 = **74,000** instances.

**Relation between the trees and the acceptance manifest** (§9.4 there): 0 tree leaves are
outside the manifest; 52 manifest leaves, all in U_L7, are not tree leaves: each strictly contains
a tree leaf (cubes below a node that was both closed and split). So 73,690 + 52 + 138 = 73,880.

**Trust base.** To read `V2L.mirrorExclusionLine_final` as the theorem of §1 one trusts:
1. The Lean kernel and the definitions `Point`, `GeneralPosition`, `ConvexPosition`,
   `HasConvexNGon` (main repository, `ErdosSzekeres/Definitions.lean`), `reflLine` (H3),
   `convexHull` (Mathlib), `DimacsSatisfiable` (H), `cubeCnf`, `coverCheck`, `hullCnf`,
   `interiorCnf` (H3), `hullLeaves` (V1-L), `negClause`, `RootCertificate`, `UpCertificates` and
   the data definitions `upCubes`, `upTable`, `caseTable`, `casesOf`, `treeOf` (V2-L).
2. **cake_lpr verdicts read as unsatisfiability of byte-identified files.** cake_lpr at
   a36874a8, `cake_lpr.S` sha256 `2f3af32d…72b7d4a`, verified in HOL4/CakeML down to x64; the
   trusted remainder is `basis_ffi.c`, gcc/ld and the OS (`results/V2-L/README.md` §6). A verdict
   `s VERIFIED UNSAT` on a file is read as `¬DimacsSatisfiable` of the Lean term whose DIMACS text
   that file is. CaDiCaL, march_cu and lrat-check (the patched version, and drat-trim's unpatched one, which is
   unsound: `results/E2/logs/lrat_check_soundness.md`) are not trusted. Where the verdicts are
   recorded: root and up:U in `results/Mii-S/cover_lrat.jsonl`; the 172 direct cases in
   `results/Mii-S/cases.jsonl` (`UNSAT_VERIFIED`); the other 138 + 73,690 tree leaves in the
   `leaves.jsonl` records under `results/WAVE1`–`WAVE4` at Zf; sub-case (i) as in
   `results/V1-L/SUMMARY.md` (`results/V2-L/README.md` §9.6).
3. **DIMACS emission.** `Emit.lean` (H3) and `V2L/DataEq.lean` are unverified string formatting.
   They reproduced, from the Lean terms, F's sha256, the 122 obligation CNFs (byte/sha256 equal to
   the files cake_lpr checked) and the 450 case CNFs (sha256 equal to `cases.jsonl`)
   (`results/V2-L/README.md` §5), and `hm33k7.sub.cnf` (`results/V1-L/README.md` §2).
4. **The drivers' leaf recording.** For the leaf facts, the per-leaf files were written by
   unverified Python ("case file + leaf units" in recorded order; `results/V2-L/README.md` §3, a
   grep over the 56 WAVE1 driver scripts; the drivers of WAVE2–WAVE4 were not checked this way),
   and the cubes in `treeOf` are the literal sequences of UNSAT records with `cake_lpr` exactly
   `s VERIFIED UNSAT` (§9.3). For sub-case (i) the same holds for the V1-0..V1-3 drivers and
   V1-L's backup driver `scripts/backup_leaves.py`, which checked 291 of the leaves
   (`results/V1-L/SUMMARY.md`, trust base item 3 and table).
   The V3 acceptance removes the dependence on the wave drivers' verdicts but not on file identity:
   its leaf CNF is F + case units + only the leaf literals not in the case cube, sorted by
   |literal|, while the Lean term `cubeCnf (cubeCnf F c) l` appends all of l's literals in recorded
   order. The two have the same set of clauses (duplicate unit clauses removed, order changed), so
   they are equisatisfiable, but they are not byte-identical and this step is not checked in Lean.
   A V3 leaf that contradicts its case cube is accepted without a solver call; the corresponding
   Lean term then contains complementary unit clauses and is trivially unsatisfiable. In the
   final table no leaf took this path (`results/V3Z/problems.txt`, n = 73,880 solved leaves).

## 7. Reproduction

**Commits** (new hashes):
- Zf, the commit at which every wave case is closed: 06c1f798cd8b8b066df804282f95e9ec075c4d99
  [old 14447d0d] (`results/FINAL/READY.json`).
- verify/v3: 92746acb [old bdf319c] (`results/V3Z/README.md`).
- V3Z table built at branch head 569b763f [old ff29bc68]; V3Z summary committed in 45bce6a0.
- V2-L tree data at Zf (`V2L/Trees/`, `scripts/gen_trees.py`): 8f3fdb83 [old 14fdad2c];
  `FinalTree.lean` last changed in 6ba4e377, which is also the new hash of e1d13c7b, the commit
  of the trial data cited in `results/V2-L/README.md` §9.5.
- Generator scripts of Mii-S: fef1a241 [old 6a44b5f] (`results/Mii-S/README.md`).
- The Python reference generators `tools/etv/gen_etv.py` and `results/C/scripts/mirgen.py` at
  3a04d94 (unchanged by the rewrite) (`results/H3/README.md`).
- This write-up's task: 852bee7.

**Tools** (`results/V3Z/tools.txt`, `results/Haudit/AUDIT.md` task 1):
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04;
- cake_lpr, https://github.com/tanyongkiam/cake_lpr commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa,
  `make cake_lpr` (bundled example prints `s VERIFIED UNSAT`);
- march_cu from CnC 705b60c6, built with `-fcommon`;
- Lean 4.24.0, Mathlib v4.24.0 (built from source; the Mathlib cache was blocked by the proxy).

**Commands.**
- F: `python3 tools/etv/gen_etv.py 33 7 7 7 --mirror -o m33k7.cnf; python3 results/C/scripts/mirgen.py m33k7.cnf 33 --interior --yflip-unit -o F.cnf`
  (sha256 69c1dc8f…932d), or `lake exe mir_dimacs interior 33 7 OUT` in `results/H3`
  (`results/V3Z/tools.txt`, `results/V2-L/README.md` §1).
- Cases: `results/Mii-S/scripts/hullsplit.py` (`cases`, `cubes`, `case F U L`); obligations:
  `results/Mii-S/scripts/cover.py`.
- Manifest at Zf: `v3_jsonl_leaves.py ROOT results/WAVEk jtreek` for k = 1..4, then
  `v3_manifest.py ROOT M.jsonl C.jsonl results/WAVE1 jtree1 results/WAVE2 jtree2 results/WAVE3 jtree3 results/WAVE4 jtree4`
  (`results/FINAL/READY.json`).
- Leaves: `v3_check.py --root ROOT --base F.cnf --manifest M --shard I --nshards N --out OUT --skip-covers --work W --jobs 4 --cap 1800`
  (`verify/v3/README.md`, `results/V3B/TASK.md` step 4); covers: the same with `--skip-leaves
  --jobs 4 --cap 3600` (`results/V3Z/README.md`); table: `results/V3Z/scripts/run_aggregate.sh`.
- Lean: `lake build` in `results/H`, `results/H3`, `results/V1-L`, `results/V2-L` (sharing H's
  `.lake/packages`); trees: `python3 -I scripts/gen_trees.py R OUTDIR` in `results/V2-L`
  reproduces `V2L/Trees/` byte for byte (`results/V2-L/README.md` §9.6).

**Compute used** (as recorded; there is no single total for the waves in the repository):
- Machines: 4-core, 15 GB cloud VMs throughout (`env.txt` files). Wave machines: 36 + 12 + 26 + 75
  = 149; acceptance machines: 1 (V3T) + 9 + 16 + 16 + 24 + 8 (V3A–E) + 1 (V3Z) = 75.
- Acceptance of the 73,880 wave leaves: 1,353,233 s (375.9 h) CaDiCaL and 301,295 s (83.7 h)
  cake_lpr, summed over the `solve_s` and `check_s` columns of `results/V3Z/accepted_final.tsv`.
  These columns count one VERIFIED record per leaf plus the cover proofs
  (`results/V3Z/scripts/aggregate_final.py`); repeated runs of the same leaf in V3A–V3E are not
  counted, so the V3 compute actually spent is larger.
- Covers and direct cases: 122 obligations 503 s + 222 s (Mii-S) and 515 s + 313 s (Haudit
  rerun); 172 direct cases 443 s + 331 s (Mii-S) and 699 s + 445 s (Haudit).
- Sub-case (i) leaves: CaDiCaL 26,142 s, cake_lpr 4,608 s (`results/V1-L/SUMMARY.md` table).
- Lean kernel check of the trees: 2,230 s CPU, 694 s wall (`results/V2-L/README.md` §9.5).
- Wave solving time is recorded per record in the `leaves.jsonl` files of `results/WAVE1`–`WAVE4`
  and was not summed for this note.

## 8. Numbers and their sources

The same table is in `NUMBERS.tsv`.

| number | value | source |
|---|---|---|
| points | 33 | statement |
| F variables / clauses | 47,002 / 515,121 | `results/H3/README.md` §3; `results/V2-L/README.md` §1 |
| F sha256 | 69c1dc8f…932d | `results/V3Z/tools.txt` |
| F free orbits | 2,736 | `results/C/README.md` |
| sub-case (i) CNF variables / clauses | 47,002 / 535,454 | `results/H3/README.md` §3 |
| sub-case (i) leaves (Lean) | 1,198 | `results/V1-L/SUMMARY.md`; `verify/README.md` |
| sub-case (i) leaves verified | 1,198 | `results/V1-L/SUMMARY.md` |
| sub-case (i) leaves, earlier H3 list | 5,589 | `results/H3/README.md` |
| hull cases | 450 | `results/Mii-S/soundness.md` |
| 4-gon / 6-gon cases | 30 / 420 | `results/Mii-S/soundness.md` |
| cases by U size 0/1/2 | 120 / 225 / 105 | `results/Haudit/AUDIT.md` task 2 |
| vacuous cases | 56 | `results/Haudit/AUDIT.md` NOTE-3 |
| cube length | 61–535 literals | `results/Mii-S/README.md` §1 |
| upper chains U | 121 | `results/Mii-S/soundness.md` |
| split obligations | 122 | `results/Mii-S/cover_lrat.jsonl`; `results/Haudit/t3_cover_lrat.jsonl` |
| direct cases | 172 | `results/Mii-S/cases.jsonl`; `results/Haudit/t5_all172.jsonl` |
| wave cases | 278 | `results/Mii-S/cases.jsonl` (OPEN); `results/FINAL/READY.json` |
| manifest leaves | 73,880 | `results/FINAL/READY.json`; `results/V3Z/inputs.txt` |
| leaves verified by V3 | 73,880 | `results/V3Z/problems.txt` |
| covers verified | 278 (140 cake_lpr + 138 empty cube) | `results/V3Z/README.md`; `results/V3Z/covers.jsonl` |
| wave cases accepted | 278 | `results/V3Z/accepted_final.tsv` |
| SAT records | 0 | `results/V3Z/problems.txt` |
| leaf records read / REJECTED | 75,459 / 1 | `results/V3Z/README.md` |
| cover records VERIFIED / NOT_COVERED | 377 / 9 | `results/V3Z/README.md` |
| solve median / max per leaf | 10.9 s / 730.0 s | `results/V3Z/problems.txt` |
| check median / max per leaf | 3.0 s / 52.0 s | `results/V3Z/problems.txt` |
| tree leaves (hleaves) | 74,000 | `results/V2-L/README.md` §9.6 |
| non-trivial trees / their leaves / split nodes | 140 / 73,690 / 910 | `results/V2-L/README.md` §9.3 |
| sibling lists / modules | 1,050 / 220 | `results/V2-L/README.md` §9.5 |
| manifest leaves not in a tree | 52 (U_L7) | `results/V2-L/README.md` §9.4 |
| largest tree | U_L2, 22,529 leaves | `results/V2-L/README.md` §9.3 |
| wave machines | 36 / 12 / 26 / 75 | `results/WAVE1`–`WAVE4` directory listings |

## 9. Where the files disagree or have been superseded

- **Status lines written before the end.** `results/H3/README.md` says sub-case (ii) is open
  (1,340 open cubes); the first paragraph of `results/V2-L/README.md` gives 316/450 closed at
  10:20 UTC; `verify/v3/README.md` ends "Not yet reviewed or tested by an independent agent";
  `results/Haudit/AUDIT.md` RISK-2 says the clause-cover lemma "is not written yet";
  `results/Mii-S/README.md` says "Nothing here is a claim that sub-case (ii) is closed". All are
  snapshots superseded by V2-L §9, V3T and V3Z.
- **Leaf counts.** V2-L's tree hypothesis has 74,000 instances; the manifest has 73,880 wave
  leaves, which with the 172 direct cases is 74,052 (`results/V2-L/README.md` §7a). The difference
  is the 52 U_L7 leaves of §6. V2F's per-record assembly closed only 411/450 cases with 74,031
  leaves, because of record formats of 39 WAVE2 directories of machines S1–S5 (§7a there); the directory-level rule
  closes 450/450.
- **Timings of the same checks.** 122 obligations: 503 s CaDiCaL / 222 s cake_lpr
  (`results/Mii-S/README.md`) against 515 s / 313 s (`results/Haudit/AUDIT.md`, a rerun). 172
  direct cases: 443 s / 331 s (Mii-S) against 699 s / 445 s (Haudit). Different runs, same verdicts.
- **`results/Mii-S/pass2_lrat.jsonl`** has 174 records for 174 cases, of which 172 carry
  `s VERIFIED UNSAT` and 2 no cake_lpr field; `results/Mii-S/cases.jsonl` lists exactly 172 as
  `UNSAT_VERIFIED`.
- **Geometric test coverage.** 279 distinct cases hit (Mii-S) against 394 (Haudit); different tests.
- **Vacuous cases.** `results/Haudit/AUDIT.md` NOTE-3 states the rule as "2 ∈ U or 3 ∈ L",
  which matches 57 cases; its count 56 and `results/Haudit/t4_summary.txt` ("U2.. or L3..")
  exclude U = ∅, L = {2, 3} (§4).
- **Sub-case (i) normal form.** `results/H3/README.md` §2 calls both `rotA` and `rotB` a
  rotation; `rotB` (x, y) ↦ (y, x) is a reflection (`Frame.lean`, `orient_rotB`) (§3).
- **Related work.** For Koshelev–Koshka (arXiv:2604.20120) the 14 Oct survey records a mention
  of axially symmetric 18-point sets; `results/LIT/RELATED.md` §3 found in the snippets only a
  25-point 3-fold example for a hexagon-type variant (§1).
- **Leaf literal order.** The Lean leaf terms and the V3 rebuilt files differ in unit-clause order
  and duplicates (§6, item 4).
