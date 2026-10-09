# Verification records

## Complete residual geometric transfer — 2026-10-09

The main `lake build --wfail` passes with **3,245 jobs**. The
[current full audit](validation/axiom-audit-residual-2026-10-09.txt) covers
**444 named roots**, including 94 added roots for the residual geometry and
Baek prerequisite. Only `propext`, `Classical.choice` and `Quot.sound` occur.
All **63 Python tests** pass with optional solvers and Lean controls enabled.

The separate [residual artifact](../experiments/omission-residual-geometry-2026-10-09/README.md)
checks **39 cycle modules and 24 block/composition modules**, covering every
one of the 1,187 residual rows. Three additional reduction theorems are audited.
`all_geometric_rows` has only actual geometric restrictions as premises;
`feasible_holes` constructs the complete Boolean hole vector and proves its
exact cardinality complement. The population bound and global numerical
conclusion remain conditional on `ExcludesThirtyHoles`.

The artifact manifest verifies all successful prerequisite bindings, generated
source hashes, compiled output hashes and archived source contents. All 63
geometric sources reproduce byte for byte. The scan covers **157 loose Lean
files**, plus the generated archives, with no placeholders or custom axioms.
Git tracks no cache directories or compiled artifacts. The 13 new geometry
modules contain 1,433 lines; 16 separately attributed Apache-2.0 modules supply
the remaining Baek proof dependencies. Earlier immutable artifact records are
preserved.

The [third residual batch](../experiments/omission-residual-progress-2026-10-09-batch3.json)
adds 30 parts and 1,304 leaves, bringing the checked frontier to **360 parts
and 15,131 leaves**. This is a partial arithmetic result, not a root exclusion.

Lean accepts the literal residual cycle and block controls and rejects a
corrupted cyclic order and collapsed compression thresholds. A further control
builds two complete small arithmetic trees with distinct module prefixes and
imports them together. This addresses the exporter's historical module-name
collision; it does not pretend that production certificates were rebuilt under
new imports. See the [updated remaining-work estimate](ES8_REMAINING.md).

## Complete geometric partition — 2026-10-09

The main `lake build --wfail` passes with **3,216 jobs**. The
[current full audit](validation/axiom-audit-partition-2026-10-09.txt) covers
**350 named roots**, including all 73 public theorems in the eight new partition
modules. Only `propext`, `Classical.choice` and `Quot.sound` occur. All **55 Python
tests** pass with the optional solvers and Lean integration controls enabled.
The separate
[composition artifact](../experiments/omission-partition-2026-10-09/README.md)
checks four more theorems against the previously verified balanced certificate.

The complete partition includes actual induced configurations, an exact
disjoint cover, the three-chain argument, and every avoidance and junction
restriction. The resulting `OmissionBalanced.forces_317_of_residual_123` still
has the unproved `Partition.ResidualBound 123` hypothesis. The unconditional
structural conclusion extracts at least 124 residual chart points from any
putative octagon-free set of at least 317 real points. Neither theorem proves
the global bound without the residual population argument.

The validation manifest records the full source inventory, checks the saved
balanced prerequisite bindings and stores the exact standalone axiom output.
The large certificate trees are not rebuilt at this checkpoint; their compiled
objects match the earlier successful check records. Earlier records below
remain historical and are not overwritten.

The scan covers **127 loose maintained Lean files** with no proof placeholders
or custom axioms. Git tracks no caches or compiled outputs. The source bindings
of all 86 balanced geometry checks and their 114 prerequisite inputs match the
previous successful records; the new manifest also records the adapted
upstream source hashes.

## Projective/root transfer — 2026-10-09

The main `lake build --wfail` passes with **3,208 jobs**. The
[saved audit](validation/axiom-audit-projective-2026-10-09.txt) passes for
**277 named roots**, including the eight new projective-transfer theorems.
Only `propext`, `Classical.choice` and `Quot.sound` occur. All **55 Python tests**
pass with the optional solvers and Lean integration controls enabled.

`ErdosSzekeres.Omission.forces_317_of_asymmetric_315` is conditional on
`AsymmetricBound 315`, which remains unproved. Its audit certifies that
conditional statement, not ES(8) ≤ 317. The actual normalization and root-deleted
chart, cap exclusion, polygon pullback and threshold accounting are complete.

The [separate composition artifact](../experiments/omission-projective-transfer-2026-10-09/README.md)
also passes Lean and its axiom check:

