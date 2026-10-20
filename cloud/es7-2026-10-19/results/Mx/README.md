# Task Mx: independent re-encoding of the mirror-symmetric 33-point class (20 Oct 2026)

Question (shared with C, C2, Mi-*, Mii-*): is there a set of 33 points in general position,
symmetric under a reflection, with no 7 points in convex position? This directory holds an
independent CNF encoding, its validation, and cube-and-conquer runs on it. Nothing here is a
theorem: the encoding is not formally verified. "Certified" below means only that every leaf
UNSAT was checked by lrat-check against the exact CNF solved, and that the cube set was shown to
cover the CNF (also LRAT-checked).

## Where it ran

- One cloud VM, x86_64, 4 vCPUs, 15 GB RAM, Linux 6.18 (`env.txt`). Started 02:53 UTC and wrapped
  up about 06:50 UTC.
- Tools were built from source: CaDiCaL 3.0.1 (git c607304), lrat-check from drat-trim (git
  head), and march_cu from marijnheule/CnC (git head; it needs `-fcommon` to link with gcc ≥ 10).
- Scripts are in `scripts/`. CNF and LRAT files are not committed; regenerate the CNFs with
  `python3 scripts/mxgen.py 33 7 --mode top|interior -o F.cnf` (sha256 in
  `logs/top33_sha256.txt`).

## Encoding (scripts/mxgen.py, written without reading gen_etv.py, mirgen.py or mirlib.py)

Points 0..n−1 are sorted by x. chi(i,j,k) for i<j<k is true iff the triple is counter-clockwise,
i.e. j lies below the chord ik (a "cup triple"). The axis is vertical, so the mirror sends point
i to point m−i with m = n−1; for n = 33 the axis point is a = 16.

**Mirror sign rule.** The task statement gives chi(m−k, m−j, m−i) = −chi(i,j,k). That is
wrong for an x-sorted signotope: the correct rule is **chi(m−k, m−j, m−i) = +chi(i,j,k)**.
The reflection reverses orientation, giving one minus sign:
orient(σi, σj, σk) = −orient(i,j,k). It also reverses the x-order, so re-sorting
(m−i, m−j, m−k) into (m−k, m−j, m−i) is an odd permutation and gives a second minus sign.
The two cancel. Geometrically, a reflected cup is still a cup. With the minus rule, the 16
self-mirror triples (i, a, m−i) would be forced to be zero, so every CNF would be trivially
UNSAT. The + rule was checked on every triple of all 10,000 validation sets (0 violations).
It agrees with the rule stated in results/C/README.md.

**Variables.** There is one variable per mirror orbit of triples: 2,736 orientation variables
for n = 33 (16 orbits of size 1 and 2,720 of size 2). This substitution is sound because it
is equivalent to adding the equality clauses.

**Signotope axioms.** For each a<b<c<d, the sign sequence (abc, abd, acd, bcd) may change sign
at most once. This is encoded by forbidding +−+ and −+− on every 3 of the 4 positions (8
clauses per 4-set; after deduplication across orbits, 163,440 remain for n = 33).

**No convex k-gon: the "anchored chain" encoding.** gen_etv.py has no-cap and no-cup
counters; this encoding is built differently. Take a convex k-gon with leftmost vertex p and
rightmost vertex q. Its lower chain is a cup p…q with s vertices, and its upper chain is a
cap p…q with t vertices, where s + t = k + 2 and s, t ≥ 2. The auxiliary variables are:

- U[p,j,q,ℓ]: "some cup of exactly ℓ vertices starts at p and ends with the pair j,q". It is
  defined one-directionally: chi(p,j,q) → U[p,j,q,3], and U[p,i,j,ℓ] ∧ chi(i,j,q) →
  U[p,j,q,ℓ+1].
- EU[p,q,ℓ]: the OR over j of U[p,j,q,ℓ], also one-directional.
- C and EC: the same for caps, with ¬chi in place of chi.

