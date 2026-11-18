# ES(7) feasibility study: what a brute-force proof of ES(7) = 33 would cost (15 Nov 2026, written 05:45 KST)

**Status: a costed plan, not a result.** Every cost figure below is HEURISTIC. The only EXACT parts are the CNF sizes
and hashes. All solver verdicts are COMPUTED, and none is CERTIFIED. Nothing here proves or refutes ES(7) = 33.

This is section 3's "costed feasibility study" from `README.md`. It was written by the night workflow's study agent
(work notes: `/home/jay/research/data/roadmap-20261115/es7feas/README.md`). An adversarial critic then checked it, and
the numbers below already include the critic's corrections (§2). No repo file was changed, no git was used and no new
compute was run for this write-up.

## 1. Bottom line

- **Brute force on ES(7) at 33 points is out of reach on this machine and probably on any cluster.** With the
  project's encodings and solver setups, a complete cube-and-conquer proof would take:
  - about **10^3 to 10^4 CPU-years** at the central reading;
  - **10^2 CPU-years to at least 10^6 CPU-years** as the plausible range. The data do not bound the upper end (§4).
- One night here is 16 threads x 8 h = 128 thread-h = 0.0146 CPU-years. The central reading is therefore about
  **6.8 x 10^4 to 6.8 x 10^5 nights**, and the plausible range about 6.8 x 10^3 to at least 6.8 x 10^7 nights.
- The central reading is about 500 to 5,000 times the largest comparable published run, h(6) = 30. That run took
  about 17,300 CPU-h. The figure is recalled and is not in the arXiv abstract (§7).
- **The cheapest reading of the data is 4-42 CPU-years, and it is for a weaker statement, N(7,5,7) = 26** at
  27 points. ES(7) = 33 implies that statement (ES7SPLIT, §4). At that level, N(7,5,7) = 26 alone might be feasible
  on a cluster. That is the one open, campaign-relevant question a night on this machine can sharpen.
- **Recommended first experiment** (§6):
  - a 2-4 thread-hour pilot on the Lean-verified 33-point CNF that can confirm "stop" for 33 points;
  - then one night on a calibrated estimate for (7,5,7) at 27 points, at three cutoff depths, calibrated on
    (7,5,6)@26 sub-trees that run to completion;
  - everything on one solver build.

## 2. Critic's verdict and what changed

**Verdict: "flawed".** The main conclusion holds, and the corrections make the cost *higher*, not lower. The flaws were
in how several numbers were derived and in the recommended experiment. Every fix below is applied in this file.

