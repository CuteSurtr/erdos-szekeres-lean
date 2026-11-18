# STATUS20261118: session of 18 November 2026 (from 02:20 KST)

**Status: FINISHED 12:45 KST, 18 November 2026. Nothing runs.**  Results: ES(8) ≤ 307 (PROVED, computer-assisted; [ES307N20261118](../ES307N20261118/README.md)); N66 ≤ 55 CERTIFIED; saturation numbers sat_g(6..10) ≤ 12, 16, 27, 40, 52 ([SATG20261118](../SATG20261118/README.md)); cleanup 103.5 GB (owner-approved).
- The previous handoff, [STATUS20261116_1900](../STATUS20261116_1900/README.md), with
  [STATUS20261115_2300](../STATUS20261115_2300/README.md), stays the reference for everything not changed here.
- **At the owner's request (about 12:55 KST) everything under `archive/` was committed and pushed to `main`** (one commit on
  top of 8621eb159; `.claude/` and `AGENTS.md` left untracked as before). Deletions: only the owner-approved cleanup of
  12:18 (below). Nothing was published or e-mailed; public wording and e-mails remain the owner's decisions.

The owner's message (about 02:15 KST): "continue where we left off and try to find whatever is novel, now go. go as
furthest as you can." No end time was given; the main session chose a compute deadline of 18 Nov 18:00 KST (units end
by themselves; it can be extended) and agent waves of about six hours.

## Aim

ES(8) ≤ 307 by route A of [ROUTE307_1116.md](../ROADMAP20261115/ROUTE307_1116.md) (claim `p307-chain`, CONFIRMED):
N66 ≤ 55 (level-14 cubes, 22 leaves open at the start, 94.1 % by measure) **and** the budget-35 slice (20,15) EXACT TREE
(1,652 of 8,065 contexts closed at the start; about 53 thread-hours of frontier left by AS's lower estimate, plus the
high-cap contexts). Then verification. Side tracks: Δ theory, lower bounds, a novelty map.

## What runs (started 02:24 KST)

