# CERTIFIED: no one-point cup-side n7 lift; PROVED: weak n8 survives ≤5 insertions

Local continuation completed on 14 November 2026. **CERTIFIED:** the all-gap
one-insertion cup-side n7 extension CNF is UNSAT, with cake_lpr's exact
`s VERIFIED UNSAT` line. **PROVED:** a 5-cap-free extension of a hexagon-free
set by ≤5 points has a weak n8 Delta. **COMPUTED:** the two-insertion n7 cup
search was UNKNOWN after four seconds. No n7/n8 counterexample was found.
No general Delta conjecture, numerical ES bound or novelty claim follows.

## Statement

Fix the increasing-x orientation of the real cup15 counterexample, source
SHA-256 `1e8b43136d096abb2deaea14743ed62a52ff622a991dd2fbbcb7140a15593b04`.
Every 16-point signotope containing an increasing copy of this source and
having no 5-cap or convex heptagon has a 4-cap-free subset meeting the lower
chain, including endpoints, of every hexagon. This includes every real
one-point extension, in **all 16 x-order gaps**. It does not cover arbitrary
16-point sets or extensions by two or more points.

Separately, if S has no hexagon, Q=S∪A has no 5-cap and |A|≤5, every heptagon
uses ≥2 points of A. There is a 4-cap-free R⊆A omitting at most one point:
trivial for |A|≤4; if all four-subsets of a five-point A were caps, every
triple would be negative and A would be a forbidden 5-cap. Thus R meets
every heptagon. No absence-of-octagons assumption is needed. The argument
also applies to signotopes. See [MODEL.md](MODEL.md).

## Model and soundness

`extension_cnf.cpp` includes the existing, independently reviewed
`../../encoder/delta_cnf.cpp` unchanged. It adds exactly-one monotone
selectors placing old point i at i+d_i, and fixes every old triple sign
at its selected positions. This covers all C(15+k,k) insertion patterns
in one formula. Both directions are proved in [MODEL.md](MODEL.md).
The default includes the complete counterexample condition, no symmetry
restriction and no cluster assumption. It fixes the old **order type**, not
metric coordinates, and includes secant-aligned and nonlocal insertions.
SAT would still require real realization. Partial `--base-only` and
`--embedding-only` controls are not counterexample searches.

MODEL.md also proves that isolated secant ties reproduce generic binary
signs. Escaping that model requires an aligned doubled fiber to distinguish
representatives of another doubled fiber. Its exact sign-split control is
not a valid Delta candidate: 15 five-caps and 13 heptagons are retained.

## Method

The streaming C++ encoder and bounded Python runner retain every outcome,
CNF, log and LRAT trace. `audit_extension.py` imports no existing encoder
or checker; it checks every actual clause, the old copy, geometric premises
and all Delta subsets. Integer-coordinate controls use exact determinants
and hulls. SAT models remain abstract until separately realized.

All local jobs used one CPU and <400 MB AS (360 MiB or 380,000,000 bytes),
with outer deadlines ≤29s. The C++ compile used <500 MB AS, 1.80s and
184,808 KiB RSS. No long job/unit was launched here and the generic-cluster
certificates were not re-solved.

## Results

| Cup-side case | Variables | Clauses | Literals | Local outcome |
|---|---:|---:|---:|---|
| n7 +1, all 16 gaps | 142,767 | 453,999 | 2,120,077 | CERTIFIED UNSAT |
| n7 +2, all 136 patterns | 279,911 | 813,993 | 3,887,521 | UNKNOWN, 4s |
| n7 +3, all 816 patterns | 550,491 | 1,453,700 | 7,083,695 | generated only |
| n8 +3, all 816 patterns | 570,680 | 2,067,027 | 10,818,523 | generated only |

