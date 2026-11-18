# Delta research checkpoint — 14 November 2026

Owner requested work through **08:40 KST**. Search and verification jobs
have finished. Final scope review and shutdown checks completed at08:40.
This pass began at 04:45.
The general Delta conjecture remains open and no ES bound changes here.
[RESULTS.md](RESULTS.md) states the mathematical findings and their scope.

## Main results

| Result | Evidence and scope |
|---|---|
| The smallest n=6 terminal-safe obstruction has exactly 12 points | **PROVED** minimum deduction using independently audited **CERTIFIED** lower bounds. The 12-point real obstruction itself is fully **Lean-checked**, with fresh parent replay; minimality is not fully Lean-formalized. |
| All admissible n=5 sets have a terminal-safe selector | **CERTIFIED** finite cases and independently reviewed written coverage/capacity chain. |
| The n=7 terminal minimum is14 or15 | Independent coverage through 13 and a fully **Lean-checked** 15-point real obstruction. All 14-point searches in this pass ended **UNKNOWN**. |
| Universal T6(L) and T7(L) | **PROVED** written composition: independent encoder audits, fresh **CERTIFIED** finite proofs through left11/16, and **Lean-checked** geometric capacity bounds. Not an end-to-end Lean selector theorem. |
| Two further geometric lemmas | **PROVED**, written: an explicit all-cap-split selector, and a rooted T_n construction when deleting the rightmost point removes every long cup. Independent exact controls supplement the arguments. |
| The fixed forced16 abstract model is nonrealizable | **PROVED**, written exact algebra with independent worker and parent replay. Its finite product contradiction additionally passed a fresh 338-module **Lean** replay. The real-coordinate bridge remains outside Lean. |
| A real 15-point example defeats cup-support selection | **CERTIFIED**, independently audited. It still has 7078 ordinary weak Deltas and uniform witnesses, so it does not refute general Delta or uniform existence. |

Terminal safety is a stronger sufficient protection rule. Its failure must
not be described as failure of ordinary weak Delta. The exact real12 and
real15 examples both retain ordinary weak and uniform selectors.

## Evidence map

- Exact n6 minimum: [terminal12](terminal12/README.md),
  [independent lower-bound/geometry audit](terminal12_audit/VERIFY_TERMINAL12.md),
  [fresh full real Lean replay](lean_terminal12_parent/README.md), and
  [an explicit uniform witness](terminal12/uniform/README.md).
- Positive n5 case: [terminal5_audit](terminal5_audit/README.md).
- n7 bounds: [terminal15](terminal15/README.md),
  [independent through 13 replay](exact_audit/replay13/README.md), and
  [fresh full real15 Lean replay](lean_real_parent/README.md).
- Universal left lemmas: [the complete T6/T7 chain](low_split/CLOSURE.md),
  [checked capacity11/16](low_split/capacity_checks/README.md), and
  [clean independent original left16 replay](low_split_audit/left16_replay/VERIFY_LEFT16.md).
- New written lemmas: [all-cap](low_split/consequences/all_cap.md),
  [rooted T_n](low_split/consequences/ROOTED_LEMMA.md), and
  [independent all-cap/formula review](fourcuts14_audit/VERIFY_FOURCUTS14.md).
- Forced16: [written real nonrealizability proof](protection_models/forced16_realization/VERIFY_FORCED16.md),
  [separate parent symbolic/integer checker](protection_models/forced16_parent/README.md), and
  [fresh finite-certificate Lean replay](protection_models/forced16_instance_parent/README.md).
- Real cup-support counterexample: [protection_models](protection_models/README.md)
  and [independent exact metric audit](protection_models/cup15_uniform/README.md).

The complete T6/T7 chain implies that a cardinality-minimal n6/n7 terminal
counterexample has none of the high, low, all-cup or all-cap cuts. Every
admissible all-cap join at those parameters is directly positive. For low
joins, the singleton-left critical case still requires a selector in the
right block: universal T_n alone is not an unconditional all-low-joins
theorem. The closure record makes this distinction explicit.

The rooted lemma applies to every n>=5 and does not need a no-n-gon
premise: no-four-cap plus absence of an(n-1)-cup after deleting the
rightmost point yields Option1 of T_n. It is a partial geometric theorem,
separate from the finite T6/T7 closure.
Its [independent parent controls](low_split/rooted_parent/README.md)
pass 3360 eligible cases, including 400 with an n-gon; the written proof
remains the universal evidence.

## Checks completed and questions left open

The last original left16 proof passed clean independent replay at 08:17:29
with stable pre/post hashes and exact `s VERIFIED UNSAT`. A prior accepted
checker line followed by a telemetry-wrapper failure is retained, and is
not used in place of that clean retry. Both redundant augmented left16
searches were cleanly stopped after original certification and archived.

The final four-cut14 search returned UNKNOWN after 720.110 solver seconds.
Its complete 48-row projection audit passed independently, but the run
provides no 14-point theorem. Its partial trace and verified compressed
archive are retained. Earlier generic, high-cut, three-cut and no-six-cup
searches likewise leave the full14-point problem open.

The forced16 Lean replay passed 338 modules and all 354 exact axiom lists.
The independent parent transcription matches 560 triples, 560 signs and
all 387 weighted rows. This checks the finite algebraic certificate and
conditional product contradiction. The actual-coordinate-to-product
bridge and a Mathlib real adapter are not yet checked in Lean.

General weak D(5,7), weak D(5,8), and universal uniform selection remain
open. Fixed examples, stronger-rule failures and excluded nonreal models
do not settle these questions. No new ES bound or novelty-priority claim
is made. Nothing in this pass has been refereed, published or committed.

Earlier completed components remain available: the
[weighted-envelope Lean lemmas](lean/FINAL.md),
[exact metric witness audit](envelope/README.md), and
[2797674-subset replay](subset_audit/README.md).

## Reproduction and resources

The numerical records keep commands, checker outputs and SHA-256 values
beside each result. Large inputs/proofs remain under
`/home/jay/research/data/delta3-codex-20261113/extension/`; no large proof
directory was deleted. Only cake_lpr's exact acceptance line certifies
an LRAT proof. UNKNOWN and cleanly stopped checks remain labelled.

[RESOURCES.md](RESOURCES.md) records allocations, zero-swap observations,
file-cache watermark incidents and clean development stops. No owner cap
was raised. The verifier allocation stayed within 6000 MiB; long work used
bounded `nov13c-vfy-*` user units. Source packets frozen by workers were
left unchanged; later closure statements live in separate parent records.

The branch remains `es7-night-2026-11-01`. There was no commit, push,
branch change, install, external message or root README/math edit.
[NEXT_STEPS.md](NEXT_STEPS.md) gives concrete remaining work.
The [final integrity manifest](data/final-manifest.json) pins the selected
integration files and receipts; it is an integrity record, not a new proof.
