# Independent audit of the direct budget34 pass

**FINAL:971/971 coupled rows confirmed through v5 — CERTIFIED (812 initial plus159 added).
Slice19 is confirmed —
EXACT TREE. Slice20 is PARTIAL:1222/4064 contexts checked,2842 missing.
ES(8) <= 308 is not confirmed. All audit jobs stopped by10:46:38 KST.**

This audit was written from new code in this directory. Source data and
earlier research records were opened read-only. No finder, old verifier,
old witness killer, or original coupled encoder was imported by the new
reconstruction and replay code. The trusted integer tree checker is the
requested `scripts/omission_tree.check_tree`.

## 1. Independent provenance results

The ordered frozen pool is exactly the 812 rows of s23 `extra.json[2:]`.
All supports are strictly increasing, unique, in 0..153, and have integer
demand 1. The frozen file's SHA-256 is
`91a4e36f31712231ed1386576d6dcbe846ddf6c1b0d4de41e225bbdb4a18bcf8`.

| source or prior independent audit | matching pool rows | evidence qualification |
|---|---:|---|
| killtools/certified.jsonl |804|old ledger, not sufficient by itself|
| p2/proofs/recert.jsonl |705|retained pairs, old per-row stdout not saved|
| p2/pool/pool_v1.json |614|identity source, not itself an acceptance|
| VERIFY309 residual audit |578|448 fresh proofs plus130 inherited from VERIFY_LO|
| VERIFY_LO |130|subset of the578|
| VERIFY_G main audit |570|subset of the578|
| VERIFY_G two kill-row audit |2|pool indices578 and579, outside the578|
| new audit here |812|every CNF independently reconstructed; every retained LRAT freshly accepted|

Indices are zero-based in the frozen pool. Indices570..577 are the eight
LO33 additions absent from the killtools ledger. Their CNF/LRAT identities
match both pool_v1 and p2 recertification. The union of the named prior
independent audits covers580 rows, so232 rows gain their first matching
independent replay in this audit's checked inventories. This is a statement
about those inspected inventories, not a claim that no other audit exists.

Exactly705 retained pairs are in p2/proofs and107 in killtools/proofs. Every
support/CNF/LRAT match, prior audit entry number, and retained path is listed
in `pool_inventory.json`. It also records the448 surviving old cake stdout
logs and their literal acceptance lines. All identifying hashes agree
across the matched records; no missing, ambiguous or conflicting pair was
accepted. The original compressed sources occupy1,052,108,158 bytes.

The fresh replay finished at10:12:14 KST in237.48 wall seconds. For every
row, in order:

1. New scalar code reconstructed the complete DIMACS bytes and matched the
   recorded CNF SHA-256.
2. Retained compressed CNF and LRAT were hashed, decompressed, and their raw
   SHA-256 values matched the same support's certificate identity.
3. cake_lpr ran on that identified pair with heap400/stack32. The exact
   stdout line `s VERIFIED UNSAT` was required. Exit status was recorded
   but was never used as the acceptance condition.
4. Raw and compressed file hashes were checked again after replay. All
   pinned inputs and executables were rehashed at the end.

`pool_replay.jsonl` binds those operations and actual stdout/stderr hashes
for all812 rows. `pool_summary.json` pins the inventory and replay ledger.
Raw new checker logs remain in W/audit/cake. Source proofs remain retained
and unchanged. There are no unresolved row certification obligations.

This section describes the original812-row pool. The appended144 rows
have separate identities and accepted proof replays in section7 below;
the original inventory and proof receipts remain frozen. V4 adds another
10 rows, described in section8.

## 2. Encoder identity and written soundness

The applicable written proof is VERIFY309N20261113 link(c). It assigns to
an actual residual pair u<v the label
`(6 - longest cap starting with (u,v), longest cup ending with (u,v) - 1)`.
These labels justify thresholds, source cup ceilings, cell-domain
differences with (1,6) excluded, chronological transitivity and cap/cup
growth. The scalar six-order forcing test uses unrefined cell differences,
so it is conservative. Signotope packets, the convex-four truth table,
and the complete no-octagon clauses are geometric necessities as explained
in that audit. Therefore UNSAT of a support's full CNF forces a hole in
that support.

