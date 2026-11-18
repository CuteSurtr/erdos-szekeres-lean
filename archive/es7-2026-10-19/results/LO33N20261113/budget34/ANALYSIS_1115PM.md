> Saved by the main session at 18:40 from track A2's returned text, unchanged. The harness refused the agent's own Write.

# Analysis 15 Nov 2026 afternoon: the budget-35 (20,15) omission-tree loop (track A2)

**Status 17:10 KST: read-only analysis.**
- Labels: COMPUTED for counts read from the loop's logs and the closed context files, HEURISTIC for estimates.
- No run, no unit; the loop `esr-lo-b35s20v10b` and its files were not touched.
- (20,15) is not closed: 987 of 8,065 contexts at 16:47. The live round c142s1 was still in its re-walk prefix at 17:05 (24 too-big attempts, 0 closes). So ES(8) <= 307 is not reached.
- **Main finding:** every finder start re-attempts all known too-big contexts, starting from context 0. In the three afternoon rounds this took 43-47 min of each 63-81 min round and about two thirds of the finder's thread time: 201 attempts at the 150,000-node cap, 30.2 M nodes thrown away, against 14.5 M nodes in the 432 trees closed.
- **HEURISTIC model:**
  - The current loop needs about 106 h at 4 threads (89 h of it re-walking) for one pass over the remaining 7,002 contexts. It can never close the roughly 238 contexts above its cap.
  - Skipping known too-big contexts (fastbb2 already has `--ctx=`) and adding one separate worker without a low cap: about 17.5 h at 4 threads, plus 20-25 thread-hours.

## Data and method
- Data root: W = /home/jay/research/data/es308-20261114, read only.
- Finder logs: the 51 finder logs and receipts W/runs/b35s20/<tag>.log|json on the live packet bb (the 5 bb-v9test logs are excluded).
  - One JSON event per line: start; closed (nodes, seconds, elapsed); context_too_big (nodes_so_far); WITNESS.
  - Run start = receipt finished - seconds.
- Loop events: W/continuation-b35s20v10a|b/events.json.
- Contexts: W/runs/b35s20/bb/contexts.json. Each of the 8,065 contexts fixes 14 master states as missing or occupied, so |missing| + |occupied| = 14.
- Rows: W/inputs/b35s20-v100..v142.
- Finder source: FASTBB20261113/tools/fastbb2.cpp (same SHA-256 as fastbb-20261113/p2/src/fastbb2.cpp).
- Consistency checks:
  - The 987 closed events match the 987 ctx-*.json.gz files.
  - Their node sum, 43,712,345, equals the branch + leaf count read directly from the files by my own C++ scanner rowscan.cpp. The scanner also counts row use in every weighted leaf (21,856,666 leaves).
  - The rows.txt of v100..v142 are append-only: each is a prefix of the next. Row indices are therefore stable:
    - base rows 0-2649;
    - capacity rows 2650-2651;
    - coupled rows 2652-3671;
    - appended rows 3672-4162 (491 rows in 51 batches).
- Scripts and derived data are in /home/jay/research/data/roadmap-20261115/pm1115/a2/:
  - scripts: runs.py, q1.py, q1b.py, tbhist.py, q2.py, q3.py, q3b.py, q4.py, q4b.py, q4sim.py, q4sens.py, q4cap.py, rowscan.cpp;
  - derived data: runs.json, tb.json, q3_rows.json, q4_strata.json, closed_at.json, rows*.tsv, ctx*.tsv.
  - All ran in the foreground, single-threaded, each under a minute.

## Q1. Closed contexts over time (COMPUTED)

Counts at key times:
- 54 (05:14), 55 (06:24), 129 (06:55), 247 (07:44), 294 (08:12), 483 (08:53), 555 (09:35).
- No loop ran 09:35-13:12.
- 674 (14:34), 677 (15:20), 711 (15:28), 905 (15:43), 905 (15:58), 905 (16:27), 980 (16:42), 987 (16:47).

