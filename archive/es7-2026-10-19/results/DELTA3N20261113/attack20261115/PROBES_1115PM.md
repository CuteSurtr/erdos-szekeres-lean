# Δ-route SAT probes, 15 November 2026 afternoon (track T3, work 13:22-18:35 KST)

**Final status, 18:22 KST. All T3 units are stopped (none left at 18:21).** Weak D(5,7) and weak D(5,8) remain
OPEN as general statements. No ES bound changes.

- **Weak D(5,8) is CERTIFIED at 16 points** (DELTA2N's eager encoder, CaDiCaL 4,973 s, cake_lpr exact line; claim
  `wd58-m16`, CONFIRMED by V2 after a cake_lpr re-run by the main session): it now holds for all sets with at most
  16 points (was 15).

Labels are the house labels; nothing is rounded up. A claim counts as verified only with a CONFIRMED verdict in
`/home/jay/research/data/roadmap-20261115/pm1115/claims/`.

- **ROOT(7) fails for an abstract 17-point (5,7)-valid signotope** (T3 SAT model, EXACT; claim `root7-m17-abstract`
  CONFIRMED by V1). On that set CONJ-TS′(7) and ENV#(7) fail too; weak D(5,7) and LR(7) hold. The model itself has no
  real realization (claims `root7-m17-nonreal-1` by R7 and `root7-m17-t3-nonrealizable` by T1, both CONFIRMED), but
  R7 and T1 then found REAL 17-point counterexamples to ROOT(7) (claims `root7-real-17`, `root7-real-17-t1`, CONFIRMED).
- **LR(6) is true for all signotopes and all point sets**: T1 certified LR(6) at 15 points on T3's CNF
  `cnf/lrr6_m15.cnf` (encoder `tools/lr_cnf.py`; claim `lrr6-certified`, CONFIRMED, with the verifier's own review of
  the encoder); T3 certified it again with T4's independent CNF [corrected 15 Nov pm (H1, as C1 issue 7 for THEORY):
  independent in code and in the left-side construction, same base-clause patterns (V2's verdict)] (claim `lr6-m15-second`, CONFIRMED); ≤ 14 follows from ROOT(6),
  ≥ 16 is vacuous.
- **TS±(6) is decided for signotopes: CERTIFIED for |S| ≤ 14 and FALSE at |S| = 15** (abstract model in 49 s; claims
  `tspm6-le13` (filed by T4), `tspm6-14`, `tspm6-m15-abstract`; all CONFIRMED). [note 15 Nov pm (C1 issue 5): V3's
  verdict on `tspm6-m15-abstract` confirms the counterexample, but its file (16:33:57, unchanged at 19:15) still marks the
  sentence "TS±(6) is decided … true up to 14" NOT CONFIRMED, for a reason that lapsed at 16:53:54, when V2 changed
  `tspm6-14` to CONFIRMED.] On the 15-point counterexample LR(6), ROOT on both
  sides, TWO-ENV#(6) and weak D(5,6) hold. Realizability not decided (4 × 120 s of `realize_sig.py`: no hit).
  [superseded 15 Nov pm (C1 issue 2): decided. This abstract model has no x-sorted realization: a BFP certificate on
  9 points + V, 76 inequalities, the first line of `t1/ts15/models.jsonl`, accepted by V2's checker
  (VERIFY_TSPM6_REAL15.md). And TS±(6) is false for a real 15-point set: claim `tspm6-real-15` (T1; V2 CONFIRMED,
  verdict file 15:26:34), `t1/tspm6_real15.json` (`142707d7…376d`).]
- **TWO-ENV#(6) holds for all signotopes** (T4's r-independent two-sided form, hypothesised version): |S| = 15
  CERTIFIED with a new T3 encoder (claim `twoenv6-m15`, CONFIRMED) and again with T4's encoding (claim
  `twoenv6-m15-second`, CONFIRMED), 13 and 14 directly (claim `twoenv6-13-14`, CONFIRMED), smaller sizes from ENV#(6) ≤ 11 and TS±(6) ≤ 14 (T4's L2);
  so at n = 6 TWO-ENV# survives where TS± fails.
- **ENV#(6)** fails at |U| = 14 and 15 (claim `env6-fails-root6m15`, CONFIRMED; real sets: T4's `env6-real-14-15`,
  CONFIRMED) and is CERTIFIED for |U| ≤ 11 (claim `env6-le11`, CONFIRMED). 12 and 13 open.
- LR(7) gluing probes (T4 candidate K2′) with the three 17-point ROOT(7) failures as right blocks: no LR(7)
  counterexample with 1 or 2 extra points anywhere left of r (COMPUTED); none of the three blocks admits a new
  leftmost point at all.

## Status table

