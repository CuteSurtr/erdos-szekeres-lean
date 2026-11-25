# STATUS20261121_1930: Linux session of 21 November 2026 from 19:15 KST (handoff, updated as it goes)

**Status (24 Nov 02:40): ES(8) ≤ 302 ESTABLISHED (ES302N20261124; the budget-69 tree passed both in-project checks; not reviewed independently, not in Lean). Verify-then-delete running (§6).** Earlier: **Status (23 Nov 00:50): STOPPED FOR THE NIGHT; four jobs keep running unattended (§6, "Night of 22-23 Nov").** Owner, about 21:55: no new agents, stop after formalization wave 5. ES(8) ≤ 303 established 22 Nov 06:21 ([ES303N20261120](../ES303N20261120/README.md); computer-assisted, unrefereed). Commits of this session: b01f0acd9, 708f7c917, 7c1562871 and 59becd99c (pushed), and the wave-5 commit that carries this page (owner, about 22:00: commit and push at wrap-up). Nothing was e-mailed.
- The Mac pushed its own handoff, `STATUS20261121`, on the unmerged branch `origin/es-mac-2026-11-21`. That name and the
  Mac's record names (ES8CHECK20261121, M57R36N20261121, M57R36E20261121, PREFIX20261121) are taken. This Linux page uses a
  time suffix.
- Previous Linux handoff: [STATUS20261120](../STATUS20261120/README.md) (stop of 20 Nov 23:52 and resume commands, §6).

## 1. Owner request (21 Nov ~19:15)

Check GitHub, push further on the ES lower and upper bounds and on Erdős problem #810, use agents freely, "fully utilize
this pc and keep researching until you find something useful". Caps unchanged: 28 of 32 threads, 24 GB for research
jobs (SKILL.md §1).

## 2. GitHub state (fetched 19:10, read-only)

- ES repository: new branch `origin/es-mac-2026-11-21`, 4 Mac commits on top of main 2d1cb6baa (1f084cc62, a4405765c,
  dedc94e62, ee7994318). Merging into main is an open owner decision; main is unchanged.
- #810 repository (`~/research/sat/erdos-810-research`): new remote branches `research/810-overnight-20261121` (last
  commit 7bbe261, 19:00 KST), `research/810-evening-20261120`, `main`, `lean-formalization`. The local working tree is
  on the two-week-old `research-2026-11-07` and is not used.

## 3. What runs (resumed 19:23–19:25 in the layout of STATUS20261120 §6)

| unit | job | note |
|---|---|---|
| `esr-memguard-1121b` + `esv-memguard-1121` | memory guards, 21,000 MB (bal 9500, dlt 7000, n66 17000, r36 8500, ag 3000; log `memguard-20261119.log`) + 3,000 MB (fv 3000) | started before every other unit; `-1121b` replaced `-1121` at about 20:10 to add the r36 and ag tracks |
| `esr-bal-zbs68` | budget-68 tree with the Z*-row → ES(8) ≤ 303 ([ES303N20261120](../ES303N20261120/README.md)) | CPUQuota 1600 %, `taskset -c 5-15,21-31`; resumed with todo 7,817 of 32,755 contexts |
| `esr-n66-drv15` + 4 `esr-n66-c15-*` | N66 level-15 cube campaign → N66 ≤ 54 | driver deadline moved from 23 Nov 12:00 to **24 Nov 08:00** (the stop lasted 19.5 h); the n66 memory track allows 4 cubes |
| `esr-vfy-drv15` | independent check of the level-15 leaves | |
| `esv-fv-drv` + 2 `esv-fv-c-*` | FV304, the Lean check of the 304 tree | resumes after the 379 finished modules |

At 19:27 the anonymous memory was 11.8 GB under the research guard and 1.1 GB under the FV guard, and the CPUs were
69 % busy at nice, with Tctl at 78.5 °C.

No finish time is quoted for b68. The remaining contexts are the tail of the context order, where the cost per context
rises. The block before the stop averaged about 2,800 s of wall time per 1,000 contexts, and its last partial block cost
91 CPU-s per context against about 60 before that (HEURISTIC). After the search come the assembly with `check_tree` and
`balcheck2`; at budget 67 these took 4 and 3.5 minutes.

## 4. Results of this session

| time | result | label | record |
|---|---|---|---|
| 19:55 | Rung N = 36 of the M(5;7) owner model, **case B** (`c36_tle22`): cake_lpr accepted the 13 Nov CaDiCaL 2.1.3 proof (heap 6,000 MB, 176 s; CNF `08b8ea9c…`, LRAT `a0d2cb92…` re-hashed) | **CERTIFIED** (modulo the written arguments of ETV7SAT §2) | [ETV7SAT20261113](../ETV7SAT20261113/README.md) §6.2 update |
| 22 Nov ~19:30 | **Lean verification, wave 4 and formalization wave 3** (each item has an independent review; standard
axioms).
- (1) FV304 closing audit passed: 13,199-module closure, one provider each. Finding: 4 chunk logs had profiler-garbled
  axiom lines, all re-printed standard. **ES(8) ≤ 304 is Lean-checked modulo N66Bound 55 and ResidualBound 118.**
  The combined `FV4A.forces_304_of_slices_rows_n66` (modulo N66Bound 55, 4 row blocks, 6 slices) compiles.
- (2) Residual slices in Lean: `RS.s33_18`, `RS.s34_18`, `RS.s35_18` (reviewed) and `RS.s34_19` (compiled, rc 0,
  standard; not yet reviewed). Remaining: s35_19 and s35_20.
- (3) The four Res118 row blocks are Lean-checked modulo per-row cake_lpr verdicts (E1–E6).
- (4) `N66G15.n66_bound_54_of_cubes : CubesUnsat105 → RowsValid R0_15 → N66Bound 54`.
- (5) The N66 encoder's byte identity was re-run with the frozen exe: all MATCH.
- (6) #810: χ_rainbow(G) = 6 for the 182-vertex graph, Lean-checked modulo the 4,404 verdicts (the 6-colouring half
  is unconditional).
- (7) AE33 radius 1 is Lean-checked modulo the 203 verdicts (review pending).
- (8) Rung-36 driver v3 (RQ1): review 8/8; ready to launch.
- (9) b69 checks prepared: v5n54, chain302, rows binding, pre-registration; review 6/6.
| as stated; no record label changes except 304's Lean status; unrefereed | `~/research/data/formalize-20261122/*`,
`bal186-20261119/b69prep`, `r36-linux-20261121/caseA/v3` |
| 22 Nov ~20:50 | **Formalization wave 3 finished, all reviewed** (record `FORMAL20261122`):
- Res118 row blocks: 5 of 5 confirmed; 2,025 of 2,025 rows bound by hash; E2 evidence copied into the record.
- **N66 rows (level 14): partial.** `RowGeo.n66_bound_55_of_cubes_rows : CubesUnsat132 → RowCertsUnsat → R0Parse →
  N66Bound 55`. So N66Bound 55 is Lean-checked modulo 132 cube verdicts, 629 row-CNF verdicts and **R0Parse**
  (`N66Enc.R0 = R1`, evidence COMPUTED by `#eval`, E4-class; the kernel cannot evaluate the `include_str` row list).
  Review: 11 confirmed, 2 not confirmed (the target without R0Parse; the T208 sub-list print not independently
  reproduced, about 3 GB). Always quote the label with R0Parse named.