| round | thr | run | re-walk prefix min | forward min | first-attempt closes | re-attempt closes | fwd closes/h | mean nodes of first-attempt closes | too-big attempts | witnesses | too-big share of thread time |
|---|---|---|---|---|---|---|---|---|---|---|---|
| c134s1 | 6 | 06:24-06:55 | - | - | 0 | 74 | - | - | 18 | 2 | 0.28 |
| c135s1 | 6 | 06:55-07:44 | 35.9 | 12.6 | 65 | 53 | 308 | 48,582 | 45 | 4 | 0.44 |
| c136s1 | 6 | 07:45-08:12 | 22.4 | 4.3 | 38 | 9 | 528 | 34,983 | 39 | 2 | 0.68 |
| c137s1 | 6 | 08:13-08:53 | 19.4 | 20.7 | 189 | 0 | 547 | 29,405 | 46 | 2 | 0.54 |
| c138s1 | 6 | 08:53-09:35 | 23.9 | 17.5 | 70 | 2 | 240 | 63,789 | 58 | 5 | 0.64 |
| c139s1 | 4 | 13:13-14:34 | 43.5 | 37.6 | 110 | 9 | 176 | 58,566 | 66 | 1 | 0.57 |
| c140s1 | 4 | 14:35-15:43 | 46.5 | 21.5 | 227 | 4 | 632 | 19,470 | 63 | 1 | 0.65 |
| c141s1 | 4 | 15:43-16:46 | 44.1 | 18.8 | 81 | 1 | 259 | 24,814 | 72 | 3 | 0.84 |
| c142s1 | 4 | 16:47- (live) | >18 at 17:05 | | 0 | | | | 24 so far | | |