| # | Issue in the study draft | Fix applied here |
|---|---|---|
| 1 | Nights were rounded up: "10^5 to 10^6" | 1e3-1e4 CPU-years / 0.0146 = **6.8e4-6.8e5 nights**. The plausible range is 6.8e3 nights to at least 6.8e7 |
| 2 | "Most optimistic anchor about 30 CPU-years" | The optimistic floor is **about 4-42 CPU-years, for the weaker (7,5,7)@27 statement**. B3 at depth 18 gave >= 3.7e4 core-h (n = 5, censored), and B3 found the estimate rises with cutoff depth (18 < 24 < 30) |
| 3 | G's 2^30-2^40 leaves were converted to 1e10-1e12 CPU-s, which assumes a different cost per leaf at each end | One cost per leaf (1-10 s) gives 1e9-1e13 CPU-s, i.e. **34 to 350,000 CPU-years per hull case**, up to about 1.4e6 for the four cases |
| 4 | Ladder steps x1e3 (mean/median) and x1.3e5 (CaDiCaL 2.1.3 single solve vs a CaDiCaL 3.0.1 CnC estimate) are not like for like | Dropped. The like-for-like (7,5,6)@26 to (7,5,7)@27 step is **x184 (mean/mean) or x311 (median/median)**. The assumed x2-x30 per later rung is below every measured k = 7 step, so the ladder's top end may be optimistic, and the plausible range is widened to "at least 10^6, not bounded" |
| 5 | "Symmetry breaking can cut the work by about 12 at most" | 2h <= 12 bounds the number of **symmetric copies** (2 reflections x anchor choice among h <= 6 hull vertices), not the CDCL work. Symmetry-breaking predicates can shrink proofs by more than the group order (pigeonhole). The measured datum: at k = 6 the hull split cost **1.9x** the unsplit run in total (G) |
| 6 | "--xsb = x-reflection lex-leader" | `--xsb` adds **one binary clause**. `es6_17x.cnf` = `es6_17.cnf` + `-1 680 0` (37,630 against 37,629 clauses). That is only the first comparison of the lex-leader chain. So "ES(6)@17 with the lex-leader had no verdict" says nothing about symmetry breaking, and the draft's third A/B arm (gen_etv 33 7 7 7 --xsb) is in effect the plain un-anchored instance. It is relabelled as a control |
| 7 | The draft experiment could not change the decision. "Go" (calibrated upper 90% <= 1e5 CPU-h) sat below the (7,5,7)@27 central figures (2.05e5-2.5e5 core-h) and about 28x below G's lowest per-case figure as first converted (2.8e6 CPU-h; still about 3x below after the one-cost-per-leaf correction of row 3, 2^30 leaves x 1 s = 3.0e5 CPU-h). It also rested on the bootstrap upper bound of a heavy-tailed estimator, which is the bound unsampled tails pull down most | Redesigned (§6): a cheap pilot for "stop", the night spent on a rung whose answer is open, and a decision rule that survives heavy tails |
| 8 | Calibration on ES(6)@17 and (6,5,6)@16 does not carry over. Those trees are tiny (473 cubes, 100 s), so the bias factor there would come out near 1. The k = 7 bias comes from tail mass at depth 30-40 | Calibrate only on k = 7 trees that can be finished: random (7,5,6)@26 sub-trees |
| 9 | Solver build left unchecked; B3's estimator called march_cu | `~/research/data/erdos810-20261106/cadical/build/libcadical.a` reports **VERSION 3.0.1**. Use it for calibration and production alike, and never compare with tonight's CaDiCaL 2.1.3 timings. **march_cu is not installed**, so B3's descend.sh / sample_node.sh cannot be re-run without installing it (owner's OK needed). Only B2's pipeline (cncw lookahead splitting) can be reused |
| 10 | Loose probe budget ("400 s per probe") | Measured: plain CaDiCaL 2.1.3 on es7_33.cnf ran at **1,383 conflicts/s** (1 thread, 100 s, COMPUTED UNKNOWN; peak RSS 183 MB after 138k conflicts). That is about 14 s per 2e4-conflict node at the root and about 400-560 s per 30-40-node dive, before lookahead time. Expect about **150-300 probes per instance per night** (HEURISTIC). Time one dive before starting 15 workers |
| 11 | Literature figures stated as checked | Check status per figure in §7 |

## 3. Exact CNF sizes (EXACT; recomputed from the files by the critic)

The generators are `archive/es7-2026-10-19/tools/etv/gen_etv.py` and `tools/trackB/gen_cnf.py`. Record H proves both
sound in Lean. `gen_etv 33 7 7 7` and `gen_cnf 33 7` give the same clause multiset.

| instance | command | variables | clauses |
|---|---|---|---|
| ES(7)@33 | gen_etv 33 7 7 7 | 47,002 (5,456 = C(33,3) orientation + 41,546 auxiliary) | 679,038: 134,988 binary + 544,050 ternary; 1,902,126 literals |
| ES(7)@33, hull anchor | gen_etv 33 7 7 7 --hull | 47,002 | 679,534 (+496 = C(32,2) units) |
| mirror-class sub-CNF (H3) | | 47,002 | 535,454 |
| ETV (7,5,7)@27 | | 20,078 | 261,082 |
| ETV (7,5,6)@26 | | 15,829 | 210,132 |
| ETV (7,5,5)@21 | | 6,992 | 79,762 |
| ES(6)@17 | gen_etv 17 6 6 6 | 4,702 | 37,629 (`--xsb`: 37,630) |
| ES(5)@9 | | 462 | 2,044 |

- In ES(7)@33, 327,360 = 8 x C(33,4) clauses are the signotope 4-point rules (3-literal clauses, 8 per 4-set). The
  file is 12.2 MB.
- From k = 5 to k = 6 to k = 7, variables grow x10.18 then x9.996, and clauses x18.41 then x18.05.
- **Formula size is not the obstacle; the search tree is.** Rank-3 signotopes number 2^Theta(n^2) (OEIS A006245;
  2.9e15 at n = 12 and 1.4e25 at n = 15 are recalled by both agents, not re-checked).

## 4. Cost of the upper side (HEURISTIC throughout)

**Measured tonight** (plain CaDiCaL 2.1.3, 1 thread; verdicts COMPUTED, times HEURISTIC):

