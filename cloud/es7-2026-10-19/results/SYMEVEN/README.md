# SYMEVEN: centrally symmetric sets of 2^(k−2) points without a convex k-gon, for every even k ≥ 6

Local work on an Apple M5 Pro, 1 November 2026 (UTC).

**Statement.** For every even k ≥ 6 there is a set S of 2^(k−2) points in the plane, in general position, with S = −S
and 0 ∉ S, that contains no k points in convex position. With `SYM2` (odd k), such sets exist for every k ≥ 3 except
k = 4, where four centrally symmetric points in general position always form a parallelogram.

**Credit and status.**
- The statement is **implied by known results**, although no source inspected states it (§6):
  - k = 6: the fourfold symmetric 16-point sets without a convex hexagon of Subercaseaux, Mackey, Qian and Heule
    (arXiv:2506.00224v1, §6.1 and App. C, Table 1) and of Mackey's thesis (CMU-CS-25-108, Fig. 3.28) are centrally
    symmetric, since the square of a quarter-turn is the half-turn.
  - Every even k ≥ 8: Baek and Balko's blow-up lemma (SoCG 2025, Definition 13 and Lemma 14), applied to either of
    these 16-point sets with a half-turn-symmetric labelling that is not a threshold, gives such a set (§6.2). The SoCG
    version omits the proof of Lemma 14; the full text of the journal version (JCTA 222 (2026) 106195) was not read.
  - Odd k (`SYM2`): Valtr's construction as described by Baek and Balko, with a centrally symmetric base.
- **What this directory adds.**
  - `PROOF.md`: an independent, self-contained proof that does not use Lemma 14. **Written proof, refereed** by an
    independent review (§3). Not machine-checked.
  - Explicit instances for k = 6, 8 and 10, with 16, 64 and 256 points: **exact computation** (§4).
  - Two explicit sets from the Lemma 14 route, for k = 8 and 10: **exact computation** (§6.2).
- This settles the even case that `SYM2/README.md` (section "Even k") left open; by §6 the answer already follows from
  published results. `SYM2` and `WRITEUP` are not changed here.

## 1. The construction (`PROOF.md` §§2–3)

Fix an even k ≥ 6, and let n = k − 2 and m = k/2.
- **Base.** The abscissae −(n−1), …, −3, −1, 0, 1, 3, …, n−1 on the cubic y = x³. Three base points are collinear only
  in the forced triples (x, 0, −x): a sum of three odd numbers is odd.
- **Outer clusters.** For j < n/2, the Erdős–Szekeres set G(j+2, k−j) (C(n, j) points, no (j+2)-cup, no (k−j)-cap),
  scaled by (ε, ε²) and placed at base point j. The cluster at base point n − j is its negative.
- **Middle cluster.** ε²·M_0, where M_0 = −M_0 has C(n, n/2) points, no (m+1)-cup, no (m+1)-cap and no point at 0.
- **Size.** Σ_j C(n, j) = 2^(k−2).

The middle cluster is smaller than the outer clusters by a factor ε, and this is what handles the collinear base
triples. At the outer scale, or at a scale δ with ε ≪ δ ≪ 1, convex k-gons appear: an argument is sketched in
`PROOF.md` Remark 3, and exact computations confirm it for k = 6 and 8 (`review/README.md`, "Variants"; controls in
§4).

## 2. The proof

- **Lemma 3**, a blow-up lemma for this collinear base, gives conditions (H0)–(H5) under which a clustered set has no
  convex k-gon. The condition for the middle cluster is (H4): for p in cluster j < n/2, q in the middle cluster and r
  in cluster n − j, with x(p) + x(r) ≠ 0, orient(p, q, r) has the sign of −(x(p) + x(r)).
- **Idea.** The lower chain of a convex polygon is a cup in its leftmost cluster followed by single points of other
  clusters; the upper chain is single points followed by a cap in its rightmost cluster. The sign conditions put the
  two chains through disjoint clusters, except in one configuration through the middle cluster, where (H4) leaves only
  4 points. This is the one place where k ≥ 6 is used.
- **The theorem:** for small ε the construction satisfies (H0)–(H5) and is in general position.
- Lemma 3 uses no symmetry. It is not a case of Lemma 14, which needs a base in general position.
- **Provenance.** A first variant (base 0, ±2^(j−1); middle cluster scaled by (ε², ε⁴)) had its own write-up and sets,
  not included here. `PROOF.md` was derived without reading that write-up, and it is the version that was reviewed.

## 3. Independent review (`review/`)

