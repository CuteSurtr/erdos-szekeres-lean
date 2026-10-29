# Independent adversarial review of the axis-point extension (2026-10-29)

**Scope.** The 33-point mirror proof uses `zcnf.py mirror 16 7 --axis 1`. Two earlier audits checked only the
axis-free branch (`zcnf_v1.py`), so this review covers the axis-point extension of `zcnf.py`. It was asked to refute
soundness: to find any clause that a real reflection-symmetric 33-point set in general position with one axis point,
labelled in the normal form, could violate.

**Verdict: sound.** No clause can be violated by such a configuration except the clauses forbidding a convex 7-gon.

**Points checked by hand.**
- `flip` fixes the axis point. The reflection is diag(1, −1, 1) with determinant −1 and sends Z to −Z. So triples of set
  points change sign, triples containing Z keep it, and the axis point changes neither. The 16 triples {left, right,
  axis point} map to themselves with multiplier +1, so there is no contradiction.
- `is_zero` is restricted to pair points. An axis point at the height of a pair would be collinear with it. The map lists
  C(34,3) − 16 = 5,968 triples.
- The centre identity v_right − v_left = 2|x| v_Z holds for every third vector, including the axis point. It needs the
  left point to have x < 0, which is the labelling used.
- Acyclicity holds: w + εx is 1 on the axis point and ε on Z.
- The 16 Grassmann–Plücker patterns of the fast path were checked by hand. The generic path enumerates the cases
  exactly.
- The sign algebra of the union-find, including path compression, is correct.
- Orbit reduction only drops clauses, and the reflection preserves convex position.
- The normal-form units are valid, since pair heights are distinct.
- The K-gon clauses range over all 33 points. The counts 20,520 / 118,728 / 554,064 / 2,136,304 and the 2,616 triple
  classes match independent hand counts.

**Computations** (scripts in `review/`).
1. **Regeneration.** The current `zcnf.py` regenerates a clause body byte-identical to `m_t16k7a1.cnf`, with an
   identical variable map. The solver log shows that this file was the one refuted.
2. **Independent checker** `review/indep.py`. It is exact-integer and does not use `zvalidate.py` or `zrandtest.py`:
   - it labels real sets and checks the zero pattern and the consistency of every identified class;
   - it numbers the convexity variables independently and sets them to actual convexity;
   - it evaluates every clause, and accepts a violated clause only if it is the clause of a 7-set really in convex
     position.
3. **Small instances.** t = 3..6 and K = 5..7, about 370 sets. Axis-point positions included top, bottom, near a pair's
   height, and near-equal pair heights. There were no failures, and the sets without a convex K-gon satisfied every
   clause.
4. **The real 33-point CNF** (`review/evalcnf.c`). 13 real configurations were tested: 6 random, and 7 built from the
   7-gon-free 32-point mirror set plus an axis point at different heights.
   - Every Grassmann–Plücker, acyclicity, convexity-definition and normal-form clause was satisfied.
   - Every violated clause was the clause of a 7-set really in convex position.
5. **Mutation tests.** Five deliberately broken generators were tried: reversed centre identity, wrong GP sign, wrong
   acyclicity sign, reversed normal form, and wrong sign on axis-point triples. The checker caught all five. Flipping
   either group sign was also caught by the generator's own contradiction check.

**Minor notes (no effect on the result).**
- `tau()` in `zcnf.py` does not know about axis points. All current call sites are guarded.
- `val_real.sh` has no real-set test with exactly one axis point. The independent checker above covers it.
