# ROADMAP20261115 / SYNTHESIS: report of the resumed overnight workflow (15 Nov 2026, written 05:48-05:58 KST)

**Status: a research plan plus tonight's probe results. No new bound.** Nothing here is refereed. Labels follow
es-research §2: PROVED / CERTIFIED / EXACT TREE / COMPUTED / HEURISTIC. Every cost and every odds figure is HEURISTIC,
and the odds are subjective. "New" means only "not found in this search" (full check NOVELTY20261113B; bounded check
NOVELTY20261115, 03:00-04:20).

**Relation to README.md.** README.md in this folder (main session, 04:50, last changed 05:34) was written before the
topic syntheses, the probes and the completeness critic of the resumed run had finished. It is not modified here. Where
the two disagree, §5 says where and why; the main session decides which record to change.

## 1. Headline: what tonight concluded

- **ES(8) ≤ 308 is unchanged:** a computer-assisted chain, unrefereed and uncommitted, |S| ≤ 1 + 187 + 119.
  - The balanced 187 is Lean-checked (RESULTS.md A1).
  - The residual 119 rests on:
    - the budget-34 slices 18, 19 and 20 (EXACT TREE);
    - 1,020 CERTIFIED coupled rows;
    - the PROVED bridge;
    - the budget-33 baseline.
  - VERIFY308 (LO33N20261113/budget34/VERIFY308) re-checked budgets 34 and 35 with independent code.
  - The two budget-33 trees, (18,15) and (19,14), are EXACT TREE by `check_tree` only. No independently written checker
    has accepted them (VERIFY308/CHAIN_REVIEW.md line 24).
