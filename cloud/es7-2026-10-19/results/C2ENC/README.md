# C2ENC: soundness of the central encoder

Local work on an Apple M5 Pro, 1 November 2026 (UTC). Paths are relative to `cloud/es7-2026-10-19/results`, except
`proof.md`, `perturbation.md`, `class_table.md`, `tests/` and `referee/`, which are in this directory.

**Statement** (`proof.md`, Theorem 1). Let S be a set of 34 points in general position that is invariant under a
half-turn about a point c and has no 7 points in convex position. Then for every vertex p₀ of conv(S), the normal-form
labelling from p₀ exists and is unique, and its real assignment satisfies every clause of the base CNF written by
`SYMZ/zcnf.py rot 17 7 --m 2 --hull` (`p cnf 838032 16653336`, SHA-256 `b0061e90…fd8ff1`; map `2476faff…`).
Consequences:
- if the base plus a cube is UNSAT, no labelled configuration lies in the class of the cube (Corollary 2);
- a certified cover of the base places every labelled configuration in the class of one of its cubes (Corollary 3);
- a certified cover inside a cube Q places every labelled configuration of the class of Q in the class of one of its
  subcubes (Corollary 3′). This is the form of the second-layer covers inside a hull cube.

**Status.**
- Complete written proof, refereed. The referee found it sound, with minor documentation gaps and no blocking or major
  finding (`referee/NOTES.md`). The fixes the referee asked for are applied here (§4).
- **Not Lean-checked.** The step from the certificates to the Lean class `HalfTurn34` rests on this proof, on the case
  split and on the certificates (`class_table.md`).
- Computational evidence, exact: a specification match of all 16,653,336 clauses, evaluation of real labellings on the
  full base, and mutation tests; the referee added nine mutants and two independent evaluators (§3).
- Not proved here: any UNSAT verdict; the geometric meaning of the cubes; reductions A and B; the bookkeeping of
  `C2FINAL`; the threefold, fivefold and mirror encoders.

**Credit.** The model is a relaxation by orientation signs, in the line of the computer proofs of ES(6) = 17
(Szekeres–Peters 2006, a model of signature functions; Marić 2019) and of the SAT encodings of Heule–Scheucher (TACAS
2024) (`LIT/RELATED.md`). SAT encodings with built-in rotational symmetry were used for 7-gon-free sets by
Subercaseaux, Mackey, Qian and Heule (arXiv:2506.00224, CICM 2025; fourfold, 32 points), the closest prior symmetric
study (`LIT/RELATED.md` §3). The clause families of the model are standard: Knuth's interiority axiom (*Axioms and
Hulls*, 1992), the three-term Grassmann–Plücker relations, and the four-point criterion for convex position
(Carathéodory's theorem). B. C. Dumitru's SAT encoding of the 33-point problem (arXiv:2512.24061) uses the same kind of
variables, triple orientations with the four-point criterion. A soundness proof of an encoding has a formal precedent:
Subercaseaux, Nawrocki, Gallicchio, Codel, Carneiro and Heule (ITP 2024, arXiv:2403.17370) verified in Lean the encoding
behind h(6) = 30. The proof here is written, not formal. The encoder is the project's `SYMZ/zcnf.py` (last changed 29
October 2026).

## 1. Files

| file | content |
|---|---|
| `proof.md` | the proof: normal form (Lemma 4), variable classes and literal meaning (Lemmas 5, 6), one proposition per clause family (Propositions 7–11), Theorem 1 and Corollaries 2, 3, 3′; adversarial checklist (§7); computational evidence (§8) |
| `perturbation.md` | the centre-perturbation lemma for odd rotation orders, used by `Threefold33` and `Fivefold35` (not needed for the half-turn), with an exact illustration for m = 3 |
| `class_table.md` | from certificates to the five Lean case classes: encoder, normal form, soundness document, certificates and weakest link of each |
| `tests/` | the test scripts, their logs (`tests/logs/`) and result summaries (`tests/mut/summary*.json`, `tests/work_full/results.json`); `tests/zcnf_orig.py` is a byte-identical copy of `SYMZ/zcnf.py` (`13d6c162…`) |
| `referee/` | the referee's notes, scripts and logs |
| `SHA256SUMS` | SHA-256 of every other file in this directory |

