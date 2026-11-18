# Low-split consequences and geometric partial lemmas

**FROZEN: PROVED universal T6 by the written finite/capacity chain,
low-cut corollaries and a geometric partial lemma; COMPUTED exact controls.**
Started14 November2026 at07:37KST; the exact freeze time is in `FREEZE.json`,
before08:20. Only this directory was written. The earlier
`extension/structure2/` packet remains read-only.

## Statement

The audited finite chain establishes T6(L) through left size11 and T7(L)
through left size15. The subsequently checked geometric Capacity11 now
completes **universal T6**. Capacity16 is checked too. The parent left16
certificate is accepted and its instance audit passes; the final fresh
independent proof-closure receipt is still pending in this snapshot.
The failed first capacity attempt and separate successful retry remain
distinguished, as does the interrupted first independent left16 wrapper.

Universal T6 implies terminal-safe selection for every admissible n6 low
join with at least two left points. The singleton-left branch with right
cup maximum4 still needs a selector on the right block. Minimality, or
an exact smaller-size theorem, supplies that premise when available.
There is no unconditional all-low-join claim.

Two bounded corollaries needed no capacity check: every terminal n6
counterexample of size12, and every terminal n7 counterexample of size14,
has no low cut. Separately, Option1 of T_n is proved whenever deleting
the rightmost point of L removes every (n-1)-cup. This permits long cups
in L and applies for all n>=5.

The additional [all-cap proof](all_cap.md) justifies the fourth full14
cut family, including both singleton directions. It gives all-size n6
all-cap positivity and n7 all-cap positivity through full16 using the
already closed bounded T7 range. Inside a four-cap-free set, a separate
[written theorem](internal_cuts.md) proves Option1 of T_n for any of the
four uniform cut patterns, for all n>=5.

## Model and soundness

All geometry is real, in general position, with distinct x coordinates.
T_n is the established two-option cup/endpoint predicate. The written
[consequence chain](CONSEQUENCES.md) separates finite projection and
certificate evidence, geometric capacity, low-join transfer, and the
critical singleton induction. The [geometric lemma](ROOTED_LEMMA.md)
contains its own proof and states the unclosed unrestricted step.

## Method

This pass read the independent audit packets and retained receipts,
checked the deductions on paper, and ran four short exact control jobs.
It did not replay a certificate or compile Lean. Sources and their
snapshot hashes are recorded in `data/source_snapshot.json`; their
verification status is in [DEPENDENCIES.md](DEPENDENCIES.md).
The whole T6 chain combines written proofs, finite certificates and
Lean-checked capacity; it is not entirely formalized in Lean.

## Results

| Result | Scope at freeze |
|---|---|
| Universal T6 | Closed by independent finite audits and checked capacity11 |
| Bounded T7 | Independently closed through left15, including fresh73.805s left15 replay |
| Universal T7 | Parent certificate and instance audit pass; independent post-hash proof closure pending |
| Low-cut consequences | Non-singleton-left positivity and precisely conditional singleton reduction |
| Rightmost-point lemma | Written Option1 proof for n>=5; unrestricted T_n is not proved geometrically |
| All-cap ambient cuts | Written proof, parent review and68 independent positive controls; full14 exclusion justified |
| Four cut patterns inside L | Written Option1 proof under no-four-cap/no-n-gon, for all n>=5 |

## Controls

All20 named controls for n5,n6,n7,n8 pass. The bounded n5 grid finishes
all19,609 inputs and checks all432 eligible sets, including202 in T5's
no-five-gon domain. The remaining230 test the stronger geometric lemma,
which does not require the no-n-gon hypothesis. [CONTROLS.md](CONTROLS.md)
gives exact scope, counts, resources and the first-vertex exception.
The all-cap theorem has24 further fixtures and68 successful prescribed
selectors, independently replayed by the parent in3.069s.

## Files and hashes

`SHA256SUMS` pins every file of this packet except itself; `FREEZE.json`
records the freeze and mechanical validation. The controls' source hashes
are also embedded in each output. A small byte-identical successful
capacity receipt is retained here. No large proof, CNF, frozen manifest
or shared record was modified.

## What remains

The assigned paper pass is complete. The parent owns the pending fresh
independent left16 replay and separate full14 searches. The purely
geometric critical-size16 exploration yielded the restrictions in
[critical16.md](critical16.md), but its compatible-prefix-selector
candidate remains explicitly unproved. Evidence is not promoted to proof.

All own short jobs have ended. No unit, solver, compiler, or reservation
remains active; the one-CPU/AS150MiB short-check allowance is released.
This record makes no novelty, ordinary weak-Delta failure, or ES-bound claim.

## Resume

Read `CONSEQUENCES.md`, then `DEPENDENCIES.md`, before using a corollary.
`data/commands.txt` preserves the exact control commands. Any replay must
use a new output location and current resource coordination; the drivers
refuse to overwrite outputs. Later external successes should be recorded
in a new append-only packet rather than changing this frozen snapshot.
