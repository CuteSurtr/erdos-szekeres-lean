# Task E2: 3-fold symmetric 33-point class (`n33k7m3`), cloud run, 20 October 2026

Nothing here is a theorem. "UNSAT" always means "UNSAT of one specific CNF"; the
encodings are tested but not formally verified.

## Status in one paragraph

**`n33k7m3` is still open.** No cube of the cube-and-conquer tree closed in this run
(closed weight exactly 0/1); no model was found. The frontier went from 55 cubes at
depth 5–6 (inherited from task E) to __FINAL_OPEN__. A Knuth random-probe estimate puts
the remaining tree at 10^4.4 leaves or more, with a heavy tail. The run is far from
converging on 4 cores (see §4). **A side finding matters more than the run:** the
`lrat-check` that task E used (drat-trim git 2e3b2dc, which is also current upstream
master) accepts a forged one-line proof on a satisfiable CNF (§2). E2 re-checked E's three
D3 proofs with a patched lrat-check and with the CakeML-verified `cake_lpr`. All three
pass both, so E's D3 result stands as LRAT-checked UNSAT of those CNFs, now with a sound
checker.

## 1. Where it ran (`env.txt`)

- Cloud container: `Linux vm 6.18.44-fc-v139 x86_64`, 4 cores, 15 GiB RAM, no swap,
  hostname `vm`. Started 2026-10-20 00:21 UTC.
- The container was **restarted twice** (about 01:57 and 02:40 UTC), which killed all
  processes. The scratch disk survived. The driver resumed each time from `state.json`,
  which is saved every 60 s; jobs running at the time were re-queued. `env.txt` records
  both restarts.
- Tools built from source at the same commits as task E: CaDiCaL 3.0.1 (git c607304),
  drat-trim/lrat-check (git 2e3b2dc). Also built: `cake_lpr` (git a36874a; `cake_lpr.S`
  sha256 2f3af32d…, matching its `cake_lpr.sha256`). Python 3.11.
- The regenerated `n33k7m3.cnf` (`symcnf.py 33 7 3`) has sha256 `4c214b4c…daa73b`,
  identical to E's. It has 463,980 variables (2,002 orientation variables) and
  9,498,158 clauses.

## 2. Controls

### Encoder and solver controls with the rebuilt tools (`logs/controls.log`)

All 8 agree with task E. Every SAT model was re-checked by `symcheck.py`: no axiom,
symmetry, centre or symmetry-breaking violations, and the largest convex subset is below K.

