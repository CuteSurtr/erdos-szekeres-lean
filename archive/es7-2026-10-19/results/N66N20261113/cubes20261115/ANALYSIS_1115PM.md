> Saved by the main session at 18:40 from track A1's returned text, unchanged. The harness refused the agent's own Write.

# N66 level-14 cube campaign: cost analysis and proposals (track A1, 15 November 2026, afternoon)

**Status (17:12 KST): analysis finished for the data snapshot of 16:56:47 KST.**
- Snapshot (campaign_status.json): 65 certified, 24 split, 5 running, 18 queued; 88 leaves.
- At 17:09:31: 66 certified, 26 split, 5 running, 19 queued; 90 leaves.
- Data analysis only. No solver runs, no units, nothing in the campaign touched.
- **N66 <= 55 is NOT decided.** N66 <= 56 (level 13, CERTIFIED) remains the bound.
- Labels: counts read from the logs are COMPUTED; every estimate is HEURISTIC.

## Main findings

1. **A rule known before any run sorts cubes into cost classes ("band").**
   - Definition: b = (number of occupied states among 25 12 16 29 17 37, with 37 counted twice), minus 1 if 25 is a hole and 29 and 37 are occupied, minus the number of hole literals on re-split states.
   - Check: b = round((v1 − 114,643)/6,300), where v1 is the active-variable count after CaDiCaL's first elimination round. This holds for all 86 runs whose log has that line (asserted in model.py; COMPUTED).
   - Counts, full 1,200 s runs: b ≤ 2: 17/17 certified; b = 3: 31/33; b = 4: 9/25; b = 5: 0/3.
2. **The 'o' children do get easier with depth, but slowly.**
   - In band ≥ 4, each 'o' re-split multiplies the conflicts needed by ×0.77 (profile 95 % interval ×0.68–×0.87; likelihood-ratio test against "no effect" p = 0.0001).
   - An 'h' re-split lowers the band by one: ×1/2.2 on average, ×1/1.9 at the band 3→4 step. So an 'o' half needs about 1.7–2.9 times the conflicts of its 'h' sibling.
   - The main session's "o halves stay as hard as the parent" is right in direction but too strong: each 'o' split removes about a quarter of the work.
   - Band-4 'o' children, counts: k = 0: 2/10, k = 1: 2/7, k = 2: 2/5, k = 3: 3/3.
3. **The current strategy needs about 210–325 slot-hours more** (1,200 s limit, split on a timeout, RESPLIT order; three model variants).
   - That is about 42–65 h wall at 5 slots, with 300–475 more timed-out runs.
   - The 5 open cubes of band 6–7 (four 1-hole cubes with 37 occupied, and oooooo) carry 55–75 % of it.
   - In two of the three variants, the all-'o' chains run past the end of the 12-state RESPLIT list.
   - Kept partial files (about 3.9 GB per timed-out run) need 1.1–1.8 TB more disk; 686 GB were free at 17:04.
   - A hold-out check shows the model leans pessimistic. Read these totals as upper-leaning.
4. **The conflict rate rises through a run.**
   - Median of 21 full-limit timeouts: 990/s at 100–300 s, 1,900/s at 300–600 s, 2,900/s at 600–900 s, 3,400/s at 900–1,150 s.
   - The monolithic level-14 run on the same base CNF (b14h2) reached 3.49M conflicts at 1,200 s, 11.39M at 2,400 s and 19.75M at 3,600 s: about 6,600/s between 1,200 and 2,400 s.
   - Every fresh child pays the warm-up again. Every certified leaf also pays a certification pipeline of 125 s + 115 s per million conflicts.
   - Timed-out runs used 31 % of all wall time so far, and about half of the simulated remainder.
5. **Best proposal: a 2,400 s limit plus pre-splitting down the 'o' side** for cubes that the model says cannot finish.
   - Expected remaining work: about 50–90 slot-hours (−64 % to −84 %).
   - No cube run has gone past 1,200 s; the evidence for later conflict rates is the monolithic run. Test it cheaply first (§5).