- N66 ≤ 54 at level 15: 11 confirmed; RowsValid R0_15 and the 302 plug are not claimed.
- χ_rainbow = 6 (182 vertices) and AE33 radius 1: 5 of 5 confirmed each.
- s35_19 Lean check running unattended (`esr-fvr-drv`, 3 compiles; HEURISTIC end 23 Nov 05:00–08:30). s35_20
  feasibility: the 4,642-row catalog needs a 13-bit exporter (built and controlled); cost 360–440 CPU-h and
  246–297 GB with chunk sources, 140–169 GB without (HEURISTIC, from s35_19's calibration). | Lean-checked modulo
  the named hypotheses | `FORMAL20261122` |
| 22 Nov ~21:45 | **Wave 4 finished, all reviewed.** b69 check preparation 6 of 6; FV304 audit 5 of 5; P2 census 3 of 3: the reviewer re-ran shards 301, 246 and 223 with their own PRUNE checker and got identical counts and outputs; the one survivor (shard 301) complements to the notes' unique 15-vertex graph; wording fixes only. M(16) run 4 + 1 not confirmed (stale self-test documentation, known). Rung-36 RQ1 8 of 8; n66enc byte identity 8 of 8; small slices 5 of 5. **M(16) disk:** kept proofs grow about 13 GB/h (43.3 GB at 21:44; 17,308 cubes certified, about 2.5 MB each; 49,182 open). 12 of 209 hard subtrees closed so far, at 400–4,900 CPU-s each (HEURISTIC; the earliest closed are likely the easiest). The run pauses itself at 250 GB of kept proofs. Owner decision pending. | as stated | `e810-linux-20261121/{p2-census,m16-le72-run}` |
| 23 Nov 00:43 | **Formalization wave 5 finished, all reviewed** (record `FORMAL20261122`):
- **N66 ≤ 54 without R0Parse.** `N66R15.n66_bound_54 : CubesUnsat105R → RowCertsUnsat → N66Bound 54` (and `_55`). The
  level-15 rows are kernel-checked chunk constants, and the cube printer reads the same constants (105 of 105 trims
  byte-identical to the certified files). N66 ≤ 54 is Lean-checked modulo the 105 level-15 cube verdicts and the 629
  row-certificate verdicts (E1-E6). Review: 13 confirmed, 1 not confirmed (the co-import compile was not re-run; off the
  label's path); no fixes.
- **End theorems.** `Combined.es304`, `es303`, `es302` and `residual_bound_118` (part 1; review: 8 confirmed, 2 not
  confirmed: H-T69 has no evidence, and the s35_19 switch template is not compiled) and their level-15 instances `*_l15`
  (part 2; review: 8 confirmed, 2 not confirmed, the same two). **ES(8) ≤ 304 is Lean-checked modulo the 105 + 629 + 2,025 cake_lpr verdicts (E1-E6) and the
  slices s35_19 and s35_20** (EXACT TREE, not in Lean). 303 adds the budget-68 tree (EXACT TREE by two checks). 302 adds
  the budget-69 tree, which does not exist yet, so `es302_l15` is not a bound claim.
- **s35_20 launch gate passed (acceptance item 3 only through re-prints); not launched.** The largest context (320,422 leaves, 57 chunk modules) and its context
  theorem compile: 3 of 3,212 units. The new exporter writes the reference's bytes. Cost 383-417 CPU-h; disk 228-239 GB
  with the chunk sources kept or about 140 GB without (HEURISTIC). Review: 12 confirmed, 2 not confirmed (acceptance
  item 3 met only through re-prints; `FVR_JOBS=4` in LAUNCH_PLAN §5 contradicts its §6.5). 4 LAUNCH_PLAN fixes are due
  before launch.
| Lean-checked modulo the named hypotheses; no record label changes; unrefereed | `FORMAL20261122` |
| 22 Nov 16:45 | **N66 ≤ 54.** The L15 campaign ended at 13:07 with 105 certified leaves and a complete cover. vfy15 did
all four checks on all 105 (fresh cake_lpr, trim ⊆ cert, cert = F_c + units, rows). Own exact partition on the cube
literals and on the real unit literals (measure 1). L = 15 confirmed; F_c `2f78368f…` | CERTIFIED + PROVED (written model, L =
15); unrefereed | [N66N20261113/cubes20261120](../N66N20261113/cubes20261120/README.md) §8 |
| 22 Nov 12:19 | **FV304 complete:** `E304Z.Final.excludes_67 : ExcludesHoleBudgetZ 67` and `forces_304_of_n66_res`,
standard axioms. ES(8) ≤ 304 is Lean-checked modulo N66Bound 55 and ResidualBound 118 (with Res118: modulo N66Bound 55,
six slices and four row blocks) | Lean-checked modulo the named hypotheses; closing pin and import audit running (wave 4) |
`/home/jay/research/data/fv304-20261120` |
| 22 Nov 06:55 | **182-vertex graph of the #810 notes: no rainbow-C4 5-colouring, so χ_rainbow = 6.** All 4,404 pieces of
the cube cover have an independent cake_lpr acceptance (1,623 from wave 1's verifier, 2,781 re-run by wave 3 on its own
regenerated CNFs; the rebuild verifier re-ran all 2,781 again). The cover was checked by own code; the 6-colouring is
exact | CERTIFIED (pieces) + EXACT (cover) + PROVED (reduction, wave 1); rebuild and soundness verifiers CONFIRMED;
unrefereed | `~/research/data/e810-linux-20261121/v182-recheck` (README, `verify/`) |
| 22 Nov ~07:30 | **Formalization, waves 1-2** (each reviewed for statement fidelity; standard axioms). (1) Composition
audit: the 30x files rebuilt in one olean dir, closure check, 31 theorems standard. (2) `Res118.residual_bound_118_of_slices`:
ResidualBound 118 as a Lean theorem modulo N66Bound 55, six slice exclusions and four row blocks; `forces_304_of_slices`.
(3) `N66Geo.n66_bound_55_of_cubes : CubesUnsat132 → RowsValid R0 → N66Bound 55`. (4) `EncB.Geo7.sevenfold_es8_of_text`:
the 7-fold (64) case modulo one cake_lpr verdict, the level of the sixfold case | Lean-checked modulo the named hypotheses;
not refereed; review fixes listed in each VERIFY file | `~/research/data/formalize-20261122/{comp-audit,res118,n66enc,sevenfold}` |
| 22 Nov ~07:30 | **#810 M(16) work (wave 3).**
- P1, F(14,16) ≤ 57: re-run by own exact checkers inside the notes' generator, nauty 2.8.9 geng, so not a fully
  independent route. COMPUTED.
- P2, the unique 65-edge support: not re-established; its census stopped at 26 of 512 shards.
- M(13) census: 11,461 graphs, equal to the notes' full census. M(14): 52 supports.
- M(16) ≤ 72: forced structure PROVED (conditional on P1/P2) and encoder sound; base controls CERTIFIED, including a
  march_cu cube-and-conquer refutation of 10/31; the 16/73 run itself has not been made
| COMPUTED / PROVED (conditional) / CERTIFIED controls; verifiers confirmed | `~/research/data/e810-linux-20261121/{m16-premises,m16-le72}` |
| 22 Nov 06:21 | **ES(8) ≤ 303.** Both tree checks of `ExcludesHoleBudgetZZsF 68` passed with every pre-registered value:
check_tree via v5 at 06:06 and balcheck2 at 06:21. Files 32,765; nodes 246,300,833; leaves 123,166,799; minimum margin
1; cover complete. The rows binding is asserted; `composition_303_zzsf` has standard axioms on Linux | EXACT TREE ×2 + Lean
composition; N66 ≤ 55 CERTIFIED + written model; ResidualBound 118 a written chain; unrefereed; not found in the 21 Nov
search | [ES303N20261120](../ES303N20261120/README.md) §5 |
| 22 Nov 01:08 | **Budget-68 finder complete**: all 32,755 contexts closed (rc 0). The assembly + check_tree step was stopped cleanly by the memory guard twice (01:09:41 and 01:12:07; one context alone needs > 8 GB in v4). It was re-run from 01:26 with the memory-lean `balz_assemble_v5.py` (controls 27/27 equal, 7/7 negative caught); balcheck2 follows via `chain303.sh` | – (no claim yet) | [ES303N20261120](../ES303N20261120/README.md) §5 |
| 22 Nov 00:40 | **sat_g(6) ≤ 11, sat_g(8) ≤ 26, sat_g(9) ≤ 39** (were 12, 27, 40): explicit saturated sets, five exact implementations agree, including the verifier's own code; cell counts equal the Euler count | **EXACT** (stated coordinates) | [SATG20261118](../SATG20261118/README.md) SAT4 addendum |
| 22 Nov 00:45 | Radius 1 around AE33 is empty at the order-type level: all 203 two-point CNFs UNSAT, a fresh cake_lpr gives one verdict line each, all 223,165,944 clauses checked by own code | **CERTIFIED + PROVED soundness** (unrefereed; support evidence for ES(7) = 33 only) | [LOWERBOUND_RUN_1118](../ROADMAP20261115/LOWERBOUND_RUN_1118.md), claim `lb-l18-e72-ae33` |

#810 results of wave 1 (kept in the work folders under `~/research/data/e810-linux-20261121/`, since #810 has its own
repository; nothing was written there):

- **M(16) ≤ 73, extension step** (B2): all 210 extensions with 74 edges and all 6,435 with 73 edges are UNSAT under
  an own encoder. This is CERTIFIED (CaDiCaL 2.1.3 plus cake_lpr; the verifier stored cake stdout for 6,645/6,645).
  6,615 of them also have a 17-edge conflict clique, which is EXACT. M(16) ≤ 73 itself stays **conditional** on the
  notes' two one-run censuses, F(14,16) ≤ 57 and the uniqueness of the 65-edge optimum.
- **Ten-point and Hamming CNFs** (B1): 125 + 1 CNFs CERTIFIED, at the CNF level only. The encodings and the
  ten-point reduction were not checked independently.
- **t = 34 copies** (A1): for all 7 open shapes, χ_f(C_B) = 901/3 exactly. Hence the price method cannot exclude
  t = 34, and the single-star test passes (EXACT). χ(C_B) = 301 for six shapes; for {0,2,8} it is between 301 and
  306. Whether t_max is 33 or 34 stays open.
- **182-vertex graph** (A2):
  - the proper version with 7 colours is CERTIFIED UNSAT;
  - the fractional value is χ_f = 5 (EXACT);
  - rainbow with 5 colours is **undecided**: 78 of 120 Y1-cubes are CERTIFIED, 1,624 proofs, re-run by the verifier;
  - the reduction to cubes is PROVED.
- **Proof attempts** (F: 1/4 − δ, G: 1/18 − δ): no δ > 0 was found. The lemmas are in the work folders.
  - Several lemmas are conditional on Lean theorems that were not rebuilt here (F Thm 3; G L2, Cor 7, L3(ii), L3(iv)).
  - G L3(iii) carries the graph-limit transfer GAP-S.
  - F Prop. 5 is true only with "at least one edge": the edgeless graph refutes the literal statement.

Case A of rung 36 is still open: 34 cubes, 65/256 of the case-A cube space, according to the Mac's records as of
18:59 (`es_mac_digest.md` §1). M(5;7) ≤ 35 is not established.

## 5. Agents (read-only digests, 19:30)

Outputs in `~/research/data/agents-20261121/`: `es_mac_digest.md` (Mac ES branch: rung-36 open set, ES8CHECK findings),
`e810_digest.md` (#810 overnight branch: frontier and next steps), `lower_digest.md` (what "lower bound" covers here and
what can improve). Agent summaries are not evidence.

### Wave 1 (workflow `research-wave1-1121`, launched about 20:15)

Seven workers. Each positive claim is checked by an independent rebuild (own code) and a soundness review.

| worker | slot (1 thread each) | task | work dir |
|---|---|---|---|
| A | `esr-ag-a810-*`, 700 MB | #810: t = 34 copy count (local colouring of at most 304 classes, or integer prices); 5 colours on the 182-vertex graph | `~/research/data/e810-linux-20261121/a-t34-sat182` |
| B | `esr-ag-b810-*`, 700 MB | #810: re-certify the ten-point and Hamming CNFs with cake_lpr; own-encoder recheck of the 210 + 6,435 extensions behind M(16) ≤ 73 | `…/b-recert-ext16` |
| C | `esr-ag-ae33-*`, 1,000 MB | ES lower side: AE33 radius 1 (203 pairs): hashes, cake_lpr re-run, own clause check, draft record text | `~/research/data/lower-20261121/ae33` |
| D | `esr-ag-satg-*`, 600 MB | sat_g descents (K = 8 below 27, K = 6 below 12, K = 9 below 40) | `…/satg` |
| E | none | prepare rung-36 case A on Linux: all 84 leaves with 2.1.3, no solving | `~/research/data/r36-linux-20261121/caseA` |
| F, G | none | proof attempts: M(n) ≤ (1/4 − δ)n², g(n;7,4) ≤ (1/18 − δ)n² | `…/f-quarter`, `…/g-eighteenth` |

- The agent pool has 4 threads and 3,000 MB (memguard track `ag`, inside the research total of 21,000 MB).
- `agents-20261121/yield_guard.sh` creates `agents-20261121/YIELD` at a Tctl 5-minute average of 87 °C or above, or
  at a research memory total above 19,000 MB. Agents then stop their units.
- Agents write only under `~/research/data/`. The main session applies record edits after it has checked the verdict
  lines and hashes itself.

**Wave 1 finished at 00:32 (22 Nov).** 19 agents ran with no errors. Every claim was confirmed by both verifiers,
except F's Prop. 5, which holds only in the amended form above.
- The memory guard stopped one agent unit cleanly (`esr-ag-a810-combo1`, 703 MB of 700 MB); there was no kernel OOM
  kill.
- E (rung-36 case A preparation) had no verifier stage. Its ported driver (`drive2.py`, which includes a race fix)
  must be reviewed before case A starts.
- Proofs kept: about 12 GB of zstd LRATs under `a-t34-sat182/a2/` and about 330 MB under `b-recert-ext16/`.

### Wave 2 (workflow `research-wave2-1122`, 00:48 to 02:57; stopped by the main session before the 03:00 stop)

Four workers, each meant to be followed by an independent rebuild and a soundness review. Only the driver review
finished. None of the workers' claims below reached the verifier stage: they are agent outputs, not evidence.

- **Rung-36 case-A driver review** (two independent reviewers, both finished; `~/research/data/r36-linux-20261121/caseA/review/REVIEW_drive2_lens1.md`, `…_lens2.md`).
  - Neither found an unsound path for a single driver instance.
  - Lens 2's verdict: **not ready to launch as is**. Before launch: RF1 (a lock against a second driver on the same
    directory), RF2 (atomic cube write), RF3a (record the solver identity), RF4 (an esr-total check). Before the
    CERTIFIED label: RF3b, a solver check in `cover.py --final`. RF3b can be added after the run because the per-cube
    logs are kept.
  - Lens 1: `cover.py --final` never checks "CaDiCaL 2.1.3, exit 20", and the README §8.4 recovery edits statuses by hand.