| statement | size | result | label | time | files (under `/home/jay/research/data/roadmap-20261115/pm1115/t3/`) | claim / verdict |
|---|---|---|---|---|---|---|
| ENV#(6), weak D(5,6), mirror forms, per-set left-or-right forms on the ROOT(6) 15-point model `root6_m15` | 15 (S), 14 (S − r) | **ENV#(6) fails on S and on S − r** (0 ENV# Δs each). Weak D(5,6) holds (467 weak Δs). Mirror forms hold (l = 0 starts 26 four-caps; 231 left-rooted, 206 initial-safe weak Δs of S − l), so both left-or-right disjunctions hold on S | EXACT (abstract signotope; own code) | 13:30 | `runs/root6_m15.forms.json`, `tools/check_forms.py`, `tools/t3lib.py` | `env6-fails-root6m15` CONFIRMED (V1) |
| ENV#(6) | 5-11 | UNSAT, round 6's `env_cnf.py 6 m`, each proof `s VERIFIED UNSAT` (heap 500); |U| ≤ 4 trivial. Encoder control at n = 6 PASS 3/3 (`runs/env_control_n6m12.log`) | CERTIFIED | 13:35 | `cnf/env6_m*.cnf`, `cert/env6/` | `env6-le11` CONFIRMED (V2) |
| ENV#(6) | 12 | no verdict in 45 s (`env_cnf.py`) and 52 s (`root_compact.py --env`) | UNKNOWN | 13:34 | `cnf/env6_m12.cnf`, `cnf/ec6_m12.cnf` | – |
| ROOT(6), LR(6), ENV#(6) | 16 | vacuous: no (5,6)-valid signotope has 16 points (DELTA2N20261113 §4.1, base(5,6,16) CERTIFIED UNSAT) | CERTIFIED (cited) | – | – | T4's `root6-m16-vacuous` |
| ROOT(6) (second abstract model, compact encoder) | 15 | SAT in 13 s; valid, 90 four-caps, r ends 48, 0 rooted Δs; mirror forms hold; ENV# fails on S and S − r | EXACT (abstract; own code) | 13:38 | `models/rc6_m15_fg.json`, `runs/rc6_m15_fg.forms.json` | – (not a new statement) |
| ROOT(7) | 16 | no verdict: CaDiCaL `--sat --seed=1` stopped at its 2,100 s limit (round-6 encoder). No single deletion of the 17-point counterexample is a 16-point counterexample | UNKNOWN | 13:29-14:06 | `cnf/root7_m16.cnf`, `runs/r7m16_s1.log`, `runs/root7_m17_s1.descend.jsonl` | – |
| **ROOT(7)** | **17** | **SAT: abstract counterexample** (CaDiCaL `--sat --seed=1`, 1,599 s). Own exact check: valid, 163 four-caps, r ends 109, U = S − r has 205 convex hexagons and **0 rooted Δs**. Same S: 0 terminal-safe weak Δs (**CONJ-TS′(7) fails at 17**), 0 ENV# Δs for S and for S − r (**ENV#(7) fails at 16 and 17**), weak D(5,7) holds (7,736 weak Δs), mirror forms hold (l starts 25 four-caps; 3,741 left-rooted, 3,263 initial-safe), so LR(7) holds on S. No single deletion S − p (p ≠ r) is a ROOT or CONJ-TS′ counterexample. `realize_sig.py` seeds 1-4 at 120 s: no realization (best min margin about −1.02e-5, 7 violated triples); the model is non-realizable (BFP certificates by R7 and T1, CONFIRMED) | EXACT (abstract; own code) | 13:57 | `cnf/root7_m17.cnf`, `runs/r7m17_s1.log`, `models/root7_m17_s1.json`, `runs/root7_m17_s1.forms.json`, `runs/root7_m17_s1.sha256`, `real/` | `root7-m17-abstract` CONFIRMED (V1) |
| LR(6) (= LRR(6), rooted left-or-right) | 15 | UNSAT, certified by T1 on T3's CNF (CaDiCaL 1,225 s, LRAT 3.62 GB, cake_lpr exact line). Encoder `tools/lr_cnf.py` (soundness in its docstring); T3 positive control PASS 3/3 (`runs/lr_control_n6m13.log`) | CERTIFIED (T1's run; cake_lpr re-run by T3 at 16:45 through a FIFO: exact line, decompressed LRAT SHA-256 `625dffe5…` equal to T1's record, 276 s, heap 1500; `replay/t1_lrr6_m15.json`) | 14:13 | `cnf/lrr6_m15.cnf` (`0555d770…`), `tools/lr_cnf.py`; proof `pm1115/t1/lrrcert/cert/` | `lrr6-certified` CONFIRMED |
| LR(6), LR-TS(6), weak D(5,6), ENV#(6) on T1's 21 real 15-point ROOT(6) counterexamples | 15 | LR and LR-TS hold on all 21 (left-rooted 220-268, initial-safe 179-211); weak D(5,6) holds (409-600 weak Δs); ENV# fails on S and S − r in all 21 | EXACT (own code) | 14:00 | `runs/t1real_forms_summary.txt`, `runs/t1real_*.forms.json` | – (supporting check) |
| ROOT(7) on every prefix of real (5,7)-valid point sets (and of their mirrors, i.e. suffixes) | prefixes with 15-26 points whose last point ends a 4-cap | holds in every instance: 4,643 + 4,711 (mirror) prefixes of the 1,123 real sets of `round6/envroot/pool_valid.jsonl`, and 859 + 854 of the 121 real 26-point sets of DELTA3N `real_pool/full-n7.pool` [corrected 15 Nov pm (C1 issue 20): not a path on disk; the file is `/home/jay/research/data/delta3-codex-20261113/selection/rooted/full-n7.pool` (header `D3POOL 1 121`; converted to `runs/full-n7.jsonl`)]; 0 failures. Control: flags exactly the 21 real ROOT(6) counterexamples of T1 at k = 15 (n = 6) and none of the three real 13-point sets | COMPUTED (pysat verdicts on exact sign data) | 14:12 | `tools/prefix_root.py`, `runs/prefix_*.jsonl` (empty = no failure), `runs/prefix_ctl_n6.jsonl` | – (negative result) |
| TS±(6) (T4 candidate K2) | 13 | UNSAT with T4's `tspm6_m13.cnf` (`0bbee2d5…`): CaDiCaL 71 s, LRAT 520,270,484 B (`5583aea8…`), cake_lpr exact line (16 s, heap 1000) | CERTIFIED (encoder and controls: T4) | 14:17 | `cnf/tspm6_m13.cnf`, `cert/tspm6/` | `tspm6-le13` (filed by T4) CONFIRMED (V3) [corrected 15 Nov pm (C1 issue 11): verdict state added; verdict file 14:27:56] |
| LR(6), second certificate with T4's independent encoding (round 6's `root_cnf.py 6 15` plus T4's mirrored copy) | 15 | UNSAT: CNF `cae7193d…`, CaDiCaL 1,402 s, LRAT 3,524,550,835 B (`fc824a77…`), cake_lpr exact line (122 s, heap 1500) | CERTIFIED (encoder and controls: T4) | 14:59 | `cnf/t4_lr6_m15.cnf`, `cert/t4lr6/` | `lr6-m15-second` CONFIRMED (V2; cake_lpr re-run by the main session) |
| TS±(6) | 14 | UNSAT with T4's `tspm6_m14.cnf` (`921018d6…`): CaDiCaL 599 s, LRAT 2,348,480,245 B (`aa802dae…`), cake_lpr exact line (79 s, heap 1500) | CERTIFIED (encoder and controls: T4) | 14:33 | `cnf/tspm6_m14.cnf`, `cert/tspm6/` | `tspm6-14` CONFIRMED (V2; cake_lpr re-run by the main session) |
| LR(7) gluing (K2′): a 17-point ROOT(7) failure B (T1's real set, R7's real set, T3's abstract model) as the right block plus k new points anywhere left of r; asks for a valid W whose leftmost point starts a 4-cap and is unrootable | 18 (k = 1), 19 (k = 2) | UNSAT for every interleaving pattern: k = 1: 17 patterns, 16 admit a valid W with the hypothesis, 0 LR failures; k = 2: 153 patterns, 136 admit one, 0 failures (each block). Position 0 (a new leftmost point) admits no (5,7)-valid W at all for any of the three blocks (independently re-encoded without mirroring: signotope + no 5-cap is SAT, adding no convex 7-set gives UNSAT). Control: k = 0 gives UNSAT for B and SAT for mirror(B) | COMPUTED (pysat/CaDiCaL verdicts) | 14:20 | `tools/glue.py`, `tools/glue2.py`, `runs/glue_*.log` | – (negative result) |
| LR(7) | 17 | no verdict: compact encoder `tools/lr_compact.py` (positive control PASS 3/3, `runs/lc_control_n6m13.log`), CaDiCaL `--sat --seed=1` stopped at 2,496 s | UNKNOWN | 14:07-14:48 | `cnf/lc7_m17.cnf`, `runs/lc7m17_s1.log` | – |
| CONJ-TS′(7), LR(7), TS±(7), weak D(5,7), ENV#(7) on the two REAL 17-point ROOT(7) counterexamples (R7's and T1's) | 17 | 0 terminal-safe weak Δs in both, so **CONJ-TS′(7) is false for real 17-point sets** (least real counterexample now 15-17 points, was 15-19); left side works (left-rooted 4,316 / 4,129; initial-safe 3,825 / 3,683), so LR(7) and TS±(7) hold; weak D(5,7) holds (8,435 / 8,195 weak Δs); ENV# fails on S and S − r | EXACT (own code, integer coordinates) | 14:36 | `runs/blk_r7real17.forms.json`, `runs/blk_t1real17.forms.json` | `cts7-real-17` CONFIRMED (V1) |
| **TS±(6)** | **15** | **SAT in 49 s: abstract counterexample.** T4's `tspm6_m15.cnf` (`1467209f…`). Own exact check: valid, 25 four-caps, r ends 3, l starts 5; U = S − r has 0 terminal-safe and V = S − l has 0 initial-safe weak Δs, so **TS±(6) fails at 15**; with ≤ 14 CERTIFIED, TS±(6) is decided for signotopes. Same S: ROOT and mirror ROOT hold (914 / 717 rooted Δs), so LR(6) holds; ENV# holds on S (1,014) and U (526), so TWO-ENV#(6) holds; weak D(5,6) holds (1,607). `realize_sig.py` seeds 1-4 at 120 s: no realization (best min margin about −8.5e-6, 9 violated triples) | EXACT (abstract; own code) | 15:01 | `cnf/tspm6_m15.cnf`, `cert/tspm6/tspm6_m15.cadical.log`, `models/tspm6_m15.json`, `runs/tspm6_m15.forms.json`, `runs/tspm6_m15.sha256`, `real/tspm6_m15*` | `tspm6-m15-abstract` CONFIRMED (V3) |
| CB(7), CB(8) (T4 candidate K3) | CB(8) ≤ 15, CB(7) ≤ 13 | hold: the strong form D(5,n; strong) implies CB(n) (an (n−1)-cup is a convex (n−1)-set), and DELTA2N certified the strong form for (5,8) at 7-15 and (5,7) at 6-13 (cnf_hashes.tsv; those proofs were not kept) | PROVED (implication) + CERTIFIED (cited) | 15:01 | – | `cb78-from-strong` CONFIRMED (V1) |
| TS±(7) | 16, 17 | stopped after about 70 CPU-s each without a verdict, because T4 withdrew TS± (v6) after the n = 6 failure. Compact encoder `tools/ts_compact.py` (controls PASS: 3/3 real 13-point sets, d7_13_real, and at m = 15 the TS±(6) model (full CNF SAT), root6_m15 and a real ROOT(6) set (full CNF UNSAT); `runs/tc_control_*.log`) | UNKNOWN | 15:10-15:13 | `cnf/tc7_m16.cnf`, `cnf/tc7_m17.cnf`, `runs/tc7m1*_s1.log` | – |
| LP0(7) (T4 candidate K6: r unrootable ⟹ P0 = points ending no 4-cap meets every gon) | 17 | no verdict: CaDiCaL `--sat --seed=1` stopped at its limit (1,500 CPU-s; CaDiCaL's `-t` counts wall-clock time, so at 50 % CPU it got half). `tools/lp0_add.py` = compact ROOT CNF + "P0 misses a gon" (control PASS 4/4 incl. both branches: `runs/lp0_control_n7m17.log`; root7_m17_s1, both real 17-point sets: P0 meets every gon, CNF UNSAT; mirror of root7_m17_s1: P0 misses a gon, no-rows CNF SAT, full CNF UNSAT), [superseded 15 Nov pm (C1 issue 2): LP0(7) is no longer open for signotopes: it is false for an abstract 19-point W (claim `lp0-7-false-abstract`, P2; V2 CONFIRMED 17:26), and none of the 108 models of P2's scan has an x-sorted realization (claims `lp0-7-w19-nonreal`, `lp0-7-realblock-nonreal`, `lp0-7-scan-all-nonreal`, CONFIRMED). It is open for point sets; the 17-point question of this row stays UNKNOWN] | UNKNOWN | 15:13-16:03 | `cnf/lp0_7_m17.cnf` (`9d13c085…`), `runs/lp07m17_s1.log` | – |
| **TWO-ENV#(6)** (T4 candidate K2′, hypothesised form: r ends and l starts a 4-cap ⟹ U has an ENV# Δ or V has a mirror-ENV# Δ) | **15** | **UNSAT, certified**: new encoder `tools/tenv_compact.py` (controls PASS 3/3 at m = 13 and 3/3 at m = 15: TS±(6) model 526 / 124, root6_m15 0 / 206, a real ROOT(6) set 0 / 201 ENV# / mirror-ENV# Δs; `runs/te_control_*.log`). CaDiCaL 1,857 s wall at 50 % CPU, LRAT 2,953,348,221 B (`87f7f7de…`), cake_lpr exact line (167 s, heap 1300). With |S| ≤ 12 from ENV#(6) ≤ 11, 13-14 from TS±(6) via T4's lemma L2 (and being certified directly), ≥ 16 vacuous: **TWO-ENV#(6) holds for all signotopes** | CERTIFIED | 15:49 | `cnf/te6_m15.cnf` (`fde81f37…`), `cert/te6/` | `twoenv6-m15` CONFIRMED (V1) |
| TWO-ENV#(6) | 13, 14 | UNSAT, certified directly with the same encoder: m = 13 CaDiCaL 70 s, LRAT 407,379,827 B (`f988e0df…`), cake_lpr exact line (17 s); m = 14 CaDiCaL 480 s, LRAT 1,823,924,534 B (`663d3e5f…`), cake_lpr exact line (96 s); heap 1300 | CERTIFIED | 15:52, 16:01 | `cnf/te6_m13.cnf` (`1fe964af…`), `cnf/te6_m14.cnf` (`66da85a3…`), `cert/te6/` | `twoenv6-13-14` CONFIRMED (V3) |
| TWO-ENV#(7) | 15 | no verdict: `tools/tenv_compact.py 7 15` (controls at n = 7 PASS: d7_13_real 232 / 924; root7_m17_s1 0 / 3,741; T1's real 17-point set 0 / 3,685; `runs/te_control_n7m*.log`), CaDiCaL with LRAT at 70-100 % CPU stopped at its 5,400 s wall limit (17:33; about 4,600 CPU-s; the 12.5 GB partial LRAT was deleted, not a proof); in parallel T4's independent encoding `twoenv/twoenv7_m15.cnf` (`c2ce861c…`, over round 6's `env7_m14.cnf`) with LRAT at 50-100 % CPU: no verdict at its 3,800 s wall limit (17:07; partial LRAT deleted, not a proof; `cert/t4te7/`). ≤ 14 follows from ENV#(7) ≤ 13 (CERTIFIED, ROUND6) | UNKNOWN | 16:03-17:33 | `cnf/te7_m15.cnf` (`9b597cfd…`), `cert/te7/` | – |
| TWO-ENV#(6), second certificate with T4's independent encoding `twoenv/twoenv6_m15.cnf` (`b48d3fac…`, T4's `twoenv_cnf.py` over round 6's `env_cnf.py 6 14`) | 15 | UNSAT: CaDiCaL 1,491 s, LRAT 3,750,585,456 B (`2f07f3c9…`), cake_lpr exact line (124 s, heap 1500); proof kept. TWO-ENV#(6) at 15 is now certified by two independent encodings | CERTIFIED (encoder: T4) | 18:01 | `cnf/twoenv6_m15.cnf`, `cert/t4te6/` | `twoenv6-m15-second` CONFIRMED (V2) |
| LR(8) | 16 | no verdict: compact encoder `tools/lr_compact.py 8 16`, CaDiCaL `--sat --seed=1` stopped at its wall limit (1,139 CPU-s) | UNKNOWN | 18:01-18:20 | `cnf/lc8_m16.cnf` (`acbfba00…`), `runs/lc8m16_s1.log` | – |
| TWO-ENV#(7) | 17 | no verdict: CaDiCaL `--sat --seed=1` on `cnf/te7_m17.cnf` (`84dd0965…`) stopped at its wall limit (3,895 CPU-s). TWO-ENV# can fail where LR holds, so this was the easier refutation target at the size where ROOT(7) fails | UNKNOWN | 17:07-18:12 | `runs/te7m17_s1.log` | – |
| ROOT(8) (and LR(8) on failures) on every prefix of the 194 real (5,8)-valid sets of DELTA3N `real_pool/full-n8.pool` [corrected 15 Nov pm (C1 issue 20): not a path on disk; the file is `/home/jay/research/data/delta3-codex-20261113/selection/rooted/full-n8.pool`] (24-42 points) and of their mirrors | prefixes ≥ 16 points | original order: holds in all 2,264 prefix instances (0 failures; 2,051 s at 20 % CPU); mirror order running [superseded 15 Nov pm (C1 issue 11): the mirror pass stopped unfinished at 15:46 to free memory (§2 below)] | COMPUTED (pysat verdicts on exact sign data) | 15:00- | `runs/prefix_full_n8*.jsonl`, `.log` | – |
| **weak D(5,8)** | **16** | **UNSAT, certified.** DELTA2N's reviewed eager encoder (`tools/gen_weakD.py` reproduces the recorded m = 15 CNF hash `228120ee…`); 15,640 vars / 778,924 clauses; CaDiCaL 4,973 s wall (4,114 s process, 3,610,927 conflicts); LRAT 5,572,040,812 B (`68c70856…`); cake_lpr exact line (289 s, heap 1700); proof kept (`.zst` 1,226,706,336 B, `5ba30ae7…`). **Weak D(5,8) now holds for every set with at most 16 points** (open from 17). No ES(8) bound changes | CERTIFIED | 16:17 | `cnf/wd58_m16.cnf` (`d6d34086…`), `cert/wd58/` | `wd58-m16` CONFIRMED (V2; cake_lpr re-run by the main session) |

Encoders written by T3 today (each with a written soundness argument in its docstring and a positive control on real
sets, exact coordinates: fix the signs, delete exactly the rows of the true solutions → SAT, keep all rows → UNSAT):
`lr_cnf.py` (LR, flat rows; PASS 3/3), `root_compact.py` (ROOT and, with `--env`, ENV#; recursive "contains a gon" /
"contains a bad set" flags; PASS 3/3 at n = 6, 1/1 at n = 7 for ROOT; 3/3 and 1/1 for ENV#; deletion counts equal the
main session's control 1,068/460/1,098), `lr_compact.py` (PASS 3/3), `wd_compact.py` (weak D(5,n); PASS 3/3 at n = 6,
1/1 at n = 7). Logs: `runs/*control*.log`.

## Definitions

As in `ROUND6.md` (Definitions), `CONJTS_TEST.md` §2, `VERIFY_ATN_MAIN.md` (mirror form) and T4's
`/home/jay/research/data/roadmap-20261115/pm1115/t4/candidates.md` §0 and K1-K6. In short: (5,n)-valid = signotope
with no 5-cap and no convex n-gon; gon = convex (n−1)-gon; weak Δ of W = 4-cap-free subset of W meeting every gon of W;
r / l = right- / leftmost point, U = S − r, V = S − l; mirror = the same statement on the reflection x → −x (caps stay
caps). Hypotheses "r ends a 4-cap" and "l starts a 4-cap" are the ones a minimal counterexample to weak D(5,n) has.
- **ROOT(n):** r ends a 4-cap ⟹ U has a weak Δ A with A + r 4-cap-free (equivalently: S has a weak Δ through r).
- **CONJ-TS′(n):** r ends a 4-cap ⟹ U has a terminal-safe weak Δ (every 3-cap a<b<c inside has (b,c) ending a
  4-cap of U).
- **ENV#(n):** every valid U has a weak Δ A with (b,c) ∈ ↑P4(U) for every 3-cap a<b<c in A.
- **LR(n)** (= LRR(n) in T3's file names; T4's K1): r ends and l starts a 4-cap ⟹ S has a weak Δ through r or one
  through l. LR(n) for all sizes ⟹ weak D(5,n) (PROVED, T4 L1).
- **TS±(n)** (K2): same hypotheses ⟹ U has a terminal-safe weak Δ or V has an initial-safe one (mirror notion).
- **TWO-ENV#(n)** (K2′, tested in the hypothesised form): same hypotheses ⟹ U has an ENV# Δ or V has a mirror-ENV# Δ
  (an ENV# Δ of the reflected V). TS± ⟹ TWO-ENV# ⟹ LR (T4 L2, CONFIRMED).
- **LP0(n)** (K6): r unrootable ⟹ P0 = {points ending no 4-cap} meets every gon of S. **CB(n)** (K3): every valid S has
  a weak Δ containing no (n−1)-cup.
- **Weak D(5,n):** every (5,n)-valid set has a weak Δ (DELTA2N20261113 README §1-§2).

## Details

### 1. Forms on the ROOT(6) 15-point model (13:30, EXACT, own code)

`tools/check_forms.py` (own code from the definitions; exhaustive over all subsets) on `models/root6_m15.json`
(copy of `round6/mainsession/root15/root6_m15.json`, SHA-256 `165b1b7e…`; the sign string equals the CaDiCaL model's
variables 1-455). Positive control: on the three real 13-point CONJ-TS′(6) sets the script reproduces every count of
the main session's tables in `VERIFY_ATN_MAIN.md` (weak Δs 1,074/2,062/1,997; rooted 462/1,124/1,094; terminal-safe 0;
l starts 4/1/1 four-caps; initial-safe 354/63/78; left-rooted 609/1,201/1,191; ENV# of S 719/1,431/1,437 and of S − r
208/467/508).

Results on root6_m15: valid (0 signotope violations, 0 five-caps, 0 convex hexagons), 98 four-caps, r ends 43;
S has 329 convex pentagons and 467 weak Δs (e.g. {0,1,2,3,4,5,7}); S − r has 292 pentagons, 0 rooted Δs and 0
terminal-safe weak Δs; l = 0 starts 26 four-caps, S − l has 230 pentagons, 231 left-rooted Δs (e.g. {1,2,3,4,5,7})
and 206 initial-safe weak Δs; P4/↑P4 pairs: 19/34 (S), 9/19 (S − r); **ENV# Δs: 0 (S) and 0 (S − r).**

Reading: ENV#(6) fails abstractly at |U| = 14 (this also follows from ROOT(6) failing at 15, by the implication
ENV#(U) ⟹ ROOT(U + r) of ROUND6 track 1 statement 13) and at |U| = 15 (new). The per-set left-or-right forms survive
on root6_m15.

### 2. ROOT(7) at 17 points: the abstract model and what followed (13:57-14:20)

- The round-6 encoder `root_cnf.py 7 17` (251,616 clauses, 108 MB) gave SAT after 1,599 s of CaDiCaL `--sat`
  (seed 1); `root_cnf.py 7 16` gave no verdict in 2,100 s. Decoding: variables 1-680 are the lexicographic triples,
  true = cup; the model satisfies every clause (`runs/root7_m17_s1.model_check.txt`).
- Own exact check (`check_forms.py`, all 2^16 and 2^17 subsets): see the status table. Deletion descent
  (`descend.py`, `descend_ts.py`): no S − p (p ≠ r) is a ROOT(7) or CONJ-TS′(7) counterexample, so this model is
  minimal under single deletions.
- Realizability: `realize_sig.py` seeds 1-4 × 120 s found nothing (best margin −1.02e-5). R7 and T1 then proved it
  non-realizable (BFP certificates, CONFIRMED) and found two REAL 17-point ROOT(7) counterexamples by BFP-CEGAR
  (CONFIRMED). T3's exact check of those two sets: CONJ-TS′(7) fails on both (claim `cts7-real-17`, CONFIRMED), while
  LR(7), TS±(7) and weak D(5,7) hold.
- Real-pool prefixes: ROOT(7) holds on every prefix of 1,244 real (5,7)-valid sets and of their mirrors (11,067
  instances), and ROOT(8) on the 2,264 prefixes of the 194 real (5,8)-valid sets (COMPUTED; mirror pass of n = 8
  stopped unfinished at 15:46 to free memory).
- LR(7) gluing (T4's K2′ test): every interleaving of 1 or 2 extra points with each of the three 17-point blocks is
  UNSAT; a new leftmost point is impossible for all three blocks (no (5,7)-valid extension).

### 3. n = 6 completed for the two-sided forms (14:13-16:01)

- LR(6) at 15: T1's certificate of T3's CNF (claim `lrr6-certified`, CONFIRMED) and T3's certificate of T4's
  independent CNF (claim `lr6-m15-second`; V2 could not re-run cake_lpr within its 0.4 GB budget, so NOT CONFIRMED
  for budget reasons only). [superseded 15 Nov pm (C1 issue 4): V2 changed `lr6-m15-second` to CONFIRMED (verdict file
  16:53:54) after checking the main session's cake_lpr re-run (`round6/mainsession/lr6secondrecake/`, finished 15:08:44,
  exactly one `s VERIFIED UNSAT`).]
- TS±(6): CERTIFIED at 13 and 14 with T4's CNFs, SAT at 15 in 49 s. The model is valid, r ends 3 and l starts 5
  four-caps, U has 0 terminal-safe and V 0 initial-safe weak Δs; LR, TWO-ENV# and weak D hold on it.
- TWO-ENV#(6): T3's new encoder `tenv_compact.py`; UNSAT certified at 13, 14 and 15. Sizes ≤ 12 follow from ENV#(6)
  for |U| ≤ 11 (claim `env6-le11`, CONFIRMED), ≥ 16 are vacuous. So at n = 6 the true two-sided forms are LR and
  TWO-ENV#; the one-sided forms (ROOT, CONJ-TS′, ENV#) and TS± are false.

### 4. Weak D(5,8) at 16 points (14:49-16:18)

The DELTA2N eager CNF for (a, n, m) = (5, 8, 16), written by DELTA2N's own `Enc` class (the wrapper reproduces the
recorded m = 15 CNF hash), was solved with LRAT output in 4,973 s wall and checked by cake_lpr at heap 1700 in 289 s
(exact line). The growth from m = 15 (242 s) was about ×17. By the same factor m = 17 would need about 20 CPU-h
(HEURISTIC), so it was not attempted.

