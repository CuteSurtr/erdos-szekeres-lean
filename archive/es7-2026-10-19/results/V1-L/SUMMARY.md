# V1-L summary: mirror sub-case (i)

## The statement

Lean, package `V1L` (this directory), on top of `results/H3` and `results/H`:

```lean
theorem V1L.hullVertexLine_of_leaves
    (h : ∀ c ∈ hullLeaves, ¬DimacsSatisfiable (cubeCnf (hullCnf 33 7) c)) :
    ∀ (S : Finset Point) (a u c : Point), u 0 ^ 2 + u 1 ^ 2 = 1 → GeneralPosition S →
      S.card = 33 → (∀ q ∈ S, reflLine a u q ∈ S) → c ∈ S → reflLine a u c = c →
      c ∉ convexHull ℝ (↑(S.erase c) : Set Point) → HasConvexNGon 7 S
```

In words: let `S` be a set of 33 points in general position that is symmetric in some line,
with `c ∈ S` on the line and `c` a vertex of `conv S`. Then `S` contains 7 points in convex
position. The y-axis form is `V1L.hullVertexY_of_leaves`.

- The only hypothesis is the family of 1,198 per-cube UNSAT facts. `hullLeaves` is
  `verify/hull_leaves.icnf` (sha256 `cc11270a…2478b6`) as Lean data.
- The cover fact `coverCheck hullLeaves = true` is **proved in the kernel** (`decide +kernel`,
  no axioms). It is not a hypothesis.
- `#print axioms V1L.hullVertexLine_of_leaves`: `[propext, Classical.choice, Quot.sound]`.

## Status of the hypothesis

Checked at 06:38 UTC on 20 Oct 2026 with `scripts/check_siblings.py`. Output:
`logs/sibling_check.json`. Criteria: for every line `i` of `hull_leaves.icnf` there is a
record with that index and the same cube, solver exit 20, and cake_lpr `s VERIFIED UNSAT`
(cake exit 0 where the record has that field).

**All 1,198 leaves have such a record. There are no gaps, no SAT results, no checker
rejections and no cube mismatches.**

| leaves `i mod 4` | count | records from | solver exit 20 | cake_lpr `s VERIFIED UNSAT` | patched lrat-check | CaDiCaL s | cake_lpr s | largest proof |
|---|---|---|---|---|---|---|---|---|
| 0 | 300 | V1-0 (complete) | 300 | 300 | 300 `c VERIFIED` | 5,058 | 1,075 | 189 MB |
| 1 | 300 | V1-1: 9; V1-L backup: 291 | 300 | 300 | 9 (V1-1 only) | 1,481 + 5,259 | 142 + 917 | 255 MB |
| 2 | 299 | V1-2 (complete) | 299 | 299 | 299 | 6,981 | 1,305 | 239 MB |
| 3 | 299 | V1-3 (complete) | 299 | 299 | 299 | 7,363 | 1,169 | 242 MB |

**V1-1 did not finish.** Its last push, at 04:57 UTC, had 9 of its 300 leaves, and it had not
pushed again by 06:07 UTC. So this VM checked the other 291 V1-1 leaves itself
(`backup_v1-1/`, 06:08–06:38 UTC). Details:
- driver `scripts/backup_leaves.py`, run in reverse order, skipping leaves V1-1 had already
  verified;
- the same per-cube file construction as `results/H3/scripts/check_cubes.sh`, on the
  Lean-generated `hm33k7.sub.cnf` (sha256 `bfbc2d60…757d`);
- CaDiCaL 3.0.1 (c6073042) and cake_lpr a36874a8 (`cake_lpr.S` sha256 `2f3af32d…72b7d4a`),
  built here, see `backup_v1-1/tools.txt`.

The two record sets are disjoint and together cover all 300 leaves with `i mod 4 = 1`. The
backup ran cake_lpr only, so those 291 leaves have no second check by the patched
lrat-check. cake_lpr is the trusted checker in any case. The live file
`backup_v1-1/leaves_cake.jsonl` is not committed; `leaves_cake.snapshot.jsonl` is its final
copy.