- **182-vertex graph, rainbow with 5 colours** (A2). The agent's `a2/campaign_status.py` (run by the main session at
  03:05) prints:
  - 118 of 120 Y1-cubes refuted: 84 directly, 34 via 120 sub-cubes each;
  - cube 118 is partly done (115 of 120 sub-cubes); cube 119 is open.
  - Undecided. Wave 1's verifier re-ran the proofs of the first 78 cubes only, so cubes 78–117 still need an
    independent re-check.
- **M(16) ≥ 72 and factor checks** (`~/research/data/e810-linux-20261121/m16-72/README.md`; the agent marked it "DONE" at 02:45).
  - The agent reports exact factor-level checks of the notes' 32,768-vertex and 226,981-vertex constructions.
  - No 16-vertex 72-edge witness among 1,816,353 candidates (HEURISTIC negative).
  - "Every 72-edge example has minimum degree ≥ 8": COMPUTED, conditional on the notes' two one-run censuses.
  - Not verified independently.
- **sat_g descents** (`~/research/data/lower-20261121/satg2/README.md`): no new bound (HEURISTIC finder runs only).
  - K = 8: stuck at 2 failing cells at 25 points.
  - K = 10: 51 points with 2 failing cells (`seeds/k10u_best_n51.txt`).
  - Exhaustive one-point relocation repairs neither (COMPUTED by the finder).

## 6. Resume

### 25 Nov evening (to ~21:15): FV302 accepted, s35_20 Root aborted, C4/C5/D2 re-certified

- **FV302 ACCEPTED ~20:40** (pre-registered items 1-4; formalize-20261122/fv302-audit, tools/fv2a.py; mirror
  FORMAL20261122/fv302): Root 17:15-18:13, Final 18:13-19:22, `E302ZZ.Final.excludes_69 : ExcludesHoleBudgetZZsN 16 69`
  and `forces_302_of_n54_res : N66Bound 54 → ResidualBound 118 → ForcesConvexNGon 302 8`, standard axioms. **The
  budget-69 tree is Lean-checked.** Checked by the session's own tool only (no independent review); deviations in
  fv302/PLAN.md (pilot modules without run.tsv rows, the fv2a symlink bug fixed after a first NOT ACCEPTED).
- **s35_20 Root join failed twice** (lean_rc 134, "Stack overflow detected"; 21,495 imports and 23,485 joins in one
  file; memory.high throttling; tries exhausted, driver ended). Next: sub-roots as a pure partition (res-slices README,
  deviation of 25 Nov). PART3 gates 2-3 wait for it; PART3's memory rule was corrected (dated) before any compile.
- **Re-certified on Linux (RECERT20261125):** C5 `c4_n32L_cuts`, C4 `c5_n35L`, D2 `B_m7K8t10` (CaDiCaL 2.1.3, cake_lpr
  c14ff498, proofs kept); RESULTS rows C4, C5, D2 raised back to CERTIFIED; D2 Lean-checked modulo that verdict and E1,
  E3-E6 (sevenfold record updated).
- **E3 on every text:** cake_lpr's parse = the Lean printers' texts for all 2,759 verdict texts of the end theorem
  (`~/research/data/e3-20261125/e3all.json`).
- **Deletion now follows fv2a, not part 3** (advisor): FV302's 32,953 chunk sources (78.06 GiB; receipts
  `FORMAL20261122/fv302/receipts/fv302_chunk_sources_20261125.tsv`) go by `verify-20261124/delete_proofs.py` after this
  push and a clean dry run; `export/ctx` and the join sources stay.
- **C2 upload from the Mac** (owner 21:00): private archive branch `research/c2-certificates` + release
  `c2-p8-1-9-2026-11-25`: the half-turn (central34) proof P8_1-9 (2,398,761,295 B, sha256 `ef13b40d…` = the Mac
  inventory) and replay tools; being downloaded and checked here with cake_lpr.
- **Paper:** `~/research/data/paper302-20261125/paper/main.pdf`, 74 pages, compiles; 66 TODOs. Owner: no more agents
  after the paper workflow; all further work solo.

### 25 Nov from 15:15 (owner: "keep cleaning ... 1.8 tb"; "formalize everything first"; scope "302 + SAT results' encoders"; paper written here; adversarial checks of theorems and citations; "upload them to my github repo")

- **Disk:** 1,061 GB free. `df -h` shows 1.8T as the disk size, so 1.8 TB free is out of reach. Tiers: about
  1,235 GB once the generated chunk sources of FV302 and s35_20 go, about 1,520 GB with the oleans as well, about
  1,770 GB with the evidence moved off this disk. Archive target: the owner's Google Drive (5 TB, rclone not
  installed). Waits until the formalization program is done; no evidence-tier deletion before then.
- **Tonight (critical path):** FV302 Final → `formalize-20261122/fv302-audit` (fv2a.py: PLAN items 1-4, token scan,
  olean order, deviations; compile `src/Audit302.lean` without -o first) → s35_20 by the res-slices-fv §9 recipe,
  tag 3520, Lean leaf sum **119,054,033** → `combined/PART3.md` (pre-registered, pushed 7311d7e66; leaf sum corrected
  f2c925d1f): links3 from the module list of `logs/RS_Final3520.log`, compile `src/Combined/ES302Final.lean`,
  control `controls/Bad302.lean` must fail, audit3 → records → push. Only then delete `export/src/E302ZZ/C*.lean`
  (regen test passed: `cleanup-20261125/fv302-regen`, 83 contexts / 137 modules byte-identical; the join sources and
  the two new Lean modules are mirrored in `FORMAL20261122/fv302/`).
