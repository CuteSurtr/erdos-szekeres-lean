# Exact controls of the rightmost-point lemma

**COMPUTED, exact integer controls; not order-type exhaustion.** The
written proof is [ROOTED_LEMMA.md](ROOTED_LEMMA.md). No solver, CNF or
certificate checker is used in these controls. The consequence chain
uses the separately owned, independently audited finite certificates.

The checker uses an expanded integer determinant, monotone-chain convex
hulls, and exact cup/cap dynamic programming. Every target of the stated
size is explicitly enumerated. It checks the prescribed B is a cup,
each nonfirst B vertex has an ambient three-cap ending there, and B meets
every target. A separate fixed-endpoint upper/lower-chain DP checks the
maximum polygon of the full set and of B's complement. For sets of size
at most8 that DP is compared with exhaustive convex-subset enumeration.
No parent checker, frozen checker, or producer is imported. The second
small driver imports only this packet's own unchanged checker.

## Named controls

Sixteen initial controls cover n=5,6,7,8 in each of four families:

* A pure (n-1)-cup. The selected penultimate singleton has no End3 witness;
  this checks the essential first-vertex exception.
* A single (n-1)-gon with upper chain three and lower chain n-2. The root
  has End3, and B is the root alone.
* The recursive cup/cap construction with maximum cup n-2 and cap3.
  The root has End3, and the prefix has internal targets with nonempty E.
* The preceding construction with a sufficiently high rightmost singleton.
  Long cups are now present, the root has no End3, and the selected top
  prefix rank hits both old and new targets. These examples have sizes
  7,11,16,22 and 19,101,616,4327 targets, respectively.

Four additional controls put a point (6,4k-1) inside the k-cup
{(4i,4i^2):0<=i<k}, where k=n-1. They have a long cup, the root has End3,
and every long cup contains the root. This makes Case 1 nonvacuous even
when the earlier global absent-long-cup hypothesis fails. All20 named
sets satisfy the no-four-cap/no-n-gon premises; n5 and n8 are included.

The initial16 controls take0.646s, peak17,768KiB. The extra four take
0.001s, peak17,200KiB. Full coordinates, selectors, endpoint sets, ranks,
maxima and target counts are in `data/rooted_named.json` and
`data/rooted_longcup.json`.

## Bounded grid

The n5 grid uses m=1,...,7, x_i=i, y0=y1=0 when present, and every other
y_i in [-3,3]. All19,609 candidates are visited:3,364 are GP,888 have no
four-cap, and432 also have no four-cup after deleting the rightmost point.
All432 pass the prescribed construction:395 have root End3 and37 do not.

Of these432,202 have no five-gon and hence are controls in T5's domain.
The other230 still test the stronger geometric lemma, which does not
assume no n-gon; they are not counted as admissible T5 examples. In total
274 eligible sets have a four-cup. This is a finite normalized grid, not
an exhaustive search of real order types. It completes in0.158s with
peak16,840KiB. Detailed counts and branch examples are in
`data/rooted_grid.json`.

## All-cap controls and parent replay

The later all-cap request adds24 fixtures and68 prescribed selectors
at n5,n6,n7,n8. It checks every choice of the one selected left point
in the two non-singleton cup blocks, plus both singleton directions.
The singleton-right fixtures use explicit Option1 witnesses, without
assuming an unproved all-size T8 theorem. The largest control has23
points. Every crossing sign, full premise, selected four-cap exclusion,
terminal-pair witness and target hit is recomputed exactly. All pass in
1.002s, peak18,412KiB, in `data/all_cap_controls.json`.

The parent independently checked all68 selections in3.069s, PASS, in
[all-cap-parent-controls.json](../../data/all-cap-parent-controls.json).
Its input hash identifies this packet's exact output. The parent also
reported a careful written review of the all-cap and rightmost-point
proofs as sound. These reviews do not constitute an encoder audit.

## Resources and reproducibility

The first CPU preflight printed12 free research threads; the later
all-cap preflight printed14. All four runs were
sequential, pinned to CPU3, AS150MiB, CPU18s, external wall20s. Each
completed within1.002s; no long unit or additional reservation
was created. The exact commands are in `data/commands.txt`. Each driver
requires a new output filename and records failures before re-raising;
all four retained outputs are PASS, with no partial grid or failed run.

Controls are evidence against implementation or boundary-case mistakes;
they are not the proof of the lemma and do not establish unrestricted
geometric T_n. No claim here changes an old frozen record.
