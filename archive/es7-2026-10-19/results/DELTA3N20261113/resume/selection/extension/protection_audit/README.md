# Cup/forced protection audit — COMPLETE

**PROVED:** the stated protection predicates and mixed-obstruction
projection are sound, using the already reviewed compact geometric base.
**COMPUTED:** every new clause and map entry in both supplied CNFs passes
independent streamed reconstruction, native regeneration and exact controls.
**No new finite-size theorem or certificate is claimed.**

## Statement

The reviewed sources are `cup_terminal_general.cpp` and
`forced_terminal_general.cpp`. The checked instances are cup n7/m15
(`n7m15-cup.cnf`) and forced n7/m13 (`n7m13-forced.cnf`), including their
maps. No geometric premise or fixed signs were added to the inherited base.

The formulas express nonexistence of their specific protected weak Deltas.
They do not express exact uniform-envelope nonexistence. A future accepted
UNSAT certificate would apply to its exact ambient size: **no monotonicity
in ambient size has been proved**. The subset and exact-augmentation audit
packets remain frozen, and the separate m15 realization audit was not repeated.

## Model and soundness

End4, support ANDs, Covered ORs and uncovered cap-triple flags are exact.
The cup support cache reuses only identical conjunctions. Shared endpoints,
empty End4 ORs and the direct identical-pair support have the correct signs.
The forced predicate is independently interpreted by direct integer line
differences at the extreme endpoints.

The bad-containment family contains **both uncovered cap triples and old
four-caps**. At size four its one-way row uses all four bad-triple children
and the exact Cap4 term; larger sets use five deletion children. Descent
proves every asserted flag has a genuine obstruction. Canonical exact
containment satisfies every row because a witness of size at most four
misses one of five deleted vertices. Target containment retains the reviewed
n-child recurrence. All failure rows of sizes 0 through m-n+2 are present.

The independent projection and line-domination proofs, the required
old-cap correction, and the limits of the claims are in
[VERIFY_PROTECTION.md](VERIFY_PROTECTION.md). The accepted
[generic base audit](../audit/VERIFY_EXTENSION.md) is an explicit dependency.
The separate [317-case predicate audit](../envelope/cup_dominance/comparison/prototype_check/README.md)
is cited as inherited support evidence, not as this subtrack's computation.

## Method

[tools/check.py](tools/check.py) imports no parent or earlier checker.
It reconstructs the full map and streams all new clauses in order, comparing
every line and both EOFs. The geometric prefixes are compared byte-for-byte
with existing generic inputs. Exact real controls compute caps, convexity,
protection and canonical containment independently using Python integers
and rational arithmetic. No floating-point optimizer is used.

Frozen copies of both parent sources were separately compiled. They
regenerated both supplied CNFs and maps byte-for-byte. Generated small
control formulas also pass independent row/map checks. Rebuilt CNFs/maps
and binaries remain in the assigned scratch directory.

## Results

| Instance | Variables | Geometry clauses | New clauses | Total clauses |
|---|---:|---:|---:|---:|
| cup n7/m15 | 69,673 | 79,326 | 114,554 | **193,880** |
| forced n7/m13 | 18,563 | 32,461 | 35,618 | **68,079** |

The cup instance has 3,380 support flags, 442 exact cache reuses, 105 End4
pairs and 27 empty End4 ORs. The forced instance has 2,585 support flags,
78 End4 pairs and 23 empty End4 ORs. Detailed map/phase counts and hashes
are in [cup15.json](data/cup15.json) and [forced13.json](data/forced13.json).
There are no fixed-sign units in either supplied instance.

## Controls

- **Old four-cap retained:** both separated four-point blocks are caps,
  all 48 mixed triples are cups, and there is no five-cap or five-gon.
  The specified n7 A={0,1,2,3} and n5 A={0,1,2,3,4} hit all targets and
  have protected cap triples, but contain the old four-cap. In the actual
  n5 CNFs, deleting the A4 Cap4 term or the fifth A5 child rejects the
  canonical real assignment. Both encoders correctly retain those terms.
- **Two-support h=5:** A={0,3,6} is an ordinary weak Delta with exact
  uniform margin 11/4 from the half-weight combination of two ambient
  lines. No single ambient line dominates its terminal line. Both predicates
  correctly keep Covered(3,6)=false and Bad(0,3,6)=true.
