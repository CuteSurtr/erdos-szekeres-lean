# Review of the ES(7) > 33 plan, 19 Oct 2026

**Scope.** I modified no files and touched no processes. I used about 5 s of CPU in total: exact `Fraction` checks on the AlphaEvolve point sets, plus some JSON and grep reads.

**Checked online:**
- Krapivin–Przybocki–Heule (KPH), arXiv 2607.02958, abstract and HTML
- Baek, arXiv 2206.04260
- Baek–Balko, SoCG 2025 HTML
- Subercaseaux–Mackey–Qian–Heule, arXiv 2506.00224 HTML
- Balko–Valtr, ENDM 2015, full PDF
- Balko's ES_SAT page
- The raw AlphaEvolve notebook on GitHub, and the paper text via alphaxiv
- Damásdi et al., arXiv 2312.01223
- Koshelev–Koshka (KK), arXiv 2604.20120 HTML

**Checked locally:** `.cache/erdos-tuza-valtr`, `.cache/erdos-szekeres-sat`, Schroeder's archive `.cache/es7_es8_bounds_81_319_v1.zip`, the scratchpad `enc/gen_etv.py` and its outputs, `.cache/es7/cnc/cnc.py`, and `experiments/es7-search-2026-10-13/encoding/gen_cnf.py`.

**Verdict.**
- **The maths mostly holds.** I re-derived the deep-below Proposition, the (7,6,6) gluing, the rung thresholds, the symmetry-class arithmetic, the orbit counts and the lemma bounds. All are correct.
- **The scheduler bugs are real.** In `cnc.py`, line 33 pops the newest cube, line 35 steals the oldest, and line 58 adds weights as floats.
- **Before acting or emailing, fix:** attribution/novelty (items 1–2), the realizability premise of the ladder (item 3) and the certification claims (item 4).
- **The plan also misses** its cheapest realizable-anchored experiment (item 5).

---

## Blocking

### 1. The ETV gluing is a published theorem, not "our derivation, possibly known"
**Severity:** blocking for the email; major for the plan.

The block replacement and the rule "a SAT model at a rung gives an ES(7) counterexample" are Erdős–Tuza–Valtr 1996. The reference is *Ramsey-remainder*, European J. Combin. 17 (1996) 519–532.

The equivalence of their conjecture with ES is stated in:
- the abstract of Baek, https://arxiv.org/abs/2206.04260;
- Baek–Balko, https://drops.dagstuhl.de/storage/00lipics/lipics-vol332-socg2025/html/LIPIcs.SoCG.2025.13/LIPIcs.SoCG.2025.13.html;
- Balko–Valtr, Conjecture 3.1 and the sentence after it, https://eurocomb2015.w.uib.no/files/2015/08/endm1938.pdf;
- KPH, Section 2, who cite ETV for the existence of their 26-point set;
- our own `.cache/erdos-tuza-valtr/README.md`.

Asking Prof. Suk "Is the Proposition known from ETV 1996?" would hurt our credibility.

**Fix:**
- Cite ETV 1996 for the ladder and gluing.
- Drop email question 3.
- Present only the deep-below Proposition, as an easy observation. It is essentially the first induction step behind Baek–Balko Thm 8 plus Baek's a = 4 theorem.

### 2. (7,5,6) has already been claimed, with Lean; and the email under-attributes Schroeder
**Severity:** blocking for any write-up or email; major for the ranking.

Schroeder's Zenodo record 22842891 (19 Sep 2026) claims the (7,5,6) case equals 25, for planar sets with distinct abscissae. Local copies are `.cache/schroeder-record-22842891.json` and the archive.
- The upper bound is formalized in Lean (`ES7CapacityStage.restricted25`, per `audit/THEOREM_MAP.md`). Its finite checks use native evaluation: the archive README lists 19 native-evaluation dependencies for ES7.
- The lower bound is an exact 25-point example (`certificates/restricted_25_points.json`).

So the plan's "short paper with certified N_sig(7,5,6) = 25" is largely pre-empted. Separately, our ES(8) ≤ 311 builds on Schroeder's omission method (repo README lines 84–87), but the "safe to state" email bullet does not say so.

**Fix:**
- Reframe (7,5,6) as an independent signotope-level cross-check. It is stronger only if Schroeder's certificates are planar-specific, which is unconfirmed; check `ES7CoverageData` in the archive.
- Make (7,5,7)@27 the headline new target.
- In the email, say that ES(8) ≤ 311 builds on Schroeder's method, is unreviewed, and give its axiom footprint.

---

## Major

