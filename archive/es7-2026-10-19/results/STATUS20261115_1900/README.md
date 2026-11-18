# STATUS20261115_1900: handoff at the end of the 15 November afternoon session (13:05-19:00 KST)

This is the newest status page. It supersedes [STATUS20261115_1000](../STATUS20261115_1000/README.md), which is still the
place for the 14-15 November night. **Nothing was committed, pushed, published or deleted by the main session this
afternoon** (`git log`: the last commit is still 8621eb159; 17:10). All of today's records are untracked files in the
working tree.

How the afternoon ran (all research units had stopped by 18:42; the memory guard was stopped at 18:43 and the
main session's watcher at 18:43; load average 0.5):

- **Compute.** Every job ran as an `esr-*` systemd user unit under a memory guard (`esr-memguard-pm15` from 13:12:05,
  restarted as `esr-memguard-pm15b` at 13:57:23 with the n66 track raised from 13,500 to 17,000 MB): 24,000 MB in
  total, per-track budgets (n66, lo, agx, vfy, agy, abs), and the 16-thread cap on the summed CPUQuota. The guard's
  5-minute samples stayed between 6.3 and 13.6 GB (log `/home/jay/research/data/memguard-20261115pm.log`, read 18:19).
  It stopped one unit cleanly (16:05:17; see Process notes); no other stop in the log. No OOM kill.
- **Agents.** Workflow agents T1 (realizability), T3 (SAT probes), T4 (theory), T5 (d6_12 recount), U1 (N66 cube
  verifier), U2 ((20,15) batch audits), L1 (ABSAT8 independent encoder), V1, V2, V3 (verifiers); extra agent R7 (ROOT(7)
  realizability); wave 2 P1 (LR proof attempt), P2 (LP0 proof attempt), A1 (N66 cost analysis; no record at 18:07),
  A2 (working files on the (20,15) loop in `pm1115/a2/`; no record at 18:07), W1 (Δ-to-ES(8) ledger), C1 (critic);
  wave 3: D1 (this draft), E7 (lower-bound plan,
  [LOWERBOUND_PLAN_1115PM.md](../ROADMAP20261115/LOWERBOUND_PLAN_1115PM.md)); other wave-3 tracks: unclear, see the
  workflow.
- **Claims protocol.** Agents filed claims in `/home/jay/research/data/roadmap-20261115/pm1115/claims/`
  (`<id>.claim.json`); an independent verifier wrote `<id>.verdict.json` and a `VERIFY_<KEY>.md` in the record, with
  its own code. **At 18:28, 45 claims had been filed (13:18-18:18) and all 45 had a CONFIRMED verdict.** Two of them
  carry an exception (`tspm6-m15-abstract`: one sentence NOT CONFIRMED; `w1-cb-window`: one sentence refuted as
  worded), and `p1-c2six` was confirmed at the label COMPUTED only (its CERTIFIED status comes from the main session's
  cake_lpr run at 18:20). Final count at 18:41: 45 claims, 45 verdict files, all CONFIRMED. Three verdicts (`tspm6-14`,
  `lr6-m15-second`, `wd58-m16`) were first NOT CONFIRMED only because the verifier's memory budget could not hold
  cake_lpr; V2 changed them to CONFIRMED at 16:53 after checking the main session's re-runs (each file keeps the
  earlier verdict in its `previous` field).
- **Main-session checks** are in [MAINSESSION_1115PM.md](../DELTA3N20261113/attack20261115/MAINSESSION_1115PM.md): own
  exact checks of the real ROOT(6) and ROOT(7) sets, and fresh cake_lpr runs on nine proofs that the verifiers' memory
  budgets could not hold (14:19-18:20).
- **Critic.** C1's issue list `/home/jay/research/data/roadmap-20261115/pm1115/c1/ISSUES.md` is FINAL (18:12; the
  records as they stood at 17:45-18:10; 20 numbered issues plus open items). Its points that change this page are
  folded in below.

**Headlines (final, 18:41; details and labels below).**
- No ES bound changed. ES(8) ≤ 308 stands; 307 still needs (20,15) and N66 ≤ 55 (or a (21,14) tree).
- Δ program: every one-sided rooted form is false for real point sets (ROOT(6) at 15, ROOT(7) at 17, CONJ-TS′(7) at
  17, ENV#(6), ENV#(7), TS±(6) at 15; EXACT). LR(6) and TWO-ENV#(6) hold for every signotope in their hypothesised
  form, and weak D(5,8) for every set with ≤ 16 points (CERTIFIED). LP0(7) is false for signotopes, but all 108 models
  found are non-realizable. Weak D(5,7) and weak D(5,8) remain OPEN.
- ES(8) upper bound: (20,15) has 998 of 8,065 contexts closed and 507 CERTIFIED rows (final, 18:40); the N66 cube campaign
  has **79 CERTIFIED of 102 leaves, 25/32 = 78.1 % of the split by measure** (final, 18:40). U1 re-verified the 76
  certified by 18:23; 3 remain for its checks.
- ES(8) lower bound: the ABSAT8 one-point non-extendability of 28 + 7 named 64-point order types is now CERTIFIED with a
  PROVED soundness argument (independent encoder).

**Times.** Verdict times below are the verdict files' modification times (for files rewritten later, the first verdict's
time from the verifier's log or the main session's watcher). The `time` fields inside some claim and verdict files run
up to about 20 minutes ahead of the file times (C1, issue 14).

## Results (labels as in the records; nothing rounded up)

**No ES bound changes this afternoon.** ES(8) ≤ 308 stands (computer-assisted, unrefereed, uncommitted). No novelty
statement is made for any item; the last full literature check is [NOVELTY20261115](../NOVELTY20261115/README.md).
Track N1 added [DELTA_PM_CHECK.md](../NOVELTY20261115/DELTA_PM_CHECK.md) for today's statements (bounded search, 17:25).
- **Not found in this search:** weak D(5,n) in the project's sense, ROOT, CONJ-TS′, ENV#, TS±, TWO-ENV#, LR, LP0, CB,
  and the wave-2 lemmas.
- **Closest related work:** the Erdős–Szekeres 1935 argument on left ends of cups (the cup analogue of a weak Δ); Baek's
  Lean-checked Δ induction, whose Δ meets cups and not gons; the "transversal cup" conjecture in gotrevor's public notes.
  The step "SAT model, then a BFP non-realizability certificate" is established practice (Heule–Scheucher).
- **Side lead (not verified):** Baek's theorem with two signotope facts from today may give M(4;n) ≤ C(n−1,2)+1 for
  every signotope.

### Δ program: weak D(5,7) and weak D(5,8) remain OPEN

The folder index [attack20261115/README.md](../DELTA3N20261113/attack20261115/README.md) gained a section "Afternoon of
15 November" at 17:59 that links the main records. They are:
[THEORY_1115PM.md](../DELTA3N20261113/attack20261115/THEORY_1115PM.md) (T4's map; its title says v6 16:55, the file
last changed at 18:02),
[PROBES_1115PM.md](../DELTA3N20261113/attack20261115/PROBES_1115PM.md) (T3, status 18:13),
[ROOT6_M15_REALIZE.md](../DELTA3N20261113/attack20261115/ROOT6_M15_REALIZE.md) (T1, final 18:22),
[ROOT7_M17_REALIZE.md](../DELTA3N20261113/attack20261115/ROOT7_M17_REALIZE.md) (R7, final 18:05),
[LEDGER_1115PM.md](../DELTA3N20261113/attack20261115/LEDGER_1115PM.md) (W1),
[D6_12_NOTE.md](../DELTA3N20261113/attack20261115/D6_12_NOTE.md) (T5),
[MAINSESSION_1115PM.md](../DELTA3N20261113/attack20261115/MAINSESSION_1115PM.md), the update sections of
[ROOT6_MAIN.md](../DELTA3N20261113/attack20261115/ROOT6_MAIN.md), the two proof-attempt files and the `VERIFY_*.md`
files named in the tables.

In short: every one-sided induction statement fails for real point sets at n = 6 (15 points) and n = 7 (17 points);
the two-sided forms LR(6) and TWO-ENV#(6) hold for every signotope (in their hypothesised form: r ends a 4-cap and l
starts one); weak D(5,8) now holds for every set with at most 16 points. Late in the afternoon (17:26) **LP0(7), one
of the three surviving reductions, was found false for an abstract 19-point signotope W**; LR(7) and weak D(5,7) hold
on W. W itself has no realization at all (EXACT, 17:37), and none of the 108 models of P2's scan has an x-sorted
realization (EXACT, 17:49), so **LP0(7) is still open for point sets**.