## 2. The proof in brief

- **Normal form** (Lemma 4). Put X₀ = p₀ and X₁ = h(p₀). Every other pair has exactly one point in the open half-plane
  to the left of c → X₀; these 16 representatives are sorted by angle about c and labelled X₂, X₄, …, X₃₂, and
  X_{2o+1} = h(X_{2o}). The labelling exists and is unique for every hull vertex p₀. No perturbation of the centre is
  needed: by general position, the only collinear triples through c are {c, p, h(p)} (Lemma 3).
- **Variables** (§4). Over the 6,528 nonzero triples, the half-turn identity (det +1, fixing c) and the centre identity
  χ(c, p, q) = χ(h(p), p, q) give 2,856 sign classes: 2,720 orbits {T, h(T)} and 136 classes of 8 triples, whose signs
  are the angular order about c. A union-find with signs builds them, and its invariant is proved (Lemma 5). Under the
  real assignment every literal is true exactly when its triple is counter-clockwise (Lemma 6).
- **Clause families** (§5). Grassmann–Plücker 12,588,160; interiority 413,440; convexity definitions 950,912; no convex
  7-gon 2,689,808; angular order 136 units; first point on the hull 10,880. The sum is the header count. Each family is
  satisfied by the real assignment; only the 7-gon clauses use "no convex 7-gon", and only the hull clauses use "p₀ is a
  hull vertex".
- **Covers** (Corollaries 3 and 3′). A certified cover needs no geometric argument. The certificate alone places every
  labelled configuration in some cube's class, both for the 136 hull cubes and, inside the hull cube of P_a, for the
  second-layer cubes (`C2C34/p8/mkunits.py`, `C2P/tools/lane.py`).

## 3. Tests and what they can detect

All geometry is exact (Python integers; `tests/count7.c` with 64-bit integers below 2³⁰). `tests/evalcnf.c` evaluates
clauses under assignments computed exactly in Python.

| test | what it checks | result | what it would detect |
|---|---|---|---|
| `identities.py` | symbolic expansion of every polynomial identity of the proof: GP, interiority (also weighted), the centre identity, the zero triple, half-turn invariance, the sign change across a line through c, the barycentric identity, orient = det | all expand to 0 (`identities.log`) | four false variants leave nonzero residuals (36, 24, 6 and 6 terms): GP with the middle sign +, interiority without first coordinate 1, centre identity with the wrong sign, a reflection (det −1) |
| `classes.py` | the base map against the hand-derived partition (2,720 + 136 classes) and relative signs; the triples missing from the map are exactly the 17 zero triples; 2,856 + 835,176 = 838,032 variables | passed (`mapcheck_base.log`) | a wrong identification or sign; the mutant with the wrong centre identity fails it |
| `spec.py` | each family regenerated from §5 and compared with the CNF as a multiset (count, sum and XOR of 128-bit hashes, length histogram) | all 8 families match on the full base (`spec_base.log`) and on 16 small instances (`spec_small.log`) | a missing, extra or changed family; it is the only test that catches the missing interiority family (the missing GP family is also caught by the t = 9, K = 6 instance). It shows coverage: for the GP generic path and interiority it enumerates as the encoder does (referee note R4) |
| `run_base.py` with `evalcnf` | the full base on 25 real 34-point sets, from every hull vertex (122 labellings) and from one non-hull point each (25 controls) | passed (`base_full.log`, 720 s, peak RSS 1.41 GB). In every hull labelling the violated clauses are exactly the 7-gon clauses of the canonical convex 7-sets, matched by clause index: from 1 clause (five near-extremal sets built from `SYM2/sym7_32points.txt`) to 1,375,883 | any clause of any family that a real configuration violates. In the controls, the number of violated hull clauses (216 to 1,198) equals the number of triangles containing p₀; the script compares the number, not the clauses (referee note R2) |
| `mutate.py` | 12 deliberate defects of the encoder, each at t = 4, 5, 6 with `--hull`, t = 5 without the normal form, and t = 8 with K = 7: real labellings, a two-way SAT test (CNF plus the real triple values must be SAT), map check, spec comparison, and for weakening defects the known-UNSAT instance t = 9, K = 6 | `mutation.log`, `mut/summary.json`; table below | see below |
| `famviol.py` | violated clauses of 7 defects (8 runs) attributed to their families (t = 5, K = 6) | `famviol.log` (the last line, with an empty name, is the unmodified encoder: 0 violations) | which family a defect breaks |
| `a4redundancy.py` | whether interiority follows from the other clauses at t = 4, 5, 6 without 7-gon clauses and without the normal form (K = 2t + 1, `--no-sb`) | each of the 8,128 positive circuits that the interiority clauses forbid gives UNSAT when forced (`a4redundancy.log`; its line for `mut/original` used `--sample 200`, the others `--all`) | explains why a missing interiority family is invisible to every semantic test (evidence, not proof) |
| `perturb3.py` | exact illustration of the perturbation lemma for m = 3 (Eisenstein coordinates) | 30 sets, 3 or 6 pairs collinear with c before and 0 after, all orientation signs and convex-subset counts kept (`perturb3.log`) | an orbit rotation that changes the order type or leaves c non-generic |

