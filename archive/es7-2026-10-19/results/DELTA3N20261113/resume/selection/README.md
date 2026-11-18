# Favorable Delta selection, 14 November 2026

**Continuation at 04:10 KST:** [boundary/README.md](boundary/README.md)
adds independently replayed terminal-safe selection through 9/11/13 old
points for n=6/7/8, an explicit all-n refutation of the cup/complement
shortcut, and exact uniform-envelope lemmas. The earlier pass below is
retained with its original scope. The general conjectures remain open.

**PROVED written selection/repair lemmas; CERTIFIED finite rooted statements
and three fixed-instance obstructions. Weak D(5,7) and D(5,8) remain open.**
This pass tests the existence assumptions behind the previous extension
criteria. It finds a useful selection theorem and refutes two stronger rules
which would have made a general induction easy. Nothing is Lean-checked,
refereed, or claimed as a literature first. No ES bound changes.

The parent investigated weak Deltas containing a prescribed rightmost point.
Parallel tracks covered terminal-safe selection (`terminal/`), repair by
newly selecting old points (`repair/`), and cup-rank selection arguments
(`structure/`). A separate worker audited both rooted encodings and replayed
all ten successful finite certificates. Every track has a disjoint scope.

A Delta in U=S−r which remains cap-free after adjoining r exists exactly
when S has a weak Delta containing r: restriction and extension give the
two directions. This is stronger than unrestricted weak Delta. A failure
of this rooted statement would invalidate that induction route, not the
unrooted conjecture. No failure of rooted existence was found. Failures of
other proposed selection rules are distinguished from weak-Delta failures.

## Positive written results

**PROVED:** for n≥6, any five-cap-free set S with |S|≤2n−3 has a weak Delta
containing its rightmost point. No no-n-gon assumption is needed. This gives
11 points for n=7 and 13 for n=8. The proof chooses a sufficiently long cup
when one exists; otherwise, old target polygons' right endpoints all lie in
one cup-rank level which is safe for extension.

The underlying subclass theorem has no point-count bound: put U=S−r. If U
has no (n−2)-cup, its target polygons' right endpoints E give a rooted Delta
E∪{r}, provided r is rightmost and S remains five-cap-free. The key rank
lemma says a cap triple a<b<c with ambient terminal rank three must have
β(a)<β(b), where β is longest cup length ending at a vertex. A single
β-level is therefore terminal-safe. See [structure/theory.md](structure/theory.md).

**PROVED:** for n≥5, any old weak Delta on S−r can be repaired by deleting
selected points and selecting at most one previously unselected old point
when S is five-cap-free and |S|≤n+2. At |S|≤n+1, no newly selected old point
is needed. r need not be extreme; no no-n-gon assumption is used. See
[repair/THEORY.md](repair/THEORY.md).

The structure record also reviews the parent's separate nonconvex-four
argument: for n≥6, |S|≤n+3, no five-cap and no n-gon, **any prescribed root**
belongs to a weak Delta. Its seven-point example refutes a proposed pure-cap
cardinality tool, not rooted Delta.

## Finite rooted certificates

**CERTIFIED and independently replayed:** every (5,n)-valid signotope has a
weak Delta containing its rightmost point through **13 points for n=7** and
**14 points for n=8**. Ten individual LRAT proofs passed cake_lpr and a
separate worker's replay. Smaller sizes have a direct cardinality argument.
The real-point statements follow. These are stronger finite statements than
ordinary weak Delta, not a proof of the arbitrary-size conjecture.

| Method | Accepted sizes | UNKNOWN sizes / allowance |
|---|---|---|
| Filtered rooted formula, n7 | m9–13 | m14–16, 60 seconds each |
| Filtered rooted formula, n8 | m10–14 | m15–16, 60 seconds each |
| Specialized rooted formula | none claimed | n7/m14 and n8/m15, 300 seconds each |

All 15 filtered formulas independently regenerate byte-for-byte; canonical
real controls verify the root-preserving projection and size reduction.
See [ROOTED.md](ROOTED.md) and [independent audit](audit/VERIFY_ROOTED.md).
The alternative formula has its own source review and controls; no accepted
theorem depends on its UNKNOWN runs. Its preliminary ten-second probe also
ended UNKNOWN. All 315 supplied real sets admit a checked rooted Delta in
the C++ finder; this finite observation is not an all-size proof.

## Certified failures of stronger rules

| Rule refuted | Real witness | Exact result |
|---|---|---|
| Some Delta always has every cap triple ending in an ambient rank-four pair | n7, 18 points | 18-variable / 108-clause core CERTIFIED; no terminal-safe Delta among all 262,144 subsets |
| Every old Delta admits repair with at most one newly selected old point | n7, 14 points, rightmost r=13, old A={5,11,12} | 14-variable / 213-clause formula CERTIFIED; minimum cost exactly two |
| Same repair rule | n8, 16 points, rightmost r=15, old A={7,13,14} | 16-variable / 277-clause formula CERTIFIED; minimum cost exactly two |

