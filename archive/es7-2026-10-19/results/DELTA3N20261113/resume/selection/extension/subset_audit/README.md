# COMPUTED: minimum terminal obstruction size is 18 within this fixed 23-point set

**Independent bounded audit COMPLETE.** Every one of the **2,797,674**
subsets of sizes 13 through 17 of the fixed `n7-i076` set has a checked
terminal-safe weak Delta. Every required mask occurs exactly once; no
extra, nonpositive, or UNKNOWN row occurs. The existing 18-point obstruction
is an exact coordinate subset and independently has zero terminal-safe
selections. The computation finished **14 November 2026, 05:19 KST**.

## Statement

For each audited W, the supplied A is contained in W, contains no four-cap,
and hits every convex six-subset of W. Every cap triple a<b<c in A has a
four-cap u<v<b<c entirely in W. The ambient 23-point set has strictly
increasing integer x-coordinates, no collinear triple, no five-cap and no
convex seven-subset.

Combining this computation with the **previously certified coverage through
12**, explicitly cited below, every subset of this one 23-point set through
size 17 admits a terminal-safe Delta. The mapped obstruction has size 18.
Thus the minimum obstruction size **within this fixed 23-point set** is 18.
This is not a claim about the global minimum, ordinary weak Delta failure,
or the uniform-envelope selection problem.

## Model and soundness

The independent C++ checker uses signed `__int128`, with coordinate
magnitudes restricted to at most 2^40 before taking any determinant.
Determinants have magnitude at most 2^83, below the signed 128-bit limit.
Convexity is reconstructed by triangle containment on four-subsets: a set
is convex exactly when every four-subset is convex. No convex-hull
algorithm, finder source, solver, or prior checker is imported or executed.

Exact subset-OR propagation completes the forbidden-subset tables.
Terminal support is recomputed **inside each W**, never inherited merely
from the full ambient set. [VERIFY_SUBSETS.md](VERIFY_SUBSETS.md) gives the
soundness argument and dependency boundaries.

## Method

The 145,297,300-byte JSONL was streamed with a strict five-field integer
schema. The nodes field is metadata only. A bitmap scan of all 2^23 masks
verifies exact coverage, independently of input order. The stream,
coordinates, executable, sources and cited evidence were SHA-256 hashed
before and after, with identical hashes and file metadata. The large stream
was neither copied nor loaded as a list.

## Results

| Subset size | Checked rows = binomial(23,size) |
|---|---:|
| 13 | 1,144,066 |
| 14 | 817,190 |
| 15 | 490,314 |
| 16 | 245,157 |
| 17 | 100,947 |
| Total | **2,797,674** |

Ambient geometry: 1,771 nonzero triple determinants, 409 four-caps,
zero five-caps, 1,930 convex six-subsets and zero convex seven-subsets.
Minimum absolute determinant: 151,035,643; maximum: 2,006,444,047,885.
Across witnesses, 866,581 terminal-pair obligations cover all 1,485,088
selected cap triples.

The mapped 18-point obstruction has mask **7339980** and zero-based indices
**[2,3,6,7,8,9,10,11,12,13,14,15,16,17,18,19,21,22]**.
All 262,144 selections were enumerated: 8,149 ordinary weak Deltas, zero
terminal-safe Deltas, and minimum ordinary Delta size five. Its 115
four-caps, 402 hexagons and 219 bad triples agree with the frozen record.
See [data/result.json](data/result.json) and [data/mapping.json](data/mapping.json).

Inherited evidence, explicitly cited:

- Through size 11: [boundary audit, Encoders and coverage](../../boundary/audit/VERIFY_BOUNDARY.md),
  including its small-size argument and [n7 replay](../../boundary/audit/data/replay-n7.json).
- Size 12: [general extension audit, Independent certificate replay](../audit/VERIFY_EXTENSION.md)
  and [n7/m12 replay](../audit/data/replay-n7m12.json).
- Size 18: [terminal obstruction](../../terminal/README.md),
  [certification receipt](../../terminal/data/certification/result.json),
  [accepted cake log](../../terminal/data/certification/cake.log), and
  [retained compressed LRAT](../../terminal/data/certification/proof.lrat.zst).

All three cited acceptance logs contain the exact line `s VERIFIED UNSAT`.
This subtrack inspected and hashed those records; **it did not rerun cake_lpr**.
The new audit and the combined fixed-set minimum are labeled **COMPUTED**.

## Controls

Passed 272 general-position six-point grid permutations, 17,408 exhaustive
subset table/convexity comparisons, 65,280 direct terminal-support comparisons,
and 354,959 independent supporting-edge checks covering **every** ambient
four-, six-, and seven-subset. Large-coordinate and upward/downward parabola
controls check arithmetic, cap orientation and premise rejection.

