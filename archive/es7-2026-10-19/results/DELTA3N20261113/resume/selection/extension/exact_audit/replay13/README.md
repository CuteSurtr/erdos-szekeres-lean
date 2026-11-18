# CERTIFIED: independent n7/m13 exact-augmentation replay accepted

The fresh independent cake_lpr log contains exactly **`s VERIFIED UNSAT`**.
The CNF, 1,356,527,316-byte binary LRAT, compressed proof and checker binary
have identical streamed SHA-256 and file metadata before and after replay.
Completed **14 November 2026, 06:17 KST**. The unit is stopped and its
900 MiB reservation released; the track has returned to short AS300 checks.

## Statement and dependencies

This accepts the exact-augmented **n7/m13** CNF already reviewed in
[VERIFY_EXACT.md](../VERIFY_EXACT.md), using the inherited
[generic base audit](../../audit/VERIFY_EXTENSION.md). Accordingly, every
real x-ordered general-position 13-point set with no five-cap and no
convex seven-gon has a terminal-safe weak Delta.

Coverage **through 13** additionally uses the separately established
[through-11 boundary result](../../../boundary/audit/VERIFY_BOUNDARY.md)
and [size-12 certificate](../../audit/data/replay-n7m12.json).
It is not inferred by monotonicity from the size-13 certificate. No larger
ambient size, Lean formalization or unconditional m14 result is claimed.

## Method and soundness

The formula's canonical projection and reverse-augmentation proof were
already independently checked; no source regeneration or re-solve was
needed. This new subdirectory is an append-only continuation of the frozen
formula packet. The prior packet's files and manifest remain unchanged.

[tools/replay.py](tools/replay.py) independently checked the completed parent
receipt, streamed hashes, invoked cake_lpr, required an exact acceptance
line, and rehashed all inputs. Exit zero alone was not acceptance. The new
stdout is [data/cake.stdout](data/cake.stdout); detailed evidence is
[data/result.json](data/result.json). The parent's accepted log is not used
as a substitute for this fresh checker invocation.

## Results and controls

Cake: **40.166 seconds**, 668,728 KiB peak RSS; exit zero and one exact
acceptance line. Total unit work including pre/post hashes: **43.506 seconds**.
Cgroup peak: **743,759,872 bytes** (about 709 MiB), zero swap, below both
the requested 1,200 MiB unit limit and its 80% threshold. No memory-stop,
timeout, failure, or re-solve occurred.

Pre/post hashing read 1 MiB blocks and issued 70 cache-release calls,
releasing completed regions every 64 MiB plus each final remainder.
During cake, 39 once-per-second input-cache releases occurred, each before
64 MiB of additional observed input; the 64 MiB progress fallback did not
need to fire. The 100 ms monitor also enforced a clean-stop threshold of
900 MiB current cgroup memory. These releases did not change proof bytes.
The active shared memory guard lifted the kernel memory.max as designed
and enforced the original nominal limit. No allocation was raised by us.

## Files and hashes

Inputs remain in `/home/jay/research/data/delta3-codex-20261113/extension/finite13-b/`.
Both raw and compressed proof are retained, unmodified.

| Artifact | SHA-256 |
|---|---|
| input.cnf | `3ec4b75d9076b6f257fed83f3cbb17b8372a43f53f1c0fc8d30730e4c5d35b87` |
| proof.blrat | `d54f53ee64be1b7ddbc4c0eab2aa53ec41899112e319ff0272b3b24ddf8bca64` |
| proof.blrat.zst | `61aff8b5a0f8e7deb851fd286a6063303f59461d08f7ca02becbec82ac5e7514` |
| cake_lpr | `c14ff49853e890436d6a2fbf66a85b9492dad1dcd2d76254f16a89f2236c8a54` |

[data/hashes-before.json](data/hashes-before.json) and
[data/hashes-after.json](data/hashes-after.json) include sizes and metadata.
The compressed proof was hashed independently; its decompression roundtrip
is inherited from the completed parent receipt, not rerun here. The raw
proof itself was independently checked in full. [SHA256SUMS](SHA256SUMS)
covers this new replay packet only.

## Resource authorization and what remains

The user's explicit reservation was one CPU, AS900 MiB, cake heap650/stack32,
CPUQuota100%, MemoryMax1200M, MemorySwapMax=0 and RuntimeMaxSec600 in
`nov13c-vfy-delta6-replay13`. Actual process limits and affinity 5 are
retained in [data/start.json](data/start.json); the cake command is
[data/command.json](data/command.json). The monitor used an internal
480-second cake wall deadline. The unit's outcome and stopped state are
retained. No additional verifier overlapped this allocation.

The assigned independent replay is complete. No replay job remains active
or queued. Protection and conditional m14 formula audits are separate work.

## Reproduction

The script refuses to overwrite receipts. A future run must use a fresh
authorized output directory and a renewed resource reservation, check CPU
availability and the shared guard, and preserve all outputs. Use the exact
cake command from `data/command.json` under the same bounds. A long replay
must retain finite systemd limits and periodic input-cache release.