Column notes:
- re-walk prefix = time until the first close of a context never attempted before;
- too-big share = (too-big attempts x 150,000 nodes) / (the run's node rate x threads x seconds).

Why the curve jumps:
- **Mechanism.** fastbb2 solve puts every context without a ctx file on its to-do list, in ID order. The loop restarts it every round, and run_tree_v5.py stops it 600 s after its first witness. So each round first re-attempts all known too-big contexts (no new closes for 43-47 min in the afternoon), then closes new contexts quickly until 600 s after the first witness.
- **711 -> 905, all between 15:28 and 15:43.** This is the forward phase of c140s1 over ids 741-969, a region of small trees:
  - mean 19,470 nodes, against 58,566 in c139s1's forward phase;
  - mean |missing| 5.80 against 5.42;
  - 30 % of ids 741-969 have |missing| >= 7, against 13 % in 500-740.
  - The count then stayed at 905 from 15:43 to about 16:27 while c141s1 re-walked.
- **It was not new rows unlocking old contexts.** Of the contexts attempted before, only 4 closed in c140s1:
  - 74, 218 and 625, at 149,367, 149,905 and 147,285 nodes, just under the cap, after 6, 5 and 1 failed attempts;
  - 710, the previous witness context, cut by the v140 rows.
  - The other 227 were first attempts.
  - The LP does use the newest rows widely: 184 of the 231 c140s1 trees use one of the 8 v140 rows, all 119 c139s1 trees use a v139 row, 40 of the 82 c141s1 trees use a v141 row. That shows use, not necessity.
- **Morning jumps.**
  - The cap rose from 50k to 150k at 06:24. c134s1 then closed 74 contexts, all of which had been too big at 50k; c135s1 closed another 53.
  - c137s1's forward phase covered ids 328-530 (mean 29,405 nodes).
  - The morning ran 6 threads; the afternoon runs 4.

## Q2. Nodes per closed context; contexts above the cap (COMPUTED except where marked)

Closed trees:
- 987 trees, 43,712,345 nodes.
- Mean 44,288; median 35,365; p10 3,993; p25 11,825; p75 65,669; p90 103,075; p95 126,623; p99 147,961; max 149,905.
- Histogram: <5k 115; 5-10k 105; 10-20k 125; 20-50k 294; 50-100k 241; 100-150k 107.
- Node rate: 885 nodes per thread-second (49,396 thread-seconds).

Open contexts known to exceed 150,000 nodes: **72**.
- Ids: 0, 33, 51, 80, 81, 96, 97, 100, 101, 102, 113, 129, 132, 133, 137, 140, 142, 143, 152, 153, 154, 163, 178, 180, 184, 186, 188, 190, 204, 208, 209, 210, 216, 219, 220, 221, 252, 254, 329, 518, 521, 522, 528, 529, 531, 534, 538, 540, 542, 545, 580, 582, 624, 644, 657, 664, 680, 704, 705, 708, 712, 716, 720, 1024, 1026, 1030, 1041, 1042, 1043, 1044, 1052, 1053.
- Attempts at 150k so far (attempts: contexts): 1: 9, 3: 11, 4: 8, 5: 6, 6: 1, 7: 23, 8: 3, 9: 11.
- Also open: the witness contexts 1040, 1046 and 1060, and 1061 (in progress when c141s1 stopped). Every context from 1063 to 8064 (7,002 in all) has never been attempted.

Retries rarely pay:
- Of the 86 contexts ever too big at 150k, 14 closed later, all at 115,861-149,905 nodes (12 of them above 141,000).
- Since 14 Nov 23:11, completed runs threw away 219.1 M nodes in too-big attempts: 3,160 attempts at the 50k cap (158.0 M) and 407 at 150k (61.1 M).
- That is 68.8 thread-hours thrown away, against 43.7 M nodes (13.7 thread-hours) in closed trees.

Size by |missing| (stratum):

| missing | contexts | closed | median | mean | open too-big | untried |
|---|---|---|---|---|---|---|
| 0-1 | 14 | 10 | 46,564 | 62,196 | 2 | 2 |
| 2 | 78 | 43 | 61,495 | 71,420 | 7 | 27 |
| 3 | 286 | 112 | 64,716 | 70,114 | 20 | 153 |
| 4 | 715 | 190 | 49,777 | 60,343 | 31 | 492 |
| 5 | 1,287 | 250 | 41,106 | 47,972 | 7 | 1,030 |
| 6 | 1,714 | 207 | 19,679 | 30,006 | 4 | 1,503 |
| 7 | 1,706 | 119 | 10,627 | 17,383 | 1 | 1,586 |
| 8 | 1,256 | 45 | 5,753 | 8,557 | 0 | 1,211 |
| 9-13 | 1,009 | 11 | 863 (k=9) | 4,268 (k=9) | 0 | 998 |

- Too-big fraction among attempted contexts: 14.5 % at |missing| <= 4, 2.4 % at 5-6, 0.6 % at >= 7.
- Stratum means are stable along the ID order (ids <500 vs >=500): k=4 60.9k/59.6k, k=5 48.1k/47.8k, k=6 33.0k/28.2k, k=7 23.7k/15.3k.
- HEURISTIC: about 166 more of the untried contexts are expected above 150k (about 238 in all), about 20 of them in ids 1063-1499.

## Q3. Which appended rows do the work (COMPUTED; use is not necessity)

Over the 21,856,666 weighted leaves of the 987 closed trees:

| rows | count | used | leaves using >=1 | share of certificate weight |
|---|---|---|---|---|
| base 0-2649 | 2,650 | 2,538 | (1.0 % of leaves use base rows only) | 91.2 % |
| capacity 2650-2651 | 2 | 2 | 98.7 % | 4.2 % |
| coupled 2652-3671 | 1,020 | 832 | 90.1 % | 2.4 % |
| appended 3672-4162 | 491 | 475 | 83.8 % | 2.2 % |

- Every appended row that existed before the last close is used in some closed tree. The 16 unused rows are v142's, appended after the last close.
- Top rows by leaf references (row, batch, |S|, references, trees using it / trees closed after it existed):

| row | batch | \|S\| | references | trees using / available |
|---|---|---|---|---|
| 3675 | v101 | 9 | 1.70 M | 936/986 |
| 3953 | v129u | 9 | 1.47 M | 901/941 |
| 3781 | v116u | 13 | 1.46 M | 287/960 |
| 3819 | v119u | 12 | 1.42 M | 196/956 |
| 3792 | v117u | 13 | 1.27 M | 256/957 |
| 4018 | v134u | 9 | 1.22 M | 904/933 |
| 3676 | v101 | 9 | 1.16 M | 935/986 |
| 3677 | v101 | 9 | 0.99 M | 935/986 |
| 4026 | v134u | 9 | 0.93 M | 787/933 |
| 3965 | v130u | 12 | 0.92 M | 179/940 |

- Top batches by references: v134u (13 rows) 4.47 M; v101 (7) 4.28 M; v119u (19) 2.69 M; v116u (15) 2.36 M; v126u (19) 2.11 M; v129u (10) 2.09 M; v127u (13) 1.99 M; v131u (14) 1.79 M.
- Afternoon batches get fewer references per available tree: v139w2u 991 (432 trees), v141w1u 363 (82), v140w1u 207 (313), against 4,793 for v134u.
- Small supports do the broad work: |S| = 9 rows (44 of them) appear in 68 % of the trees closed after them; |S| = 12-14 rows (428) appear in 27-29 %.
- Witnesses cut, over the 54 distinct witnesses logged on the packet:
  - 412 rows cut exactly one witness (their own) and 66 cut two;
  - 13 cut three or more: 3792 (v117u) 11, 3732 (v109p) 7, 3837 (v120u) 7, 3965 (v130u) 6, 4020 and 4023 (v134u) 4 each.
- The 8-rows-per-witness cap:
  - Since v135 every batch stopped at 8 accepted rows while 9-23 candidates were available.
  - All 168 rows tried were certified, at about 1.7 s per row (cuts-v142w2u: 8/8 in 14.1 s).
  - The 104 candidates left out would have cut 2 later witnesses: 586 (c138s1) and 812, the only witness of round c140s1. This is HEURISTIC, because those candidates are uncertified.

## Q4. Remaining effort (HEURISTIC)

Method: an expected-value model by stratum (|missing|).
- Each untried context gets its stratum's mean closed size, too-big fraction and witness rate. Witness rates come from the 150k-cap rounds: 18 witnesses in 840 newly attempted contexts.
- Node rate 885 nodes per thread-second.
- A round ends 600 s after its first witness.
- Each round re-walks the current too-big list at 150,000 nodes per context, plus 60 s and 30 s per witness of row work, plus the in-progress contexts lost at the stop.
- Too-big sizes come from censored log-normal fits: E[size | >150k] is about 265-330k (median about 220-230k), and P(>1M | >150k) is about 1-3 %. The fit overstates the too-big fraction at |missing| 5-6 (7.5 % against 2.4 % observed), so treat it as rough.
- Backtest: the same accounting gives 2.4 h + 1.1 h = 3.5 h for the three afternoon rounds; observed 3.55 h.

Results:
- **Untried contexts (7,002):**
  - about 174 M nodes of trees that close under the cap: about 25k per context, against 44k for the closed ones, because most untried contexts have |missing| >= 5;
  - about 166 new too-big contexts (238 in all);
  - about 93 witnesses.
- **Near term:** ids 1063-1499 are harder (22 % have |missing| <= 4): about 16 M nodes, 20 new too-big contexts, 8 witnesses.

| variant | wall time for one pass | of it re-walk | rounds | contexts left above cap |
|---|---|---|---|---|
| current loop, 4 thr (cap 150k, grace 600 s) | 106 h | 89 h | 46 | 238 (never closed by this loop) |
| current, 6 thr | 59 h | 47 h | 37 | 238 |
| current, 12 thr | 21 h | 15 h | 23 | 238 |
| current, 4 thr, grace 3,600 s | 43 h | 27 h | 14 | 238 |
| current, 4 thr, cap 300k | 72 h | 52 h | 48 | 67 |
| skip known too-big, 4 thr, cap 150k | 17.5 h | 0 | 46 | 238 |
| skip, 4 thr, cap 300k | 20 h | 0 | 48 | 67 |
| skip, 6 / 12 thr | 12 h / 6.2 h | 0 | 37 / 23 | 238 |

Sensitivity (current / skip, 4 threads):

| change | current loop | skip-list loop |
|---|---|---|
| witness rate x0.5 | 77 h | 16.9 h |
| witness rate x2 | 138 h | 18.2 h |
| node rate -15 % | 135 h | 20.5 h |
| stratum means x1.3 | 123 h | 21.9 h |
| stratum means x0.7 | 88 h | 13.1 h |

Too-big pass:
- About 238 x 265-330k = 63-79 M nodes, about 20-25 thread-hours. The 72 known now need only 6-7.5 thread-hours.
- Total with skipping: about 174 M + about 25 M of first attempts that hit the cap + 63-79 M = about 260-280 M nodes, or 82-88 thread-hours. That is about 22-24 h at 4 threads or about 8 h at 12, followed by the fresh replay and the independent checker.
- The whole tree implied (44 + 174 + 63-79, about 280-300 M nodes) agrees with the 02:50 Knuth estimate of 3.3e8.

## Q5. Proposals for the next session

1. **Skip known too-big contexts in the frontier finder.**
   - fastbb2 already supports --ctx=a,b,c (only those contexts, still in ID order). Only a new runner version is needed, passing the open contexts minus the too-big list. fastbb2 and the trusted check_tree replay stay unchanged.
   - Evidence: a 43-47 min re-walk prefix per afternoon round and 67 % of afternoon thread time. Model: 106 h -> 17.5 h at 4 threads.
   - Retries at the same cap almost never pay (14 of 86, all just under the cap).
2. **Add one separate worker for the too-big list, never stopped at witness rounds.**
   - Command shape: fastbb2 solve <latest rows> ... --ctx=<too-big list> --max-ctx-nodes=3000000 (or more) --on-witness=continue, on 1-2 threads.
   - It shares runs/b35s20/bb through fastbb2's claim files, which are built for several processes on one packet.
   - Rows are append-only (checked v100-v142), so trees closed on an older version stay valid for the final replay.
   - Its witnesses must be fed into the row batches, because the frontier finder no longer visits those contexts. Witnesses do occur deep in big contexts: 1060's appeared at 135,723 nodes.
   - Cost: about 6-7.5 thread-hours for today's 72 contexts.
3. **--max-ctx-nodes: keep 150k-300k for the frontier.**
   - The night's 50k cap threw away 158 M nodes and closed only 54 contexts by 05:14. Of the 183 contexts too big at 50k, 150 have closed since (median 82,788 nodes).
   - If proposal 1 cannot be done, 300k alone (a parameter change) cuts the modelled pass from 106 h to 72 h and leaves 67 contexts instead of 238.
   - The cost: each stop loses more work. fastbb2 has no SIGTERM handler, so in-progress contexts are lost at every slice stop.
4. **--slice-seconds (grace) matters only while re-walks remain.** 600 -> 3,600 s gives 43 h instead of 106 h at 4 threads. With proposal 1 it only moves 17.5 h to 16.2 h.
5. **Ordering.** Once re-walks are gone, ID order is fine. Size depends strongly on |missing|. The frontier ahead is easier on average but has pockets with 18-22 % of contexts at |missing| <= 4 (ids 1063-1499, 2000-2999, 4000-4999). Report progress per stratum, not as a raw context count.
6. **More rows per witness.** Raise --accept-per-witness from 8 to about 24. Each row costs about 1.7 s and all 168 tried rows certified; the left-out candidates would have cut 2 later witnesses, one of them a whole round's only witness. Prefer small supports: |S| = 9 rows appear in 68 % of later trees, |S| = 13 rows in 29 %.
7. **Threads.** Even without re-walks one pass takes about 17.5 h at 4 threads and 6 h at 12, within the 16-thread cap shared with other tracks.
8. **(21,14).** ES(8) <= 307 also needs (21,14) (Knuth 1.85e9 nodes, about 6x (20,15)) unless N66 <= 55 removes it. With re-walks it would be far worse, so proposals 1 and 2 come first.

## What remains
- Not checked:
  - whether any appended row is necessary for any tree (that needs an ablation run, which was outside this track);
  - the actual sizes of the too-big contexts, which are only known to exceed 150,000 nodes.
- Re-run q1.py / q1b.py after the next rounds to test the model. It predicts about 20 new too-big contexts in ids 1063-1499.