## Files and hashes

All work files are under `/home/jay/research/data/roadmap-20261115/pm1115/t3/` (not in Git):
- `tools/`: T3's code. Exact checkers: `t3lib.py`, `check_forms.py` (all forms on one set), `decode.py`,
  `check_model.py`, `descend.py`, `descend_ts.py`, `prefix_root.py`. Encoders: `lr_cnf.py`, `root_compact.py`,
  `lr_compact.py`, `wd_compact.py`, `ts_compact.py`, `tenv_compact.py`, `lp0_add.py`, `glue.py`, `glue2.py`,
  `gen_weakD.py` (writes DELTA2N's eager CNF). Controls: `*_control.py`. Runners: `certify_t.sh` (copy of round 6's,
  unchanged), `cad_lrat.sh`, `cake.sh`, `on_sat.sh`, `realize4.sh`, `enum_valid.py`, `pool2jsonl.py`.
- `cnf/` (CNFs, regenerable), `runs/` (solver logs, check outputs, controls), `models/` (decoded sign strings, copied
  point sets), `real/` (realize_sig logs), `cert/` (`certify.jsonl` / `solve.jsonl`, CaDiCaL logs, cake_lpr outputs,
  proofs kept as `.lrat.zst`), `claims/` (the JSON files filed with `file_claim.sh`).