`soundness_source_links.json` pins the audited RES33N encoder, current
killtools encoder and common sources, plus the written audit records.
The encoder diff consists only of three scratch-directory strings; clause
generation is unchanged. `residual_encoder.py` independently implements
the same public variable numbering and clause order, using scalar cell
sets and explicit six-order tests instead of importing NumPy tables or
the original code. State-independent bytes are freshly generated once
per support size, and the source/domain/sign clauses are regenerated for
each actual support. All812 complete hashes agree, so this is an identity
reconstruction of the previously audited CNFs, not a new clause family.
No additional geometric assumption is introduced.

The154-state catalog and2650-row source are pinned by decompressed SHA-256
`e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6`.
This audit does not independently redo the Lean proof of those base rows.

## 3. Exact two-slice scope

The N5<=65 audit in ETV5N/VERIFY_N5 and the N66<=56 follow-up in
VERIFY309/followup56 are inherited inputs. Their large main certificates
were not replayed under this worker's small memory allocation. The latter
audit reports a fresh acceptance of the retained N66 proof and four newly
certified row obligations; the N5 audit includes its own32-cube PB encoder
and accepted proofs. The ordinary geometric transfer of these bounds to
the F/Lo owners is the written Lemma A used in LO33/VERIFY_LO.

F is the84 catalog states with first component at least5. Lo is the
complement of70 states with first component at most4. Thus h(F)>=19 and
h(Lo)>=14 for actual residual configurations. The already established
ES309 residual result gives total holes at least34. A counterexample to
the stronger residual119 bound would therefore have exactly34 holes.
Writing t=h(F), we get19<=t<=34-14=20. The cases are exactly:

| t | required capacity rows | population pair |
|---|---|---|
|19|(F,19), (Lo,15)|(65,55)|
|20|(F,20), (Lo,14)|(64,56)|

The slice19 Lo15 row is a consequence of that *slice's exact hole count*,
not a claim of the stronger universal N66<=55. Likewise slice20's F20
row is conditional on the slice, not a claim of universal N5<=64.

The empty residual configuration satisfies the proposed population bound
immediately; state0 occupancy is needed only for the nonempty case.
Excluding both cases at budget34 would imply at least35 holes, hence
at most154-35=119 residual points. With balanced population187 the existing
composition gives187+119+2=308. These would be computer-assisted written
results with exact tree arithmetic and certified row inputs; they would
not be an unqualified Lean theorem `Excludes2650Zero 34`. The extra
capacities and coupled rows must remain explicit in any formal interface.

## 4. New-tree wrapper and controls

`replay34.py` accepts only the new frozen W/inputs and the new tree
directories W/runs/s19/bb and W/runs/s20/bb. It checks the
complete source bytes, exact row count and order in the compiled finder
row files, both capacities, the ordered812-row pool and every fresh cake
log/hash binding. No verdict-only pool item is sufficient.

The wrapper traverses the master independently, validating tree structure,
variable uniqueness along paths, node reachability and a bijection of
context identifiers. It compares contexts.json and each context file to
the complete derived path, with state0 occupied at the root. It calls
check_tree at budget34 on the master and every context, wrapped in the
derived path with artificial pending siblings. All internal pending leaves
are rejected. It removes those artificial siblings when computing the
global totals. Full closure requires every master context to be present
and replayed, no unexpected context files, unchanged input hashes, positive
integer margins, and exactly one pending leaf: state0 missing. The latter
is discharged by the existing zero_mem_residualOccupied geometric fact.

The13 negative controls in selftest_replay.py include duplicate identifiers,
shared or invalid children, repeated state0, unreachable nodes, corrupt
stored paths, an unfinished context, an unjustified over-budget leaf and
the34-versus35 arithmetic boundary. All are rejected; a valid synthetic
budget34 leaf has margin1. These are checker controls, not evidence for
the actual finite exclusion.

