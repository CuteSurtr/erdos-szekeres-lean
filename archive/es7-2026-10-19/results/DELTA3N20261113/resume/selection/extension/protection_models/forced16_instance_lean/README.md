# Forced16 finite product certificate — PROVED in Lean

The fixed system of **387 strict product inequalities in 560 positive variables is
infeasible**. Lean also checks all positive integer weights, all 560 weighted
exponent cancellations, and every row's finite GP sign/factor binding to the frozen
sign table. This packet does **not** yet prove that real coordinates realizing that
table produce those inequalities. The separate written real nonrealizability proof
remains in `../forced16_realization/VERIFY_FORCED16.md`.

## Statement

In namespace `Delta3.Forced16Instance`, the main theorem is
`no_positive_product_assignment` in `F16IPairs.lean`. For an ordered commutative
ring with the stated `Lean.Grind`/`Std` instances, any function `x : Nat → K` satisfying

```
∀ j ∈ vars, 0 < x j
∀ r ∈ rows, x r.small1 * x r.small2 < x r.large1 * x r.large2
```

implies `False`. The hypotheses contain precisely the fixed finite product system;
they do not assert any relation between `x` and geometric determinants.
`F16IAggregate.lean` supplies the equivalent monomial contradiction and the closed
finite facts. `F16ITable.lean` checks that `triples` is exactly the lexicographic
enumeration of increasing triples from labels 0 through 15, and checks weight sum
**19,282,471,848,322,771**.

## Model and soundness

`F16IData.lean` transcribes the 560 signs and 387 raw five-label rows. Each row has
distinct labels below 16, a permutation of the three GP term slots, and a positive
natural weight. `rowValid` reconstructs the two bracket factors of each GP term
from those labels. It sorts triples, computes permutation parity, includes the
minus sign in term 1, checks the canonical factor indices, and verifies that the
chosen large term has the unique sign. This is a finite Boolean calculation with
explicit definitions, not a geometric realization predicate.

The exponents are defined from the two small and two large factor indices.
`every_exponent_balanced` proves equality of their weighted natural totals for
every variable. The imported frozen algebra proves that a nonempty family of
positive-weight strict monomial inequalities with cancelling exponents is
impossible. The new `monomial_indicator` and `monomial_pair` lemmas identify the
monomials with the two-factor products in the main statement.

## Method and results

**338 modules passed; 354 axiom reports contain only standard axioms.** The 194 row
blocks and 140 column blocks use kernel reduction with `decide +kernel`, not an
external evaluator. Those 334 block theorems depend on no axioms. The final product
theorem uses only `propext`, `Classical.choice`, and `Quot.sound`.
`data/manifest.json` records every theorem's exact axiom list, all source and
compiled-module hashes, receipts, logs, and the two frozen algebra dependencies.

Total successful Lean check time was **180.365 seconds**, maximum process RSS
**766,148 KiB**. Checks used one CPU affinity, `-j1 -M500`, AS3GiB, a 950MiB RSS
guard within the allocated1000MiB slot, no swap, and 18-second per-file deadlines.
The long sequential replay used `nov13c-vfy-delta6-lean`, CPUQuota100%,
MemoryMax1300M, MemorySwapMax0, and a finite runtime. The final three modules were
checked separately after the sequential runner's lexical scan rejected the
ordinary English word “admit” in a comment; that comment was corrected.

## Controls and retained failures

`F16Iprepare_audit.py` independently reconstructs the numerical certificate and
checks two exact integer point controls: 774 GP identities and 6,720 permutation
identities. Each real control satisfies only152 of the387 selected unique-sign
rows. Perturbing the first weight by one breaks cancellation. These Python checks
are controls, not the Lean evidence.

The original 480MiB row probe and a later16-row block at950MiB both clean-stopped;
receipts remain in `work/` and `data/attempt-block16/`. Smaller blocks succeeded
without increasing the allocation. Two bounded probes unintentionally overlapped
for under one second because a terminal call yielded before completion; both
finished without swap or guard, the parent was notified, and all subsequent Lean
checks were strictly sequential. See `data/probe-overlap.txt`.
The initial pair-adapter namespace ambiguity is retained in `work/f16i-pairs-v1.*`;
only its corrected, successful final receipt supports the result.

## Files and hashes

- Input certificate SHA-256:
  `cfe42cec6041709b2ed7ac18ee16b13e57f091239ac19b8e5257aac46d2a326d`.
- Input signs SHA-256:
  `b21664b06887c4019d75023025b1cd80582064a0b06f53698d2a70bc8fc49067`.
- `F16Igenerate.py` produces the transcription, decision blocks, and aggregation.
- `data/generation.json` lists their dependency order and reconstructed raw rows.
- `data/manifest.json` and `FROZEN.json` identify the exact accepted packet.
- `work/*-final.{log,json}` are the accepted per-module receipts; other logs are
  preparation or failure records and are not promoted to finished results.

Earlier algebra, Boolean, finite15, real15, and terminal12 packets were not edited.

## Remaining boundary

The coordinate adapter is unfinished: it must connect actual oriented determinants
to the canonical bracket array, transport the verified sign/parity metadata to
strict signs in the ordered ring, apply the GP identity, and derive the387 product
inequalities. A Mathlib real-number instance/adapter is also not checked here.
Accordingly, this packet alone is **not a Lean theorem that the fixed sixteen-point
sign model is nonrealizable over the reals**. No minimality, selector theorem, or
claim about other orientation models is made. No further Lean work is running;
the1000MiB allocation was explicitly released for parent replay.

## Fresh replay

Keep this packet and its frozen algebra dependency read-only. The parent can set
`F16I_WORK_DIR` and `F16I_RECORD_DIR` to new directories it owns. The replay script
then exports all338 new modules and logs there, verifies frozen source/dependency
hashes, and checks the exact axiom reports. It imports only the two already-frozen
generic algebra modules from their recorded cache.

From the repository root, after allocating the1000MiB slot:

```bash
systemd-run --user --unit=nov13c-vfy-forced16-instance-parent \
  -p CPUQuota=100% -p MemoryMax=1300M -p MemorySwapMax=0 -p RuntimeMaxSec=600 \
  --nice=10 --working-directory=/home/jay/research/lean/erdos-szekeres-lean \
  /usr/bin/env \
  F16I_WORK_DIR=/home/jay/research/data/delta3-codex-20261113/extension/forced16-instance-parent-a/work \
  F16I_RECORD_DIR=/home/jay/research/data/delta3-codex-20261113/extension/forced16-instance-parent-a/data \
  /usr/bin/prlimit --as=157286400:3221225472 --core=0 /usr/bin/taskset -c 4 \
  python3 -B \
  cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/protection_models/forced16_instance_lean/F16Ireplay.py
```

Independent parent collection/review remains outside this frozen packet. Do not
rerun the generator or freezer as part of replay.
