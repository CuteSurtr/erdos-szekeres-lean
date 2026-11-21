# VERIFY D-satg-descents, lens SOUNDNESS AND SEMANTICS (independent verifier, 22 Nov 2026, 00:05-00:20 KST)

**Status: DONE. All four claims confirmed at their stated labels.** Nothing is rounded up. The wording points in
section 8 do not affect any bound. I had no compute slot. Every run of my own code took less than 2 CPU-seconds
(the largest: 1.85 s and 64 MB). Scripts, logs and controls are in `verify/sound/`.

| claim | label claimed | verdict | basis (details below) |
|---|---|---|---|
| satg6-le-11 | EXACT | **confirmed** | Convention matches DDSZ; the reduction is sound. Logs of 3 implementations (the vx1118 pair, VX2, satcheck; hashes match). I found no log of the worker's `satcheck_big.py`; my re-run of it says SATURATED (1,145 cells). My own code checks everything from the points file alone, including my own cell enumeration with no samples used: 0 of 1,145 cells fail |
| satg8-le-26 | EXACT | **confirmed** | Logs of 3 implementations (hashes match). My own C++ replay: general position; convex subsets 2,600 / 8,299 / 9,557 / 3,929 / 497 / **0**; own Euler F = 45,800; 45,800 distinct samples, all on no line, all witnesses verified |
| satg9-le-39 | EXACT | **confirmed** | Logs of 3 implementations (hashes match). My own C++ replay: general position; convex subsets ... / 1,140 / **0**; own Euler F = 248,938; 248,938 distinct samples, all witnesses verified |
| point-adjacent-cell-lemma | PROVED | **confirmed** | I checked the written proof step by step: it is correct, for K >= 4. My own sector-by-sector test on 12 states found 0 mismatches. My counts equal the worker's figures on the 11 listed states I re-ran |

## 1. Problem convention (semantics)

DDSZ, arXiv:2312.01223 v3, section 1.3, read from the arXiv LaTeX source:
- "A planar point set P is n-gon-saturated if it is n-gon-free while any q ∉ P with P ∪ {q} being in general
  position is part of an n-gon in P ∪ {q}. Denote by sat_g(n) the smallest size of an n-gon-saturated set."
- n-gon-free means "containing no n points in convex position".
- Section 1.2 says "general position (meaning without three collinear points throughout this paper)". The extra
  "distinct x-coordinates" condition belongs only to their "generic" sets (cups and caps). It is not part of sat_g.

Comparison with the claims:
- **"Convex n-gon" means n points in convex position.** Empty polygons (holes) are not meant. Every checker tests
  convex position (4-point test, hull size, DP); none tests emptiness. This matches DDSZ.
- **P in general position.** DDSZ's sentence does not literally require P itself to be in general position. Without
  that requirement, any non-general-position set would be saturated vacuously. The record (section 2) and the
  intended reading require it. All claimed sets are in general position (0 collinear triples, checked by me), so they
  meet both readings.
- **Which q are tested.** q ∉ P with P ∪ {q} in general position means q lies on no line through two points of P.
  The points of P are vertices of the arrangement, so they are excluded automatically. These q form exactly the union
  of the open 2-cells of the arrangement of the C(N,2) lines. Every checker quantifies over exactly these cells, and
  unbounded cells are included (they are counted in F).
- **"Part of an n-gon".** P is n-gon-free, so every convex n-subset of P ∪ {q} contains q. This equals "q is a vertex
  of a convex n-gon of P ∪ {q}", the predicate the checkers decide.
- **sat_g(n) is a minimum.** One saturated set of size m gives sat_g(n) <= m. This is all the claims assert.

## 2. Soundness of the reduction (record section 3 (II), used by every checker)

- **One sample per cell is enough.** On an open cell every orient(a, b, q) keeps a fixed nonzero sign (the cell is
  connected and misses every line). So the order type of S ∪ {q} is constant on the cell. Convex position of a set
  in general position depends only on its orientations. DDSZ use the same cell argument in their section 5.
- **Completeness.** The insertion argument gives F = 1 + L + Σ_v (k_v − 1). A line that meets the earlier lines in
  m distinct points adds m + 1 faces. A vertex with k lines is counted once by each of its k − 1 later lines.
  Parallel lines never meet. This holds for non-simple arrangements too.
  - F samples on no line with pairwise distinct sign vectors lie in F distinct cells, so they meet every cell.
  - The only risk is a wrong F. Merging two distinct vertices would undercount F and could hide a cell. Each
    implementation groups vertices by exact rational equality. Mine does the same, independently.