Master preflight succeeded for3643 contexts in slice19 and4064 in slice20.
All master weighted leaves have positive exact margins, minimum1.
At10:16:01 KST the complete slice19 replay succeeded:3643/3643 contexts,
1,658,483 nodes,829,242 leaves, minimum exact margin1, sole global pending
leaf state0 missing. This establishes the conditional(F19,Lo15) exclusion
at budget34.447 coupled rows are actually used with positive weights;
the full812-row file has fresh accepted proof coverage regardless of use.
`s19-summary.json` records the frozen input and checker hashes and pins
the individual context receipts. Its receipt SHA-256 is
`06d6a59e99846ae7468678d7e9355ff396b77a5f2a46bbf06eecba35e3be21b1`.
Slice20 is still partial. Context receipts and current summaries are
saved under this directory.
**A partial replay does not exclude any missing master context and does
not establish either slice or ES308.**

## 5. Resources and limits

Both audit jobs run sequentially, one CPU on affinity10, MemoryMax1600M,
Swap0, RuntimeMaxSec<=2400. The proof driver used parent AS300MiB plus one
child AS800MiB; quick controls used AS100MiB. Peak RSS was85.5MiB for Python
and403.3MiB for children. The tree wrapper uses AS1000MiB and bounds each
context load before parsing. Read-only cache advice prevents accumulated
source/closed-context page cache from approaching the unit limit. Cache
advice does not change file contents or delete a proof.

No old huge tree was loaded, no new search was duplicated, no third-party
code installed, no proof directory deleted, and no Git mutation occurred.
No new long unit may start after10:45; the current replay's work deadline
is approximately10:51:30, with an absolute internal stop before10:54.
Later context files can be resumed in a separately authorized session.

## 6. Concrete commands and artifacts

The completed proof replay is intentionally exclusive: pool_audit.py
refuses to overwrite an existing pool_replay.jsonl. A future repeat should
use a separately reviewed output directory rather than rerun it over this
packet. Its accepted rows can be reviewed directly in pool_verified.tsv;
the row indices in that table identify the exact positions2652..3463
after the2650 base rows and the two slice capacities.

Read-only structural preflight (AS100MiB was sufficient here):

```bash
python3 -B cloud/es7-2026-10-19/results/LO33N20261113/budget34/audit/replay34.py --preflight
```

The long replay, run only in its bounded unit and within the approved
deadline, is:

```bash
python3 -B cloud/es7-2026-10-19/results/LO33N20261113/budget34/audit/replay34.py --watch --seconds=2300
```

pool_inventory.json and pool_replay.jsonl give all per-row identities and
raw cake log locations; pool_summary.json pins them. The independent
reconstruction code, wrapper, controls, small resource receipt and written
source links are in this directory. New large tree packets and all old
compressed proof packets remain at their original read-only source paths.

## 7. Append-only strengthening after finite-model witnesses

The original slice20 finder stopped on a34-hole Boolean vector, not a
real point-set counterexample. Own exact checks verified all3464 rows,
state0 occupied, F20 and Lo14. Its actual file SHA-256 is
fbb91635e1a9fb342ccabc41ca1244192284e16053e7390d75f9d26e22a61a52.
Seven candidate support rows were independently reconstructed with
residual_encoder.py and their retained LRATs freshly replayed. All seven
had matching CNF/LRAT identities and literal new cake acceptances;
all seven are disjoint from that witness's holes. Completed10:20:36,
2.513 seconds. Evidence: cuts-v2/summary.json and replay.jsonl.

The v2 manifest adds exactly those seven rows to the original ordered
extra file. Own preflight checked the3471-row text file, the prefix and
all provenance bindings. Replaying all134 saved v2 contexts yielded
2,623,651 nodes,1,311,826 leaves, minimum margin1,3931 global pending leaves.
The watcher stopped at the parent's request after the second finite-model
witness; its summary and receipts remain under s20-v2/. This is PARTIAL
EXACT REPLAY, not a slice exclusion.

