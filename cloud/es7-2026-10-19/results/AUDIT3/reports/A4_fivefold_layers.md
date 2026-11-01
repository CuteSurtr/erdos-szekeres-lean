# A4: fivefold, layer lemma and the even-m layered encoder

Component audit, 1 November 2026 (UTC), against `es7-cloud` at 9cf4949a5. Texts returned by the auditor and by the independent verifier of each finding, lightly edited: machine paths replaced by placeholders and internal job names by descriptions; trust-table labels as explained in `../README.md`, §7. "Bogdan" below is B. C. Dumitru, the author of arXiv:2512.24061 (`../README.md`, §5 row 7).

**Component.** FIVEFOLD >= 35, the layer lemma, and the even-m layered encoder (SYM5 + C4CUT)

**Statement audited.** Every set of at least 35 points in general position with a rotation of order 5 contains 7 points in convex position (SYM5: reduction to 35 centre-free points, angle-form CNF P1 and layer-form CNF L1, both UNSAT). This includes: the layer lemma (rotation of order m >= 4, no convex K-gon, K <= 2m, so every convex layer is one orbit); soundness of symcnf.py and symcnf_layers.py (m = 5 with an auxiliary centre, m = 4 without a centre); the six C4CUT realizability cuts; and the chain to the UNSAT certificate for the fourfold 32-point formula.

**Verdict.** `sound_with_caveats`

## Summary

Verdict: sound with caveats. I found nothing blocking or major. Five minor findings are about documentation and record-keeping, and none threatens the claim.

Layer lemma: true. I proved it in full (finding A4-7). The proof uses m >= 3 for the centre being interior, K <= 2m for "two orbits would form a K-gon", and general position only for strict nesting. If the centre is in the set, {c} is the last layer. The centre is strictly inside every layer polygon, which is exactly what the layer units assert. The note's lemma is correct but omits the nesting facts the encoder uses (A4-2).

Fivefold coverage: complete. A fivefold set has 5t or 5t+1 points, so sizes 33 and 34 do not exist. Any larger set, with or without the centre, reduces to a 35-point centre-free set by deleting the centre and whole orbits. P1 (angle form, no layer lemma) and L1 (layer form) each settle that case. Both regenerated CNFs are byte-identical to the solved ones. Both checkers' verdicts are recorded in the logs and the archived proofs match their hashes; I did not replay the checkers, because the audit rules forbid it at that size.

