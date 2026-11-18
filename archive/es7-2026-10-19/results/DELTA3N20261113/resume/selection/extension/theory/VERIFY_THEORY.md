# Exact checks of the two-support example

**Confirmed by separate arithmetic code within this track.** The parent
has separately reported independent geometry checks; independent parent
review of the written line calculations is not claimed here unless it is
recorded later in the parent's own scope. No SAT solver or certificate is
used. This is not a CERTIFIED result in the repository's LRAT terminology.

## Independent arithmetic implementation within this track

`tools/verify_examples.py` imports no finder and no prior envelope code.
It uses expanded 3x3 determinants and decreasing adjacent slopes, while the
finder used translated determinants and all negative triple orientations.
It cross-checks both cap definitions on every subset of sizes 3,4,5.

The replay checks all 56 determinants at both integer endpoints, identical
orientation signs, the complete list of three four-caps, absence of every
five-cap, the unchanged target cap triple, all ambient line coefficients,
failure of every single support, and the half-weight identity with surplus
11/4. The exposed endpoint is checked through exact affine differences;
its interval is (14/3,7). The insertion (13,-65/4) is in general position,
preserves five-cap-freeness and creates the target four-cap. Family checks
at h=3,7/2,34/9,4,5 include both signs and the exact zero-surplus transition.
The continuous-family statement additionally uses the written affine
determinant argument, rather than inferring it from those samples.

Output: [data/exact_replay.json](data/exact_replay.json), PASS. Both endpoint
sets have smallest absolute determinant 1. This check took about 0.009 s
and used 16,568 KiB peak RSS on the recorded run.

## Delta scope and insertion

`tools/verify_delta_scope.py` imports no other local checker. It enumerates
all subsets of both old sets and the augmented set, using monotone-chain
convex hulls, and checks every six-gon for intersection with the specified
selection. Output: [data/delta_scope_replay.json](data/delta_scope_replay.json),
PASS. All full-set maxima are (cap,cup,gon)=(4,4,6); the complement of A has
maximum gon four, including after insertion. A={0,3,6} remains a weak Delta
with r excluded, whereas A+r has a four-cap and fails. No six-gon containing
r exists in this insertion. There is no monotone failure claim.

The first version included an unjustified assertion that a new six-gon
must exist. It failed because the new-target list is empty. The initial
source and failure are preserved under `data/development/`; the final
version checks coverage without assuming nonemptiness. Geometry and line
results did not change. The final run took about 0.008 s and 16,200 KiB RSS.

## Parent geometry report

In the task conversation the parent reported a separate endpoint-chain DP
check using `boundary/check_envelope.py`, importing none of this track's
code. It found both eight-point sets and the nine-point extension have
maxima (4,4,6), and the complements in question have maximum gon four.
It also checked the four-cap in A+r. These agree with the exhaustive replay.
This file records the report, without manufacturing a parent result file.

## Search failures, limits and remaining unknowns

Two bounded eight-point random batches respectively gave no hit in 3,000
attempts (1,362 valid) and one hit by attempt 3,999 (1,805 valid). The hit
was simplified by hand to the small displayed coordinates. A seven-point
batch gave no hit in 200,000 attempts (127,088 valid); this is not an
exhaustive classification or a minimality proof. All three outputs remain
in `data/search/`, including the original larger-coordinate hit.

Five exploratory coordinate variants are in `data/development_variants.json`.
Two are collinear and invalid; neither was used for the conclusion. These
invalid controls and both bounded no-hit results are retained. No timeout,
OOM, solver UNKNOWN or omitted solver proof occurred. No pool-wide scan or
uniform-selection search was performed.

The proof does not classify global existence of uniform Deltas, rule out
the one-support selection rule on this particular set, prove minimality of
eight points, or change any weak Delta or ES bound. No Lean check is claimed.