That second vector's packet SHA-256 is
44d406ac6d10cc7982537baa66e985c351045a56e28dbbe36ccc0358738b52fd.
Own exact checks confirm34 holes and every3471 v2 row. The next append is:

| batch | independently reconstructed CNFs | fresh accepted LRATs | intersection with its cited witness |
|---|---:|---:|---|
|near9|128|128|exactly1 hole each; no witness refutation|
|direct v3|9|9|zero holes each; all9 cut the second vector|

The new generic audit_batch_rows.py pins the actual witness snapshot
specified by the candidate hash, checks the applicable original row file,
and records intersection counts separately from certificate acceptance.
It never treats a nearby support as violated without computing the
intersection. The batches completed at10:25:34 and10:25:37 KST in8.337 and
2.203 seconds. Actual stdout is under W/audit/cuts-near9 and cuts-v3;
the per-row bindings and summaries are under the matching record folders.
The batch unit used7.632 CPU seconds,10.666 wall seconds,459MiB peak.

V3 adds the ordered137-row combined list to v2, giving956 coupled rows
and3608 total rows. replay_batches.py validates the entire manifest chain,
checks original acceptance receipts and own fresh logs for every added
support, proves exact prefix preservation, and checks every text-row index.
The accepted combined-list SHA-256 is
76fc9346976a67d6d37dfb21d84098b31dd2f626ab1b7f313a3c56484b3e45a7.
Final extra SHA-256:
a17f889c980d00a896312e4a17c83105108c1034b4d6bbbebc2593062016c331.
Final rows.txt SHA-256:
b586b2ffa56368b84e032a4f53ef67abdd3e21a9c0108fd8fc91b78504309263.

V3 context replays go into s20-v3/, preserving earlier packets. The
completed slice19 proof uses only its original812 coupled rows. This
difference is harmless for the two-case geometric argument: every actual
residual configuration satisfies both certified row pools, and each
slice can be excluded using its own valid subset of those constraints.
No fresh slice19 replay or alteration is required. Slice20 is still open.

## 8. Incremental continuation and transfer of checked contexts

The v4 append contains10 additional direct rows. Each independently
reconstructs to its retained CNF hash and has a new literal cake acceptance;
the batch completed10:30:45. Evidence is in cuts-v4/. The immutable v4
system has3618 rows, of which966 are coupled rows. The v3 full-pass
wrapper detected the changed current master and stopped on its final
hash guard; it did not issue a summary claiming closure. Its151 finished
context receipts still identify individually checked subtrees.

The incremental controller validates the historical input bindings using
the parent's retained version snapshots, then pins its own master and
context-description copies under W/audit/incremental. A carried receipt
contains the original input version, original row count and ordered-prefix
digest, original ledger and line hashes, current subtree hash, path, and
maximum row index used with positive weight. It transfers only if the
current rows begin with exactly that old ordered row system, the actual
subtree bytes are unchanged, and the complete current master path agrees.

This transfer preserves each checked integer margin: every multiplier
continues to refer to the identical support and demand, the missing and
occupied sets are unchanged, and the budget remains34. Newly appended
rows have no weights in that previously checked leaf, so they contribute
nothing to its loads or lower bound. The old structural check also remains
valid for identical subtree bytes. Appending valid constraints therefore
cannot invalidate that exact subtree proof. This is a proof transfer,
not a finder verdict or a claim based on the current pool's label.

The initial carry step checked151 context identities and transferred
2,987,123 already checked subtree nodes. Every new context is replayed
with check_tree against one pinned version. If the current master advances,
the controller changes epoch and checks new row certificates before
using the new version. An unfinished or incompatible context is not
counted. Checkpoints list every still-pending frontier context explicitly.
Full closure additionally requires the complete master frontier, positive
minimum exact margin, a current unchanged master and only state0 missing
as the global pending leaf. The controller's latest summary is under
incremental/, with frozen older version summaries alongside it.