The forbidding clauses are ¬EU[p,q,s] ∨ ¬EC[p,q,t] for s + t = k + 2 with s, t ≥ 3, plus
¬U[p,j,q,k] and ¬C[p,j,q,k] (a k-cup or k-cap is itself a k-gon). Every auxiliary clause is
Horn with exactly one positive auxiliary literal. So for fixed orientations, the least model
is reached by forward chaining. The CNF is satisfiable iff that least model satisfies the
purely negative gon clauses.

*Soundness for point sets.* Take any real k-gon-free set and set every auxiliary variable to
"the chain exists". Every definition clause then holds. A violated gon clause would give a cup
p…q and a cap p…q with s + t − 2 = k vertices in total. The cup's inner points lie below the
line pq and the cap's lie above it, so together they form a convex k-gon, a contradiction.
Hence UNSAT implies that no such point set exists.

*Completeness.* A convex k-gon decomposes into a cup and a cap with the same endpoints, and
the propagation forces the corresponding variables to true. Both directions were tested
against an exhaustive brute force (see Validation).

**Case split and symmetry breaking (my own choice; soundness argument).**

- *Distinct x.* The projective map used in results/C is not needed. General position and "no
  convex 7-gon" depend only on the strict orientation signs, and those signs survive small
  perturbations. A mirror-symmetric perturbation (x, y) → (x + ε_P, y) applied to each pair,
  with ±ε on the two partners, therefore makes all x distinct while keeping the symmetry and
  every sign. The axis point stays at x = 0 and is the median point a = (n−1)/2.
- *y-reflection.* The map (x,y) ↦ (x,−y) keeps the mirror, the x-order, general position and
  convex position. It negates every chi and swaps cups with caps. Each CNF below, before its
  symmetry-breaking literal, is invariant under "negate all orientation variables, swap U↔C
  and EU↔EC".
- **Sub-case "top"** (the analogue of (i)): the axis point is a vertex of the upper hull. With
  a strictly between the leftmost and rightmost points, this holds iff a lies above every
  chord ik with i < a < k, which is the 136 unit clauses ¬chi(i,a,k) after orbit
  substitution. "Lower-hull vertex" is the y-reflection of "upper-hull vertex", so the
  y-reflection is spent here.
- **Sub-case "interior"** (the analogue of (ii)): the axis point is on neither hull. This is
  two clauses: OR chi(i,a,k) and OR ¬chi(i,a,k) over i < a < k. The interior class is closed
  under y-reflection, so one unit chi(0,1,2) = true is added without loss of generality.
- *Coverage.* In general position the axis point is an upper-hull vertex, a lower-hull vertex
  or interior. It cannot be both an upper and a lower vertex, because chord (a−1, a+1) has it
  on one side. So top ∪ y-flip(bottom) ∪ interior covers every 33-point mirror-symmetric set
  in general position.
- No other symmetry breaking is used. The x-reflection is the mirror itself.

Sizes for n = 33, k = 7 (all with 2,736 orientation variables):

| CNF | vars | clauses | sig | aux | gon | case/sym |
|---|---|---|---|---|---|---|
| top33 | 51,590 | 492,920 | 163,440 | 320,354 | 8,990 | 136 |
| int33 | 51,590 | 492,787 | 163,440 | 320,354 | 8,990 | 2 + 1 |

## Validation (scripts/validate.py, logs/validate_10k.json): passed, 0 errors

- **Sets.** 10,000 exactly mirror-symmetric integer point sets with n odd, uniform over 9..33 (about
  770 per n), each with one axis point, in general position and with distinct x.
  - 6,943 are random. Coordinate ranges run from 30 to 10^7. The axis point is forced to the
    top in a quarter of them and to the bottom in another quarter.
  - 3,057 are "structured": random mirror pairs taken from the mirror-symmetric classical
    32-point heptagon-free set (tools/decomp/mirror.py, rotated so the axis is vertical), plus
    one axis point.
- **Brute force (scripts/bfgon.c).** For each set, an exhaustive search over subsets in convex
  position with exact integer orientation tests gives the largest convex subset size L. Then k
  is drawn from {L, L+1}, plus k = 7 for structured sets, with k ≥ 4.