- **307 is not reached.**
  - Budget-35 (18,17) and (19,16) are EXACT TREE.
  - (20,15) is open. The context reports 42 of 8,065 contexts closed. The upper synthesis counts 202 contexts touched
    and 18 closed over w116-w127 (runs/b35s20/*.log).
  - (21,14) is open. It disappears if N66 ≤ 55 holds, and N66 ≤ 55 is undecided after two 3 h 10 min solves
    (N66N20261113).
- **Verdicts of the workflow, by topic:**
  - *Upper bound.* Two levers decide 307: the work-keeping (20,15) loop and N66 ≤ 55 by level-14 cubes.
    - Item 4, the F6-row insurance, is **parked by its own probe** (HEURISTIC). That makes N66 ≤ 55 the critical path.
    - Balanced 186 was re-costed at about 280 CPU-h for the search stage only (HEURISTIC). That figure was measured on
      a **restricted problem** (state 0 fixed), so its rank is held until a rerun with state 0 free.
  - *Delta conjecture: OPEN.*
    - The doubly-rooted necessary condition of LT-cover fails on abstract signotopes: 10 distinct sign vectors at n6/m11,
      n6/m12 and n7/m13 (COMPUTED, SAT models checked by brute force).
    - It holds on all 496 real sets tested (COMPUTED).
    - The realization probe was deferred.
  - *ES(7) lower bound.*
    - The colouring-27 repair is dead. Six of chi's values outside V force a 5-cap in every signotope completion
      (PROVED by a verifier).
    - (7,6,6)@31 windows at r = 2-5 around the classical middle 30 gave 0 SAT in 10,611 calls (COMPUTED, local only).
  - *ES(8) lower bound.*
    - 28 one-point-extension CNFs of 64-point octagon-free sets are UNSAT, CERTIFIED (cake_lpr 28/28, re-run 28/28 by
      a verifier). The geometric reading ("no point can be added") is COMPUTED.
    - The k=9 two-arm scan found no zero (HEURISTIC, float). Its best value, 80, came from the 104 seed, which cannot
      reach record size. The 112 seed bottomed at 1,344.

## 2. Ranked programs by topic (after probes and critic)

Ranking uses expected value = payoff × P / cost. CPU-h figures are HEURISTIC, with their basis given.

### 2.1 ES(8) upper bound below 308

1. **(20,15): make the live cut loop keep its work.** This is a hand-off to the main session, which owns
   esr-lo-b35s20*; no workflow agent runs it.
   - *First steps.*
     - Write run_tree_v5.py as a copy of run_tree_v4 with asserted diffs: `--on-witness=continue`; `--ctx` in chunks of
       at most 10,000 ids; WITNESS.json moved aside between chunks (otherwise fastbb2.cpp 1637-1651 makes the next
       chunk exit 3).
     - Select rows by greedy hitting set, at most about 300 per pass; never certify the union of candidates. Use
       slicedrv.py's batching rule (4 witnesses or 15 min).
     - Run one fastbb2 call per |M| class: |M| ≥ 7 first (3,970 open), then |M| = 6 (1,710), because the `--ctx`
       order is ignored (fastbb2.cpp 1720-1724). Split what remains with `--split-open=3`.
     - Audit each row batch in its own process (audit_followup_rows_v4 hit 300 MiB at v118u). Batches from v129 on
       must be audited before any closure claim.
   - *Precheck (critic §5.4, new).* Re-solve about 100 budget-34 slice-20 leaves (runs/s20/bb-s2) at budget 35, on
     1 thread for minutes, to test a warm start from the s20 tree. This buys robustness, not fewer nodes (about
     3.1e7 × 9 ≈ 2.8e8). Unchecked preconditions: the s20-v13 rows must be a subset of the b35s20 rows, and the context
     split must match.
   - *Cost.* About 200 CPU-h (110-450). Basis: Knuth 2.47e8-3.3e8 nodes × calibration 1.35 × overhead 1.5-1.8 at
     2.6-3.3 M nodes/CPU-h. P(EXACT TREE within 48 h of the switch) ≈ 0.35.
   - *Evidence when done.* EXACT TREE plus CERTIFIED rows, checked by fresh_replay_v3 and tcheck_b35 (two
     implementations).
2. **N66 ≤ 55 by level-14 cube-and-conquer.** Now the critical path.
   - *Before starting.* The owner decides on the 58.8 GB of b14h2/b14i2 partial LRATs, and the k9 memory slice is
     shrunk (§4).
   - *Method.*
     - Copy p2_batch.py with asserted diffs so it stores 'cube' (line 39 hard-codes `'cube': []`). Set ETV_A=4 and
       ETV_B=4 in the unit environment.
     - Cube on the sb pair (32,37) into 00, 01 and 11; cube 10 is killed by sb. Warm start from p2/s14/h2.json. Run
       2 cubes in parallel (2 × 2.9 GB) and the third after, each with RuntimeMaxSec ≈ 14 h.
     - Never rerun the b14h2/b14i2 configuration: `--seed` seeds only numpy (p2_batch.py line 32).
     - Budget for SAT rounds: every level-14 iteration on 13 Nov was SAT, with 4,974-7,363 violated quadruples.
   - *Cost.* 20-60 CPU-h. Basis: each level-11 cube took 35-52 % of the full lazy run (lm/cubeA-C.out against
     lm/full.out). On top: cake_lpr with a heap of at least 3.2 GB per cube, and raw LRAT at about 9.35 GB/h per slot,
     up to about 390 GB for 3 cubes × 14 h. cake_lpr time on about 130 GB per cube is not included. P(CERTIFIED within
     48 h) ≈ 0.3.
   - *Evidence when done.* CERTIFIED per cube, plus p2_verify and an independent cover check. With item 1 this gives
     ES(8) ≤ 307.
   - *Level 15 (N66 ≤ 54).* Gives 307 with today's trees. P ≈ 0.1 within 3 days. Start it only if level 14 is
     CERTIFIED while (20,15) is still open; otherwise aim at 306. It must be N5-free, because the N5 ≤ 65 LRATs were
     deleted.
3. **Evidence before any 307 claim (LEAN308 S0).** No new bound.
   - *What.* Build tcheck_b33 and pycheck_b33 from the VERIFY308 tools and run them on bb_66_55_leanrows and
     bb_65_56_leanrows (data/lo33-20261113). Hash-compare against VERIFY_LO's tars.
   - *Cost.* About 1 CPU-h: 2 threads, about 35 min, under 1.5 GB. P ≈ 0.9.
   - Every new slice, cube and balanced-65 tree gets the same two-implementation audit.
4. **Balanced 186 (budget 65 warm start from the 7,048,218 budget-64 leaves).** This is the only 307 route that is
   independent of the residual cases. Held at rank 4, conditionally.
   - *Measured tonight.* Arm B (`--dtop=0 --dmid=0`) projects 279 CPU-h for the search stage (bootstrap 260-304; an
     independent resample gave 260-271).
   - *Not included.*
     - Python glue: 9-12 CPU-h (the probe's 21 CPU-h was refuted).
     - Tails: unmeasured; the bound is only < about 17-19 % of contexts, since 0 of 16 contexts failed.
     - check_tree replay of about 6.5e7-1.0e8 new leaves.
     - Any Lean check: about 500 CPU-h, unmeasured. The 310 Root already used 20.7 GB RSS, so a Lean check needs a
       restructured Root to fit the 24 GB cap.
   - *Blocking caveat (critic §5.1).* leaf65ab.py fixes state 0 as occupied; the official trees leave it free. The
     re-solves therefore cover only part of each leaf's region. Only 2 kept subtrees were checked against the balanced
     setting.
   - *First step.* Rerun the paired 160-leaf A/B with state 0 free, keeping the subtrees for a check_tree positive
     control (about 0.1 CPU-h). Alternatively, write an argument that fixing state 0 loses nothing.
   - *Also before any campaign.* Run a CP-SAT hunt at budget 65 with ES8UPPER20261105 witness_hunt.py (1-2 CPU-h).
   - *Evidence when done.* EXACT TREE over Lean-proved rows. The earlier "P ≈ 0.35-0.5 within 2-3 weeks" is withdrawn
     until the rerun.
5. **F6 derived row h(F6) ≥ 7: PARKED.** Probe 2 found hits for 16 of 42 patterns, at or below its own 50 % threshold.
   - *Salvage (minutes).* Certify and audit the 3 minimized F6-only cores (11, 11 and 13 states; probe2/f6wit.jsonl;
     COMPUTED in the fast model only) with cut34_v4, then hand them to the (20,15) packet. They kill 7 of the 42
     witness patterns (HEURISTIC). For scale, 313 witness-killing rows moved (20,15) by only 1.1×.
6. **(21,14) tree: fallback only.**
   - *Cost.* 700-6,000 CPU-h. Basis: Knuth 1.85e9-2.59e9 nodes, with calibration and overhead.
   - Decide only after the per-cube costs of item 2 and the rerun of item 4 are known. A multi-day job needs the
     owner's OK.
7. **One verdict on the F-side lever (critic §5.3).** Three entries are one lever:
   - the Baek-block attainment rows 22→21 (README §1 row 3, "promising");
   - "all nine Baek blocks at 21" (dropped by the upper synthesis);
   - N5 ≤ 63/62 by ETV5N cores at 21/22 holes (delta item 3).

   **This synthesis' verdict:** h(F) ≥ 21 is the stalled part. ETV5N stalled at N5 ≤ 65 after 439 cores, probe 2
   parks F6, and the N5 ≤ 65 LRATs are deleted. N5 ≤ 63/62 has no credible cost basis, so do not schedule it.

**Dropped (upper synthesis, unchanged):**
- the monolithic level-14 portfolio;
- core-seeded relaxation;
- capacity-row what-if pricing;
- the greedy-D8 proof (shape lemma fails on 1,030 of 1,035 red 4-caps);
- the mono5 N5 ladder;
- Lean S4 and S7 for now;
- the ctx-2565 witness (already cut by v130 row 3969).

### 2.2 Delta-reduction conjecture (M(5;8) and consequences)

1. **Consequence ledger and correction note.** 0.1 CPU-h, P ≈ 0.95. Evidence: PROVED arithmetic over Lean, CERTIFIED
   and PROVED links, plus COMPUTED exact witness checks.
   - *The ledger.* ES(8) ≤ 189 + c5 + c66 (THEORY310N §2 Lemma A, |H| ≤ 187 Lean,
     Partition.forces_of_population_bounds), with N66 ≤ 56. Every row below is conditional on OPEN statements.

     | Statement | ES(8) bound |
     |---|---|
     | weak Conj(8) | 303 |
     | weak Conj(7) + weak Conj(8) | 298 |
     | strong Conj(8) | 297 |
     | N5 ≤ 62 | 307, with no budget-35 tree |
     | N5 ≤ 63 | leaves only (21,14) |
     | deletion form | N5 ≤ 22 + M(5;7) + e |

   - *Prior art (critic §5.7).* The strong-Conj(8) row must cite GLitchfield's PASCAL-SPLIT, which equals the strong
     form at u = k = n; the a = n split is refuted at n = 6.
   - *PS(6,6) → 304* rests on Schroeder's literature value M7(5,6) = 25 (not re-certified) and on N5 ≤ 65 (LRATs
     deleted). The N5-free arithmetic gives 305.
   - *Superseded statements* (ETVTHY l.183 and l.383, ETV7SAT §7.1, DELTA2N l.83-84, FLAYER l.34/79/577, THEORY310N
     §1 W1/W1+) are listed apart from the false one (ETV5N l.18/25).
   - Inserting the ledger into budget34/bridge needs the owner's OK; otherwise it becomes a new record.
2. **Doubly-rooted / realization test of LT-cover.** About 0.2-0.5 CPU-h. Tonight's probe DR-REAL was deferred and
   computed nothing.
   - *First step.* Calibrate realize2.py on signotopes of real 11-13-point subsets of ETVTHY pool sets. Its 15-of-15
     and 4-of-4 control failures (Synthesize stage) are uncalibrated and decide nothing.
   - *Then.* Try to realize the 10 distinct sign vectors and check any realization with chk2.py (exact integers). Also
     run d8_14.cnf (sha 485c0385…) for at most 10 min.
   - *Evidence.* COMPUTED. One realization checked by chk2.py would be an exact counterexample to LT-cover_6 or
     LT-cover_7.
   - *Wording fixed (critic §5.9).* The SAT models show that a proof needs *some realizability property*, not
     "metric uniformity" specifically.
3. **Re-certify the 15-point weak (5,7)/(5,8) frontier.** About 1 CPU-h, after the main session's jobs end. E1 must
   match DELTA2N's cnf_hashes, plus E3 with `--sym none`. Evidence: CERTIFIED only on cake_lpr's exact line; keep the
   proofs as zstd. This is the conjecture's only computational support, and its LRATs were deleted before any
   re-run.
4. **Deletion form W_beta[e]: test only on known obstructions.** About 0.3 CPU-h. Tonight's probe DT-OBST was deferred
   and computed nothing.
   - *Run.* mts.cpp on real12, real15, the 18-point n7 witness and the n7/14 and n8/16 repair witnesses. A durable copy
     of mts.cpp is in scratchpad-snapshot-20261115/mbeta.
   - *Evidence.* COMPUTED. A CERTIFIED result needs a clause-justification checker first.
5. **LT-cover written work.** Gated on item 2. Write the reduction as a corollary of envelope Lemma 5 plus the slope
   iff (d). Prior for LT-cover_8 ≤ 1 %.
6. **Lean capacity interface: deferred** (THEORY310N §6.4 gate). If Lean time is spent, do the catalog Lemma A first.
7. **Direct N5 ≤ 63/62 costing: replaced** by the single F-side verdict in §2.1 item 7.

### 2.3 ES(7) lower bound (33-point heptagon-free sets)

1. **Records-only cost note for the exhaustive route.** 0 CPU-h, about 1 agent-hour, HEURISTIC.
   - *Contents.* C3-S against C3FINAL, the cost ladder of the symmetric classes, the gate estimates (B2, B3, ETV7SAT
     §6.3, gotrevor ≥ 811 CPU-h censored) and HS Table 2 (×1.6-4.3, constant factors only).
   - *Withdrawn.* The unsourced "≥ 15,000 / ≥ 17,000 CPU-h".
   - *Conclusion.* A new structural idea must come before any exhaustive compute.
2. **(7,6,6)@31: exact seed mining from realized 32-point pools.** ≤ 1 CPU-h. Evidence: EXACT for mined subsets.
   - *Windows done tonight.* All r = 2-5 windows around mid30 are UNSAT (COMPUTED). By the probe's rule there is no
     bulk window sweep around mid30.
   - *Remaining.* A C miner over A's pool sets, F2's 93 glued sets and D2's swept states. Look for 30- or 31-point
     subsets with cap ≤ 5 and cup ≤ 5 in some sweep direction; a 31-point hit is a witness. Run windows only on mined
     seeds (r = 6 has exactly 7,242 calls, about 0.2-0.65 CPU-h).
   - *Before any "untried" wording.* Read Balko-Valtr EJC 2017, and write the double-gluing note (ES7SPLIT Cor. 4
     twice).
3. **Shape-variable partition test on the owner model.** About 1.5 CPU-h at about 1.5 GB, P(GO) ≈ 10 %, HEURISTIC.
   Test (3,4,7,26) with and without packets, 3 seeds per configuration.
4. **M(5;7) ladder: owned by the ETV/upper program.** The case-B LRAT c36_tle22.lrat (5,233,911,342 bytes) needs one
   spec and one owner (§5.8). This synthesis adopts the stricter upper-side spec: heap 4,300 then 4,600, MemoryMax
   ≥ 6.2 GB. Evidence: CERTIFIED only on the exact line. Case B alone does not give M(5;7) ≤ 35.
5. **One-point extensions of the six C7 maxima.** 0.5-1 CPU-h. A CERTIFIED footnote to SYMMAX, of low value.
6. **Near-mirror M16+1 in the zcnf model.** About 3 CPU-h calibration. Soundness note and literature check first.
   Stop if t = 1 is more than 10× slower than SYMZ.
7. **Colouring-27 repair: DROPPED** (critic §5.5). Every signotope completion of chi's outside-V values contains the
   5-cap 9,11,13,17,19 (PROVED). The minimum-flip fallback exists only if ETV(27;5,7,7) is SAT; otherwise it amounts
   to proving that instance UNSAT, at 1e4-1e6 core-h (B2, B3), not ≤ 0.5 CPU-h.
   - *Salvage.* Move the verifier's cake_lpr-accepted ring LRATs out of its scratchpad into a work dir, or re-run
     certify_cnf.sh. Until then, phase A stays COMPUTED.

**Dropped earlier (unchanged):**
- program 3's x-sorted overlays (identical to record C's m33k7 and hm33k7);
- program 2's compute steps;
- program 4's steps 4-7;
- program 1's growth and bulk parts.

### 2.4 ES(8) lower bound (65-point octagon-free sets, symmetric maxima)

1. **ABSAT8-core (radius 0).** The compute is cheap; the evidence work remains (critic §5.10).
   - *Done tonight.* 28/28 CNFs UNSAT, CERTIFIED.
   - *Untested.* The 7 seven-fold types, which need exact Z[ζ7] tables cross-checked with MPFR, and the walker end sets
     beyond w1-w3.
   - *For the geometric reading* (COMPUTED now): a one-page soundness note (sector, triangle and slot lemmas) and an
     independent plain-C encoder. crit.cpp ran on only 4 of the 28 sets.
   - *Value check.* Run the encoder on a DDSZ saturated set of non-maximum size. This is the only step that shows
     whether abstract saturation says more than geometric saturation.
   - *Cost.* Compute is about 0.29 CPU-s per set (measured), plus about one agent-day. P ≈ 0.85.
   - A targeted literature check comes before any "new" wording.
2. **CONE4 gate.** About 2 CPU-h in a 5 GB unit (calls at 3-4 GB), once memory is free. COMPUTED at fixed phases.
   - *Gate.* lpcegar2.py's first SAT call at 8 annealing and 4 random t=14 vectors, (a) with root units only and
     (b) with threshold chains added.
   - *Outcomes.* Park CONE4 if (a) is SAT at any vector. If it is UNSAT at all of them, build the exact finite
     abstraction (30 CPU-h box). The full line is 60-200 CPU-h, P ≈ 0.05-0.15.
   - *Record the negative now.* ALGAN model 30 satisfies encoder A + chord + cone + cell(B ≤ 4) + binorder (COMPUTED).
3. **Two-arm Phase 0 (k=9): re-target or park the construction arm** (critic §5.6).
   - Do **not** run the scheduled lpc8.py follow-up on the 104-seed slots. 104 + 8 = 112, and PRIMEFOLD already has
     N9 = 0 sets at 112 and 120.
   - The 112 seed bottomed at 1,344 (about 168 per orbit), above the 150 drop level, so the decision rule's "drop"
     branch applies to the seed that matters.
   - *Keep.* The cheap EXACT step: label8.py run structure of c8_104 and c8_112 in Z[√2].
4. **Two-arm one-descent theorem.** Gated behind the ring and its written completeness check from ring_cases.py.
   25-400 CPU-h. CERTIFIED per cube.
5. **Radius-1 joint two-point model.** Sizing only, after item 1. 2 CPU-h of sizing; the full run is 20-300 CPU-h.

## 3. Probe results tonight (as verified)

### Upper, probe 1: bal65-depth-ab

Done, about 0.02 CPU-h. Work dir: data/roadmap-20261115/upper/probe1.

- **Survives, HEURISTIC.**
  - *Arm B* (`--ktop=16 --klow=4 --dtop=0 --dmid=0`): 0.1427 s/leaf weighted, so 7,048,218 × 0.1427 s = 279 CPU-h
    (281 on wall time). Bootstrap 260-304 CPU-h; an independent resample (seed 4242, 16 other contexts) gave 260-271.
    The ≤ 0.12 s branch is not met.
  - *Arm A* (`--dtop=8`): 0.3716 s/leaf, 727 CPU-h (about 672-786). This confirms the top of the earlier 530-760 band
    and contradicts its process-start premise: process start is about 4.5 ms.
  - *Pairing.* B/A = 0.392 of solver time. B used 1.58× the nodes but was faster on all 160 leaves. 40 leaves were
    reproduced exactly.
- **Survives, COMPUTED.**
  - All 320 solves ended rc 0. Solver verdicts on a 160-leaf sample; no subtree was replayed by check_tree.
  - Exact margin check: bal.rows equals balanced-v2-source.json (3,131 rows). All 160 sampled leaves have budget-64
    margin 1-671, and none closes at budget 65 with its stored certificate.
- **REFUTED: the overhead finding.** The probe gave 21 CPU-h of Python glue; the verifiers found about 9-12 CPU-h,
  because per-context loads are paid once per context.
- **Downgraded.**
  - The 1.9 % rule-of-three tail bound assumes independent leaves. With the clustered sample it is only < about
    17-19 % of contexts.
  - The 320-520 CPU-h Lean extrapolation is unmeasured.
  - The probe's "Result=success" readout showed systemd defaults. Success rests on the journal and the 160/160 rc-0
    records.
- **Critic.** State 0 was fixed as occupied, so the cost is for a restricted region (§2.1 item 4).

### Upper, probe 2: f6-witness-cores

Done, 0.071 CPU-h. Work dir: data/roadmap-20261115/upper/probe2. **The verify stage did not check these findings; they
are stated as the probe reported them.**

- At K=19, 16 of 42 witness patterns (38.1 %) had an F6-only UNSAT subset in coupled.fast_solve (HEURISTIC). The
  probe's own rule therefore parks item 4.
- Pattern 11 contains pattern 5's 13-state core, which makes 17 of 42 (40.5 %).
- The 3 minimized cores (11, 11 and 13 states) kill 9,331 of the 148,628 allowed patterns and 7 of 42 witness patterns
  (COMPUTED in the fast model). Nothing was certified.

### Delta, probes 1 (DR-REAL) and 2 (DT-OBST)

Both **DEFERRED; nothing computed; no evidence either way.**

- They stopped on their procedures' 05:15 gate, while the stage allowed jobs until 05:40.
- **Survives (file facts only).**
  - 17 input files were copied byte-exact to delta/probe1/inputs. The check line in probe1/README.md points to a
    nonexistent file; use `(cd inputs && sha256sum -c ../SHA256SUMS)`.
  - The 15 failure files have 11 distinct byte contents and **10 distinct sign vectors**. Nothing was realized.
  - The *.real.json files hold no coordinates.
  - mts.cpp (sha256 c25de35c…) also has a durable copy in scratchpad-snapshot-20261115.
- **REFUTED: "the unit name esr-agx-delta-1-droot fits both naming rules".** It follows the allowance pattern and is a
  second deviation from the procedure's esr-agx-droot.

### ES(7), probe es7lb-nearwitness

Done, about 0.11 CPU-h. Work dir: data/roadmap-20261115/lower7/probe1.

- **Survives, COMPUTED.**
  - The self-checks reproduce chi: sha256 b42aebe4…d484, 383 violated packets, cap 4, cup 6.
  - The CNFs are byte-identical to fresh gen_etv output.
- **Phase A.** Rings F0-F3 are all UNSAT (COMPUTED).
  - A verifier's CaDiCaL 2.1.3 + cake_lpr run printed "s VERIFIED UNSAT" for all four. The proofs exist only in its
    scratchpad, so the label stays **COMPUTED** until they are re-run into a work dir.
  - Sharpened: the contradiction needs only the packet and no-5-cap clauses. The forced 5-cap 9,11,13,17,19 is
    **PROVED** (a short propagation argument plus an exact unit-propagation check).
  - The probe's "comes from cap, cup and 7-gon clauses" is corrected accordingly.
- **A2 threshold.** Quick UNSAT ends somewhere between 80 % and 95 % of the outside-V triples freed (HEURISTIC
  bracket, 3 samples per level). At 98 % freed and with no assumptions, the runs are UNKNOWN at 2e5 conflicts.
- **S0.** chi outside V extends to a signotope (SAT, model checked exactly). The model is not a witness: cap 5,
  cup 8, polygon 8.
- **Phase B.** The seed and both controls pass.
  - At r = 2, 3, 4 and 5 respectively, 935, 1,780, 3,052 and 4,844 windows are all UNSAT: 0 SAT and 0 UNKNOWN in
    10,611 calls (COMPUTED).
  - An independent Glucose4 re-run gave the same counts.
  - Local scope only: x-consecutive windows of one 30-point set, gaps within ±2.
- **Downgraded (label too strong) to HEURISTIC: the cost note.** Timings vary 1.1-3× with load. r = 6 has exactly
  7,242 calls (about 0.21-0.26 CPU-h, up to about 0.65); r = 7 has 10,320 calls, so 1.2-1.8 CPU-h, not "≥ 1.5".

### ES(8) lower, probe 1: ABSAT0-BATCH

Done, 0.014 CPU-h. Work dir: data/roadmap-20261115/lower8/probe1.

- **CERTIFIED: all 28 CNFs are UNSAT.** They cover the 17 pilot sets, the walker end sets w1-w3 and the 8 vertex
  deletions of AlphaEvolve's 65-point set.
  - cake_lpr printed exactly one "s VERIFIED UNSAT" line for each, and a verifier re-ran it with 28/28 again.
  - The hashes match certify.jsonl and summary.tsv, and the LRATs are kept as zstd.
- **Downgraded (label too strong).** "No point, real or abstract, can be added" is **COMPUTED**: it depends on
  absext.cpp's soundness, for which there is no written note and no independent encoder. It covers these 28 sets only.
- **COMPUTED.**
  - The AlphaEvolve set has exactly 1 convex octagon, with vertices {0,1,15,23,27,29,30,57}. A second counter written
    by the verifier confirms this.
  - crit controls passed on 4 of 28 sets; overflow kept them off c2_64points_k8 and the AE deletions.
- **HEURISTIC.** Encode + certify costs 0.285 CPU-s per set, so about 0.8 CPU-h per 10^4 similar sets.
- **Deviation.** cpu_free.sh printed 0. The unit started at CPUQuota 70 %, which kept the sum at 16.0 at launch.

### ES(8) lower, probe 2: K9ARM-SLOTS

Done, about 0.41 CPU-h. Work dir: data/roadmap-20261115/lower8/probe2.

- **Survives (HEURISTIC float control).** cnt9.c is byte-identical to the LBK9OCT copy and reproduces PRIMEFOLD §5:
  K=9 gives 0 on the 104, 112 and 120 sets, and K=8 gives 1,153,006,585 on the 120 set.
- **Not independently verified** (stated as the probe reported them; HEURISTIC float counts).
  - The specified run found minima of 1,344 (112 seed) and 18,856 (104 seed).
  - The extension found 80 and 88 on the 104 seed (slot 3 gap 4, and slot 1 gap 8). A separate program using the same
    counter reproduced them.
  - The 112 seed has an apparent floor of 1,344.
  - No zero was found, so nothing went to exact_check.sh.
- **Critic.** The 1-149 rule fired on the wrong seed (§2.4 item 3).

## 4. Cross-topic priorities (16 threads / 24 GB)

The completeness critic's resource figures are the syntheses' own; this synthesis did not read the memguard config.

- **Memory.** The k9 slice (14,000 MB) plus the n66 track (9.5 GB) is already about 23.5 of the 24 GB.
- **Threads.** The 16-thread cap cannot hold all of these at once: (20,15) at 10-12 threads, the N66 cubes at 2-3
  slots, balanced 186 at 4-8 threads and the ring at 2.
- **Disk.** 942 GB was free at 05:45.

**Recommended order:**

0. **Owner decisions, which block what follows.**
   - The 58.8 GB of b14h2/b14i2 partial LRATs and the 70 GB of m9 partials.
   - Shrinking the k9 ring to at most 1 job, with a smaller slice.
   - One owner and one spec for the case-B cake_lpr.
   - Commit or push of the 308 chain: not this workflow's call.
1. **When esr-lo-b35s20* ends.**
   - Precheck: the warm-start test of 100 leaves (1 thread, minutes).
   - Start the run_tree_v5 (20,15) loop at 10 threads, about 20 h (§2.1 item 1).
2. **In parallel, once memory is freed.** N66 level-14 cubes, 2 slots at about 2.9 GB each, then the third. When a cube
   needs cake_lpr (heap ≥ 3.2 GB), stop the other slots first.
   - Budget: 10 + 2 + 1 (ring) + 0.3 (memguard) = 13.3 threads, leaving about 2.7 threads for light work.
3. **Light items in the remaining threads** (each ≤ about 1 CPU-h, 1-2 threads):
   - LEAN308 S0 (§2.1 item 3);
   - certifying the 3 F6 cores (§2.1 item 5);
   - the delta ledger (§2.2 item 1);
   - the calibrated DR-REAL (§2.2 item 2) and DT-OBST (§2.2 item 4);
   - the ES(7) cost note and seed miner (§2.3 items 1 and 2);
   - the ABSAT8 soundness note and independent encoder (§2.4 item 1);
   - label8.py;
   - the ring completeness write-up.
4. **After item 1 ends.**
   - The balanced-65 A/B rerun with state 0 free (§2.1 item 4).
   - Then choose the balanced-186 campaign (4-8 threads, weeks) over the (21,14) tree, unless N66 ≤ 55 has already
     removed (21,14).
5. **When at least 6 GB of memory is free.**
   - The case-B cake_lpr (heap 4,300 then 4,600, MemoryMax ≥ 6.2 GB);
   - the CONE4 gate (5 GB unit);
   - the ES(7) shape-variable test (1.5 GB);
   - the 15-point frontier re-certification (§2.2 item 3).
6. **Parked:**
   - the F6 row;
   - the colouring-27 repair;
   - lpc8.py on the 104 seed;
   - the (21,14) tree, unless both N66 ≤ 55 and balanced 186 fail;
   - N5 ≤ 63/62.

**Odds (subjective, HEURISTIC).** ES(8) ≤ 307 within a week is about 0.2, via items 1 and 2 of §2.1. The "about 0.4
within three weeks" figure is withdrawn until the state-0-free rerun. ES(8) ≤ 306 within two weeks is below 0.1. Any
such bound would be computer-assisted and unrefereed.

## 5. Corrections from the completeness critic (05:47) and how they are applied

1. **The balanced-186 cost was measured on a restricted problem** (state 0 fixed). Applied: rank held at 4,
   conditional on a state-0-free rerun, and the 3-week odds are withdrawn.
   - README.md §1 ranks this program 5th; this file ranks it 4th, conditionally. The main session should make one of
     the two records match the other.
2. **Item 4 (F6) is parked by its own probe, so N66 ≤ 55 is the critical path.** Applied in §2.1 items 2 and 5, with
   the 3-core salvage.
3. **The records disagree on the F-side lever.** Applied: one verdict, in §2.1 item 7. It conflicts with README.md §1
   row 3 ("promising").
4. **New lever: warm start of (20,15) from the s20 tree.** Applied as a precheck in §2.1 item 1. Its preconditions are
   unchecked.
5. **Colouring-27 repair is dead, and its fallback was mis-costed.** Applied: dropped, in §2.3 item 7.
6. **Two-arm: the decision rule fired on the wrong seed.** Applied: no lpc8.py on the 104 seed (§2.4 item 3).
7. **Stale references and overstated claims.**
   - *Literature.* Cite NOVELTY20261115. Per the critic's reading, it records Schroeder's 319 as the newest public
     bound (Zenodo 10.5281/zenodo.22842891) and Mojarrad–Vlachos's 408 as the best refereed one. This file did not
     re-read that record.
   - *Strong Conj(8) row.* Needs the PASCAL-SPLIT prior art (§2.2 item 1).
   - *k9 ring count.* The context says 59/175 cyclic and 2/95 linear CERTIFIED. STATUS20261115_0450 says 79+ by 03:27,
     with verify_cycx on the first 30 only. Stated here as "CERTIFIED per CNF, cover check on 30"; this file did not
     recount.
   - *Tree checks.* STATUS0450's "Trees … independently re-checked (VERIFY308)" covers budgets 34 and 35 only; the
     budget-33 trees are check_tree only (§1, §2.1 item 3).
8. **Resources were not reconciled.** Applied in §4: one schedule and one case-B spec (the stricter one).
   - Item 2's disk use and cake_lpr time were added to its cost.
9. **Delta "metric uniformity" overstated.** Applied: reworded to "some realizability property" (§2.2 item 2), with
   10 distinct sign vectors.
   - Still open: check that scratchpad-snapshot-20261115 contains droot*.cpp and the CNFs. The probe did not save
     them, and this file did not check.
   - 16 Nov (main session): scratchpad-snapshot-20261115 and the full copy scratchpad-snapshot-20261116 each hold
     four `droot*` files. The CNFs were not checked by name.
10. **"ABSAT8 compute essentially done" overstated.** Applied in §2.4 item 1: the remaining sets and the evidence work
    are listed.

## 6. Files and work dirs

- **Records:**
  - archive/es7-2026-10-19/results/ROADMAP20261115/README.md (main session; not modified) and ES7_FEASIBILITY.md;
  - LO33N20261113/budget34 (README, VERIFY308, bridge, tools, audit);
  - N66N20261113;
  - STATUS20261114_2220 and STATUS20261115_0450;
  - SATOPEN20261113 (tools/k9/ring_cases.py);
  - NOVELTY20261113B and NOVELTY20261115;
  - DELTA2N20261113 and DELTA3N20261113;
  - ETV5N20261113 and ETV7SAT20261113;
  - FASTBB20261113/tools (fastbb2.cpp, slicedrv.py).
- **Workflow outputs:** /home/jay/research/data/roadmap-20261115/
  - agent_results_roadmap.jsonl, agent_results_extra.jsonl and overview.txt;
  - scratchpad-snapshot-20261115/ (durable copy of the tmpfs scratchpad, including dr/, mbeta/ and absext8/).
- **Probe dirs:**
  - .../upper/probe1: A.jsonl, B.jsonl, leaf65ab.py, leaf65ab.diff, SHA256, OUTPUTS.SHA256;
  - .../upper/probe2: f6wit.jsonl, f6wit.diff, sha256_*.txt;
  - .../delta/probe1: inputs/, SHA256SUMS, README.md;
  - .../delta/probe2: README.md;
  - .../lower7/probe1: etv27.cnf, etv31_667.cnf, nb31.tsv, c27repair.tsv, phaseA*.py;
  - .../lower8/probe1: absat/cnf, cert/*.lrat.zst, summary.tsv, certify.jsonl;
  - .../lower8/probe2: zeros.tsv (empty), arm2.cpp, arm3.cpp.
- **Main-session work dirs:**
  - /home/jay/research/data/es308-20261114 (runs/s20/bb-s2, runs/b35s20);
  - /home/jay/research/data/lo33-20261113 (bb_66_55_leanrows, bb_65_56_leanrows);
  - /home/jay/research/data/etv7sat-20261113/run/c36_tle22.lrat.
- **Temporary:** /tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/1e71bc06-5c09-4f54-ae48-3fca76aaa352/scratchpad
  (RAM-backed). It holds the verifier's ring LRATs (§2.3 item 7).
  - A full durable copy with the same relative paths (16 Nov 00:55 KST) is at
    /home/jay/research/data/roadmap-20261115/scratchpad-snapshot-20261116/.

*Not checked by this report:* the memguard config; whether the b35s20 contexts match the s20 contexts; NOVELTY20261115
and the Balko–Valtr text; probe 2 (upper) and the K9ARM scan, beyond what the probes themselves recorded.