```text
'OmissionBalanced.large_avoiding_set_has_chart_cup' depends on axioms: [propext, Classical.choice, Quot.sound]
```

This proves the 194-point structural consequence in the [projective proof map](OMISSION_PROJECTIVE.md).
It uses the previously checked balanced arithmetic and geometry objects;
this checkpoint does not rebuild their large proof trees. Its validation
manifest records source and object hashes and verifies the saved prerequisite
bindings. The source scan covers **118 loose maintained Lean files**, with no
proof placeholders or custom axioms. Git tracks no caches or compiled outputs.
The earlier records below are preserved as historical checkpoints.

## Balanced geometry library — 2026-10-09

The main library now includes twelve modules for attained ranks, exact balanced
state indexing, the actual real-point connection, computed boxes, geometric
cycle soundness and the first literal row. The main `lake build --wfail` passes
with **3,207 jobs**. The [saved audit](validation/axiom-audit-geometry-2026-10-09.txt)
passes for **269 named roots**, including 68 new geometry roots. Every transitive
axiom is among `propext`, `Classical.choice`, and `Quot.sound`; some finite and
structural results are axiom-free. The audit parser now accepts Lean's explicit
axiom-free report while still rejecting missing, duplicate and nonstandard
reports, with tests for each case.

All **55 Python tests** pass in the existing solver environment with the Lean
integration controls enabled. The standard-library-only run passes 39 and
skips 16 optional tests. A new Lean control accepts the source's first cycle and
rejects a deliberately corrupted cyclic order, with the same support. CI runs
that control separately, in addition to the existing arithmetic exporter
controls. A literal-data test verifies that the geometric catalog has exactly
the same 252 profiles in the same order as the archived arithmetic row source.

The [second residual batch](../experiments/omission-residual-progress-2026-10-09-batch2.json)
adds twenty successful part checks (862 leaves), bringing the checkpoint to
**330 parts and 13,827 leaves**. The residual root is still unchecked. The
historical record below is retained rather than overwritten.

The [standalone geometric certificate](../experiments/omission-balanced-geometry-2026-10-09/README.md)
also passed all **86 module checks**: the occupancy prerequisite, 84 row blocks,
and the final assembly. The 85 generated geometry sources reproduce byte for
byte and contain no placeholders or custom axioms. The final two reports are:

```text
'OmissionBalanced.all_geometric_rows' depends on axioms: [propext, Classical.choice, Quot.sound]
'OmissionBalanced.real_configuration_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
```

All 2,685 row supports and demands are equated with the arithmetic catalog
inside Lean. The standalone theorem concludes the actual-point bound 192 under
the explicit balanced avoidance hypotheses. It is not part of the default
269-root audit or a global ES(8) theorem. The [artifact validation manifest](../experiments/omission-balanced-geometry-2026-10-09/validation.json)
records all sources, prerequisite bindings, output hashes and test-log hashes.
The final source scan covers 116 loose Lean files, plus the 900 archived
arithmetic and 85 archived geometry sources; no placeholders, custom axioms or
compiled artifacts occur in those source archives. Git tracks no cache or
compiled build outputs.

## Earlier arithmetic-only checkpoint — 2026-10-09

The [complete balanced artifact](../experiments/omission-balanced-lean-2026-10-09/README.md)
records the successful October 7 build of all 898 parts and the final root,
covering 9,862 leaves. On October 9, every one of its 900 generated Lean sources
was regenerated byte for byte and checked against the archived hashes. The
catalog and root were rechecked, and the new `OmissionBalanced.occupied_card_le`
corollary passed Lean. All three current axiom reports contain only the standard
axioms. This was not a second full-tree rebuild.

The source archive contains no compiled objects and no proof placeholders or
custom axiom declarations. Its complete build reports, source manifest and
fresh axiom output are saved alongside it. The main geometric library is
unchanged; this separate result is not included in its 201-root audit. The main
`lake build --wfail` was rerun successfully (3,194 jobs), and a fresh 201-root
axiom audit exactly matches the saved October 5 output. A scan of all 103 loose
maintained Lean files also finds no placeholders or custom axioms.