**Mutation tests** (`tests/logs/mutation.log`). The unmodified encoder gives 0 violated clauses in all 114 labellings,
every two-way test SAT, map and spec checks passed, and t = 9, K = 6 UNSAT.

| defect | how it is caught |
|---|---|
| centre identity with the wrong sign | map check; every labelling violates interiority clauses (and the angular units when present), never GP; every two-way test UNSAT |
| no zero triples | the encoder's own contradiction check |
| two extra zero triples | with the normal form, the encoder's own assertion; without it, map check, GP violations in every labelling, two-way UNSAT |
| cyclic angular order | with the normal form, every labelling violates an angular unit, every two-way test is UNSAT and spec flags the units (without the normal form there are no units to break) |
| hull clauses anchored at X₂ | 62 of 90 labellings violate hull clauses; two-way UNSAT in most configurations; spec flags the family |
| interiority missing | **sound** (a weakening): spec only; t9k6 stays UNSAT |
| interiority with the wrong sign | every labelling; two-way UNSAT |
| GP middle coefficient +1 | every labelling; two-way UNSAT |
| GP missing | **sound** (a weakening): spec; t9k6 becomes SAT with a model that violates GP in 9,164 instances |
| half-turn with det −1 | the encoder's own contradiction check |
| convex (K−1)-gons forbidden | every labelling; two-way UNSAT; at K = 5 the encoder crashes |
| a non-convex 4-point pattern counted as convex | most labellings; two-way UNSAT for some configurations in every instance |

Every unsound defect is caught by real labellings together with a two-way UNSAT, or by the encoder's own checks.
Defects that bite only on some geometries (the hull anchor, the 4-point pattern) are caught per instance, not per
labelling.

**The referee's own tests** (`referee/`).
- Four of the authors' mutants, re-run in a copy of the authors' harness: output byte-identical
  (`mutation_rerun_authors.log`).
- Nine additional mutants, run through the same harness, on code paths the authors' set did not touch
  (`scripts/refmutants.py`, `mutation_new_mutants.log`). Caught in every instance that emits the defective family (all
  labellings violate, all two-way tests UNSAT, spec flags): the GP generic path ignoring polarity (5-sets with c), one
  sign in a GP fast-path clause, the hull orientation χ(a,d,X₀) for χ(d,a,X₀), and the interiority sign on 4-sets with
  c only. Rejected by the encoder's own checks: a parity bug and a wrong centre identity for p = 0 only. Equivalent: a
  sign bug in path compression, since union-find paths never exceed length 2 for t = 4..9 and t = 17 (`ufdepth.log`).
  Sound controls behave: hull clauses anchored at X₁ give an identical clause multiset, and allowing c as a triangle
  vertex is flagged by the spec comparison only.
