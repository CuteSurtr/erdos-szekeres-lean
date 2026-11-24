# Budget34: ES(8) ≤ 308 (computer-assisted; new components independently verified)

**Status at 23:20 KST, 14 November 2026.** Budget-34 slices 18, 19 and 20 are excluded (EXACT TREE). With the
budget-33 baseline (h(C) ≥ 34) this gives h(C) ≥ 35, |R| ≤ 119, |S| ≤ 307, i.e. **ES(8) ≤ 308, without N5 ≤ 65.**
Independent verification [VERIFY308](VERIFY308/README.md): own C++ and Python tree checkers (written without reading
the project checker) accept all three slice packets; all 1,020 coupled-row LRATs re-accepted by cake_lpr with
recorded hashes; bridge arithmetic re-derived with own code (nine Lean rows give h(F) ≥ 18; the 34-hole cases are
exactly (18,16), (19,15), (20,14)); the 86 `pending_kernel`-tagged catalog rows are covered by the Lean theorem
`all_rows_2650`. Trust boundary (inherited, not re-checked tonight): the Lean components (`all_rows_2650`, budget-32
exclusion, balanced 187, population composition), the written encoder soundness of the coupled rows (VERIFY309N link
(c); every row's CNF also matched an independent re-encoding in the batch audits), N66 ≤ 56 (followup56), the
budget-33 slice trees (VERIFY_LO) and Lemma A. **Not Lean-checked, unrefereed.** Root README.md, RESULTS.md and
math.md are unchanged; nothing is committed.

Earlier status (22:17, superseded):

## Budget34: slices 19 and 20 excluded; ES(8) ≤ 308 candidate, independent audit pending

**Status at 22:17 KST, 14 November 2026 (evening continuation; details in the last section).**

- **EXACT TREE: slice 20 (h(F) ≥ 20, h(Lo) ≥ 14, budget 34) is excluded** over rows `s20-v13` (3,672 rows: 2,650
  Lean rows, the two capacity rows, 1,020 coupled rows). Packet `W/runs/s20/bb-s2`: 4,289 contexts, 15,479,542
  leaves, minimum exact margin 1, sole pending branch state 0 missing. Checked twice by `scripts/omission_tree.check_tree`
  (SHA-256 `35cb3050…`, the committed file): the incremental replay `audit/incremental-v10` (receipts carried under
  row-prefix and file-hash checks) and the fresh full replay `audit/fresh-v13` (no receipt reused).
- **CERTIFIED:** every one of the 1,020 coupled rows matches an audited row with a fresh cake_lpr stdout containing the
  exact line `s VERIFIED UNSAT` (812 pool, 128 near9, 80 in batches v2-v13); the capacity rows are exactly
  F = {f1 ≥ 5} with demand 20 and Lo = {f1 ≤ 4} with demand 14 (checked against the catalog).
- **Consequence (PROVED conditional bridge, [bridge/README.md](bridge/README.md) §3):** with slice 19 (EXACT TREE, this
  morning) both budget-34 slices are excluded, so **ES(8) ≤ 308** follows: every 308 points in general position contain
  a convex octagon. This is a computer-assisted chain (written geometric arguments, CERTIFIED rows, EXACT TREE
  replays, existing Lean components); **it is not Lean-checked, not refereed, and has not yet had an independent audit
  of its own (the analogue of VERIFY309N).** It uses **N5 ≤ 65** for h(F) ≥ 19; that result rests on audited but
  recorded verdicts, because its original and independent arithmetic LRATs were deleted (bridge §4). Excluding one
  more slice, (h(F) ≥ 18, h(Lo) ≥ 16), would remove the N5 dependency: the Lean rows give h(F) ≥ 18 and N66 ≤ 56 gives
  h(Lo) ≥ 14, so (18,16), (19,15) and (20,14) are the only 34-hole cases.
- `FINAL_MANIFEST.json` and `SHA256SUMS` describe the record as of this morning and do not cover the evening files.

---

Started14 November2026 at10:00:22 KST for the owner-requested one-hour
research pass, ending about11:00:22. Discovery stopped before10:45.
The final tree replay completed at10:46:38. No improved ES bound is claimed.

**EXACT TREE:** slice19 is independently closed at budget34: 3,643
contexts, 1,658,483 nodes, 829,242 leaves, minimum exact margin1, and only
the impossible state-zero-missing branch pending. See
[the replay summary](audit/s19-summary.json) and
[mathematical bridge](bridge/README.md). With the inherited N5<=65 result,
this proves the conditional implication **N66<=55 => ES(8)<=308**.
The established N66 bound is56;55 is not claimed.

**PROVED structural consequence:** a residual configuration cannot
simultaneously have at least65 F owners and55 Lo owners. This follows by
padding its Boolean hole set to the excluded slice, and needs neither N5
nor N66. See [the standalone tradeoff](tradeoff/README.md) and its
[independent mathematical review](bridge-followup/README.md).

The remaining finite slice20 uses capacities F20/Lo14. Several abstract
34-hole vectors have survived earlier pools and then been excluded by
new, individually certified coupled constraints. They are not real point
configurations. Killing these vectors does not close the slice.

## Final mathematical and computational outcomes

| Result | Evidence and scope |
|---|---|
| Slice19 excluded at budget34 | **EXACT TREE**,1,658,483 nodes; all3,643 contexts; sole impossible state0-missing branch |
| Residual population tradeoff | **PROVED:** F owners<=64 or Lo owners<=54; Boolean-padding deduction independently reviewed; no N5/N66 capacity input |
| Supporting coupled rows | **CERTIFIED:** all971 rows independently CNF-reconstructed and accepted in fresh cake replays |
| Slice20 at final version5 | **PARTIAL EXACT REPLAY; NO EXCLUSION:** all1,222 present contexts checked;2,842 of4,064 remain open;11,366,003 counted nodes and5,683,002 leaves including the pending frontier; minimum checked margin1 |
| ES bound | Existing project result ES(8)<=309 remains unchanged. ES(8)<=308 is open. Nothing here is refereed or a complete Lean formalization |

Final replay: [stable version5 summary](audit/incremental/s20-v5-summary.json)
and [frozen post-stop checks](audit/incremental/finished-by-control.json).
Its2,843 pending branches comprise2,842 unresolved contexts plus state0
missing; the latter alone is discharged geometrically. A positive margin
on all checked leaves does not settle the other branches.

The final row file has3,623 rows:2,650 base,2 capacities(F20,Lo14),971
coupled. [Frozen input copies](data/frozen-inputs/s20-v5/manifest.json)
preserve the append-only chain. Final extra SHA-256:
`e6601e5edcddfcc653a0891eef63d8010a6dd303431d312515fa8e8e03618126`;
row-file SHA-256:
`8d8c970f37b99309e94a7a8b06537024fe7264abfe8c2af501c6f0cf6b463fb0`.

The971-row proof inventory consists of the original812 and batches
7+128+9+10+5. Independent receipts are in
[the audit record](audit/VERIFY_BUDGET34.md). Four explicit Boolean
witnesses for earlier versions are retained in data/witness-v1.json
through data/witness-v4.json. Each was excluded by subsequently certified
rows. No satisfying assignment or UNSAT certificate is claimed for final
version5. The independent [SAT track](sat/VERIFY_FINITE_SAT.md) records its
separate encoding, exact controls and bounded solver outcomes.

One useful negative finding: witness4 also satisfies all6,829 additional
provisional nine-state rows from the supplied discovery files. Adding
that entire supplied candidate family to v4 still leaves a34-hole Boolean
model; indiscriminately certifying those rows cannot close that system.
The five new13-state rows in v5 exclude this witness. This says nothing
about undiscovered nine-state constraints or geometric realizability.
The final v5 encoding audit and214 exact real-point controls passed;
the bounded solver searches ended UNKNOWN, not with an exclusion proof.

## Retained artifacts and resumption

All large evidence is retained under W=/home/jay/research/data/es308-20261114.
No large proof was deleted. The successful slice19 is archived as described
below. The live slice20 checkpoint is W/runs/s20/bb; its master contains
4,064 contexts and its1,222 closed files are immutable. Final row inputs
are W/inputs/s20-v5. `tools/run_tree.py` accepts `--input-folder=s20-v5`,
a new exclusive `--tag`, and a bounded thread/time allocation; it resumes
the existing master and skips closed contexts. Read the live CPU/memory
state and restart the prescribed guard before any future long run.

The last75.9-second v5 search returned finder code4: some contexts exceeded
the50,000-node cap; no new context closed in that short retry. This is an
algorithmic limit, not an invalid proof or a geometric witness. A useful
next step is to refine only open contexts (the native finder supports
`--split-open`) in a preserved successor packet, or reassess per-context
limits within the same memory caps. The current wrapper does not expose
`--split-open`. Do not rewrite a frozen master or treat old33-hole helpers
as34-hole tools. The independent audit must check the successor frontier.

The two separate tail probes contributed76 and115 additional closed
contexts. Imports used exclusive hardlinks only after identical master
and context definitions plus ordered-row-prefix checks. Every imported
context then received an independent exact replay in the final packet.
Their commands, partial outcomes and import hashes are copied into data/.

`run_tree_v1.py` and `cut34_v2.py` preserve the exact earlier runner and
certificate-helper sources; the latter matches the original v2 source
hash. The C++ finder, frozen row inputs, complete stdout, CNF/LRAT pairs,
receipts and per-version witness snapshots remain available in W.

All work is uncommitted. No push, branch change, root README.md/math.md
edit, installation or external message was performed. Resource snapshots
and job receipts are retained; observed active cgroups had zero swap and
zero OOM counters. All research units were inactive by10:51:37;
memguard5 was then stopped and p2-watch-d1b was already not loaded.
See [shutdown.json](data/shutdown.json) and the
[next-session handoff](../../STATUS20261114_1100/README.md).

Target: prove every actual residual configuration has at least35 holes,
so its population is at most119. With the existing balanced bound187,
the checked composition gives ES(8)<=187+119+2=308.

The independently established ES(8)<=309 chain already gives at least34
holes. N5<=65 gives h(F)>=19; N66<=56 gives h(Lo)>=14. At exactly34 holes,
only h(F)=19 or20 remain. Both need new exclusions at budget34. Reusing
budget33 certificates without checking their arithmetic would be unsound.

Parent owns compiled tree search and integration. Independent tracks own
row/proof provenance and a separate SAT encoding of the finite row system.
All prior frozen results and proof directories stay untouched. Inputs and
large outputs go under /home/jay/research/data/es308-20261114/.

Resources: no research jobs active on entry;16 CPUs available. The shared
verifier budget remains6000MiB, global caps16 threads/24GB. Long jobs will
use nov13c-vfy-308-* units with quota, finite deadline, MemoryMax and zero
swap. Parent plans two bounded compiled searches; separate exact audits
and witness checks determine the evidence label. Only cake_lpr's exact
s VERIFIED UNSAT accepts an LRAT. No lrat-check or HiGHS verdict is evidence.
No commit, push, branch change, installation, large-proof deletion or
external message is part of this pass.

## Initial frozen instances and resource estimates

The812 coupled rows are frozen from FASTBB's completed slice23, with its
old capacity rows removed. New capacity rows are exactly F19/Lo15 and
F20/Lo14 at budget34. Each instance has3464 rows on154 states. The source
and hashes are in data/input-manifest.json. Independent proof provenance
and fresh replay are running separately; a finder status is not evidence.

Each compiled finder has3 worker threads,1400MiB AS and1200MiB clean RSS
stop, MemoryMax2000M, Swap0,900s search plus180s outer grace and1140s unit
limit. The per-context cap is50000 nodes; bounded context buffers and the
small154-column LP make this allocation conservative. Completed context
file cache is synced/released every second. Two finder reservations2800,
two independent slots1200 each, parent150 and monitor160 total5510MiB,
within the6000MiB verifier budget. CPU quota totals8 cores including both
independent tracks, below16. No new CPU/memory cap is raised.

A compatibility hazard was found before use: the old witness_kill2.py
assumes budget33 and treats len(holes)>33 as already refuted. It must not
be used unchanged at budget34. This pass uses a new exact34 witness check
and does not call that old mutating helper. Old files remain unchanged.

## Live progress, 10:17 KST

All812 coupled rows now have independently reconstructed full CNFs,
matching retained CNF/LRAT identities, and fresh cake acceptance lines.
See [the independent audit](audit/VERIFY_BUDGET34.md). This establishes
the supporting row certificates, not either budget34 exclusion.

At10:12, both three-worker finders were stopped in a controlled manner and
resumed with six workers each, retaining closed contexts. Their1400MiB AS
limits did not change. Each new unit has CPUQuota600%, MemoryMax2000M,
MemorySwapMax0, RuntimeMaxSec1980, and a1800s finder deadline. The two
independent numerical tracks bring the total to14 CPUs; one additional
read-only mathematical sidecar is bounded at1 CPU/150MiB. The global16-CPU
and6000MiB verifier limits remain in force. CONTROLLED_RESUME.json files
and run receipts retain the stop/resume history.

`tools/cut34.py` provides an isolated fallback for exact34-hole vectors:
it checks all current rows, selects discovery candidates, and can build
full coupled CNFs and retain fresh CaDiCaL/cake proofs. Its small positive
encoding control reproduces a previously certified nine-owner CNF hash.
No new row is accepted from a discovery ledger or solver status alone.
This fallback has not yet generated a new supporting row.

## Findings through 10:33 KST

The fallback subsequently certified seven rows excluding the first
slice20 vector, nine excluding the second, and ten excluding the third.
A deterministic sample of128 nearby nine-owner candidates also passed
fresh certificates. All CNFs, LRATs, stdout and identities are retained.
The independent auditor has separately reconstructed/replayed the first
144 additions (7+128+9); the ten newest additions are queued for that
audit. This paragraph is a checkpoint, not the final audit status.

| Version | Coupled rows | Total rows | Finite result at this checkpoint |
|---|---:|---:|---|
| s20 |812|3464|COMPUTED SAT witness; independent row and CNF checks passed|
| s20-v2 |819|3471|COMPUTED SAT witness; independent row and CNF checks passed|
| s20-v3 |956|3608|COMPUTED exact row witness; new cuts exclude it|
| s20-v4 |966|3618|Search running; no exclusion claimed|

Each version is an immutable directory under W/inputs. `append_cuts.py`
checks literal cake acceptance and proof identities, then preserves the
entire old row prefix. `continue34.py` runs finder/certifier stages
sequentially and stops discovery by10:45; its event ledger is
W/continuation/events.json. The parent finder has at most12 workers.
The independent auditor and SAT track each have one CPU. Address-space
reservations remain below the6000MiB verifier budget. All active research
cgroups checked at this checkpoint had zero swap and zero OOM counters.

The slice19 archive is W/archive/s19-exact.tar,290,508,800 bytes,
SHA-256 `586793624172691d00a4c5f364ab29f6b4e4e3cb9e1e21458a93ab4232f3aeee`.
Every archived member was read back and matched byte hashes/lengths to
the original. [The archive manifest](data/s19-archive.json) also binds
the independent replay summary. The original tree remains unchanged.

The inherited N5<=65 audit reports that its original and independent
arithmetic LRATs were deleted in that earlier session. This pass inherits
that audited result; it does not claim a fresh retained-proof replay of
N5. The preferred existing309 chain avoids N5 and these coupled rows.
The new geometry/certificates/tree replay and conditional deduction are
not a complete Lean theorem, and nothing is refereed.

## 14 November evening continuation (v6), in progress

Started 21:11 KST. **No new exclusion is claimed until the replay below reports EXACT TREE.**

- Finder: unmodified `tools/run_tree.py` (SHA-256 `459b07c9…`), `20 --input-folder=s20-v5 --tag=v6 --threads=12
  --seconds=4200`, unit `esr-lo-s20v6` (CPUQuota 1200 %, MemoryMax 2 G, no swap, RuntimeMaxSec 4800). Same frozen
  v5 rows (rows `8d8c970f…`, extra `e6601e5e…`); resumes the existing master; the 1,222 closed context files are untouched.
  Reason: contexts 1024-3071 had never been attempted with v5 rows (v4 stopped at its witness, v5 ran 72 s);
  only about 70 open contexts are known to exceed the 50,000-node cap.
- Replay: `audit/incremental_audit_v2.py` (SHA-256 `af7b45d2…`), a copy of `incremental_audit.py` whose only changes
  are the deadline and output folder from argv (`2026-11-14T22:45:00+09:00 incremental-v6`) and carrying the
  receipts of `audit/incremental/{carried,new-contexts}.jsonl`; carried receipts are used only after the unchanged
  path, row-prefix and context-hash checks. Unit `esr-vfy-s20v6` (1 thread, 1.5 G). Output `audit/incremental-v6/`.
- Guard: `.claude/skills/es-research/scripts/memguard.sh esr 24000 lo=3000 vfy=6000`, unit `esr-memguard`,
  log `W/memguard-v6.log`.
- Prepared for the contexts that exceed the 50,000-node cap (15 at 21:14, all from the old hard list), not yet run:
  `tools/run_tree_v2.py` (SHA-256 `a73c43ad…`; adds `--bb` and `--split-open`, refuses
  to split the original packet), `tools/prepare_successor.py` (`bb84d1f0…`; hard-links closed context
  files, copies the three master files, checks every hash, refuses while a finder runs) and
  `audit/incremental_audit_v3.py` (`25f5e743…`; packet folder from argv, v1-v3 bindings still
  resolved in the original `bb`, carries the receipts of earlier replay folders).
- **21:18 finder v6 stopped on witness 5** (context 1336, 34 holes; independent row check PASS over all 3,623 v5 rows;
  abstract hole vector, not a real point set) after closing 285 more contexts (1,507 closed). Replay `incremental-v6`
  confirmed all 1,507 (PARTIAL EXACT REPLAY, minimum margin 1) and was then stopped by the operator
  (`incremental-v6/STOPPED_BY_OPERATOR.json`) to give the next replay more memory.
- 21:20 cut loop `tools/continue34_v2.py` (SHA-256 `6c845635…`; copy of `continue34.py` with `--out`,
  `--start-receipt` and finder tags `w<version>`), unit `esr-lo-s20loop`, deadline 23:30 KST, output `W/continuation-v6`.
  Round v6: 9 rows selected from the discovery pools and **CERTIFIED** (cake_lpr `s VERIFIED UNSAT`, 9/9), appended
  as `inputs/s20-v6` (3,632 rows); finder resumed as tag `w6`.
- Replay `audit/incremental_audit_v3.py ... incremental-v7 bb incremental-v6`, unit `esr-vfy-s20w` (2.5 G, until 23:55):
  independent audit of batch v6 PASS (own encoder 9/9, fresh cake 9/9, all 9 cut witness 5); epoch s20-v6 pinned;
  1,507 receipts transferred.
- 21:31-22:02 the loop ran rounds v7-v12 (10, 7, 5, 2, 4, 7 rows; each round killed the witness that stopped finder
  `w<k>`, each witness passing the independent row check). Finder `w12` then ended with exit 4: **4,034 of 4,064
  contexts closed; the 30 open ones all exceeded the 50,000-node cap** (none untried). Rows `s20-v12`: 3,667.
  Replay `incremental-v7`: batches v6-v12 (44 rows) all PASS (own encoder + fresh cake); **4,034 contexts replayed,
  minimum margin 1, pending = 30 contexts + state 0 missing** (PARTIAL EXACT REPLAY); stopped by the operator after
  catching up (`incremental-v7/STOPPED_BY_OPERATOR.json`).
- 22:03 successor packet `runs/s20/bb-s1` (`tools/prepare_successor.py bb bb-s1`: 4,034 context files hard-linked,
  three master files copied, all hashes checked, receipt `bb-s1/SUCCESSOR.json`; original `bb` master `44e0d7e3…`
  unchanged). Finder `run_tree_v2.py 20 --input-folder=s20-v12 --bb=bb-s1 --split-open=3 --tag=s1 --threads=12
  --seconds=5000`, unit `esr-lo-s20s1`: split 30 -> 240 contexts (4,274 in all). Replay
  `incremental_audit_v3.py ... incremental-v8 bb-s1 incremental-v6 incremental-v7`, unit `esr-vfy-s20s1`, until 23:55.
- 22:04 finder `s1` stopped on a witness (34 holes, row check PASS over 3,667 rows) after closing 57 split contexts.
  **Replay `incremental-v8` failed closed** (`incremental-v8/failure.json`, NOT CONFIRMED): `replay34.frontier` requires
  context labels 0..n-1, but `--split-open` numbers new contexts 4064-4303 and retires the 30 split labels. No context
  was replayed by that run. Fix, each a copy with an exact asserted diff (originals untouched):
  `audit/replay34_v2.py` (`7267cd3f…`; the 0..n-1 assertion replaced by "labels are natural numbers"; distinct labels,
  the label count = `master.contexts`, and closure = context files exactly equal to labels, each checked under its
  exact path, are unchanged), `audit/audit_followup_rows_v2.py` (`76283f19…`; witness snapshot looked up in `bb*`
  packets), `audit/incremental_audit_v4.py` (`fd087cd1…`; imports both) and `tools/continue34_v3.py`
  (`a4977a69…`; `--bb`, finder via `run_tree_v2.py`). Self-check `audit/test_replay34_v2.py` PASS: six synthetic
  masters (skipped labels accepted; duplicate label, count mismatch, unreachable node, uncertified leaf and negative
  label rejected; v1 still rejects skipped labels) and the real packets (all 4,034 closed contexts have identical paths
  in `bb` and `bb-s1`; each of the 30 split contexts has exactly 8 descendants; no new context lies elsewhere).
- 22:06 loop `continue34_v3.py --start-version=12 --bb=bb-s1 --out=continuation-s1` (unit `esr-lo-s20loop2`, deadline
  23:30). Round v13: 5 rows CERTIFIED, `s20-v13` = 3,672 rows. Replay `incremental_audit_v4.py ... incremental-v9 bb-s1
  incremental-v6 incremental-v7` (unit `esr-vfy-s20s1b`, until 23:55): batch v13 PASS, split epoch pinned (4,274 contexts).
- 22:09 finder `w13` ended with exit 4: **4,273 of 4,274 contexts of `bb-s1` closed; only context 4240 open** (over the
  cap). Replay `incremental-v9`: 4,273 replayed, minimum margin 1, pending = context 4240 + state 0 missing; stopped by
  the operator after catching up (`incremental-v9/STOPPED_BY_OPERATOR.json`).
- 22:10 successor packet `bb-s2` (`prepare_successor.py bb-s1 bb-s2`: 4,273 files hard-linked; `bb-s1` master
  `c337355c…` unchanged). Finder `run_tree_v2.py 20 --input-folder=s20-v13 --bb=bb-s2 --split-open=4 --tag=s2`
  (unit `esr-lo-s20s2`): context 4240 -> 16 contexts (4,289 in all). Replay `incremental_audit_v4.py ... incremental-v10
  bb-s2 incremental-v6 incremental-v7 incremental-v9` (unit `esr-vfy-s20s2`, until 23:55).
- 22:11 finder `s2` closed all 16 new contexts in 9 s (exit 0, DONE: 4,289/4,289; COMPUTED). 22:11:22 replay
  `incremental-v10`: **EXACT TREE** (`finished.json`), 4,289/4,289 contexts, 30,959,083 nodes, 15,479,542 leaves,
  minimum margin 1, global pending 1 (state 0 missing), `master_still_current` true.
- 22:13-22:17 `audit/fresh_replay.py bb-s2 s20-v13 fresh-v13 6` (unit `esr-vfy-fresh13`, 6 processes, 4 G, peak about
  1.3 G): **EXACT TREE (fresh full replay, no receipts reused)**: master (`cfe6dce8…`) and all 4,289 context files
  re-checked from scratch against all 3,672 rows; 15,479,542 leaves (identical), minimum margin 1, pending state 0
  only. (Its node count, 30,963,370, counts master nodes plus context nodes; the incremental count subtracts the
  4,289 context placeholders and adds the two path nodes: 30,963,370 - 4,289 + 2 = 30,959,083.)
- Checklist (own script): capacity rows exactly F = {f1 ≥ 5}/20 and Lo = {f1 ≤ 4}/14 (84 + 70 = 154, disjoint);
  all 1,020 coupled rows (rhs 1) matched to audited rows with a fresh `s VERIFIED UNSAT` line; checker
  `scripts/omission_tree.py` byte-identical to the committed file.

### Evening files and hashes (W = /home/jay/research/data/es308-20261114)

| File | SHA-256 |
|---|---|
| `W/inputs/s20-v13/rows.txt` | `ac0494347075bda4…` |
| `W/inputs/s20-v13/extra.json` | `daad72f991c803cb…` |
| `W/runs/s20/bb-s2/master.json` | `cfe6dce8961b98d6…` |
| `audit/incremental-v10/latest-summary.json` | `4a5840c6ec2a537f…` |
| `audit/incremental-v10/finished.json` | `97138241cb5d4e51…` |
| `audit/fresh-v13/summary.json` | `7da1145c8debeb97…` |
| `audit/fresh-v13/contexts.jsonl` | `02f6fd01b8c193ee…` |

Packets `W/runs/s20/{bb,bb-s1,bb-s2}` (context files hard-linked across them, 7.2 G for all of W), every cut
directory `W/cuts-v6`…`W/cuts-v13` (CNF, LRAT, cake stdout) and the inputs `W/inputs/s20-v6`…`s20-v13` are retained.
No proof was deleted.

### What remains

1. Independent audit of the 308 chain with own code (`VERIFY308`): re-derive the bridge, re-check the 49 evening rows'
   encoder soundness and certificates, and replay slice 20 with an independently written leaf checker.
2. Optional: exclude slice (h(F) ≥ 18, h(Lo) ≥ 16) at budget 34 to remove the N5 ≤ 65 dependency.
3. Nothing is committed; root README.md, RESULTS.md and math.md are unchanged.

### Resume

Fresh replay: `cd audit; <venv>/python fresh_replay.py bb-s2 s20-v13 <new-outdir> 6` (unit with CPUQuota 600 %,
MemoryMax 4 G). Cut/search loop on a packet: `tools/continue34_v3.py --deadline=... --start-version=<k> --bb=<packet>
--out=<new folder> --start-receipt=<finder receipt with a witness>`; replay `audit/incremental_audit_v4.py <deadline>
<new outdir> <packet> <earlier replay folders...>`.

## 14 November late evening (22:25-): slice 18 and the N5-free chain

- New tools, copies with exact asserted diffs (originals untouched): `tools/prepare_slice.py` (`ba117447…`; inputs of a
  further slice from an existing row version: Lean rows, (F, T), (Lo, 34 - T), then every coupled row in order),
  `tools/run_tree_v3.py` (`3786e397…`; slice 18 allowed), `tools/cut34_v3.py` (`35722431…`; witnesses of slice 18 allowed),
  `tools/continue34_v4.py` (`90c4d257…`; `--slice`), `audit/audit_followup_rows_v3.py` (`7b0d6bc9…`; any slice, witness slice tied to
  the input's capacity rows), `audit/fresh_replay_v2.py` (`ef0fe84d…`; packet `s<T>/<folder>`; asserts the capacity rows are
  exactly (F, T) and (Lo, 34 - T)).
- Inputs `W/inputs/s18-v13` (`prepare_slice.py 18 s20-v13 s18-v13`): 3,672 rows = 2,650 Lean rows, (F, 18), (Lo, 16) and
  the same 1,020 CERTIFIED coupled rows; extra SHA-256 `1b72eb934e00c7f5…`.
- 22:47 finder `run_tree_v3.py 18 --input-folder=s18-v13 --tag=a --contexts=4096` (unit `esr-lo-s18a`): master 19,361
  nodes in 68 s, then all 4,296 contexts closed in 4.5 s (exit 0; COMPUTED).
- 22:48 `audit/fresh_replay_v2.py s18/bb s18-v13 fresh-s18-v13 6`: **EXACT TREE (fresh full replay)** for slice 18
  (h(F) ≥ 18, h(Lo) ≥ 16, budget 34): 4,296 contexts, 45,833 nodes, 20,770 leaves, minimum margin 1, only state 0
  missing pending; capacity demands asserted [18, 16]; master `72c5a954820f6880…`.
- **Bridge arithmetic re-checked with own code:** rows 973, 1165, 1167, 1171, 1175, 1179, 1183, 1186 and 2315 of the
  Lean catalog each have demand 6 and a 28-state support inside F, and cover every F state exactly 3 times, so
  h(F) ≥ 18 for every vector satisfying the Lean rows; with h(Lo) ≥ 14 (N66 ≤ 56, Lemma A) the 34-hole cases are
  exactly (18,16), (19,15), (20,14).
- **Consequence:** the budget-33 baseline (h(C) ≥ 34, the ES(8) ≤ 309 chain) plus slices 18, 19 and 20 at budget 34
  give h(C) ≥ 35, |R| ≤ 119 and |S| ≤ 1 + 187 + 119 = 307: **ES(8) ≤ 308 without N5 ≤ 65.** Inputs used: the Lean
  components, N66 ≤ 56 (CERTIFIED, retained LRAT independently replayed), the budget-33 slice trees (EXACT TREE,
  VERIFY_LO), the three budget-34 slice trees (EXACT TREE), the 1,020 CERTIFIED coupled rows with their written
  encoder soundness, and the written bridge. Still a candidate: the independent audit `VERIFY308` (own tree checker,
  fresh LRAT checks) is running.

## 14-15 November night: towards ES(8) ≤ 307 (budget 35) and N66 ≤ 55 (in progress)

- With h(C) ≥ 35 (the 308 chain), ES(8) ≤ 307 needs the four 35-hole cases (18,17), (19,16), (20,15), (21,14)
  excluded at budget 35. Inputs `W/inputs/b35s{18,19,20,21}-v13` (`tools/prepare_slice_v2.py`, `916d8950…`: budget argument;
  same 1,020 coupled rows). **HEURISTIC** Knuth estimates (`fastbb2 dive`, 200 dives, `W/probe35/`): (18,17) 7.0e5 nodes,
  (19,16) 1.1e7, (20,15) 3.6e8 and a dive hit an abstract 35-hole witness (exit 3; holes in the unit journal), (21,14)
  4.3e9; for calibration the same estimate for budget-34 slice 20 v13 gives 2.3e7 (actual tree 3.1e7). (21,14) is the
  case where the Lo owners attain N66 = 56; **N66 ≤ 55 would remove it.**
- N66 ≤ 55 = level 14 of N66N20261113 (lazy monolithic search, CaDiCaL 2.1.3; stopped on 13 Nov at 23:50 after 3
  iterations). Resumed 22:55 with the record's own `p2_batch.py` (unchanged), two slots `esr-n66-s14h2` (warm
  `p2/s14/c.json`) and `esr-n66-s14i2` (warm `p2/s14/g.json`), both `--tauclose --sb --cadopts=--unsat`, ETV_A=ETV_B=4,
  MemoryMax 5.8 G (the certificate step's cake tiers go to 5.5 G; level 13 needed the 3.2 G tier), until 01:55.
  Two first attempts (`h`, `i`) stopped at import because the unit environment lacked ETV_A/ETV_B; nothing ran.
- Budget-35 tools: `tools/run_tree_v4.py` (`14b2c294…`; `--budget`, run folder `runs/b35s<T>`) and
  `audit/fresh_replay_v3.py` (`466aa324…`; budget from the input name `b<B>s<T>-v<k>`, capacity rows asserted (F, T), (Lo, B - T)).
  22:56 finder (18,17): `run_tree_v4.py 18 --budget=35 --input-folder=b35s18-v13 --tag=a --threads=6`.
- Memory guard restarted 22:54 as `esr-memguard2`: total 24 G, tracks lo 4 G, vfy 8 G, n66 9.5 G.
- 22:56-22:58 finder budget 35, (18,17): master 11,519 nodes, all 4,838 contexts closed (exit 0). 22:59 fresh replay
  `fresh_replay_v3.py b35s18/bb b35s18-v13 fresh-b35s18-v13 4`: **EXACT TREE** for budget-35 slice (h(F) ≥ 18,
  h(Lo) ≥ 17): 4,838 contexts, 416,935 nodes, 206,050 leaves, minimum margin 1, only state 0 missing pending; master
  `e1f3cfb9570ec360…`. First of the four budget-35 cases.
- 22:59 finder budget 35, (19,16) (`esr-lo-b35s19`, 6 threads). Budget-generic cut tools prepared, not yet run:
  `tools/cut34_v4.py` (`906db163…`), `tools/append_cuts_v2.py` (`5f0d1905…`), `tools/continue34_v5.py` (`010e7883…`; `--budget`),
  `audit/audit_followup_rows_v4.py` (`f0df1c0f…`).
- 23:04 finder (19,16) budget 35 stopped on an abstract 35-hole witness after 122 contexts (row check PASS). Cut loop
  `continue34_v5.py --slice=19 --budget=35 --start-version=13 --out=continuation-b35s19` (unit `esr-lo-b35s19loop`,
  deadline 02:00): round v14 11 rows, v15 13 rows CERTIFIED and appended (`inputs/b35s19-v14`, `-v15`), finder resumed.
- 23:20 VERIFY308 finished (independent tree checkers, 1,020 fresh LRAT acceptances); see the headline and
  [VERIFY308](VERIFY308/README.md), including the follow-up on the `pending_kernel` rows.
- 23:11 budget 35, (20,15): inputs `b35s20-v100` (identical rows to `b35s20-v13`; numbered from 100 so that its cut batches
  `cuts-v101…` cannot collide with the (19,16) loop), unit `esr-lo-b35s20`: finder `run_tree_v4.py 20 --budget=35 --tag=a`
  then the cut loop `continue34_v5.py --slice=20 --start-version=100 --out=continuation-b35s20`, deadline 02:00.
  Not expected to finish tonight (HEURISTIC estimate 3.6e8 nodes); closed contexts and certified rows are kept.
  Correction: that unit started at 23:11 (not 23:27). It ran rounds v101 (7 rows) and v102 (1 row), then stopped at
  23:15 with "no violated support in discovery pools": the precomputed pools have no row avoiding that witness.
- Discovery when the pools are exhausted: `tools/probe35.py` (`8f598d58…`; the method of
  `fastbb-20261113/killtools/probe_vec.py` with a copy of its encoder whose output paths are redirected to
  `W/discovery/`; HEURISTIC, proposes candidates only) and `tools/continue34_v6.py` (`e414e4eb…`; `--discover`: when the pool
  file of round k is empty it runs probe35 and certifies its candidates as batch `v<k>p`). On the stuck (20,15) witness
  probe35 tested 508 supports in 11 s and found 12 refuted ones; `cut34_v4.py certify` (pinned full encoder, LRAT,
  cake_lpr) accepted **12/12** as batch `v103p`; appended as `inputs/b35s20-v103`; unit `esr-lo-b35s20b` resumed the
  finder and then runs loop v6 with `--discover` until 02:00.
- Independent audit of the budget-35 batches (`audit_followup_rows_v4.py v14 v15 v101 v102 v103p`): **all CERTIFIED**,
  44 rows, own encoder matches 44/44, fresh cake_lpr 44/44, every row cuts its witness (witnesses re-checked against
  their input rows: 35 holes, F19/Lo16 resp. F20/Lo15, state 0 occupied).
- 23:20 the first loop v6 run (`esr-lo-b35s20b`, after finder `w103` hit the next witness) stopped at its first probe:
  as a loop child, probe35 inherited the loop's 100 MiB soft address-space limit and could not load numpy/OpenBLAS
  (`continuation-b35s20b/probe-v104.log`); nothing was certified or appended by that stage. Fix, copies:
  `tools/probe35_v2.py` (`b9948e95…`; raises its soft limit to the inherited hard limit, single-threaded BLAS) and
  `tools/continue34_v7.py` (`d3644f6b…`; calls probe35_v2; resumes an interrupted round by reusing its pool file after a
  witness-hash check). probe35_v2 was tested under `prlimit --as=100MiB:1.6GiB` (12 refuted supports for witness w103).
- 23:21 loop v7 (`esr-lo-b35s20c`, `--discover`, deadline 02:00): round 104 reused the empty pool file, probe found
  candidates, 12/12 CERTIFIED as batch `v104p`, appended as `b35s20-v104`; finder resumed.
- 23:52 finder `w16` closed all 7,170 contexts of budget-35 (19,16) (3 cut rounds v14-v16: 11 + 13 + 11 rows).
  Batch v16 independently audited: CERTIFIED 11/11 (own encoder, fresh cake). 23:53-23:55 fresh replay
  `fresh_replay_v3.py b35s19/bb b35s19-v16 fresh-b35s19-v16 4`: **EXACT TREE** for budget-35 slice (h(F) ≥ 19,
  h(Lo) ≥ 16) over 3,707 rows (extra `1257c4a15a52d894…`): 7,170 contexts, 15,533,581 nodes, 7,763,207 leaves,
  minimum margin 1, only state 0 missing pending; master `249497e821641bd3…`. **Two of the four budget-35 cases done.**
- 23:56 (20,15): loop v7 had run rounds 104-110 (each killing a witness; batches v104p … from probe35 or the pools);
  25 contexts closed of 8,065. Stopped by the operator during finder `w110` (no witness pending; closed files are
  written atomically) and restarted with 12 threads: `discovery/restart110.sh` (finder tag `x110` on `b35s20-v110`,
  3,749 rows, then loop v7 `--start-version=110 --out=continuation-b35s20d`), unit `esr-lo-b35s20d`, deadline 02:00.
- 00:16 independent C++ checker (VERIFY308 `tcheck`, budget-35 copy `tcheck_b35.cpp`) on both closed budget-35 packets:
  **EXACT TREE** for (18,17) (4,838 contexts, 416,935 nodes, 206,049 leaves, margin 1) and (19,16) (7,170 contexts,
  15,533,581 nodes, 7,763,206 leaves, margin 1); node counts equal the fresh replays. See the VERIFY308 addendum.
- 00:16 (20,15): rounds 110-114 had added few rows per witness (pools 1-3 rows). Loop v8 `tools/continue34_v8.py`
  (`7baa1b77…`; `--discover-always`: probe35_v2 every round, certify the union of probe and pool candidates as batch
  `v<k>u`). Stopped `esr-lo-b35s20d` during finder `w114` (after append-v114) and restarted: `discovery/restart114.sh`
  (finder tag `y114`, 12 threads, then loop v8 `--out=continuation-b35s20e`), unit `esr-lo-b35s20e`, deadline 02:00.
- 00:22 first loop v8 round: probe + pools gave 12 candidates, **12/12 CERTIFIED** (batch `v115u`), appended.
- 00:26 (20,15) restarted once more with 10 threads (to make room for the lower-bound track) and deadline 02:45:
  `discovery/restart115z.sh` (finder tag `z115`, then loop v8 `--out=continuation-b35s20f`), unit `esr-lo-b35s20f`.
- 00:26-02:45 (20,15) loop v8 (`continuation-b35s20f`): 13 rounds (v116u-v128u, 10-19 rows each, every round probe35 +
  pools). Its last finder (`w128`, 10 min) found no witness and stopped at the deadline (exit 4: some contexts over the
  50,000-node cap). Closed contexts: 45 of 8,065. **Independent batch audit of every (20,15) batch v101-v128u: all
  CERTIFIED, 279 rows** (own encoder + fresh cake_lpr, each row cuts its witness; batches audited one process each
  after a first multi-batch run hit the audit's own 300 MiB soft memory limit at v118u, with no replay written for it).
- 02:45 (20,15) restarted with 6 threads until 05:45 (`discovery/restart128q.sh`: finder tag `q128` on `b35s20-v128`,
  then loop v8 `--out=continuation-b35s20g`), unit `esr-lo-b35s20g`.
- 02:50 **re-estimate with all certified coupled rows** (`tools/prepare_union.py`, `829f502c…`: union in first-seen order of
  s20-v13, b35s19-v16 and b35s20-v128 = 1,333 coupled rows; inputs `b35s21-u1`, `b35s20-u1`). HEURISTIC `fastbb2 dive`,
  200 dives: **(21,14) 1.85e9 nodes** (was 4.3e9 with the 1,020 rows) and **(20,15) 3.3e8** (was 3.6e8); no dive hit a
  witness. Calibration: budget-34 slice 20 v13 estimated 2.3e7, real tree 3.1e7 nodes, about one hour of 12 threads
  including witness rounds. So (20,15) is roughly a 6-10 hour 12-thread job and (21,14) a multi-night job unless
  N66 <= 55 removes it; the witness-killing rows cut specific vectors but shrink the trees only modestly.
- 02:45-05:14 (20,15) continued: loop v8 runs `continuation-b35s20g` (6 threads), `-h` (12 threads from 04:47) and `-i`
  (6 threads from 05:00), rows up to `b35s20-v133`; stopped by the operator at 05:14 to give the agent probes threads
  (closed files are atomic; the stopped finder lost only contexts in progress). Final state: **54 of 8,065 contexts
  closed; every batch v101-v133u independently audited, 342 CERTIFIED rows** (own encoder + fresh cake_lpr, one process
  per batch). Resume: `run_tree_v4.py 20 --budget=35 --input-folder=b35s20-v133 --tag=<new> --threads=<t>` then
  `continue34_v8.py --start-version=133 --slice=20 --budget=35 --discover --discover-always --start-receipt=<that receipt>`.
- 05:25-06:24 (20,15) loop v8 at 4 threads (`continuation-b35s20j`): one more round (v134u); then stopped at a safe point.
- **Batch loop v9** (workflow `es-batch-loop-v9`, review verdict *ready*, no soundness defect): `tools/run_tree_v5.py`
  (`ce1e9b4e…`; `--on-witness=continue`, every logged witness written once as `WITNESS.json.r<k>w<i>` and exact-row-checked)
  and `tools/continue34_v9.py` (`e009f52a…`; per round: finder slice in continue mode, then pool select + probe35 per witness,
  certification capped at 8 rows per witness, ONE merged append through the unchanged `append_cuts_v2.py`). Tested end to
  end in a separate namespace (inputs `b35s20-v500..v502`, packet `runs/b35s20/bb-v9test`; 7 batches `cuts-v501w*u`,
  `cuts-v502w*u` audited CERTIFIED — these test audits sit next to the live ones in `audit/` and must not be counted as
  live rows). Main throughput finding: each finder start re-walks the open contexts from context 0, most of which exceed the
  50,000-node cap (165 of contexts 0-218 in the live run).
- 06:25 **(20,15) switched to `tools/continue34_v10.py`** (`8f37ddfc…`; v9 plus `--max-ctx-nodes` passed to the finder),
  unit `esr-lo-b35s20v10`: `--start-version=134 --threads=6 --max-ctx-nodes=150000 --slice-seconds=600 --max-witnesses=12
  --accept-per-witness=8`, deadline 09:45, output `continuation-b35s20v10a`. Resume after an interrupted round with
  `--start-receipt=<the receipt named in the last 'round' event>` (reviewer's note).
- 06:25-09:35 **(20,15) loop v10, final state** (`esr-lo-b35s20v10`, 6 threads, 18 h 49 min CPU in 3 h 11 min):
  - Rounds v135-v138 appended certified rows up to `inputs/b35s20-v138`.
  - Every row batch, v134u-v138w1u, was **independently audited** at 09:04 by the main session with
    `audit/audit_followup_rows_v4.py`, one process per batch. All 10 batches are CERTIFIED: 85 rows, own encoder 85/85,
    fresh cake_lpr 85/85, and every row cuts its witness.
  - **Total for (20,15): 43 batches and 427 CERTIFIED rows**, recounted from the audit summaries (342 in v101-v133u, 85
    from v134u on).
  - **Closed contexts: 555 of 8,065** (`runs/b35s20/bb/ctx-*.json.gz`; 54 at 05:14, 483 at 09:04). Many open contexts
    exceed the 150,000-node cap.
  - The last round (version 138, receipt `runs/b35s20/c138s1.json`) logged 5 new witnesses. The 09:35 deadline came
    before batch v139w1 was certified (`deadline_in_round`, then `FINISHED`, not broken).
  - Resume: `tools/continue34_v10.py --start-version=138 --slice=20 --budget=35 --start-receipt=runs/b35s20/c138s1.json`,
    with the other options of the 06:25 line.
  - (20,15) is not closed, so ES(8) ≤ 307 is not reached.
- 13:12-18:40, 15 November **(20,15) loop v10b, final state.** Unit `esr-lo-b35s20v10b`, 4 threads, result success.
  Details are in [ADDENDUM_1115PM.md](ADDENDUM_1115PM.md) (track U2) and [ANALYSIS_1115PM.md](ANALYSIS_1115PM.md) (track A2).
  - Rounds v139-v143 appended **80 rows in 10 batches**. U2 audited all of them independently: 80/80 CERTIFIED (own
    encoder, fresh cake_lpr, each row cuts its witness). **Total for (20,15): 53 batches and 507 CERTIFIED rows.**
  - **Closed contexts: 998 of 8,065** (555 at 09:35).
  - A2 found that each finder start re-walks every known too-big context. That costs about two thirds of the finder's
    time; skipping them is A2's first proposal.
  - Resume: `--start-version=143` and no receipt (round 142 was appended as v143), with the other options of the v10
    line.
  - (20,15) is not closed, so ES(8) ≤ 307 is not reached.
- 18:52-20:36, 15 November **(20,15) loop v10c** (`esr-lo-b35s20v10c`, 4 threads; `--start-version=143`). Round 143
  was appended as `b35s20-v144` (16 rows, 20:03:59). The loop was stopped by the main session at 20:36 during finder
  c144s1, a safe point (event `FINISHED`, stopped). The audit of the v144 batches is owed (track VB/U2 rule).
- 20:36 **switched to the skip-list finder v11**:
  - `tools/run_tree_v6.py` (`d6608ce9…`) and `tools/continue34_v11.py` (`81d2c9e2…`), by track S1; notes in
    [tools/V11_NOTES.md](tools/V11_NOTES.md).
  - Independent review [tools/V11_REVIEW.md](tools/V11_REVIEW.md) (S1R): **READY WITH NOTES**. The skip list only
    changes fastbb2's `--ctx` selection; COMPUTED_CLOSED still needs every context of the full master; the witness,
    exact-row and cut/probe/append paths are unchanged.
  - Live too-big record `runs/b35s20/bb/TOO_BIG.txt` (`init_too_big_v1.py … --log=c144s1`; 3,391 events from 47 logs;
    77 open contexts above 150,000 nodes; SHA-256 `91679b5a…`).
  - Unit `esr-lo-b35s20v11a`: `--start-version=144`, no receipt, `--threads=3 --extra-cap=300000 --extra-threads=1`,
    the other v10 options, deadline 22:40, output `continuation-b35s20v11a`.
  - Liveness note from the review: the contexts recorded above the extra cap still need the standalone high-cap pass
    (V11_NOTES §4) before (20,15) can close.
- 20:36-22:39, 15 November **(20,15) loop v11, final state** (`esr-lo-b35s20v11a`, 3 frontier + 1 extra thread,
  result success).
  - **1,504 of 8,065 contexts closed** (998 at 18:40).
  - Appends v145-v148, 31 rows. With v10c's v144, that makes 47 rows in 6 batches tonight, all audited CERTIFIED by the
    main session at 22:40.
  - **Total for (20,15): 59 batches and 554 CERTIFIED rows.**
  - Resume: `continue34_v11.py --start-version=148`, no receipt, with the v11 options. The high-cap pass over the
    contexts recorded above 300k is still owed (tools/V11_NOTES.md §4).

**Retention (25 Nov 2026; owner re-approved after declining on 18 Nov: "yeah keep cleaning ...", answering whether the
b35s20 finder test packets may go).** The finder test packets `~/research/data/es308-20261114/runs/b35s20/{bb-v9test,
bb-v11test, bb-v11test2, bb-v12test*, bb-r1118*}` (51 exact paths, 2,466 files, 15.35 GB; cleanup id C38) are deleted after
`receipts/b35s20_test_packets_20261125.tsv` is pushed and an advisor check. No result depends on them; the V11/V12 review
documents of `tools/` (V11_REVIEW.md, V12_REVIEW.md, VERIFY_V11*.md, the claims s1-v11-*, s1r-v11-review,
r-v12-review-1118) lose in-place reproducibility. Never touched: `bb`, `bb-s1` (the s35_20 tree, input of its running
Lean campaign) and `bb-hc1*`.