- A referee-style review, run separately and with its own code, checked the first version of `PROOF.md` line by line.
  **Verdict: correct and complete, no mathematical gap.** It asked for six expository fixes, all applied
  (`review/README.md` lists them and where they went).
- Its own computations, in exact arithmetic:
  - `PROOF.md` §3 as written, built with its own code: all hypotheses hold and the largest convex subset is k − 1 at
    every tested ε ≤ 1/32 for k = 6 (1/32, 1/64, 1/128, 1/1024, 10^−6), at every tested ε ≤ 1/256 for k = 8 (six
    values down to 2^−20), and for k = 10 at ε = 1/4096 and 2^−20. At the larger ε tested (H4) fails, and a convex
    k-gon occurs for k = 6 at ε = 1/4, 1/8, 1/16, for k = 8 at 1/4 and 1/16 (not at 1/64), and for k = 10 at 1/64
    (177,625 of them).
  - The three instance files: all hypotheses and general position hold, and the largest convex subset is k − 1 (§4).
  - Attempts to falsify Lemma 3: of 7,000 random clustered sets for k = 6 and 800 for k = 8, the 4,905 and 480 that
    satisfy all hypotheses have no convex k-gon, while 934 and 108 of those failing only (H4) have one. Exact Step-4
    shapes: 15,381 / 14,715 / 7,108 valid configurations for k = 6 / 8 / 10, none in convex position. This is
    **computational evidence** for Lemma 3, which is proved.
- The review did not check literature claims. §6 rests on a separate search.

## 4. Explicit instances (exact computation)

`construct.py K FILE` builds integer sets from the same ingredients with a different scaling (`PROOF.md` §4). It
regenerates the three files byte for byte (`logs/regen.log`). Lines are `x y cluster`.

| file | k | points | max abs coordinate | SHA-256 | collinear triples | largest convex subset |
|---|---|---|---|---|---|---|
| `k6_points.txt` | 6 | 16 | 2.7e10 | `4b63878b…` | 0 of 560 | 5 |
| `k8_points.txt` | 8 | 64 | 1.25e13 | `d45851d0…` | 0 of 41,664 | 7 |
| `k10_points.txt` | 10 | 256 | 3.43e17 | `c315fb0f…` | 0 of 2,763,520 | 9 |

Each set has S = −S, 0 ∉ S, distinct x-coordinates, and cluster j of size C(k−2, j).

**Checks by the authors' code** (integer arithmetic; logs in `logs/`).
- `verify_instance.py` (k = 6, 8): an angular DP and a cup+cap DP for the largest convex subset, a hull test of the
  witness, a counting DP, and random subsets compared with brute force; for k = 6 also a brute force over all subsets
  of 3 to 7 points (no convex 6-subset, hence none larger).
- `dfs_convex.c` (k = 6, 8): enumeration of all convex subsets, with `__int128` orientations. For k = 8 it finds
  41,664 / 345,986 / 1,177,512 / 1,792,349 / 1,032,956 convex 3- to 7-gons and no octagon; for k = 6, 560 / 924 / 322
  and no hexagon. The counting DP gives the same numbers.
- `lcs_dp.c` (k = 10): C versions of both DPs give 9, and the witness is checked.
- `structure_check.py`: (H0)–(H5) hold exactly; all 136 / 13,944 / 1,116,280 triples relevant to (H3) and all
  72 / 4,800 / 272,440 relevant to (H4) are examined.
- Validation against brute force, 0 failures: 400 random sets for the Python DPs, 150 for `dfs_convex.c`, 200 for
  `lcs_dp.c` (`logs/test_*.log`).
- `logs/regen.log` and `logs/test_*.log` were written when this directory was assembled. The other logs are from the
  original runs; all of them were reproduced then, timings aside.

**Checks by the review's code** (§3): two DPs and a counting DP for all three files (for k = 10 its C port), (H0)–(H5)
and general position; for k = 6 also a brute force over all 2^16 subsets. For k = 10 the convex 3- to 9-gons number
2,763,520 / 97,332,082 / 1,562,634,294 / 12,856,727,575 / 55,985,587,892 / 120,029,899,063 / 97,687,514,964
(`review/logs/author_k10.log`).

**A second route.** Since (H0)–(H5) and general position hold exactly, Lemma 3 alone also shows that no file contains a
convex k-gon.

**Controls** (`negative_controls.py`, `random_lemma_test.py`).
- Scaling the middle cluster up by F (Λ = 10^18; F = 1, 10, 10², 10³, 10⁴, 10⁶) gives a convex hexagon for k = 6 at
  every tested F ≥ 10 and a convex octagon for k = 8 at every tested F ≥ 10², and none below. A split middle (k
  clusters, no centre) gives a convex k-gon for k = 6 and 8.