- **Checks on every set.** All passed on all 10,000.
  - The mirror sign rule holds on every triple.
  - The orbit variables are consistent.
  - Every signotope clause is satisfied.
  - The "top" clauses hold iff the axis point is an upper-hull vertex (hull computed
    independently by monotone chain). The "interior" clauses hold iff it is interior. The
    "sym" unit holds iff chi(0,1,2).
  - The no-k-gon clauses hold under the least model of the auxiliary clauses iff L < k.
- **Outcome mix.** 4,530 sets were k-gon-free and 5,470 contained a k-gon, with k from 5 to 19.
  - k = 7 gon-free: 324 sets, all with n ≤ 19.
  - n = 33, k = 7: 154 sets, all containing a 7-gon. So gon-free acceptance at n = 33 is tested
    only for k ≥ 8.
  - Axis position: top 2,861, bottom 3,283, interior 3,856.
- **CaDiCaL subsample.** 200 sets were also solved as the written CNF plus orientation units. All
  200 agree (90 SAT, 110 UNSAT).
- **Sets from results/C/sets** (`logs/extcheck_C_sets.jsonl`, `scripts/extcheck.py`): 26 sets
  checked, all agree.
  - Pentagon-free 8, hexagon-free 11, classical mirror 32, mirror32_axismin1, the 33-point
    near-miss with one heptagon (correctly rejected), and the 21 heptagon-free mirror 32-sets.
  - Two of those 21 (seeds 6101 and 7101) have a mirror pair sharing an x-coordinate. The first
    run on them reported a mismatch, because the x-sorted signotope is undefined there. After
    the mirror-symmetric perturbation described under "Distinct x" they are in general position,
    heptagon-free, and accepted. They are recorded with `perturbed: true`.

## Controls (logs/controls.jsonl): passed except one timeout

- **Mirror, required UNSAT.** (n,k) = (9,5), (17,6), (19,6), each in all four modes (none / all /
  top / interior): 12/12 UNSAT, every one LRAT VERIFIED.
- **Non-mirror Erdős–Szekeres.**
  - n=8, k=5: SAT, and the model passes the independent signotope brute force (scripts/sigcheck.py).
  - n=9, k=5: UNSAT, LRAT VERIFIED.
  - n=16, k=6: SAT, sigcheck ok.
  - **n=17, k=6: UNKNOWN after 3,000 s** (plain CaDiCaL, no symmetry breaking). This control was
    not completed.
- **sigcheck.py** decides "no convex k-gon" for a signotope in two independent ways that must
  agree: an exhaustive 4-point-convexity subset search, and a cup/cap chain enumeration. It was
  itself checked against bfgon on 60 real sets.

## Agreement with results/C on small cases (logs/controls.jsonl, kind = compare)

gen_etv.py was run as a black box: `--mirror` (C's "m") and `--hull --mirror` (C's sub-case (i),
"hm"), with A = U = K = k.

| n | k | Mx none | Mx top | Mx interior | C m | C hm |
|---|---|---|---|---|---|---|
| 5 | 4 | UNSAT | UNSAT | UNSAT | UNSAT | UNSAT |
| 7 | 4 | UNSAT | UNSAT | UNSAT | UNSAT | UNSAT |
| 7 | 5 | SAT | SAT | SAT | SAT | SAT |
| 9 | 5 | UNSAT | UNSAT | UNSAT | UNSAT | UNSAT |
| 9 | 6 | SAT | SAT | SAT | SAT | SAT |
| 11 | 6 | SAT | SAT | SAT | SAT | SAT |
| 13 | 6 | UNSAT | UNSAT | UNSAT | UNSAT | UNSAT |
| 15 | 6 | UNSAT | UNSAT | UNSAT | UNSAT | UNSAT |
| 13–25 (odd) | 7 | SAT | SAT | SAT | SAT | SAT |

