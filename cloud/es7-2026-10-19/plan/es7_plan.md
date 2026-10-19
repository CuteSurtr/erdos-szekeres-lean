# ES(7) > 33 search: ranked plan (research-lead review, 19 Oct 2026)

Read-only. I modified no file and touched no process. I used about 3 s of CPU for `ps`, an exact-fraction recount of the two `state.json` files, and reading prototype outputs.

## 0. Bottom line

1. **Stop attacking 33 points head-on.** Climb the Erdős–Tuza–Valtr (ETV) ladder at k = 7 instead.
   - Our run33 is already the top rung, (7,6,7) at 32 points in hull-normalized form. We jumped straight to it.
   - The lower rungs are smaller instances: (7,5,6)@26, (7,5,7)@27 and (7,6,6)@31.
   - A SAT model at any of them glues into an explicit 33-point counterexample. An UNSAT result with an LRAT proof is a new certified ETV value.
   - A new elementary Proposition (below, re-checked by hand) ties (7,5,7)@27 exactly to every counterexample that splits nontrivially in some direction.
2. **Second:** the mirror-symmetric class. It is new, the CNFs already exist, and it has a realizable-first annealing arm.
3. **Third:** an exact near-miss search on the one-heptagon plateau. It is a cheap long shot, gated by a k = 6 calibration.
4. **Stop now:** `grow.py`. **Pause:** run33 as configured. **Restart run33m3** under a fixed scheduler with proofs.

## 1. What I verified myself (new since the three reports)

- **run33 is still diverging.**
  - `state.json` now has 164 open cubes, against 149 at audit time a few hours ago. Max depth went from 264 to 275, median 142.
  - The exact open weight is 6.1e-27. The float `closed_weight` is frozen at 1 − 8.9e-16.
  - In `cnc.py`, line 33 pops the newest cube and line 35 steals the oldest one. Line 58 adds float weights. This confirms audit findings B1 and B2.
- **run33m3's "75%" is a single cube.**
  - Exact open weight is 0.25000018, of which cube [4, 554] alone is 0.25. The other 45 open cubes total 1.8e-7.
  - So the remaining quarter has not been worked on. It is not nearly done.
- **Cores.**
  - Running: 4 run33 workers (PIDs 19172, 19174–19176), 2 run33m3 workers (19171, 19173), and 4 `grow.py` instances, each spawning `sat`.
  - Load is about 12.3 on 15 cores. Roughly 3 cores are free.
