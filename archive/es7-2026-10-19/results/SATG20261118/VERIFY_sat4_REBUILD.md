# VERIFY D-satg-descents (lens REBUILD), independent verifier, 21 Nov 2026 (work dir created 23:32, unit batch finished 23:42:26, file finalized about 23:50 KST)

## 1. Headline

| claim | verdict | label confirmed |
|---|---|---|
| satg6-le-11 (sat_g(6) <= 11, `found/k6_n11_k6a.txt`, plus witnesses k6n and k6d00) | **confirmed** | EXACT (for the stated integer coordinates) |
| satg8-le-26 (sat_g(8) <= 26, `found/k8_n26_k8b.txt`) | **confirmed** | EXACT (for the stated integer coordinates) |
| satg9-le-39 (sat_g(9) <= 39, `found/k9_n39_k9e.txt`) | **confirmed** | EXACT (for the stated integer coordinates) |
| point-adjacent-cell-lemma | **confirmed** | PROVED (I checked the written proof step by step). Machine check: my own code, one implementation, sector by sector, 13 of 13 listed states plus 3 more, 0 mismatches |

Each EXACT verdict rests on my own C++ checker `vsat.cpp` (written for this check from the problem definition; it
shares no code with the worker's `satcheck`/`satcheck_big.py`, the record's `satcells`/`check_cells.py`, or VX2's
`vx2sat`). The verdict combines two internal paths that must agree:

- **REBUILD**: my own enumeration of all cells, with every cell decided at the level of the definition;
- **REPLAY**: my own replay of the record finder's concrete rational samples. The set of sign vectors from the
  replay equals the set from my rebuild.

I did not run the worker's or the record's checkers; their quoted outputs were only read from logs (section 5.5).
No CNF or LRAT proof is in scope (exact integer computation only), so cake_lpr was not applicable.

## 2. Statements checked

Definition (record SATG20261118 section 2, DDSZ): a finite set S in general position is K-gon-saturated iff no K
points of S are in convex position, and every q not in S with S + q in general position is a vertex of a convex
K-gon of S + q. Then sat_g(K) <= |S|.

- satg6-le-11: the 11 points of `found/k6_n11_k6a.txt` are in general position and contain no convex hexagon (largest
  convex subset 5, exactly 22 convex pentagons). They are hexagon-saturated. The same holds for `k6_n11_k6n.txt` and
  `k6_n11_k6d00.txt` (convex 3..6-subset counts 165/148/22/0).
- satg8-le-26: the 26 points of `found/k8_n26_k8b.txt` (|coord| <= 3,850,224) are in general position and have no
  convex 8-gon (largest convex subset 7, exactly 497 convex 7-gons). They are 8-gon-saturated.
- satg9-le-39: the 39 points of `found/k9_n39_k9e.txt` (|coord| <= 621,645, "no symmetry left") are in general
  position and have no convex 9-gon (largest convex subset 8, exactly 1,140 convex 8-gons). They are
  9-gon-saturated.
- point-adjacent-cell-lemma: see section 5.4.

## 3. Model and soundness of my checker `vsat.cpp`

Arithmetic: all inputs satisfy |coordinate| < 2^28 (asserted). Every quantity is computed exactly in `__int128`:

- differences are below 2^29 and crosses below 2^60;
- comparisons of crossing parameters are below 2^119;
- vertex numerators are below 2^89.

1. **General position.** All C(n,3) orientations are nonzero.
2. **No convex K-gon**, by two methods.
   - (a) **DFS.** Grow subsets in increasing index order. A point j is added to a convex set C only if no 4-subset
     containing j fails the 4-point test. This is complete: convex position is hereditary, and by Carathéodory plus
     general position a set is in convex position iff no point lies strictly inside a triangle of three others.
   - (b) **Plain brute force** over all K-subsets and all (K-1)-subsets (Gosper enumeration, no pruning). A subset
     is convex iff none of its points is strictly inside a triangle of three of its points (precomputed triangle
     masks).
   - The counts from (a) and (b) must agree. The brute-force totals must equal the binomials.