The Python suite reports 48 tests: 46 passed and two optional Lean integration
tests skipped. A separate Lean-enabled run passes all seven exporter tests,
including both kinds of leaf, branch composition, resume, source tampering,
and a corrupted-column control that Lean rejects. CI now runs those small
Lean controls; it does not silently claim to check the full large certificate.
The residual tree and the geometric transfer remain unfinished. Its
[partial-build record](../experiments/omission-residual-progress-2026-10-09.json)
records 310 of 3,411 parts checked, including ten fresh successful retries or
completions; no residual root theorem is claimed.

## Historical library checkpoint — 2026-10-05

Proof checkpoint: `0407d69d70b12eae6c66fe8808de464264330984`.
The subsequent cleanup changes documentation, ignore rules and audit-output
recording; it does not change the finished geometric proofs.

## Main library

- `lake build --wfail`: **passed**, 3,194 build jobs (including dependencies).
- `python3 scripts/check_axioms.py`: **passed**, 201 named theorem roots.
- Python suite with the existing optional Z3/HiGHS environment: **41 tests passed**.
  The standard-library-only CI run skips 13 solver-dependent tests.
- Lean successfully resolved all **75 declarations** checked from the paper map
  (74 project-qualified names and Mathlib's `convexHull_mono`).

The [complete, unabridged axiom output](validation/axiom-audit-2026-10-05.txt)
contains these main results:

```text
'ErdosSzekeres.Suk.theorem2016' depends on axioms: [propext, Classical.choice, Quot.sound]
'ErdosSzekeres.HMPT.theorem2020' depends on axioms: [propext, Classical.choice, Quot.sound]
Axiom audit passed for 201 theorems: only standard Lean axioms.
```

`#print axioms` reports transitive axiom dependencies of each named result.
The allowlist is exactly `propext`, `Classical.choice`, and `Quot.sound`.
It excludes `sorryAx`, custom theorem assumptions declared as axioms, and
native-evaluation axioms. This records Lean verification of the stated
propositions; it does not expand them to the unformalized parts of the papers.
See [PAPER_MAP.md](PAPER_MAP.md) for those scope distinctions.

## Placeholder and repository checks

A source scan covered **all 102 tracked `.lean` files**, including finished
Suk/HMPT modules, adapted prerequisites, the audit, and standalone experiments.
There were **zero occurrences** of the tokens `sorry`, `admit`, `sorryAx` and
`native_decide`, and zero lines declaring an `axiom` or `constant`. Thus there
is no `sorry` anywhere in the maintained finished results. Failed local probes
inside the ignored cache are not maintained results and are not included in
this statement. The transitive axiom check independently covers the dependencies
of both completed final theorems.

The Git index contained **zero** files under `.cache/`, `.lake/`, or `.elan/`,
and zero compiled Lean objects, native objects/libraries, trace files or Python
bytecode. `git check-ignore` confirmed that representative toolchain and build
outputs are ignored. The committed generated `.lean` catalog is proof input,
not a compiled build artifact. Third-party licenses and modifications are
identified in [THIRD_PARTY.md](THIRD_PARTY.md).

[Source manifest](validation/source-manifest-2026-10-05.json) records SHA-256
hashes of every maintained Lean source, the toolchain/dependency pins, the audit
script, the audit output and validation logs. Its combined source digest is
`d73423332422742791949c5dc190e90ce7a0a181a62d839c88df9211db3b65cf`.
Logs of the full build and Python run remain in the ignored cache; their hashes
are recorded, while the requested full axiom output is committed above.

To reproduce the main audit, after building:

```sh
python3 scripts/check_axioms.py --output /tmp/erdos-axiom-audit.txt
```

For this Mac's workspace-local toolchain:

```sh
ELAN_HOME="$PWD/.elan" .elan/bin/lake build --wfail
ELAN_HOME="$PWD/.elan" python3 scripts/check_axioms.py \
  --lake "$PWD/.elan/bin/lake" --output /tmp/erdos-axiom-audit.txt
```

## Separate certificate checkpoint

The [chunked catalog and leaf](../experiments/omission-chunked-2026-10-05/README.md)
were checked separately, with both Lean processes exiting zero. Their saved
profiler and axiom output are in the directory's `validation.json`. They are
not part of the default-library build or its 201-root audit. Their conclusions
certify the 2,685 balanced row encodings and a single conditional leaf only.
At that historical checkpoint, both complete omission trees and their geometric
transfer remained unproved in Lean. Certificate work stopped after it was pushed;
the October 9 section above records the subsequent resumed work.