- **Novelty caveat for the ladder (important).**
  - `.cache/erdos-szekeres-sat` is a clone of Baek–Balko's public tool (https://github.com/jcpaik/erdos-szekeres-sat). Its `lib/erdos.py` already has an `etv_signotope(n,a,b,N)` mode.
  - So they very likely ran small ladder instances in the signotope model. Their SoCG paper reports only that experiments found nothing above the conjectured values, without parameters ([SoCG 2025](https://drops.dagstuhl.de/storage/00lipics/lipics-vol332-socg2025/html/LIPIcs.SoCG.2025.13/LIPIcs.SoCG.2025.13.html)).
  - What would still be new is a completed, proof-checked result at a = 5 or 6, which nobody has published.
  - The tool is also a free, independent encoder to cross-check ours.
- **(7,4,7) = 16 is already Lean-verified, in a stronger form.**
  - `.cache/erdos-tuza-valtr` is Baek's Lean 4 formalization (https://github.com/jcpaik/erdos-tuza-valtr).
  - Its `theorem main` in `Main/Main.lean` says: C(n+2,2)+2 points contain a 4-cap or an (n+3)-gon. It is stated for an arbitrary `Config`, meaning any 2-colouring of triples with no axioms.
  - So N(7,4,7) = 16 holds even for pure colourings. The repo contains no `sorry` (grep checked; I did not rebuild it).
  - This makes the cardinality "lemma injection" built on it sound in every model.
- **Prototype controls in `scratchpad/enc/`** (all under 1 s unless noted):

  | Instance | Result | Time |
  |---|---|---|
  | (6,4,6)@11 / @12 | SAT / UNSAT | 0.01 s |
  | (6,5,5)@14 / @15 | SAT / UNSAT | 0.55 s |
  | (6,5,6)@16 | UNKNOWN | 4 s cap |
  | (7,4,7)@17 | UNSAT | 0.79 s |
  | k = 5 mirror, 8 points | SAT | |
  | k = 5 mirror, 9 points | UNSAT | |
  | k = 6 hull + mirror, 17 points | UNSAT | 0.01 s |
  | 32-point mirror CNF with the known mirror set's orientations fixed | SAT | 0.12 s |

  - (6,5,6)@16 is the hull-normalized ES(6) instance, which took 125 s in our logs.
  - CNF sizes:

    | Instance | Variables | Clauses |
    |---|---|---|
    | (7,4,7)@17 | 3,933 | 33,817 |
    | (7,5,6)@26 | 15,829 | 210,133 |
    | `m33k7` (mirror) | 47,002 | 684,478 |
    | `hm33k7` (mirror + hull) | 47,002 | 684,494 |

- **One unexpected result to treat with suspicion:** `m16k6` (8 mirror pairs, hexagon-free, no axis point) is UNSAT in 0.01 s.
  - It may be true: for even k the classical construction has a self-mirror middle block.
  - But a surprising instant UNSAT is the classic sign of an over-constrained encoding. It must be cross-checked before any mirror UNSAT claim is trusted (see Plan #2).
  - It also means the k = 6 mirror "speed-up" (0.01 s vs 125 s) tells us nothing: the k = 6 mirror class is empty already at 16 points.
- **The Proposition behind strategy S1 checks out (my independent re-derivation).**
  - **Lemma.** If A is deep below B, a subset with points in both is in convex position iff its A-part is a cup and its B-part is a cap.
    - For a 3-cap a1 a2 a3 in A and any b in B, b lies above the lines a1a2, a2a3 and a1a3, which puts a2 inside the triangle a1 a3 b.
    - The converse follows from the 4-point checks (3+1, 2+2, 1+3), each a line-separation argument.
  - **Proposition.** A heptagon-free 33-point set splitting as A deep below B, with |A|, |B| ≥ 2, exists iff a 27-point set with no 5-cap and no convex 7-gon exists.
    - Let p be the longest cup in A and q the longest cap in B, so p + q ≤ 6 with p, q ≥ 2.
    - p = 2: A has no 3-cup, so A is a cap of at most 6 points, and B has at least 27 points and no 5-cap.
    - p = 4 is the mirror case.
    - p = 3: Baek's (7,4,7) bound applies to both sides, giving at most 16 + 16 = 32 points.
    - Conversely, put a 6-cap deep below the 27-point set.
  - Gluing recipes for the other rungs also check out: 31 points with no 6-cap and no 6-cup, plus one point deep below and one deep above, gives 33 points.
  - This may be implicit in Erdős–Tuza–Valtr 1996, which none of us has read. Present it as "our derivation; possibly known".
- **Tooling gap:** scipy is not installed. The fixed-x LP realizer needs an LP solver. Installing one is a download, so it needs your OK.

## 2. Merged strategies and scores

The nine candidates collapse into four lines plus two shared enablers.

- **M1, the ETV ladder.** Merges structure S1, encoding S1 and heuristic "ladder". Rungs (7,5,6)@26, then (7,5,7)@27, then (7,6,6)@31, plus the Proposition, cardinality lemma injection, and an annealer arm.
- **M2, the mirror / D3 / C3 symmetric class.** Merges structure S2, encoding S2 and heuristic "symmetric annealing".
  - The abstract side covers mirror sub-case (i), where the axis point is a hull vertex (odd hull), and sub-case (ii), where it is interior. D3 and a lighter C3 encoding come later.
  - The realizable side is mirror-preserving annealing with an exact 1-D axis scan.
- **M3, the near-miss plateau.** Merges structure S3 and heuristic "relocation walk". It is an exact count of how many 7-gons each face creates, then a walk that moves a heptagon vertex to faces creating exactly one, seeded by 273 one-heptagon sets plus AlphaEvolve's set.
- **M4, the proof-direction rebuild.** Encoding S3: a hull-size case split of run33 with LRAT, plus the optional blow-up integer program (Baek–Balko Lemma 14).
- **E1 (enabler), a fixed cube-and-conquer engine.** Orientation-only cubing, FIFO or breadth-balanced scheduling, exact weights, budgets that grow, and an LRAT check per leaf. M1, M2 and M4 all need it.
- **E2 (enabler), a working realizer.** A fixed-x LP in y, alternating with a fixed-y LP in x; Localizer as fallback. It must pass the 5-fold 16-point control (Subercaseaux et al. report 92 of 948 realizable; we got 0 of 30).

All probabilities below are subjective.

| Line | (a) Counterexample chance | (b) Rigorous partial result | (c) Novelty | (d) Laptop feasibility | (e) First-experiment cost | Overall |
|---|---|---|---|---|---|---|
| **M1 ETV ladder** | 1–2%. A SAT rung glues to an explicit 33-point set, or at least a 33-point signotope that refutes Goodman–Pollack at k = 7 | **High.** Proposition in hand. Certified N_sig(7,5,6) = 25 in about 2 weeks: 35–50%. (7,5,7) = 26: 15–25%. (7,6,6): under 10% | Medium-high. Baek–Balko's tool has the mode, but no a ≥ 5 result is published at k = 7 | Good at 26, unknown at 27, poor at 31 | **Very low.** CNFs exist and controls pass; about 40 core-h on day 1 | **1st** |
| **M2 Mirror class** | ≤ 1% | Sub-case (i) closed in about a week: 30–40%. Full mirror exclusion: 15–25%. "Every counterexample is asymmetric" needs C3 too: weeks | **High.** No mirror search found in the literature | Medium. Sub-case (i) is run33-sized with half the free orbits; (ii) has no hull trick | Low. CNFs exist; annealer wrapper about 1 day | **2nd** |
| **M3 Near-miss plateau** | ≤ 0.5%. Its only edge is that it searches real coordinates at 33 points | Low (data, not a theorem) | Medium. AlphaEvolve already ran this objective; what is new is complete face-level information | Good | Medium. About 1 day to write a count mode for `sat.c`, plus about 13 core-h | **3rd** |
| **M4 Hull split + blow-up program** | about 0% (blow-up program about 0.5%) | Hull size 6 excluded: 30–40%. Hull size 5: about 20%. Blow-up closure is uncertain because Lemma 14 is only in garbled HTML | Medium | Medium | Medium; needs E1 first | **4th, conditional** |
| run33 as configured | about 0%. Any model is abstract, and 0 of 200,000 such 32-point models were realized by Krapivin–Przybocki–Heule | about 0%. No LRAT, and the frontier is growing | none | n/a | n/a | **pause** |
| `grow.py` | about 0% at the margin. Witness-derived starts, about 9% face coverage, duplicates | 0 | none | n/a | n/a | **stop** |

Source for the 0 of 200,000: https://arxiv.org/abs/2607.02958.

## 3. Ranked plan

New code would live in, e.g., `.cache/es7/etv/` or `experiments/etv-ladder-2026-10-20/`. Writing there needs your go-ahead, because this task was read-only.

### #1. ETV ladder at k = 7, with lemma injection and certificates (M1 + E1 + E2)

**Why first.**
- The instances are small and graded. Per rung, the ES(6) analogue costs 0.01 s, then 0.55 s, then 125 s. At k = 7, (7,4,7)@17 already closes in 0.8 s.
- Every SAT outcome gives an explicit construction. Every UNSAT outcome is a certifiable theorem.
- Schroeder's unreviewed point-set claim (7,5,6) = 25 ([Zenodo](https://zenodo.org/records/22842891)) gets an independent check in a stronger model.

**Files to write**
- `gen_etv.py`: reconcile `scratchpad/etv/gen_etv.py` and `scratchpad/enc/gen_etv.py`; the second adds `--mirror` and `--hull`.
  - Symmetry breaking: x-reflection as a lex-leader, σ(i,j,k) ↦ σ(N+1−k, N+1−j, N+1−i). y-reflection only when a = u.
  - Derive the joint lex-leader for the whole group; a unit clause plus a lex clause on the same pair is unsound.
  - No projective hull normal form here: caps and cups are affine notions.
- `crosscheck_bb.py`: import `.cache/erdos-szekeres-sat/lib/erdos.py` directly (no `fire` needed), emit their `etv_signotope` CNF, solve with our CaDiCaL, and require identical SAT/UNSAT on every control.
- `lemmas.py`: two-sided chain-end indicators e_r(q), plus totalizer cardinality constraints.
  - The argument: points that end no r-cup form a set with no r-cup, so there are at most N(a,r,7) of them.
  - At 27 points under (7,5,7): at least 17 points end a 4-cup (the cup-cap bound C(5,2) = 10), at least 11 end a 4-cap (Baek's 16, Lean-verified), and at least 7 end a 5-cup (C(6,3) = 20). The same holds for left ends.
- `cnc2.py` (E1):
  - exact weights (store depths; sum as integers or Fractions);
  - a global queue ordered shallowest-first;
  - GROW = 1.6 (the code default; the runs used 1.0);
  - BASE_LIMIT honoured on resume;
  - split only on orientation variables, consecutive triples first;
  - `cadical --lrat` per leaf, checked with `.cache/drat-trim/lrat-check`;
  - a script that checks the cube tree covers the whole space.
- `realize_fixedx.py` and `glue.py` (E2): exponential x-grid; LP in y with margin, alternating with x; exact rational re-check; signotope or point concatenation for gluing; final check with `countk.c` and `brute7`.

**First experiment (under 1 day, 4 cores)**
1. Encoder correctness, about 1 h on 1 core.
   - The Baek–Balko cross-check on every k = 5 and k = 6 rung, and on (7,4,7)@16 SAT / @17 UNSAT.
   - Positive controls at the conjectured sizes: (7,5,6)@25, (7,5,7)@26 and (7,6,6)@30 must be SAT; the classical blocks realize them. Any UNSAT here means a bug.
   - LRAT for (6,5,6)@16 and (7,4,7)@17.
2. Lemma A/B test, about 30 core-min: (6,5,6)@16 with and without cardinality constraints, against the 125 s baseline.
3. (7,5,6)@26, 12 h: plain CaDiCaL with LRAT on 1 core, plus `cnc2` on 3 cores. Log open-cube count and depth every 30 min.
4. Tree-size estimate for (7,5,7)@27, about 3.3 core-h: 200 random orientation-only cubes of depth about 20, 60 s budget each.

**Continue if any of these holds**
- (7,5,6)@26 closes within 24 h, or its open count falls monotonically over the last 6 h.
- The lemmas give at least a 5× speed-up at k = 6.
- The (7,5,7) estimate is at most about 500 core-h.

Then queue (7,5,7)@27 with proofs. A model at any rung means stop everything and realize, glue and verify.

**Stop the UNSAT direction if** the frontier looks like run33's (open count flat or rising, depth growing). In that case keep only cheap model-finding runs: random seeds, and initial phases from Balko–Valtr's colourings (https://kam.mff.cuni.cz/~balko/ES_SAT). Downloading those needs your OK.

**Payoff if it works:** a short paper with the Proposition, certified N_sig(7,5,6) = 25 and perhaps N_sig(7,5,7) = 26. The Proposition plus (7,5,7) UNSAT gives a clean corollary: no heptagon-free 33-point set splits deep-below in any direction with both parts of size at least 2. That strengthens Baek–Balko's Theorem 8 at k = 7.

### #2. Mirror-symmetric class: abstract exclusion plus a realizable-first arm (M2)

**Why.**
- 3-fold rotation and mirror are the only symmetry classes possible at 33 points.
- No mirror search appears in the literature we surveyed.
- Mirror-symmetric extremal 32-point sets exist (our exact check), so the class is not empty.
- The abstract side gives a theorem; the annealing side needs no realizer.

**Steps**
1. Validation, about 1 h.
   - `mircheck.py` on 1,000 random exactly mirror-symmetric 33-point sets: every orientation must satisfy the clauses.
   - Settle the `m16k6` surprise independently: run the mirror annealer at k = 6 with 16 points. If it finds a hexagon-free mirror set, the encoding is wrong. If it never does, the result becomes a nice side fact: no mirror-symmetric extremal set at k = 6.
2. Abstract runs, 12 h.
   - `hm33k7.cnf` (sub-case (i), 47,002 variables / 684,494 clauses): plain CaDiCaL with LRAT on 1 core, plus `cnc2` on 2 cores.
   - Sub-case (ii): `m33k7.cnf` plus a y-reflection unit and an "axis point is interior" clause, on 1 core.
   - Substitute variables instead of adding equivalence clauses: about 2,480 / 2,736 free orbits instead of 4,960.
3. Mirror annealer, about 300 lines over `.cache/es7/trackA/src/gen_core.h`.
   - State: 16 representatives plus the axis point. Energy: the exact number of convex 7-gons.
   - Exact axis scan of every heptagon-free mirror 32-point set visited: at most C(32,2)+1 = 497 intervals.
   - Control: mirror-32 at k = 7 must reach E = 0 from random starts.

**Continue if** sub-case (i)'s frontier shrinks while run33's grows, or the minimum axis multiplicity reaches 1–2 and keeps falling. **Stop if** after 24 h sub-case (i) behaves like run33.

**Later:** D3 (5 orbits of 6 plus 1 of 3; a quick sub-case), then the lighter C3 encoding by angular order. Restart run33m3 under `cnc2` in the meantime; that run is the C3 class.

### #3. Exact near-miss plateau walk, gated by a k = 6 null (M3)

**Why.** It is the only line that searches real coordinates at 33 points with complete local information. The plateau is cheap to reach: about 35–40 CPU-s from random starts. Yet it has had only about 20 CPU-min of exploration (26 short walks).

**Steps**
1. Copy `.cache/es7/trackA/src/sat.c` to a new `satcount.c`. Emit min(m,3) per face, where m is the number of 7-gons a new point there creates, plus the blocking heptagon when m = 1. Validate against `cgon count` at sampled points and at k = 6.
2. Null distribution at k = 6. Since ES(6) = 17, every k = 6 set is saturated. Measure the m = 1 face counts for deletions of one-hexagon 17-point sets. This takes minutes.
3. Sweep the 7 deletions of each of 274 seeds: `nearfull_p2c.txt` (147), `nearfull_p2d.txt` (126) and AlphaEvolve's set (`scratchpad/ae/pts.json`). That is about 1,918 sweeps at an estimated 25 s, about 13 core-h.
4. Guided relocation walk with a tabu list on `gen.c` canon signatures, against plain near-mode walks at equal CPU.

**Continue only if** the k = 7 m = 1 counts are clearly heavier-tailed than the k = 6 null, or the guided walk is at least 3× faster at re-reaching heptagon-free sets. **Otherwise stop:** a set with 1 near-miss is generic. The minimum number of convex pentagons among 9 points is already 1 ([Aichholzer–Hackl–Vogtenhuber](https://publications.ist.tugraz.at/files/publications/geometry/ahv-o5g5h-11.pdf)).

### #4 (conditional). Proof-direction rebuild (M4)

Start only after `cnc2` has proven itself on #1.
- First an ES(6) hull-split calibration (minutes).
- Then a hull-size-6 pilot on 2 cores for 12 h, with the proved cardinality lemmas. In run33's 32-point frame: at least 16 points end a 4-cup and at least 17 end a 4-cap.
- If hull size 6 does not close in a day, retire run33 for good.
- The blow-up program waits until Lemma 14 is confirmed from the PDF or journal version.

## 4. What to stop or change among current runs (your call; I touched nothing)

1. **Stop the 4 `grow.py` processes now.** They are depth-1 relocations of 168 witness-derived sets, with about 9% face coverage per set after 40 seeds and repeated exact duplicates. Saturation there is expected (Damásdi et al., https://arxiv.org/abs/2312.01223). This frees about 4 cores for #1.
2. **Pause run33** (4 workers). `state.json` is kept, so it can resume.
   - Since the audit its frontier grew from 149 to 164 open cubes and from depth 264 to 275.
   - It cubes only on auxiliary flags, which overlap in configuration space, and keeps no LRAT, so even a finish would not be a certificate.
   - Its cores go to #1 and #2. It comes back only as M4's case split under `cnc2`.
3. **run33m3** (2 workers): keep it until `cnc2` exists, then restart from `state.json` with shallow-first scheduling and LRAT. Cube [4, 554] (weight 0.25) must go first.
4. **Make no realization attempts** with the current realizers until E2 passes the 5-fold 16-point control.
5. **Run no more abstract-first SAT at 32/33 points** in the hope of a counterexample.
6. **Stop citing** "168,000 tested", "8,537 order types saturated" or "75% closed". Corrected wording:
   - 160,000 per-realization tests with duplicates;
   - one realization per order type;
   - one untouched quarter-weight cube.
   Fix the READMEs (audit items B5, B6, B10) when edits are allowed.
7. **Park the ES(8) family-completion work.**

Suggested core split after steps 1–2: #1 on 4 cores, #2 on 3, #3 on 2 (after about a day of coding), run33m3 on 2, leaving about 3 spare.

## 5. Material for the email to Prof. Suk (claims ranked by how safe they are; nothing drafted or sent)

**Safe to state**
- 65 ≤ ES(8) ≤ 311 is formalized in Lean (commit c019a54), along with ES(n) ≥ 2^(n−2)+1.
- Our searches so far found nothing. Word them honestly: about 160k per-realization saturation tests near the classical witness, and a non-converging cube-and-conquer without proofs.
- AlphaEvolve's public notebook comment claiming zero 7-gons and zero 8-gons is wrong. Their 33-point set has exactly one convex 7-gon and the 65-point set exactly one 8-gon (exact rational recount). The paper's own text says one. Every 32-point heptagon-free set derived from the 33-point set is saturated.
  - Paper: https://arxiv.org/abs/2511.02864. Notebook: https://github.com/google-deepmind/alphaevolve_repository_of_problems.

**State as "our derivation, possibly known"**
- The deep-below Proposition and the gluing recipes from section 1.

**State as "our check, code validated only on the classical construction"**
- Subercaseaux et al.'s 4-fold and 5-fold hexagon-free 16-point sets are not decomposable in any direction ([arXiv 2506.00224](https://arxiv.org/abs/2506.00224)).
- A mirror-symmetric extremal 32-point set exists.

**The plan:** the ETV ladder in the signotope model with LRAT, and mirror-symmetric exclusion.

**Questions to ask**
1. Did Baek and Balko complete (7,5,6) or (7,5,7) with their `etv_signotope` encoder?
2. Is Schroeder's (7,5,6) = 25 considered correct?
3. Is the Proposition known from Erdős–Tuza–Valtr 1996?
4. Is a certified mirror-class exclusion worth writing up?

## 6. Honest odds

The conjecture is proved for k ≤ 6. At k = 7, every realizable-model search has come up empty:
- our 160k tests and 8.5k pool;
- Krapivin–Przybocki–Heule, 0 of 200,000 abstract 32-point models realized;
- AlphaEvolve and our annealer, both stuck at exactly one heptagon;
- Baek–Balko's blow-up genetic algorithm up to k = 20.

The only known "counterexamples" live in the weaker pure-colouring model (Balko–Valtr, https://eurocomb2015.w.uib.no/files/2015/08/endm1938.pdf), and the signotope model at k = 7 is still open.

My subjective probability that ES(7) > 33 is about 5–10%. The chance that this laptop-scale program finds a counterexample in the next few months is about 1–2%, most of it in the ladder rungs and the realizable near-miss search. The realistic return is one or two rigorous partial results within a month:
- the deep-below Proposition plus a certified N_sig(7,5,6) = 25, independent of Schroeder;
- with luck, N_sig(7,5,7) = 26 or the mirror-class exclusion.

Those are honest, small-paper results and good material for Prof. Suk, even though they are not the counterexample.

## 7. Unconfirmed

- The Proposition and gluing recipes are our derivation. Erdős–Tuza–Valtr 1996 has not been read.
- Whether Baek–Balko ran a ≥ 5 rungs at k = 7 is unknown.
- `m16k6` UNSAT is unverified.
- All run-time and probability figures are estimates.
- Lemma 14's exact form and the proof of Theorem 8 in Baek–Balko are unverified.
- Schroeder's results are unreviewed.
- Baek's Lean repo was grep-checked, not rebuilt.

## Files referenced

- `.cache/es7/cnc/cnc.py` (lines 14, 31–35, 58)
- `.cache/es7/cnc/run33/state.json`
- `.cache/es7/cnc/run33m3/state.json`
- `.cache/erdos-szekeres-sat/lib/erdos.py` (`etv_signotope`)
- `.cache/erdos-tuza-valtr/ErdosTuzaValtr/Main/Main.lean` (line 74)
- `.cache/es7/trackA/src/sat.c`, `gen_core.h`
- `.cache/es7/trackA/data/nearfull_p2c.txt`, `nearfull_p2d.txt`
- `scratchpad/enc/`: `gen_etv.py`, `*.cnf`, `*.out`, `*.time`, `mircheck.py`
- `scratchpad/etv/gen_etv.py`
