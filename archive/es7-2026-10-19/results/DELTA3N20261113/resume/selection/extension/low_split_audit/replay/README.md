# Independent low-split proof replays — CERTIFIED / PASS

All four fresh cake_lpr runs printed exactly `s VERIFIED UNSAT`. Together
with the frozen [formula and projection audit](../VERIFY_LOW_SPLIT.md) and
the explicit lower-size coverage below, this establishes **T7(L) for every
left size at most14**, for real x-ordered GP L with no four-cap and no
seven-gon. No left15/16 or unrestricted all-size assertion is made.

T7(L) is the disjunction of: (1) a cup B meeting every convex six-subset,
with every selected vertex after its first ending an ambient L three-cap;
or (2) a partition into cups B and D with |D|<=5. The source audit proves
the encoded failure is precisely failure of these options on real L.

For |L|<=10, join L to a sufficiently low three-cup. This admissible set
has at most13 vertices; its terminal selector gives T7(L) by the audited
two-option classification. The separate dependencies are the
[through11 theorem](../../../boundary/audit/VERIFY_BOUNDARY.md),
[size12 formula/certificate audit](../../audit/VERIFY_EXTENSION.md), and
[independent exact size13 replay](../../exact_audit/replay13/README.md).
The empty left case is immediate. Sizes11,12,13,14 are covered individually
by the four replays here. There is no inference from a larger ambient size
to a smaller one by monotonicity.

| Left size | Heap / AS MiB | Cake elapsed seconds | Cake peak RSS KiB |
|---|---:|---:|---:|
| 11 | 128 / 300 | 0.101 | 134268 |
| 12 | 128 / 300 | 0.402 | 134296 |
| 13 | 128 / 300 | 2.708 | 134344 |
| 14 compact | 450 / 700 | 17.973 | 464212 |

The replay driver independently invokes the pinned checker and requires
its exact acceptance line; exit zero alone is insufficient. Each CNF,
raw proof, compressed proof, and checker binary has identical streamed
pre/post SHA-256, size, mtime, inode and device. Hashing releases cache
every64MiB and at the remainder. The raw/compressed proofs remain at their
original paths; full hashes and commands are in data/m*/result.json.

The compact14 CNF hash is
`0d8a698c0253d249a6ebbb4d021295ffc06569a34b274ee885cd12fff2931183`;
its624,474,740-byte binary LRAT hash is
`7d67e3161247eb508fc0378a888a3508fb9c36d2b60200d7cd2ece8da916b494`.
The original parent's heap128 exhaustion is preserved in low14-n7-b;
it is not relabeled as an accepted run.

All runs were sequential, on one CPU/affinity5/nice10, stack32, with no
other own check or compile overlapping cake. Short wrappers enforce
AS300, wall20/CPU19. Compact14 ran in
`nov13c-vfy-delta6-low14-independent` with AS700, CPU450,
CPUQuota100%, nominal MemoryMax1000M, MemorySwapMax0, RuntimeMaxSec480,
and an internal360-second cake deadline. The shared guard was active;
the driver separately monitors its700MiB cgroup threshold every0.1s and
releases both inputs every1s or64MiB read progress. Observed cgroup peak
was537,980,928 bytes (513.06MiB); swap remained0. Its19.571-second total
includes all pre/post hashes. The unit is inactive and the extra400MiB
reservation was released. After systemd garbage collection its final
properties omit peak fields, so the in-unit saved counters are authoritative.

This is a new append-only subpacket. The original128-file audit manifest
is rechecked unchanged; its historical statement of zero fresh replays
remains correct for that earlier packet. This addendum supplies the fresh
replays. No solver, compilation, deletion, git or external action occurred.

`data/short.command.sh` and `data/low14.command.sh` preserve exact commands.
The driver creates output directories exclusively: do not rerun over this
frozen record. Any later replay needs a new disjoint record and allocation.