- `SHA256SUMS.final` (366 entries, written 18:21; its own SHA-256 `b3770647…`) and the earlier `SHA256SUMS.1515`: SHA-256 of
  every tool, model, run log, claim, replay record, CNF under 200 MB and certificate file (logs, cake_lpr outputs, `.zst` proofs);
  `runs/sha256_early.txt`, `runs/sha256_tools_1424.txt`, `runs/*.sha256` (per-result hash lists).
- Key hashes. CNFs: root7_m17 `44626ab2…`, lrr6_m15 `0555d770…`, t4_lr6_m15 `cae7193d…`, tspm6_m13 `0bbee2d5…`,
  tspm6_m14 `921018d6…`, tspm6_m15 `1467209f…`, wd58_m16 `d6d34086…`, te6_m15 `fde81f37…`, lp0_7_m17 `9d13c085…`.
  Models: root7_m17_s1.json `8d6bedc1…` (sign string `72a678a9…`), tspm6_m15.json `a3210576…`. Proofs (LRAT SHA-256 of
  the decompressed file): tspm6_m13 `5583aea8…`, tspm6_m14 `aa802dae…`, t4_lr6_m15 `fc824a77…`, te6_m13 `f988e0df…`,
  te6_m14 `663d3e5f…`, te6_m15 `87f7f7de…`, twoenv6_m15 (T4 CNF) `2f07f3c9…`, wd58_m16 `68c70856…`, env6_m5..m11 in
  `cert/env6/certify.jsonl`. Kept as `.lrat.zst` (15 files); no partial LRAT is left on disk.