- **fv2a dry run 25 Nov ~17:00:** item2 ok (32,618 manifests, 32,953 chunk modules, 43,967,444 leaves, min margin 1,
  one exporter = pin, all 84 GB of chunk sources = manifest sha256), scan ok (33 join sources + 2 modules), order ok
  (30,921 oleans); item3: 42 profiler-split axiom lines confirmed standard by the log audit; open only the logs of
  running compiles; item1/item4 wait for Final.
- **Re-solves (pre-registered `~/research/data/resolve-sym-20261125/PLAN.md`):** C4 `c5_n35L` (90dea1cf…), C5
  `c4_n32L_cuts` (2aa18f1e…) and D2 `B_m7K8t10` (b4d29017…) regenerated from the repository generators, all five
  hashes MATCH (`cnf/regen.log`). Next: certify_cnf.sh (CaDiCaL 2.1.3 + cake_lpr) one at a time after s35_20's Root
  join, cake heap per formula (C5: 8000 with stack 4000), read every cake output before recording a rejection.
- **Checks made today (read-only agents; reports in `~/research/data/audit-20261125/`):**
  - end-theorem statement review (2 lenses): `ForcesConvexNGon 302 8` is ES(8) ≤ 302 exactly; no blocker.
  - adversarial theorem audit (8 areas + 10 skeptics, `AUDIT.md`): 0 blockers, 11 major (all confirmed, all
    downgraded to minor: labels and stale records, no false theorem), 43 minor, 25 info. Fixes pending, one commit,
    lowering labels only: N66 ≤ 54 VERIFY wording (state the Lean theorem, E1 105/105, two recorded acceptances and
    that no cube proof remains), ES302N check A text, ES303N stale label, D1/D11 "recorded verdicts", D2/C4/C5 label
    until the Linux re-solves, C2, D10 (δ = reduced offset; ROT456 model), D11 (second float step; window 0..11),
    STATUS P2 wording.
  - citation audit (208 references, `CITATIONS.md`): 172 verified, **0 fabricated**, 21 content and 13 metadata
    mismatches (25 touch .tex manuscripts), 2 unclear (keep out of the paper); references.bib `Schroeder2026Zenodo`
    needs its real title, given name, DOI and "Zenodo preprint, version 1".
  - SAT-encoder map: D2 already Lean-checked modulo one verdict (FORMAL20261122/sevenfold); C4 → C5 next (symcnf
    port); D11 first only the exact re-check of its 38,250 float-accepted clauses; C3, C2 and D11 encoders take
    weeks (C2's verdicts cannot be re-checked): ask the owner whether the archive waits for them.
  - paper dossiers A-E: `~/research/data/paper302-20261125/dossiers/`; drafting waits for the label fixes.
- **Token budget:** about 16 M subagent tokens today; no new workflows until part 3 is accepted (advisor).

### 25 Nov from 01:00 (owner: "delete unnecessary files please?"; "you can deploy more agents ... 10% of weekly quota")

- Deleted after pushed receipts, an advisor check and the guarded script: the b67 finder contexts (8.76 GB; FV304
  accepted as the independent check of the 304 tree; b67/files verified 8,192/8,192 first), all 251 K9 proofs
  (75.83 GB; re-checked 24 Nov), the b69 review sandboxes (2.01 GB) and 2,114 Mac-bundle duplicates (1.15 GB).
  Records: ES304N, SATOPEN, LBK9OCT, ES302N §10, ES8B64MAC.
- Two read-only mapping agents (data/cleanup-20261125/{formalize,evidence}) found nothing else safely deletable. Their
  N66 trace items were dropped: they included a certified level-15 leaf folder and the state files of 14 level-14 leaves.
  Not done: lossless compression (27.5 GB, HEURISTIC; it would rename CNFs that Lean work and scripts bind by path).
- s35_20: FVR_JOINMEM 18000 and guard esr-memguard-1125a (fvr 19000) for its Root join; units 1793/2080 re-export
  identically. FV302: export complete (acceptance item 2 met), 13 of 32 sub-roots compiled.
- Owner (25 Nov ~02:10): "yeah keep cleaning and formalize and verify everything and delete what has already been
  formalized". Deleted: the FV304 chunk sources (20.62 GB; regenerate byte-identically from the kept 304 tree, 44/44
  sampled incl. all 12 multi-module contexts; compiled proof kept) and the b35s20 test packets (15.35 GB; bb, bb-s1,
  bb-hc1* kept). Rule adopted: for a finished, accepted Lean check keep the compiled proof (oleans) and the compact
  tree it was exported from, delete the generated chunk sources after a per-exporter regeneration test. FV302 and
  s35_20 sources (about 335 GB) follow only after their acceptance; nothing in res-slices-fv until its driver exits.

### FV302 and the s35_19 switch (24 Nov from 02:56; owner: "then fully formalize and verify it, even if it takes multiples of days? you have my permission. go"; no additional agents)

- **s35_19 switch done** (formalize-20261122/combined, recipe §2.9 steps 1-6): `Combined.Switch3519L15` compiled
  03:22 (`es302_l15_s3519`: 8 hypotheses, none N66Bound), import audit 03:28 (`problems []`), REMAINS.md rewritten and
  `data/manifest3.sha256` 05:10. The combined 302 theorem now assumes only the cake_lpr verdict props, s35_20 and the tree.
- **FV302 runs** (`~/research/data/fv302-20261124`, PLAN.md = log + pre-registration): unit `esr-fv2-drv`
  (tools/drive302.py: export → chunks → 32 sub-roots → Root → Final; FV2_JOBS 8, MEM 11000, TMAX 86, YIELD honoured;
  restart = the command in PLAN.md, it adopts running units). New Lean: `CompactChecker.FcatZZs16`, `BridgeZZs16`
  (`zzsn16_of_root`). Gates passed: pilot 13 modules, corrupted-certificate and swapped-join controls rejected by Lean,
  multi-level join, Root and the exact Final template over stubs. HEURISTIC: 230-305 CPU-h, about 2 days.
- **s35_20** sets the finish date: 119 M leaves at about 0.010 s/leaf, about 340 CPU-h (3.5 days at 4 jobs); raise
  FVR_JOBS when `esr-vfy-all` ends. Its 9 axiom ALERTs are profiler text inside the axiom lines (LAUNCH_NOTE, 04:55;
  `fv302-20261124/tools/axiom_audit.py`); unit 161 re-exports byte-identically.
- **c6upper proofs deleted 05:06** (96, 43.34 GB) after a fresh cake_lpr re-check 96/96 and pushed receipts (868733e95,
  C6UPPER §8); CNFs kept. The advisor check of the protocol above was made only afterwards (no objection).
- **Guards:** `esr-memguard-1124d` (fv2=12500, total 36000); `esr-ygd-guard` restarted 05:09 with a 10-day horizon (the
  old one would have exited 26 Nov 01:11); `esr-pin-guard` (agents-20261121/pin_guard.sh, to about 18:14) keeps the
  M(16) cubes on cores 0-3 and moves unpinned bulk jobs to cores 4-15.
- **Keep:** `bal186-20261119/b69prep` (ES302N §8 resume command and the control trees) and the 302 certificate
  `b69zs54/files` (FV302's input).
- **M(16) run ended 17:29:54 by RuntimeMaxSec, NOT closed** (open cubes A 10,646, B1 23,995, B2 13,539; certified
  unsat cubes 68,124 / 52,701 / 82,262; no SAT, no rejection): M(16) <= 72 undecided, the run resumable. Re-checker
  stopped; README_RECHECK 9.3 final pass + audit from 17:40 (unit esr-rck-final). Its cores went to s35_20
  (FVR_JOBS 13 from 17:31); the pin guard was stopped. Relaunching M(16) is the owner's call (it competes with the
  Lean campaigns for the heat budget).
  9.3 result 17:52: pass_rc 0 (745 last proofs re-checked OK and deleted), audit_rc 2 (open work), problems [];
  audited ledger sha256 `32657d28…` = the last ledger copy. Audit counts: A 68,126 leaves / 10,644 open, B1 52,702 /
  23,994, B2 82,262 / 13,539, no cover missing. No 9.4 record (needs audit_rc 0).
- **Owner 24 Nov ~17:55: "keep cleaning, commit and push, delete redundant or useless files, map roadmaps, and consider
  starting m16 if its necessary".** Record edits pushed (9acd1e9c3). Roadmap map: ROADMAP20261115/CLEANUP_MAP_20261124.md.
  52 roadmap proofs re-checked 52/52, receipts pushed (6e39be770), advisor, deleted 19:18-19:25 (29.97 GB; 6709ee1b8).
  M(16) not restarted (own projection >= 5.7e4 CPU-h). Open for the owner: the b67 finder contexts (8.8 GB) need an
  explicit "FV304 is the independent check of the 304 tree" (ES304N §4 keeps them until one); FV304 chunk sources
  stay (owner, 23 Nov).