- **Witnesses.** A pass needs a (K−1)-subset T of S with T ∪ {q} in convex position, checked by definition (4-point
  test or exact hull size). A SATURATED verdict therefore does not need the list of convex (K−1)-gons to be complete.
  Completeness matters only for "no convex K-subset of S". That rests on brute force (K = 6 and 8: all subsets; K = 9:
  VX2 over all C(39,9) and C(39,8)) and, independently, on hereditary DFS growth plus DPs.
- The record's argument and the claims use the same definitions. I found no gap.

## 3. Code reading of the two implementations the claims rest on, and provenance

- **Record replay `check_cells.py`** (`4b6cd648…072d`, unchanged; read in full).
  - Part (a): it counts collinear triples and computes the largest convex subset by a DP over the lowest vertex. The
    angular order is asserted, and the closing and first turns are automatic because all points lie in a half-plane
    of angle < π.
  - Part (b1): exact Fraction intersections, with the assertion that each group holds C(k,2) pairs, then F.
  - Part (b2): for every sample, QD > 0 is asserted. All L values of QD·orient are computed exactly, a zero counts
    as bad, and a repeated sign vector counts as bad.
  - Part (b3): T has K − 1 distinct in-range indices, and the exact hull of T ∪ {q} must have K vertices.
  - Verdict SATURATED only if bad = 0, samples = distinct = F, and no sample is tagged F.
  - This is sound.
- **Worker's fresh checker `check/satcheck.cpp`** (`06cfa5fc…`; read in full).
  - Coordinates are bounded by 2^30, so all __int128 products stay below 2^126.
  - Convex subsets: grown in index order with the "exactly one visible edge" test. This is complete, because convex
    position is hereditary and, for a convex polygon P and a point z on none of its edge lines, P ∪ {z} is convex iff
    z sees exactly one edge. Every (K−1)-gon is re-verified by the 4-point test. A separate DP gives the largest subset.
  - Cells: for every line it builds both sides of every edge. The sign of another line m on the edge is
    sign(d_m)·(± by rank), from f_m(t) = d_m (t − t_m), which I verified by hand. Every face has an edge on its
    boundary, so all cells are produced by construction, and C = F is a cross-check.
  - Pass: a 4-point test on the cell's exact chirotope. The rotations orient(q,b,c) = orient(b,c,q) and
    orient(a,q,c) = orient(c,a,q) are correct.
  - This is sound.
- **Provenance.**
  - All 5 point files, the 3 sample files, both checker sources and binaries, and the record binaries `a0495961…`,
    `da8750d1…` and `3537f493…` match the hashes in `SHA256SUMS` and in the claims.
  - The `runs/<name>/found_*.txt` files named in the logs are byte-identical to the `found/` files.
  - `bin/satcheck` (mtime 20:36) is older than the last write of `check/satcheck.cpp` (21:48). I rebuilt the current
    source with the README's flags. The result has SHA-256 `fd44f84d…`, **bit-identical** to `bin/satcheck`. So the
    source hash does correspond to the binary that wrote the logs.
  - The rebuild reproduces `fresh.log` (11 points) and `logs/fresh_k8_n26_k8b_rebuilt.log` (26 points) line for line,
    apart from the input-path line.

## 4. My own exact checks (own code; exact integers and Fractions only)

Two programs, written for this check. They share no code with satcheck, satcheck_diag, satcheck_big, satcells,
check_cells.py, vx2sat or the finders:
- `sound/sound_check.py` (Python; modes `full`, `lemma`, `spot`);
- `sound/replay.cpp` (C++, __int128 with explicit bounds: coordinates < 2^24, sample numbers < 2^70, all products
  < 2^122).

The sample files are the record finder's output. My replay treats them as untrusted input and checks everything the
claim needs.

| check | 11 pts K=6 (k6a) | 26 pts K=8 | 39 pts K=9 |
|---|---|---|---|
| general position (all triples) | 0 collinear | 0 | 0 |
| convex subsets | brute force: 146 quadrilaterals, 22 pentagons, **0** hexagons | own DFS (C++ and Python agree): 2,600 / 8,299 / 9,557 / 3,929 / 497 / **0** | own DFS: 9,139 / 44,021 / 77,117 / 53,383 / 14,010 / 1,140 / **0** |
| own vertices, F | 1,001 (990 simple, 11 of mult. 10), **F = 1,145** | 44,876 (26 of mult. 25), **F = 45,800** | 246,792 (39 of mult. 38), 0 parallel, **F = 248,938** |
| own cell enumeration, no samples used (Python, exact rational probe inside every edge, both sides) | 1,145 cells = F; **0 failing** by definition (4-point test on every convex 5-subset + q) | not run (too slow in Python) | not run |
| replay of the record finder's samples | 1,145 lines, distinct, **set equal to my own cell set**, 1,145 witnesses verified | 45,800 lines, all on no line, distinct, count = F, 45,800 witnesses verified: SATURATED | 248,938 lines, distinct, count = F, all witnesses verified: SATURATED |

