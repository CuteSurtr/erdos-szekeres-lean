# Independent original left16 replay and all-left T7 closure — PASS

**CERTIFIED:** the original compact left16,n7 CNF has a fresh accepted
binary LRAT replay with stable before/after streamed hashes. This uses
the original formula, with no long-cup augmentation. The complete map,
variables and clause families were independently rebuilt in the frozen
[left16 instance audit](../left16_longcup/README.md).

CNF SHA256: `2e233545d18e3a9acf9a253b80a102935828bee27c079ba18946dfbd4efd53d8`.
Raw4724116807byte proof SHA256:
`247f64c822609e878be490e059fb7e0c96e5e71fde0e265de74c7be36cd8dd42`.
Compressed proof SHA256:
`9b34ae9a407ce304f0ed82b9dbc6947a0219419a46145a326cfa189dd772b206`.
Checker SHA256:
`c14ff49853e890436d6a2fbf66a85b9492dad1dcd2d76254f16a89f2236c8a54`.
Proof files remain at the original scratch paths in data/retryB/result.json.

## Clean replay and preserved failure

AttemptA printed the exact accepted line, then optional /proc child-IO
telemetry raised PermissionError at child exit. Its source and logs remain
unchanged in data/attemptA, including its FAIL wrapper record. This was an
accepted checker line with failed wrapper, not a checker rejection. The
manual posthash recovery remains supplemental evidence only.

The parent requested fresh clean retry. RetryB changes only the output
directory, unit identity and vanished-process telemetry exception handler
(PermissionError added alongside FileNotFoundError and ProcessLookupError).
It changes no proof access, checker arguments, acceptance or hashing logic.
The source hashes and exact substitutions are in data/retryB-preparation.json.
Exclusive outputs in data/retryB show exit0 AND the exact line
`s VERIFIED UNSAT`; all four input identities and hashes match after the
check. RetryB finished08:17:29KST, checker134.536872s, total145.347806s.
Peak RSS2870348KiB; cgroup peak3010473984bytes; swap0. The final unit is
inactive/dead with Result=success and ExecMainStatus=0. Allocation released.

Limits: heap2800MiB, stack32MiB, AS3100MiB, CPUQuota100%, affinity5,
nominal MemoryMax4000M, Swap0, Runtime780s, checker660s; internal3100MiB
guard. Cache release every1s or64MiB read progress, plus64MiB chunks and
remainders during both streaming hashes. There were133 checker release
rounds and210 hash cache-release calls. No other own audit or compilation
overlapped the large check. Packaging uses AS150, one CPU, wall20/CPU19.

## Exact all-left statement and explicit coverage

**PROVED (written, with the following certified and checked dependencies):**
For every finite real GP set L with distinct increasing x coordinates,
no four-cap and no convex seven-subset, at least one of these holds:

1. A cup B meets every convex six-subset of L, and every member of B after
   its first is the right endpoint of an ambient three-cap in L.
2. L partitions into cups B,D with |D|<=5.

This is T7(L). Empty and small sets are included by the explicit lower
coverage; no monotonicity in the size of the ambient set is assumed.

* |L|<=10: form the standard low join with a three-cup. The join has no
  five-cap/no seven-gon and total size<=13. Terminal existence at those
  sizes uses separately [through11](../../../boundary/audit/VERIFY_BOUNDARY.md),
  [size12](../../audit/VERIFY_EXTENSION.md), and
  [exact13](../../exact_audit/replay13/README.md). The audited exact low-join
  classification converts its terminal selector to T7(L). The construction
  and classification are written in [the low encoder audit](../VERIFY_LOW_SPLIT.md)
  and the explicit lower coverage in [replay](../replay/README.md).
* |L|=11,12,13,14: each individual formula is independently audited and
  freshly certified in [replay](../replay/README.md).
* |L|=15: individual compact formula and fresh accepted replay are frozen
  in [left15](../left15/VERIFY_LEFT15.md).
* |L|=16: the original compact instance audit and this clean retryB.
* |L|>=17 is excluded by the inherited checked geometric_capacity16
  theorem, whose exact source and parent PASS receipt are retained here.

Capacity16 source SHA256 is
`8d5ced5ab84da9ba9347bc4fd1f99952dfa876302c35a712e9e8fec284a003d3`.
Its conclusion is n<=16 for a Configuration with no4cap and no convex7gon,
with no extra cup restriction. The parent Lean4.24.0 check exits0 and its
three axiom reports contain exactly propext, Classical.choice, Quot.sound.
This packet reviews that source/scope and pins its source, receipt and log;
it does not independently rebuild Lean or claim end-to-end Lean checking
of the finite encoder/certificate chain.

The all-left statement is not unconditional positivity for every low join.
The critical n7 branch with singleton L and right cup maximum5 still needs
a selector in the right block. No unrestricted terminal theorem, weak-Delta
existence theorem, ES bound or global minimum is inferred here.

All prior packets stay frozen. No longcup16 or UNKNOWN14 formula is used.
No further proof replay is needed for this packet; the saved launch command
documents the run and must not be reused against its exclusive output path.
