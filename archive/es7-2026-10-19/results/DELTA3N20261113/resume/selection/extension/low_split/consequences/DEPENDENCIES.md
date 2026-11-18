# Premises and their evidence status

This file records source statements read during the consequence pass.
It is not a new solver run, independent proof replay, or Lean compilation.
The snapshot time and source hashes will be pinned at freeze.

| Premise | Status read through 08:14 KST, 14 November 2026 | Role |
|---|---|---|
| Exact geometric classification and arbitrary-R transfer | Written proof; independent projection/geometry audit PASS | Converts full selectors to T_n and transfers T_n back to low joins |
| Terminal n6 through11 | Independently closed, including fresh generic10/11 replays | Supplies T6 at left sizes0–9 via the standard two-cup join |
| Direct T6 left10 and left11 | Independently rebuilt, fresh cake acceptance, audit frozen PASS | Completes T6 through left11 |
| Capacity11: no four-cap/no six-gon implies at most11 points | Parent kernel check PASS, current source hash matches, two standard-axiom reports; imported bridge checked too | Completes universal T6 with the finite audits |
| Terminal n7 through13 | Explicit audited smaller-size chain and exact13 replay | Supplies T7 at left sizes0–10 via the standard three-cup join |
| T7 left11–14 | Independent row/projection audit and fresh certificate replays PASS | Completes T7 through left14 |
| T7 left15 | Independent full row/map audit, exact control and fresh cake1400 replay PASS (73.805s) | Completes T7 through left15 |
| T7 left16 | Parent CERTIFIED with stable hashes; full instance audit PASS; fresh independent proof closure still pending after a telemetry race | Final independent-review obligation for universal T7 |
| Capacity16: no four-cap/no seven-gon implies at most16 points | Parent kernel check PASS, current source hash matches, three standard-axiom reports including the real bridge | Closes the left-size range after exact16 is established |

The n6 update was confirmed by reading
[VERIFY_LOW6.md](../../low_split_audit/n6/VERIFY_LOW6.md), whose frozen
packet records fresh accepted left10/11 proofs and 12,288 full-selector
controls. The parent separately confirmed its completion during this pass.
The finite T6 range is no longer marked as audit-pending here.

The terminal n6 dependency and the actual minimum12 obstruction are in
[VERIFY_TERMINAL12.md](../../terminal12_audit/VERIFY_TERMINAL12.md).
Its minimum-size statement concerns terminal-safe selection, not ordinary
weak Delta or uniform-envelope selection.

The T7 smaller-range sources are
[VERIFY_LOW_SPLIT.md](../../low_split_audit/VERIFY_LOW_SPLIT.md) and
[the independent replay packet](../../low_split_audit/replay/README.md).
They explicitly cover all left sizes through14. A size14 result alone
would not cover smaller sizes by ambient monotonicity.

The subsequently completed [left15 audit](../../low_split_audit/left15/VERIFY_LEFT15.md)
was read directly during this pass. It records all63,368 map entries and
447,615 clauses matching independent reconstruction, an exact canonical
control, and a fresh accepted replay in73.805s. The input CNF hash is
`793063f5c7c5208c16ce038c63659878adee4eb049546d775d65c5a18ed60418`.
Its explicit lower chain extends bounded T7 coverage through15. No left16
or universal-left conclusion is inferred from this receipt.

The capacity sources are [Capacity11.lean](../Capacity11.lean),
[Capacity16.lean](../Capacity16.lean), and the
[read-only Capacity16 review](../capacity_review/README.md).
The actual vendor theorem has threshold binomial(t+2,2)+2 and conclusion
four-cap or (t+3)-gon. Hence t=3 gives12/6 and t=4 gives17/7. Source review
and arithmetic specialization are distinct from successful kernel and
axiom checks. No compile is run by this consequence track.

At 07:53 the retained
[first capacity receipt](../capacity_checks/attempt-rss3000/result.json)
reported FAIL because the Capacity16 compile was terminated by its
3000MiB RSS guard after2.598s (exit -15). Its recorded peak RSS is
3,079,756KiB, swap0, and its axiom-report map is empty. This is a stopped
verification attempt, not a mathematical refutation or a completed kernel
check. Capacity11, which imports that bridge, is not established by the
stopped run. This failure remains retained in its original record and is
not relabeled by the subsequent success.