- Random clustered sets: for k = 6, the 451 of 1,500 that satisfy (H0)–(H5) all have largest convex subset 5, and all
  40 that fail only (H4) contain a hexagon. For k = 8, the 289 of 600 that satisfy them all have 7, and 22 of the 66
  failing only (H4) contain an octagon. **Computational evidence.**

## 5. Consequence for k = 8

- A centrally symmetric set in general position with at least 2 points does not contain its centre c, since p, c and
  2c − p would be collinear. So its size is even.
- `k8_points.txt` has 64 points and no convex octagon. So the largest centrally symmetric set in general position
  without a convex octagon has at least 64 points.
- If ES(8) = 65 (the Erdős–Szekeres conjecture for k = 8: a **conjecture**, open), every 65 points in general position
  contain a convex octagon, and that maximum is exactly 64.
- Conversely, since sizes are even, "the maximum is 64" says exactly that every centrally symmetric set of 66 points in
  general position contains a convex octagon: the centrally symmetric case of ES(8) = 65. Any proved central bound
  below 66 would therefore be 64.
- For every even k ≥ 6 the central maximum is at least 2^(k−2), with equality if ES(k) = 2^(k−2) + 1. For k = 6 it is
  16, because ES(6) = 17 (Szekeres–Peters 2006).

## 6. Literature (search of 1 November 2026)

### 6.1 k = 6

- Subercaseaux–Mackey–Qian–Heule, arXiv:2506.00224v1 (also CICM 2025), §6.1 and App. C, Table 1: an explicit fourfold
  symmetric 16-point set in general position without a convex hexagon (their Fig. 4a).
- Mackey, CMU-CS-25-108 (2025), Fig. 3.28 on p. 40, with coordinates on p. 41: another fourfold realization.
- Their 16 points form four rotation orbits of size 4, so 0 ∉ S, and the square of the quarter-turn is the half-turn.
  Exact check (`lit/cor15_arcs.out`; coordinates ×10 in `lit/smqh_table1_16points_x10.txt` and
  `lit/mackey_fig328_x10.txt`): both sets are centrally symmetric and in general position, with 272 convex pentagons
  and no convex hexagon. Neither source calls them centrally symmetric ("centrally" occurs in neither text).
  `WRITEUP/SYMMETRIC.md` already derives the twofold value 16 for k = 6 from the fourfold example.

### 6.2 Every even k ≥ 8 from Lemma 14 (`lit/`)

- **Lemma 14** (Baek–Balko, SoCG 2025). Let p_1, …, p_N be in general position, sorted by x, and let s_{i,j} be the
  largest size of a convex subset with leftmost point p_i and rightmost point p_j. For nonnegative x_i, y_i with
  (a) x_i + y_i ≤ k − 1 and (b) x_i + y_j ≤ k − 1 − s_{i,j} for i < j, the (X, Y)-blow-up of their Definition 13 has
  no k points in convex position, and it has Σ_{l≤x_1} C(k−2, l) + Σ_{i=2}^{N−1} C(x_i + y_i, x_i) + Σ_{l≤y_N} C(k−2, l)
  points.