| k = 6 ladder | time | k = 7 ladder | time |
|---|---|---|---|
| (6,4,6)@12 | 0.00 s | (7,4,7)@17 | 0.59 s |
| (6,5,5)@15 | 0.63 s | (7,5,5)@21 | 5.42 s |
| (6,5,6)@16 | 60.1 s | (7,5,6)@26 | not run; B2 estimate below |
| ES(6)@17 | no verdict in 330 s, plain or with `--xsb` (G: 217 s on CaDiCaL 3.0.1) | (7,5,7)@27, (7,6,6)@31, (7,6,7)@32, (7,7,7)@33 | not run tonight |

**Earlier records:**

- (7,5,6)@26 (B2, Knuth probes, CaDiCaL 3.0.1 CnC): median 201 core-h, mean 1,117 core-h, bootstrap 90% interval for
  the mean 336-2,000 core-h.
- (7,5,7)@27:
  - B2: mean 205,458 core-h, bootstrap 90% interval for the mean 5.9e4-3.7e5 core-h;
  - B3 (march_cu cubes, censored lower bounds): >= 3.7e4 core-h at depth 18 (n = 5), >= 2.46e5 core-h at depth 24.
  - B2's probes ranged from 636 to about 1.6e6 core-h.
- ES(7)@33, record G: each hull-size case is about 2^30-2^40 leaves. No cube closed in 3 hours.
- ES(7)@33, n33k7hm (hull anchor + mirror lex-leader): about 2,200 cubes refuted in about 17 h wall time on 12, later
  4, workers. The open frontier was not shrinking. An 8-run portfolio of 2.9 CPU-h each returned UNKNOWN.

**Anchors for ES(7)@33 (corrected):**

| anchor | figure | comment |
|---|---|---|
| (7,5,7)@27 floor | 3.7e4 to 3.7e5 core-h = **4-42 CPU-years**; central 2.05e5-2.46e5 core-h = 23-28 CPU-years | A weaker statement: for point sets, ES(7) = 33 implies N(7,5,7) = 26 (ES7SPLIT; compare Erdős-Tuza-Valtr 1996, recalled, not re-checked). CDCL cost is not monotone under such reductions, so this is a heuristic floor, not a proved bound. The step to signotopes was exercised only by B3's glue control; no written abstract-level proof was checked |
| G hull cases | 1e9-1e13 CPU-s = **34-350,000 CPU-years per case**, four cases, about 136 to 1.4e6 in total | One consistent cost of 1-10 s per leaf |
| Ladder from (7,5,7)@27 over three more rungs | x2-x30 per rung from B2's mean 2.05e5 core-h: **about 187 to 6.3e5 CPU-years** | x2-x30 is below the measured like-for-like k = 7 step (x184-x311). Applied per rung, that step would give about 1e8 CPU-years. The rungs differ in how many points they add, so this is only an illustration of why the upper end is unbounded |

- **Total:** central 10^3-10^4 CPU-years; plausible 10^2 to at least 10^6 CPU-years; optimistic floor 4-42
  CPU-years, for the weaker statement only.
- **Symmetry:** at most 2h <= 12 symmetric copies. The CDCL gain is empirical: the hull split at k = 6 took 1.9x the
  unsplit work in total.
- **Szekeres-Peters-style enumeration:** no figure can be given, because no known pruning rule is strong enough at
  k = 7.
- **Certification:** an LRAT proof of this size would plausibly run to petabytes (by analogy with Schur number five,
  about 2 PB; recalled), and cake_lpr time would be of the same order as solving. Nothing at this scale could be
  CERTIFIED with the project's toolchain on this machine.

## 5. Lower side (a 33-point set with no convex heptagon)

- **An exhaustive search is the same instance with the opposite answer**, so it costs the same. A SAT model is only a
  signotope and would still need a realization. Krapivin-Przybocki-Heule reportedly realized none of 200,000 abstract
  32-point solutions. That figure is unverified: the paper (arXiv:2607.02958) exists, but its abstract does not
  mention it.
- **Heuristic searches so far have all failed**, and a heuristic search can never show that no such set exists:
  - N2: 60 runs, 36,082 CPU-s; the best set still had 1 heptagon.
  - All 8,537 annealed 32-point order types are saturated (no 33rd point can be added).
  - AlphaEvolve's 33-point set has exactly one 7-gon.
- **Proved constraints:** any counterexample has only unbalanced splits, and a split exists iff N(7,5,7) >= 27
  (ES7SPLIT). No counterexample is mirror-symmetric (MIRRORETV).
- A night of heuristic search is not worth it as the first experiment. Roadmap §3 reached the same reading.

## 6. Recommended first experiment (revised after the critic)