- **Re-check finished 06:11** (`esr-vfy-all`, fresh cake_lpr each, 0 alerts): K9 satopen 179/179, c6upper 96/96, K9
  lower-bound cubes 68/68, the 4 G3 (S11) cube proofs 4/4 (their first cake_lpr acceptance: COMPUTED → CERTIFIED per
  cube; G3 is a stopped family implied by Theorem 2 of LBK9OCT, so no claim changes). K9 proofs are kept (K9 is not
  formalized); receipts pushed 8afcc9efd (SATOPEN, LBK9OCT). s35_20: 6 jobs from 06:13, 10 from 08:48 (FVR_MEM 8000).

### Verify, push, then delete (24 Nov from 01:00; owner: "verify every one of these git push and commit, then delete"; "you can fully utilize this pc to verify them"; no additional agents)

- **Protocol per set:** an independent check (or the record of one), then a receipts file in git (per proof: file hash,
  decompressed proof hash, CNF hash, the campaign's exact cake_lpr line, the independent re-check line), pushed, then an
  advisor check, then `verify-20261124/delete_proofs.py` (re-hashes every file against the pushed receipts just before
  deleting; refuses if a Lean project file, a FORMAL "original in" line or a running unit names a file). Manifest:
  `~/research/data/verify-20261124/manifest_deletions.txt`. The keep-set override is recorded there and in memory.
- **Batch 1 done (01:50-02:00): 128.3 GB.** The 237 N66 cube proofs (receipts `N66N20261113/receipts/`, 237 of 237:
  decompressed hash = cert.json, plus U1/VB re-checks for level 14 per VERIFY_N66LE55_FINAL.md and vfy15's full hash for
  level 15) and the 4,405 proofs of the 182-vertex campaign (receipts and the campaign/verifier records in
  `FORMAL20261122/evidence/`; 4,405 of 4,405 matched to the re-check that accepted them). Kept: every trim.cnf,
  cert.json and cake output, all 4,617 182-vertex CNFs. Pushed: 8432cb070, e42dee1bb, 79c9eaa7a.
- **ES(8) <= 302 established (01:43; record ES302N20261124, pushed fb2c03376).** The budget-69 tree passed both
  in-project checks with every pre-registered criterion met (ACCEPT302). Caveats: no independent review yet, tree not
  in Lean, N66 <= 54 rests on 105 cube verdicts accepted twice (proofs deleted today after receipts), no new
  literature search. 303 is superseded.
- **Batch 2 done (02:50): about 213 GB.** The 303 tree `zrow/b68zs` (178.5 GB; check logs and a certificate digest
  are in ES303N data/accept303) and the 32,334 raw b69 context files (34.2 GB). Kept: the 302 certificate
  (`b69zs54/files`, 32,618 files, digest in ES302N; `occ/master.json`, `contexts.json`). Loss, stated in the manifest:
  if 302 were withdrawn on review, the bound falls back to 304 and 303 would need a finder re-run. Free disk: 1,257.6 GB.
- **Running:**
  - `esr-vfy-all`: own fresh cake_lpr re-check (`verify-20261124/recheck_set.py`; controls 5 of 5) of the K9 proofs
    (satopen 179, lb-k9oct 68, the 4 G3 proofs: their first cake_lpr run would change their label from COMPUTED) and the
    96 c6upper proofs; deletion only after receipts are pushed; c6upper keeps its CNFs (ENCBLEAN reads them);
  - **s35_20 Lean campaign** (owner, 24 Nov about 01:25: "Run the Lean campaign"; supersedes "Not now"; chunk sources
    kept): `esr-fvr-drv` with drive_v3, FVR_JOBS=4 (exporter + 3 compiles, then 4), exporter from 01:38; launch note
    `formalize-20261122/s3520-gate/LAUNCH_NOTE_20261124.md`. Its tree (es308 runs/b35s20, inputs/b35s20-v169),
    res-slices-fv and s3520-gate are off every deletion list until its finish recipe is accepted.
- **Heat:** with about 14 threads busy (the b69 assembly is the hot part) Tctl's 5-minute mean reached 87 C at 01:22 and
  the yield guard (now its own unit `esr-ygd-guard`) paused M(16) and the s35_20 start until it cooled; it cleared before
  01:38. Heat, not the thread cap, sets the load. Guard: `esr-memguard-1124b` (vfy=20000, fvr=16000).

### Cleanup and the M(16) re-check (23 Nov 00:50-04:30; stopped for the day after them)

- **Owner, 23 Nov:** "delete that is already verified or not needed for our future" (00:50); "can we start to formalize
  everything clean up whatever is left so that we can use our space effectively" (00:58); answers at about 01:05:
  s35_20 **not now**; **keep** Lean chunk sources (so FV304's export C44 stays too); b69 checks **wait** for the owner's
  OK; M(16) kept proofs: **re-check, then delete**. Later: "do not add additional agents"; "if these two finishes we
  call it a day". The open questions 1-4 of the next subsection are answered by this.
- **Audit** (read-only workflow `cleanup-formalize-audit-1123`, 22 agents, two skeptics per candidate set, nothing
  deleted by agents): `~/research/data/cleanup-20261123/plan/PLAN.md`, `plan.json`, `owner_question.md`, and the
  formalize-to-free map `formalize-map/FORMALIZE_TO_FREE.md`.
- **Deleted (set A, 04:05, advisor-checked; manifest `~/research/data/cleanup-20261123/manifest.txt`):** C42 (11
  `cert.cnf` of SIGTERM-killed N66 CEGAR iterations, no verdict), C43a (2 temp dirs), NO-A2 (1 temp CNF): 14 paths,
  7.48 GB. The certified twin `p2/b13g/it1/cert.cnf` and the F_c `p2/b14h2/it1/cert.cnf` stay; the ledger's 1,302
  must-keep paths: 0 missing.
- **Set B, owner answer about 04:35 ("can they be deleted?"; ticked: small safe groups, duplicates, Delta-3 traces,
  stopped searches; compress the N66 cube CNFs and the CNFs beside proofs).** Executed 16:19 by
  `cleanup-20261123/exec-b/delete_B.py` (every duplicate re-checked byte for byte against its surviving copy just before
  deletion; no protected path inside a deleted folder; no process using a path; advisor-checked): **4,783 paths, 81.07 GB
  freed** (df 718.45 -> 799.52 GB). Sets: C18a, C15a, NO-B8, C42b, C32 (the trace only), C33, two crash reports, C23a,
  N66-B2, C24, NB03, C29, C30, NO-B9, NB01 (b68z), NO-B16 (10 unanswered K9 bases), C37 (budget 65 abandoned), C40.
  Small logs and models copied aside to `cleanup-20261123/kept/` first. Record notes (local, uncommitted): DELTA3N,
  VERIFY309N, ES309N, ES306N, LBK9OCT, N66N cubes20261115/VERIFY_N66CUBES.md. Kept on purpose: N66-B5/B6 (inside the N66
  keep folders), NO-B11 (desktop indexer: a desktop setting), the K9 G3 family (owner kept it on 18 Nov), NB02 (after
  the b69 checks), C35 and C27 (record-cited proofs and replay masters inside), NO-B5 (Mac bundle) and NO-B10
  (installer) (not named in the question), and the unpicked groups (FV304 chunk sources per "keep sources", b67 finder
  contexts, superseded FASTBB/K9 trees, after-commit items, #810 B2 proofs, Mathlib cache). After: must-keep 1,302: 0
  missing.
- **Compression (owner-approved):** `exec-b/compress_B.py` packs the 131 N66 level-14 cube `p2/c14/<id>/it1/cert.cnf` (now
  `cert.cnf.zst`; decompressed bytes checked against `cert.json` full_cnf_sha256 before each original goes) and 158 CNFs
  beside verified proofs (rot45 imp4/imp5, six10 recert_cake, lb-k9oct cnf; checked against their own pre-compression
  hash). Ledger `exec-b/compress_ledger.jsonl`. Readers that open these CNFs by name (the U1/VB/VN step-3 re-runs, the
  N66 FULL control, the rot45/six10/K9 recert scripts) need `zstd -dc` first.
  Done 16:25: 289 of 289 packed (131 + 60 + 96 + 2), 0 ALERT, 0 SKIP, **87.21 GB saved**; free disk 886.6 GB.
- **Finished while the session was paused (about 05:20-16:15):**
  - **s35_19 Lean check** (driver end 05:00:55; 1,411 modules, root, final, five-slice specialisation). **Accepted by
    the res-slices-fv §9 finish recipe at 16:30:** standard axioms for `RS.s35_19` and `RS.residual_bound_118_fv`, audit
    7,763,206 leaves / 307 units / 1,411 modules, 42 profiler-split axiom lines re-printed (n_problems 0), snapshot in
    `res-slices-fv/data/spec-snapshots/`. Not yet: its independent review, and `combined/src/Combined/Switch3519L15.lean`
    (about 7 min) that would drop H-S3519 from `Combined.es304_l15`. Remaining slice in Lean: s35_20 (not launched).
  - **P2 census** (09:22): 512 of 512 shards, exactly 1 survivor (shard 301), 0 mismatches against the notes' per-shard
    calls, rejects, survivors and output sha256 (COMPUTED; own checker, but nauty geng with the notes' exact arguments
    and 512-way split). So the P2 premise of M(16) <= 73 is re-run with an own checker inside the notes' generator and
    split, conditional on P1 (-D6); the census README's post-run `tools/verify_census.sh` was never run and the
    second-party review covers the first 29-32 shards only (corrected 25 Nov, adversarial audit; earlier wording
    'independent run' overstated it). P1 (F(14,16) <= 57) remains a COMPUTED re-run inside the notes' generator.
  - **M(16)** at 16:19: 95,162 cubes certified (A 36,839, B1 21,913, B2 36,410), 0 SAT, 0 alerts, not paused;
    written-bytes sum 416.6 GB of the 1,200 budget; the re-checker has re-checked and deleted 81,858 proofs, 0 alerts.
- **M(16) re-check and delete (owner-approved):** unit `esr-rck-m16` (since 04:11; `--delete --follow --jobs 1`, 1
  thread, MemoryMax 2600M) re-checks each kept proof with its own code (CNF rebuilt from the base CNF and split files
  and matched to the recorded hash; LRAT matched to its recorded hash; a fresh cake_lpr; exact line), writes the
  ledger `e810-linux-20261121/m16-recheck/ledger.jsonl`, and only then unlinks the `.lrat.zst` (the run's `.cake.out`
  stays). Hourly copy: timer `esr-rck-m16-copy` into `e810-linux-20261121/m16-ledger-copy`. **Both are keep-set**: they
  are the only licence for each deleted proof. Label: a second cake_lpr run by separate code on the same machine, not an
  external referee; after deletion no third party can re-run cake_lpr on those proofs without re-solving. Tool review:
  85/85 controls, two reviewers, one fix round confirmed (`m16-recheck/review/`). Final certification:
  `m16-recheck/README_RECHECK.md` §9.3 (`audit_rck.py --ledger`, exit 0 only).
- **First checks (04:12-04:18):** 461 proofs re-checked and deleted, 0 alerts, 0 torn-tail warnings; sampled proofs gone
  with their `.cake.out` kept; `audit_rck.py --ledger` on a live snapshot (deleter paused): exit 2 (open work), 0
  problems, rechecked_deleted 461 = DELETED lines, 3/3 sample re-checks accepted (`m16-recheck/snap-live1/`).
- **M(16) driver restarted 04:16** with `--proof-budget-gb 1200` (copy `m16-recheck/restart_with_preflight_b1200.sh`,
  diff = that number only), original end 24 Nov 17:29:54 kept. Gate: live audit clean, YIELD absent, Tctl 5-minute mean
  80.0 C (< 83 C). Preflight T1 closed (0 problems, 2/2 re-checks); resumed with 48,719 tasks queued, not paused, no
  alerts, counts at or above the earlier ones. The written-bytes sum was 146 GB at 04:16, rising about 19 GB/h over the
  last 2.7 h (HEURISTIC): about 850 GB by the end, under 1,200.
- **b69 finder DONE 02:36:16:** 32,334 of 32,334 contexts closed (rc 0). A candidate tree for ES(8) ≤ 302, **not a
  claim**: the two prepared checks (`bal186-20261119/b69prep`, review 6/6) wait for the owner's OK.

### Night of 22-23 Nov (stopped 00:50; owner: "do not add new agents from now on, formalize wave 5 1122 finishes then we call it a day")

- **No agents or workflows run.** Formalization wave 5 (`formalize-wave5-1122`, 21:05 to 00:43) is in §4 and in
  `FORMAL20261122`.
- **Left running unattended** (owner: "Keep them running"). State at 00:24-00:28 on 23 Nov:

| unit | job | state | deadline |
|---|---|---|---|
| `esr-bal-zbs69` | budget-69 finder (`zrow/zbs54_finder.sh 69 16 16384`; CPUQuota 1400 %, CPUs 5-15,21-31) | **DONE 23 Nov 02:36:16**: 32,334 of 32,334 contexts closed, rc 0 (checks wait for the owner) | ended |
| `esr-fvr-drv` + 3 `esr-fvr-c3519-*` | s35_19 Lean check (`res-slices-fv/tools/drive.py`, `FVR_JOBS=3`) | 626 of about 1,412 modules; no root or final yet | driver 23 Nov 21:03 |
| `esr-p2-census` | #810 P2 census (4 shard workers, CPUs 0-4,16-20) | 190 of 512 shards, 1 survivor (shard 301), 0 mismatches against the notes | 24 Nov 16:45 |
| `esr-m16-cnc` | M(16) ≤ 72 cube-and-conquer (3 lanes) | 32,249 cubes certified, 0 SAT, 0 rejected, 0 errors; 49,268 open; kept proofs 79.9 GB | 24 Nov 17:29; it pauses itself at 250 GB of kept proofs |
| `esr-memguard-1122f`, `esv-memguard-1122c` | memory guards (`esr 36000 bal=9500 ag=8000 r36=8500 m16=6000 p2=4000 fvr=10000 dlt=7000 n66=4000 s20=8000`; `esv 4000 fv=4000`) | – | none |

- About 24 threads are busy, under the cap of 28. The yield guard runs as a background shell of the main session and ends
  with it; the b69 watcher already exited (8 h heartbeat). The memory guards stay.
- **Nothing new starts** (owner): not b69's checks when the finder ends, not the s35_20 campaign, not rung-36 case A.
- **Next steps, each after the owner's OK and an advisor check:**
  - b69 finder ended: its checks are prepared in `bal186-20261119/b69prep` (v5n54 assembly, chain302; review 6 of 6).
  - s35_19 finished: accept it by `res-slices-fv/README.md` §9, then compile `combined/src/Combined/Switch3519L15.lean`
    (`combined/README.md` §2.9).
  - s35_20: apply the 4 fixes in `s3520-gate/review/VERIFY_s35_20-gate.md` to LAUNCH_PLAN first, and set `FVR_JOINMEM`
    from the s35_19 Root measurement.
- **Open owner questions:**
  1. Delete Lean chunk sources once their olean exists (regenerable; s35_20 needs 228-239 GB with them, about 140 GB
     without)?
  2. Clean up C42 and C43a (8.1 GB) and C44 (20.7 GB, the FV304 export)?
  3. M(16): keep the 250 GB cap on kept proofs (set by the agent), raise it, or re-check and then delete? At 13.4 GB/h
     (21:44 to 00:28) the run reaches the cap around 13:00 on 23 Nov and pauses (HEURISTIC).
  4. s35_20: how many compiles (more than 3 needs the owner's OK), and when?
  5. Older: merging `origin/es-mac-2026-11-21`; e-mails (owner only).
- **Restart commands** (only if a unit stopped; each resumes from its own state; start the guards first, and stop
  `esr-fvr-drv` before touching a guard):

```bash
G=/home/jay/research/lean/erdos-szekeres-lean/.claude/skills/es-research/scripts/memguard.sh
systemd-run --user --unit=esr-memguard-1123 -p CPUQuota=30% -p MemoryMax=200M -p MemorySwapMax=0 --nice=5 \
  $G esr 36000 bal=9500 ag=8000 r36=8500 m16=6000 p2=4000 fvr=10000 dlt=7000 n66=4000 s20=8000
systemd-run --user --unit=esv-memguard-1123 -p CPUQuota=20% -p MemoryMax=200M -p MemorySwapMax=0 --nice=5 \
  -E LOG=/home/jay/research/data/memguard-20261119.log $G esv 4000 fv=4000
systemd-run --user --unit=esr-bal-zbs69 -p CPUQuota=1400% -p MemoryMax=8G -p MemorySwapMax=0 -p RuntimeMaxSec=259200 \
  --nice=10 --working-directory=/home/jay/research/data/bal186-20261119/zrow \
  /usr/bin/taskset -c 5-15,21-31 ./zbs54_finder.sh 69 16 16384
systemd-run --user --unit=esr-fvr-drv -p CPUQuota=20% -p MemoryMax=400M -p MemorySwapMax=0 -p RuntimeMaxSec=86400 \
  --nice=10 -E FVR_JOBS=3 --working-directory=/home/jay/research/data/formalize-20261122/res-slices-fv \
  /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -I tools/drive.py
systemd-run --user --unit=esr-p2-census -p CPUQuota=400% -p MemoryMax=3600M -p MemorySwapMax=0 -p RuntimeMaxSec=172800 \
  --nice=10 --working-directory=/home/jay/research/data/e810-linux-20261121/p2-census \
  /usr/bin/taskset -c 0-4,16-20 tools/p2_driver.sh
# M(16) since 23 Nov 04:16: the copy with --proof-budget-gb 1200 (the running sum of written proof bytes; the 250 GB
# free-disk floor stays). The old tools/restart_with_preflight.sh (budget 250) would pause the run.
systemd-run --user --unit=esr-m16-cnc -p CPUQuota=300% -p MemoryMax=5400M -p MemorySwapMax=0 \
  -p RuntimeMaxSec=$(( $(date -d "2026-11-24 17:29:54" +%s) - $(date +%s) )) --nice=10 \
  --working-directory=/home/jay/research/data/e810-linux-20261121/m16-le72-run \
  /home/jay/research/data/e810-linux-20261121/m16-recheck/restart_with_preflight_b1200.sh
# M(16) re-check and delete (23 Nov; resumable; one instance per ledger) and its hourly ledger copy
W=/home/jay/research/data/e810-linux-20261121/m16-recheck; R=/home/jay/research/data/e810-linux-20261121/m16-le72-run
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
SPECS="A=cnf/f73A.cnf=cnf/f73A_d8.icnf B1=cnf/f73B1.cnf=cnf/f73B1_d8.icnf B2=cnf/f73B2.cnf=cnf/f73B2_d8.icnf"
systemd-run --user --unit=esr-rck-m16 -p CPUQuota=100% -p MemoryMax=2600M -p MemorySwapMax=0 -p RuntimeMaxSec=172800 \
  --nice=10 --working-directory=$W bash -c "exec $PY -I $W/recheck_delete.py --root $R run $SPECS --delete --follow \
  --jobs 1 --ledger $W/ledger.jsonl >> $W/rck_m16.log 2>&1"
systemd-run --user --unit=esr-rck-m16-copy --on-calendar='*:23' -p CPUQuota=100% -p MemoryMax=500M -p MemorySwapMax=0 \
  -p RuntimeMaxSec=900 --nice=10 --working-directory=$W $PY -I $W/ledger_copy.py $W/ledger.jsonl \
  /home/jay/research/data/e810-linux-20261121/m16-ledger-copy
```

### Resumed 22 Nov 03:48 (owner: research ES and #810 with the new tools; fully use the PC)

- **Caps (owner, about 03:55):** memory at most 80 % in use (48.7 GB of 60.9 GB), CPU at most 90 % (28 threads). With
  about 8–10 GB used by the desktop, the guards are `esr-memguard-1122` (`esr 34000 bal=9500 dlt=7000 n66=23500 r36=8500
  ag=5000`) and `esv-memguard-1122` (`esv 6000 fv=6000`). They were started before the old 21,000 / 3,000 MB guards were
  stopped. SKILL.md §1, AGENTS.md and memory `caps-80-90-20261122` record the new caps.
- **Restarted:**
  - b68 v5 assembly with a fresh marker (03:48:48), then `chain303.sh` (balcheck2). Same SHA and parameters as in §6.
  - The L15 driver: 7 slots, `C15_RES_MB=3300` (observed cube peaks ≤ 2.7 GB), `C15_CPU_CAP_MILLI=24500`.
  - vfy15.
  - FV304: `FV_JOBS=6`, `FV_MEM=5500`. FV_MEM is the total over all FV jobs, not a per-job limit.
- **Restart race (fixed at 03:56).** The old L15 driver launched `ohooho_40o` seconds before its restart. The new
  instance then marked that cube `failed` while its unit ran. Fix: driver stopped, unit stopped, cube set back to
  `queued` with a note, partials renamed `.stopped-20261122b`, driver restarted.
  - Lesson: stop the drivers BEFORE changing the guards.
  - The FV driver had the same clash. It was harmless: the old units finished with rc 0 and their oleans exist.
- **182-vertex graph, 5 colours: the campaign finished at 03:57.** Its own `campaign_status.py` reports 120 of 120
  Y1-cubes refuted (84 directly, 36 through 120 sub-cubes each). **Not a claim yet**: about 2,900 pieces (cubes 78–119)
  have no independent re-check. Wave 3's `v182-recheck` does that re-check.
- **Wave 3** (workflow `research-wave3-1122`, launched about 04:00; 5 workers, each followed by verifiers):
  - `v182-recheck`: independent re-check of the 182-vertex campaign;
  - `m16-premises`: SMS and nauty second routes for P1 = F(14,16) ≤ 57 and P2 = the unique 65-edge support, with census
    controls;
  - `m16-le72-encoder`: forced-structure encoder for M(16) ≤ 72, with 4 positive controls; no run longer than 60 min;
  - `r36-fixes`: RF1–RF4 and RF3b, then an adversarial re-review;
  - `bal2-assure`: sanitizers, clang-tidy and bounded model checking of balcheck2; production binary untouched.
- **Tools:** the owner's installs are checked (`~/research/data/agents-20261121/tools-20261122.md`).
- **Cleanup** (owner-approved, each item checked first; manifest `~/research/data/cleanup-20261122/manifest.txt`):
  - Deleted:
    - the stopped L15 partials `p2/c15/*.stopped-2026112*` (60.1 GB by per-entry du; no certified cube's
      certdir is among them);
    - the two Delta partials (28.6 GB; "not a proof");
    - Lean toolchains 4.35.0 and 4.36.0 (elan's default is now 4.24.0; nothing pins 4.35 or 4.36);
    - `esbmc-v8.7.zip`.
  - `df`: 962 GB → 897 GB used.
  - Not deleted: `~/.cache/uv`. The running uvx MCP servers use it. A `uv cache clean` was started by mistake; it
    blocked on their lock and was stopped before it removed anything.
  - **Not deleted, and must be kept: `~/research/data/es308-20261114/runs`.** The owner approved it as superseded
    307/308 evidence, but the check found that ES(8) ≤ 304, and the pending 303 and 302, use **ResidualBound 118**
    from ES307N20261118. Its slice trees (L10/L11: `runs/b35s18`–`b35s20`) live there.

### Afternoon of 22 Nov (from 16:18; the machine had been idle since about 13:14)

- **Guards** (no drivers running at the swap): `esr-memguard-1122d` = `esr 36000 bal=9500 ag=8000 r36=8500 m16=6000 p2=4000
  fvr=6000 dlt=7000 n66=4000`; `esv-memguard-1122c` = `esv 4000 fv=4000`.
- **Yield guard:** fixed. Its memory trigger is now relative to the running esr total, and it runs for up to 48 h.
- **Guard opened for 302:** marker `zrow/N66_LE_54_VERIFIED`, which names the N66 record §8.
- **b69 finder:** only the finder step runs (`zrow/zbs54_finder.sh 69 16 16384`, unit `esr-bal-zbs69`, 16 threads), from
  16:25. Its inputs re-hashed equal to the pins (`balzs_n54.rows` `9e2dc29a…`, fastbb256 `df17fa74…`, `zzs_rows_n54.json`
  `8419984c…`). The checks will use a v5 variant at rhs 16 and a chain with the fixed summary check, both being prepared.
  No finish time is quoted.
- **Wave 4** (`wave4-squeeze-1122`):
  - b69 check preparation;
  - the FV304 closing audit and a combined Lean theorem for 304;
  - the P2 census resumed (`esr-p2-census`);
  - M(16) ≤ 72 cube-and-conquer (`esr-m16-cnc`);
  - the rung-36 RQ1 fix;
  - the n66enc byte-identity re-run on the frozen exe;
  - the small residual slices in Lean (`esr-fvr-*`).
- **"Lean verify everything" (owner, about 17:00):** formalization wave 3 (`formalize-wave3-1122`) has five Lean
  encoder projects, each with a statement-fidelity review:
  - the four coupled-row blocks of ResidualBound 118;
  - RowsValid R0 for N66 ≤ 55;
  - N66 ≤ 54 at level 15 (the N66 input of 302);
  - χ_rainbow = 6 for the 182-vertex graph (#810);
  - AE33 radius 1.
- **b69 CPU cap:** the finder's CPUQuota was set live to 1400 % so that the total stays at or below 90 % with the
  wave-4 jobs and the Lean compiles.
- **Not started:**
  - the large residual slice trees (s20, b35s19, b35s20: hundreds of CPU-h and up to about 300-500 GB of oleans);
  - FV302, after b69's checks;
  - FV303, skipped because 302 supersedes it.
  Each needs an advisor check before launch.
- **Commit and push** of the N66 ≤ 54 record and these notes: blocked by the permission system, which read the
  owner's "yeah" as not explicit enough for a push; an explicit OK is needed.
- **Cleanup sets whose conditions now hold** (not approved): C42 and C43a (the L15 campaign has ended) and C44 (after
  the FV304 closing audit).

### Cleanup, NOW bucket (22 Nov ~07:45, owner-approved)

- **Basis:** the ledger workflow `ledger-1122` (27 agents) mapped all 195 records and all 64 data folders; skeptics
  overruled 9 of the 44 candidates. Plan: `~/research/data/ledger-20261122/CLEANUP_PLAN.md`.
- **Approved:** the owner approved the NOW bucket only (16 sets).
- **Checks before deleting:** the advisor reviewed the list; every survivor condition was re-checked; a re-grep of all
  work after the skeptic pass and of the two new commits found no reference; C12's 27 paths contain no kept certified
  CNF; nothing had changed since 05:30.
- **Deleted:** 59 exact paths, 13.71 GB. All 1,302 must-keep paths are still present.
- **Two proof sets among them:**
  - C03 removed two cake-accepted proofs that are byte-identical duplicates of `encblean-m9/resolve-smoke-fix`;
  - C31 removed two partial proof traces without a verdict (THEORY310N §7a: deletable with the owner's OK).
- **Result:** `df` shows 949 GB used, 791 GB free. Manifest: `~/research/data/cleanup-20261122/manifest.txt`.
- **Not approved yet:** the other buckets (after copy/note 34.4 GB, narrowed 16.6, after L15 8.1, after FV304 20.7,
  waiver 5.9, declined 15.4).

### Rebalance after the 303 checks (22 Nov 06:28)

The bal track was free and the CPU at about 60 %. The drivers were stopped first, then the guards were swapped:
- `esr-memguard-1122c` = `esr 30000 bal=9500 dlt=7000 n66=27000 r36=8500 ag=7000`;
- `esv-memguard-1122b` = `esv 10000 fv=10000`.

Together that is 40,000 MB, under the 80 % rule. The L15 driver now has 8 slots (`C15_RES_MB=3300`,
`C15_CPU_CAP_MILLI=24500`), and FV304 runs `FV_JOBS=10`, `FV_MEM=9500`. At 06:29:
- L15: 68 certified, 8 running, 25 queued;
- FV304: 2,577 modules, 10 running, none failed;
- machine: CPU 69 %, RAM 47 %, Tctl 77 °C.

### Formalization decisions (owner, 22 Nov 04:45-06:00)

- **Goal: full Lean formalization of every result that is worth it**, before any cleanup of the machine.
  - The keep-set stays on this disk; the running jobs finish; the cleanup scope is not decided yet.
  - SAT-certificate parts aim at **Lean + cake_lpr**: each encoding is formalized in Lean (the ENCBLEAN pattern), and
    cake_lpr's verdicts are the one trusted step. Lean uses the standard axioms only.
  - The owner approved a commit and push of these records.
- **Inventory:** `LEAN_STATUS_20261122.md` (this folder) is the Lean-status agent's map of the 30x chains, with a
  correction of its 303/302 cost figures. The ledger workflow `ledger-1122` is still mapping every record and data
  folder.
- **Formalization wave 1** (`formalize-wave1-1122`, about 05:50):
  - an audited rebuild of the nine 30x composition files into one olean directory, with an import-closure check and
    `#print axioms` (including `composition_303_zzsf` on Linux);
  - `ResidualBound 118` as a Lean theorem modulo explicit slice and row hypotheses (Lemma A, h(F) ≥ 18, gluing).
  - Each item has a statement-fidelity reviewer. No Lake build runs in the repo, because FV304 depends on hash-pinned
    oleans.
- **Preserved in git:** the 14 hash-pinned inputs of the 304/303 tree checks that existed only on disk (LEAN_STATUS
  finding 10). They are rows, zrow.json, assemblers, run scripts, and the balcheck/balcheck2 sources and binaries.
  They were copied into `ES305N20261119/{tools,data}` and `ES303N20261120/data`; every copy matches its record pin
  (`data/PRESERVED_20261122.tsv`).
- **182-vertex graph:** wave 3's `v182-recheck` reports every one of the 4,404 pieces independently accepted (04:35).
  Its rebuild and soundness verifiers are still running, so this is not filed as a result yet.

### Stopped 22 Nov 03:00 (owner: "stop at 3 o clock")

At 02:57 the main session stopped the wave-2 workflow. At 03:00:00 the timer unit `stop0300-research` ran
`~/research/data/agents-20261121/stop0300.sh`. It stopped the drivers, then the job units, then the two guards; by
03:00:05 no `esr-*` or `esv-*` unit was left, and there was no kernel OOM line (log `agents-20261121/stop0300.log`).

- **b68 (ES(8) ≤ 303).**
  - The finder is complete (01:08, rc 0).
  - The v5 assembly + check_tree was stopped after it had written 12,168 of the 32,765 files: all 2,007 big
    contexts, which run first, and part of the small ones. It had run 93.5 minutes. It writes no summary until the
    end, so **no check result exists**.
  - v5 has no resume. Re-run it from the start with a fresh marker, then chain303 (commands below). balcheck2 never
    started. The acceptance values pre-registered in ES303N20261120 §5 stay as they are.
- **L15 campaign (N66 ≤ 54).**
  - 63 certified (51 at the 20 Nov stop; the last one, `ohoooo_40h`, at 02:43), 34 split, 35 queued. The leaf
    cover holds over 98 leaves; the certified cover is not complete.
  - The 4 cubes running at the stop (`ooohho_40o`, `oohoho_40o`, `oohhoo_40o`, `ooohoo_40h_52h`) were set back to
    `queued` with a `requeued` note. Their partial files were renamed `p2/c15/<id>*.stopped-20261122`; nothing was
    certified there.
  - Copy of the status before the stop: `campaign_status.before-stop-20261122.json`.
  - The driver deadline is 24 Nov 08:00; move it if the stop lasts long.
- **Verifier (`vfy15`):** up to date at the stop. The last certified leaf (`ohoooo_40h`) passed cake and sub at 02:48,
  both rc 0.
- **FV304:** 1,280 of 8,192 modules done, none failed (status 02:59:56). The two compiles running at the stop left no
  olean. The driver skips finished modules.
- **Agents:**
  - Wave 2 is stopped (§5).
  - The stop script created `agents-20261121/YIELD`. Delete it before agent units run again.
  - Rung-36 case A has not started; RF1–RF4 of the driver review (§5) come first.

Restart order: the guards first, then the b68 checks, the campaign driver, the verifier, FV.

```bash
# memory guards (start before any unit of their prefix)
systemd-run --user --unit=esr-memguard-1121b -p CPUQuota=30% -p MemoryMax=200M -p MemorySwapMax=0 --nice=5 \
  -E LOG=/home/jay/research/data/memguard-20261119.log \
  /home/jay/research/lean/erdos-szekeres-lean/.claude/skills/es-research/scripts/memguard.sh esr 21000 bal=9500 dlt=7000 n66=17000 r36=8500 ag=3000
systemd-run --user --unit=esv-memguard-1121 -p CPUQuota=20% -p MemoryMax=200M -p MemorySwapMax=0 --nice=5 \
  -E LOG=/home/jay/research/data/memguard-20261119.log \
  /home/jay/research/lean/erdos-szekeres-lean/.claude/skills/es-research/scripts/memguard.sh esv 3000 fv=3000
# b68 checks: v5 assembly + check_tree from the start, then chain303 (waits for the assembly unit, then starts balcheck2)
cd /home/jay/research/data/bal186-20261119/zrow
date '+%F %T' > b68zs/asm_v5_start.txt     # fresh marker: chain303 rejects any file older than it
echo "$(date '+%F %T') start assemble (v5 sha 964b00007e5b..., re-run after the 22 Nov 03:00 stop)" >> b68zs/steps.log
systemd-run --user --unit=esr-bal-zbs68asm -p CPUQuota=1000% -p MemoryMax=8G -p MemorySwapMax=0 -p RuntimeMaxSec=21600 \
  --nice=10 --working-directory=$PWD -E NW_BIG=3 -E BIG_BYTES=10000000 -E SUB_NODES=30000 /usr/bin/taskset -c 5-14 \
  bash -c 'O=/home/jay/research/data/bal186-20261119/zrow/b68zs; python3 -I balz_assemble_v5.py 68 $O/occ - $O/files 10 > $O/assemble.out 2>&1; rc=$?; echo "$(date "+%F %T") assemble+check_tree (v5) rc=$rc $(tail -c 700 $O/assemble.out)" >> $O/steps.log; exit $rc'
systemctl --user is-active -q esr-bal-zbs68asm && systemd-run --user --unit=esr-bal-chain303 -p CPUQuota=10% \
  -p MemoryMax=200M -p MemorySwapMax=0 -p RuntimeMaxSec=28800 --nice=10 --working-directory=$PWD ./chain303.sh
# L15 campaign driver (state in p2/c15/campaign_status.json; move the deadline if needed)
cd /home/jay/research/data/n66-20261113
systemd-run --user --unit=esr-n66-drv15 -p CPUQuota=6% -p MemoryMax=300M -p MemorySwapMax=0 --nice=10 \
  --working-directory=$PWD -E C15_DEADLINE_DAY=24 -E C15_DEADLINE_HM=08:00 -E C15_SLOTS=5 -E C15_RES_MB=3800 \
  -E C15_CPU_CAP_MILLI=27500 /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -u p2c15_driver.py
# verifier
systemd-run --user --unit=esr-vfy-drv15 -p CPUQuota=5% -p MemoryMax=200M -p MemorySwapMax=0 --nice=10 \
  --working-directory=/home/jay/research/data/n66-20261113/vfy15 /bin/bash /home/jay/research/data/n66-20261113/vfy15/bin/driver15.sh
# FV304 driver (resumable)
systemd-run --user --unit=esv-fv-drv -p CPUQuota=20% -p MemoryMax=300M -p MemorySwapMax=0 -p RuntimeMaxSec=432000 \
  --nice=10 --working-directory=/home/jay/research/data/fv304-20261120 -E FV_JOBS=2 -E FV_MEM=2800 -E FV_TMAX=90 \
  taskset -c 5-15,21-31 /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -u \
  /home/jay/research/lean/erdos-szekeres-lean/experiments/omission-compact-checker-2026-11-05/drive_es304z.py
```

Tools: the owner finished the installs at about 03:10 (kissat, drat-trim, SMS, march_cu, z3, cvc5, cbmc, esbmc, ethos,
cryptominisat, nauty 2.8.9 from source, and the Mathlib cache of the #810 Lean project). Versions, hashes and three passing smoke tests are in
`~/research/data/agents-20261121/tools-20261122.md`; es-research SKILL.md §5 lists them.

Open owner questions (unchanged): may main be fast-forwarded to `es-mac-2026-11-21`; deletion of the kept wave-1
proofs (about 12 GB under `a-t34-sat182/a2/`, about 330 MB under `b-recert-ext16/`) once they are re-checked;
whether the Mac session still runs.
