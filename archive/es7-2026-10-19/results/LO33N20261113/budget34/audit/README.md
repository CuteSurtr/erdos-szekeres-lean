# Final budget34 audit — 971 rows CERTIFIED; slice19 EXACT TREE; slice20 PARTIAL

**Finalized14 November2026 at10:48 KST. ES(8)<=308 is not established by
this pass. All audit jobs are inactive.**

| item | independently checked outcome |
|---|---|
|Coupled rows|971 full-CNF reconstructions and971 fresh cake acceptances|
|Slice19, budget34, (F19,Lo15)|EXACT TREE;3643/3643 contexts;1,658,483 nodes; minimum margin1; sole pending state0 missing|
|Slice20 v5, budget34, (F20,Lo14)|PARTIAL;1222/4064 contexts;11,366,003 nodes; minimum margin1|
|Unfinished slice20 frontier|2842 contexts, plus the deliberate state0 branch:2843 global pending leaves|
|Tail imports|All76+115 imported contexts independently replayed and source/destination hashes matched|
|Written corollary|No actual residual configuration has both F population>=65 and Lo population>=55; no N5/N66 input needed|

All published slice20 context files were replayed. After the controller
stopped cleanly at10:46:38, every context hash and all frozen epoch inputs
were checked again; the master was stable at v5. This is **not** a
discovery-SAT claim for v5 and is not a complete slice20 exclusion.
The final packets are `incremental/finished-by-control.json`,
`final-audit.json`, `tail-import-audit.json` and `final-manifest.json`.

14 November 2026. This worker owns provenance and eventual new-tree replay.
All writes are confined to this audit directory and
`/home/jay/research/data/es308-20261114/audit/`. Earlier packets stay read-only.

## Statement and exact scope

The proposed conclusion is ES(8) <= 308. The inherited ES309 result already
gives at least34 holes for an actual residual configuration. The catalog has
154 states. F comprises84 states with f1>=5 and Lo comprises the other70.
The written geometric partition lemma and N5<=65 give h(F)>=19;
N66<=56 gives h(Lo)>=14. At exactly34 holes the only possibilities are:

| slice | h(F) | h(Lo) | F population | Lo population |
|---|---:|---:|---:|---:|
|19|19|15|65|55|
|20|20|14|64|56|

Thus the new trees must exclude budget34 with capacities **(F,19),(Lo,15)**
and **(F,20),(Lo,14)** respectively. Their rows consist of the pinned2650
Lean rows, these two capacities, and initially the same812 frozen
demand-one rows. Slice20 now has append-only strengthening to956 coupled
rows, independently audited below. The completed slice19 proof retains
its original, weaker row system unchanged.
Two completed exact replays would force35 holes and residual population119;
the existing balanced bound187 and composition give187+119+2=308.
No budget33 tree is sufficient for the new exclusions. The old witness
killer's hardcoded `len(H)>33` is invalid at budget34 and is not invoked.

## Model and evidence boundary

Read `VERIFY309N20261113/README.md` link(c), the followup56 audit, and
`ETV5N20261113/VERIFY_N5.md`. Link(c) supplies the written soundness of the
residual coupled encoder; the geometric meaning of certified CNFs is
inherited from that argument. This audit independently reconstructs each
support CNF without importing the original encoder or its tables and
replays its retained LRAT with cake_lpr. It does not rebuild the N5 or N66
main certificates, and it does not produce a Lean theorem.

## Provenance findings

Frozen pool SHA-256:
`91a4e36f31712231ed1386576d6dcbe846ddf6c1b0d4de41e225bbdb4a18bcf8`.
Its ordered rows equal s23 `extra.json[2:]` exactly,812 distinct supports.
There are101 nine-state,355 thirteen-state and356 fourteen-state supports.

All812 have retained CNF/LRAT pairs:705 in p2/proofs and107 in
killtools/proofs,1,052,108,158 compressed bytes in total. The killtools
ledger alone covers804 rows; the remaining8 are the LO33 additions
carried by p2/pool/pool_v1.json and p2's recertification inventory.

Prior audit coverage: VERIFY309 covers578 (448 fresh,130 inherited from
VERIFY_LO); VERIFY_G covers570 plus2 separately re-certified kill rows.
These sets overlap; they must not be added. Their union is580 rows;
232 have no matching earlier independent audit in these inventories.
234 pool rows lie outside VERIFY309. Actual earlier cake stdout survives
for448 rows. p2's705-row
ledger records acceptance strings but did not retain individual stdout.
`pool_inventory.json` enumerates exact support/CNF/LRAT identities,
retained files and every matching prior audit entry. Ledger statements
alone are not treated as a fresh acceptance.

## Method and resources

`residual_encoder.py` is new scalar code for the audited clause families.
It recreates variable numbering, source/domain constraints, six-order
forced signs and all state-independent clauses. Initial independent
9-,13-,14-state reconstructions matched the recorded hashes.
`pool_audit.py` checks all812 reconstructions, decompresses retained files,
matches raw and compressed identities, and requires an exact stdout line
`s VERIFIED UNSAT` from each new cake replay. Sources are rehashed after
use. No source packet is written, no solver search is run, and no proof
is deleted. Full replay completed at10:12:14 KST: **812 independent encoder
matches,812 retained CNF/LRAT hash matches,812 fresh exact cake stdout
acceptances**. `pool_summary.json` and `pool_replay.jsonl` pin every outcome.
Total237.48s wall;213.498s unit CPU time. No row remains pending.