- **Other two 11-point witnesses** (`found/k6_n11_k6n.txt`, `found/k6_n11_k6d00.txt`): the same full check passes
  (1,145 cells, 0 failing, samples equal to my cell set). They have 146 and 148 convex quadrilaterals respectively.
  The count of convex quadrilaterals is an order-type invariant, also under reflection. So "k6d00 is a different
  order type" is a sound inference. "k6n possibly the same" is correctly left open.
- **Claim text against the file:** the 11 points listed in claim satg6-le-11 equal `found/k6_n11_k6a.txt` line for
  line. The coordinate bounds 3,850,224 (26 points) and 621,645 (39 points) are correct.

## 5. Controls: can they fail?

- **Negative controls (S minus point 0).** If S is K-gon-free and saturated, S − p always has at least one failing
  cell: the cell that contains p. So a checker that always answered SATURATED would fail this control. The exact
  counts also agree across independent code:
  - K = 6: 166 of 756 (VX2 log; my own Python enumeration; rebuilt satcheck);
  - K = 8: 712 of 38,826 (VX2 log; rebuilt satcheck re-run by me, `sound/satcheck_cur_k8b_minus0.log`);
  - K = 9: 2,037 of 223,517 (logs of VX2, satcheck and the finder; not re-run by me).
  - VX2 also reports `dropped_point_cell FOUND FAIL`.
- **Controls on my replay** (`sound/ctl/`, `sound/replay_controls.log`). Four corrupted copies of the 11-point sample
  file are each rejected (NOT_SHOWN):
  - last line dropped (1,144 < F);
  - first line duplicated (bad = 1);
  - one witness replaced by 0 1 2 3 4 (bad = 1);
  - one sample moved onto a point of S (on a line, bad = 1).
- **Worker's controls.** The known vx1118 counts reproduced by satcheck (pentagon 33 of 38; sl31 − p0: 1,206;
  sl31 − p11: 99; s36 − p35: 121) differ from 0 and from one another, so they can fail. Input-rejection controls
  (collinear triple; convex hexagon + 1) are also present. These are adequate.

## 6. The point-adjacent-cell lemma

**Proof check (written argument in the worker README, section "Point-adjacent failing cells").**
- **Step 1.** Membership in R(P) (points seeing exactly one edge of P) is constant on the cell C. If C ⊂ R(P), then
  C lies in one of the disjoint open polyhedra {f_i < 0, f_j > 0}. Then p lies in its closure, and, being on none of
  its lines, in the polyhedron itself. So P + p would be a convex K-gon of S. Correct.
- **Step 2.** orient(o,p,p+εu) = ε·cross(p−o,u) and orient(p,r,p+εu) = ε·cross(r−p,u). Edges not at p are invisible
  for small ε. "Exactly one visible" means opposite signs. The equivalence "opposite signs ⇔ o and r strictly on one
  side of p + Ru" follows from cross(u, o−p) = cross(p−o, u) and cross(u, r−p) = −cross(r−p, u). The step from o, r
  to all of P − p follows from the cone at p. Correct.
- **Step 3.** The cyclic order of the rays ±(x − p) is determined by the signs of their pairwise crosses, which are
  orientations of S. So are the sides of the points and the list of convex (K−1)-gons. The condition is the same for
  every u in the open sector, because no point of S − p changes side inside the sector. Correct.
- Gap: none. The proof silently needs K ≥ 4 (neighbours o ≠ r), which holds in every use (K ≥ 6).
- The corollary "moves that keep the order type cannot repair such a cell" follows.
- The worker's adjacency test ("signs agree with orient(a,b,p) off p's lines") is equivalent to "the closure
  contains p". The region where those signs agree is an open convex polygon around p, cut into sectors only by the
  lines through p.