### 3. KPH contradicts the realizability premise of the ETV ladder
KPH ran exactly the (7,5,7) conjectured-maximum instance: 26 points, no 5-cap, no 7-gon (Section 6, https://arxiv.org/html/2607.02958).
- They generated 200,000 abstract solutions and found **32** realizable ones.
- This took 1,193 core-hours, with Localizer at 15 s per model and a mean of 38 violated orientations.
- So at these rung sizes, abstract-to-real conversion succeeds about 1.6×10⁻⁴ of the time.

Three consequences:
- The plan's "every SAT outcome gives an explicit construction", and the structure report's "size range where realizers succeed", are wrong.
- A large abstract solution space at the threshold suggests (7,5,7)@27 UNSAT will be hard.
- M1's "1–2% counterexample chance" is inconsistent with the plan's own 5–10% prior times the fraction of counterexamples that split, times the realization rate.

**Fix:**
- Say "a SAT rung gives a 33-element signotope; it gives a point set only if realized."
- Use KPH-style realizability feedback for any models.
- Calibrate E2 on our own (7,5,7)@26 models against KPH's rate before trusting any "not realized" verdict.
- Lower M1's counterexample odds.

### 4. "Certified" is an overclaim
LRAT checks only the CNF. The link from CNF to theorem is unverified at every step:
- the signotope axioms;
- the one-directional cap/cup auxiliaries and the gon clause;
- the x-reflection lex-leader;
- the totalizer cardinality lemmas, which rely on Baek's theorem and the cup–cap theorem;
- for M2, the mirror identification and the hull-plus-mirror projective step.

Heule–Scheucher's result needed a Lean-verified encoding (Subercaseaux et al., ITP 2024), and we have `.cache/EmptyHexagonLean`.

**Fix:**
- Either verify the encoding in Lean and import the UNSAT as a declared axiom (this must be disclosed, given the never-`sorry` rule), or claim only "LRAT-checked UNSAT of encoding X, cross-validated against Baek–Balko's `etv_signotope`."
- Base any claim on a run without lemma injection, unless the lemma encodings are proved.

### 5. The cheapest realizable-anchored experiment is missing
The audit found that the abstract one-point extension test (`trackB-sat` ext) takes about 0 s per CaDiCaL call. It has been run on fewer than 100, mostly witness-like, sets. The plan drops it.

**Add:**
- **(a)** Run it on the 8,537 pool sets (6,881 of them annealed and not witness-derived), the 7 AlphaEvolve-derived 32-point sets, and the 168 starts.
- **(b)** Generalize it to an r-point abstract large-neighbourhood search:
  - delete r = 2–5 points from a realizable 32-point set;
  - fix the orientations among the remaining points;
  - solve for r+1 new points, which is a few hundred to about 1,500 free variables.
- **(c)** Realize SAT outcomes with a fixed-x LP seeded from the existing coordinates.

This bridges KPH's 0/200,000 abstract-first record and our face-level relocation, and it costs less than M1–M3. UNSAT answers also give order-type-level saturation, which fixes the audit's B5 wording issue.

### 6. The fixed-x LP realizer (E2) has a numeric and a citation problem
- **Citation.** KK's 1,937,396 is a special class: their Table 2 counts signotopes that minimize empty quadrilaterals. It is not all 10-point signotopes, which number about 1.8×10¹⁰ (OEIS A006245). KK also say fixing abscissae can lose realizations.
- **Numerics.** Exponential grids at 26–33 points span about 10³⁵ (base 12). That is beyond a double-precision LP, so scipy/HiGHS will be unreliable.

**Fix:**
- Use an exact rational LP (a download, so it needs your OK), or take x-coordinates from known realizations or a multi-scale grid.
- Quote KK's figure as 37.7% of their 10-point extremal class.

### 7. Compute and probability estimates are unsupported, and the estimator is biased
- "(7,5,6) certified in ~2 weeks, 35–50%" and "(7,5,7) 15–25%" have no comparator.
- The comparators we do have point the other way:
  - KPH's 23-point theorem took 1,727 core-hours;
  - h(6,7) = 24 took 231 CPU-hours with tuned cubes (from our survey);
  - Schroeder needed a geometric partition to settle (7,5,6).
- The proposed tree-size probe (200 random depth-20 cubes, 60 s cap) is censored, since timeouts are underestimates, and it has high variance.
- A 12-hour single-core LRAT run can produce TB-scale proofs. 753 GB is free.

**Fix:**
- Use Knuth-style probing with the solver's own split heuristic, track censoring, and report a range.
- Rank M1 only after that probe.
- Keep LRAT per leaf or stream-check it.

### 8. m16k6 UNSAT is misread
The x-sorted mirror encoding has a vertical axis, so it cannot represent two points on the axis (they would share an x-coordinate).
- With 16 points the axis can hold 0 or 2 points. `gen_etv.py` encodes only the 0-point case: with N even, no index is fixed.
- So m16k6 UNSAT neither signals over-constraint nor shows that no mirror-symmetric extremal set exists at k = 6.
- The 32-point controls have the same gap.
- For 33 points exactly one axis point is forced, so `m33k7` and `hm33k7` are complete for Euclidean mirror symmetry.
- I checked the published 4-fold and 5-fold 16-point sets in `decomp/sets.py`: neither is mirror-symmetric, so no ready-made 2-axis-point example exists.

**Fix:** state the restriction, and add a 2-axis-point variant if the k = 6 side fact is wanted.

---

## Minor

9. **"N(7,4,7) = 16 even for pure colourings" conflicts with Balko–Valtr §4.**
   - They give a 17-vertex colouring with no red 4-path and no 7-gon, so N̂(4,7,7) = 17 (N̂ there is a maximum).
   - My reading: Baek's Lean `Gon` (`Config/Defs.lean`) requires the cap and cup only to share endpoints (a weak gon). Balko–Valtr's gon requires the two paths to be vertex-disjoint.
   - In signotopes the two notions coincide, so lemma injection stays sound there. Never use these lemmas in pure-colouring runs.
10. **"Refutes Goodman–Pollack" is imprecise.** A 33-element signotope without a 7-gon refutes the pseudolinear strengthening, which Balko–Valtr §5 list as open. It refutes Goodman–Pollack only together with ES(7) = 33.
11. **Cup/cap convention.** `gen_cnf.py` and `gen_etv.py` set X(1,i,j) = true, which is a cup, so the hull frame forbids a 6-cup.
    - The plan's bounds (at least 16 points end a 4-cup, at least 17 end a 4-cap) are therefore correct.
    - The structure report says "no 6-cap"; with that convention the two bounds swap, and the swapped clause would be unproved.
    - Derive the bounds in code from (A,U) and test them on known extremal sets.
12. **The 4-fold 16-point count is consistently 66 in Subercaseaux et al.;** the "6" is the inner-12 count. Our 0/30 against 18/66 has probability about 7×10⁻⁵ under uniform sampling. The 5-fold 948 vs 932 inconsistency is confirmed.
13. **The M3 gate cannot discriminate.** Comparing m = 1 tails against a k = 6 null has no calibrated alternative, and the sizes differ (16 vs 32 points). Keep M3 only as a long shot.
14. **AlphaEvolve point: confirmed.**
    - The raw notebook comment claims 0 k-gons, and its print cells have no output.
    - The paper says one convex k-gon for every k ≤ 8.
    - I confirmed exactly that the 7-gon at indices 23, 32, 25, 14, 15, 17, 20 and the 8-gon at indices 29, 15, 57, 27, 0, 30, 1, 23 are convex, with no collinear triples.
    - "Exactly one" rests on our `countk.c`. Use it as a footnote only.
15. **Baek–Balko Lemma 14's hypotheses are visible in the SoCG HTML,** but its size formula is garbled. The blow-up program is small enough for exhaustive Python search over small base sets.
16. **Leave the subjective odds out of the email.** They are mutually inconsistent.
17. **Ask the people who ran these instances.** Baek–Balko ship `etv_signotope` and report finding no signotope above S(a,u,k), without parameters. KPH have the exact 26-point (7,5,7) pipeline. Ask Prof. Suk for an introduction, or write to them directly.

---

## Checked and sound
- The deep-below Proposition and its lemma.
- The (7,6,6)@31 gluing (one point deep below, one deep above).
- Rung thresholds 25, 26, 30, 31 and 32.
- Symmetry classes at 33 points: 3-fold rotation, one mirror axis with one point on it, and D3 as five orbits of 6 plus one of 3.
- Orbit counts 2,480 and 2,736.
- Lemma bounds at 27 points: at least 17, 11 and 7.
- The mirror sign rule, the xsb clause and the signotope clauses.
- (7,4,7)@17 is UNSAT in 0.79 s.
- The ETV conjecture is known only in the trivial range and for a = 4 or u = 4 (Baek–Balko).
- Damásdi et al.'s saturation results (classical construction saturated; saturated sets of (7/8)·2^(n−2) points).
- KPH: 0 realized out of 200,000 at 32 points, and the method does not scale well past 30 points.

## Unconfirmed
- The weak-versus-strong gon reading in item 9.
- Whether Schroeder's restricted25 certificate is signotope-level.
- Whether Baek–Balko ran a ≥ 5 rungs.
- The JCTA version of Baek–Balko and the Morris–Soltan text, which I did not re-read.

## Files
- `.cache/erdos-tuza-valtr/ErdosTuzaValtr/Config/Defs.lean`
- `.cache/erdos-tuza-valtr/README.md`
- `.cache/erdos-szekeres-sat/README.md`
- `.cache/es7_es8_bounds_81_319_v1.zip`
- `.cache/schroeder-record-22842891.json`
- `.cache/es7/cnc/cnc.py`
- `experiments/es7-search-2026-10-13/encoding/gen_cnf.py`
- `scratchpad/enc/gen_etv.py`
- `scratchpad/ae/pts.json`
- `scratchpad/decomp/sets.py`
- `(local session file)` (Balko–Valtr full text)