- `scripts/refeval.py`, an evaluator that shares no code with `tests/` (own labelling, own convexity test, expected
  violations derived clause by clause): the original passes 383 labellings at 8 size and option combinations; 7 of 7
  unsound mutants fail; the 3 sound or equivalent ones pass (`refeval.log`).
- `scripts/refbase.py`, an independent evaluator of the full base (streamed, 33 s, peak RSS 1.17 GB): 9 labellings of
  3 configurations; the violated-clause multiset equals the prediction exactly, including 1 clause of 16,653,336 for a
  near-extremal set and, for three non-hull controls, the identity of the hull clauses (`refbase.log`).
- `scripts/conv4stats.py`: of the 16 sign patterns on 4 points, the kept ones are exactly the 6 convex ones (`n_in` = 0,
  1, 4 for 6, 8, 2 patterns, the last two not realizable).

**Re-run from this layout** (1 November 2026, UTC, after the edits of §5). A copy of this directory was placed in a
tree that mirrors `results/` with `SYM2/sym7_32points.txt`, and the scripts were run from there with CaDiCaL 3.0.1.
- Byte for byte, these reproduced their logs: `identities.py`, `run_spec_small.sh`, `perturb3.py 30`, `classes.py` on
  the base map (`mapcheck_base.log`), `mutate.py` (all 12 defects and the control: `mutation.log`, `mut/summary.json`),
  `mutate.py original` (`mutation_original.log`, `mut/summary_original.json`), the nine runs of `famviol.py`
  (`famviol.log`), and the referee's two mutation runs, `ufdepth.py` and `conv4stats.py`.
- `spec.py` on the full base reproduced `spec_base.log` except the timings and the last line, `done`, which the original
  wrapper printed.
- `a4redundancy.py` reproduced each of the five result lines of its log. The CNFs of its t = 4, 5, 6 lines, written by
  the commands under Reproduction, are byte-identical to those of the original run.
- `refeval.py` reproduced its verdicts and counts on the original (t = 5, K = 6, seed 3) and on two unsound mutants
  (`conv4_pattern`, `hull_orient`); its output line names the encoder's directory, here `tests` instead of `work`.
- The full-base evaluations (`run_base.py`, `referee/scripts/refbase.py`) were not repeated.

## 4. The referee's findings and their resolution

The referee (1 November 2026) listed the clause families from the code before reading the proof, re-derived every
lemma and proposition, and ran the tests above. Verdict: sound, with minor documentation gaps.

