# Weak Delta: extreme-point extension and sharp repair obstructions

**PROVED:** a geometric sufficient condition for extending a weak Delta at a
rightmost point, an exact deletion criterion, and a sharp size bound for
failure of monotone extension of an arbitrary deletion solution.
**COMPUTED, checked by two separate implementations:** real nine-point n=7
and ten-point n=8 obstructions attaining that bound. Both have the full weak
Delta {0}; neither is a counterexample to D(5,n).

The original weak D(5,7) and D(5,8) remain open here. No cup-side assumption,
certificate claim, Lean formalization, literature-priority claim, or change
to an Erdős–Szekeres bound is made. Completed 14 November 2026 in the existing
DELTA3N20261113 record, exclusively in this assigned subdirectory.

## 1. Statement

Let U=S minus its rightmost point r=(X,Y), and let A be a weak Delta in U:
A is four-cap-free and meets every whole convex (n-1)-gon of U. Let

    F_j(V;X) = max height at X of a line through the last pair of a j-cap in V,

with max(empty)=-infinity. If S has no five-cap and

    F_3(A;X) <= F_4(U;X),

then A+r is a weak Delta in S. A sufficient combinatorial certificate is:
every terminal pair of a three-cap in A also ends a four-cap in U. Thus an
actual cap blocker can end only on a pair of ambient cap rank exactly three.
The complete proof is in [theory.md](theory.md), Sections 1–2.

For arbitrary removal R subset A, (A minus R)+r works exactly when R hits
every blocking triple and does not contain all selected vertices of any old
target polygon. This is a whole-polygon criterion with no hidden lower-chain
requirement. A blocker transversal of size t is safe when every old polygon
has at least t+1 selected points. See Section 3.

## 2. Model and soundness

All geometry is real, with distinct x-coordinates and no collinear triples.
Consecutive slopes characterize caps. A new cap must end at r, and appending
r to a cap ending b,c succeeds precisely when Y is below the line bc at X.
Five-cap-freeness therefore gives Y>F_4(U;X); the sufficient comparison gives
Y>F_3(A;X). Old polygons keep their old hits, and all new polygons contain r.

No n-gon-free hypothesis is needed for this sufficient extension theorem.
It applies in particular to valid (5,n) instances. The unknown part is whether
one can select a favorable old Delta on every valid deletion.

## 3. Method

Read AGENTS.md, the es-research skill, STATUS20261113, this record's root
README/VERIFY_DELTA3, and descent/theory.md, hypergraph/theory.md, a4/theory.md.
The new probe uses only integer determinants, hulls, and subset enumeration.
It exhaustively examined old Deltas on the two saved 12/13-point endpoint
fixtures, then retained smallest supports for a specific private-polygon
obstruction. No SAT solver, LP, random search, long job, or systemd unit ran.

`independent_check.py` imports none of the finder or earlier research code.
It uses triangle containment on four-subsets for convexity, consecutive turns
for caps, and exact rational line heights. This is a second implementation,
not a separate human review or a proof-assistant verification.

## 4. Results

| parameter | points | four-caps | target polygons | five-caps / n-gons | full weak Delta |
|---|---:|---:|---:|---:|---|
| n=7 | 9 | 9 | 9 hexagons | 0 / 0 | {0} |
| n=8 | 10 | 7 | 11 heptagons | 0 / 0 | {0} |

For n=7 take r=8 and A={4,6,7}; for n=8 take r=9 and A={6,7,8}. In each,
T=A+r is a four-cap, B=S minus T has n-2 points, and every B+t, t in T,
is a target polygon. Thus A solves the deletion, every q in A has private
polygon B+q, and B+r is missed. Breaking T loses a private polygon. All
16 choices of C or C+r with C subset A fail, including arbitrary many deletions.