**My machine test is stronger than the worker's count comparison** (`sound_check.py lemma`, own code).
- For every p and every open sector at p, it takes the sector's exact sign vector: orient(a,b,p) off p's lines, and
  sign cross(b − a, u) on them, with u = d1 + d2 asserted to lie strictly inside the sector.
- It decides that cell **at definition level**: over all convex (K−1)-subsets, every hit is confirmed by the 4-point
  test, and every uncovered sector is confirmed on all subsets by the 4-point test alone.
- It compares this decision with the lemma's criterion, **sector by sector**.

| state | K | sectors | uncovered (definition) | uncovered (lemma) | mismatches | worker's figure |
|---|---|---|---|---|---|---|
| new 11 (k6a) | 6 | 220 | 0 | 0 | 0 | 0 |
| new 11 minus point 0 | 6 | 180 | 48 | 48 | 0 | 48 |
| k6b 11-point state | 6 | 220 | 6 | 6 | 0 | 6 |
| k6i 10-point state | 6 | 180 | 8 | 8 | 0 | 8 |
| k6l 10-point state | 6 | 180 | 8 | 8 | 0 | 8 |
| k6d00 (third 11) | 6 | 220 | 0 | 0 | 0 | (not listed) |
| k8b 25-point state | 8 | 1,200 | 2 | 2 | 0 | 2 |
| k8m 25-point state | 8 | 1,200 | 2 | 2 | 0 | 2 |
| k8j 26-point state | 8 | 1,300 | 4 | 4 | 0 | 4 |
| new 26 | 8 | 1,300 | 0 | 0 | 0 | 0 |
| new 26 minus point 0 | 8 | 1,200 | 56 | 56 | 0 | 56 |
| SAT2's 27 | 8 | 1,404 | 0 | 0 | 0 | 0 |

- For the K = 6 states, my full cell enumeration also gives the number of (failing cell, adjacent point) pairs. It
  equals the uncovered-sector count: 48, 6, 8, 8. The 10-point states have 13 failing cells each, so 5 failing cells
  are adjacent to no point, as the worker reports.
- Not re-run by me: k9S-36 (32, plus 4 non-adjacent cells) and SAT3's 40 (0).
- The test can fail: states with both outcomes occur, and a polygon that avoids p but covers the cell would show up as
  a mismatch.
- The label stays **PROVED**: the written proof is correct. The machine tests are consistency evidence only.

## 7. Labels and rounding up

- **EXACT.** This label is defined in the task's rule 9 ("exact integer/rational computation by named code") and used
  throughout SATG20261118. SKILL.md section 2 lists EXACT TREE, not EXACT. I read EXACT in the task's sense.
- Each bound rests on at least two independent exact implementations, which the task required: the record's vx1118
  pair (finder + `check_cells.py`), VX2 and the worker's satcheck. My two programs are further independent
  implementations, and they agree.
- **Nothing is rounded up.**
  - The bounds are upper bounds for the stated integer coordinates.
  - "New" means only "below SATG20261118"; the worker made no literature search. The last one is WATCH_1118, 18 Nov.
  - The K = 6 at 10 points, K = 8 at 25 and K = 9 at 38 failures are reported as HEURISTIC.
  - The lemma is labelled PROVED, with the machine checks stated separately.

## 8. Wording points (none affects a verdict)

1. Claims satg6/8/9 and the worker's Statement say "every point q with S+q in general position". DDSZ says
   "q ∉ P". With S + q = S ∪ {q}, q ∈ S would trivially fail. All checks are over open cells (q ∉ S), so this is
   wording only. Add "q ∉ S" in the record.
2. satg9 says "no symmetry left". The worker's logs show only 0 parallel pairs. My own check closes the Euclidean case
   (`sound/sym_k9e39.log`): the 39 integers |39·p − Σp|² are pairwise distinct. An isometry of S fixes the centroid
   and preserves these distances, so it fixes every point and is the identity. Hence S has no nontrivial rotation or
   reflection symmetry. Wider affine maps are outside my check; the rebuild verifier reports 0 nontrivial affine
   self-maps, which is not my evidence. The remark is peripheral to the bound.
3. The recipes give the sample line format as `QX QY QD P t1..t_{K-1}`. The files carry an extra trailing token
   (e.g. `e4`), which a checker must ignore.
4. In the K = 9 `satcells_nb` log, the line `a.bruteforce convex_9-subsets=0 …` follows `a.bruteforce SKIPPED`. It
   is the DFS compared with itself, not a brute force (record section 6). The claim correctly takes the brute force
   from vx2sat2 (`vx/vx2_k9e/brute.log`).