**Purpose:** make the next decision with measured, calibrated numbers. The decision is whether to write a cluster
proposal for N(7,5,7) = 26 and whether to stop brute force on 33 points for good. Nothing here can prove anything
about ES(7).

**Setup (all parts):**

- Rebuild B2's `cncw.cpp` (`results/B2/scripts/`) against `~/research/data/erdos810-20261106/cadical/build/libcadical.a`
  (3.0.1). B2's `knuth.py` is the estimator. B3's `iworker.cpp` exists, but B3's march_cu cube generation does not run
  here. Use this one build everywhere.
- Install nothing (march_cu and kissat stay uninstalled unless the owner agrees).
- Run `scripts/memguard.sh` as its own unit.
- Use the same seeds across variants.

**Step 0: pilot that can confirm "stop" for 33 points (2-4 thread-hours, 1 unit).**

- Instance: the Lean-verified n33k7hm CNF (`gen_cnf 33 7 --hull --mirror`; not generated tonight).
- First time one dive end to end.
- Then run 20-50 random lookahead dives, recording depth to leaf and leaf cost.
- At 1-14 s per leaf, 1e6 CPU-h corresponds to about 2^28-2^32 leaves. G's dive depths were 30-40.
- **Rule:** if the pilot's (censoring-aware, hence low-biased) estimate is >= 1e6 CPU-h, stop brute force on 33 points
  and record it.
  - Only if it comes out clearly below 1e6 CPU-h is a 33-point A/B worth a night. Its arms would be n33k7hm, hull-only
    and the plain control (formerly "--xsb"), under the rule below.

**Step 1: the night (up to 15 units at 1 GB each, plus memguard; 16 threads, well under 24 GB).**

- **Main arm:** a B2-pipeline Knuth estimate for (7,5,7)@27 at three cutoff depths, about 18, 24 and 30. B3 found
  depth 18 cheapest and the estimate rising with depth, which is itself a sign of tail mass the deeper samples see.
  Use about 3-4 units per cutoff.
- **Calibration arm (about 4 units):** several random 1/1024 sub-trees of (7,5,6)@26, each run to completion (B2: mean
  about 1.1 core-h per sub-tree, heavy-tailed). Run the same probe procedure inside each one. The ratio of the full
  cost to the probe estimate is the **Knuth bias at k = 7**. A factor measured at k = 6 would not carry over.
- **Probe budget:** set it from the Step 0 timing. Expect about 150-300 probes per instance per night (HEURISTIC).
  If the (7,5,7)@27 tree has about 2^18 cubes at depth 18, B2's mean puts the average leaf at about 0.8 core-h, so cap leaf solves and count capped probes
  as censored.