At 07:54:09 the parent reported a successful separate primary-b run. This
pass read its result directly and retains a byte-identical small
[receipt copy](data/capacity_pass_receipt.json), SHA-256
`bac50eb753b6cda69956a1cd116031ebdf2e026148234d8b3ff11a4c08f8829f`.
The original is
`/home/jay/research/data/delta3-codex-20261113/extension/capacity-lean/primary-b/result.json`;
the parent is archiving it under `low_split/capacity_checks/pass/`.
Both Lean commands exit0 with no stop reason. Capacity16 takes1.548s,
Capacity11 takes1.342s; peak RSS3,111,920KiB and swap0 are recorded under
the parent-authorized4500MiB RSS guard. All five axiom-report lists are
exactly `propext`, `Classical.choice`, `Quot.sound`.

The source hashes were compared with the actual current files:

* Capacity16: `8d5ced5ab84da9ba9347bc4fd1f99952dfa876302c35a712e9e8fec284a003d3`.
* Capacity11: `d34ad0ecbcba8a507e71c43b2d54e9a887e9362f1f9d265ae7fa8efcb9296156`.

The checked statements concern actual-real `Configuration n`, excluding
`HasCap 4` and `HasConvexNGon 6` or7, respectively. The generic-q list
boundary-to-real-polygon bridge is included among the checked declarations.
Thus capacity is no longer pending in this snapshot. Universal T6 is
closed by the finite audits plus this geometric capacity. The complete
written/certificate chain itself has not been formalized entirely in Lean.
Universal T7's exact left16 input now has parent acceptance and an
independent instance audit; final fresh independent proof closure remains
pending in this snapshot, as detailed next.

## Left16 verification updates

The parent reported solver UNSAT after2648.668s on the original compact16
instance. The initial cake550 run exhausted its heap. The separate parent
heap2800 replay then printed exactly `s VERIFIED UNSAT` after205.49s,
with stable CNF/proof hashes. This is parent CERTIFIED evidence; it is
not relabeled as our own replay. The independently rebuilt base instance
is in the separate `low_split_audit/left16_longcup/` packet.

The first independent checker also printed acceptance, but its wrapper
hit PermissionError while reading `/proc/<exiting child>/io` and did not
finish the post-hash receipt. The owner explicitly withheld final closure
and assigned a corrected fresh replay. The
[independent replay record](../../low_split_audit/left16_replay/README.md)
still says IN PROGRESS at the last read. A checker stdout line without
that intended complete receipt is not silently promoted to the finished
independent review. The parent primary certificate remains valid.

The raw proof is reported as4,724,116,807 bytes, SHA-256
`247f64c822609e878be490e059fb7e0c96e5e71fde0e265de74c7be36cd8dd42`.
This consequence track has not read, rehashed or replayed that large
proof. All-size T7 corollaries are prepared but retain the independent
closure qualification until a successful new receipt is read.

At08:16 a separate
[post-hash recovery receipt](../../low_split_audit/left16_replay/data/recovery/result.json)
was read. It is PASS/CERTIFIED: the earlier fresh independent stdout is
exactly `s VERIFIED UNSAT`, and the recovered post-hashes agree with the
original pre-hashes for the CNF, raw/compressed proof and checker. It
explicitly retains the wrapper FAIL, does not claim to know the checker
exit status, and states that no checker was rerun during recovery. This
supplies recovered independent acceptance evidence, not a fabricated
successful original wrapper or a second fresh checker run. The owner had
requested a further fresh replay; its final review status is kept separate
until its receipt/owning record is available.

No unaccepted original checker run is silently replaced by a later
acceptance. In particular the original compact14 heap128 exhaustion and
the later accepted replay remain separate in their owning records.
The unrelated cup15/forced16 SAT reports are not premises of this chain;
their realization status does not affect these written implications.