## 1. Data and method

**Inputs (read-only).**
- W/p2/c14/campaign_status.json (W = /home/jay/research/data/n66-20261113).
- Per cube: W/p2/c14/<id>.out and W/p2/c14/<id>/it1/cadical.log. Only it1 exists, so no lazy re-solves occurred.
- used_rows.json of the certified cubes.
- The cadical.log of the monolithic runs W/p2/b14h2/it1 and W/p2/b14i2/it1.
- README.md, PROGRESS.md and STATUS_campaign.md of this folder, and W/p2c14_driver_r3.py.

**Per run.**
- From the log: verdict, conflicts, process and real time, and the report lines (process s, conflicts, active variables).
- From the events: solve time and pipeline time.
- From the status file: holes, depth, the literals, the limit, and parent and children.

**Classes.** Holes (the driver's count), depth, sign of the last literal, band b, and k = the number of occupied re-split literals.

**Cost model.** A censored log-normal (Tobit) model of conflicts to UNSAT; timeouts are right-censored at their conflicts.
- log C = α + β·b + γ·k + ε, with ε ~ N(0, σ²).
- Fitted by maximum likelihood on 82 runs, 24 of them censored.
- Variant A: common β and γ: ×2.13 per band, ×0.84 per 'o' split, σ 0.37.
- Variant B: separate intercepts for bands 0–4 (steps ×3.38, ×2.66, ×1.91, ×1.89); bands ≥ 5 extrapolated with the 3→4 step; γ ×0.86; σ 0.35.
- Variant C: β ×2.20; γ ×0.77 for b ≥ 4 and ×0.98 for b < 4; σ 0.35.
- Fit: C has negative log-likelihood 31.25, against 34.60 for A, with one parameter more.

**Time model.**
- Base: the median conflicts-versus-process-time curve of the 18 afternoon full-limit timeouts. It reaches 2.60M at 1,175 s; per-run speed factors 0.80–1.27.
- Beyond 1,175 s: linear at 3,712/s (the slope of its last 200 s). A sensitivity run uses 4,800/s, the shape of the monolithic run.

**Other cost terms.**
- Pipeline: 125 s + 115 s per million conflicts (least squares, 32 afternoon certified cubes).
- Overhead outside CaDiCaL and the pipeline: 13 s per run.
- CPU = 0.98 × wall (CPUQuota 98 %).

**Simulation.** Monte-Carlo over the tree the driver would grow from the 22 open roots.
- Running cubes are conditioned on the CPU they had already used.
- A timeout costs limit + 13 s and spawns (b, k+1) and (b−1, k). A run beyond depth 12 counts as "depth cap hit".
- 150–300 trees per variant. Repeated runs of the same variant differ by up to about 7 % (heavy right tail).

**Hold-out check.** Model C fitted on earlier runs only, then used to predict later full-limit runs.

## 2. Cost model (question 1)

### 2.1 Outcomes by band and k (COMPUTED counts; full 1,200 s runs; Clopper–Pearson 95 %)

| band | k | certified/runs | 95 % interval | median CaDiCaL s | median pipeline s | median conflicts |
|---|---|---|---|---|---|---|
| 0 | 0 | 1/1 | 0.03–1 | 124 | 98 | 0.11M |
| 1 | 0 | 4/4 | 0.40–1 | 251 | 144 | 0.34M |
| 2 | 0 | 11/11 | 0.72–1 | 472 | 214 | 0.93M |
| 2 | 1 | 1/1 | 0.03–1 | 670 | 307 | 1.33M |
| 3 | 0 | 21/22 | 0.77–1 | 784 | 310 | 1.85M |
| 3 | 1 | 6/7 | 0.42–1 | 767 | 244 | 1.42M |
| 3 | 2 | 4/4 | 0.40–1 | 931 | 331 | 1.76M |
| 4 | 0 | 2/10 | 0.03–0.56 | 1,063 | 410 | 2.71M |
| 4 | 1 | 2/7 | 0.04–0.71 | 1,042 | 319 | 2.24M |
| 4 | 2 | 2/5 | 0.05–0.85 | 1,190 | 475 | 2.48M |
| 4 | 3 | 3/3 | 0.29–1 | 908 | 363 | 1.57M |
| 5 | 0 | 0/3 | 0–0.71 | – | – | – |

- The two band-3 timeouts are oohhoh and its child oohhoh_23o.
- ooohho_23h_49o counts as certified: it was UNSAT at 1,021 s, and the driver accepted it at 17:03.
- Shortened runs are excluded: ohhoho (449 s), ohhhoo (307 s) and ohohho_23h (352 s) were split; ohhooh (1,132 s) was certified.
- The 8 UP-refuted cubes took 45–51 s wall each.

### 2.2 By holes, depth and sign of the last literal (COMPUTED; full-limit runs)

| holes | k | depth | runs | C | T | median CaDiCaL cpu s (C) [range] | median conflicts (C) [range] |
|---|---|---|---|---|---|---|---|
| 6 | 0 | 0 | 1 | 1 | 0 | 124 | 0.11M |
| 5 | 0 | 0 | 5 | 5 | 0 | 246 [239–385] | 0.34M [0.30–0.63] |
| 5 | 0 | 2 | 1 | 1 | 0 | 368 | 0.64M |
| 4 | 0 | 0 | 12 | 12 | 0 | 618 [333–930] | 1.44M [0.47–2.15] |
| 4 | 0 | 1 | 6 | 6 | 0 | 738 [400–768] | 1.38M [0.78–2.00] |
| 4 | 0–2 | 2–3 | 11 | 11 | 0 | 579–912 | 1.23–1.76M |
| 3 | 0 | 0 | 14 | 9 | 5 | 890 [550–1,048] | 2.17M [1.20–3.60] |
| 3 | 0 | 1 | 5 | 4 | 1 | 847 [664–1,041] | 1.71M [1.09–2.11] |
| 3 | 1 | 1 | 7 | 1 | 6 | 907 | 1.86M |
| 3 | 2 | 2 | 6 | 3 | 3 | 1,152 [1,023–1,166] | 2.39M [2.36–2.48] |
| 3 | 3 | 3 | 3 | 3 | 0 | 889 [821–897] | 1.57M [1.51–1.58] |
| 2 | 0 | 0 | 6 | 0 | 6 | – | – |

**Sign of the last literal.**
- At depth 0 the last literal is state 37. A cube with 37 = o sits one band higher than a cube with the same holes and 37 = h.
  - 4 holes: 37 = o median 705 s (5/5 certified), against 530 s (7/7) for 37 = h.
  - 3 holes: 37 = o 4 certified / 4 timed out, against 5 certified / 1 timed out for 37 = h.
- At depth ≥ 1, with 3–4 holes: an 'h' last literal 20/21 certified, an 'o' last literal 8/17.
- Within a band, the sign adds nothing beyond k.

**Fitted P(certified within 1,200 s), model C.**
- Band 3: 0.83–0.90.
- Band 4: 0.10, 0.30, 0.59, 0.84, 0.96 for k = 0–4.
- Band 5: 0.00, 0.00, 0.02, 0.10, 0.30, 0.59, 0.84 for k = 0–6.
- Band 6: ≤ 0.10 up to k = 6.

### 2.3 Model C medians (HEURISTIC; afternoon speed; seconds = CaDiCaL wall, linear extrapolation beyond 1,175 s)

| band | k0 | k1 | k2 | k3 | k4 | k5 | k6 |
|---|---|---|---|---|---|---|---|
| 3 | 1.85M/994 s | 1.82M | 1.79M | 1.75M | 1.72M | 1.69M | 1.66M |
| 4 | 4.08M/1,606 s | 3.13M/1,346 s | 2.40M/1,148 s | 1.85M/991 s | 1.42M | 1.09M | 0.84M |
| 5 | 8.98M/2,954 s | 6.89M/2,381 s | 5.29M/1,941 s | 4.06M | 3.12M | 2.40M | 1.84M |
| 6 | 19.8M/5,921 s | 15.2M | 11.7M | 8.95M | 6.87M | 5.28M | 4.05M |
| 7 | 43.6M/12,456 s | 33.4M | 25.7M | 19.7M | 15.1M | 11.6M | 8.92M |

- Bands 6 and 7 have no data; band 5 has only 3 censored runs.
- Consistency check: the monolithic level-14 runs passed 57.8M conflicts without a verdict.

### 2.4 Throughput (COMPUTED medians)

**Warm-up**, median of 21 full-limit timeouts:

| process-time window | conflict rate |
|---|---|
| 40–100 s | 375/s |
| 100–300 s | 992/s [828–1,609] |
| 300–600 s | 1,893/s [1,330–2,972] |
| 600–900 s | 2,907/s [2,270–3,959] |
| 900–1,150 s | 3,399/s [2,816–4,762] |

- The rate was still rising at the limit.
- b14h2 (the same base CNF, no cube units): 0.99M conflicts at 600 s, 3.49M at 1,200 s, 7.02M at 1,800 s, 11.39M at 2,400 s, 19.75M at 3,600 s, 57.6M at 11,339 s. b14i2 is similar (3.33M, 11.12M, 19.31M).
- First elimination happens at 35–65 s (median 49 s).
- Example oooohh: simplification takes 46 % of process time, most of it vivification (33 % of the total).

**Load.**
- Band-4, k = 0 timeouts reached 3.24–3.80M conflicts in the morning (about 2.4 cubes at once).
- The same class reached 2.61–3.24M in the afternoon (about 4.0 cubes at once, plus other tracks' jobs).
- Medians 3.5M against 2.87M (×0.82). Confounded: other tracks' load is not logged per run.
- Because the limit is wall time (`-t`), the same cube can certify in the morning and time out in the afternoon.

**Where the wall time went** (finished runs, 23.6 h).
- Certified runs: 16.1 h (CaDiCaL 11.4 h, pipeline 4.5 h).
- Timed-out runs: 7.4 h (31 %, 24 runs).
- UP-refuted cubes: 0.1 h.
- Morning (r1): 33 certified, 6 split. Afternoon (r2/r3 from 13:12): 32 certified, 18 split, 5 running.

## 3. Do the 'o' children become easier with depth? (question 2)

Conflicts in millions. T = timed out (conflicts at the limit, a lower bound); C = certified; U = UNSAT with the pipeline still running at the snapshot.

| parent (band, k) | parent | split | 'o' child | 'h' child |
|---|---|---|---|---|
| oohhoh (3,0) | T>3.50 | 23 | T>3.30 | C 1.26 (517 s) |
| oohhho (4,0) | T>3.24 | 23 | T>2.73 | C 1.97 (765 s) |
| ohohho (4,0) | T>3.80 | 23 | T>2.70 | T>0.48 (352 s limit) |
| hohhoo (4,0) | T>2.89 | 23 | T>2.36 | C 1.41 (728 s) |
| hhohoo (4,0) | T>2.82 | 23 | T>2.42 | C 1.36 (768 s) |
| ohhoho (4,0) | T>0.71 (449 s limit) | 23 | C 1.86 (907 s) | C 0.78 (400 s) |
| ohhhoo (4,0) | T>0.35 (307 s limit) | 23 | T>2.39 | C 2.00 (748 s) |
| oohhoh_23o (3,1) | T>3.30 | 49 | C 2.39 (1,023 s) | C 1.33 (656 s) |
| oohhho_23o (4,1) | T>2.73 | 49 | T>2.40 | C 1.54 (784 s) |
| ohohho_23o (4,1) | T>2.70 | 49 | T>2.27 | C 1.42 (751 s) |
| hohhoo_23o (4,1) | T>2.36 | 49 | C 2.36 (1,152 s) | C 1.33 (710 s) |
| hhohoo_23o (4,1) | T>2.42 | 49 | C 2.48 (1,166 s) | C 1.38 (751 s) |
| ohhhoo_23o (4,1) | T>2.39 | 49 | T>2.40 | C 1.52 (809 s) |
| ohohho_23h (3,0) | T>0.48 (352 s limit) | 49 | C 1.27 (579 s) | C 0.64 (368 s) |
| ooohho_23h (4,0) | T>2.61 | 49 | U 2.24 (1,021 s; accepted 17:03) | C 1.23 (660 s) |
| oohhho_23o_49o (4,2) | T>2.40 | 44 | C 1.57 (889 s) | C 1.74 (891 s) |
| ohohho_23o_49o (4,2) | T>2.27 | 44 | C 1.58 (897 s) | C 1.65 (864 s) |
| ohhhoo_23o_49o (4,2) | T>2.40 | 44 | C 1.51 (821 s) | C 1.76 (912 s) |
| 6 two-hole base cubes (4–5,0) | T>2.09–3.24 | 23 | queued | C 1.09–2.11 (4), T 1, 1 then running (T at 17:07) |

**Answer: yes, by about ×0.77 per 'o' split in band ≥ 4** (95 % profile interval ×0.68–×0.87, model C).
- The 'h' halves certify at once: 21 of 22 full-limit 'h' children (the exception is ooohho_23h, band 4).
- From band 4, the 'o' halves need about three 'o' splits before P(1,200 s) exceeds 0.8 (model 0.84 at k = 3; counts 3/3).
- At k = 2 they sit right at the limit: two certified at 1,152 s and 1,166 s, and three timed out at 2.27–2.40M.
- In band < 4 no 'o' effect is detectable (×0.98), but those cubes certify anyway.
- All 'o' splits so far were 23, then 49, then 44, so the effect of the state cannot be separated from depth. The 44 step looks largest: k2→k3 about 2.4M → 1.55M, ×0.65 (n = 3).
- Events after the snapshot agree with the model's P = 0.10 for band 4, k = 0: ohoooh timed out at 2.69M (16:59), oohhoo_23h timed out at 2.59M (17:07), and ooohho_23h_49o was accepted.

## 4. Remaining work under the current strategy (question 3; HEURISTIC)

**Open roots at the snapshot (22).**
- Band 4, k = 0 (5): hhoooo, hohooo, hoooho, plus the running ohoooh and oohhoo_23h.
- Band 4, k = 1 (3): oohooh_23o, ooohoh_23o, oooohh_23o.
- Band 5, k = 0 (6): hoohoo, hooooo, ohhooo, oooooh, plus the running ohohoo and ohooho.
- Band 5, k = 1 (3): oohhoo_23o, oohoho_23o, ooohho_23o.
- Band 6 (4): ohoooo, oohooo, ooohoo, ooooho.
- Band 7 (1): oooooo.

**Remaining wall slot-hours** (mean, with Monte-Carlo p10–p90 in brackets):

| current strategy (1,200 s, split on timeout) | model A | model B | model C |
|---|---|---|---|
| slot-hours | **324** [309–340] | **295** [279–311] | **210** [199–219] |
| leaves / timed-out runs | 484 / 474 | 438 / 424 | 317 / 295 |
| simulations hitting the 12-state depth cap | 100 % | 98 % | 3 % |
| by root band 4 / 5 / 6 / 7 | 14 / 67 / 128 / 117 | 13 / 60 / 115 / 105 | 13 / 52 / 81 / 64 |

**Reading the table.**
- CPU-hours = 0.98 × slot-hours.
- At 5 slots this is 42–65 h wall, if per-cube throughput holds; it fell with load (§2.4).
- In models A and B the totals are truncated at the depth cap, where the driver marks the cube timeout_no_split_state.
- Sensitivity, model A: ±1 SE on β gives 200–499 h; ±1 SE on γ gives 220–531 h.

**Hold-out.**
- Model C fitted on the morning runs (n = 31) predicted 20.8 certified among the 51 afternoon full-limit runs; 33 were certified (Brier 0.173, against 0.228 for a constant rate).
- Fitted on the runs before 15:00 (n = 59), it predicted 8.1 certified among the 23 later runs; 15 were certified (Brier 0.223, against 0.227).
- So the model leans pessimistic, and the absolute totals are upper-leaning. The relative savings in §5 change less: with an 'o' factor of 0.65 instead of 0.77, P1+P2 still saves about 60 %.

**Disk** (the r2/r3 driver keeps partial files).
- Per timed-out run: about 3.9 GB (partial LRAT about 1.29 KB per conflict, plus cert.cnf 664 MB).
- Per certified leaf: about 1.3 GB (cert.cnf, trim.lrat about 345 B per conflict, zstd copy).
- Projection for the current strategy: about 1.6 TB (model C) to 2.5 TB (model A).
- At 17:04, / had 686 GB free, and W/p2/c14 already held 159 GB (69.9 GB of it kept partials of 18 runs).
- **The current strategy runs out of disk before it finishes**, unless partial files are compressed or deleted. That is the owner's decision.

## 5. Proposals for the next session (question 4; nothing was run)

The ranges cover models A, B and C and repeated Monte-Carlo runs.

| # | proposal | evidence | expected remaining slot-h | saving |
|---|---|---|---|---|
| P1 | CaDiCaL limit 2,400 s instead of 1,200 s (at least for band ≥ 4) | the warm-up and the monolithic curve (§2.4); model C P(≤2,400 s): band 4 k0 0.94, k1 0.99; two k2 cubes certified at 1,152/1,166 s | linear slope: A 108–112, B 69–70, C 84–87; monolithic slope (4,800/s): A 72, B 50, C 73 | −59 % to −83 % |
| P1+P2 | P1 plus a staircase pre-split: split without running, 'o' side only, every node with P(certified within 2,400 s) < 0.2 | model C (band 6 k ≤ 2 and band 7 k ≤ 5 are below 0.2; band 5 k0 is 0.23) | linear: A 86–92, B 62–65, C 73–78; monolithic: A 67, B 48, C 62 | −64 % to −84 % |
| P2 alone | keep 1,200 s; pre-split down the 'o' side when P(1,200 s) < 0.2 (band 4 k0, band 5 k ≤ 3, band ≥ 6) | 0/6 two-hole base cubes certified; band-5 P ≈ 0 | A 263, B 250, C 166 | −15 % to −21 % |
| P1' | 3,600 s for every cube | as P1 | A 66 (linear slope) | −80 % (A) |
| P3 | re-order the remaining re-split states by level-14 core usage: 40 52 46 44 45 39 32 30 20, then 57 14 53 38 47 33 19 50 58 62; 23 and 49 last | in the 62,001 row uses of the 57 certified cores (own split states excluded), 40, 52, 44 and 46 rank #1–#4; 23 ranks #55 and 49 #28; the 44 'o' step (×0.65, n = 3) was larger than the 23 and 49 steps (about ×0.75–0.8) | if the 'o' factor became ×0.65: model C 121 (current) / 48 (P1+P2) | up to −42 %; unproven |
| P4 | add a conflict limit (`-c`) next to `-t`, e.g. 2.6M for 1,200 s or 7M for 2,400 s | per-cube throughput fell about 18 % between morning and afternoon load | reproducible split decisions; no direct saving | – |
| P5 | extend RESPLIT beyond 12 states (P3's tail) before any branch reaches depth 12 | band 7 needs about 11 'o' splits for P(1,200 s) ≥ 0.5 (model C); models A and B hit the cap in ≥ 98 % of simulations | needed to finish at all with 1,200 s | – |
| P6 | owner decision: zstd the partial LRATs of timed-out runs (ratio about 4.9 on cube B) or delete them (they certify nothing); keep cert.cnf only as the F_c hash plus cube units (U1 already checks cert.cnf = F_c + units) | §4 disk projection | 1–2 TB of disk | – |

**First step: a decisive, cheap test of P1.**
- Run the 3 queued band-4, k1 cubes (oooohh_23o, ooohoh_23o, oohooh_23o) with `-t 2400` and the same pipeline.
- Model C gives each P(≤1,200 s) = 0.30 and P(≤2,400 s) = 0.99.
- If 2 or 3 of them certify, adopt P1+P2. If they time out at 2,400 s, the extrapolation is wrong: go back to 1,200 s with P2 and P3.

**Risks of P1.**
- CaDiCaL memory: the peak RSS so far is 2.69 GB at 1,200 s, and the monolithic peak was 2.86 GB after 3 h 10 min, about 70 % of the 4.1G unit.
- cake_lpr memory: trim.lrat grows at about 345 B per conflict, so about 2.4 GB at 7M conflicts (largest so far: 1.24 GB at 3.6M). Every cake_lpr run used the 2,000 MB heap. A 4,000 MB+ tier does not fit in a 4.1G unit, so such a cube would end unsat_not_accepted and need its pipeline re-run in a bigger unit.
- Disk: a 2,400 s timeout leaves about 9–10 GB of partial files.

Not proposed: march-style cubing (third-party code), and CaDiCaL option changes (untested).

## 6. Limits of this analysis

- **Independence.** Lineages are drawn independently by class. The k ≥ 1 classes contain only children of timed-out parents, so that selection is inside their fit.
- **Extrapolation.** Bands 5–7 are extrapolated: band 5 has 3 censored runs, bands 6–7 none. They dominate the totals, which are uncertain by about a factor of 2 either way.
- **Confounding.** The effect of the state is confounded with depth, because the order 23, 49, 44 was fixed.
- **Load.** Machine load is not modelled.
- **Pipeline cost.** It is linear in conflicts, fitted only up to 2.5M conflicts.
- **Not checked here:** the certificates (VERIFY_N66CUBES.md does that), the cover, and the driver.

## 7. Files

All in /home/jay/research/data/roadmap-20261115/pm1115/a1/ (not in Git). Hashes are in SHA256SUMS (17 entries).

| file | content |
|---|---|
| extract.py → cubes.json | one record per cube |
| tables.py → tables.txt | class tables, parent/child table, rates, v1 bands |
| model.py → model_out.json, model_stdout.txt | model A, time and pipeline models, simulations, calibration; asserts the band rule |
| model_b.py → model_b_out.json | models B and C, breakdown by root band |
| model_c_se.py | profile interval and likelihood-ratio test |
| classC.py | §2.3 table |
| model_p3.py | P3 value |
| model_mono.py | P1 with the monolithic slope |
| holdout.py | hold-out check |
| rowfreq.py | core row frequencies |
| extra.py | wall split, proof bytes per conflict, Clopper–Pearson table, open cubes by band |

## 8. Resume

```bash
cd /home/jay/research/data/roadmap-20261115/pm1115/a1
P=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
export OPENBLAS_NUM_THREADS=1
$P -I extract.py && $P -I tables.py > tables.txt && $P -I extra.py
$P -I model_b.py 150; $P -I model_c_se.py; $P -I classC.py; $P -I model_p3.py; $P -I model_mono.py
$P -I holdout.py 46800; $P -I holdout.py 54000; $P -I rowfreq.py
$P -I model.py 300 > model_stdout.txt   # run last: every script above imports model.py and overwrites model_out.json
```
