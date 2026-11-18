# STATUS20261115_1000: handoff at the end of the 14-15 November session (written 09:06-09:42 KST; final numbers)

This is the newest status page. It supersedes [STATUS20261115_0450](../STATUS20261115_0450/README.md), which is still the
place for the night's first half. Then read [ROADMAP20261115](../ROADMAP20261115/README.md): its §6 and
[SYNTHESIS.md](../ROADMAP20261115/SYNTHESIS.md) take precedence over its §§1-5. **Nothing was committed, pushed or
published after the 21:01 snapshot push of 14 November.** All of tonight's records are untracked files in the working tree.

## Results (labels as in the records; nothing rounded up)

### ES(8) upper bound

- **ES(8) ≤ 308**: unchanged since the night's first half. Computer-assisted, unrefereed, uncommitted. See the
  [budget34](../LO33N20261113/budget34/README.md) headline, [VERIFY308](../LO33N20261113/budget34/VERIFY308/README.md),
  [CHAIN_REVIEW](../LO33N20261113/budget34/VERIFY308/CHAIN_REVIEW.md) and [NOVELTY20261115](../NOVELTY20261115/README.md).
- **Toward 307** (budget 35, cases (F,Lo) = (18,17), (19,16), (20,15), (21,14)):
  - (18,17) and (19,16): EXACT TREE, as before.
  - (20,15): the work-keeping loop v10 ran 06:25-09:35 with 6 threads.
    - Every row batch through v138w1u is independently audited. That is **427 CERTIFIED coupled rows** for this case
      (own encoder plus fresh cake_lpr, one process per batch), 85 of them added after 05:14.
    - **555 of 8,065 contexts are closed**, up from 54 at 05:14. Many open contexts exceed the 150,000-node cap.
    - The last round logged 5 new witnesses, which are not yet cut. The resume line is in the budget34 README.
  - (21,14): untouched. It needs N66 ≤ 55 or a tree of its own (HEURISTIC estimate 1.85e9 nodes).
- **N66 ≤ 55: NOT decided; N66 ≤ 56 stays.**
  - Level-14 cube campaign, 05:50-09:29: 64 sign cubes on six split states. 6 cubes reached their time limit and were
    split again, so there are 70 leaves.
  - **At the stop, 33 of 70 leaves were CERTIFIED. That is 32 of the 64 base cubes, 50 % by measure.** Each certified
    leaf has its own cake_lpr acceptance (exact line) plus the full acceptance path, re-checked by the workflow's
    monitoring step. No cube was SAT. 37 leaves are open.
  - Final record: [PROGRESS.md](../N66N20261113/cubes20261115/PROGRESS.md), with exact resume commands in §10.
  - Cubes with many holes are the easy ones. The open leaves are mostly cubes with 0-3 holes, which are harder. Measured
    so far: 4 holes took 571-1,221 s and 3 holes 788-1,485 s.
  - The synthesis's estimate of 20-60 CPU-hours for the whole campaign still stands (HEURISTIC).
  - The driver deleted the partial cert.lrat and cert.cnf of its own timed-out runs: 19.64 GB, none of it part of a
    certificate. The campaign's critic had flagged that deletion as an owner question (PROGRESS.md §5).

### Lower bounds

- **ES(8)**: the ABSAT8-core probe is CERTIFIED 28/28. It covers 28 named 64-point octagon-free sets outside the stacking
  family, including the 8 vertex deletions of AlphaEvolve's 65-point set. All their one-point-extension CNFs are UNSAT,
  and cake_lpr accepted all 28 on two separate runs. The geometric reading (no real 65-point extension of those order
  types) is COMPUTED until an independent encoder and a soundness note exist. Source: ROADMAP §6.
- **k = 9 ring "two displaced layers"** (exact list `SATOPEN20261113/tools/k9/ring_cases.py`: 95 linear and 175 cyclic
  cases):
  - **155 of 175 cyclic cases are CERTIFIED** (final, 09:40), each with the exact cake_lpr line in its own `cake.out`.
  - All 155 pass `verify_cycx.py`: the order is the intended cyclic spiral, the free layer is unused, and the CNF hash
    recomputes and matches (`k9/verify_cycx_20261115b.txt` and `…c.txt`).
  - 2 of 95 linear cases are certified.
  - No case was SAT. The ring is not finished: 20 cyclic and 93 linear cases remain, roughly 40 CPU-hours
    (HEURISTIC).
- **ES(7)**: brute force at 33 points is infeasible, about 1e3-1e4 CPU-years (HEURISTIC). No ES(7) experiment ran. See
  [ES7_FEASIBILITY.md](../ROADMAP20261115/ES7_FEASIBILITY.md).

### Δ-reduction conjecture: weak D(5,7) and weak D(5,8) remain OPEN

The index is [attack20261115/README.md](../DELTA3N20261113/attack20261115/README.md).