Ten malformed parser cases, seven coverage/membership mutations and three
semantic defects were rejected internally. Fifteen executable interface
mutations were also rejected; exact inputs, stdout, stderr, commands and
resource logs remain in `data/`. No real audit failure, timeout, OOM or
memory-guard stop occurred. Two initial compile indentation warnings were
corrected before execution; both compile logs remain.

## Files and hashes

- [tools/audit.cpp](tools/audit.cpp): independent verification and controls.
- [tools/run_audit.py](tools/run_audit.py): bounded orchestration, streaming
  hashes, coordinate mapping, input mutations and receipts.
- [data/commands.jsonl](data/commands.jsonl): executed checker commands.
- [data/inputs-before.json](data/inputs-before.json) and
  [data/inputs-after.json](data/inputs-after.json): full external hashes.
- [SHA256SUMS](SHA256SUMS): local packet; the large stream stays in parent scratch.

| Artifact | SHA-256 |
|---|---|
| 23-point input | `f62bd72aa0fef049ddc772b9f649e674b53c36f530e088c28f4bb79ce173fbfe` |
| all13-17.jsonl | `972e8f1139de7f9067a77bccd8941ea0bf70a8be19d0064e2816845170519969` |
| Executed C++ source | `5fdc9ab20612e7cff38d9f8aadb8b5c6820abd11289936fa8cffd8c34a64b9f2` |
| Executed binary | `1b426fecec0505d855736c684a0dd001444ca57090277b813f50105bc50c017e` |

## What remains and resource accounting

This assigned audit is complete; no subtrack job remains running or queued.
No global minimality or Lean formalization was attempted. Only the assigned
repository and scratch directories were written. No git operation,
installation, proof deletion, external action, or root README/math change
was performed.

The launch used `nov13c-vfy-delta6-subset-audit`, CPUQuota100%, affinity CPU 5,
AS300 MiB, MemoryMax500M, MemorySwapMax=0, RuntimeMaxSec=1200, and nice 10.
The main checker also had timeout1100 and CPU1099; controls had timeout20
and CPU19. Compilation had AS500 MiB, timeout20 and CPU18. The actual launch
check reported 11 free CPU slots, 6.93 GB aggregate research anonymous
memory plus swap, and 0.291 GB in the verifier track, with no swap.

Main audit: **1.24 seconds, 13,128 KiB peak RSS**. Complete unit: 1.937 CPU
seconds, **168,394,752 bytes peak cgroup memory** including file cache, zero
swap. Compilation peaked at 148,340 KiB RSS. All remained well below their
allocation. The existing shared guard lifted kernel memory.max and enforced
the requested 500 MiB threshold itself; see [guard log](data/memguard-excerpt.txt).
This subtrack did not raise its allocation. The successful exited unit was
stopped and its reservation released: [unit outcome](data/unit-final.txt),
[stopped state](data/unit-stopped.txt).

## Resume commands

The original driver refuses to overwrite receipts. To repeat the core check,
use fresh output files under the same authorized scratch directory, check
CPU availability and guard status, and run:

```sh
audit_scratch=/home/jay/research/data/delta3-codex-20261113/extension/subset-audit
audit_record=/home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/subset_audit
bash .claude/skills/es-research/scripts/cpu_free.sh esr,nov13c -v
systemctl --user is-active memguard5-20261113.service
timeout -k 1 20s prlimit --as=524288000 --cpu=18 taskset -c 5 \
  g++ -std=c++17 -O2 -Wall -Wextra -Wpedantic "$audit_record/tools/audit.cpp" \
  -o "$audit_scratch/audit-recheck"
systemd-run --user --unit=nov13c-vfy-delta6-subset-audit \
  -p CPUQuota=100% -p MemoryMax=500M -p MemorySwapMax=0 -p RuntimeMaxSec=1200 \
  -p StandardOutput="append:$audit_scratch/recheck.stdout" \
  -p StandardError="append:$audit_scratch/recheck.stderr" --nice=10 \
  --working-directory="$audit_scratch" \
  /usr/bin/prlimit --as=314572800 --cpu=1099 /usr/bin/taskset -c 5 \
  /usr/bin/timeout -k 1 1100 "$audit_scratch/audit-recheck" run \
  "$audit_scratch/../terminal-subsets/input.points" \
  "$audit_scratch/../terminal-subsets/all13-17.jsonl" 13 17 \
  "$audit_record/../../terminal/data/witness.points"
```

Recheck input hashes against the receipts. A repeated result must include
both PASS records. `controls POINTS` runs internal controls; the original
orchestration receipt records every external mutation.