5. I found no log (searching `*.log` and `*.txt`) of satcheck on the K = 6 (166) and K = 8 (712) negative controls,
   nor of `satcheck_big.py` on the 11-point sets; only the README states them. I reproduced the two controls with the
   bit-identical rebuild of satcheck, and re-ran `satcheck_big.py` on `found/k6_n11_k6a.txt` (VERDICT SATURATED,
   1,145 cells, 0.9 s; `sound/satcheck_big_k6a_rerun.log`). The K = 9 control is logged.
6. The lemma's statement should say K ≥ 4.

## 9. Files and SHA-256 (all under `/home/jay/research/data/lower-20261121/satg/`)

| file | SHA-256 |
|---|---|
| `verify/sound/sound_check.py` | `bdfc003d277d86a28cbd5bd111d9b9fc9475ea84e8692baf6bebc1f85b44e85e` |
| `verify/sound/replay.cpp` | `c45388c70cee67c284d2a6f2cb20d92c7887f193196899a7348350c7247c2611` |
| `verify/sound/replay` (g++ -O2 -std=c++17) | `9205c7d35ad328e816caece08ea3b6cff3c763ae7c86d982726a3674baeef106` |
| `verify/sound/satcheck_cur` (rebuild of `check/satcheck.cpp`) | `fd44f84daa65bd785a5c327350593c6f5395f79a46f5e428b0256b94dded9a23` (= `bin/satcheck`) |
| `verify/sound/replay_k8b26.log` | `ad2cdc121179c26ad8da37eb58ccc8b51cdf51b938aa57c7e2775b109ba89892` |
| `verify/sound/replay_k9e39.log` | `9fae681395113727d2b7e039a8e9da0ebf96e25e96ac3e7f0b6236c0f15d76de` |
| `verify/sound/full_k6a.log` | `8ebf49d6db6b52af7d2d30d3c8fd7c30d1d48e2ad05bb9758195ba89387444ed` |
| `verify/sound/full_k6a_minus0.log` | `2ecdbb125045cbdb38c13dd2f7d4fe19a1984adc53e1eba4d0c9e81014c54a3c` |
| `verify/sound/lemma_*.log` (12 states), `full_k6{b,i,l,n,d00}.log`, `spot_*.log`, `replay_controls.log` | see `sha256sum verify/sound/*` |

Inputs checked (hashes equal to `SHA256SUMS`):

| input | SHA-256 |
|---|---|
| `found/k6_n11_k6a.txt` | `0583fc7d…f35d` |
| `found/k8_n26_k8b.txt` | `123fcd39…057d` |
| `found/k9_n39_k9e.txt` | `204a0744…d50b` |
| `vx/k6a_found_n11_144/samples.txt` | `f34ae78d…0b31` |
| `vx/k8b_found_n26_73/samples.txt` | `6edfafdf…c456` |
| `vx/k9e_found_n39_533/samples.txt` | `1f831171…41e8` |

`vx/k6n_found_n11_8/samples.txt` (`7c00d8d6…bb5`) is not listed in `SHA256SUMS`. It is used only for the
non-essential second witness.

## 10. What remains and how to re-run

- Not done by me:
  - a run of my own cell enumeration without samples for the 26- and 39-point sets (my replay of the record
    finder's samples, with my own F, is complete);
  - a re-run of the K = 9 negative control;
  - the lemma test on k9S-36 and SAT3's 40.
- For the record (main session): add "q ∉ S" to the statements. Write "no symmetry left" as "no nontrivial rotation
  or reflection (distinct centroid distances)" (section 8, point 2).

```bash
D=/home/jay/research/data/lower-20261121/satg; cd $D; PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
g++ -O2 -std=c++17 -o verify/sound/replay verify/sound/replay.cpp
verify/sound/replay found/k8_n26_k8b.txt 8 vx/k8b_found_n26_73/samples.txt        # VERDICT SATURATED (0.1 s)
verify/sound/replay found/k9_n39_k9e.txt 9 vx/k9e_found_n39_533/samples.txt       # VERDICT SATURATED (1.9 s, 64 MB)
$PY -I verify/sound/sound_check.py full found/k6_n11_k6a.txt 6 vx/k6a_found_n11_144/samples.txt
$PY -I verify/sound/sound_check.py full check/k6_n11_k6a_minus0.txt 6             # 166 of 756 failing
$PY -I verify/sound/sound_check.py lemma check/k8_n26_k8b_minus0.txt 8            # 56 = 56, 0 mismatches
```
