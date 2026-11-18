# Independent boundary audit — confirmed within the stated scope

**PROVED:** the written cup-rank, endpoint, `2n-3` extreme-root, and
`2n-2` localization arguments in `../../structure/theory.md`, Sections 1–4,
are valid for real points in general position with distinct x-coordinates,
n>=6. **CERTIFIED:** all three terminal-boundary CNFs passed independent
cake_lpr replay. Their geometric interpretation and coverage are justified
below. **COMPUTED:** the independent exact controls pass. No formal Lean
check, general-size Delta theorem, or new ES bound is claimed.

## Written arguments and signs

For a<b<c, positive determinant means increasing consecutive slopes (cup);
negative means decreasing slopes (cap). Consecutive monotonicity implies
the same sign for every triple, by weighted-average secant slopes.

1. If a,b,c is a cap and beta(a)>=beta(b), then beta(a)>=2 because b has
   a two-point cup. A longest cup ending p,a cannot extend by b, so p,a,b
   is a cap. Its slope inequality combines with a,b,c to give the ambient
   four-cap p,a,b,c. Thus h(b,c)>=4, with the inequality direction as written.
2. In a five-cap-free U, a selection with nonincreasing beta has no
   four-cap: a hypothetical a,b,c,d would extend an ambient four-cap ending
   b,c by d. The identical argument prevents a new cap a,b,c,r when r is
   rightmost. A single beta-level is therefore terminal-safe and extendible.
3. A convex (n-1)-gon has upper/lower chain lengths summing to n+1.
   No five-cap bounds the upper length by four. If there is no (n-2)-cup,
   the lower length and the right endpoint's ambient beta both equal n-3.
   The endpoints form one safe rank level and hit every old target.
4. If |S|<=2n-3 and U=S-r contains an (n-2)-cup C, then |U-C|<=n-2.
   C hits every target. C plus any one point is four-cap-free because a
   four-cap would contain a triple of C. Otherwise use the endpoint case.
5. At |U|=2n-3, failure of terminal-safe selection forces maximum cup
   length exactly n-2: shorter cups invoke the endpoint result, and a
   longer cup has a small enough complement. Every maximum cup must leave
   its entire (n-1)-point complement convex. Upper chain length two would
   force an (n-1)-cup; lengths above four are forbidden. The remaining
   upper/lower pairs are (3,n-2) and (4,n-3). This argument needs neither
   an added root nor a no-n-gon premise. It supplies necessary conditions,
   not their impossibility.

The leftmost reflection is sound with an explicit change of ranks.
For R(x,y)=(-x,y), sorted reflected triples are R(c),R(b),R(a), and
det(R(c),R(b),R(a))=det(a,b,c): reflection and order reversal cancel.
Caps and cups are preserved, but ending cup ranks become starting cup
ranks, and terminal pair safety becomes initial pair safety. The rooted
existence conclusion reflects; the same ending-rank labels cannot simply
be reused. This is a clarification, not a gap in the stated bound.
The displayed projective normalization in Section 7 also has the corrected
sign: a cap through r corresponds to positive transformed edge slope.

## Encoders and coverage

The inherited geometry is unchanged. Its ordered four-point sign sequence
has at most one change for real points. On these eight patterns, the
convex-four clauses are equivalent to a=b and c=d. A nonconvex set has a
nonconvex four-subset (triangle containment). Among five distinct deleted
vertices, one is outside that witness; hence the five-child convexity
recurrence and no-n-gon clauses are sound. Consecutive negative turns in
the no-five-cap clause characterize a five-cap.

`complement.cpp` adds exactly: all-triple cup equivalences, some
(n-2)-cup, no (n-1)-cup, and convex complements for every (n-2)-cup.
The old universe has 2n-3 points in both modes. Root mode adds the last
point only to the geometric base. Own compilation regenerated all six
base CNFs and maps byte-for-byte. The new families were reconstructed
independently as literal multisets.

`refine.py` preserves every parent clause and appends precisely the
negative-all-triple rows for (n-1)-subsets containing the root. Together
with the old no-longer-cup rows, this forbids every full-set (n-1)-cup.
The justification is valid: augment such a cup to n selected points,
using the root if absent or one arbitrary outside point if present. The
selection is a cup plus one, contains the root, and leaves only n-2 points.
The refined models show that this extra necessary condition still does
not imply failure of rooted Delta.

`terminal_boundary.py` starts from the **old** obstruction CNF; it does
not depend on the root refinement. Its four-cap flags are exact
conjunctions of the four negative triple signs. A bad-triple flag is true
exactly when a<b<c is a cap and no ambient four-cap ends at b,c.
Under no five-cap, absence of bad triples is equivalent to terminal safety:
any four-cap a,b,c,d would have a bad prefix triple, since an ambient
four-cap ending b,c would extend by d to a five-cap.