**Decision rule (made to survive heavy tails; the thresholds are the study's):**

- Report a cost figure for a cutoff only if all of these hold:
  - it has at least 150 probes;
  - no probe is censored. Otherwise report it as a lower bound only;
  - it is multiplied by the measured k = 7 bias factor;
  - it passes a tail check: recompute it with the top 1% of probe values doubled and with them removed. If it moves
    by more than x3, call it unbounded.
- **Go** (write a cluster proposal for N(7,5,7) = 26): the bias-corrected, tail-checked figure at the cheapest cutoff
  is <= 1e5 CPU-h (about 11 CPU-years, about 6x the h(6) = 30 run).
- **Stop** (drop brute force on (7,5,7)@27 too, and turn to structure): its lower bound is >= 1e6 CPU-h (about
  114 CPU-years). "Structure" means, for example, the ES7SPLIT §7 conjectures (no hexagonal hull at 33 points, at
  least 7 convex layers).
- **In between, or censored:** inconclusive. Next would come symmetry variants on (7,5,7)@27 with a real lex-leader
  chain, not `--xsb`.
- Prior figures for (7,5,7)@27 (3.7e4 to 3.7e5 core-h) straddle the go threshold, so this night's outcome is open.
  The draft's 33-point night was not.

**What it would show:**

- a calibrated order of magnitude for the cost of N(7,5,7) = 26 on one solver build;
- the cheapest cutoff;
- the size of the Knuth bias on k = 7 trees;
- whether 33-point brute force is past 1e6 CPU-h on the Lean-verified CNF;
- any SAT leaf, which would be an abstract signotope model only and would need a realization before it says anything
  about point sets.

**What it would not show:**

- anything about whether ES(7) = 33 is true;
- any certificate (nothing CERTIFIED);
- a lower bound for other methods: ideas took ES(6) from about 1,500 CPU-h to seconds;
- a reliable number if many probes are censored. In that case it gives a lower bound only.

## 7. Literature figures and their check status

| claim | source | status tonight |
|---|---|---|
| ES(6): Szekeres-Peters 2006 about 1,500 CPU-h | LIT/RELATED.md | **across three independent implementations**, secondary; not a single run |
| ES(6): Marić 2019 about 0.5 h | LIT | from the LIT record, not re-checked |
| Heule-Scheucher 2024 (arXiv:2403.00737): h(6) = 30 in about 17,300 CPU-h; ES(6) in seconds | LIT, recollection | **neither figure is in the abstract**; both agents recall 17,300, not confirmed |
| Dumitru 2025 (arXiv:2512.24061): UNSAT only for anchored subfamilies, heavy-tailed run times dominate | abstract | **confirmed from the abstract** |
| Krapivin-Przybocki-Heule (arXiv:2607.02958, 3 Jul 2026): 0 of 200,000 abstract 32-point solutions realized | secondary | paper exists; **figure not in the abstract, unverified** |
| Erdős-Tuza-Valtr 1996: the ES conjecture for n implies the refined bound for that n | recollection | not re-checked |
| Schur number five (about 14 CPU-years, about 2 PB); Pythagorean triples (about 35,000 CPU-h); A006245 values | recollection | not re-checked |
| arXiv search, abstracts since June 2025 | study agent | nothing newer found ("new" only means not found in this search) |

## 8. Risks and what remains

- **Every cost figure is HEURISTIC.** Knuth and cube-sample estimates on heavy-tailed trees are biased low under
  censoring. Do not quote the central value without the range.
- The (7,5,7)@27 floor depends on the ES7SPLIT gluing for point sets. The abstract (signotope) version was not checked
  in writing.
- ES(6)@17 gave no verdict within 330 s on CaDiCaL 2.1.3, against 217 s on 3.0.1 in G. This is one reason to use one
  build.
- **Not done:**
  - generating and timing n33k7hm (`gen_cnf 33 7 --hull --mirror`);
  - any probe on a 33-point instance tonight. All 33-point costs come from G and the n33k7hm run.
  - a full x-reflection lex-leader chain for gen_etv. Only the one-clause `--xsb` exists.
- About 60 MB of scratch CNFs sit in `/home/jay/research/data/roadmap-20261115/es7feas/cnf/`. Deleting them is the
  owner's call.

## 9. Files and hashes

- Work notes and logs: `/home/jay/research/data/roadmap-20261115/es7feas/`
  - `README.md`, `sizes.txt`, `sizes2.txt`, `times.txt`, `times2.txt`, `run.sh`, `run2.sh`, `SHA256SUMS.cnf`.
- SHA-256 of the generated CNFs (from `SHA256SUMS.cnf`):

```
854a20b91250e90bf18213c7788275b7cf94b72d0578fe615572e9d5ca9a32d8  cnf/es7_33.cnf   (gen_etv 33 7 7 7)
8d75ee0b4f1633790b2ef52f3c2164467abf68a30864ed7036004823eed898fd  cnf/es7_33h.cnf  (gen_etv 33 7 7 7 --hull)
7c93c0ed74ecc0383ec443b9e8321e69ced26203cd57ecc738522b3da1f42c09  cnf/es6_17.cnf   (gen_etv 17 6 6 6)
f92d263c7b05b1c0e864dd16c1565074b047f4d4a4e061a5814abe2718299cc9  cnf/es6_17x.cnf  (gen_etv 17 6 6 6 --xsb)
```

- Records used: G, H, H3, B2, B3, ES7SPLIT, MIRRORETV, N2, LIT (all under `archive/es7-2026-10-19/results/`).

## 10. Resume commands

```bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
T=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/tools
cd /home/jay/research/data/roadmap-20261115/es7feas
$PY -I $T/etv/gen_etv.py 33 7 7 7 -o cnf/es7_33.cnf && sha256sum cnf/es7_33.cnf   # expect 854a20b9...
# Step 0 / Step 1 (§6): rebuild results/B2/scripts/cncw.cpp against
#   ~/research/data/erdos810-20261106/cadical/build/libcadical.a (3.0.1); flags and driver: see results/B2/README.md.
# Run each job as: systemd-run --user --unit=esr-<track>-<job> -p CPUQuota=100% -p MemoryMax=1G \
#   -p MemorySwapMax=0 -p RuntimeMaxSec=<s> --nice=10 ...   with scripts/memguard.sh running alongside.
```