The conditional terminal-pair extension lemma remains valid; its sufficient
condition cannot always be met. The 18-point example nevertheless has a
Delta {0,5,6,7,8} satisfying the **weaker envelope condition for every X to
its right**, proved by exact rational line comparisons. It has 8,149 ordinary
weak Deltas. Thus it does not refute envelope-based favorable selection.
See [terminal/README.md](terminal/README.md).

The repair formulas allow arbitrary deletions from A and either color for r.
Both examples still have ordinary and rooted Deltas: {1,5,9} and {1,5,9,13}
for n7; {2,3} and {2,3,15} for n8. A short private-polygon argument proves
that two old-blue selections are necessary; these examples attain two.
See [repair/README.md](repair/README.md). No weak conjecture is refuted.
No global size-minimality is claimed. The terminal witness is one-point-
deletion minimal; the terminal-rule question at n8 remains unresolved.

## Independent checks, proofs and failures

`check_obstructions.py` imports no finder/encoder. It reconstructs each CNF
family using integer hulls and all-triple cap tests, scans all subsets,
checks the terminal core is a literal subformula, and verifies minimum
repair costs and the all-X envelope witness. Its
[report](data/parent_obstructions.json) agrees with the tracks' separate
implementations. Fresh accepted proofs are in `data/certificates/`.

| Obstruction | CNF SHA-256 | Fresh LRAT SHA-256 |
|---|---|---|
| Terminal core | `5318a34178cd3aa6acb9f83de54f4e9510b0a968a98fc0c8eb40b20ce135d0dd` | `0689a7c86c3173803b6fab75a557cb1eb1383d51c6b9ef50c8369003d3614881` |
| Rightmost repair n7 | `ef26f775f629af551be837b84e9f106948b4163e674018e9980fd225b5df0edd` | `aa502ff4a7bee4a01aef7c9e15b2dd4f60838c8dda63222607953d110258b1ac` |
| Rightmost repair n8 | `6517d49858bbaf2ae7cd743fb1d4597f62f8320ad05642a9952ea8ae65950f74` | `4eb33137aa612a3aeb077cbdc1b03f51df6d328a08c85095dc197b0bb324d194` |

All proofs and incomplete traces are retained. Parent runner zstd copies
have verified decompressed hashes. Failed/invalid probes and UNKNOWN results
remain in the record. The structure track corrects the parent's initial
projective sign suggestion: with its displayed transformation, a cap turn
through r corresponds to a **positive**, not negative, transformed slope.
That corrected normal form is a reformulation, not an existence proof.

## Remaining target and resources

A general induction must choose a favorable old Delta or permit more
extensive recoloring. The weaker envelope selection rule remains open.
The written cup-rank proof narrows a first possible failure at |S|=2n−2:
the old maximum cup length would be n−2, and **every** such cup would leave
a convex (n−1)-gon. Combining this with the no-n-gon hypothesis is a concrete
remaining proof problem; no contradiction is claimed here.

All five new long units finished. The two sweeps used CPUQuota100%, AS900MiB,
MemoryMax1200M, no swap, RuntimeMaxSec900. The specialized pair used the
same CPU/memory limits and RuntimeMaxSec600. The obstruction unit used one
CPU, AS400MiB, MemoryMax600M, no swap, RuntimeMaxSec180. Independent short
cake replays used a parent-reserved AS800MiB allocation within the existing
6000-MiB track cap. Other short probes used one CPU, AS400MiB (compiles up
to 500MiB) and at most 20 seconds. Global caps stayed 16 threads and 24 GB.

No new unit was stopped by the guard. Specialized-job anonymous memory was
observed at about 81/110 MiB; larger cgroup usage was file cache, with zero
swap and OOM events. The existing memguard5 stays active for unrelated jobs.
No research cap or guard setting was changed. All new workers are closed
after finalization.

`data/summary.json`, `data/archive_manifest.json`, unit logs and live-state
snapshots preserve commands, outcomes and external hashes. No proof was
deleted; no commit, push, branch change, repository-root README or math.md
edit was made.

Scratch: `/home/jay/research/data/delta3-codex-20261113/selection/`.
Scoped manifests and the refreshed parent DELTA3 SHA256SUMS pin the result.
From the repository root, reproduce the parent coordinate audit or refresh
small evidence with the research venv Python, under a 20-second timeout and
AS400MiB, using this directory's `check_obstructions.py` or
`collect_selection.py`. Track README files give exact commands. Archive
refreshes change timestamps and require manifest refreshes. Long solver
reruns require the same systemd limits and a fresh live-resource check.
