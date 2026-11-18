# Terminal-safe selection at the first boundary

**CERTIFIED finite boundary cases, independently replayed; PROVED written
reductions and an all-n counterexample to the cup/complement shortcut.**
Started 14 November 2026, 03:51 KST. Weak D(5,7), D(5,8), and general
uniform-envelope selection remain open. No numerical ES bound changes.
Nothing here is Lean-formalized or externally refereed, and no literature-
priority claim is made.

## Statement

For **n=6,7,8**, every real set U in general position with distinct
x-coordinates, no five-cap, no convex n-gon, and **|U|<=2n-3** has a
terminal-safe weak Delta A. It contains no four-cap, meets every whole
convex (n-1)-gon, and every three-cap in A ends in a pair that is also the
last pair of an ambient four-cap in U.

Consequently the **same A**, chosen before the insertion, works after
adjoining **every** rightmost point r for which U+r remains five-cap-free:
A+r is a weak Delta. The extension U+r may contain an n-gon. The old-set
bounds are **9, 11, 13** at n=6,7,8, and extension sizes are 10,12,14.
This improves the terminal-safe bound by one old point. It does not enlarge
the previous finite rooted frontier under the full no-n-gon premise. The
extra no-n-gon hypothesis on U is used for this additional old point.

## Model and soundness

The prior cup-rank argument handles |U|<=2n-4 and the short-cup subclass.
At |U|=2n-3, failure requires maximum cup length n-2 and a convex complement
to every maximum cup. The new terminal formulas test failure of every
terminal-safe Delta in precisely this remaining class.

They inherit the reviewed compact geometric CNF. New exact flags represent
four-caps and bad triples: cap triples whose last pair is not the last
pair of an ambient four-cap. Under no-five-cap, avoiding all bad triples
already excludes four-caps. Each failure row requires a bad triple in A
or an old target disjoint from A. All sizes **0 through |U|-n+2** are tested.
Larger safe solutions can be shrunk; growing a safe two-set to three is
not assumed. See [SOUNDNESS.md](SOUNDNESS.md) and
[the written reduction, Section 8](theory/theory.md).

## Method and results

| n | Old points | Variables | Clauses | Result |
|---|---:|---:|---:|---|
| 6 | 9 | 672 | 5,675 | CERTIFIED; independent replay accepted |
| 7 | 11 | 2,376 | 23,135 | CERTIFIED; independent replay accepted |
| 8 | 13 | 8,437 | 97,047 | CERTIFIED; independent replay accepted |

CaDiCaL 2.1.3 produced retained LRATs; cake_lpr printed exactly
`s VERIFIED UNSAT` for each proof. A separate worker reconstructed the new
clause families with its own code, checked canonical real assignments,
reviewed the written arguments, and replayed all three proofs. The largest
proof is 121,542,197 bytes; its verified zstd copy is 37,753,179 bytes.
See [the independent audit](audit/VERIFY_BOUNDARY.md).

The initial complementary-cup formulas were SAT in all six old/root
cases at n=6,7,8. All three root models have exact integer realizations.
Adding exclusion of a full-set (n-1)-cup gave three more realized SAT
models. Parent and independent checks confirm these six real fixtures.
All have terminal-safe and rooted Deltas; they refute only the shortcut.

## A written obstruction family for every n>=6

An explicit integer family has **2n-3 points** in three cup blocks of sizes
n-3,3,n-3. It has no five-cap or n-gon, exactly six maximum (n-2)-cups, and
a convex complement for every maximum cup. Its maximum-cup exchange graph
is two disjoint triangles. Nevertheless any two points from the middle
block form a terminal-safe weak Delta.

The proof classifies the triples and target polygons for every n>=6.
Independent exact controls at n=6,7,8 passed. See
[the construction](theory/theory.md) and
[parent controls](data/parametric_parent.json). Thus the geometric premises
of the boundary class cannot be disproved; selection within it is necessary.

## The weaker uniform-envelope route

A cap triple's terminal line exceeds the ambient four-cap envelope only
on an explicit open rational interval. Safety on the whole rightward
half-line has a certificate of one ambient line or a convex combination
of two. These yield a finite forbidden-triple formula for choosing **one
Delta before all insertions**; old four-cap clauses remain necessary.
A deletion-repair criterion uses the union of exposure blockers over all X.