**Sharp bound (PROVED):** on at most n+1 points every old Delta either already
works or safely adds r. If A misses a target polygon H, disjointness gives
|A|<=|S|-(n-1)<=2, so A+r cannot contain a four-cap. The examples therefore
have the minimum possible number of points for this precise repair obstruction.

Section 4 of theory.md also characterizes every obstruction at the threshold
n+2: necessarily |A|=3, T=A+r is a cap, and all four B+t are target polygons.
Section 5 proves a leftmost-point insertion preserving this obstruction while
raising n by one, giving sharp examples for every n>=7. Exact rational controls
of the lift from n=7 to 8 and n=8 to 9 pass independently.

## 5. Controls, failures, and labels

The final independent audit passed in under 0.04 seconds with 18,308 KiB maximum RSS.
It checks both complete coordinate instances, their source-file hashes and
retained indices, all 32 monotone failures, both alternative full Deltas,
and two rational lift controls. On the two obstruction fixtures and two
additional nonvacuous valid sets it checks:

- 863 old weak Deltas and 22,892 exact deletion choices;
- 553 terminal-pair sufficient cases, including 141 containing a three-cap;
- 565 envelope sufficient cases, so envelope domination is strictly more
  flexible than identical terminal pairs;
- 601 actual red extensions, so envelope domination is sufficient, not necessary;
- 508 blocking-triple occurrences, all with ambient terminal rank exactly three;
- 26 terminal-safe Deltas that miss an old polygon's lower chain.

These are finite **COMPUTED** controls, not a universal search over point sets.
Theorems are supported by their written arguments, not by these counts.

Two failed attempts are retained. A proposed simple family introduced an
explicit five-cap (`findings.json`, `failed_construction`). The first synthetic
positive controls were collinear; the independent checker rejected them.
`failed_audit_01.json` records the error. Their original statistics remain at
scratch `refined_initial_invalid_controls.json`. The corrected controls use
r=(8,1), have general position checked explicitly, and pass both implementations.
No UNKNOWN solver or compute outcome is omitted; no solver was invoked.

## 6. Files and hashes

- [theory.md](theory.md): precise statements, proofs, coordinates, and remaining gap.
- [findings.json](findings.json): frozen obstructions, source hashes, thresholds,
  and the rejected five-cap construction.
- [independent_check.json](independent_check.json): final audit, every failure
  witness, lift coordinates, and exhaustive counts.
- [VERIFY_WEAK_THEORY.md](VERIFY_WEAK_THEORY.md): verification scope and limits.
- `probe.py`, `refine.py`, `independent_check.py`: bounded standard-library tools.
- `failed_audit_01.json`: rejected synthetic-control record.
- `SHA256SUMS`: hashes of the delivered files, excluding itself.

Working results, including original endpoint scans and rejected-control data,
are retained under
`/home/jay/research/data/delta3-codex-20261113/resume/weak_theory/`.
The final manifest also hashes each retained scratch artifact by absolute path.

## 7. What remains

A proof of either original conjecture needs a favorable choice of old Delta
or a repair that can select old blue points. Deleting arbitrary old red points
does not suffice for an arbitrary old solution, already at nine/ten points.
The threshold and terminal-edge conditions give exact, non-cup-side targets
for a favorable choice; their existence on every valid deletion is unproved.
The parent's separate maximal-red-set investigation is neither duplicated nor
assumed. No further work is queued by this track.

## 8. Resume and resource policy

From the repository root, rerun the independent check:

```sh
timeout 20s env PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  python3 cloud/es7-2026-10-19/results/DELTA3N20261113/resume/weak_theory/independent_check.py
```

It rewrites only its own audit JSON; timing fields vary, so the manifest then
describes the delivered snapshot rather than the new timing bytes. `refine.py`
regenerates the small finder result in scratch; `probe.py --help` documents
the original endpoint scan. Every computation was one thread with an external
20-second limit, internal 18-second CPU limit, and 384 MiB address-space limit.
No third-party installation, git mutation, root record/root README/math.md
edit, or edit to another agent's files was made.