The +1 solver used 0.36s and 87,756 KiB RSS. Its replay used cake heap192/
stack16, 0.65s and 200,252 KiB RSS. Only the exact success line supplied the
certificate label. The +2 probe used 4.09s and 212,388 KiB RSS; its partial
trace is not a proof. No larger local solver probe followed. Additions
0–5 are supported; larger exact counts are in `data/sizes.json`.

The parent's fresh independent certification unit
`nov13c-vfy-delta3r-lift-n7add1` also **passed**: solver 0.364s, cake 0.564s,
the exact success line, and the same CNF and 2,338,806-byte LRAT hashes.
Its result and checker log were read, and copied into `data/parent-add1/`.
The larger +2 run remains for a parent memory reservation.

## Controls and retained failures

The final [control report](data/controls.json) passed:

- 10,240 exhaustive orientation/embedding combinations: 5,120 accepted and
  5,120 rejected exactly as direct triple lookup requires; three invalid
  selector assignments rejected. All 35 placements on seven parabola points.
- A valid real16 extension: no 5-cap or heptagon, 95 four-caps, 30 hexagons,
  12 lower targets, 10,924 working cup Deltas; all **203,832 actual base/
  embedding clauses** hold under exact coordinates.
- Independent source15 counts: 80 four-caps, no 5-cap or hexagon, 216
  pentagons, 103 lower targets, zero cup Deltas. Its full pinned formula
  is SAT and passes all 182,481 actual clauses.
- The interacting-secant control: opposite pair/third signs, 650
  distinct-fiber representative triples preserving old signs, and all
  9,289 embedding clauses satisfied; geometric invalidity is retained.
- A nonvacuous weak-n8 control with a four-cap among five inserted points:
  the displayed four-point Delta meets all 40 heptagons; no 5-cap exists.

These controls share this sidecar's independent geometry module; they are
not mutually independent encoders. Existing universal-encoder soundness
and audit remain dependencies. See [VERIFY_LIFT.md](VERIFY_LIFT.md).

Failures remain in scratch and saved reports: `controls-1` placed its
nonlocal point collinearly with the q-pair (normalized (2,1)); (2,3) fixed
the fixture. `controls-3` had no heptagons and was rejected as vacuous;
the replacement has 40. Neither failed fixture supports a claim.
No proof, SAT trace or UNKNOWN trace was deleted.

## Files and hashes

All changes are in this sidecar. Scratch:
`/home/jay/research/data/delta3-codex-20261113/resume/lift/`.
Sources, model, checks and commands are here; small reports/logs/fixtures
and a frozen source snapshot are in `data/`. Large CNFs remain in scratch.
`READY.json` indexes the handoff; `SHA256SUMS` hashes this snapshot.

| Artifact | SHA-256 |
|---|---|
| add1 full CNF | `9138cb5807ca6d208e2cb3f1519b0060026d495e295e9388c1f45bc35284d233` |
| add1 original LRAT | `41978f2d53df04787a34aba49a119675079d95b63bb5f5350cef7541289467f1` |
| unchanged universal encoder | `b953e14fc7d0840712bbf63f502e00c7342cbd1cdb9ef3ed548759e8ae8aa12c` |
| extension encoder | `eac5c72391a0090468e28022f424f4aa43c6efa8aea1767207d3e0985d5dec5a` |

Plain and zstd proofs/traces are retained, with decompressed hashes checked.
The certified compressed proof is also in `data/`. Optional unit propagation
is separately documented and tested; **the certificate did not use it**.

## What remains

Cup n7 with ≥2 insertions is open here; cup n8 becomes nonvacuous at two
insertions, since one cannot create a heptagon over a hexagon-free source.
Weak n7 needs ≥4 insertions. Weak n8 cannot fail with ≤5 by the written
proof. No result here is Lean-checked. The successful independent parent rerun is
separate from the local first replay. No commit, branch change, push,
install, root README/math edit or other-agent file edit occurred.

## Resume commands

See [COMMANDS.md](COMMANDS.md). The next useful search is n7 cup +2 after
the parent reserves memory. No long job or queue was launched by this task.