3. **Cells.**
   - **Euler count.** F = 1 + L + sum_v (k_v - 1), over the distinct vertices of the arrangement of the
     L = C(n,2) lines. Vertices are the exact intersections of all line pairs, normalized by gcd. A vertex met by
     r pairs has k_v lines with C(k_v,2) = r (checked to be a binomial). Parallel pairs are counted; coincident
     lines would abort.
   - **Rebuild enumeration.** Take each line l = s_i + t(s_j - s_i). For every other line m,
     orient(s_a, s_b, s_i + t d) = A_m + t B_m. Sort the crossing parameters t_m = -A_m/B_m exactly and group
     equal values. On each edge (an open interval between consecutive distinct crossings, or a ray), the sign of
     line m is sign(B_m) * sign(t - t_m); a parallel line has the constant sign sign(A_m). Points just off the
     edge on either side lie in one open cell, whose sign vector is that vector with ± for l.
   - **Why every cell is found.** Every open cell borders an edge, so it is hit. Distinct sign vectors are
     distinct cells, since a cell is the intersection of its open half-planes, which is convex. The number of
     distinct vectors must equal F; exceeding F aborts. A cross-check also requires
     sum_l (distinct vertices on l) = sum_v k_v.
4. **Per-cell decision** (q abstract; its exact sign vector fixes the order type of S + q).
   - S has no convex K-gon, so q is on a convex K-gon iff some convex (K-1)-gon P of S has P + q in convex
     position.
   - Fast filter: exactly one edge of the CCW polygon P is visible from q.
   - **Every pass** is re-verified by the 4-point test on P + q.
   - **Every failing cell** is re-verified by the 4-point test against **all** convex (K-1)-gons of S, whose list
     is complete by 2(a) and 2(b).
5. **Replay** of `samples.txt` (lines `QX QY QD P t1..t_{K-1} [extra]`, q = (QX/QD, QY/QD)).
   - Each orientation is computed as QD * orient(s_i, s_j, q) = dx*(QY - y_i*QD) - dy*(QX - x_i*QD), with
     |QX|, |QY| < 2^80 and 0 < QD < 2^50 asserted, so every value is below 2^112.
   - Checks: q lies on no line; sign vectors are pairwise distinct (compared as full vectors, not by hash); the
     count equals my F; the witness is K-1 distinct indices, and witness + q passes the 4-point test (for K points
     in general position this is the same as "K hull vertices").
   - Every replayed vector must also be a member of my rebuild set. With equal counts, this shows the two sets are
     **equal**.
6. **Affine symmetry** (`affsym.py`, exact integers). This counts the affine maps f with f(S) = S.
   - Each such map is determined by the images of s0, s1, s2.
   - A finite-order affine map has det = ±1, which prunes the search.

## 4. Method

- Built with `g++ -O2 -std=c++17` (g++ 15.2.0).
- The small K = 6 runs were run directly (each under 1 s).
- Everything else ran in one unit, `esr-ag-satg-v1` (CPUQuota 100 %, MemoryMax 600M, MemorySwapMax 0,
  RuntimeMaxSec 5400, nice 10; script `run1.sh`). Unit runtime was 12.5 s, CPU 12.4 s, memory peak 64.7 MB.
- YIELD was absent before the start, and no other `esr-ag-satg-*` unit was active.

## 5. Results

### 5.1 satg6-le-11: confirmed (EXACT)

| set | general position | DFS convex 3..6 | brute C(11,5)/C(11,6) | lines / parallel / vertices (hist) | F | rebuild: distinct = F, fail | replay of record samples |
|---|---|---|---|---|---|---|---|
| k6a (`0583fc7d…0f35d`) | 0 collinear | 165 / 146 / 22 / **0** | 462 subsets: 22 convex / 462 subsets: **0** | 55 / 0 / 1,001 (990 simple, 11 of mult. 10) | **1,145** | 1,145 = F, **fail 0** (all 1,145 passes 4-point verified) | 1,145 samples, 0 on a line, 0 duplicates, 1,145 witnesses verified, **sets equal** |
| k6n (`d11855a4…efb5`) | 0 | 165 / 146 / 22 / 0 | 22 / 0 | 55 / 0 / 1,001 (same hist) | 1,145 | fail 0 | sets equal, 1,145 verified |
| k6d00 (`46e742ad…75ea`) | 0 | 165 / **148** / 22 / 0 | 22 / 0 | 55 / 0 / 1,001 (same hist) | 1,145 | fail 0 | sets equal, 1,145 verified |