The single incremental unit started10:33:23 KST and uses one CPU. It
switches between tree AS1000MiB and row-audit parent AS300MiB with a single
child AS800MiB; there are no simultaneous audit workers. Checker heaps
remain400/32. New row batches are checked before continuing tree work.
The unit has RuntimeMaxSec1300 and an internal10:53 stop, leaving time
for final reporting by10:55. No long unit starts after10:45.

## 9. Independent written corollary of the completed slice19 tree

The completed tree also excludes any Boolean hole vector satisfying the
original3462 non-capacity rows, state0 occupied, h(F)<=19 and h(Lo)<=15.
Indeed, extend the holes inside F to exactly19 and inside Lo to exactly15,
always keeping state0 occupied. There are84 F-states and69 eligible
nonzero Lo-states, so this is possible. Every row is a nonnegative lower
bound on missing states, hence remains satisfied after adding holes.
The resulting vector satisfies the slice19 capacity rows with exactly34
holes, contradicting its exact tree.

For an actual nonempty residual configuration this gives the written
Pareto statement: **F population>=65 and Lo population>=55 cannot both
hold**. The empty case is immediate. This uses the coupled-row soundness
and the completed exact tree, but neither N5<=65 nor N66<=56. This audit
has not independently replayed any new Lean file for that corollary.

## 10. Final stable checkpoint and shutdown

The final v5 append contains5 direct witness cuts. All5 independently
reconstructed CNF hashes and fresh cake stdout acceptances passed at
10:43:30.792 KST in1.636 seconds. The exact preceding witness passed all
3618 v4 rows, with34 holes, F20, Lo14 and state0 occupied; each new row
is disjoint from that witness's holes. The retained witness packet hash
is2adcfb0e749e181d7a192d9b57ed3f81b5e055ad50d569dd7403aa497ff65ee1.
This does not assert a witness for v5.

Final row total:2650 base+2 capacities+971 coupled=3623. The coupled count
is812+7+128+9+10+5. The final master SHA-256 is
ab1b3b888c376011c0b8587f19fbf9989d76c56f444f8d46bdfacaef637339ad.

| final v5 replay statistic | value |
|---|---:|
|master contexts|4064|
|present and independently replayed|1222|
|missing contexts|2842|
|global pending leaves, including state0 missing|2843|
|nodes in partial assembled tree|11,366,003|
|leaves in partial assembled tree|5,683,002|
|minimum checked integer margin|1|

The two tail imports contributed76 and115 closed contexts. Their original
source files, destination files, import receipt hashes and exact-replay
hashes were compared independently; all191 match. Their context paths,
row bindings and leaf arithmetic were checked in the final v5 replay, not inferred
from the parent's import status. See tail-import-audit.json.

At10:46:38 the parent had stopped discovery and every published context
had been audited, so the controller was stopped using systemctl rather
than idling until its deadline. The final control then rehashed all1222
context files and every pinned epoch input, verified their exact match to
the receipt set, and checked that the missing contexts are exactly the
complement in the4064-context master frontier. The master remained stable.
The result and full context hash list are in
incremental/finished-by-control.json. The controller used530.035 CPU
seconds over794.981 wall seconds; cgroup peak770.4MiB, swap0.

The remaining2842 contexts are genuine unfinished obligations in this
packet. Neither the finder stopping nor the partial exact checks establish
a SAT result for v5, an UNSAT result for the whole v5 row system, or the
ES308 bound. The final audit collector records this explicitly.

No audit job remains active, no long unit began after10:45, and no source
proof was deleted. The only preserved failures are a harmless AS100MiB
control MemoryError (fixed by streaming) and the deliberate master-change
guard stopping the obsolete v3 full-pass watcher. Neither was a kernel
OOM. They do not invalidate any accepted row proof or individually checked
context; the incremental carry step separately verified those bindings.