V1-1's 9 records spell the verdict `"VERIFIED UNSAT"`. Its `run_leaves.py` writes that string
exactly when cake_lpr's output contains the line `s VERIFIED UNSAT`, so it is accepted.

So the hypothesis of `V1L.hullVertexLine_of_leaves` has been established outside Lean, on the
trust base below. Its conclusion is sub-case (i).

## Trust base

To read the Lean theorem as "sub-case (i) holds", one must trust:

1. **The Lean kernel** (4.24.0), and the definitions:
   - `Point`, `GeneralPosition`, `ConvexPosition`, `HasConvexNGon` (parent repository);
   - `reflLine`, `convexHull` (Mathlib);
   - `DimacsSatisfiable` (results/H, plain DIMACS semantics);
   - `cubeCnf`, `hullCnf`.

   Everything between these definitions and the conclusion is kernel-checked, including
   the soundness of `hullCnf` (H3) and the cover of the leaves.
2. **DIMACS string emission** in `results/H3/MirrorEncoding/Emit.lean`, which is unverified. It
   turns the Lean term `hullCnf 33 7` into the file `hm33k7.sub.cnf`. Here it produced a file
   with sha256 `bfbc2d60…757d`, byte-identical (`cmp`) to the independent Python generator
   `results/C/scripts/make_cnfs.sh` (`logs/mir_dimacs_hull.log`).
3. **The CNF identity via sha256.** The sibling runs regenerated `hm33k7.sub.cnf` themselves and
   checked the same sha256. Each per-cube file is that CNF with its header count raised by
   `|c|` and the unit clauses of `c` appended. That is the DIMACS text of
   `cubeCnf (hullCnf 33 7) c = hullCnf 33 7 ++ c.map (fun z => [z])`. The drivers' unit-clause
   appending is unverified Python. The cube recorded in each sibling record equals line `i`
   of the cube file (`scripts/check_siblings.py`), and `hullLeaves` equals the file
   (`lake exe leaves_eq`, regeneration + `cmp`).
4. **cake_lpr's verdicts on the 1,198 per-cube files.**
   - cake_lpr a36874a8, `cake_lpr.S` sha256 `2f3af32d…72b7d4a`. It is verified in HOL4/CakeML
     down to x64; the trusted remainder is `basis_ffi.c`, gcc/ld and the OS.
   - Each verdict `s VERIFIED UNSAT` is read as `¬DimacsSatisfiable (cubeCnf …)`, under the same
     standard DIMACS semantics on both sides.
   - The verdicts were produced in other VMs (V1-0..3) and are taken from their logs. CaDiCaL
     and the patched lrat-check are not trusted.

Not trusted: CaDiCaL; the compiled `cover_check` (the cover is in the kernel); drat-trim's
unpatched `lrat-check` (unsound, `results/E2/logs/lrat_check_soundness.md`); the Python
encoders, except as the second side of the byte comparison.

## What remains

- **Sub-case (ii)**: the axis point is interior to `conv(S ∖ {c})`. This needs
  `¬DimacsSatisfiable (interiorCnf 33 7)` (`m33k7int.sub.cnf`, sha256 `69c1dc8f…932d`). H3's
  `Mir.mirrorExclusionLine_of_cubes` combines it with sub-case (i) into the full mirror
  statement `Mir.MirrorExclusionLine`. At H3's time it was far from closed (C2: 1,340 open
  cubes, weight 0.364), and this run did nothing on it.
- **The 3-fold (rotational) symmetry class** of the ES(7) programme is a separate class. Nothing
  here bears on it.
- Importing the cake_lpr verdicts into Lean. They stay a hypothesis of the theorem (an
  in-kernel LRAT check of ~10⁹ proof bytes is out of reach, per results/H and H2).