These are written characterizations, not an existence theorem. Eight
selected real fixtures have positive exact solutions. The parent separately
checked their geometry, target exclusion, and all **364** cap-triple
domination certificates using integer/rational arithmetic and an independent
endpoint-chain calculation. See [envelope theory](envelope/theory.md),
[its record](envelope/README.md), and
[parent verification](data/envelope_parent_checks.json). No full-pool
coverage or universal uniform-selection conclusion is claimed.

## Controls, provenance and hashes

`check_models.py` uses direct integer determinants, convex hulls and subset
enumeration for the first three realized fixtures, cup complements, Delta
counts and safe extensions. `check_refined.py` checks the stronger short-cup
fixtures. The independent worker uses its own implementation again, with
valid and deliberately invalid-premise controls. A false failure row on
a positive Delta is the expected control result.

`check_envelope.py` imports no envelope-track code. Its DP was tightened
during review to exclude transitions from unreachable zero states; the
initial source and positive output remain under `data/development/`.
The final reachable-state version passed all eight cases. Its scope is
positive witnesses and rational certificates, not every exposure/CNF row.
It also agrees exactly with exhaustive subset/hull calculations on 280
deterministic general-position controls of sizes 2 through 8; see
[envelope_dp_controls.json](data/envelope_dp_controls.json).

| n | Terminal CNF SHA-256 | LRAT SHA-256 |
|---|---|---|
| 6 | `1e40345bfedd16d0130a0a00bc6a412d7a0caceb04bcd39879be99d71d9621c3` | `f34baddd285f8d0654223edf110c9e2986c43e707ff675a0aae5deedd420f9ce` |
| 7 | `0e166f5b577214271ab3ee72be49eb6e1f6d9eb02f1b5814774102252081f385` | `93fcdae4cc55d956f3b2d70e3d6e405b3b941cfa012eedd76599fa73b50dc6bd` |
| 8 | `aa3eb2c583c4db1f453085c2304a0ab8825a1365dab315fad3552c0eedff548c` | `f2626849d315ce741a7fce06c18ab03f7d8f6017b936b91f1f3d44849e4bc38b` |

Sources, commands, result receipts and selected compressed proofs are in
`data/archive/`. [archive_manifest.json](data/archive_manifest.json) pins
all retained external files; [summary.json](data/summary.json) indexes the
parent outcomes. Scoped SHA256SUMS and refreshed selection/DELTA3 manifests
pin the completed record. Proofs and incomplete SAT traces remain in scratch.

## Resources and remaining work

All four parent units finished: `nov13c-vfy-delta5-boundary`, `-realize`,
`-refined`, `-terminal`. Each used one CPU, AS900MiB, MemoryMax1200M,
MemorySwapMax=0, and RuntimeMaxSec900/180/600/720 respectively. The largest
formula has 536,536 literals (about 135 MB by the conservative per-literal
solver estimate); cake used heap600/stack32. The largest observed unit peak
was 762.8 MB. No guard stop occurred. Independent replays used a parent-
reserved AS800MiB allocation within the existing 6000MiB verifier track.
Short checks used AS400MiB and 20-second deadlines. Owner caps stayed
16 threads and 24 GB. The guard remains active for unrelated research.

No proof deletion, installation, commit, push, branch change, protected
repository-root README/math edit or external action was performed.

General favorable selection remains open. Terminal-safe selection already
fails at 18 old points for n=7; this pass proves a positive bound of 11,
without claiming 12 is the first failure. The weaker envelope condition
survives the tested examples. Intermediate sizes and repair using actual
exposure blockers are concrete remaining targets.

## Resume commands

From the repository root, use the research venv Python under a 20-second
external deadline for `check_models.py`, `check_refined.py`, or
`check_envelope.py`. Track README files give their own commands. Generators
refuse to overwrite run directories. Fresh solver runs need a fresh output
path, live resource check, and the same systemd limits. `collect.py` refreshes
small evidence and external hashes; this requires refreshing manifests.

Scratch: `/home/jay/research/data/delta3-codex-20261113/boundary/`.