| # | severity | finding | resolution |
|---|---|---|---|
| R1 | minor | Corollary 3 states covers of the whole base only; the second-layer covers are covers inside a hull cube (base, hull-cube units, one clause ¬(L_i ∖ Q) per subcase) | `proof.md` Corollary 3′ (statement in §0, proof in §6): if base ∧ Q ∧ ⋀ᵢ ¬(L_i ∖ Q) is UNSAT, every configuration in the class of Q lies in the class of some Q ∪ L_i; dropping the literals of Q from ¬L_i is equivalent under the units of Q. §0 and §6 now cite it; `class_table.md` cites it for the second-layer covers |
| R2 | note | §8.3 says the non-hull controls violate "exactly the predicted" hull clauses, but `run_base.py` compares only their number | §8.3 says what is compared and cites the referee's clause-identity check on three full-base controls (`referee/logs/refbase.log`); the docstring of `tests/run_base.py` says the same |
| R3 | note | Lemma 8 justifies equal signs "by the barycentric identity", which gives only the sum; `perturbation.md` (P2) repeats this | `proof.md` §1 now has a paragraph on barycentric coordinates: by Cramer's rule they are D(b,d,q)/D(a,b,d), D(d,a,q)/D(a,b,d), D(a,b,q)/D(a,b,d), and equal signs follow from their positivity. Lemma 8, Proposition 11 and (P2) cite it |
| R4 | note | `spec.py` shows coverage; for the GP generic path and interiority it mirrors the encoder's enumeration | `proof.md` §5.6 and §8.2 say so, and correctness is attributed to Propositions 7–11 and the semantic tests; the docstring of `tests/spec.py` states the scope |
| R5 | note | path compression in the union-find never rewrites an interior node at these sizes, so a bug there would be invisible | no change needed: Lemma 5 covers the branch, and `classes.py` validates the base map independently |
| R6 | note | Lemma 4 says "at least 3 vertices … even", meaning at least 4; the remark that a short-circuit keeps `tau` away from Z is moot | Lemma 4 now concludes "at least 4 vertices"; the remark (§2) and the checklist row (§7) now say that `is_zero` applies `tau` only to elements other than Z |
| R7 | note | §1 identifies the Lean notions of general and convex position with the orientation notions informally | no change needed: the step from the certificates to `HalfTurn34` is declared not Lean-checked (`proof.md` §9) |
| R8 | note | `class_table.md`: "8 × 287 orbit representatives closed by 2,385 UNSAT records" could be read as a count identity | rewritten: 8 × 287 = 2,296 orbit facts plus 8 covers, each with an UNSAT record carrying both verdicts; 2,385 of the 2,492 records are UNSAT, an orbit may have several, and the two counts are not meant to match |

## 5. Other changes for the repository

- **Versions.** The referee read `proof.md` `ae379b45…`, `perturbation.md` `28fbbd6a…` and `class_table.md`
  `d7d7c9fc…`. The files here are the revised versions (`SHA256SUMS`). Besides the fixes of §4, the documents now give
  paths relative to `cloud/es7-2026-10-19/results`, name the audit `AUDIT3`, and use impersonal wording.
  `perturbation.md` also notes that the mirror classes are proved in Lean (`class_table.md` §2).
- **`class_table.md`.** The mirror classes point to their Lean proof from Baek's theorem (`SYMLEAN/mirror`; J. Baek,
  Eur. J. Combin. 124 (2025) 104085, arXiv:2206.04260, Theorem 1.6 in the arXiv numbering), with the SAT certificates of
  `SYMZ` as an independent confirmation; the value 16 that the mirror bound uses was reported earlier by SAT by Balko
  and Valtr (2015; `MIRRORETV`). `HalfTurn34`, `Threefold33` and `Fivefold35` point to their certificates (`C2FINAL`
  with `C2C34`; `C3FINAL` with `C3LEAN` and `C3SPOT`; `SYM5` and `WRITEUP/CERTIFICATES.md`). The `Fivefold35` row
  credits the computation reported by B. C. Dumitru (arXiv:2512.24061, §7, Table 1) and says that its two certificates
  come from two normal forms of one encoder (`AUDIT3`, A4-3). The Lean file states six case classes; the table now says
  that the main theorem uses five of them.
