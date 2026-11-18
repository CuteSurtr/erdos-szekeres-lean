# Exact containment augmentation — formula audit complete

**PROVED:** adding the reverse implications preserves the reviewed
orientation projection and admits the canonical flags of every real
counterexample. **COMPUTED:** every added row and map entry matches
independent reconstruction; the original CNF body is byte-for-byte intact.
**Certificate replay remains pending.** No new m13 existence bound is claimed.

## Statement

Reviewed `augment_exact.py` and `n7m13-exact.cnf` against the unconditioned
`terminal7-a/m13/input.cnf` and `.map`. There are no new variables, no extra
geometric premises and no fixed signs. The previously accepted
[generic base audit](../audit/VERIFY_EXTENSION.md) remains an explicit
dependency. Its full geometric review and the separate m15 model/coordinate
audit were not duplicated. The earlier fixed-23 subset audit is frozen.

## Model and soundness

For witnesses of size k, an internal containment flag means that its set
contains a true leaf witness. The chosen k+1 deletion children cover every
k-element witness. The original clauses say parent implies some child;
the new clauses say each child implies parent. Together they give exact
OR equivalence, hence canonical exact containment by induction.

Any original model can be repaired to those canonical flags without
changing its geometry or losing any originally true containment flag.
All positive selection-failure rows remain true, the old containment rows
hold by the cover argument, and every other base row is unchanged. This
preserves the projection while removing some noncanonical auxiliary
assignments. [VERIFY_EXACT.md](VERIFY_EXACT.md) contains the full proof,
source review, implementation checks and precise claim boundary.

## Method

Independent standard-library Python reconstructs all map IDs, kinds and
masks; the forward containment and selection-failure interfaces; and every
new clause. It checks every original body byte and rebuilds the complete
augmented CNF independently. It neither imports nor executes the parent
augmenter or any previous checker. Inputs and source were hashed before
and after the structural audit with stable results.

## Results

| Item | Independently checked count |
|---|---:|
| Variables/map entries | 15,822 |
| Original clauses | 59,815 |
| Bad-containment parents | 6,721 |
| Added bad-family reverse clauses | 26,884 |
| Target-containment parents | 4,096 |
| Added target-family reverse clauses | 28,672 |
| All added clauses | **55,556** |
| Augmented clauses | **115,371** |
| Old forward containment rows | 10,817 |
| Positive selection-failure rows | 7,099 |

Every parent has the intended four or seven distinct children; every child
has a smaller ID and the correct subset/leaf meaning. No added row is
duplicated. Every possible witness was checked against every parent's
cover: 182,182 bad-family and 217,932 target-family cases.
The original 1,167,995-byte body is unchanged, and the independently rebuilt
whole CNF and map are byte-identical to the supplied artifacts.

## Controls

Two independent real 13-point integer fixtures satisfy all 55,556 added
clauses and every non-failure base clause. Their respective 87 and 345
false selection-failure rows are expected because these fixtures admit
valid selections. They are geometric controls, not SAT counterexamples.

The five-point bad lattice was exhaustively checked on 1,024 leaf patterns
and all internal assignments (65,536 cases). The actual n7 target width
was tested on an eight-point lattice for 89 deterministic leaf patterns
and all internal assignments (45,568 cases). Every old model repairs
monotonically to its unique exact extension. Missing/duplicate rows,
wrong direction/polarity/parent and a wrong map mask are rejected; too-short
deletion covers have explicit uncovered witnesses. All controls passed.

## Files and hashes

- [tools/check_exact.py](tools/check_exact.py): independent implementation.
- [data/structure.json](data/structure.json), [data/controls.json](data/controls.json): full results.
- [data/inputs-before.json](data/inputs-before.json) and
  [data/inputs-after.json](data/inputs-after.json): input/source hashes.
- `data/source/`: frozen reviewed source and inherited audit snapshots.
- `data/*.time`, `data/*.stdout`, `data/*.stderr`: commands, outputs and limits.
- [SHA256SUMS](SHA256SUMS): local packet manifest.

| Artifact | SHA-256 |
|---|---|
| Original CNF | `8101afdcee113a7674a4b09fb1fcb112d07038ca81bba2ed013e1b9c805f8daf` |
| Variable map | `e1881e1b8b8807d7954c2da807de4c446cd48cb0940914527f75e5a6f393e9d4` |
| Augmented / independently rebuilt CNF | `3ec4b75d9076b6f257fed83f3cbb17b8372a43f53f1c0fc8d30730e4c5d35b87` |
| Parent augmenter | `6ba217c01a3341b0f2d501c97688643b0a247ba40b22256324f7fa6762d08a24` |

Scratch: `/home/jay/research/data/delta3-codex-20261113/extension/exact-audit/`.
Its `independently-rebuilt.cnf` and `.map` preserve the reconstruction.

## What remains and resource use

The formula audit is complete. The parent's `nov13c-vfy-delta6-finite13`
solve is still in progress, writing to `finite13-b/`; its growing binary
LRAT is not a certificate. Independent replay awaits a complete retained
proof and coordinated resources. The present authorization is only AS300
MiB, one CPU and <=20 seconds per invocation; no long verifier was launched.
Acceptance must be cake_lpr's exact `s VERIFIED UNSAT` line. No new SAT,
UNSAT or finite-size existence result follows from this row audit alone.

Structure: 0.42 seconds, 80,664 KiB RSS. Controls: 0.38 seconds, 80,140 KiB
RSS. Both used AS300 MiB, CPU19, wall20, CPU affinity 5 and nice 10, sequentially.
No compilation, timeout, OOM or unexpected failure occurred. The subtrack
has no running or queued job. All writes stayed in the two assigned
directories; no git, installation, deletion or external action occurred.

## Resume

The checker deliberately refuses to overwrite result files. The two exact
commands are preserved in the corresponding time logs. For a repeat, first
retain the existing receipts and use a new authorized output directory or
adapt its output-path constants in a separately saved copy. The bounded
invocation pattern, from the repository root, is:

```sh
audit_record=cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/exact_audit
bash .claude/skills/es-research/scripts/cpu_free.sh esr,nov13c -v
timeout -k 1 20s prlimit --as=314572800 --cpu=19 taskset -c 5 nice -n 10 \
  python3 -B "$audit_record/tools/check_exact.py" structure
timeout -k 1 20s prlimit --as=314572800 --cpu=19 taskset -c 5 nice -n 10 \
  python3 -B "$audit_record/tools/check_exact.py" controls
```

For the pending LRAT, use [REPLAY_HANDOFF.md](REPLAY_HANDOFF.md); do not
treat the currently growing proof or a solver exit status as acceptance.
