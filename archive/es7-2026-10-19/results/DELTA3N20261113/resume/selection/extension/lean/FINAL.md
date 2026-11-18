# PROVED: frozen envelope algebra and fixed Boolean refutation

Frozen at 06:18 KST, 14 November 2026. The parent freshly replayed all six finished
Lean files, matching every source hash. Each check exited zero without warnings
or a resource-guard stop. The 41 declaration audits in each pass use only
`propext`, `Classical.choice`, and `Quot.sound`.

| Finished source | Result | Parent seconds | Parent max RSS (KiB) |
|---|---|---:|---:|
| `WeightedEnvelope.lean` | Weighted coefficient certificate for the nonnegative ray | 0.668 | 1,308,308 |
| `FieldAdapter.lean` | Canonical field adapter for checked arithmetic proofs | 0.496 | 1,296,524 |
| `TwoSupport.lean` | Finite one-or-two-support necessity and equivalence | 2.031 | 1,325,852 |
| `NumericalExample.lean` | Exact margin, individual failures, and exposure interval | 1.997 | 1,315,624 |
| `OpenHalfline.lean` | Equivalence of domination on `t > 0` and `t ≥ 0` | 0.658 | 1,289,316 |
| `Terminal15Boolean.lean` | Fixed 15-variable, 313-clause Boolean UNSAT | 11.818 | 583,912 |

The envelope theorems hold over any linearly ordered field. The numerical example
proves the half-sum margin `11/4`, single-support failures, and exact height-three
exposure interval `14/3 < t < 7`. The open-ray bridge needs no continuity import.

The Boolean source contains the full fixed formula and derives its contradiction
from the supplied 98-clause subset using ordinary proof terms. All 313 source
rows were matched to the original DIMACS input. This does not formalize coordinate
validity, geometric encoding, convexity, or the full 15-point geometric claim.

Detailed records and bounded replay commands:

- [Closed-ray algebra and exact example](README.md)
- [Open-ray bridge](OPEN_RAY.md)
- [Fixed Boolean refutation](BOOLEAN.md)
- [Fresh parent replay manifest](data/parent-replay-manifest.json)

The parent replay manifest SHA-256 is
`624d8556c547d9c7f482437d933db9c2149458559b62b642bdab770bdb86469c`.
It links the original algebra, open-ray, and Boolean manifests and hashes every
fresh replay log and run record. The Boolean manifest SHA-256 is
`dd1eae579f3a3e2191b6b31dbb221d5cfe6dce0d397aade454d78d7a3121f7d3`.

`Envelope.lean` remains an explicitly excluded draft. No separate real specialization
or determinant theorem belongs to this packet. The earlier records' pending-replay
notes describe their checkpoint times; this final record and the parent manifest
record the completed replays. Any later geometry work is separate and must not
modify these frozen sources or evidence.

No Lean process or systemd Lean unit remains from these packets. The 1300 MiB slot
was released before parent replay and has subsequently been reassigned explicitly
for the separate geometry assessment. No commit, installation, branch change,
deletion, or write outside the authorized task directories was performed.