- **Scripts.** Only path lines changed, so that they run from this directory: CaDiCaL is taken from `$CADICAL` (default
  `cadical`) in `mutate.py` and `a4redundancy.py`; the results directory is `../..` in `mutate.py` and `run_base.py`;
  `run_spec_small.sh` creates `cnf/`; `referee/scripts/run_refmut.py` (from the referee's private `work/`) imports the
  harness from `../../tests`. Docstrings changed in `run_base.py` (R2), `spec.py` (R4), `refeval.py` and `refbase.py`
  (directory name). SHA-256 of the versions that wrote the logs: `mutate.py` `4fd1cffc…`, `a4redundancy.py`
  `ff04597e…`, `run_base.py` `323c2392…`, `spec.py` `792ca96e…`, `run_spec_small.sh` `9053737e…`, `refeval.py`
  `372bdf11…`, `refbase.py` `364192ae…`, `run_refmut.py` `1a4a785f…`.
- **Logs.** Machine-specific path prefixes were removed from `base_full.log`, `base_quick.log` and `regen_base.log`;
  in the last, `REF/` stands for the directory of the reference copies of the base CNF and map. Nothing else changed.
  The referee's two timing files were renamed after the logs they belong to.
- **Not copied.** CNFs and the small maps written by the tests (all regenerable), the compiled `evalcnf` and `count7`,
  the mutant copies of the encoder (written by `mutate.py`), and the referee's private copy of `tests/`.

## 6. Scope

- `proof.md` is a complete written proof, refereed. It is not Lean-checked, and no formal link joins the CNF to the
  Lean class `HalfTurn34`.
- It does not establish any UNSAT verdict. Those rest on the certificates and their checkers (`C2C34`, `C2FINAL`,
  `WRITEUP/CERTIFICATES.md`).
- The model is a relaxation: a satisfying assignment need not be realizable by points, and only UNSAT answers are used.
- `perturbation.md` is a complete written proof, refereed, not Lean-checked. `class_table.md` records where the trust of
  each Lean class lies; its status entries are as of 1 November 2026.

## Reproduction

From `cloud/es7-2026-10-19/results`, with `W` a scratch directory outside the repository (the base CNF has 621 MB):

```sh
python3 SYMZ/zcnf.py rot 17 7 --m 2 --hull -o $W/base.cnf --map $W/base.json   # b0061e90…, 2476faff…
cd C2ENC/tests
cc -O2 -o evalcnf evalcnf.c && cc -O2 -o count7 count7.c   # the machine used also needed -isysroot (macOS 26 SDK)
export CADICAL=/path/to/cadical                       # CaDiCaL 3.0.1
python3 -I identities.py                              # about 1 s
python3 -I classes.py $W/base.json
./run_spec_small.sh                                   # 16 small instances, about 7 s
python3 -I spec.py $W/base.cnf $W/base.json --hull     # about 100 s, peak RSS 227 MB
python3 -I run_base.py $W/base.cnf $W/base.json work_full   # 720 s, peak RSS 1.41 GB
python3 -I mutate.py                                  # about 44 s; writes the defective encoders mut/*/zcnf_mut.py
for m in identity_sign zero_extra gp_sign a4_sign conv4_pattern; do
  python3 -I famviol.py mut/$m/zcnf_mut.py 5 6 --no-sb; done
for e in mut/identity_sign/zcnf_mut.py mut/angular_cycle/zcnf_mut.py mut/hull_anchor/zcnf_mut.py zcnf_orig.py; do
  python3 -I famviol.py $e 5 6 --hull; done           # the nine lines of famviol.log
python3 -I a4redundancy.py mut/a4_missing/t5k6_no-sb.cnf mut/a4_missing/t5k6_no-sb.json --all
python3 -I a4redundancy.py mut/original/t5k6_no-sb.cnf mut/original/t5k6_no-sb.json --sample 200
for t in 4 5 6; do
  python3 -I mut/a4_missing/zcnf_mut.py rot $t $((2*t+1)) --m 2 --no-sb \
    -o mut/a4_missing/noK_t$t.cnf --map mut/a4_missing/noK_t$t.json > /dev/null
  (cd mut/a4_missing && python3 -I ../../a4redundancy.py noK_t$t.cnf noK_t$t.json --all); done   # about 75 s
python3 -I perturb3.py 30                             # about 17 s
```

`run_spec_small.sh`, `mutate.py`, `famviol.py` and the loop above write small CNFs under `tests/cnf/` and `tests/mut/`;
they are not part of the repository. The referee's commands are in `referee/NOTES.md` §6; `referee/scripts/refbase.py`
needs numpy. Further commands for single tests are in `proof.md` §8.5.