Encoders: sound by clause-by-clause argument, and my own exact Z[zeta5]/integer tests found no violation:
- 4,415 evaluations on random sets and 5,688 on the extremal sets and all their whole-orbit subsets.
- The solved 35- and 32-point formulas themselves, on real configurations of that size: only the 7-gon clauses are violated, exactly (#convex 7-sets)/m of them.
- All 1,750+ wrong labellings were caught.
- An adversarial test confirms the per-orbit rotation argument for the auxiliary centre.
- For even m (the fourfold encoder), the labelling exists by plain general position, but that argument is never written down (A4-1).

C4CUT cuts: the soundness argument is correct, and my own checker re-verified all six certificates (A4-9). The chain base -> base+cuts and the archive hashes reproduce. Which checker binaries C4CUT used is not recorded (A4-5); this matters because the upstream lrat-check is known to accept a forged proof.

Other minor points:
- The two fivefold encodings share all but about 150 unit clauses, so "independent" overstates it (A4-3).
- Several documents still describe the fourfold case as pending review or as resting on the published enumeration (A4-4).

Structural observation (A4-6): once the central-34 result holds, the fourfold case follows from it, because a rotation of order 4 contains the half-turn. So C4CUT is off the critical path. The fivefold case is not implied by any other case and is essential.

All scripts, logs and regenerated CNFs are in AUDIT3/A4_fivefold_layers/. The large regenerated CNFs (about 1.1 GB in big/ and work/) can be deleted; they regenerate in about a minute.

## Trust table

| # | claim | basis | notes |
|---|---|---|---|
| 0 | Layer lemma: let S be in general position, invariant under a rotation of order m >= 3 about c, with no K points in convex position, where K <= 2m. Then every convex layer is exactly one m-point orbit (with {c} as the last layer if c is in S). Every later point and c lie strictly inside each earlier layer polygon. | written proof, re-derived by the auditor | Full proof re-derived (finding A4-7). The note's Lemma lem:layers is correct but terse. Empirical check on 1,050 non-nested random sets: 0 violations. |
| 1 | Fivefold reduction: a 5-fold set has 5t or 5t+1 points, so sizes 33 and 34 are impossible. Every 5-fold set of >= 35 points, with or without the centre, contains a 35-point centre-free 5-fold set with no convex 7-gon. | written proof, re-derived by the auditor | Delete the centre, then delete whole orbits. Symmetry, general position and 7-gon-freeness are all inherited. |
| 2 | Odd m: rotating each orbit by its own small angle preserves the chirotope of the set and the symmetry, and puts the auxiliary centre in general position, so the sector normal form exists. | written proof, re-derived by the auditor | Adversarial exact test on 20 sets whose centre is collinear with points of two orbits: the normal form was undefined before perturbing, the chirotope was preserved exactly, and 400 CNF evaluations passed afterwards. |
| 3 | symcnf.py angle normal form (m = 5, auxiliary centre) is sound: every real configuration gives a model. | written proof, re-derived by the auditor | Checked clause family by clause family: triple-orbit signs, interiority, GP sign clauses, centre facts, convexity and K-set clauses, sector and order units. Exact evaluation with zero violations on random sets (N = 10..25), on the extremal sets, and on the full solved formula c5_n35.cnf. |
| 4 | symcnf_layers.py is sound for m = 5. | written proof, re-derived by the auditor | Rests on the layer lemma and the per-orbit perturbation. Exact tests at N = 10..25 and 30, and on the full solved formula c5_n35L.cnf: 0 violations, and all negative controls caught. |
| 5 | symcnf_layers.py is sound for m = 4 (no centre; sector cut out by the diameters of orbit 0). | written proof, re-derived by the auditor | The labelling exists without any perturbation, by general position, but the project never writes this argument down (A4-1). Exact tests at N = 8..24, 28 and 32 (full c4_n32L.cnf): 0 violations. |
| 6 | The solved CNFs are exactly the outputs of the reviewed encoders: c5_n35.cnf ead55228..., c5_n35L.cnf 90dea1cf..., c4_n32L.cnf c3933d9a... with map f72b186e..., and base+cuts 2aa18f1e... | exact computation (full regeneration) | Not a sample: a complete deterministic regeneration, byte-identical. base+cuts was rebuilt with my own appender. The archived .zst copies decompress to the same hashes. |
| 7 | c5_n35.cnf (angle form) is UNSAT (proof P1). | certificate accepted by both checkers (auditor's label) | Taken from the logs (lrat-check: c VERIFIED; cake_lpr with heap 30000: s VERIFIED UNSAT). The archived proof matches its recorded sha eff67c0f... Not replayed: the audit rules forbid loading CNFs > 50 MB and running cake_lpr. |
| 8 | c5_n35L.cnf (layer form) is UNSAT (proof L1). | certificate accepted by both checkers (auditor's label) | Taken from the logs (lrat-check and cake_lpr). The archived proof matches its sha 8625b321... and ends with an empty-clause step. Not replayed. |
| 9 | Each of the six C4CUT cut clauses is satisfied by every real labelled configuration. | written proof, re-derived by the auditor | The argument (biquadratic final polynomial on 3-term GP relations, using only signs and general position) is correct. I proved the GP identity symbolically. My own exact checker re-verified all six certificates. Each clause covers exactly the 55 inner triple-orbit variables. 36/36 mutations were rejected. |
| 10 | c4_n32L_cuts.cnf (base plus the 6 cuts) is UNSAT. | certificate accepted by both checkers (auditor's label) | From final.json and cad_c4cuts.out. The archived CNF and proof match 2aa18f1e... and 6e1199aa... Not replayed. The hashes of the checker binaries used are not recorded (A4-5). |
| 11 | Lower examples: c5_31points.txt is 5-fold, in general position (centre included) and has no convex 7-gon, so N(C5) >= 31. c4_28points.txt is the same for fourfold, so N(C4) >= 28. | exact computation (auditor's own code) | Checked in full with my own exact Z[zeta5] and integer code: largest convex subset 6 in both, and every convex layer is one orbit. The project's verify5.py was not rerun. |
| 12 | The fourfold case follows from the central-34 theorem (C4 contains C2). The fivefold case is not implied by any other case. | argument only | Observation of this audit (A4-6). |
| 13 | Bogdan's reported 33-point UNSAT run implies the fivefold bound. | not assessed | I inspected neither his generator nor his paper. This is a prior-work remark only and does not bear on the certificates. |

## Findings

### A4-1 (minor): Even-m sector normal form: the argument that every real set has such a labelling is never written down

For even m, symcnf_layers.py (and symcnf.py) pin each inner orbit's representative (o,0) to the open sector (0, 2pi/m) cut out by the m/2 diameters (0,j)(0,j+m/2) of orbit 0. Soundness needs every real fourfold set to admit this labelling, i.e. no point of another orbit lies on such a diameter. The project only asserts it ('sound: every realizable symmetric set has such a labelling', symcnf.py docstring). The perturbation argument of SYM5/README.md §1 covers only odd m with the auxiliary centre, and it cannot be copied for even m, because the centre cannot be added there. The fact is true and needs no perturbation: (0,j+m/2) = 2c - (0,j), so a point of another orbit on that line would make three points of S collinear. Neither C4CUT/README.md nor C4CUT/review states this. The review checked the signs of the sector units, not that the labelling exists.

*Evidence.* SYM5/symcnf.py docstring lines 38-48; SYM5/README.md §1 (odd m only); C4CUT/review/README.md. My m = 4 exact tests (720 labellings in random runs, 956 on c4_28points, 5 full N=32 configurations) found no violation.

*Suggested fix.* Add the one-line collinearity argument to SYM5/README.md §4 and C4CUT/README.md §1.

**Independent check:** real = yes; severity minor -> **minor**.

The finding is correct, and minor is the right severity.

(1) The certificate really does depend on this labelling. I took the 142 unit clauses from the C4CUT base CNF, streamed from the auditor's regenerated copy, which has the recorded sha c3933d9a…. I decoded them through the archived map (f72b186e…) without using the encoder:
- 14 sector units;
- 16 polygon units;
- 112 nesting units.

The sector units state chi((0,0),(0,2),(o,0)) = −1 and chi((0,1),(0,3),(o,0)) = +1 for o = 1..7. An exact grid sweep shows these hold exactly when (o,0) lies in the open quadrant counter-clockwise from (0,0). They are identical to LayerEncoding(32,7,4).add_sb(). So soundness needs every real fourfold 32-point set to have exactly one point of each inner orbit in that open sector.

(2) The fact is true, and it follows directly from general position, as the auditor says. R^{m/2} is the half-turn, so (0,j+m/2) = 2c − (0,j). Each boundary line of the sectors therefore contains two points of S. A point of another orbit on such a line would make three collinear points. Otherwise its m angles at c miss the boundary rays, and exactly one of them falls in the open sector.

(3) The written record has no such argument. I read the following and searched all .md/.tex/.py files for "sector", "diameter", "labelling" and "collinear":
- symcnf.py docstring, l.38 "sound: every realizable symmetric set has such a labelling". Lines 44–48 justify only the angular order (the half-plane argument), not existence.
- symcnf_layers.py docstring, l.11–12: "the point of O_o in the open sector", with no argument.
- SYM5/README §1: the perturbation is for m = 5 only ("multiple of 72°"). For even m the centre cannot be a general-position chirotope point (symcnf.py l.10, l.130).
- SYM5/README §4.
- C4CUT/README §1: invokes only the layer lemma.
- C4CUT/review/README l.16: gives the unit signs "for a representative in the open quadrant", which presupposes existence.
- WRITEUP/SYMMETRIC.md, and the LaTeX note. The note's lem:sizes(b) states that c, p, ρ^{s/2}p are collinear, but never applies it to the normal form, and the note credits the fourfold bound to arXiv:2506.00224, not to C4CUT.

Existence was only checked empirically: the review's geom.py and the project's validate_z2.py both assert len(cand) == 1 on test sets in general position.

(4) Why minor and not more: the missing step is a one-line consequence of general position, so the C4CUT claim still follows. The fix is documentation only. Impact is limited further because the even-m sector clauses are used for UNSAT claims only in C4CUT. Central-34 uses SYMZ/zcnf.py, and the 2-fold symcnf runs gave no answer.

A small inaccuracy in the auditor's evidence, which does not matter: their m = 4 random-run logs show 1,040 evaluations, not 720. 720 is the subtotal for N = 12/16/20. The figures of 956 on c4_28 and 5 full N = 32 configurations (4, plus 1 in the killed run) match the logs.

*Verifier's evidence.* Scripts and logs are in AUDIT3/A4_fivefold_layers/verify_A4-1/. The encoder copies there are byte-identical to SYM5 (symcnf.py a8056da0…, symcnf_layers.py 71b2d7e7…).

- check_even_sector.py / .log, exact integer arithmetic:
  - Geometries: Z^2 for m = 2 and 4; Eisenstein coordinates for m = 6.
  - (1a) The encoder's float pattern is [−1, +1, …, +1] for every even m from 2 to 16.
  - (1b) The sector units hold exactly when the point is in the open sector (0, 2π/m). Checked on an 81×81 grid for m = 2, 4, 6.
  - (4) The grid equivalence holds: an orbit has a number of open-sector points other than 1 exactly when one of its points lies on a line (0,j)(0,j+m/2). That makes a collinear triple in S, and then no labelling satisfies the units. There were 6, 12 and 26 such degenerate orbits for m = 2, 4, 6, against about 6,550 regular orbits each.
  - (2,3) 2,130 labellings of 230 random exact sets in general position, covering every choice of orbit 0 and of (0,0), for m = 2, 4, 6, angle and layer forms:
    - every other orbit had exactly one open-sector point;
    - 0 of the encoder's own SB units were violated;
    - every shifted-representative control was caught.
- mutation_selftest.py / .log: all 4 mutations of the checker are caught.
- decode_c4_units.py / .log:
  - The base CNF c3933d9a… has 142 units: 14 sector, 16 polygon, 112 nesting.
  - Decoded through the map f72b186e…, the sector units are chi((0,0),(0,2),(o,0)) = −1 and chi((0,1),(0,3),(o,0)) = +1 for o = 1..7.
  - They are equal to LayerEncoding(32,7,4).add_sb().
- Doc check:
  - symcnf.py l.38–48 and symcnf_layers.py l.11–12 assert the labelling without an argument.
  - SYM5/README.md §1 is m = 5 only.
  - C4CUT/README.md §1 and C4CUT/review/README.md l.16 contain no existence argument.
  - The note's lem:sizes(b) has the collinearity fact but does not apply it.

### A4-2 (minor): Layer lemma is stated without all the facts the encoder uses

The note's Lemma lem:layers has the right hypotheses (general position, c not in S) but concludes only that every convex layer is a single orbit. The layer units also need two more facts: (i) every point of a later layer is strictly inside each earlier layer polygon; (ii) the centre is strictly inside each layer polygon (unit chi((o,0),(o,1),c) = +). Both follow in one line: general position excludes points on edges, and c is interior to every regular m-gon centred at c. The SYM5 README statement omits 'general position' although its step 4 uses it. The symcnf_layers.py docstring omits both general position and c not in S; with c in S the lemma still holds, with {c} as the last layer. Documentation only.

*Evidence.* WRITEUP/note/symmetric_es7.tex lines 134-141; SYM5/README.md §2 'Layer lemma'; SYM5/symcnf_layers.py docstring.

*Suggested fix.* State the lemma once with all hypotheses and conclusions (as in A4-7) and point to it from the README and the docstring.

**Independent check:** real = yes; severity minor -> **note**.

The finding is partly correct, but it overstates the gap. I downgrade it from minor to note.

Correct parts:
(a) Note, lines 134-141: the lemma has the right hypotheses (general position, m >= 4, c not in S, K <= 2m) and concludes only that every convex layer is a single orbit. Line 146 adds "seven nested regular pentagons" but never says strictly nested.
(b) SYM5/README.md, lines 64-65: the lemma statement does not mention general position. Proof step 4 (line 71) uses it to conclude strict nesting, and that conclusion is not in the statement. General position is ambient, though: the README's theorem (line 6) is about sets in general position.

Incorrect or overstated parts:
(c) The docstring claim is a misreading. symcnf_layers.py line 2 says "no centre in the set (N = m t)". Lines 8-9 say "every point of O_o' with o' > o lies strictly inside conv(O_o) (general position)". Line 18 lists the centre unit, and line 29 asserts not center_in_set. Only the "Fact" parenthetical omits the two hypotheses. That is harmless: with c in S the fact still holds, and the strictness clause names general position.
(d) Fact (ii) is not a layer-lemma fact. The unit chi((o,0),(o,1),c) = + is the same CNF literal as the base-model centre unit chi(c,(o,0),(o,1)) = + (k = 1). That unit holds for every orbit, is emitted by symcnf.py in both P1 and L1, and is documented as part of the base model (README line 48; symcnf.py docstring item C). The lemma does not need to supply it.

What remains is fact (i), strict nesting. It is the only family of units that depends on the layer lemma (105 units). It is written in README proof step 4 and in docstring lines 8-9, and it follows in one line from the definition of convex layers plus general position, which the note's lemma assumes. CERTIFICATES.md cites the README and the encoder as the soundness basis for c5-layer, and together they contain every fact the encoder uses.

The claim is unaffected. P1 (angle form) proves Theorem E without the layer lemma, and L1's facts are all true (verified exactly below). What is left is editorial: the lemma statements do not list a standard corollary, and the README statement leaves out an ambient hypothesis. No soundness gap.

*Verifier's evidence.* Files re-read (R = work directory/results):
- R/WRITEUP/note/symmetric_es7.tex, lines 134-141 and 146.
- R/SYM5/README.md, lines 48 and 64-73.
- R/SYM5/symcnf_layers.py, lines 2, 5-9, 16-19 and 29.
- R/SYM5/symcnf.py, lines 31 and 222-233.
- R/WRITEUP/CERTIFICATES.md, line 89.
The encoder hashes match CERTIFICATES.md (71b2d7e7..., a8056da0...).

My checks, in AUDIT3/A4_fivefold_layers/verify_A4-2/:

1. unit_families.py (log: unit_families.log). For N=35, K=7, m=5 the layer form adds 145 unit clauses:
   - 12 sector units (shared with the angle form);
   - 21 polygon units (orbit facts);
   - 7 centre-inside units, all identical literals to base centre units;
   - 105 nesting units, the only family that depends on the layer lemma.

2. cnf_tail_check.log, on the regenerated L1 CNF:
   - its sha256 is 90dea1cf..., the recorded hash;
   - its last 145 lines are byte-identical to my rebuilt list;
   - it has 159 unit clauses but only 145 distinct literals: 7 centre duplicates, plus 7 polygon self-duplicates (k=2 and k=4 give the same literal by rotation).

3. check_layers_exact.py uses exact Z[zeta5] sign arithmetic. Real sets (log: real_sets.log):
   - On c5_30points, c5_31minus_centre and c5_31points, every layer is one orbit in counter-clockwise order.
   - Nesting is strict (minimum orientation sign +1), the centre is strictly inside every layer, and all layer units hold.
   - c5_31points, which contains the centre, has layers 5,5,5,5,5,5,1, so {c} is the last layer.
   - In the non-general-position set (pentagon plus its edge midpoints), the layers are still single orbits but the nesting sign is 0. So general position is needed only for strictness.

4. Random test, 600 random fivefold sets in general position (logs: random_sets.log, random_inspect.log):
   - strict nesting held in 600/600;
   - the centre was strictly inside the layers in 256/256 sets whose layers are all single orbits;
   - every one of the 429 layers containing two or more orbits was in convex position;
   - the units held in 174/175 sets; the exception has a non-generic centre (no sector representative), which README §1 removes by rotating each orbit slightly.

The repo was not modified: the existing __pycache__ dates from 21:26, before my runs, and I ran only copies with -B.

### A4-3 (minor): 'Two independent encodings' overstates independence

P1 (symcnf.py) and L1 (symcnf_layers.py) share every clause family: triple-orbit variables, interiority, GP sign clauses, centre facts, and the convexity and K-set clauses (about 7.92 M clauses, identical code). They differ only in the normal-form units: 27 clauses against 145, with the sector clauses common to both. So they are two normal forms over one encoder, not encodings that are independent with respect to bugs in the shared code. The README's own description says they 'differ only in how they label the points'. The real value of the pair is that P1 does not use the layer lemma and L1 does not use the angle order. My exact tests exercised the shared code directly, so this does not threaten the theorem.

*Evidence.* SYM5/README.md §2 ('L1 is an independent second encoding'; 'What is ours. Two independent encodings'); gen.log sb_clauses 27 vs 145.

*Suggested fix.* Say 'two normal forms of the same abstract encoding'.

**Independent check:** real = yes; severity minor -> **minor**.

The finding is correct. P1 and L1 come from one encoder with two different normal forms. They are not independent encodings.

Code: `symcnf_layers.py` defines `LayerEncoding(SymEncoding)` and overrides only `add_sb` (lines 26-57). Everything else is inherited from `symcnf.py`: `_triples`, `add_axioms` (interiority and GP), `add_center_facts`, `add_kgon` (conv4/5/6 and the K-set clauses). The SYM5 copy of `symcnf.py` is byte-identical to `tools/symmetric/symcnf.py` (sha a8056da0...).

CNF check: I regenerated both CNFs from copies of the encoders. Their sha256 values match `SYM5/sha256.txt` (ead55228...5450dbb and 90dea1cf...c0668a8). The variable maps are identical and both have 401,464 variables. A streaming line diff, cross-checked with `cmp`, shows:
- The first 7,923,894 clause lines are byte-identical. That is 7,923,882 non-normal-form clauses plus the 12 sector units chi(c,(0,0),(o,0))=+ and chi(c,(0,1),(o,0))=-.
- After that, P1 has 15 angle-order units chi((o,0),(o',0),c)=+ and L1 has 133 layer units. No tail clause appears in both.
- So 148 unit clauses differ, about 0.002% of the formula. This confirms the auditor's figures: 27 vs 145, sector clauses common, "all but about 150" units.
- Extra detail: 7 of L1's 133 units are duplicates, because by rotation the k=4 unit chi((o,0),(o,1),(o,4)) is the same orbit variable as k=2. So L1 adds 126 distinct units. This is harmless.

The independence that does exist is only in the normal-form argument: P1 does not use the layer lemma, and L1 does not use the angle order. The two still share the sector clauses, the auxiliary-centre argument, every clause family, the solver (CaDiCaL 3.0.1) and both checkers. A bug in the shared code would affect both formulas in the same way.

Where the overclaim appears:
- `SYM5/README.md` line 23 says "What is ours. Two independent encodings". This is in the Prior-work bullet at the top, not §2 as the auditor cited, but the difference does not matter.
- Line 83 says "L1 is an independent second encoding".
- The same README is accurate elsewhere: line 43 says "abstract model of symcnf.py, copied here unchanged" and line 55 says they "differ only in how they label the points".
- The main write-ups do not repeat the word "independent". `SYMMETRIC.md` line 86 says "two encodings", and the LaTeX note (line 148) correctly says "a second normal form".

Why minor and not major: no document relies on the pair's independence as the safeguard for soundness. Soundness rests on the written clause-by-clause argument plus tests, and it holds up under my own test:
- I wrote an exact Z[zeta5] test from scratch and ran it on real 35-point nested-pentagon sets, using both solved CNFs.
- Not one of the triple-variable clauses was violated: 6,126,609 in P1 and 6,126,727 in L1.
- With the conv variables set to their least model, the number of violated K-set clauses equals the number of convex 7-subsets divided by 5, in every run.
- That was 4 layer-form runs and 9 angle-form runs (3 seeds × 3 choices of orbit 0).
- In label-swap mutations, each form violated a normal-form unit.

So the wording overstates how strong the evidence is, but it does not hide a gap that the theorem depends on. The fix is a wording change: in `SYM5/README.md` lines 23 and 83, say "two normal forms of one abstract encoding (symcnf.py)". Optionally say the same in `SYMMETRIC.md` line 86.

*Verifier's evidence.* Files read:
- SYM5/symcnf_layers.py: lines 23 and 26-57, only `add_sb` is overridden.
- .../SYM5/symcnf.py: `build()` = `add_axioms`, `add_center_facts`, `add_kgon`, `add_sb`.
- .../SYM5/README.md: lines 23, 43, 55, 83.
- .../SYM5/gen.log: sb_clauses 27 vs 145; clauses 7,923,909 vs 7,924,027.
- .../WRITEUP/SYMMETRIC.md:86 ("two encodings").
- .../WRITEUP/note/symmetric_es7.tex:148 ("a second normal form").

My scripts and logs are in AUDIT3/A4_fivefold_layers/verify_A4-3/.
- `regen.sh` regenerated both CNFs in about 40 s with about 118 MB RSS. `big/sha.txt` gives ead55228944c920a9ab26eaab98ae0f9963ecf69f651323a664e813715450dbb and 90dea1cf87d3d8500dffff9d9741e84abc9babe4e1ac4e32035448ce7c0668a8, which equal `SYM5/sha256.txt`. I deleted the large CNFs afterwards; `regen.sh` recreates them.
- `diff_cnf.py` (output in `diff_out.txt`):
  - The variable maps are identical.
  - The common clause prefix is 7,923,894 lines.
  - The tails are P1 15 and L1 133, with 0 clauses in common.
  - The tails decode to the angle-order units chi((o,0),(o',0),c)=+ (P1) and the layer units chi((o,0),(o,1),·)=+ (L1).
  - `cmp` after the headers reports "differ: ... line 7923895".
- `decode_units.py`: the last 12 common lines (94, -204, 229, -319, ..., 519, -529) are exactly the sector units chi(c,(0,0),(o,0))=+ and chi(c,(0,1),(o,0))=-, for o=1..6.
- `realtest.py`, `run_batch.sh` (logs `logs_real_L_seed1.txt`, `logs_real_batch.txt`): exact Z[zeta5] real-set test on both solved CNFs.
  - All runs: 0 violated triple-variable clauses.
  - K-set violations equal convex 7-subsets / 5: 4184, 4623, 7742 and 7413 for seeds 1-4, all MATCH.
  - Swap mutations violate unit 608 (P1 order unit) and unit 533 (L1 layer unit).

### A4-4 (minor): Stale statements about the fourfold case across documents

C4CUT/README.md still says the even-m encoder has 'no independent review. An independent review is pending' and that N(C4) = 28 is 'conditional on the encoder review above'. Yet C4CUT/review/README.md, of the same date, reports no blocking or major finding. SYM5/README.md §4 still says the fourfold 32-point exclusion 'rests on the enumeration in arXiv 2506.00224'. WRITEUP/SYMMETRIC.md (§2 table, Corollary 3) and the note (cor:only, prop:C) still cite the published fourfold exclusion. By C4CUT's own reading, the last step of that exclusion rests on a heuristic realizer; I did not check the paper. C4CUT, which this audit finds sound, or the central-34 theorem (A4-6) discharges this hypothesis, but the write-up does not yet say so.

*Evidence.* C4CUT/README.md 'Credit and status' and §5; SYM5/README.md §4; WRITEUP/SYMMETRIC.md lines 59, 81.

*Suggested fix.* Update these documents to cite C4CUT and/or derive C4 from C2.

**Independent check:** real = yes; severity minor -> **minor**.

The finding is correct, and minor is the right severity. I checked every quoted statement against the committed files at HEAD 9cf4949a5. All of them exist where the auditor says.

**The C4CUT README is plainly stale.**
- It still says the even-m encoder has "no independent review. An independent review is pending." It also says N(C4) = 28 is "conditional on the encoder review above".
- C4CUT/review/README.md, dated 1 Nov 2026, reviewed exactly that encoder (symcnf_layers.py with m = 4). Its verdict is "No blocking or major finding".
- Commit 755081b76, which recorded the review, edited C4CUT/README.md in two other places but left these lines unchanged.

**The other documents still lean on the paper.**
- SYM5 §4 still says the exclusion "rests on the enumeration in arXiv 2506.00224".
- SYMMETRIC.md (Corollary 3 and the §2 table) and the note (cor:only and prop:C) still rest the fourfold step on SMQH25 §6.2.
- C4CUT is not referenced anywhere outside its own directory.

**What the paper actually says.** I read arXiv 2506.00224v1 myself.
- §6.2 says that none of the six inner-12 configurations is realizable. It gives no method or certificate for this, only realization attempts "using heuristics".
- Footnote 2 says the realizer "can only determine realizability, not unrealizability".
- So the published last step is uncertified. C4CUT's reading is fair, though the paper is silent on the method rather than saying outright that the realizer was used.

**Why this does not threaten the claim.**
- C4CUT supplies the missing step. My copy of verify_cuts.py accepts all 6 cuts, and the cuts and map hashes match final.json and the README. The review and this audit both found it sound.
- Corollary 3 and cor:only are stated as conditional ("Assume ..."), so they remain logically valid.
- Only prop:C and the §2 table assert N(C4) = 28 on an uncertified citation. The note's abstract and introduction ("showed") also overstate the paper.
- All of this is a text fix.

**Corrections to the finding.**
1. The alternative "or the central-34 theorem discharges this hypothesis" and the suggested fix "derive C4 from C2" hold only for Corollary 3 and cor:only.
   - A fourfold set of at least 33 points has at least 36 points and is centrally symmetric. Deleting one antipodal pair leaves a centrally symmetric 34-point set, so the central-34 theorem covers it.
   - The central-34 theorem says nothing about 32 points, and a centrally symmetric 32-point 7-gon-free set exists (SYM2). So it can never give N(C4) = 28 (the §2 table, prop:C, SYMMAX, C4CUT §5). Only C4CUT does.
   - The central-34 statement is also "not yet claimed" at HEAD (C2FINAL/README.md line 7).
2. The list of stale places is incomplete. Further statements cite the paper or leave C4CUT out; the evidence field lists them.
3. Two of the cited items are already flagged as pending by the project itself (review item 5, and C4CUT §5 "WRITEUP itself is not changed here"). The "review is pending" line was never flagged.

*Verifier's evidence.* **Committed text at HEAD 9cf4949a5** (paths relative to R = results):
- C4CUT/README.md
  - l.12-14: "...one real-set test (`SYM5/validate_z2.py`) and no independent review. **An independent review is pending.**"
  - l.81: "Hence N(C4) = 28, conditional on the encoder review above."
  - l.83-84: "...discharged by this certificate. `WRITEUP` itself is not changed here."
- C4CUT/review/README.md
  - l.1: "Independent review of C4CUT (1 November 2026)"
  - l.7: "No blocking or major finding."
  - l.11: the encoder symcnf_layers.py with m = 4 was checked for every clause family.
  - l.68: "`SYM5/README.md` §4 still cites the enumeration; it will be updated with the write-up."
- `git show 755081b76`: the review commit changes C4CUT/README.md only at the map-hash line and the "matching the six patterns" wording.
- SYM5/README.md
  - l.124: "(arXiv 2506.00224, §6.2)"
  - l.133-134: "the abstract route fails, and the exclusion rests on the enumeration in arXiv 2506.00224".
- WRITEUP/SYMMETRIC.md
  - l.59-60: "Assume ... the published fourfold exclusion (arXiv:2506.00224, §6.2)"
  - l.81: the 4-fold table row credits SMQH25 for excluding 32 points.
  - l.133: trust base lists symcnf_layers.py as "(fivefold)" only.
  - l.201: "no real fourfold set of that size exists".
- WRITEUP/note/symmetric_es7.tex
  - abstract l.21-22 ("Combined with the fourfold result of ...")
  - intro l.36-37 ("showed that no real fourfold symmetric 32-point set avoids a convex heptagon")
  - cor:only l.122-123
  - prop:C l.165-166 ("The fourfold bound is due to [SMQH25 §6.2]")
  - l.249-251
- Stale places the auditor missed:
  - SYMMAX/README.md l.12
  - SYMZ/README.md l.82
  - WRITEUP/CERTIFICATES.md: no C4CUT archive entry
  - `git grep 'C4CUT|es7-c4-32-cuts'` outside C4CUT/: no hits.
- Central-34 status: C2FINAL/README.md l.7 says the statement "is **not yet claimed**". Commit 9cf4949a5 says "the claim stays open".

**Paper** (arXiv HTML v1, downloaded to verify_A4-4/download_arxiv/):
- §6.2: "We attempted to realize several of them using heuristics ... all 310 million solutions have only 6 different configurations to the inner 12 points and none of those are realizable. Thus, there does not exist a realizable 4-fold symmetry on 32 points without a 7-gon."
- Footnote 2: "The realizer tool can only determine realizability, not unrealizability. However, for several of the configurations for which the tool was unable to find a realization, we were able to find a subset 10-point configuration that is known to be unrealizable."
- No unrealizability certificate is given for the six patterns.

**My checks** (all under AUDIT3/A4_fivefold_layers/verify_A4-4/):
- scripts/stale_check.sh, output in stale_check.log: greps the committed blobs.
- scripts/extract_text.py: extracts the paper passages.
- scripts/verify_cuts_copy.py, a copy of C4CUT's verifier run with python -I. Result in verify_cuts_copy.log:
  - "6 cuts verified"
  - map SHA-256 f72b186e…, matching the README
  - cuts.jsonl SHA-256 3852ece5…, equal to final.json's cuts_jsonl_sha256.

**Side note, outside this finding:** gitignored __pycache__ directories were created in the read-only worktree this evening, at 21:19-21:26, in SYM5, SYMMAX, C3a, C3-S/tools and C3U2/tools. Some process imported project modules in place. This is harmless to the hashes, but it breaks the read-only rule.

### A4-5 (minor): C4CUT does not record which checker binaries produced its verdicts

results/E2 found that upstream lrat-check (drat-trim 2e3b2dc) accepts a forged one-line proof, so only the patched build (sha f2046212...) counts. c4final.sh takes the binary directory as an argument, and neither final.json nor the README records the path or the hashes of the lrat-check and cake_lpr that were used. The claim is still carried by cake_lpr if that binary is the recorded CakeML build (2fee767...). The only builds present in <night run>/bin are the patched lrat-check and that cake_lpr. The final proof's empty-clause step has hints, so the E2 defect is not triggered.

*Evidence.* C4CUT/c4final.sh, final.json; results/E2/README.md §'side finding'; shasum of resolve/bin binaries: f2046212..., 2fee767..., e12ecc8c...

*Suggested fix.* Record the tool hashes in final.json. When memory allows, replay the patched lrat-check on the archived proof (it used ~0.5 GB RSS on L1).

**Independent check:** real = yes; severity minor -> **minor**.

The finding is correct, and minor is the right severity. It is a real gap in the records, but the claim does not depend on it.

What I confirmed:
- c4final.sh takes the binary directory as $2. Nothing names the lrat-check and cake_lpr builds used or their hashes: not final.json (repo or archive copy), README §3, the archive's SHA256SUMS, or the commit messages 4292bd34b and 755081b76.
- The project does pin its tools elsewhere (the CERTIFICATES.md tools table and es7-symmetry/tools/tools_sha256.txt). C4CUT never appears in CERTIFICATES.md, so it departs from the project's own practice.
- The gap matters in principle. The unsound upstream build is on this machine: sha bd7eb805…, at <local-tools>/sat/src/drat-trim/lrat-check (drat-trim git 2e3b2dc), with a copy under work/m10. It is the same size as the patched build (36,552 bytes) and prints the exact string final.json stores, "c VERIFIED".
- My controls on the satisfiable CNF "1 0": bd7eb805 accepts both "2 0 0" and "2 0 1 0" (exit 0). The patched builds f2046212 and 66780e68 reject both.
- The resolve/bin hashes are as the auditor stated. f2046212 is the patched build (checked by behaviour) and 2fee767 is the pinned cake_lpr a36874a8.

Why the claim is not threatened:
1. cake_lpr (the CakeML-verified checker) also accepted, and 2fee767 is the only cake_lpr build on the machine (four copies).
2. The lrat-check verdict means the same whichever build produced it:
   - I streamed the archived proof and CNF. Proof SHA-256 6e1199aa… and 1,040,775,249 bytes, CNF 2aa18f1e…, all matching final.json.
   - The proof has no RAT hints and exactly one empty-clause step, its last line: `11765772 0 11765265 11765756 11764908 11764905 0`.
   - Those hints are the units -854, 836 and 461 and the clause (-461 854 -836), which they falsify. That is a genuine RUP conflict.
   - The E2 patch changes only the branch for an empty clause whose RUP check ends without a conflict, so the patched and unpatched builds take identical paths on this proof.
3. Circumstantial evidence on which directory was used:
   - The archived cad_c4cuts.out keeps CaDiCaL's build stamp "Sun Oct 25 15:14:29 KST 2026", which matches cadical e12ecc8c.
   - All four directories on the machine holding that build also hold f2046212 and 2fee767. c4final.sh needs all three tools in one directory, and the unpatched builds have no cadical or cake_lpr beside them.

Imprecision in the finding itself:
- "The empty-clause step has hints, so the E2 defect is not triggered" is not a valid argument. The unpatched build accepts an empty clause with any non-conflicting hints, as my "2 0 1 0" control and a lemma-hinted self-test show. The conclusion holds only because these hints do reach a conflict, which I checked.
- "The only builds in resolve/bin" is true, but it misses the unpatched build elsewhere on the machine.

Related record-keeping points, not separate findings:
- The repo copy of cad_c4cuts.out drops the build-stamp line that the archived copy keeps.
- The repo final.json has a rewritten archive_dir.
- The archived verify_cuts.py is the pre-review version.
- So the repo copies are not the files hashed in the archive's SHA256SUMS.

Fix: as the auditor suggested, record the bin directory and tool hashes in final.json and the README, and keep the build-stamp line. A full lrat-check replay would load the 183 MB CNF, which the audit rules forbid, so I did not run it.

*Verifier's evidence.* Scripts and outputs are in AUDIT3/A4_fivefold_layers/verify_A4-5/:
- checker_controls.sh and checker_controls.log: forged and genuine tiny proofs run on every lrat-check build found. bd7eb805 prints "c VERIFIED" on all forgeries; f2046212 and 66780e68 reject them with "c FAILED: empty clause without a RUP conflict".
- tool_inventory.tsv: every cadical, lrat-check and cake_lpr binary on the machine, with hash, mtime, and either the forged-proof result or the CaDiCaL build stamp.
- empty_step_check.py, empty_step_check.json and empty_step_check.log: a streaming pass over the archived c4cuts.lrat.zst and c4_n32L_cuts.cnf.zst (0.2 GB RSS, 8.5 s).
  - Proof: sha 6e1199aa…, 1,040,775,249 bytes, 8,773,778 lines, 0 RAT hints, 1 empty-clause step (line 8,773,778, id 11765772, 4 lemma hints). Replay result: CONFLICT at the 4th hint after 3 units.
  - CNF: sha 2aa18f1e…, 5,272,500 clauses.
- proof_tail4000.txt: the four hint lemmas are `11764905 -461 854 -836 0`, `11764908 461 0`, `11765265 -854 0` and `11765756 836 0`; none is deleted in the tail.
- selftest/: on a bad lemma-hinted empty step, the script says NO_CONFLICT and the unpatched build still says VERIFIED.

Cited project files:
- C4CUT/c4final.sh (B=$2), C4CUT/final.json, C4CUT/README.md §3.
- E2/README.md §2 and E2/tools/lrat-check-E2.patch (the patch adds only `if (size == 0) ... return FAILED;` after the RUP check).
- WRITEUP/CERTIFICATES.md lines 14-19 (the tool table; C4CUT is absent).
- Archive <proof-archives>/es7-c4-32-cuts-2026-11-01/: SHA256SUMS lists no tools. The archived cad_c4cuts.out has the "Sun Oct 25 15:14:29 KST 2026" line, which is missing from the repo copy. The archived final.json differs from the repo copy in archive_dir.
- <local-tools>/sat/src/drat-trim is at git 2e3b2dc and its lrat-check.c is unpatched (line 161 is commented out, and the E2 line is absent).

### A4-6 (note): Fourfold is on no critical path once central-34 holds; fivefold is indispensable

A rotation of order 4 contains the half-turn. A fourfold set in general position has 4k points (the centre is excluded), so one with >= 33 points has >= 36. Deleting one antipodal pair leaves a 34-point centrally symmetric set. Hence the central-34 theorem implies the fourfold case, and also order 6. C4CUT and the even-m layered encoder are then not on the critical path of the overall claim: they give an independent proof of N(C4) = 28 and a fallback. C5 contains no half-turn, no order-3 rotation and no reflection, so the overall claim needs the fivefold theorem. That theorem has two certificates, and P1 needs no layer lemma.

*Evidence.* Group-theoretic argument; WRITEUP/SYMMETRIC.md Corollary 3.

*Suggested fix.* State this in the assembly of the final theorem.

### A4-7 (note): Layer lemma: proved in full

Setting: S is finite with no three points collinear. R is the counter-clockwise rotation by 2pi/m about c, with m >= 3 and R(S) = S. S has no K points in convex position, with K <= 2m. Layers: S_0 = S; L_j = vertices of conv(S_j), i.e. the points x of S_j with x not in conv(S_j - x); S_{j+1} = S_j - L_j.
(a) R is an affine bijection with R(S_j) = S_j, so R(L_j) = L_j and R(S_{j+1}) = S_{j+1}.
(b) For p != c, R^k p = p iff m divides k, so non-centre orbits have exactly m points: the vertices of a regular m-gon centred at c.
(c) If S_j != {c}, then S_j contains some p != c, and c lies in int conv(orbit p), which is inside conv(S_j); so c is not in L_j, and L_j is a non-empty union of m-point orbits.
(d) L_j is in convex position. Two orbits would give 2m >= K points in convex position, so L_j is exactly one orbit. If S_j = {c}, then L_j = {c}.
(e) A point x of S_{j+1} lies in conv(L_j) and is not a vertex. If it were on the boundary, v_r, x, v_{r+1} would be collinear. So x is interior, and so is c by (c).
(f) Label L_j as v_r = R^r v_0, counter-clockwise. Then chi(v_r, v_{r+1}, x) = + for every interior x, and chi(v_0, v_1, v_k) = + for 2 <= k < m.
This is exactly what the layer units assert. The proof uses m >= 3 in (c), K <= 2m in (d), and general position only in (e). The hypothesis K <= 2m is necessary: for m = 3 and K = 7, two triangles forming a convex hexagon violate the conclusion.

*Evidence.* Empirical check on non-nested random sets: m=4, 600 sets; m=5, 450 sets. All 266 7-gon-free sets have single-orbit layers. All 640 sets with a multi-orbit layer have >= 2m points in convex position (logs/test_layer_lemma.log).

### A4-8 (note): Exact soundness tests of both encoders found no violation

Own Z[zeta5] and integer arithmetic, labelling and CNF evaluator, using unmodified encoder copies whose hashes match the originals. Every clause of the CNF was evaluated with the triple values taken from exact orientations and the least Horn model for the convexity variables, which is a complete test.
- Random sets: 629 (309 of them 7-gon-free), m=5 layer and angle forms at N=10..25, m=4 layer form at N=8..24. 4,415 evaluations, covering every (0,0) choice and, for the angle form, every orbit-0 choice. 0 violated axiom, centre, normal-form or definitional clauses. In every evaluation the violated K-set clauses equal (#convex 7-sets)/m. 1,750/1,750 wrong labellings were caught.
- Extremal sets c4_28, c5_30 and c5_31 (centre removed), with their mirror images and all whole-orbit subsets: 5,688 evaluations, including the full N=28 and N=30 formulas, which match the project's hashes. 0 violations.
- Solved formulas c5_n35L (3 real 35-point sets), c5_n35 (3) and c4_n32L (4, plus 1 in a stopped run): T = D = 0, K = (#convex 7-sets)/m exactly, and every negative control caught. So no clause of the solved formulas other than the 7-gon clauses is violated by a real configuration.
- The three evaluators (in-memory, streaming, chunked) agree on 16/16 evaluations with non-zero counts.

*Evidence.* logs/rand_*.log, logs/real_*.log, logs/full_*.log, logs/test_agree.log, logs/test_perturb.log

### A4-9 (note): C4CUT cut soundness confirmed independently; hash chain reproduced

In a real configuration in general position the brackets equal the orientation determinants, which I checked symbolically, and [abc][ade] - [abd][ace] + [abe][acd] = 0 identically (symbolic expansion). All three terms are nonzero, so exactly one term has the minority sign, and its absolute value equals the sum of the other two, hence strictly exceeds each. A positive integer combination of the resulting log-inequalities in which every bracket cancels gives 0 > 0. The certificate reads only the signs fixed by the clause, so the clause removes no real configuration, with no symmetry assumption needed. My own checker re-verified all six certificates (142-152 rows each). Each clause consists of exactly the 55 triple-orbit variables of labels 20..31. Each forbidden pattern is a rotation-invariant abstract uniform acyclic chirotope (so the cuts are genuine realizability cuts), and the six are pairwise distinct. I reproduced the chain base -> base+cuts byte for byte (c3933d9a..., f72b186e..., 2aa18f1e...), and the archived CNF and proof match their recorded hashes.

*Evidence.* logs/check_cuts.log, big/gen_c4_32.log, logs/archive_hashes.log

### A4-10 (note): Checker verdicts taken from logs, not replayed

I did not rerun lrat-check or cake_lpr on P1, L1 or the C4 final proof: the audit rules forbid loading CNFs > 50 MB and running cake_lpr. What I did verify: the regenerated CNFs are byte-identical to the recorded hashes; the archived compressed CNFs and the LRAT proofs (P1, L1, C4) decompress to their recorded SHA-256; both inspected proofs end with an empty-clause step; the logs show lrat-check 'c VERIFIED' and cake_lpr 's VERIFIED UNSAT' for P1 (heap 30000), L1 and C4 final, with clause counts matching the CNF headers.

*Evidence.* logs/archive_hashes.log; SYM5/chk_*.out; C4CUT/final.json

*Suggested fix.* Replay the patched lrat-check when the machine is free.

### A4-11 (note): Prior-work remarks not checked

I did not inspect Bogdan's generator or paper (arXiv:2512.24061), nor the description of arXiv:2506.00224 §6.1-6.2. The remark that deleting two points of the innermost pentagon of a 35-point fivefold set gives his '5^6' configuration is logically consistent with the layer lemma, given the README's description of his encoding. None of this bears on the certificates.

*Evidence.* SYM5/README.md 'Prior work'

## Tests run by the auditor

- geo.py self-test of exact Z[zeta5] predicates (orientation, Re/Im signs, rotation, multiplication, conjugation) against floating point on 20,000 random cases plus 2,000 exact collinearity and rotation cases: 0 mismatches (logs/geo_selftest.log)
- test_dp.py: angular-DP counts of convex k-subsets against brute force on 20 symmetric sets: identical (logs/test_dp.log)
- campaign_random.sh / test_encoders.py: 629 random nested and non-nested symmetric sets, 4,415 full CNF evaluations, 1,750 negative controls; 0 violations, all negatives caught (logs/rand_*.log)
- campaign_real.sh / test_real.py: SYMMAX c4_28points, c5_30points and c5_31points (with centre: general position, largest convex subset 6) and their mirror images, all whole-orbit subsets, 5,688 evaluations including streaming evaluation of the full N=28/N=30 formulas: 0 violations (logs/real_*.log)
- test_full.py: exact evaluation of the regenerated, hash-identical solved formulas c5_n35L.cnf, c5_n35.cnf and c4_n32L.cnf on real configurations of the solved size; only K-set clauses violated, in exactly the predicted number; negatives caught (logs/full_*.log)
- test_agree.py: in-memory, streaming and chunked evaluators agree on 16/16 evaluations with non-zero counts (logs/test_agree.log)
- test_perturb.py: 20 adversarial fivefold sets with a non-general centre; per-orbit exact rotation preserves the chirotope and fixes the centre; 400 evaluations pass (logs/test_perturb.log)
- test_layer_lemma.py: 1,050 non-nested random sets (m=4, m=5): 0 counterexamples (logs/test_layer_lemma.log)
- check_cuts.py: symbolic GP identity, independent re-verification of all six C4CUT certificates, chirotope and rotation-invariance checks of the patterns, 36/36 mutations rejected (logs/check_cuts.log)
- Regeneration with unmodified encoder copies: c5_n35.cnf ead55228..., c5_n35L.cnf 90dea1cf..., c5_n35.json = committed, c4_n32L.cnf c3933d9a..., map f72b186e..., base+cuts via own appender 2aa18f1e..., c5_n30/c5_n30L/c4_n28L = sha256.txt (big/sha_c5_35.txt, big/gen_c4_32.log)
- archive_hashes.sh: archived c5_n35, c5_n35L and C4-final CNFs and the L1, P1 and C4 LRAT proofs decompress to their recorded SHA-256; proof tails end with an empty-clause step (logs/archive_hashes.log)
- NOT run: lrat-check or cake_lpr replays (forbidden by the audit rules' 50 MB CNF and cake_lpr rules)