For each A of size 0 through m-n+2 inclusive, the final row says that A
contains a bad triple or its complement contains a convex (n-1)-gon.
All sizes 0,1,2 really occur. A larger terminal-safe solution can be shrunk
to m-n+2: safety is hereditary and the new complement has n-2 points, so
coverage is automatic. No unsafe assumption about growing a small
terminal-safe selection is used. Every added row was independently
reconstructed, and all inherited clauses and mappings were compared.

**Consequence:** for n=6,7,8, every five-cap-free, n-gon-free old set U
with |U|<=2n-3 (respectively 9,11,13) has a terminal-safe weak Delta.
Smaller sizes follow from the written dichotomy; a boundary failure
would satisfy the certified-unsatisfiable formula by localization.
Adding any rightmost r which preserves five-cap-freeness gives a rooted
weak Delta, even if the enlarged set acquires an n-gon. The no-n-gon
premise on U remains required at the new boundary size.

## Independent certificate replay

| n | old points | variables | clauses | replay seconds | receipt |
|---|---:|---:|---:|---:|---|
| 6 | 9 | 672 | 5,675 | 0.007 | [full hashes](data/replay-n6.json) |
| 7 | 11 | 2,376 | 23,135 | 0.099 | [full hashes](data/replay-n7.json) |
| 8 | 13 | 8,437 | 97,047 | 3.158 | [full hashes](data/replay-n8.json) |

All three fresh logs contain the **exact line** `s VERIFIED UNSAT`.
CNF, LRAT, and checker hashes were taken before and after each replay and
are unchanged. Exit status alone was not used. Original and compressed
proofs remain in the parent's scratch record; no proof was modified.
The root/old obstruction SAT results and refined SAT results are distinct
from these three UNSAT certificates. UNKNOWN is used nowhere as evidence.

## Independent exact controls and limits

`check.py` imports no parent encoder, finder, or earlier checker. It uses
integer determinants, monotone hulls cross-checked by triangle containment,
direct subset cup/cap ranks, and exact rational projective identities.

- All 272 general-position six-point permutations pass: 235 rank-lemma
  premises, 1,632 terminal-rank-three triples, 2,705 nonincreasing-rank
  selections, 5,440 reflected triples, and 4,080 four-point cross-checks.
  The bounded construction passes 114 cup and 138 endpoint cases, including
  40 nonempty endpoint cases. Twelve additional boundary-size-prefix
  constructions check both extreme-root directions on the supplied sets.
- All six frozen original/refined coordinate sets satisfy their exact
  signs, no five-cap, no n-gon, and the cup/complement obstruction. The
  original/refined counts of maximum old cups are 6/6, 5/5, 6/6 at n=6,7,8;
  every complement has upper/lower lengths (3,n-2). Full maximum cup lengths
  are n-1 in the originals and n-2 in the refinements.
- Their canonical assignments satisfy every relevant base and equivalence
  clause. Original coordinates fail the root-refinement rows as expected;
  all six old sets fail terminal nonexistence rows as expected.
  Cup/cap parabolas test reversed orientation and missing-cup/too-long-cup
  rejection. A raised middle point gives explicit failed convex-complement
  rows. These adversarial parabolas intentionally violate no-n-gon; they
  are clause controls, not valid-instance counterexamples. Both directions
  of the cup equivalence are tested by flag mutations.
- Wrong rank-inequality direction and treating reflected ending ranks as
  ending ranks both have explicit rejected examples in `data/small.json`.

One audit provenance lookup initially used the wrong ancestor directory;
the resulting FileNotFoundError was corrected and affected controls rerun.
The unused renamed legacy main emits a compile warning. Details are in
`data/failures.json`; there was no mathematical control failure, timeout,
OOM, or rejected certificate.

Every source/control job used one CPU, AS400 MiB (compile AS500 MiB),
external 20 seconds. Replays used the parent's explicit one-CPU AS800 MiB,
heap600/stack32 allocation, each with external 20 seconds. Maximum observed
control RSS was 76,456 KiB; cake maximum was 622,648 KiB. No long unit was
started by this track. No prior record/shared manifest, root document,
Lean file, git state, installation, or external service was changed.

Only the statements and files listed here were audited. No independent
review of other tracks' new envelope or parametric-family proofs is claimed.
Source/input hashes and the scoped manifest are recorded alongside this
report. Reproduction commands are in [README.md](README.md).