| CNF | expected | got | CNF sha256 prefix |
|---|---|---|---|
| n9k5m3 | UNSAT (ES(5)=9) | UNSAT | 243e1567 |
| n18k6m3 | UNSAT (ES(6)=17) | UNSAT | 02c5ffc2 (= E) |
| n18k6m6 | UNSAT | UNSAT | bbff9352 |
| n15k6m3 | UNSAT (E's answer) | UNSAT | fc089011 |
| n12k6m3 | SAT | SAT, model checked, max convex 5 | d84a884c |
| n16k6m4 | SAT | SAT, model checked, max convex 5 | f9866340 (= E) |
| n16k6m5c | SAT | SAT, model checked, max convex 5 | 7d74e147 (= E) |
| n13k6m3c | SAT | SAT, model checked, max convex 5 | 16ab61f7 |

### lrat-check is unsound on the empty clause (`logs/lrat_check_soundness.md`)

`lrat-check` at git 2e3b2dc prints `c VERIFIED` (exit 0) for the one-line proof `2 0 0`
on the satisfiable CNF `p cnf 1 1 / 1 0`. It does the same on n12k6m3, a SAT CNF with a
checked model. The cause is in `checkClause`. A lemma whose RUP hints do not reach a
conflict falls through to the RAT branch, because `if (res == SUCCESS) return FAILED;` is
commented out. For the empty clause the "pivot" is literal 0, which never occurs, so the
lemma is accepted with any non-conflicting hints, including none. Two of E's mutation
controls rely on this path (dropping the empty clause's hints, or its final conflict hint),
and the unpatched checker accepts both.

**Fix used here:** `tools/lrat-check-E2.patch`, one line: reject an empty clause unless RUP
reaches a conflict. **Independent checker:** `cake_lpr`, a CakeML-verified LRAT/LPR checker.
`tools/dualcheck.sh` reports VERIFIED only if both accept.

Checker controls (`logs/lrat_checker_controls.log`, `logs/lrat_controls.log`):

| proof | expected | original lrat-check | patched | cake_lpr |
|---|---|---|---|---|
| n18k6m3, genuine CaDiCaL proof | accept | VERIFIED | VERIFIED | VERIFIED UNSAT |
| `x1` (SAT) + `2 0 0` | reject | **VERIFIED** | NOT VERIFIED | rejected |
| n12k6m3 (SAT) + hintless empty clause | reject | **VERIFIED** | NOT VERIFIED | rejected |
| n15k6m3's proof against n18k6m3 | reject | NOT VERIFIED | NOT VERIFIED | rejected |
| n18 proof, empty-clause hints removed | reject | **VERIFIED** | NOT VERIFIED | rejected |
| n18 proof, last empty-clause hint removed | reject | **VERIFIED** | NOT VERIFIED | rejected |
| n18 proof, middle lemma literal flipped | reject | NOT VERIFIED | NOT VERIFIED | rejected |
| n18 proof, empty-clause step deleted | reject | NOT VERIFIED | — | — |

### Re-check of task E's D3 results (`logs/lrat_recheck.log`)

Each CNF was regenerated with a hash identical to E's, then solved from scratch with
`--elim=0 --lrat=1`, and the proof was checked with both sound checkers:

| CNF | sha256 prefix | proof | patched lrat-check | cake_lpr |
|---|---|---|---|---|
| n33k7d3direct | 7796d999 | 153 MB | VERIFIED | VERIFIED UNSAT |
| n33k7d3 | 72ebbae0 | 171 MB | VERIFIED | VERIFIED UNSAT |
| n33k7m3refl | cc329387 | 650 MB | VERIFIED | VERIFIED UNSAT |

So the D3 class result stands, as "LRAT-checked UNSAT of these three CNFs" with a sound
checker. It is still not a theorem.

### Driver end-to-end (`test_n18/`)

`cnc2.py` with the rebuilt `ccworker` on n18k6m3 (tiny budgets) closed all 116 cubes. The
exact weight is 1/1, `verify_tree.py` reports partition_ok, and 5/5 random closed cubes
pass `dualcheck.sh`.

## 3. The run (`run/`)

- **Settings:** driver `results/E/tools/cnc2.py`, unchanged. It uses a global
  shallowest-first heap, exact integer weights, orientation-variable splitting only,
  budgets 10,000 × 1.2^depth (cap 2·10^6), and `--elim=0`.
- **Start:** resumed from E's saved frontier (`run/state_from_E.json`: 55 open cubes at
  depth 5–6, 54 jobs, 2.56 solve-hours on E's machine).
- **Workers:** 3 most of the time (4 from 00:41 to 01:13); the 4th core ran the probe and
  LRAT jobs.
- **Clock:** the `t` field in the logs is cumulative driver time, including E's 1,900 s.

Frontier history (`run/progress.log`; driver restarts write "start" lines):

| UTC (approx.) | t (s) | jobs | closed | open (depth: count) | solve-hours (cumulative) |
|---|---|---|---|---|---|
| 00:24 (start, E's frontier) | 1,901 | 54 | 0 | 5: 9, 6: 46 | 2.56 |
| 00:41 | 2,787 | 97 | 0 | 6: 30, 7: 68 | 3.24 |
| 01:13 | 4,676 | 212 | 0 | 7: 43, 8: 170 | 5.23 |
| 01:43 | 6,488 | 287 | 0 | 8: 224, 9: 64 | 6.67 |
| 01:58 (after restart 1) | 7,366 | 320 | 0 | 8: 191, 9: 130 | 7.34 |
| 02:29 | 9,167 | 428 | 0 | 8: 83, 9: 346 | 8.78 |
| 02:42 (after restart 2) | 9,887 | 466 | 0 | 8: 45, 9: 422 | 9.37 |
| 03:12 | 11,688 | 529 | 0 | 9: 494, 10: 36 | 10.82 |
__FINAL_ROW__

Every job so far exhausted its budget and split; there have been no retries. The
exact-weight invariant (closed + open = 1) held at every log line.

## 4. Convergence assessment and tree size (`probe/`, `tools/knuth_probe.py`)

**The driver gives no convergence signal.** The closed weight is exactly 0 after
__FINAL_JOBS__ jobs. The tree is complete down to depth 8 or 9: all 2^8 = 256 depth-8
nodes exist and none has closed. Per-job time grows with depth, about 60–100 s at depth 8
and 3–9 min at depth 15–20, because the budget grows 1.2× per level.

**The probe.** `knuth_probe.py` follows a random path below a random frontier cube from the
01:13 frontier, applying exactly the driver's budget and split policy, until a cube closes.
Knuth's estimator then gives 2^(D−d0) leaves for that cube's subtree. Walks so far:

| walk | start depth | outcome | leaves below the start cube (estimate) |
|---|---|---|---|
| s7 #0 | 8 | closed at depth 15 | 128 |
| s10 #0 | 8 | closed at depth 14 | 64 |
| s9 #0 | 7 | **still open at depth 20** when container restart 2 killed it | ≥ 8,192 (censored) |
| s8 #0 | 7 | killed at depth 12 by container restart 1 | no information |
__PROBE_ROWS__

**Both closed probe leaves were re-proved from scratch with an LRAT proof, and both checkers
accept them** (`logs/lrat_probe_leaves.jsonl`):

- the depth-15 leaf: 153 s, 281 MB proof;
- the depth-14 leaf: 241 MB proof.

So closed cubes do appear at depth 14–15 on some paths, and the solver's "U" answers there
are confirmed.

**Tree-size range.** Taking the leaf count as 256 × (mean subtree estimate per depth-8
cube):

- **Optimistic,** using only the two closed walks: about 256 × 96 ≈ 2.5·10^4 leaves, so
  about 5·10^4 jobs. At 2–5 CPU-minutes per job that is about 2·10^3–4·10^3 core-hours.
- **With the censored s9 walk** (≥ 2^12 per depth-8 cube on that path): the mean is at least
  about 1.4·10^3, so ≥ 3.7·10^5 leaves. Jobs there take 5–10 min, so ≳ 5·10^4 core-hours.

With two complete walks and one censored walk this is a very rough, heavy-tailed estimate.
The honest summary is **"at least thousands of core-hours, plausibly tens of thousands."**
That is 3–4 orders of magnitude more than this 4-core, 4-hour session. The estimate does not
include the incremental solver's learned-clause reuse, which helps the driver somewhat
compared with the fresh-ish probe worker.

**Recommendation.** This instance needs either a large cluster or a stronger encoding before
another cube run is worth it. Stronger encodings could add symmetry breaking for the
remaining labelling freedom (the orbit labelled 0 and the mirror image are not fixed;
E's README), or lemma clauses (cup/cap or emptiness lemmas, proved separately). Further
cube-and-conquer at this scale on a few cores will not close it.

## 5. Models

None. No SAT answer from the driver or the probe, so there is nothing to realize.
`tools/realizer/` was not used.

## 6. Incidents (for anyone reproducing)

- **Open files replaced by git.** The driver writes `events.log` and `progress.log` through
  open append handles. `git pull --rebase` replaced those files in the repository, so from
  about 01:13 to 01:45 the driver wrote to deleted inodes. The data was recovered from
  `/proc/<pid>/fd` before restarting. Since 01:46 the driver writes only to a scratch
  directory, and `run/` is a copy made at each commit. `closed.jsonl` was never affected:
  it was empty, and no cube closed.
- **Two container restarts** (§1).
- No push was rejected beyond ordinary non-fast-forwards, which were fixed by
  `pull --rebase`. Everything is on `es7-cloud`.

## Files

- `env.txt`: the environment, plus the two restart records.
- `logs/`: `controls.log`, `lrat_controls.log`, `lrat_checker_controls.log`,
  `lrat_check_soundness.md`, `lrat_recheck.log` (E's D3 proofs) and
  `lrat_probe_leaves.jsonl`.
- `run/`: `state.json` (resumable frontier), `state_from_E.json`, `progress.log`,
  `events.log`, `closed.jsonl` (empty) and `final_segments.json`.
- `probe/`: Knuth probe walks (`*.jsonl`) and per-step logs (`*.jsonl.steps`).
- `test_n18/`: driver end-to-end test.
- `tools/`: `knuth_probe.py`, `dualcheck.sh`, `lrat-check-E2.patch`, and `lratcube.py`
  (E's, with the checker output filter widened to keep cake_lpr's line).
- CNFs and proofs are not committed. Regenerate with `symcnf.py 33 7 3` and compare the hash.