- Fourteen generated formulas pass complete new-row/map checks; nine
  canonical real assignments, including the primary forced13 control,
  satisfy every non-failure row. False failure rows correctly correspond
  to working selectors in these controls.
- 1,020 exact AND/OR truth assignments, 786 mixed-witness covers, eight
  boundary formulas with required empty clauses and six rejected domain
  inputs all pass. Exact failed mutations and commands are preserved.

See [semantics.json](data/semantics.json),
[native-controls.json](data/native-controls.json),
[cup-blocks5.json](data/cup-blocks5.json) and
[forced-blocks5.json](data/forced-blocks5.json).

## Files and hashes

- [VERIFY_PROTECTION.md](VERIFY_PROTECTION.md): independent written proof.
- [tools/check.py](tools/check.py), [tools/run_controls.py](tools/run_controls.py): audit tools.
- `data/source/`: frozen reviewed sources and inherited documentation.
- [data/commands.jsonl](data/commands.jsonl), `data/*.time`, `data/*.stdout`,
  `data/*.stderr`: bounded commands, outputs, resources and rejection cases.
- [data/external-manifest.json](data/external-manifest.json): streamed hashes
  of supplied/rebuilt files and binaries; [SHA256SUMS](SHA256SUMS): local packet.

| Artifact | SHA-256 |
|---|---|
| Cup n7/m15 CNF | `c5cb343fd310870af75c72214d6356bec98e2536299dbf3443dbb7883d654a0c` |
| Cup map | `336574fbd917fc523f5f09131572b52ec908fd728dca76384422b80720908dbd` |
| Forced n7/m13 CNF | `aa7354802728e9eb465a27cb345b7ef75de8a5f1da5b5a586cb7e113b955acc0` |
| Forced map | `673378d6691af93c42c28ca2b22c55553543e06d7a8ae8a7880accfd2dd5bee7` |

Scratch: `/home/jay/research/data/delta3-codex-20261113/extension/protection-audit/`.

## What remains and resources

This formula audit is complete. The parent forced13 preflight is preserved
as **UNKNOWN**, and cup15 remains separate solver work. Neither is rounded
up to a finite theorem. No cup/forced LRAT was independently replayed.
The newly authorized [exact m13 replay](../exact_audit/replay13/README.md)
completed in its separate reserved slot, which was then released; that
certificate belongs to the terminal-safe formula, not either protection
formula here. Future protection certificates must match the reviewed CNF
hashes and receive coordinated checking resources.

All research checks used one CPU, AS300 MiB, wall20/CPU19 seconds, affinity
5 and nice 10; compilation used AS500 MiB, wall20/CPU18. Primary cup/forced
checks took 0.38/0.19 seconds and peaked at 41,992/38,252 KiB RSS.
The complete native-control driver took 0.57 seconds; compilation peaked
at 159,980 KiB RSS. All ran sequentially. No timeout, OOM, swap or unexpected
control failure occurred. Both compilers emitted only the retained inherited
warning about the unused renamed compact main; parent sources were not edited.

No long subtrack job remains running or queued. Writes stayed in the two
assigned directories; no git, installation, deletion, external action or
shared-record edit was performed.

## Resume

Results and reconstructed paths refuse overwriting. For a fresh replay,
choose a new tag and fresh scratch filenames; first check resources.
The recorded commands provide exact reproduction. A standalone primary
check from the repository root uses this pattern:

```sh
audit_record=cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/protection_audit
audit_scratch=/home/jay/research/data/delta3-codex-20261113/extension
bash .claude/skills/es-research/scripts/cpu_free.sh esr,nov13c -v
timeout -k 1 20s prlimit --as=314572800 --cpu=19 taskset -c 5 nice -n 10 \
  python3 -B "$audit_record/tools/check.py" rows --variant forced --m 13 --n 7 \
  --cnf "$audit_scratch/n7m13-forced.cnf" \
  --baseline "$audit_scratch/terminal7-a/m13/input.cnf" \
  --fixture first13 --tag forced13-recheck
```

Use variant cup, m15 and the corresponding cup/base paths for that primary
instance. `semantics --tag NEW_TAG` replays the two required geometric
controls. The native-control driver has its own retained full command list.