- Every Mx UNSAT in this table has a verified LRAT proof.
- For every SAT row, five Mx models (seeds 0–4):
  - pass sigcheck (signotope axioms, mirror rule, no convex k-gon);
  - are accepted by C's `m` CNF as orientation units.
- Five C `m` models per SAT row pass sigcheck and are accepted by the Mx CNF. That is 45/45 each
  way.
- Hull-frame models were not cross-mapped, because C's hm frame uses a projective re-ordering.
- k = 7 at n = 27–31 was not compared (no time).

## n = 33, k = 7

- Cubes come from `march_cu -d 8` on each CNF: 256 cubes each, weight 1 in total, no
  march-refuted leaves. The top split took 707 s and the interior split 788 s.
- Each cube is solved as base CNF plus units by `cadical --lrat`, checked by `lrat-check`
  against exactly that file, and the proof is then deleted.
- The queue is FIFO and weights are exact.
- A cube that times out is re-split by march_cu (`-d 3`) on the cube-conditioned CNF.
- Leaf logs: `top33_leaves.jsonl`, `int33_leaves.jsonl`. Weight summaries come from
  `scripts/status.py <cubes> <leaves>`.

### Sub-case "top" (axis point is a hull vertex): 99.994 % of weight closed, 1 cube open

- **Root cubes.** 255 of 256 depth-8 cubes are UNSAT and LRAT VERIFIED. Median 23 s, max 485 s.
- **The hard root cube.** Cube −1314 −87 −1431 −1447 −536 −1462 −1476 −1489 timed out at 3,600 s
  and was re-split (depth 3) into 8 children.
  - 7 children are UNSAT and verified.
  - The child ending −1336 −928 −1414 timed out again and was re-split into 8 grandchildren.
    **7 are UNSAT and verified, and 1 depth-14 cube is still open** (weight 2^−14 = 6.1×10^−5
    of the sub-case).
  - Independently, that same child was re-split by hand with `march_cu -d 4` into 16 cubes
    (`top33_lastcube_children_d4.icnf`, `last_leaves.jsonl`). 15/16 are UNSAT and verified, and
    1 was still running at wrap-up.
  - A side depth-5 split of the hard root cube (`top33_hardcube_children_d5.icnf`,
    `hard_leaves.jsonl`) was stopped once the main run overtook it; 23 of its 32 cubes are
    UNSAT and verified.
- **Totals.** 269 leaves are UNSAT and LRAT VERIFIED in the main tree, with no failed check and no
  SAT leaf. That is 5.3 solver-hours, 9.7 GB of LRAT checked, and 295 s of checking. The
  largest proof was 408 MB.
- **Coverage check not run.** The check that the base CNF plus the negations of all leaves is
  UNSAT (`scripts/cover.py`) was **not run**, because one leaf is open. Until that check and the
  last leaf are done, this sub-case is "99.994 % of cube weight closed", not certified.

### Sub-case "interior": 2.7 % of weight closed

- 7 of 256 depth-8 cubes are UNSAT and LRAT VERIFIED, with no SAT. Each cube took 1,500–2,736 s,
  with LRAT proofs of 1.5–2.0 GB. That is 3.8 solver-hours.
- 249 cubes are open. At this rate the interior sub-case needs about 130 core-hours with this
  encoding and this cubing. A finer cube split, or the orbit/lemma strengthening that results/C
  uses, would probably be needed.

### SAT models

None were found in any run.

## Caveats

- The encoding is unverified. The links that are argued above but not formally proved are:
  the signotope axioms, the one-directional chain auxiliaries, the mirror rule, the hull and
  interior clauses, and the y-reflection unit. Everything is tested, not proved.
- During the run, a `git pull --rebase` at 03:41 replaced the live leaf files under the drivers.
  The drivers kept appending to the unlinked inodes. Those records were recovered intact from
  `/proc/<pid>/fd` (204 top leaves and 1 interior leaf), and the live files were moved to /tmp.
  The controls run from before then was lost and re-run from scratch; the re-run is what is
  reported.
- Timings are wall-clock on a 4-vCPU VM, usually with 4–5 processes running.