#### Refuted for real point sets (EXACT unless noted)

| statement | result | claim (filer) | verdict | record |
|---|---|---|---|---|
| ROOT(6) | **false for a real 15-point set**. T1's first 21 real 15-point counterexamples were all confirmed by V3's checker (one filed); by 18:22 T1 had 177 distinct ones (EXACT, T1's own checks, not filed), the smallest with every \|coordinate\| ≤ 924. With CERTIFIED ≤ 14 and 16 vacuous, ROOT(6) is completely decided | `root6-real-15` (T1) | V3 CONFIRMED 13:39; main's own check 13:37-13:40 | [ROOT6_MAIN.md](../DELTA3N20261113/attack20261115/ROOT6_MAIN.md), [ROOT6_M15_REALIZE.md](../DELTA3N20261113/attack20261115/ROOT6_M15_REALIZE.md), [VERIFY_ROOT6_REAL15.md](../DELTA3N20261113/attack20261115/VERIFY_ROOT6_REAL15.md) |
| ROOT(6), abstract | false for a 15-point signotope (main session's CaDiCaL model of `root6_m15.cnf`, SAT in 26.5 s at 13:12) | `root6-m15-abstract` (main) | V3 CONFIRMED 13:26 | [VERIFY_ROOT6_M15.md](../DELTA3N20261113/attack20261115/VERIFY_ROOT6_M15.md) |
| that abstract model | has no realization at all (BFP certificate, 288 inequalities); 8 of its points plus V already have no x-sorted realization (23 inequalities) | `root6-m15-main-nonrealizable` (T1) | V2 CONFIRMED 13:50 | [VERIFY_ROOT6_M15_NONREAL.md](../DELTA3N20261113/attack20261115/VERIFY_ROOT6_M15_NONREAL.md) |
| ROOT(7) | **false for real 17-point sets**: R7's set and, independently, T1's set (BFP-CEGAR on T3's `root7_m17.cnf`) | `root7-real-17` (R7), `root7-real-17-t1` (T1) | V1 CONFIRMED 14:13 and 14:14; main's own check 14:13 | [ROOT7_M17_REALIZE.md](../DELTA3N20261113/attack20261115/ROOT7_M17_REALIZE.md), [VERIFY_ROOT7_REAL17.md](../DELTA3N20261113/attack20261115/VERIFY_ROOT7_REAL17.md), [VERIFY_ROOT7_REAL17_T1.md](../DELTA3N20261113/attack20261115/VERIFY_ROOT7_REAL17_T1.md) |
| ROOT(7), abstract | false for a 17-point signotope (T3, CaDiCaL `--sat`, 1,599 s); that model has no x-sorted realization (9 points + V, 27 inequalities) | `root7-m17-abstract` (T3); `root7-m17-nonreal-1` (R7), `root7-m17-t3-nonrealizable` (T1) | V1 CONFIRMED 14:00; V2 14:08; V1 14:10 | [VERIFY_ROOT7_M17.md](../DELTA3N20261113/attack20261115/VERIFY_ROOT7_M17.md), [VERIFY_ROOT7_M17_NONREAL1.md](../DELTA3N20261113/attack20261115/VERIFY_ROOT7_M17_NONREAL1.md), [VERIFY_ROOT7_M17_NONREAL.md](../DELTA3N20261113/attack20261115/VERIFY_ROOT7_M17_NONREAL.md) |
| CONJ-TS′(6) | false for real 13-point sets (the main session's 09:12 result, now checked by a second party). At 14 points: V2's side observation (EXACT, V2's code), not filed and not checked by a second party | `cts6-real-13` (main) | V1 CONFIRMED 13:27 | [VERIFY_CTS6_REAL.md](../DELTA3N20261113/attack20261115/VERIFY_CTS6_REAL.md) |
| CONJ-TS′(7) | false for the two real 17-point ROOT(7) sets, so the least real counterexample has 15-17 points (was 15-19) | `cts7-real-17` (T3) | V1 CONFIRMED 14:38 | [VERIFY_CTS7_REAL17.md](../DELTA3N20261113/attack20261115/VERIFY_CTS7_REAL17.md) |
| ENV#(6) | false for real sets with \|U\| = 14 and 15 (21 real sets); VE(6) and (U) fail at U = S − r (PROVED corollaries). The abstract failure at 14 and 15 came first (T3) | `env6-real-14-15` (T4); `env6-fails-root6m15` (T3) | V3 CONFIRMED 13:51; V1 13:32 | [VERIFY_ENV6_REAL.md](../DELTA3N20261113/attack20261115/VERIFY_ENV6_REAL.md), [VERIFY_ENV6_ROOT6M15.md](../DELTA3N20261113/attack20261115/VERIFY_ENV6_ROOT6M15.md) |
| ENV#(7) | false for real sets with \|U\| = 16 and 17; VE(7) and (U) fail at U = S − r (PROVED) | `env7-real-16-17` (T4) | V1 CONFIRMED 14:21 | [VERIFY_ENV7_REAL.md](../DELTA3N20261113/attack20261115/VERIFY_ENV7_REAL.md) |
| TS±(6) (T4's two-sided terminal-safe form K2; hypothesised) | **false for a real 15-point set** (BFP-CEGAR, T1) and for an abstract 15-point signotope (T3, SAT in 49 s; that model is not x-sorted realizable, V2's side check). With CERTIFIED ≤ 14 it is decided for signotopes | `tspm6-real-15` (T1); `tspm6-m15-abstract` (T3) | V2 CONFIRMED 15:26; V3 CONFIRMED 15:04, except the sentence "TS±(6) is decided", which V3 left NOT CONFIRMED because it rested on `tspm6-14`. `tspm6-14` became CONFIRMED at 16:53; V3 had not updated its verdict by the end of the session (file still from 16:33:57, checked 18:41), so that one sentence stays NOT CONFIRMED in V3's file | [VERIFY_TSPM6_REAL15.md](../DELTA3N20261113/attack20261115/VERIFY_TSPM6_REAL15.md), [VERIFY_TSPM6_M15.md](../DELTA3N20261113/attack20261115/VERIFY_TSPM6_M15.md) |

#### Refuted for abstract signotopes only (EXACT; no realizable counterexample known)

| statement | result | claim (filer) | verdict | record |
|---|---|---|---|---|
| **LP0(7)** (r unrootable ⟹ the points that end no 4-cap form a weak Δ) | **false for a 19-point (5,7)-valid signotope W**: r = 18 lies in no weak Δ (exhaustive over 2^18), and P0(W) misses 47 convex hexagons. W minus two points is R7's real ROOT(7) set. Found by extending known right-hostile 17-point blocks by 2 points (the claim said 45 of 1,530 patterns; P2's final record corrects this to 108 patterns over the 10 blocks; V2 did not check the count). The same W refutes P2's conjecture H7U(7) at \|U\| = 18. LR(7) and weak D(5,7) hold on W (5,833 weak Δs through l) | `lp0-7-false-abstract` (P2) | V2 CONFIRMED 17:26 (own code from the signs; two further listed models also refute LP0(7)) | [VERIFY_LP0_7_FALSE.md](../DELTA3N20261113/attack20261115/VERIFY_LP0_7_FALSE.md), [PROOF_LP0_ATTEMPT_P2.md](../DELTA3N20261113/attack20261115/PROOF_LP0_ATTEMPT_P2.md) |
| that W | has no realization by any 19-point configuration: BFP certificate on the whole chirotope, no point at infinity, 686 inequalities | `lp0-7-w19-nonreal` (R7) | V1 CONFIRMED 17:37 | [VERIFY_LP0_7_W19_NONREAL.md](../DELTA3N20261113/attack20261115/VERIFY_LP0_7_W19_NONREAL.md), [ROOT7_M17_REALIZE.md](../DELTA3N20261113/attack20261115/ROOT7_M17_REALIZE.md) "LP0(7) model W of P2" |
| all LP0(7) models of P2's scan | none of the 108 satisfiable 19-point models has an x-sorted real realization. The 21 on a real 17-point block: 20 have a V-free BFP certificate (no realization at all), 1 a certificate with V (588-746 inequalities each). The other 87 inherit their block's certificate (9-14 points + V). Separately, R7's direct search over two-point extensions of the five real 17-point ROOT(7) sets tested 3.6 million valid 19-point sets and found no real LP0(7) counterexample (HEURISTIC; R7 final status 18:05) | `lp0-7-realblock-nonreal`, `lp0-7-scan-all-nonreal` (R7) | V2 CONFIRMED 17:48 and 17:49 (validity and unrootability of the 87 not checked; not claimed) | [VERIFY_LP0_7_REALBLOCK_NONREAL.md](../DELTA3N20261113/attack20261115/VERIFY_LP0_7_REALBLOCK_NONREAL.md), [VERIFY_LP0_7_SCAN_ALL_NONREAL.md](../DELTA3N20261113/attack20261115/VERIFY_LP0_7_SCAN_ALL_NONREAL.md) |

Weak D holds on every set in both tables; no counterexample to weak D is known for any n. LR, TWO-ENV#, LP0, CB and ONE
hold on all 27 rooted failures (22 at n = 6, 5 at n = 7), and LR, LP0 and TWO-ENV# on all 44 CEGAR models of rooted
failures (EXACT, T4's own code; THEORY_1115PM.md §3, §5). The 19-point W above came after T4's count, and LP0(7)
fails on it.

#### Certified (CERTIFIED = CaDiCaL 2.1.3 LRAT accepted by cake_lpr with the exact line)

| statement | result | claim (filer) | verdict and independent cake_lpr re-run | record |
|---|---|---|---|---|
| **LR(6) = LRR(6)**: if r ends a 4-cap and l starts one, S has a weak Δ through r or one through l | **holds for every (5,6)-valid signotope, hence every point set**: 15 points certified on T3's CNF (LRAT 3.62 GB) and again on T4's separately written CNF (3.52 GB; independent in code and in the left-side construction, with the same base-clause patterns, V2); ≤ 14 from ROOT(6); ≥ 16 vacuous (PROVED combination) | `lrr6-certified` (T1), `lr6-m15-second` (T3) | V1 CONFIRMED 14:18 (no re-run; heap over budget); main re-run 14:19-14:21; T3 re-run 16:45. V2 NOT CONFIRMED (V2's log: 15:08; heap 300 exhausted); main re-run 15:06-15:08; V2 CONFIRMED 16:53 | [VERIFY_LRR6.md](../DELTA3N20261113/attack20261115/VERIFY_LRR6.md), [VERIFY_LR6_M15_SECOND.md](../DELTA3N20261113/attack20261115/VERIFY_LR6_M15_SECOND.md) |
| **TWO-ENV#(6)**, hypothesised form: if r ends a 4-cap and l starts one, S − r has an ENV# Δ or S − l a mirror-ENV# Δ | **holds for every signotope**: 13, 14, 15 certified with T3's new encoder; ≤ 12 from ENV#(6) ≤ 11; ≥ 16 vacuous. Nothing is certified at 13-15 without the hypothesis (C1). A second certificate at 15 on T4's separately written CNF (`twoenv6_m15.cnf`; CaDiCaL 1,491 s, LRAT 3.75 GB, cake_lpr exact line at 18:01) | `twoenv6-m15`, `twoenv6-13-14` (T3); `twoenv6-m15-second` (T3) | V1 CONFIRMED 16:04 (no re-run); V3 CONFIRMED 16:24 (own re-run of 13; 14 from the main session's re-run); main re-runs of 13, 14, 15 at 16:06-16:16. `twoenv6-m15-second`: main re-run 18:02-18:11 (heap 1,500); V2 CONFIRMED 18:11 | [VERIFY_TWOENV6_M15.md](../DELTA3N20261113/attack20261115/VERIFY_TWOENV6_M15.md), [VERIFY_TWOENV6_13_14.md](../DELTA3N20261113/attack20261115/VERIFY_TWOENV6_13_14.md) |
| TS±(6) (hypothesised) | holds for \|S\| ≤ 13 (13 certified on T4's CNF; ≤ 12 via CONJ-TS′(6)) and at 14 (T4's CNF, LRAT 2.35 GB); fails at 15 (above) | `tspm6-le13` (T4/T3), `tspm6-14` (T3) | V3 CONFIRMED 14:27 (own re-run); V2 NOT CONFIRMED (V2's log: 14:46; heap); main re-run 14:45-14:46; V2 CONFIRMED 16:53 | [VERIFY_TSPM6.md](../DELTA3N20261113/attack20261115/VERIFY_TSPM6.md), [VERIFY_TSPM6_14.md](../DELTA3N20261113/attack20261115/VERIFY_TSPM6_14.md) |
| **weak D(5,8) at 16 points** | **holds for every set with at most 16 points** (was 15). DELTA2N's reviewed eager encoder; CaDiCaL 4,973 s; LRAT 5.57 GB. Open from 17 | `wd58-m16` (T3) | V2 NOT CONFIRMED 16:23 (no re-run in 0.4 GB); main re-run 16:19-16:23 (heap 2,000); V2 CONFIRMED 16:53 | [VERIFY_WD58_M16.md](../DELTA3N20261113/attack20261115/VERIFY_WD58_M16.md), [PROBES_1115PM.md](../DELTA3N20261113/attack20261115/PROBES_1115PM.md) §4 |
| ENV#(6) | holds for \|U\| ≤ 11 (round 6's encoder); 12 and 13 open | `env6-le11` (T3) | V2 CONFIRMED 14:30 (re-run 7/7; own encoder 5-11) | [VERIFY_ENV6_LE11.md](../DELTA3N20261113/attack20261115/VERIFY_ENV6_LE11.md) |
| CB(6) (a weak Δ with no 5-cup; between the weak and the strong form) | holds for every set with at most 13 points; 14, 15 open | `cb6-le13` (T4) | V2 CONFIRMED 14:31 (V2's log; re-run 7/7); addendum (file time 15:29): V2's own encoder certified 7-13 | [VERIFY_CB6.md](../DELTA3N20261113/attack20261115/VERIFY_CB6.md) |
| CB(7), CB(8) | CB(7) for \|S\| ≤ 13 and CB(8) for \|S\| ≤ 15, because strong D(5,n) implies CB(n) (PROVED) and DELTA2N certified the strong forms (CERTIFIED by citation). CB(8) at 15 rests on the DELTA2N record only: that proof was deleted and never re-run | `cb78-from-strong` (T3) | V1 CONFIRMED 15:23 (V1's own strong-form encoder re-certified (5,7) 6-13 and (5,8) 7-14) | [VERIFY_CB78_FROM_STRONG.md](../DELTA3N20261113/attack20261115/VERIFY_CB78_FROM_STRONG.md) |
| Left saturation of 10 right-hostile 17-point blocks (n = 7) | no (5,7)-valid signotope contains one of these 10 blocks together with a point left of its leftmost point. So every valid superset keeps the block's leftmost point, left-gluing tests on these blocks are vacuous, and an LR(7) failure containing one of them has l(W) = l(block). Control: the mirror of R7's real set admits such a point. C1: three further known right-hostile blocks (T1's real m17_it5 and m17_it6, R7's div17 set) were not tested | `leftsat-r7blocks` (P2) | V3 CONFIRMED 17:38 (own independently written CNFs certified 10/10, plus a cake_lpr re-run of each kept proof) | [VERIFY_LEFTSAT_R7BLOCKS.md](../DELTA3N20261113/attack20261115/VERIFY_LEFTSAT_R7BLOCKS.md) |
| ROOT(6) and every n = 6 statement at ≥ 16 points | vacuous: no (5,6)-valid signotope has 16 points (DELTA2N base(5,6,16), CERTIFIED by citation, its LRAT not kept; T1 re-certified it with its own encoder, proof kept, not yet re-run by a second party) + PROVED inheritance | `root6-m16-vacuous` (T4) | V1 CONFIRMED 14:19 (V1's log; summary updated 14:47) | [VERIFY_ROOT6_M16_VACUOUS.md](../DELTA3N20261113/attack20261115/VERIFY_ROOT6_M16_VACUOUS.md) |

#### Proved

- **T4's four lemmas** (`t4-lemmas`, V2 CONFIRMED 14:14, [VERIFY_T4_LEMMAS.md](../DELTA3N20261113/attack20261115/VERIFY_T4_LEMMAS.md)):
  L1 LR(n) ⟹ weak D(5,n); L2 TS±(n) ⟹ TWO-ENV#(n) ⟹ LR(n); L3 ENV# Δs of U give weak Δs through r (equality when
  r is the maximal capper); L4 Lemma M (monotonicity, gluing form of LR). V2 found a gap in the written proof of L4's
  last clause (wording fix now in THEORY_1115PM.md §2.2, Cor. 3); Cor. 4 not checked. Weak D needs only the
  hypothesised forms (L2, then L1).
- **CB window lemma** (`w1-cb-window`, W1; V3 CONFIRMED 17:10 with one exception,
  [VERIFY_W1_CB_WINDOW.md](../DELTA3N20261113/attack20261115/VERIFY_W1_CB_WINDOW.md)): CB(n) is hereditary (PROVED);
  a vertex-critical CB(n) counterexample has at most C(n−1,2) + M(5;n−1) + 1 points (PROVED from CERTIFIED inputs), so
  the open windows are 16-58 for CB(8) and 14-31 for CB(7); CB(8) at 58 points is equivalent to N5 ≤ 57, which would
  give ES(8) ≤ 302. Refuted as worded: the claim's sentence "CB(8) is open at every size ≥ 16 and CB(7) at every size
  ≥ 14" (CB(7) is vacuously true from 37 points, since M(5;7) ≤ 36).
- The implication strong D(5,n) ⟹ CB(n) (in `cb78-from-strong`), and the VE/(U) corollaries (in `env6-real-14-15`,
  `env7-real-16-17`).
- LP0(n) ⟹ weak D(5,n) (THEORY_1115PM.md §2.1; not filed as a claim, so not checked by a second party). LP0(7) itself
  is now false for signotopes (above).

#### Claims of the wave-2 proof-attempt tracks (none proves LR(7), LP0 or weak D(5,7))

- `p1-cupext` (P1): Lemma G, Cor. G2 (every gon contains a point that ends no 4-cap or one that ends an (n−2)-cup;
  mirror likewise), Cor. SD (no (n−2)-cup ⟹ P0 and Q0 are weak Δs; a re-proof), Lemma A1, Prop. R (LR(n) follows from
  two one-sided statements C1(n), C2(n)); PROVED. V2 CONFIRMED 17:13
  ([VERIFY_P1_CUPEXT.md](../DELTA3N20261113/attack20261115/VERIFY_P1_CUPEXT.md)); V2 notes that SD never applies to the
  known sets (each has an (n−1)-cup).
- `p2-lemma-a` (P2): Lemma A (a gon whose leftmost point ends a 4-cap has an upper chain of 3 or 4 points, and more)
  with corollaries; PROVED. V3 CONFIRMED 17:17 ([VERIFY_P2_LEMMA_A.md](../DELTA3N20261113/attack20261115/VERIFY_P2_LEMMA_A.md)).
- `p2-witness-refutations` (P2): four explicit-witness strengthenings of LP0 (H4, H2, H5U, H6) are false for real point
  sets of 14-25 points (EXACT). V2 CONFIRMED 17:15
  ([VERIFY_P2_REFUTATIONS.md](../DELTA3N20261113/attack20261115/VERIFY_P2_REFUTATIONS.md)).
- `h7u6-m12` (P2): H7U(6) (if some convex pentagon of U consists of 4-cap end points of U, then U has an ENV# Δ) holds
  at 12 points, CERTIFIED; with ENV#(6) ≤ 11 it holds for \|U\| ≤ 12. V2 CONFIRMED 17:18 (own cake_lpr re-run, 16/16
  semantic controls; [VERIFY_H7U6_M12.md](../DELTA3N20261113/attack20261115/VERIFY_H7U6_M12.md)). H7U(7) is false at
  \|U\| = 18 (abstract; `lp0-7-false-abstract` above).
- `p1-lemmaq` (P1): Lemma Q (with no 5-cap, Q0 together with the top β-level contains no 4-cap; mirror likewise);
  PROVED, with an EXACT negative companion (on T4's 10-point TRIV(6) model neither set meets every pentagon, so Lemma Q
  alone gives no weak Δ through r or l). V3 CONFIRMED 17:26
  ([VERIFY_P1_LEMMAQ.md](../DELTA3N20261113/attack20261115/VERIFY_P1_LEMMAQ.md)).
- `p1-c2six` (P1): **C2(6) holds for every signotope, hence every point set**: if r ends a 4-cap and lies in no weak Δ,
  then l starts a 5-cup (the CNF does not assume that l starts a 4-cap). One UNSAT CNF at 15 points; ≤ 14 by ROOT(6),
  ≥ 16 vacuous. V1 CONFIRMED 18:19 at the label COMPUTED (V1 could not run cake_lpr); the main session's cake_lpr run
  at 18:20 (heap 1,500 MB, 27 s) printed the exact line with the claimed LRAT hash, which makes it CERTIFIED
  (MAINSESSION_1115PM.md, last section; [VERIFY_P1_C2SIX.md](../DELTA3N20261113/attack20261115/VERIFY_P1_C2SIX.md)).
  C2 is one half of P1's reduction C1(n) ∧ C2(n) ⟹ LR(n); C1(6), C1(7) and C2(7) are open.
- `p1-lemmae` (P1): Lemma E (a cup ending at a point that starts a 4-cap extends; longest cups end in Q0) and
  "C2* ⟹ C2", PROVED; and a counterexample to P1's own conjecture ISO-ROOT (a weak Δ through r with non-decreasing
  β-values) on a real 17-point (5,8)-valid prefix, EXACT. V2 CONFIRMED 17:44
  ([VERIFY_P1_LEMMAE.md](../DELTA3N20261113/attack20261115/VERIFY_P1_LEMMAE.md)).

#### Open (no verdict; labels of the partial evidence as stated)

- **LR(7)**: CERTIFIED ≤ 14. At 15: CaDiCaL UNSAT (T1, 7,857 s; LRAT 23.7 GB, kept as zstd) but cake_lpr ran out of
  heap at 1,150 MB, so **COMPUTED** until a run with a heap of about 4,000 MB or more. 16: run stopped at 15:20 after
  64 min. 17: SAT-mode searches found no model, which proves nothing (T3: 2,496 s; T1: 15:23-17:16 with phases from the
  real ROOT(7) set and 16:38-17:00 from its mirror; T1 final status 18:22). Gluing probes: T3's interleavings of 1 or 2 points left of
  r in the three 17-point blocks, all UNSAT (COMPUTED); T3's left-of-l tests are vacuous by `leftsat-r7blocks`; P2's
  CEGAR over every valid 2-point extension pattern of the 10 blocks (1,360 patterns) found no extension with l in no
  weak Δ (COMPUTED, not filed; PROOF_LP0_ATTEMPT_P2.md item 6).
- **TWO-ENV#(7)** (T4's top candidate now, per PROBES): CERTIFIED ≤ 14 (from ENV#(7) ≤ 13). At 15, **both
  certification runs ended without a verdict**: T3's encoder at its 5,400 s wall limit (17:33, about 4,600 CPU-s) and
  T4's encoding at its 3,800 s wall limit (17:07); T3 deleted both partial LRATs. At 17, where ROOT(7) fails, T3's
  SAT-mode search (`cnf/te7_m17.cnf`, 17:07-18:12) stopped at its wall limit without a verdict (3,895 CPU-s; UNKNOWN).
- LP0(6) at 15 (decides LP0 at n = 6): T4's SAT-mode probe found no model in 221 CPU-s (HEURISTIC). DEPTH(6) at 15:
  no model in 190 CPU-s, stopped.
- ROOT(7) at 15 and 16 (R7, final status 18:05; all R7 units stopped): the best real 16-point sets found have 4 rooted Δs (two independent
  descents, HEURISTIC search; counts confirmed by `exact17.py`); no single deletion of either real 17-point set is a
  counterexample (EXACT); no abstract 16-point counterexample lies within Hamming distance 40 of root7_real17 − point 4,
  nor within 48 of the 9-Δ and the 4-Δ sets (COMPUTED, no proof); blind CaDiCaL runs on `root7_m16.cnf`: no verdict.
- ENV#(6) at \|U\| = 12, 13; ENV#(7) at 14, 15; CB(6) at 14, 15; CB(7) at 14-36 (window 14-31); CB(8) from 16
  (window 16-58); CONJ-TS′(7) at 15, 16; weak D(4,8) at 17-22; weak D(5,7) from 16 (CERTIFIED ≤ 15, DELTA2N).
- Proof attempts (wave 2; status lines read at 18:06):
  - [PROOF_LR_ATTEMPT_P1.md](../DELTA3N20261113/attack20261115/PROOF_LR_ATTEMPT_P1.md) (P1, read at 18:06): "LR(7)
    remains OPEN; no proof of LR(n) for any n ≥ 7 is claimed". New CONJECTUREs C1(n) ("if r ends a 4-cap and an
    (n−1)-cup, r lies in a weak Δ") and C2(n); together they give LR(n) (Prop. R, PROVED). Both hold on all 110 known
    order types and in a scan of 738 (n, type) pairs (EXACT); no counterexample in the neighbourhood of any known rooted
    failure (75,740 SAT calls, COMPUTED); C2(6) is now CERTIFIED (`p1-c2six` above), C1(6) had no model at 15 points
    in 180 CPU-s (HEURISTIC). A further
    CONJECTURE, STAIR-LR(n) (a β-staircase through r or an α-staircase through l is a weak Δ), implies LR(n) and holds
    on every tested set (EXACT). P1's normal form ISO-ROOT is refuted (`p1-lemmae`). The gap: no mechanism is known
    for C1 or C2.
  - [PROOF_LP0_ATTEMPT_P2.md](../DELTA3N20261113/attack20261115/PROOF_LP0_ATTEMPT_P2.md) (P2, final status 17:50): LP0(7)
    is false for signotopes (above); "No proof of LP0(6), LR(7) or weak D(5,7)". LP0(6) stays open only at 15 points
    (the 2-point construction has no room at n = 6). P2's
    conjecture H7 (if some gon of S consists of 4-cap end points, then S − r has an ENV# Δ; it implies LP0) and its
    U-only half H7U are refuted at n = 7 by the same sets; H7U(6) is CERTIFIED for \|U\| ≤ 12, and a SAT run at 13-14
    was in progress. Five explicit-witness strengthenings of LP0 are refuted (EXACT; four in a confirmed claim).

T4's assessment (THEORY_1115PM.md §4, v6 16:55): the Δ route is alive as a research program with the sharper targets
LR(n), TWO-ENV#(n) and LP0(n), each PROVED to imply weak D(5,n); as a route to an ES(8) bound in the near term it is
not (weak D(5,8) would give ES(8) ≤ 303, weak D(5,7) 298). Since 17:26, LP0(7) is false for signotopes (abstract;
open for point sets), so of the three targets only LR(n) and TWO-ENV#(n) are unrefuted at n = 7, both open from 15
points (LR(7) at 15 is UNSAT by CaDiCaL, COMPUTED only; the counterexample searches for both at 15-17 ended without a
model).

**What the Δ route can give ES(8)** (W1, [LEDGER_1115PM.md](../DELTA3N20261113/attack20261115/LEDGER_1115PM.md), final
status 17:13):
- It re-derives ES(8) ≤ 189 + N5 + N66 ≤ 245 + N5 (PROVED from Lean-checked, CERTIFIED and PROVED inputs) and confirms
  the bounds of THEORY §2.3: weak D(5,8), LR(8) or T(8) give 303; with weak D(5,7), 298; CB(8) 302; each one less once
  N66 ≤ 55.
- Size relevance (PROVED, elementary): for ES(8), weak D(5,8) is needed only for 59-point sets, where it is equivalent
  to N5 ≤ 58; small-size certificates carry no ES(8) information by themselves. The weak D(5,8) counterexample window
  moved from 16-59 to 17-59 today (`wd58-m16`); weak D(5,7) stays 16-32.
- No computational path (HEURISTIC costs): weak D(5,8) at 17 would need about 20-28 CPU-h and an LRAT of about
  95-110 GB; 18 is beyond the disk. The omission route is the only route to 307 with a cost basis.

### ES(8) upper bound

- **ES(8) ≤ 308**: unchanged. Computer-assisted, unrefereed, uncommitted. See the
  [budget34](../LO33N20261113/budget34/README.md) headline and [VERIFY308](../LO33N20261113/budget34/VERIFY308/README.md).
- **Toward 307** (budget 35, cases (F,Lo) = (18,17), (19,16), (20,15), (21,14)):
  - (18,17) and (19,16): EXACT TREE, as before.
  - **(20,15)** ([ADDENDUM_1115PM.md](../LO33N20261113/budget34/ADDENDUM_1115PM.md), U2): loop v10b in unit
    `esr-lo-b35s20v10b`, 4 threads, 13:12-18:40.
    - **Final, 18:40: 998 of 8,065 contexts closed** (555 at 09:35; 993 at 17:46). The unit ended with result success.
      The last event is `FINISHED` at 18:39:42: the round-144 finder `c143s1` reached the deadline without a witness.
    - Rounds 139-143 appended 80 rows in 10 batches. U2 audited every batch with the morning's audit script, one unit
      per batch: **80/80 CERTIFIED** (own encoder hash, fresh cake_lpr exact line, each row cuts its witness). U2's own
      read-only cross-check of the appends found no failure (80 rows, 10 batches; 17:45).
    - (20,15) now has **507 CERTIFIED coupled rows in 53 batches** (427 in 43 at 09:35); the newest input
      `b35s20-v143` has 4,179 rows. The finder of round 144 (`c143s1`) started at 17:45.
    - (20,15) is not closed, so ES(8) ≤ 307 is not reached.
    - **Resume:** the last `round` event is version 142 (receipt `runs/b35s20/c142s1.json`), and it was appended as
      `b35s20-v143`. By the ADDENDUM's rule, resume with `--start-version=143` and no receipt; the other options are as in
      the ADDENDUM's command line. Better first: apply A2's skip-list proposal.
    - **Throughput finding (A2, [ANALYSIS_1115PM.md](../LO33N20261113/budget34/ANALYSIS_1115PM.md), COMPUTED /
      HEURISTIC).** The harness refused A2's own write; the main session saved A2's returned text unchanged at 18:40.
      - Every finder start re-attempts all known too-big contexts from context 0. In the afternoon rounds that took
        43-47 min of each 63-81 min round, about two thirds of the finder's thread time.
      - Skipping known too-big contexts (fastbb2 already has `--ctx=`) and adding one worker without the low cap would
        need about 17.5 h at 4 threads, or about 6 h at 12, plus 20-25 thread-hours for the hard contexts (A2 §4-§5).
  - (21,14): untouched. It needs N66 ≤ 55 or a tree of its own.
- **N66 ≤ 55: NOT decided; N66 ≤ 56 (level 13, CERTIFIED) stays.**
  - The level-14 cube campaign resumed at 13:12 (driver copy r2, 4 slots) and at 13:57 (`p2c14_driver_r3.py`, at most 5
    cube units of 1 thread, MemoryMax 4.1G, no cube starting after 18:44 − 900 s). Live page:
    [STATUS_campaign.md](../N66N20261113/cubes20261115/STATUS_campaign.md).
  - **Final, 18:40:33** (driver end, `campaign_status.json` final = True): **102 leaves, 79 CERTIFIED, 23 open**.
    - 38 cubes have been split since 05:50 after reaching their time limit, 32 of them this afternoon; the two
      children of a split cover the parent.
    - Leaf cover: COVER_OK. The certified leaves do not cover the split. No cube was SAT.
    - Open leaves by number of holes: 0 holes 1, 1 hole 6, 2 holes 13, 3 holes 3.
  - Main session's count from the same file (exact fractions): **44 of the 64 base cubes are fully certified; the
    certified leaves cover 25/32 = 78.1 % of the split by measure** (09:29: 32 of 64, 50 %; 16:59: 181/256 ≈ 70.7 %).
  - **Independent verification (U1, [VERIFY_N66CUBES.md](../N66N20261113/cubes20261115/VERIFY_N66CUBES.md), final status
    18:23, U1 stopped): 76 of the 76 cubes then certified pass all four checks with U1's own code** (the 3 cubes certified after 18:23,
    hohooo_23h, oooohh_23o and one more, still need these checks): a fresh cake_lpr run with the exact
    line and input hashes equal to cert.json; trim.cnf ⊆ cert.cnf; cert.cnf = F_c plus exactly the cube's unit clauses;
    every trim.cnf clause generated by own code, rows re-justified with own code. Discrepancies: none.
  - **Cost (HEURISTIC; A1, [ANALYSIS_1115PM.md](../N66N20261113/cubes20261115/ANALYSIS_1115PM.md), data of 16:57).** The
    harness refused A1's own write; the main session saved A1's returned text unchanged at 18:40.
    - A "band" rule, computable before a run, sorts the cubes by cost. In full 1,200 s runs: band ≤ 2 certified 17 of
      17; band 3, 31 of 33; band 4, 9 of 25; band 5, 0 of 3.
    - Each 'o' re-split cuts the conflicts needed by about ×0.77, and an 'h' re-split lowers the band by one.
    - **The current strategy needs about 210-325 more slot-hours** (about 42-65 h at 5 slots). This replaces the
      morning's 20-60 CPU-h estimate. The 5 open band-6/7 cubes (four 1-hole cubes with 37 occupied, and oooooo) carry
      55-75 % of it.
    - A1's proposals for the next session are in its §5.

### ES(8) lower bound

- **ABSAT8 independent encoder (L1, [ABSAT8_INDEPENDENT.md](../ROADMAP20261115/ABSAT8_INDEPENDENT.md), final 14:21).**
  - **28 sets** (the 8 vertex deletions of AlphaEvolve's 65-point set, 17 pilot sets, walker end sets w1-w3): the
    independently written encoder's 28 CNFs are UNSAT, CERTIFIED (cake_lpr exact line 28/28), with a PROVED soundness
    argument (§3). So, computer-assisted (CERTIFIED computation + PROVED soundness): for each of these 28 order types,
    adding any point in general position to any realization creates a convex octagon through it. This replaces this
    morning's COMPUTED label for the geometric reading. Claim `absat8-l1-indep`: V1 CONFIRMED 13:54 (proof read by
    hand, own C++ regeneration equal as clause sets 28/28, 32 exact real-point samples; no cake re-run). Claim
    `absat8-l1-cake-rerun`: V3 CONFIRMED 14:01 (own cake_lpr re-run 28/28). Controls 933/933. Reports
    [VERIFY_ABSAT8_INDEPENDENT.md](../ROADMAP20261115/VERIFY_ABSAT8_INDEPENDENT.md),
    [VERIFY_ABSAT8_CAKE_RERUN.md](../ROADMAP20261115/VERIFY_ABSAT8_CAKE_RERUN.md).
  - **7 more sets: the seven 7-fold 64-point order types of PRIMEFOLD §3** (8 CNFs; two files have the same labelled
    chirotope): exact chirotopes (EXACT), CERTIFIED 8/8, same soundness. None of these seven order types has a
    realization that extends to a 65-point octagon-free set in general position. Claim `absat8-l1-sevenfold`: V3
    CONFIRMED 14:19 (own exact chirotope, own encoder, own cake re-run). Report
    [VERIFY_ABSAT8_SEVENFOLD.md](../ROADMAP20261115/VERIFY_ABSAT8_SEVENFOLD.md).
  - Scope: these 35 order types only. Nothing follows about ES(8) = 65 beyond them.
- Not run this afternoon: the k = 9 ring (no k9 unit in the memory-guard log; this morning's counts stand: 155 of 175
  cyclic and 2 of 95 linear cases CERTIFIED) and any ES(7) experiment.

## Corrections made today

1. **ROUND6 statement 12 range.** "494 to 12,176 weak Δs per set" was wrong: d6_12 has exactly 486, so the range over
   the 12 AT_n realizations is **486 to 12,176**. A summary slip (the round-6 verifier's own output already said 486); no
   conclusion changes. Claim `d6-12-correction` (T5), V3 CONFIRMED 13:30;
   [D6_12_NOTE.md](../DELTA3N20261113/attack20261115/D6_12_NOTE.md). The repo copy of
   [ROUND6.md](../DELTA3N20261113/attack20261115/ROUND6.md) carries the correction (statement 12 in line 193 and the
   closing section "Correction, 15 November 2026 afternoon (main session)"). The work copies
   `round6/writeup/ROUND6.md:193`, `round6/writeup/ROUND6.tmpl.md:172` and `round6/vatn/VERIFY_ATN.md:136` still say
   494 (17:03).
2. **ROOT6_MAIN.md.**
   - Encoder hash: the record cited `927e25b4…` (the hash of `round6/atn/realize_sig.py`) as the hash of the encoder;
     `root_cnf.py` is `aef1af7a…`. V3 found it (verdict on `root6-m15-abstract`); corrected 13:30.
   - m = 16: the record called sizes 15 and 16 open and planned m = 16 by cubes (about 11 h). Size 16 is vacuous (no
     (5,6)-valid signotope has 16 points), so that run was never needed. T4's claim `root6-m16-vacuous`, V1 CONFIRMED;
     correction section added 14:20. C1 notes that the old Status lines at the top are still not marked superseded in
     place, and that line 93 says "13 further" real sets where there are 20 further (21 in all).
3. **The main session's briefing error.** The task background given to the agents said that every abstract signotope on
   at most 8 points is realizable. That is false for x-sorted realizations: an 8-point signotope plus the vertical point
   at infinity V is a 9-element chirotope, and T1 found an 8-point sub-signotope of `root6_m15` that with V has a BFP
   certificate (23 inequalities, all multipliers 1; claim `root6-m15-main-nonrealizable`, V2 CONFIRMED 13:50). The safe
   statement is "at most 7 points" (Goodman–Pollack; V2 notes that this rests on the literature and was not checked).
   [ROOT6_M15_REALIZE.md](../DELTA3N20261113/attack20261115/ROOT6_M15_REALIZE.md), "Correction to the task background".
4. Smaller corrections found by verifiers, W1 and C1 (most were **not yet applied** to the records at 18:20; C1 issue
   numbers refer to its FINAL list of 18:12):
   - CONJ-TS′(7): the least real counterexample has 15-17 points, not 15-19. V1 found that
     [S19_REALIZABILITY.md](../DELTA3N20261113/attack20261115/S19_REALIZABILITY.md) line 23 and
     [CONJTS_TEST.md](../DELTA3N20261113/attack20261115/CONJTS_TEST.md) lines 27 and 352 still say 15-19.
   - Hypothesis dropped: THEORY_1115PM.md (and T4's `candidates.md` K2′) state TWO-ENV#(6) and TS±(6) ≤ 14 for every
     valid S, but the certificates cover only the form with "r ends a 4-cap and l starts one" (C1, issue 3). No
     conclusion changes, since weak D needs only that form.
   - Stale verdict states: MAINSESSION_1115PM.md, PROBES_1115PM.md, THEORY_1115PM.md and some VERIFY files still say
     NOT CONFIRMED for `lr6-m15-second`, `tspm6-14` or `wd58-m16` after V2's 16:53 updates (C1, issue 4); PROBES'
     claim column and ROOT6_M15_REALIZE.md's results table show older states (C1, issues 8 and 11).
   - THEORY_1115PM.md calls LR(6) and TWO-ENV#(6) "theorems"; they are CERTIFIED plus a PROVED combination,
     computer-assisted and unrefereed (C1, issue 7). Its afternoon paragraph still says LP0 "survives everywhere",
     although the same file now reports LP0(7) false (abstract), and it extends "exactly one unrootable point" and "P0
     is a weak Δ" beyond the sets where they were checked (C1, issue 1).
   - PROBES_1115PM.md lists TS±(6) realizability and LP0(7) as open; both were decided by CONFIRMED claims
     (`tspm6-real-15`, `lp0-7-false-abstract`), and its "T1 is certifying LR(7) at 15 (and 16)" is stale (C1, issue 2).
   - ROOT7_M17_REALIZE.md's LP0 section reports an LP-slack cell test without a label (it is a search, HEURISTIC) and a
     BFP certificate without a hash or claim id (C1, issue 9).
   - The index's afternoon section (README.md, 17:59) overstates the verification: not every new result has a
     verdict (unfiled EXACT items such as T1's further real 15-point sets; the ROOT(6) m = 7-14 proofs were never
     filed), and not every large proof was re-run by a second party (T1's base(5,6,16) proof, the ROOT(6) m = 7-14
     proofs) (C1, issue 6).
   - C1, issue 7b: `leftsat-r7blocks` covers the 10 blocks it names; three further known right-hostile blocks were not
     tested, so "all known blocks are left-saturated" (index, THEORY) says too much.
   - The full list, with file and line numbers, is C1's ISSUES.md (FINAL 18:12; issues 1-20).
   - W1: THEORY §1.1 still says "17-59 once wd58-m16 is confirmed" (it is), and `cb78-from-strong` and
     VERIFY_CB78_FROM_STRONG.md understate the open CB ranges ("CB(8) at 16-22, CB(7) at 14-15"); see `w1-cb-window`.
   - ABSAT8: the 14:08 version of the record said "V1 CONFIRMED" for the seven-fold claim before any verdict; the author
     corrected it at 14:12 (V3's verdict).
   - `t4-lemmas`: the proof of L4's last clause omitted one case; the wording fix is in THEORY_1115PM.md §2.2, Cor. 3
     (V2). Applied.
   - [ROADMAP20261115/README.md](../ROADMAP20261115/README.md) lines 99-102 still call the ABSAT8 geometric reading
     COMPUTED "until the soundness note and an independent encoder exist"; both now exist.
   - The attack20261115 index README.md still calls the d6_12 count "unresolved" in its morning part (line 108); its
     17:59 afternoon section marks that line superseded.

## Owner decisions waiting (nothing below was done)

1. Commit, push or publish ES(8) ≤ 308, the 14-15 November records and today's records (`git status`: the new record
   folders and files are untracked). (From this morning.)
2. Delete partial LRATs; none of them is a proof. This morning's list is unchanged: N66 level-14
   `n66-20261113/p2/b14h2|b14i2/it1/cert.lrat` (28G each by du at 17:00); m = 9, 70 GB;
   `roadmap-20261115/delta-r2-attacker/cert14/ts7_N14.lrat`, 4.7 GB; `roadmap-20261115/conjts/runs/n7_m15/cts_n7_m15.lrat`,
   22.9 GB. **New this afternoon (kept, none is a proof):**
   - **N66 partial files of timed-out cubes.** Unlike this morning's driver, the r2/r3 drivers keep the partial
     `cert.lrat` and `cert.cnf` of every cube that reaches its time limit. Final, 18:41: 32 split cubes, 64 files,
     **123.1 GB** (bytes), under `n66-20261113/p2/c14/<id>/it*/` (at 18:19: 102G by du; at 17:00: 69G).
   - T1: `pm1115/t1/lrr7/cert16/lrr7_m16.lrat`, 8.2G by du (8,779,448,320 B), from the LRR(7) m = 16 run stopped at 15:20
     (ROOT6_M15_REALIZE.md: "may be deleted with the owner's OK").
   - V1: `pm1115/v1/root6-m16-vacuous/cert_cubes/cube_ppp.lrat.PARTIAL-stopped-not-a-proof` (424M) and
     `…/cert/root6_m16_base_prefix.lrat.PARTIAL-stopped-not-a-proof` (74M).
   - Main session: `round6/mainsession/te6recake.partial-1606/` (44K), the stopped first re-run attempt.
   - P2: `pm1115/p2/h7u/cert/h7u6_m13.lrat`, 1,455,251,456 B, from its H7U(6) m = 13 run, which received SIGTERM at
     17:37 without a verdict (kept at 18:06).
   Disk: 646G free at 18:41 (654G at 18:19; 690G at 17:00; 852 GB this morning); `n66-20261113/p2/c14` alone holds 211G
   at 18:41 (203G at 18:19; 155G at
   17:00).
3. Repository cleanup: paused at "who is the cleaned-up repository for, and what should they be able to do?". (From
   this morning.)
4. Deletions of fresh partial files that were already done; please say whether these are acceptable in future. This
   morning: the N66 driver deleted 19.64 GB of partial cert.lrat/cert.cnf of its own timed-out cubes, and the main
   session deleted three partial ROOT(6) LRATs (172 MB, 103 MB, 39 MB). **This afternoon (agents only; none of these
   files was a proof):**
   - V2 deleted the partial LRATs of its own two stopped CB(6) m = 13 runs: `cert/v2cb6_m13.lrat`, 285,925,376 B
     (14:36), and the next attempt's partial LRAT (15:02; size not recorded: unclear, see `pm1115/v2/verdicts.log` and
     [VERIFY_CB6.md](../DELTA3N20261113/attack20261115/VERIFY_CB6.md)). Their logs are kept (`*.stopped-1435`,
     `*.stopped-1502`).
   - T4 deleted the partial LRAT of its CB(6) m = 14 run, stopped at 14:12:25 (size not recorded: unclear, see
     `pm1115/t4/cb/progress.log`).
   - T3 deleted the partial LRATs of its two TWO-ENV#(7) m = 15 runs that ended without a verdict: `cert/te7/te7_m15.lrat`
     (12.5 GB per PROBES_1115PM.md; ended 17:33) and `cert/t4te7/twoenv7_m15.lrat` (ended 17:07; final size not
     recorded: unclear, see PROBES_1115PM.md; D1's listing showed 7,606,837,248 B at 16:59 while it was still being
     written).
   - V3 deleted the partial outputs of a mistyped unit launch that it stopped within seconds
     ([VERIFY_TWOENV6_13_14.md](../DELTA3N20261113/attack20261115/VERIFY_TWOENV6_13_14.md)).
   - Verifiers (V1, V3) deleted their own decompressed copies of `.zst` proofs after checking them; every `.zst` is kept.
   - The main session deleted nothing: its nine cake_lpr runs streamed the proofs through FIFOs.
5. **New LRAT proofs on disk this afternoon** (du at 17:03-18:06; kept as zstd unless noted). The house rule keeps a
   proof until an independent check has re-run it; no deletion is proposed.
   - Re-run by a second party (main session, V2 or V3): T1 `lrrcert/cert/lrr6_m15.lrat.zst` 847M; T3
     `cert/tspm6/` 134M + 576M, `cert/t4lr6/` 834M, `cert/te6/` 115M + 527M + 854M, `cert/wd58/` 1.2G, `cert/env6/`
     20M, `cert/t4te6/` 888M (second TWO-ENV#(6) m = 15 certificate, 18:01); T4 `cb/cert/` 251M; L1 `cert/` + `cert7/`
     1.3M (36 proofs); P2 `h7u/cert/h7u6_m12.lrat.zst` 50 MB and `leftsat/cert/` 3.6M (10 proofs; 17:13-17:32); P1
     `c2_nolcup6_m15.lrat.zst` 429,401,302 B (C2(6); its only completed cake_lpr run is the main session's, 18:20).
   - Certified by the producing agent only: T1 `base16/cert/valid56_m16.lrat.zst` 282M (base(5,6,16)); V1
     `cb78-from-strong/cert/` 158M (V1's own strong-form CNFs); V2 `cb6-le13/cert/` 256M and `env6-le11/cert/` 21M (V2's
     own encoders); V3 `leftsat-r7blocks/` 46M (V3's own left-saturation CNFs, 10 proofs).
   - **Not certified** (cake_lpr ran out of heap): T1 `lrr7/cert15/lrr7_m15.lrat.zst` 5.0G (LRR(7) at 15, LRAT 23.7 GB);
     V1 `root6-m16-vacuous/cert/v1_base_m16.lrat.zst` 268M (V1's lemma-free base(5,6,16), LRAT 904 MB).
   - N66: the trimmed LRATs of all certified cubes, 29G, and their zstd copies, 6.4G (du at 17:00, then 65 cubes,
     including this morning's) (du at that time; not refreshed at 18:41); U1 re-ran cake_lpr on every cube certified by 18:23 (76).
   - (20,15): the folders of the afternoon batches, `es308-20261114/cuts-v139w1u` … `cuts-v142w2u` (8 batches), 515M by
     du (64 row LRATs, 151.9 MB by byte count; 17:12), plus the two v143 batches of 17:45 (du at that time; not refreshed at 18:41); U2's audits
     re-ran cake_lpr on all rows.
6. (This morning's item 5, unclear whether still relevant: the runtime CPU cap of the morning terminal, CPUQuota 800 %,
   lapses when that terminal closes.)
7. C1 lists one more as an owner decision on memory: a cake_lpr run with a 4-6 GB heap on T1's 23.7 GB LRR(7) m = 15
   proof (Resume item 3). With a unit of about 5.6 GB or more it stays inside the 24 GB total and the per-job sizing
   rule; this morning's weak D(4,8) re-run used a 6 GB heap (STATUS20261115_1000).

## Resume, in order of value

1. **N66 cube campaign** (the critical path to 307: it removes (21,14)).
   - Driver `n66-20261113/p2c14_driver_r3.py`; its deadline (18:44) is hard-coded, so make a copy with a new deadline,
     as this morning (PROGRESS.md §10). State in `p2/c14/campaign_status.json`: 23 open leaves at 18:40 (holes 0/1/2/3: 1/6/13/3).
   - Before resuming, read A1's band rule and proposals ([ANALYSIS_1115PM.md](../N66N20261113/cubes20261115/ANALYSIS_1115PM.md)):
     at the current strategy the remaining cost is about 210-325 slot-hours (HEURISTIC).
   - Decide first whether the partial files of timed-out cubes are kept (Owner decisions, item 2); at about 3.6G per
     timed-out cube (du at 18:19) they are the largest new disk use.
   - A1's cost analysis was not available at 18:07 (see above), so the remaining cost has no record-based estimate
     beyond the morning's 20-60 CPU-hours for the whole campaign (HEURISTIC, SYNTHESIS).
   - U1 stopped at 18:23 with 76 of 76 checked, so cubes certified after that still need its four checks: commands in
     VERIFY_N66CUBES.md §7.
2. **(20,15)**: resume rule in ADDENDUM_1115PM.md §Resume: if the last `round` event (version V, receipt R) has no later
   append, `--start-version=V --start-receipt=R`; if it was appended as V+1, `--start-version=V+1` without a receipt.
   Other options as in the ADDENDUM's command line. Then merge the ADDENDUM into the budget34 README (not edited by U2).
   Final: the last `round` event is version 142, and it was appended as `b35s20-v143`, so resume with
   `--start-version=143` and no receipt. First apply A2's skip-list proposal ([ANALYSIS_1115PM.md](../LO33N20261113/budget34/ANALYSIS_1115PM.md) §5).
3. **Δ, cheapest first:**
   - cake_lpr on T1's LRR(7) m = 15 proof (`pm1115/t1/lrr7/cert15/lrr7_m15.lrat.zst`, 23.7 GB unpacked) with a heap of
     at least 4,000 MB; T1's command uses 4,500 MB (ROOT6_M15_REALIZE.md, "What remains"), which by the 80 % sizing rule
     needs a MemoryMax of about 5.6 GB or more; stream it through a FIFO as the main session did. A pass makes LR(7)
     CERTIFIED for \|S\| ≤ 15.
   - TWO-ENV#(7) at 15: both LRAT runs gave no verdict in 3,800-5,400 s of wall time, so it needs a longer run or
     cubes. The m = 17 SAT search also ended without a verdict (18:12).
   - Missing second-party cake_lpr re-runs (C1, open items): the main session's ROOT(6) m = 7-14 proofs
     (`round6/mainsession/root6/cert/`; LR(6) ≤ 14 and "ROOT(6) is decided" rest on them; only their verdict lines and
     CNF regeneration were checked); T1's base(5,6,16) proof (heap 1,150 MB, 29 s; every "≥ 16 is vacuous" step rests on
     it); V1's lemma-free base(5,6,16) LRAT (needs more than 300 MB of heap). The DELTA2N proofs of strong (5,8) at 15
     (CB(8) at 15) and of base(5,6,16) were deleted and can only be re-solved.
   - LR(7) or TWO-ENV#(7) at 16, or weak D(5,7) at 16 directly (`t3/cnf/wd57_m16.cnf`): any of them extends weak D(5,7)
     to 16 points.
   - LP0(7) for point sets: all 108 models of P2's 2-point scan are non-realizable and R7's direct real search found
     nothing. R7's record ("What remains") notes that the scan kept one model per pattern and suggests a CEGAR over P2's
     extension CNF with BFP cuts; larger extensions and other blocks were not tried.
   - ROOT(7) at 15 and 16: the abstract m = 16 CNF is undecided after about 53 CPU-min of blind CaDiCaL; R7 stopped its
     m = 16 searches at 17:26 (ROOT7_M17_REALIZE.md, "What remains").
   - LP0(6) at 15 (decides LP0 at n = 6); CB(6) at 14, 15; ENV#(6) at 12, 13; weak D(4,8) at 17.
4. **Lower bounds**: E7's ranked plan [LOWERBOUND_PLAN_1115PM.md](../ROADMAP20261115/LOWERBOUND_PLAN_1115PM.md) (a plan,
   no result) recommends a first block of four experiments, ABSAT8 sweep 2 (E8-1), ABSAT7 (E7-1), the CONE4 gate (E8-2)
   and a (7,6,6)@31 seed miner (E7-3), about 5-7 CPU-h in all (HEURISTIC). The k = 9 ring (E8-4 there) is unchanged
   since 09:40: `k9/tools/sched.py` with env `MAXJOBS`, `MEMB`, `SOFT`, `HARD`, in a unit; `k9/queue.txt` holds the
   remaining list.
5. **Record hygiene**: the corrections of Corrections item 4 and C1's final list; merge the afternoon status into the N66
   PROGRESS.md and the budget34 README (the attack20261115 index got its afternoon section at 17:59).

## Process notes (the main session's own slips first)

- **Thread cap.** The summed CPUQuota of active `esr-*` units went over 16 threads, briefly: 16.46 at 16:05:16 and
  16.11 at 16:10:17 (the main session's watcher), both in the minutes when the main session started its TWO-ENV#(6)
  re-run units (16:05-16:10). These were the main session's slips. A third excursion, to 16.41, came when it started
  the second TWO-ENV#(6) re-run at about 18:02; it then cut that unit from 100 % to 25 % CPU
  (MAINSESSION_1115PM.md, last section).
- **Memory-guard stop caused by a job name.** The main session named its first TWO-ENV#(6) re-run unit
  `esr-vfy-main-te6` (16:05). The `vfy` prefix put it into the track budget that U1's units share (3,500 MB), so at
  16:05:17 the guard stopped U1's unit `esr-vfy-u1-cake-ohhhoo_23o_49o_44o` cleanly (track 3,511 MB; no OOM kill). U1
  re-ran that cube at 16:10 and it passed; U1's units now wait for room in the track. The main session moved its re-run
  to `esr-mainv-te6`; the stopped attempt is in `te6recake.partial-1606/`.
- **Duplicate V2.** A message from the main session to a workflow agent started a second V2 instance. Both worked under
  the name V2 and shared one budget (15 % CPU, 0.4 GB); the first one noticed at 15:37 and wrote
  `pm1115/v2/COORDINATION.txt`. Each claim still has exactly one verdict file.
- **Verifier budgets were too small for cake_lpr on proofs over about 1 GB.** The verifiers had about 0.4 GB each. At
  heap 300 MB cake_lpr accepted LRATs up to 846 MB (V2 on `cb6_m13`) but ran out of heap on 1.82-3.52 GB LRATs (V2 on
  `tspm6_m14` and on the second LR(6) proof, V3 on `te6_m14`; V1 at 250-300 MB on its own 904 MB LRAT); V1 did not try
  the 2.95-3.62 GB proofs at all. So the main session ran cake_lpr on nine proofs in its own units (heap 1,400-2,000
  MB, proofs streamed through FIFOs): `lrr6_m15` 14:19-14:21, `tspm6_m14` 14:45-14:46, `t4_lr6_m15` 15:06-15:08,
  `te6_m13|14|15` 16:06-16:16, `wd58_m16` 16:19-16:23, `twoenv6_m15` (T4's encoding) 18:02-18:11 and P1's
  `c2_nolcup6_m15` at 18:20 (27 s; P1's own run at heap 480 MB had not finished). Measured where recorded: LRATs of
  2.3-5.6 GB needed peak RSS 1.44-2.06 GB and 1.5-9 min each. V2 and V3 then checked those re-runs; C1 found the first
  seven re-run folders with exactly one `s VERIFIED UNSAT` line and hashes equal to the claims.
- **Time fields.** Several agents wrote `time` fields or status lines ahead of the clock (T4's claims by 12-21 min, V1's
  verdicts by up to 14 min per C1; W1's claim says 17:50 for a 17:07 filing, as W1 notes). This page uses file times.
- Smaller items from the records:
  - CaDiCaL's `-t` limit counts wall-clock time, so SAT probes run at 50 % CPU got half the CPU time they were given
    (PROBES_1115PM.md).
  - V3 launched one unit with a mistyped (non-ASCII) name and stopped it within seconds.
  - The N66 cube units ran at MemoryMax 4.1G; their peaks this afternoon reached 3,196 MB (STATUS_campaign.md), with no
    guard stop and no OOM. (This morning they had reached 85-88 % of a 3,686 MiB limit.)