- **S19′ is realizable** (EXACT, independently verified, and checked by the main session's own code). So CONJ-TS′(7) is
  false for real point sets. Theorem 3 (CONJ-TS′(n) ⟹ weak D(5,n)) is still valid, but its premise fails at n = 7.
- **Round 6** ([ROUND6.md](../DELTA3N20261113/attack20261115/ROUND6.md)):
  - **AT_n is false for real point sets at n = 6, 7, 8** (EXACT, verified). The main session also confirmed all 12 sets with
    its own code ([VERIFY_ATN_MAIN.md](../DELTA3N20261113/attack20261115/VERIFY_ATN_MAIN.md)). So the LT-cover lemma of
    program delta:1 fails as stated, and its repairs fail too.
  - ENV#(7) is CERTIFIED for |U| ≤ 13.
  - **Weak D(4,8) is CERTIFIED for every set with ≤ 16 points.** Round 6 covered 14 and 15. At 16 points the main
    session's re-run accepted CaDiCaL's own untrimmed 12.45 GB LRAT (exact line, 6 GB heap, 423 s, hashes equal to
    ROUND6), so the trimmed-proof question is moot. Open: 17-22 points.
- **Certified CONJ-TS′ test** (round 4):
  - CONJ-TS′(8) holds on all abstract signotopes with |S| = 15 (CERTIFIED, two encodings, verified). n = 7 at 15 points
    is UNKNOWN.
  - CONJ-TS′(6) fails for abstract signotopes at 13 points.
- **New, main session (09:12, EXACT, own code; no second party has checked it yet): CONJ-TS′(6) is false for real point
  sets at 13 points.** All three abstract models are realizable, and 13 is the least size. On these sets weak D(5,6), the
  rooted form, the mirror form and ENV#(6) all hold, the same pattern as on S19′. See
  [VERIFY_ATN_MAIN.md](../DELTA3N20261113/attack20261115/VERIFY_ATN_MAIN.md).
- **σ13 is a real point set** (main session's own check of one realization). So rank localisation R(4,7) fails for a real
  13-point set.
- **ROOT(6) is CERTIFIED for |S| ≤ 14** (main session; round 6's encoder with a new positive control at n = 6). For point
  sets, ES(6) = 17 leaves only sizes 15 and 16 open.
  [ROOT6_MAIN.md](../DELTA3N20261113/attack20261115/ROOT6_MAIN.md).
- No ES bound changes. No novelty statement is made for any of these items; the last full literature check is
  NOVELTY20261115.

## Owner decisions waiting (nothing below was done)

1. Commit, push or publish ES(8) ≤ 308 and tonight's records (`git status`: the new record folders are untracked).
2. Delete partial LRATs; none of them is a proof:
   - N66 level-14 `n66-20261113/p2/b14h2|b14i2/it1/cert.lrat`, about 29 GB each;
   - m = 9, 70 GB;
   - `roadmap-20261115/delta-r2-attacker/cert14/ts7_N14.lrat`, 4.7 GB;
   - `roadmap-20261115/conjts/runs/n7_m15/cts_n7_m15.lrat`, 22.9 GB.
   Disk has 852 GB free, so nothing is urgent.
3. (Resolved at 09:22: the untrimmed weak D(4,8) proof at 16 points was accepted, so no trimmed-LRAT ruling is needed.)
4. Repository cleanup: paused at "who is the cleaned-up repository for, and what should they be able to do?".
5. The terminal scope of this session carries a runtime CPU cap (CPUQuota 800 %, set at 07:29 after the load incident).
   It lapses when that terminal closes.
6. Deletions of fresh partial files that were already done; please say whether these are acceptable in future:
   - the N66 driver deleted 19.64 GB of partial cert.lrat/cert.cnf from its own timed-out cube runs;
   - the main session deleted three partial ROOT(6) LRATs (172 MB, 103 MB and 39 MB) from runs it stopped after
     seconds to a minute.
   None of these files was a proof.

## Resume, in order of value

1. **N66 cube campaign.** It is the critical path to 307, because it removes (21,14).
   - The driver is `/home/jay/research/data/n66-20261113/p2c14_driver.py`. Its deadline is hard-coded (`at('09:40')`,
     line 22), so make a copy with a new deadline. The exact commands are in PROGRESS.md §10.
   - State is in `p2/c14/campaign_status.json`: 37 open leaves. Certified leaves are kept and count only with their own
     acceptance.
2. **(20,15)**: `continue34_v10.py --start-version=138 --start-receipt=runs/b35s20/c138s1.json`, with the other options as
   in the budget34 README.
3. **k = 9 ring**: `k9/tools/sched.py` with env `MAXJOBS`, `MEMB`, `SOFT`, `HARD`, in a unit. `k9/queue.txt` holds the
   exact remaining list.
4. **Δ**:
   - ROOT(6) at m = 15 (about 75 min) and 16 (about 11 h; split into cubes). Together they would settle ROOT(6) completely,
     because ES(6) = 17. Command: `root_cnf.py 6 m`, then the house `certify_cnf.sh`
     ([ROOT6_MAIN.md](../DELTA3N20261113/attack20261115/ROOT6_MAIN.md)).
   - ENV#(7) at |U| = 14 (projected about 8 h on one thread).
   - ROOT(7) at 15 and CONJ-TS′(7) at 15.
   - Weak D(4,8) at 17 (LRAT about 120-150 GB).

## House rules learned tonight

- Agent-side Python must pin `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1`. Any job longer than a minute
  runs in an `esr-*` unit. At 07:28, a script run outside a unit took about 19 cores and the load reached 30 of 32.
- One audit process per batch, because of the 300 MiB soft address-space limit inside `audit_followup_rows_v4.py`.
- The N66 cube units broke the 80 % sizing rule three times: anon reached 85-88 % of their 3,686 MiB limit (PROGRESS.md).
  There was no memguard stop and no OOM. A resume should raise MemoryMax or lower the cake heap.
- When a scheduler stops at its soft deadline it can leave solved cases unchecked (k9, 09:36). Run `check.sh` on
  every case folder that has `solved` but no `cake.out` before counting.
