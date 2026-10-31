# Midpoint clauses for the compact encoding (exploratory, 2026-10-30)

**Result in brief.** The negative result below needed no proofs.
- **Implied.** The "parallel lines" condition of real central symmetry is already implied by the symmetric
  signotope axioms of `../sgn.py`.
- **No pruning.** Adding it as clauses does not prune the nested-parallelogram cases.
- **Side search.** It found no extension of the fourfold 28-point example by an antipodal pair.

## The condition

For a real set with p_{n+1-i} = -p_i, the centre c is the midpoint of every pair {r, -r}. Since p lies on the line
pq, c and -p are on the same side of that line. So for non-antipodal p, q and a pair {r, -r} disjoint from
{p, q, -p, -q}:

    chi(p,q,r) = chi(p,q,-r) = s  ->  chi(p,q,-p) = s.

Equivalently, the lines pq and (-p)(-q) are parallel, so no point lies beyond both of them.

`mid.py` writes these as 2 clauses per instance:
- 13,440 clauses for n = 32;
- 16,320 clauses for n = 34.

`mid.py check` confirms that the clauses hold on 183 random real centrally symmetric sets (n = 8..20) and on
`SYM2/sym7_32points.txt` and `SYMMAX/c4_28points.txt` (`logs/check.log`).

## The condition is already implied

**Lemma.** In a signotope with o(n+1-k, n+1-j, n+1-i) = -o(i,j,k) (the `--sym` relation), the condition above holds.

**Proof.**
1. **Sort the four points.** Sort p, -p, r, -r by x as w1 < w2 < w3 < w4. Negation reverses the x-order, so
   w4 = -w1 and w3 = -w2.
2. **Apply the symmetry relation.** It gives o(w1w2w3) = x, o(w1w2w4) = y, o(w1w3w4) = -y and o(w2w3w4) = -x.
3. **Apply the signotope axiom.** The sequence may change sign at most once, so x = y.
4. **Find the circuit.** The circuit on {w1, ..., w4} is
   (chi(w2w3w4), -chi(w1w3w4), chi(w1w2w4), -chi(w1w2w3)) = (-x, x, x, -x). So it separates the two antipodal
   pairs: X = (p+, -p+, r-, -r-), up to sign.
5. **Use orthogonality.** Let Y be the cocircuit of the line pq, so Y(p) = Y(q) = 0. On {-p, r, -r} the products
   X(e)Y(e) are (chi(p,q,-p), -s, -s). Circuits and cocircuits of an oriented matroid are orthogonal, so these products
   must include both signs. Hence chi(p,q,-p) = s.

Rank-3 signotopes are oriented matroids (Felsner and Weil, *Sweeps, arrangements and signotopes*, 2001), which is
what step 5 uses. The proof has not been independently reviewed.

**Solver check** (`implied.py`, `logs/implied.log`).
- Each instance is the base formula plus the negation of one random instance of the condition.
- All 84 instances are UNSAT.
- The settings are n = 10, 14 and 20, with and without the centre axioms and with and without the no-7-gon clauses.
- 36 of the instances use `--sym` alone.

## No pruning

- **32 points.** The formula is `../sgn.py 32 7 --sym --par --centre --rs`, which regenerates byte-identically
  (SHA-256 `d4f57255…`). Its quadrilateral second-layer cubes come from `../l2sgn.py`, and 26 of them survive the
  unit-propagation filter.
  - All 26 stay SAT in at most 1 s with the midpoint clauses (`logs/p32_nested_mid.jsonl`).
  - The earlier SAT model for cube Q3.4, found without the clauses, already satisfies all 13,440 of them
    (`logs/p32_Q3.4_model_viol.log`).
- **34 points.** The formula is the C2SGN formula (`3459d4c5…`) plus the clauses (`2bd8b2a5…`).
  - Six cubes that gave no answer in the certified runs were tried (`../logs/units.tsv`):
    - H3.5.24, H3.7.11 and H3.7.8, previously at 1,800 s;
    - Q3.11/Q4.9, Q3.11/Q4.16 and Q3.11/H4.10.29, previously at 1,200 s.
  - With the clauses, all six again gave no answer at a 600 s cap (`logs/s34_hard_mid.jsonl`).

## Side search: one more antipodal pair for the fourfold 28-point set

- **Search.** `addpairs.c` adds a pair (x, y), (-x, -y) with integer coordinates to `SYMMAX/c4_28points.txt` (seven
  convex layers, all quadrilaterals, coordinates up to 147). It keeps only additions in general position and computes
  the largest convex subset exactly, with an O(n^4) chain DP over the lowest vertex.
- **DP tests** (`logs/addpairs_dp_tests.log`). It gives 7 for a convex heptagon (`heptagon_test.txt`) and 6 for the
  two known examples.
- **Exhaustive result.** Every one of the 180,600 integer pairs with |x|, |y| <= 300 fails
  (`logs/addpairs_exhaustive_300.log`):
  - 7,380 break general position;
  - 132,026 give a largest convex subset of 7 points;
  - 41,194 give one of 8 points.
- **Random runs** (`run_addpairs.sh`, `logs/addpairs.log`). 5.1 million random trials in boxes 40–300 found no
  extension either.

So no 30-point centrally symmetric set without a convex 7-gon arises from c4_28 by adding an integer pair in this box.
This says nothing about non-integer positions or other 28-point sets.

## What this suggests (not tested)

The nested-parallelogram cases are hard for both encodings of `results/C2C34`. The abstract model has
nested-parallelogram solutions at 32 points; whether real ones exist is not known.

If those abstract solutions cannot be realized, a realizability step could prune the hard core at 34 points. Such a
step would check small abstract solutions for realizability and add a blocking clause for each obstruction found, as
in "satisfiability modulo realizability" (Krapivin, Przybocki and Heule, arXiv:2607.02958).

## Files

- **Scripts.** `mid.py` (clauses, real-set check, model check), `implied.py`, `run_cubes.sh` (one exploratory run per
  cube), `addpairs.c` (build with `cc -O2`), `run_addpairs.sh`, `heptagon_test.txt`.
- **Logs.** `logs/`.
- **Dependencies.** `cadical` is expected in `../../local/bin`, as for `../closesgn.py`.
- **Commands.**
  - `python3 mid.py add BASE.cnf MAP.json OUT.cnf`
  - `python3 mid.py check`
  - `python3 mid.py viol MAP.json MODEL.out`
  - `bash run_cubes.sh CNF CUBES OUTDIR CAP NAME...`
  - `addpairs BASE.txt 7 1 0 300 0`
- **Not committed.** CNFs, which regenerate with `../sgn.py`, `../l2sgn.py`, `../l3sgn.py` and `mid.py add`.