| unit / workflow | job | deadline |
|---|---|---|
| `esr-memguard-1118` | memory guard, 24,000 MB total (log `/home/jay/research/data/memguard-20261118.log`); tracks n66=17000 lo=3200 mainv=3000 agv=3000 agu=1500 agp=1500 agl=1500 ags=1200 agd=1500 agt=600 | stopped by the main session |
| `esr-n66-driver-r7` + up to 5 `esr-n66-cube-*` | N66 ≤ 55 cubes; `W/p2c14_driver_r7.py` = r6 with deadline 18 Nov 18:00, partial files of timeouts kept uncompressed (no zpart unit; the older partials were deleted by the owner on 16 Nov); state backup `p2/c14/campaign_status.json.bak-20261118-r7start` | 18:00 |
| `esr-lo-b35s20v11c` | (20,15) loop, `continue34_v11.py --start-version=148`, no receipt, **6 frontier threads + 1 extra worker** (cap 300k), CPUQuota 700 %, MemoryMax 3G, output `continuation-b35s20v11c` | 18:00 |
| workflow `wf_bcb76724-6d7` (wave A) | R (review of AS's v12 side pass), P307V (307 verification prep), VB, VS, AU ((20,15) batch audits), NOV (novelty map + watch), T (Δ theory), L (lower bounds); then critic C | 08:30 |

W = `/home/jay/research/data/n66-20261113` for N66; the (20,15) work directory is `/home/jay/research/data/es308-20261114`.
Thread budget: 0.2 (guard) + 4.96 (N66) + 7 ((20,15)) + at most 3.3 for the agents ≤ 16.

The three claims of 16 Nov whose verifiers were stopped had stale locks; these were renamed to `<id>.lock.stale1116`
in `/home/jay/research/data/roadmap-20261115/pm1115/claims/` so that today's verifiers can take them.

## Results

### Log (main session)

- **02:49** N66: `ohoooo_40o_52o_46h` (1,236.7 s wall, 1.56 M conflicts) and `oohooo_40o_52o_46h` (1,287.8 s, 1.28 M)
  certified ok by the driver at the first attempt; 112 of 132 leaves, 484/512 = 94.5 % by measure (driver's own
  acceptance; the four independent checks are VB's job). No cube SAT.
- **02:49** (20,15): 1,978 of 8,065 contexts closed (1,652 at 02:24), about 780 per hour with 6 + 1 threads (COMPUTED
  count, HEURISTIC rate). Finder slice c148s3 (02:24-02:38) found 2 witnesses; round 148 appended as `b35s20-v149`
  (16 certified rows in 2 batches, 02:39). The batch audit is track AU's job.

- **03:07** N66: `ooohoo_40o_52o_46h`, `ohohoo_23o_40o_52o`, `oohhoo_23o_40o_52o` and `oooooo_40o_52o_46h_44h` also
  certified ok (1,213-2,279 s wall); 116 certified; the two never-run 1/64 base cubes `oooooh` (03:04) and `hooooo`
  (03:07) are running.
- **03:08 high-cap side pass launched.** Track R's review [V12_REVIEW.md](../LO33N20261113/budget34/tools/V12_REVIEW.md)
  (verdict **READY WITH NOTES**, claim `r-v12-review-1118`) cleared `highcap_v1.py` (`1642fb3b…`, hash checked before
  launch) against the live v11 loop. Unit `esr-lo-highcap-1`: exactly the review's §6.1 command except CPUQuota 85 %
  instead of 100 % (thread cap: 14.66 threads in use before the launch); side packet `runs/b35s20/bb-hc1`, logs
  `bb-hc1-logs/` (status.json), inbox `bb-hc1-inbox/`; `--above=300000` (= the loop's extra cap) `--cap=1000000
  --rss-mib=600 --import`, rerun every 10 min until 17:50. First status: version v150, 5 selectable contexts. Its
  witnesses wait in the inbox until the loop is restarted with v12 (review §6.2, note N2); its closures are imported
  directly after the review's checks; the final replay re-checks every file.

- **03:58** N66: both never-run 1/64 base cubes certified at the first attempt: `oooooh` (2,137 s wall, 3.92 M
  conflicts) and `hooooo` (2,748 s, 5.94 M); also `oooooo_40o_52h_46o_44h`, `oooooo_40h_52o_46o_44h`,
  `ooohoo_40h_52o_46o`, `ooooho_40o_52o_46o`, `oohooo_40o_52o_46o`. **123 certified leaves, 507.5/512 ≈ 99.1 % by
  measure** (driver acceptance); 9 leaves open (5 running, 4 queued), open measure 4.5/512. VB's four checks keep pace
  (112 of 112 at 02:52, [VERIFY_N66CUBES_1118.md](../N66N20261113/cubes20261115/VERIFY_N66CUBES_1118.md)).
- **03:58** (20,15): 2,354 of 8,065 closed; rounds 148-153 appended v149-v154 (21 witnesses in 6 finder slices of
  11-18 min, each witness cut by certified rows); rate about 400 per hour now (HEURISTIC; contexts grow). Side pass
  `esr-lo-highcap-1`: 4 contexts above 300k closed and imported, 2 selectable, no witness. Track AU audits each batch
  ([AUDIT_1118.md](../LO33N20261113/budget34/AUDIT_1118.md)).

- **04:24** N66: 129 certified leaves (511.25/512 ≈ 99.85 % by measure); the last three pieces run
  (`oooooo_40h_52o_46o_44o`, `…_44o_45o_39o`, `…_44o_45o_39h`); the queue is empty.
- **04:25 Saturation numbers (track L, the strongest new item of the night so far).** With DDSZ's definition
  (arXiv:2312.01223: n-gon-free, and every added point in general position lies on a convex n-gon; their Thm 4 gives
  sat_g(7) ≤ 28 and sat_g(8) ≤ 56): **sat_g(6) ≤ 14, sat_g(7) ≤ 20, sat_g(8) ≤ 31** by explicit integer point sets
  ([LOWERBOUND_RUN_1118.md](../ROADMAP20261115/LOWERBOUND_RUN_1118.md) item (1c); claims `lb-l18-satg6-14`,
  `lb-l18-satg7-20`, `lb-l18-satg8-31`, `lb-l18-satg8-36`). Evidence: CERTIFIED (l1enc + realizability clauses, cake_lpr)
  + PROVED soundness, each confirmed by an independent verifier (VS/VB) with own code; in addition **EXACT, SAT-free**:
  every open cell of the line arrangement tested exactly, 0 failures — the 20-point heptagon sets by VB (14,960 cells),
  the 31-point octagon set (95,760 cells = Euler count) and the 36-point set (178,570) by the main session's verifier
  ([VERIFY_LOWERBOUND_L18_SATG8_CELLS.md](../ROADMAP20261115/VERIFY_LOWERBOUND_L18_SATG8_CELLS.md); negative controls
  fail as they must, positive controls pass). Literature: no bound after DDSZ found, and no citing work of DDSZ found
  ([WATCH_1118.md](../NOVELTY20261115/WATCH_1118.md) §2f) — "not found in this search", not a priority claim; unrefereed.

- **04:28 N66 ≤ 55 CERTIFIED (cover complete).** The last three pieces certified at the first attempt
  (`oooooo_40h_52o_46o_44o` 1,321 s; `…_45o_39o` 766 s; `…_45o_39h` 812 s); driver r7 final 04:28:08: **132 of 132
  leaves accepted, COVER_OK**; no cube was SAT in the whole campaign. Main session's independent cover check with
  P307V's `VERIFY307/tools/n66_cover_check.py --deep` (`5087351e…`): **COVER COMPLETE**, 132 accepted, 0 rejected,
  0/16,384 assignments of 14 split states uncovered (`pm1115/main1118/n66_cover_final_main.json`). VB's four checks:
  25 of today's 27 cubes at 04:28 (the other 105 cubes by earlier records), rest in progress. Claim
  `n66-le55-cubes-1118` filed for a final verifier. Record line added at the top of
  [N66N20261113/README.md](../N66N20261113/README.md). **This is one of the two inputs of ES(8) ≤ 307 (route A); the
  other, (20,15), is open.**
- **04:29 (20,15) loop switched to v12 with N66's threads.** `esr-lo-b35s20v11c` stopped in finder stage c155s1 (safe
  point; events end `FINISHED`, version 155, stopped); 2,559 contexts closed then. New unit `esr-lo-b35s20v12a`:
  `continue34_v12.py` (`ab93d16f…`, reviewed READY WITH NOTES in V12_REVIEW.md) with `run_tree_v7.py` (`7bde01a9…`),
  `--start-version=155`, no receipt, **`--threads=9 --extra-threads=3`**, CPUQuota 1200 %, MemoryMax 3G, the other v11
  options unchanged (`--max-ctx-nodes=150000 --extra-cap=300000 …`), `--inbox=runs/b35s20/bb-hc1-inbox`, output
  `continuation-b35s20v12a`, deadline 18:00. Threads after the switch: 15.35 of 16 allotted.

- **04:45 wave A stopped at the owner's request** ("es 1118 is taking way too much tokens, we should tone it down").
  Workflow `wf_bcb76724-6d7` was stopped (R had finished; P307V, VB, VS, AU, NOV, T and L were stopped mid-task; the
  critic never ran). Their records were written incrementally and stay as they are. Their autonomous units were left
  to run to their own deadlines (all by 08:20; no tokens): AU's audit driver `esr-agu-driver2` (follows both
  `continuation-b35s20v11c` and `…v12a`, rewrites AUDIT_1118.md itself), VB's N66 driver `esr-agv-vb-alldrv` (four
  checks, rewrites VERIFY_N66CUBES_1118.md itself), P307V's `esr-agp-chain2`, VS's `esr-agv-vs-tree2015`, L's
  `esr-agl-satlocal2`/`satlocal3b`/`e72t`, T's `esr-agt-anchorl6full`. Their outputs are collected later. No new agents
  until the owner says so; the main session checks the runs about once an hour.

- **04:47** One agent at a time from now on (owner): agent SAT2 (saturation record `SATG20261118` + push to smaller
  sets and n = 9; exact cell checks; deadline 08:00).
- **05:42** (20,15): **4,179 of 8,065 contexts closed** (+1,538 in the hour since 04:42, about 1,500 per hour with 9 + 3
  threads; HEURISTIC rate); rows up to v159 (every witness cut). Open contexts recorded too big: 38 (36 in the
  150k-300k band of the extra worker, 2 above 300k for the side pass, none above the side cap of 1M). The frontier is
  near context 4,225 of 8,065 (ID order).

- **06:42** (20,15): 4,688 closed; rows up to v162; rate down to about 500 per hour (harder contexts); 43 open
  too-big (42 in 150k-300k, 1 above 300k).
- **07:40 Saturation, agent SAT2** (record [SATG20261118](../SATG20261118/README.md); 12 claims `sat2-*`): smaller
  saturated sets, each checked by the exact cell enumeration of vx1118 (cells = Euler count, 0 failures, trusted
  replay `check_cells.py`; for n = 9 a copy of the finder without its brute-force C(n,9) count):
  **sat_g(6) ≤ 12, sat_g(7) ≤ 16 (track L's set from unit `esr-agl-satlocal3b`, credited to L), sat_g(8) ≤ 27,
  sat_g(9) ≤ 48** (DDSZ Thm 4: 28, 56, 112; ES(n) − 1 = 16, 32, 64, 128). Label EXACT. Not reached (HEURISTIC): 11
  (n = 6), 15 and 17 (n = 7), 26 (n = 8), 47 (n = 9).
- **08:13 all 12 `sat2-*` claims CONFIRMED by VX2** with its own code (vertical-sweep cell enumeration, a different
  method from the finder's; cells = Euler count, e.g. 53,677 for the 27-point set and 587,077 for the 48-point set;
  0 failing cells everywhere; negative controls fail; for the 48-point set also brute force over all 9-subsets).
  The four headline bounds now rest on two independent exact implementations. Unrefereed; literature status "not found
  in this search" (WATCH_1118 §2f).

- **08:15 outputs of the stopped wave's autonomous units** (all ended by 08:15):
  - AU's audit driver: **79 batches, 714 rows audited, no FAIL** (own encoder, fresh cake_lpr, witness cut; every
    append check exit 0) — [AUDIT_1118.md](../LO33N20261113/budget34/AUDIT_1118.md). Batches appended after 08:15
    still need the audit.
  - VB's N66 driver: four checks on every certified cube; "Four-check verified cover (own code): 100.00 % = COMPLETE"
    ([VERIFY_N66CUBES_1118.md](../N66N20261113/cubes20261115/VERIFY_N66CUBES_1118.md)).
  - P307V's chain2: LRAT re-check of every row of `b35s20-v155` (rc 0), rows-stated check v155 (rc 0), early check of 580
    closed (20,15) contexts (30.9 M nodes) by tcheck and pycheck: 0 errors, 15,469,755 leaves compared, 0 differences
    (`pm1115/p307v/chain2.status`).
  - T's `anchorl6_m15.cnf` (ANCHOR-L(6) at 15 points): CaDiCaL UNSAT in 7,470 s, LRAT kept as zstd; cake_lpr not run
    (COMPUTED, not CERTIFIED).
- **08:16 (20,15) loop restarted with the freed threads:** `esr-lo-b35s20v12a` stopped in finder stage c166s1 (FINISHED,
  version 166, stopped); 6,193 closed then. New unit `esr-lo-b35s20v12b`, same command with `--start-version=166
  --threads=10 --extra-threads=4`, CPUQuota 1400 %, output `continuation-b35s20v12b`, deadline 18:00.

- **08:31 N66 ≤ 55: claim `n66-le55-cubes-1118` CONFIRMED twice** — VS at 04:33 (own cover code) and VN at 08:31 (own
  code: the 132 cubes partition the split exactly, 0 of 16,384 uncovered, 0 double; all 132 four-checked; every cert.cnf
  = F_c + its cube units byte for byte; fresh cake_lpr on `hooooo` (2.0 GB LRAT) and a random cube:
  [VERIFY_N66LE55_FINAL_VN.md](../N66N20261113/cubes20261115/VERIFY_N66LE55_FINAL_VN.md)). Line in the N66 README updated.
- **08:35** AU's audit driver relaunched as `esr-agu-driver3` (same code; follows v11c, v12a, v12b; to 18:15); it
  audited the v167 batches of the v12b loop at once (rc 0).
- **08:40** Agent SAT3 (saturation: n = 10, more seeds for n = 8, 9; new sets checked by VX2's independent checker;
  appends a section to SATG20261118; CPUQuota ≤ 45 %; to 12:30).

- **08:56 (20,15) frontier done: 8,037 of 8,065 contexts closed.** The v12b loop ended at version 169 with `OPEN`
  ("finder ended without a witness … only too-big contexts left"; the end phase N4 of V12_REVIEW). Open: 28 contexts
  recorded too big (25 in 150k-300k, 3 above 300k); the side pass had recorded context 4782 above its 1M cap
  (`bb-hc1/TOO_BIG.txt`: `4782 1000002 h16`); no inbox witness.
- **08:57 end phase.** Side pass `esr-lo-highcap-1` stopped (no leftover import file). Memory guard restarted as
  `esr-memguard-1118b` with lo = 6,500 MB (n66 cut to 1,000; other tracks as before). **Standalone high-cap pass**
  (V11_NOTES §4, the reviewed v6 tool, no loop on the packet): unit `esr-lo-hcpass169a`, `run_tree_v6.py 20 --budget=35
  --bb=bb --input-folder=b35s20-v169 --tag=hc169a --threads=14 --too-big-only --max-ctx-nodes=1000000
  --on-witness=continue --seconds=10800`, CPUQuota 1400 %, MemoryMax 5G. Witnesses go to its receipt
  `runs/b35s20/hc169a.json`, to be cut by a loop restart with `--start-version=169 --start-receipt=…`; contexts above
  1M (4782 at least) need the successor-packet split.

- **09:04** `hc169a` closed 10 of the 28 (8,047 closed) and then fastbb2 aborted with `std::bad_alloc` (exit −6, no
  witness): `run_tree_v6.py` sets RLIMIT_AS = 1,400 MB for its fastbb2 child (and an RSS guard at 1,200 MB), sized for
  3-4 threads; 14 threads reserve about 64 MB of address space each in glibc malloc arenas (peak RSS was only 800 MB).
  Packet consistent (master.json, contexts.json parse; no temp files). **09:06 relaunch** `esr-lo-hcpass169b`: same
  command with `--tag=hc169b --threads=6` and `MALLOC_ARENA_MAX=2` (allocation strategy only; nothing in the search
  changes), CPUQuota 600 %, MemoryMax 3G; 18 contexts to do (4782 is known above 1M from the side pass).

- **09:24** `hc169b` (6 threads): 17 of 18 closed, no witness (receipt exit 4, PARTIAL); peak RSS 506 MiB; **8,064 of
  8,065 closed**; only context 4782 open (too big at 1,000,001 nodes).
- **09:25 successor packet** `runs/b35s20/bb-s1` by `tools/prepare_successor_b35.py` (new copy of
  `prepare_successor.py` `bb84d1f0…` whose only change is the packet path `runs/s20` → `runs/b35s20`; SHA-256
  `10fad935…`): 8,064 closed context files hard-linked, three master files copied, hashes in `bb-s1/SUCCESSOR.json`;
  the original `bb` unchanged.
- **09:30 split of 4782** (`run_tree_v6.py 20 --budget=35 --bb=bb-s1 --input-folder=b35s20-v169 --split-open=4
  --tag=s1split --threads=6 --max-ctx-nodes=1000000 --on-witness=continue`, MALLOC_ARENA_MAX=2): 16 new contexts
  8065-8080, all closed in 318 s (1,263,178 nodes), no witness. **`DONE`: 8,080 of 8,080 contexts of `bb-s1` closed
  (COMPUTED). The (20,15) tree is complete as a computation; the exact replays (VERIFY307 T5-T7) decide it.**
- **09:32 final verification started (VERIFY307 checklist, the tools of track P307V):** memory guard restarted as
  `esr-memguard-1118c` (vf=12000 vl=5000 lo=1500 sat=3000 agu=1500 mainv=3000 n66=500);
  T1+T5+T6 `esr-vf-final2015` (`final_tree_check.sh runs/b35s20/bb-s1 b35s20-v169 … 6 20 15`: prep_rows, tcheck_b35,
  pycheck_b35 in 6 shards, compare; 600 %, 11G); T4 `esr-vl-lrat169` (fresh cake_lpr on every rhs-1 row of v169; 600 %,
  5G). **T2 rows_stated (own code of P307V): ok** — v169 = 4,642 rows (1,020 base + 970 appended rows from 111 batch
  folders over 69 rounds + the two capacity rows), no problem.

- **09:36 T3 (batch audits) complete:** every one of the 111 batch folders `cuts-v101…v169*` with accepted rows has an
  audit folder `budget34/audit/cuts-<batch>/summary.json` with label CERTIFIED; together **970 rows** (= T2's appended
  rows), each with own-encoder match, fresh cake_lpr acceptance and cutting its batch's witness (main session's count
  over the summaries; 0 batches with a failed row).

- **09:55 T1 + T5 + T6: EXACT TREE (tcheck_b35 + pycheck_b35)** for the (20,15) slice, packet `runs/b35s20/bb-s1`,
  rows `b35s20-v169` (`pm1115/p307v/final-b35s20-v169/verdict.json`): problems none; **8,080 contexts, 238,116,145
  nodes, 119,054,033 leaves, minimum margin 1**, 4,642 rows; prep_rows rc 0 (capacity rows exactly (F, 20) and
  (Lo, 15), every other row rhs 1); tcheck rc 0; 6 pycheck shards; compare rc 0 (equal node totals per context).
- **09:56 T4: every rhs-1 row of v169 re-certified**: 1,990 rows, 1,994 fresh cake_lpr jobs, all ACCEPTED, no hash
  mismatch, no rejection (`pm1115/p307v/lrat-b35s20-v169/lrat-summary.json`).
- **09:58 T7 started** (the project's trusted replay, `audit/fresh_replay_v3.py b35s20/bb-s1 b35s20-v169
  fresh-b35s20-v169-bbs1 3`, unit `esr-vf-fresh169`, 300 %, 17G; guard restarted as `esr-memguard-1118d` with vf=18000).

- **10:51 T7: EXACT TREE (fresh full replay, no receipts reused)** — `audit/fresh-b35s20-v169-bbs1/summary.json`:
  8,080/8,080 contexts, 238,116,145 nodes (= tcheck = pycheck), 119,054,034 leaves, minimum margin 1, global pending 1
  = "state 0 missing" only.
- **10:55 ES(8) ≤ 307 (PROVED, computer-assisted; every item of VERIFY307 §1 passed).** Record
  [ES307N20261118](../ES307N20261118/README.md) written (headline, inputs, chain, checklist with results, files and
  hashes, small outputs in `data/`). Claim `es307-final-1118` filed for a final independent read. Not Lean-checked as
  a whole; unrefereed; uncommitted; public wording is the owner's decision. AU's idle driver stopped (no batches left).

- **10:57** T's `anchorl6_m15.cnf` (ANCHOR-L(6) at 15 points): **CERTIFIED** by a fresh cake_lpr run of the main
  session on the kept LRAT (heap 4,000 MB; T's 500 MB heap had been exhausted); addendum in
  [THEORY_1118.md](../DELTA3N20261113/attack20261115/THEORY_1118.md).

- **11:50 Saturation, agent SAT3** (section "SAT3 addendum" of [SATG20261118](../SATG20261118/README.md); claims
  `sat3-satg9-40`, `-44`, `sat3-satg10-52`, `-56`, `-60`, `-64`, `-68`): **sat_g(9) ≤ 40** (was 48) and **sat_g(10) ≤ 52**
  (DDSZ Thm 4: 112 and 224), 4-fold symmetric integer sets; each passed VX2's independent exact checker run unchanged
  (cells = Euler count, 0 failures, 1,000 method-B samples; point-0 deletion fails), the 40-point set also by brute force
  over all 9-subsets. n = 8 stays at 27. Sizes so far for n = 6..10: 12, 16, 27, 40, 52. Finder-only (COMPUTED, too large
  for VX2's checker): 72, 76 and 83 points at n = 10.
- **11:55** second implementation on SAT3's seven sets: vx1118's finder (SAT2's no-brute-force copy) + vx1118's trusted
  replay `check_cells.py` (`4b6cd648…`), unit `esr-mainv-vx1118sat3` (results `pm1115/main1118/vx1118sat3/status.jsonl`).
  Agent VR started: final independent read of `es307-final-1118` (own tcheck_b35 run on `bb-s1`, split integrity).

- **12:04 ES(8) ≤ 307: claim `es307-final-1118` CONFIRMED by VR** (final independent read: own derivation of the
  chain and of the Lean signatures; every evidence file and hash matches; own rebuild of tcheck_b35 (`a8c4f810…`) on
  `bb-s1`: EXACT TREE, 8,080 contexts, 238,116,145 nodes, minimum margin 1, 0 pending, byte-identical to the 09:31 run;
  split checked node for node; [VERIFY_ES307_FINAL.md](../ES307N20261118/VERIFY_ES307_FINAL.md)). Its wording notes
  W1-W8 were applied to the record and to VERIFY307's header (12:40). Nothing affects the bound.
- **12:40** owner: "do not add new agents please" — no agents from now on; compute units only.
- **12:40** second implementation on SAT3's sets (vx1118 finder + its trusted replay): 40 (n = 9), 44, 52 (n = 10), 56
  all SATURATED (cells = Euler count, 0 failures in both programs); 60, 64, 68 running.

- **12:18 cleanup (owner-approved groups A, B, C, F; D and E not approved, kept)** — tool and manifest
  `/home/jay/research/data/cleanup-20261118/` (cleanup.py `cb72200c…`, manifest.tsv 104 lines, done.tsv; kept.tsv empty =
  no mismatch):
  - A: 37 uncompressed proofs with a byte-identical `.zst` twin deleted, 59.8 GB (Codex delta3 `proof.blrat`; today's 22
    N66 `trim.lrat`, also = cert.json `trim_lrat_sha256`).
  - B: 8 proofs compressed losslessly (16.8 → 3.0 GB; N66 b12/b13g/c11 `trim.lrat`, lb-k9oct cubes11 `proof.lrat` ×4,
    lfr `mono_A4B4_L7.lrat`); originals removed after the stream SHA-256 matched.
  - C: 43 N66 level-14 `cert.cnf` of split parents (38) and of the 16 Nov stopped runs (5), 28.6 GB.
  - F: 16 partial/tmp proofs of the 16 Nov D track, 1.3 GB.
  - Disk 711 → 614 GB used. Records that name the uncompressed paths now refer to the `.zst` copies.
  - Kept by the owner's choice: the 132 accepted N66 cube `cert.cnf` (87.7 GB) and the (20,15) test packets (15.2 GB).

- **12:40 all seven SAT3 sets confirmed by a second implementation** (vx1118's finder + trusted Python replay,
  independent of SAT3's finder and of VX2's checker; cells = Euler count, 0 failures everywhere; 40-point n = 9 set:
  275,920 cells; 52-point n = 10 set: 815,152). The first unit was stopped cleanly by the memory guard at 2.5 GB on the
  68-point set (no OOM kill; my sizing error) and the 68-point set was re-run alone with 7 GB (2,448,272 cells, passed).
  Verdict files `sat3-*.verdict.json` (verifier MAIN-vx1118); section added to SATG20261118. **Saturation bounds now:
  sat_g(6..10) ≤ 12, 16, 27, 40, 52, each by two independent exact implementations.**
- **12:45 session work finished.** Nothing runs except the memory guard `esr-memguard-1118d` (stopped next).

### End-game plan for (20,15) (main session, 02:55)

- The extra worker is one fastbb2 with `--extra-threads` threads on the contexts recorded between 150k and 300k nodes
  (72 open at 18:48 on 16 Nov; A2's model expects about 238 above 150k in all and about 67 above 300k, HEURISTIC). It
  closes about 11-15 per hour with one thread, so it becomes the bottleneck once the frontier is done.
- When N66 finishes, its 5 threads go to (20,15): restart the loop at a finder slice with more extra threads.
- When the frontier is done: stop the loop and run the reviewed standalone high-cap pass of V11_NOTES §4
  (`run_tree_v6.py --too-big-only --max-ctx-nodes=<cap>`; no loop on the packet), with the cap limited by the trusted
  replay's memory (about 6.6 KiB per node, AS's measurement, unverified claim `as-replay-mem-1116`); contexts above the
  cap get split (successor packet) rather than solved whole. AS's concurrent side pass `highcap_v1.py` is used only if
  track R finds it READY.

## Resume

- N66: copy `W/p2c14_driver_r7.py`, change only `DEADLINE`; start a memory guard first.
- (20,15): read the last `round` event of `continuation-b35s20v11c/events.json` (version V, receipt R): if round V was
  not appended, `--start-version=V --start-receipt=R`; if it was appended as V+1, `--start-version=V+1`, no receipt.