Negative control: k6a minus point 0 (my file; same SHA-256 `e29ba769…c278` as the worker's) gives **166 failing
cells of 756**, as claimed. max |coordinate| of k6a = 461,390.

### 5.2 satg8-le-26: confirmed (EXACT)

- k8b (`123fcd39…057d`, max |coordinate| 3,850,224): 0 collinear triples. DFS convex 3..8:
  2,600 / 8,299 / 9,557 / 3,929 / **497** / **0**.
- Brute force: C(26,7) = 657,800 subsets with 497 convex; C(26,8) = 1,562,275 subsets with **0** convex.
- 325 lines, 0 parallel pairs, **44,876** vertices (44,850 simple, 26 of multiplicity 25), F = **45,800**.
- Rebuild: 181,350 probes give 45,800 distinct vectors = F, **fail 0**.
- Replay of `vx/k8b_found_n26_73/samples.txt` (`6edfafdf…c456`): 45,800 samples, 0 on a line, 0 duplicates, 45,800
  witnesses verified, **sets equal**.
- Negative control (minus point 0, `a5e77639…772b`): **712 failing of 38,826**, as claimed.

### 5.3 satg9-le-39: confirmed (EXACT)

- k9e (`204a0744…d50b`, max |coordinate| 621,645): 0 collinear triples. DFS convex 3..9:
  9,139 / 44,021 / 77,117 / 53,383 / 14,010 / **1,140** / **0**.
- Brute force: C(39,8) = 61,523,748 subsets with 1,140 convex; **C(39,9) = 211,915,132 subsets with 0 convex**.
- 741 lines, **0 parallel pairs**, **246,792** vertices (246,753 simple, 39 of multiplicity 38), F = **248,938**.
- Rebuild: 991,458 probes give 248,938 distinct = F, **fail 0**.
- Replay of `vx/k9e_found_n39_533/samples.txt` (`1f831171…41e8`): 248,938 samples, 0 on a line, 0 duplicates,
  248,938 witnesses verified, **sets equal**.
- Negative control (minus point 0, `5f38d797…8aef`): **2,037 failing of 223,517**, as claimed.
- "No symmetry left": **0 nontrivial affine self-maps**. This is a stronger test than the worker's "0 parallel
  pairs", which only excludes point reflections. Positive control: SAT3's 4-fold 40-point set shows its 3 rotations.

### 5.4 point-adjacent-cell-lemma: confirmed (PROVED)

**Proof check.** I read the proof in the worker's README, section "Point-adjacent failing cells", and checked each
step.

- **Step 1** (P not through p cannot cover C).
  - R(P) is the set of points that see exactly one edge. It is a finite union of open polyhedra
    {f_i < 0, f_j > 0}, and coverage by P is constant on C.
  - If C were inside R(P), then since p is in the closure of C, p would be in the closure of one of these
    polyhedra.
  - No edge line of P passes through p (general position, p not in P), so p would lie in the open polyhedron
    itself. Then P + p would be a convex K-gon of S, a contradiction.
- **Step 2.** Write q = p + eps*u, with o, p, r consecutive CCW vertices of P.
  - Then orient(o,p,q) = eps*cross(p-o,u) and orient(p,r,q) = eps*cross(r-p,u). Edges of P not at p stay
    invisible for small eps.
  - So exactly one edge is visible iff the two crosses have opposite signs.
  - That holds iff cross(u,o-p) and cross(u,r-p) have the same sign, i.e. o and r lie strictly on one side of the
    line p + Ru. By the cone argument this is equivalent to all of P - p lying strictly on that side.
  - Coverage of C by a K-gon through q is exactly coverage by P + q, where P is a convex (K-1)-gon of S (S has no
    convex K-gon). Both directions of the lemma follow.
- **Step 3.** The sector structure at p, the side of each point relative to a sector line, and the list of convex
  (K-1)-gons are all functions of the triple orientations.
- The criterion is well defined: a line through p in a direction inside an open sector contains no other point of
  S, so it does not depend on which u in the sector is chosen. It is also symmetric under u -> -u, so antipodal
  sectors are covered or not covered together.
- I found no gap. It is unrefereed apart from this reading.

**Machine check** (my code; stronger than the worker's count comparison). For every p and each of its 2(n-1) open
sectors I did the following:

1. built the sector's sign vector: orient(a,b,p) for lines missing p, and sign(cross(s_b - s_a, u)) for lines
   through p, with u the sum of the two bounding directions;
2. looked it up in my rebuilt cell map (it was found every time);
3. required "cell passes <=> some convex (K-1)-gon through p has all other vertices strictly on one side of p + Ru".

| state (file SHA-256) | criterion-uncovered sectors = failing (cell, point) pairs | mismatches | failing cells: adjacent / not adjacent | worker's figure |
|---|---|---|---|---|
| k8j-26 (`9234cf23…`) | 4 = 4 | 0 | 4 / 0 | 4 |
| k6b-11 (`279c7989…`) | 6 = 6 | 0 | 6 / 0 | 6 |
| k9S-36 (`2d446b8f…`) | 32 = 32 | 0 | 32 / **4** | 32 (+4 not adjacent) |
| k8b-25 (`9f0700a5…`) | 2 = 2 | 0 | 2 / 0 | 2 |
| k8m-25 (`f1c0e3a1…`) | 2 = 2 | 0 | 2 / 0 | 2 |
| k6i-10 (`runs/k6i/best_n10.txt`, `b5994548…`) | 8 = 8 | 0 | 8 / 5 (13 failing of 756) | 8 |
| k6l-10 (`runs/k6l/best_n10.txt`, `08709fae…`) | 8 = 8 | 0 | 8 / 5 (13 failing of 756) | 8 |
| saturated k6a-11, k8b-26, SAT2 k8-27, SAT3 k9-40 | 0 = 0 each | 0 | 0 / 0 | 0 |
| k8b-26 minus point 0 | 56 = 56 | 0 | 56 / 656 | 56 |
| k6a-11 minus point 0 | 48 = 48 | 0 | 48 / 118 | 48 |
| extra: SAT2 k6-12, k9e-39 | 0 = 0 | 0 | 0 / 0 | - |
| extra: k9e-39 minus point 0 | 80 = 80 | 0 | 80 / 1,957 | - |

The 10-point states k6i and k6l were identified by path, because the worker's README gives no hashes for them.
Their counts match the README's description: 13 failing cells of 756, of which 8 are point-adjacent and 5 are not
point-adjacent. I did not test whether those 5 cells are unbounded, which is what the README says.

### 5.5 Worker artefacts

- `sha256sum -c` on the worker's `SHA256SUMS`: all 70 entries OK.
- The quoted record-checker and VX2 lines are present in the logs:
  - `vx/*/cpp.log` (RESULT … fail=0 … SATURATED);
  - `vx/*/py.log` (REPLAY … bad=0 … SATURATED);
  - `vx/*/fresh.log` (VERDICT SATURATED);
  - `vx/vx2_*` (SATURATED_SET; brute force 1,140 / 0 for k9e).
- The VX2 negative controls in the logs:

  | log | line | content | verdict line |
  |---|---|---|---|
  | `vx/vx2_v11/neg.log` | 15 | `methodA fail_cells 166` | line 24: `VERDICT NOT_CONFIRMED` |
  | `vx/vx2_v26/neg.log` | 15 | `methodA fail_cells 712` | line 24: `VERDICT NOT_CONFIRMED` |
  | `vx/vx2_k9e/neg.log` | 16 | `methodA fail_cells 2037` | line 25: `VERDICT NOT_CONFIRMED` |

  For k9e, `fresh_minus0.log` and `finder_minus0.log` also give 2,037 of 223,517. All of these agree with my own
  counts.
- I found no saved log for the claimed `satcheck_big.py` run on the 11-point set (the README asserts SATURATED).
  This does not affect my verdict.

## 6. Controls (each could fail)

- **Record vx1118 controls, exact numbers reproduced:**

  | set | K | cells | failing |
  |---|---|---|---|
  | pentagon | 6 | 38 | 33 |
  | sat14 (42 parallel pairs, vertex of multiplicity 7) | 6 | 3,206 | 0 |
  | hexfree16_m4 (56 parallel pairs) | 6 | 5,728 | 0 |
  | hexfree16_m5 | 6 | 5,802 | 0 |
  | sat21 | 7 | 18,565 | 0 |
  | sl31 | 8 | 95,760 | 0 |
  | sl31 minus p0 | 8 | 83,491 | 1,206 |
  | sl31 minus p11 | 8 | 83,491 | 99 |
  | s36 minus p35 | 8 | 158,831 | 121 |

- **Record sets:**
  - SAT2_k6_n12: 1,672 cells, 0 failing.
  - SAT2_k8_n27: 53,677 cells, 0 failing.
  - SAT3_k9_n40: 275,920 cells, 0 failing (380 parallel pairs, a centre vertex of multiplicity 20).
  - The cell counts equal the record's.
- **Claimed negative controls:** 166 / 756, 712 / 38,826 and 2,037 / 223,517 (above).
- **Replay must reject** (on k6a's samples), and it did reject all four:
  - one witness index changed;
  - one line duplicated over another;
  - the last line dropped;
  - one sample moved exactly onto the line through points 0 and 1.

  (A sample moved by 1/QD stayed in its cell and was rightly accepted, so I discarded it as a control.)
- **Convexity must fail:**
  - convex hexagon + 1 point: DFS and brute force both find 1 convex 6-subset; NOT_SATURATED;
  - hexagon + 2 points: 2 found;
  - a collinear triple: CHECK_FAILED.

## 7. Files and SHA-256 (all in `/home/jay/research/data/lower-20261121/satg/verify/`; full list `SHA256SUMS_verify`, 50 entries)

| file | SHA-256 |
|---|---|
| `vsat.cpp` (my checker) | `5453cb48e5775c78edd619f72078192dc246cb087ca384e801544f3a348f8c0c` |
| `vsat` (binary) | `21dc0026e4a1824ce5bcb1df52f7f52cea32a25f718e571a6c5c55c5dc878b9c` |
| `affsym.py` | `14543aad4e5069d7fa6d0ea739e6b945362194187bc05749267cc36c18374bc9` |
| `run1.sh` (unit runner) | `8986c55d9f290690e6129f577a18367a8b0ff9105f487c761c30667f96866d25` |
| `logs/check_k6_n11_k6a.log` | `cca31297c8f5ec54225e38bec972bd70b15330cdb0ebc3c45d56d7b797c5aeef` |
| `logs/check_k8_n26_k8b.log` | `3c31c6d37ce95b9f9c7c52a44ee218d6c572f445647638eb0d9df7694435cc4f` |
| `logs/check_k9_n39_k9e.log` | `3e57b8e927bfe287076385d8086551c063f4cb5c8340468765a13ad1390df6c6` |
| `logs/brute_k9_n39_k9e.log` | `335088ebd1290f755946b57981632f9c773b742a1a9cc0b5faabb087a98f0f4f` |

Inputs (worker's, unchanged):

| file | SHA-256 |
|---|---|
| `found/k6_n11_k6a.txt` | `0583fc7d…0f35d` |
| `found/k6_n11_k6n.txt` | `d11855a4…efb5` |
| `found/k6_n11_k6d00.txt` | `46e742ad…75ea` |
| `found/k8_n26_k8b.txt` | `123fcd39…057d` |
| `found/k9_n39_k9e.txt` | `204a0744…d50b` |
| samples k6a | `f34ae78d…0b31` |
| samples k8b | `6edfafdf…c456` |
| samples k9e | `1f831171…41e8` |
| samples k6d00 `vx/k6d00_found_n11_0/samples.txt` | `ce7f1e02bc0fd6a97f449c7f217de75c27860d7f853c1f30382a6c5f22ad5b0d` |
| samples k6n `vx/k6n_found_n11_8/samples.txt` | `7c00d8d642175b675cb5e08c2e43a846935eebaf90a92b74c5b8e6b6a2ab9bb5` |

All of these match the worker's `SHA256SUMS`, except the k6n samples file, which is not listed there. Its hash above
is the one I computed myself; I replayed it.

## 8. Limits and what remains

- **Shared method.** My rebuild uses the same general method as the worker's `satcheck`: probe both sides of every
  edge, then the standard cap criterion. Only the code is independent. The second, sample-source-independent
  agreement is the replay: my rebuilt cell set equals the set of the record finder vx1118's concrete samples
  (cell by cell, full vectors).
- **Novelty not checked.** "Below the record" only; no literature search.
- **Coordinate-specific.** Saturation was checked for these exact integer coordinates only, not for their order
  types.
- **Lemma.** The proof was checked by me alone, not externally refereed. The machine check is one implementation
  (mine).
- **Nothing remains for these four claims.** Applying them to the record SATG20261118 is the main session's
  decision.

## 9. Resume commands

```bash
cd /home/jay/research/data/lower-20261121/satg/verify
g++ -O2 -std=c++17 -o vsat vsat.cpp
D=/home/jay/research/data/lower-20261121/satg
./vsat check $D/found/k6_n11_k6a.txt 6 $D/vx/k6a_found_n11_144/samples.txt lemma   # VERDICT SATURATED, R... sets equal
./vsat brute $D/found/k6_n11_k6a.txt 6
# K = 8 / K = 9, controls, lemma states, brute force (12 s, 65 MB) as a unit:
systemd-run --user --unit=esr-ag-satg-v1 -p CPUQuota=100% -p MemoryMax=600M -p MemorySwapMax=0 -p RuntimeMaxSec=5400 \
  --nice=10 --wait --collect --working-directory=$PWD -p StandardOutput=file:$PWD/logs/run1.out $PWD/run1.sh
/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -I affsym.py $D/found/k9_n39_k9e.txt
```