Unit `nov13c-vfy-308-audit-pool812`: one CPU, affinity10, MemoryMax1600M,
Swap0, RuntimeMaxSec2400. Python AS300MiB plus one sequential child
AS800MiB leaves100MiB for bounded control; cake heap400/stack32. Measured
peak RSS85.5MiB Python and403.3MiB children. Read-only POSIX_FADV_DONTNEED
on completed source packets released cgroup file cache without changing
proof content; the maximum observed cgroup charge was1,284,554,752 bytes.
No new long unit after10:45;
finish by10:55. The active guard is `memguard5-20261113.service`.

## Tree replay and remaining work

`replay34.py` re-derives master paths and checks the frozen row-file order,
source, capacities, and full812-row pool. It verifies every saved context
with `scripts/omission_tree.check_tree` at budget34 and stores resumable
hash-bound receipts. Duplicate contexts, altered path sets, unfinished
subtrees and unexpected files are rejected. The13 deliberate corruptions
in `wrapper_controls.json` all fail as intended, including a budget
off-by-one control. Artificial pending siblings are removed from the
global count; state0 missing is the one deliberately retained branch.

Unit `nov13c-vfy-308-audit-tree34` started10:13:08 KST, after the pool unit
finished. It uses one CPU, affinity10, AS1000MiB, MemoryMax1600M, Swap0,
RuntimeMaxSec2400 and a2300s work deadline (about10:51:30). It bounds a
context load using40 times compressed bytes plus80MiB and defers one
estimated above900MiB. Each read-only context packet's cache is advised
away after its hash check. No huge old tree is loaded.

At10:16:01 KST, **slice19 completed EXACT TREE**: all3643 master contexts,
1,658,483 nodes,829,242 leaves, minimum integer margin1, exactly one global
pending leaf (state0 missing).447 coupled rows have positive weights.
The capacities are exactly(F19,Lo15), at budget34.
`s19-summary.json` pins the result and all input identities.
Slice20 has4064 master contexts and remains open; its current checkpoint
is now `incremental/latest-summary.json`, labelled PARTIAL EXACT REPLAY
until full coverage. This file names the exact current input version.
Only a tree with every
master context covered and the sole global pending leaf "state0 missing"
can receive EXACT TREE. Current status is **not confirmed** for ES308.

The detailed independent argument and identity boundaries are in
[VERIFY_BUDGET34.md](VERIFY_BUDGET34.md).

## Appended rows and versioned replay

The original slice20 finder produced a34-hole vector satisfying all3464
rows; own exact checks confirmed it. Seven new support rows were each
independently reconstructed and freshly accepted by cake at10:20:36 KST.
All seven cut that vector. V2 has3471 rows; its finder produced another
valid finite-model vector. All134 saved v2 contexts were independently
replayed before the watcher stopped:2,623,651 total nodes including the
remaining frontier, minimum margin1,3931 global pending leaves.

An additional128 nearby nine-state rows and9 direct v3 witness cuts all
passed independent full-CNF reconstruction and fresh cake replay at
10:25:37. The nearby128 each meet the first witness in one hole and do not
refute it; the9 direct rows each refute the second finite-model witness.
The exact append count is137=128+9, yielding
956=812+7+128+9 coupled rows and3608 total rows in v3.

Per-row proof records are in cuts-v2/, cuts-near9/ and cuts-v3/. The new
generic wrapper replay_batches.py checks the entire immutable manifest
chain, ordered prefix equality, each original acceptance receipt, each
own fresh acceptance log and the final rows.txt order. Its v3 preflight
matches extra SHA a17f889c980d00a896312e4a17c83105108c1034b4d6bbbebc2593062016c331
and rows SHA b586b2ffa56368b84e032a4f53ef67abdd3e21a9c0108fd8fc91b78504309263.
V1 and v2 summaries are preserved. A single v3 watcher uses CPU10,
AS1000MiB, MemoryMax1600M, Swap0 and a1500s work budget, absolute stop
before10:53. ES308 remains unconfirmed until slice20 closes.

## Incremental continuation

V4 adds10 direct rows, all independently reconstructed and freshly
accepted at10:30:45. It has3618 total rows and966 coupled rows. The v3
watcher stopped safely on a master-metadata change and made no closure
claim;151 completed context receipts were retained.

The single unit nov13c-vfy-308-audit-incremental started10:33:23. It
audits every newly completed row batch before admitting its immutable
input version, pins master/context-description copies under W/audit,
and carries old exact receipts only across identical context hashes and
paths with an explicitly hashed ordered row prefix. Each carried record
retains its original version, source receipt and maximum used row index.
The first151 transfers cover2,987,123 checked subtree nodes. New leaves
still go through check_tree at34. A final closure needs all4064 contexts
and an unchanged current master, with the sole pending state0 branch.

Prior summaries and row scripts are preserved rather than overwritten.
The current controller uses AS1000MiB during tree replay and AS300MiB
plus one child AS800MiB during row replay, never concurrently. It has
quota100%, affinity10, MemoryMax1600M, Swap0, RuntimeMaxSec1300 and an
internal10:53 stop. No new long unit is needed after10:45.

The final v5 append added5 independently certified direct cuts, completed
at10:43:30. V5 has3623 total rows and971 coupled rows. The final worker
was stopped early once every published context had been checked, using
530.035 CPU seconds over794.981 wall seconds with770.4MiB cgroup peak and
no swap. No new long unit started after10:45. Source packets, proof files,
the completed slice19 packet and all prior records were preserved.