- **Base and labelling.** Either 16-point set of §6.1, swept in direction (607, 31) (for Mackey's set (607, 27)), so
  that p_{17−i} = −p_i. Sweep positions 1–7 and 9 are labelled left, positions 8 and 10–16 right: the labelling is
  half-turn symmetric but not a threshold. For k = 6 + 2x (x ≥ 0), a left point gets (x_i, y_i) = (x, k − 1 − x − s_i)
  and a right point (k − 1 − x − s_i, x), where s_i is the largest convex subset having p_i as its rightmost point
  (left points) or leftmost point (right points). (y_1 and x_16 enter neither (b) nor the size; the scripts set them
  to 0.)
- **Conditions.** (a) and (b) reduce to facts that do not depend on x: the base has no convex hexagon (pairs labelled
  left–right, and nonnegativity); s_{i,j} ≤ s_j, respectively s_i (pairs with equal labels); and for the only pair with
  a right point before a left one, (8, 9): s_8 + s_9 − s_{8,9} = 4 + 4 − 2 = 6 ≥ 5. `lit/crossed_all_x.py` computes
  all s-values by brute force and checks (a), (b), half-turn compatibility ((x_{17−i}, y_{17−i}) = (y_i, x_i)) and the
  size for x = 0..10 on both bases (`lit/crossed_all_x_smqh.out`, `lit/crossed_all_x_mackey.out`).
- **Size.** The 14 middle s-values are {2, 2, 3, 3, 3, 3, 4 (eight times)}, the profile of Baek and Balko's set M
  (their Lemma 18). The size is 2Σ_{l≤x} C(2x+4, l) + 2C(2x+3, x) + 4C(2x+2, x) + 8C(2x+1, x) = 2^(2x+4) = 2^(k−2).
  Since 2Σ_{l≤x} C(2x+4, l) = 2^(2x+4) − 2C(2x+4, x+1) − C(2x+4, x+2), this is the identity
  2C(2x+3, x) + 4C(2x+2, x) + 8C(2x+1, x) = 2C(2x+4, x+1) + C(2x+4, x+2), which follows by writing every term as a
  rational multiple of C(2x+1, x).
- **Symmetry.** Definition 13 allows an arbitrary set of the required type in each cluster. The half-turn exchanges
  cups and caps and the two parameters, so the cluster at p_{17−i} can be taken as the negative of the cluster at p_i,
  with symmetric neighbourhoods. The blow-up is then centrally symmetric.
- **Status.** Written proof, not refereed, from the published Lemma 14 (whose proof we did not see), with the s-values
  of the base by exact computation.
- **Explicit sets** (exact computation, SMQH base): `lit/smqh_crossed_k8_64points.txt` (64 points, SHA-256
  `82ed0a5b…`, built by `lit/build_labelled_x1.py`, `lit/build_k8.out`) and `lit/smqh_crossed_k10_256points.txt` (256
  points, `0d9f13ff…`, coordinates up to 3.9e27, built by `lit/build_labelled_x2.py` with the cluster routines of
  `lit/cor15_build_x2.py`, `lit/build_k10.out`; both builders regenerate their files byte for byte).
  - `lit/check_set.py`, which agrees with brute force on 300 random sets (`lit/test_check_set.out`), finds both
    centrally symmetric, without collinear triples, with largest convex subsets 7 and 9 (`lit/check_set.out`).
  - `lit/check_refdp.py`, which shares no code with it, runs the cup+cap and angular DPs of `review/refdp.c` on an
    exact sign table: largest convex subsets 7 and 9 by both DPs (`lit/check_refdp.out`).
- **Control.** With the threshold labelling of their Corollary 15 (positions 1–8 left), no sweep direction of either
  base gives more than 62 points for k = 8 (`lit/cor15_arcs.out`). The crossed labelling is what reaches 64.
- **No source inspected states the consequence.** "symmetr" does not occur in the SoCG text of Baek–Balko.
  "centrally" occurs neither in arXiv:2506.00224v1 nor in CMU-CS-25-108. §7 of arXiv:2506.00224v1 says that the
  authors "suspect that there are symmetric constructions for all k ≥ 7" and lists a twofold symmetric 32-point
  realization without a convex 7-gon as further work. The derivation above was found during the literature search for
  this directory.

### 6.3 Sources inspected

No matching prior result (the statement for all even k, or its cases k = 8 and k = 10) was found in the sources
inspected:
- **Read in full:** Baek–Balko, "The Erdős–Szekeres conjecture revisited", SoCG 2025 (LIPIcs 332, paper 13);
  arXiv:2506.00224v1; CMU-CS-25-108; Erdős–Szekeres 1960/61 (§§1–2); the surveys of Morris–Soltan (Bull. AMS 2000),
  Bárány–Károlyi (2001) and Tóth–Valtr (2005); Szekeres–Peters 2006 (§5); Aichholzer et al., "Erdős–Szekeres-type
  games" (EuroCG 2019); Balko–Valtr (EuroComb 2015).
- **Full text searched:** Krapivin–Przybocki–Heule arXiv:2607.02958; Koshelev–Koshka arXiv:2604.20120;
  B. C. Dumitru arXiv:2512.24061v1; Balko–Scheucher–Valtr arXiv:2203.07518; Damásdi–Dong–Scheucher–Zeng
  arXiv:2312.01223; Duque–Fabila-Monroy–Hidalgo-Toscano arXiv:1602.03075; Georgiev–Gómez-Serrano–Tao–Wagner
  arXiv:2511.02864 (problem 38) and its public notebook for that problem (33- and 65-point sets); Balko
  arXiv:2502.02155; Garber–Roldán-Pensado arXiv:1801.07238; Schroeder, Zenodo 22842891 (2026); Zeng et al., SSRN
  7334758 (a cached copy); Oberwolfach Report 2024/3 ("Discrete Geometry"); the arXiv papers citing or cited by the two
  main sources.
- **Indexes:** arXiv listing searches and metadata sweeps (math.CO, cs.CG, cs.DM, math.MG); OpenAlex (35 queries, and
  the citation graphs of Erdős–Szekeres 1935, Morris–Soltan 2000, Szekeres–Peters 2006 and Erdős–Tuza–Valtr 1996);
  Semantic Scholar (partly rate-limited); Google Scholar (37 queries, and the cited-by lists of Baek–Balko,
  arXiv:2506.00224, Erdős–Szekeres 1960/61 and Szekeres–Peters 2006); zbMATH Open (6 queries); MathOverflow and
  Math.SE (16 queries); erdosproblems.com #107; Wikipedia ("Happy ending problem"); MathWorld; Crossref and
  OpenCitations; a few queries in Russian and Chinese.
- **Not inspected:** the full text of the journal version of Baek–Balko (only its abstract and reference list were
  read; it may contain the proof of Lemma 14 and remarks on symmetry); the text of the CICM 2025 chapter of
  arXiv:2506.00224 (only its reference list); Erdős–Tuza–Valtr 1996; Kalbfleisch–Stanton 1995; Valtr's invited
  abstract "The Happy End Theorem and Related Results" (2014); the books of Brass–Moser–Pach, Matoušek, Soifer and
  Kharazishvili; the 2016 survey chapter of Morris–Soltan (abstract and references only); the theses of Scheucher and
  Baek (of Subercaseaux's, only the proposal); DBLP and MathSciNet; unpublished work.

This is not a novelty claim: the statement is implied by the results credited above.

## Reproduction

From `cloud/es7-2026-10-19/results`, with Python 3 (standard library only) and a C compiler. Each step takes seconds,
except `check_set.py` on the 256-point set (about 40 s). If the default macOS SDK fails to link, add `-isysroot` with
another installed SDK. The outputs are in `logs/`, `review/logs/` and `lit/`; the `regen_*` files can be deleted.

```sh
for k in 6 8 10; do python3 SYMEVEN/construct.py $k SYMEVEN/regen_k$k.txt
  cmp SYMEVEN/regen_k$k.txt SYMEVEN/k${k}_points.txt; done
python3 SYMEVEN/verify_instance.py SYMEVEN/k6_points.txt 6 400 7
python3 SYMEVEN/verify_instance.py SYMEVEN/k8_points.txt 8 300 8
for k in 6 8 10; do python3 SYMEVEN/structure_check.py SYMEVEN/k${k}_points.txt $k; done
cc -O2 -o SYMEVEN/dfs_convex SYMEVEN/dfs_convex.c
SYMEVEN/dfs_convex SYMEVEN/k6_points.txt 7; SYMEVEN/dfs_convex SYMEVEN/k8_points.txt 9
cc -O2 -o SYMEVEN/lcs_dp SYMEVEN/lcs_dp.c && SYMEVEN/lcs_dp SYMEVEN/k10_points.txt
python3 SYMEVEN/test_algorithms.py 400 1; python3 SYMEVEN/test_dfs_c.py 150 5; python3 SYMEVEN/test_lcs_c.py 200 9
python3 SYMEVEN/negative_controls.py
python3 SYMEVEN/random_lemma_test.py 6 1500 21; python3 SYMEVEN/random_lemma_test.py 8 600 31
cc -O2 -o SYMEVEN/review/refdp SYMEVEN/review/refdp.c
python3 SYMEVEN/review/check_author_files.py SYMEVEN/k6_points.txt SYMEVEN/k8_points.txt
python3 SYMEVEN/review/check_author_k10.py SYMEVEN/k10_points.txt
cd SYMEVEN/lit
python3 crossed_all_x.py smqh_table1_16points_x10.txt 6 607 31 1,2,3,4,5,6,7,9 10
python3 crossed_all_x.py mackey_fig328_x10.txt 6 607 27 1,2,3,4,5,6,7,9 10
python3 cor15_arcs.py smqh_table1_16points_x10.txt 6; python3 cor15_arcs.py mackey_fig328_x10.txt 6
python3 build_labelled_x1.py smqh_table1_16points_x10.txt 6 607 31 1,2,3,4,5,6,7,9 regen_k8.txt
python3 build_labelled_x2.py smqh_table1_16points_x10.txt 6 607 31 1,2,3,4,5,6,7,9 regen_k10.txt
cmp regen_k8.txt smqh_crossed_k8_64points.txt; cmp regen_k10.txt smqh_crossed_k10_256points.txt
python3 check_set.py smqh_crossed_k8_64points.txt; python3 check_set.py smqh_crossed_k10_256points.txt
python3 test_check_set.py
python3 check_refdp.py smqh_crossed_k8_64points.txt smqh_crossed_k10_256points.txt
```

The remaining review computations are listed in `review/README.md`.