- `tools/t3lib.py` changed at 13:34 (numpy enumeration; identical outputs on root6_m15 and the controls).

## What remains (as of 18:22)

- Independent cake_lpr re-runs: done for all T3 certificates (the main session re-ran `wd58-m16`, `tspm6-14` and
  `lr6-m15-second`; V1 and V3 confirmed `twoenv6-m15` and `twoenv6-13-14`; T3 re-ran T1's `lrr6-certified` proof).
- **TWO-ENV#(7)** (T4's top candidate now): open at 15, 16, 17. Two encodings at 15 gave no verdict in 5,400 s and
  3,800 s with LRAT; 17 gave no verdict in 3,895 CPU-s of SAT mode. ≤ 14 follows from ENV#(7) ≤ 13. A certificate at
  15 needs a longer run or cubes.
- **LR(7)** at 15-17: 17 no verdict in 2,496 s (SAT mode); T1 is certifying 15 (and 16). [superseded 15 Nov pm (C1
  issue 2): at 15 CaDiCaL ended UNSAT (T1, 7,857 s; LRAT 23.7 GB kept as zstd), but cake_lpr ran out of heap at
  1,150 MB, so it is COMPUTED only; the 16-point run was stopped at 15:20 without a verdict (ROOT6_M15_REALIZE.md).]
  LR(7) at 16 together with weak D(5,7) ≤ 15 would give weak D(5,7) at 16.
- **Weak D(5,8)** at 17 (about 20 CPU-h by the ×17 growth, HEURISTIC) and **weak D(5,7)** at 16 (about 5-19 CPU-h).
- **Realizability** of the abstract TS±(6) model (no realization in 4 × 120 s; a BFP check or T1's CEGAR would decide).
  [superseded 15 Nov pm (C1 issue 2): decided by 15:30. The model has no x-sorted realization (BFP certificate on 9
  points + V, V2 in VERIFY_TSPM6_REAL15.md), and a real 15-point TS±(6) counterexample exists (claim `tspm6-real-15`,
  V2 CONFIRMED).]
- ENV#(6) at |U| = 12, 13; ENV#(7) at 14, 15; CONJ-TS′(7) at 15, 16 (the one-sided forms are dead as general
  statements, so these only fix thresholds).
- CB(6) at 14, 15 and CB(7) at 14, 15: 45-50 s SAT tries gave nothing; CB(6) at 13 took 567 s (×63 per point), so
  certificates need cubes. LP0(7) at 17: no verdict in 1,500 CPU-s. [note 15 Nov pm (C1 issue 2): LP0(7) itself is
  false for an abstract 19-point signotope (`lp0-7-false-abstract`, CONFIRMED) and open for point sets.]
- Not run: LR(8) at 16 as a probe (the direct weak D(5,8) certificate made it unnecessary for size 16), glue k = 3,
  ONE(n), DEPTH(n) (T4). [corrected 15 Nov pm (C1 issue 11): glue k = 3 was run with `glue.py` (points left of l):
  `runs/glue_*_k3.log` (14:17-14:18) end with exit 20 (UNSAT) for all three blocks, the "9 CNFs UNSAT" (k = 1..3) of
  THEORY_1115PM.md §4; vacuous by `leftsat-r7blocks`. LR(8) at 16 was later run as a probe (status table, 18:01-18:20,
  no verdict).]

## Resume commands

```bash
T3=/home/jay/research/data/roadmap-20261115/pm1115/t3; PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd $T3
$PY tools/check_forms.py models/root7_m17_s1.json 7          # all forms on the ROOT(7) model (< 1 s)
$PY tools/check_forms.py models/tspm6_m15.json 6             # all forms on the TS±(6) model
bash tools/on_sat.sh lex 17 cnf/root7_m17.cnf runs/r7m17_s1.log 7 root7_m17_s1   # re-decode and re-check a model
# a SAT probe as a unit (example: LP0(7) at 17)
systemd-run --user --unit=esr-agz-t3-<job> -p CPUQuota=100% -p MemoryMax=900M -p MemorySwapMax=0 -p RuntimeMaxSec=<s> \
  --nice=10 --working-directory=$T3 bash -c "/usr/bin/cadical --sat --seed=1 -t <s> cnf/lp0_7_m17.cnf > runs/x.log 2>&1"
# a proof run, then the check (the check needs MemoryMax above the heap)
systemd-run --user --unit=esr-agz-t3-<job> ... bash tools/cad_lrat.sh cnf/te6_m15.cnf cert/te6 <secs>
systemd-run --user --unit=esr-agz-t3-<job>c -p MemoryMax=2500M ... bash tools/cake.sh cnf/te6_m15.cnf cert/te6/te6_m15.lrat 2000 cert/te6
grep -x 's VERIFIED UNSAT' cert/te6/te6_m15.cake.out
# controls of an encoder (example)
$PY tools/tenv_control.py cnf/te6_m15.cnf 6 models/tspm6_m15.json models/root6_m15.json
```
