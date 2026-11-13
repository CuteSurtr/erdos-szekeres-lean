# MIRRORETV: mirror-symmetric Erdős–Szekeres sets and the Erdős–Tuza–Valtr function

Local runs on an Apple M5 Pro, 1 November 2026 (UTC).

**Statement.** Let N_mirror(k) be the largest size of a set of points in the plane, no three on a line, that is invariant
under the reflection in a line and has no k points in convex position. Let N(n,a,b) be the largest size of a set in
general position with distinct x-coordinates, with no n points in convex position, no a-cap and no b-cup (Baek's notation
for the Erdős–Tuza–Valtr function). Then for every j ≥ 2

    N_mirror(2j) = 2·N(2j, j, 2j) + 2,        N_mirror(2j−1) = 2·N(2j−1, j, 2j−1).

**Status.** The upper bounds (Theorem A) are Lean-checked for every j ≥ 2 and every mirror line, with the value of N as a
hypothesis. The lower bounds (Theorem B) are a written proof (not refereed), checked by independent reviews; their
orientation estimates are Lean-checked. With Baek's theorem this gives N_mirror(k) = 2, 4, 8, 12, 32, 46 for k = 3..8,
Lean-checked on the upper side for k = 4..8 with no SAT input. For each k ≥ 9 the conjectured value is equivalent to a
case of the ETV conjecture that no source inspected settles; 128 ≤ N_mirror(9) ≤ 226 (upper bound Lean-checked) and
188 ≤ N_mirror(10) ≤ 316.

**Credit.** N(7,4,7) = 16 and N(8,4,8) = 22 are cases of Baek's theorem P(n,4,n) (J. Baek, Eur. J. Combin. 124 (2025)
104085, arXiv:2206.04260, Theorem 1.6 in the arXiv numbering); Balko and Valtr reported both values by SAT in 2015. So
the project's mirror theorem for k = 7 (`WRITEUP/note/symmetric_es7.tex`, `thm:M`: every mirror-symmetric set of at
least 33 points in general position contains a convex 7-gon) follows from Baek's P(7,4,7) and the reduction of §2, and
N_mirror(8) = 46 from P(8,4,8); `thm:M` then needs Baek's theorem instead of the 33- and 34-point SAT certificates.
The even half of Theorem A is the argument of the note's `prop:mirror`. The lower-bound sets are the Erdős–Szekeres and
Erdős–Tuza–Valtr constructions placed symmetrically; for odd k the block sets are an instance of Valtr's construction as
described by Baek and Balko (§5). All antecedents are listed in §8.

## 0. Status of each item

| item | rigor | § |
|---|---|---|
| Theorem A (upper bounds), both parities, every mirror line, N as a hypothesis | Lean-checked | 2 |
| Theorem B (matching lower bounds), hence the two identities | written proof (not refereed); its orientation estimates Lean-checked | 3 |
| Baek's theorem P(n,4,n), used for k = 7, 8 | written proof (refereed); Lean-checked in the repository's adaptation of Baek's formalization | 4 |
| N_mirror(k) ≤ 4, 8, 12, 32, 46 for k = 4..8, every mirror line | Lean-checked, no SAT input | 4 |
| N(7,4,7) ≤ 16, hence N_mirror(7) ≤ 32, by 17-point SAT | certificate accepted by lrat-check only (four encodings) | 4 |
| N_mirror(3) = 2; lower bounds 4, 8, 12, 32, 46 | written proof (not refereed) for k = 3; exact computation | 4, 5 |
| N_mirror(k) ≥ L(k) for every k (L in §1) | written proof (not refereed) | 5 |
| explicit sets for k = 3..14 | exact computation | 5 |
| Conjecture M ⟺ P(2j,j,2j); odd analogue ⟺ P(2j−1,j,2j−1) | written proof (not refereed) | 6 |
| both follow from the ES conjecture for n = k (ETV 1996, Baek's Theorem 1.5) | written proof (refereed; ETV read through Baek); reproved in `PROOFS.md` Prop. 7.1 | 6 |
| N_mirror(9) ≤ 226, every mirror line | Lean-checked (by a review, through Baek's theorem at n = 9) | 6 |
| N_mirror(10) ≤ 316 | written proof (not refereed), resting on Baek's theorem | 6 |
| N_mirror(k) = L(k) for k ≥ 9 | conjecture | 7 |
| the ETV inequality as printed in Morris–Soltan (Bull. AMS 37 (2000), p. 443) | refuted (false as printed) | 8 |

## 1. Definitions

General position: no three points collinear. Convex position: no point in the convex hull of the others. A cap (cup) is a
sequence with increasing x whose consecutive triples are clockwise (counter-clockwise); one or two points are both.
E(n,a,b) = Σ_{i=n−b}^{a−2} C(n−2,i), and P(n,a,b) is the statement N(n,a,b) = E(n,a,b), the ETV conjecture for one
triplet 2 ≤ a,b ≤ n ≤ a+b−2; P(n,n,n) is the Erdős–Szekeres conjecture. E(2j,j,2j) = (2^(2j−2) − C(2j−2,j−1))/2 =
1, 5, 22, 93, 386, 1586 and E(2j−1,j,2j−1) = 2^(2j−4) = 1, 4, 16, 64, 256, 1024 for j = 2..7. Put L(k) = 2^(k−2) for odd k
and L(k) = 2^(k−2) − C(k−2,k/2−1) + 2 for even k: 2, 4, 8, 12, 32, 46, 128, 188, 512, 774, 2048, 3174 for k = 3..14.
**Conjecture M** is N_mirror(k) = L(k) for even k ≥ 4; its odd analogue is N_mirror(k) = 2^(k−2) for odd k ≥ 3.

## 2. Theorem A: upper bounds

**Theorem A.** For j ≥ 2: N_mirror(2j) ≤ 2N(2j,j,2j) + 2 and N_mirror(2j−1) ≤ 2N(2j−1,j,2j−1) (`PROOFS.md` §3–4).

Take the mirror line as the x-axis; R = points above it, A = points on it. Then |S| = 2|R| + |A|, |A| ≤ 2, and R ∪ A has
distinct x-coordinates (otherwise p, q, μ(p) are collinear). **Mirror lemma** (Lemma 3.1): a cap C with all points on or
above the axis, together with μ(C), is in convex position and has 2|C| − (number of endpoints of C on the axis) points.
So R has no j-cap. For odd k an axis point a lies strictly below the chord of any two points of R on either side of it,
so it can only be an endpoint of a cap of R ∪ {a}; hence R ∪ {a} has no j-cap either, and |S| ≤ 2(N − 1) + 2. The even
case is the argument of the note's `prop:mirror` (and `SYMMAX/README.md`) with N(2j,j,2j) in place of the cups–caps bound.

The note's `lem:mirror` is true, but its proof (same turn at every vertex) also needs the polygon to be simple: a closed
polygon can turn left at every vertex, wind twice and have a vertex inside the hull of the others (an integer example is
in `PROOFS.md` §3). Here the polygon is simple because its two chains are the graphs of f ≥ 0 and −f ≤ 0 over one
interval; Lemma 3.1 uses a region argument instead and allows cap endpoints on the axis. `WRITEUP` is not changed here.

**Lean** (`lean/MirrorMain.lean`, SHA-256 `ca623e55…`, 2,677 lines, namespace `MirrorOdd`). With `lake env lean` at the
repository root (Lean 4.24.0, prebuilt Mathlib; commit 5bdebbb48, whose `ErdosSzekeres/` tree and lake files equal this
branch's): 45 s, 0 errors, 121 unused-simp-argument warnings; all 16 main theorems use only `propext`,
`Classical.choice`, `Quot.sound` (`lean/MirrorMain.out`). `mirror_odd_general (j M) (hj : 2 ≤ j) (hM : ∀ n (c :
Configuration n), ¬c.HasCap (j+1) → ¬HasConvexNGon (2*j+1) (univ.image c.point) → n ≤ M) S gp sym noGon : S.card ≤ 2*M`
is Theorem A for k = 2j+1 (the Lean j is the j − 1 of the text); `mirror_even_general` is the same with `HasCap j`, `2*j`
and `2*M+2`; the `_line` versions use the reflection `lineRefl n0 n1 c` in the line n0·x + n1·y = c, n0² + n1² = 1
(every line has this form). Repository definitions: `GeneralPosition` (Mathlib's `Collinear`), `HasConvexNGon` (an
n-subset that is `ConvexIndependent`), `Configuration` (x-sorted, general position), `HasCap m` (m increasing indices,
all triples clockwise); the file defines `mir p = ![p 0, -p 1]`. Independent formalizations by reviews, importing only
Mathlib: `review/MirrorA.lean` (`theoremA_even_line`, `theoremA_odd_line`) and `review/MirrorCap.lean`
(`convex_position`, `coincidences`: the mirror lemma).

## 3. Theorem B: matching lower bounds

**Theorem B.** Let X be x-distinct, in general position, with no j-cap. If X has no convex 2j-gon, there is a
mirror-symmetric set of 2|X| + 2 points in general position without a convex 2j-gon; if X has no convex (2j−1)-gon, there
is one of 2|X| points without a convex (2j−1)-gon (`PROOFS.md` §5). With Theorem A this gives the two identities.

Construction ("far-flat"): translate X so that min x = min y = 0; with W and h the largest x and y, g the smallest x-gap
and D = W + 2, take H with H·g > h·D, R = X + (0,H) and S = R ∪ μ(R) ∪ A, where A = {(W+1,0), (W+2,0)} for even k and
A = ∅ for odd k. Key step (Lemma 5.1): if P ⊆ S is in convex position and not inside R, then P ∩ R is a cap. The axis
points must lie on the same side: with one on each side, a (j−1)-cap of R, its mirror image and both axis points can
form a convex 2j-gon. In fact maxconv(S) = max(maxconv X, 2·cap(X) + [A ≠ ∅]) (Lemma 5.2). The files in `sets/` use the
slope form (Lemma 5.3): H > s(W+2), with s the largest absolute slope in X, and axis points (−1,0), (−2,0).

**Lean**: `lean/FarFlat.lean` (`orient_wzq_neg`, `orient_uqz_neg`, `orient_sum`, `inside_triangle`, `line_misses`: the
orientation bounds of Lemma 5.1, the barycentric step, the general-position estimate) and `review/FarFlatExtra.lean`
(`a1_inside`, `gp_cross_axis`, `lemma51_core`); both import only Mathlib and use the standard axioms. The combinatorial
steps (Lemma 2.3, the counting) are not formalized.

## 4. Exact values for k ≤ 8 and the mirror theorem for k = 7

For k = 3..8, N(k, ⌈k/2⌉, k) = 1, 1, 4, 5, 16, 22 and N_mirror(k) = 2, 4, 8, 12, 32, 46. N(n,2,n) = 1 and N(n,3,n) = n−1
are elementary (a set with no 3-cap is a cup); N(7,4,7) and N(8,4,8) are Baek's theorem. **Lean**: `MirrorOdd.mirror_four`
… `mirror_eight` and their `_line` versions give |S| ≤ 4, 8, 12, 32, 46 for every finite S in general position that is
symmetric under `mir` (or `lineRefl`) and has no convex k-gon. k = 4, 5, 6 use only the mirror lemma and `capacity_cup`.
k = 7 uses `MirrorOdd.capacity16`, proved in the file from the root-namespace theorem `main` at n = 4 (the repository's
adaptation of Baek's Lean theorem, `ErdosSzekeres/Vendor/ETV/Main/Main.lean`: C(n+2,2) + 2 ≤ |S| gives a 4-cap or a
weak (n+3)-gon in any configuration) and the bridges `ListGeometry.hasCap_of_list`, `BoundaryGeometry.boundary_polygon`;
k = 8 uses `ErdosSzekeres.Omission.BaekGeometry.geometric_capacity22` (wrapper `capacity22g`; it rests on `main` at n = 5).
`mirror_seven_line` is the upper half of the note's `thm:M` (Theorem 2 of `WRITEUP/SYMMETRIC.md`). `SYMLEAN/mirror`,
committed separately, adds `reflLine_eq_lineRefl` and so proves the two mirror classes of `SYMLEAN/SymmetricReduction.lean`.

**Antecedents.** k = 4 and 5 also follow from ES(4) = 5 (E. Klein) and ES(5) = 9 (Makai; first published proof by
Kalbfleisch, Kalbfleisch and Stanton, 1970). N_mirror(6) = 12 is in `SYMMAX/README.md` and the note's `prop:mirror`;
N_mirror(7) = 32 is the note's `thm:M` (`WRITEUP/MIRROR.md`, `SYMZ`, example `SYMMAX/mirror_32points.txt`); 46 was also
obtained the same night from 23-point SAT certificates for N(8,4,8) ≤ 22 (another directory). For k = 5 there are 8-point
examples with 0 and with 2 axis points (`sets/mirror8_k5_axis*.txt`, mirror x ↦ −x, `logs/vcheck_k5.log`, run with
`--alg2`); with one axis point at most 7 points are possible.

**SAT confirmation of P(7,4,7)** at 17 points (lrat-check only; cake_lpr not run): `sat/enc.py` (CNF `ef7d33ce…`, LRAT
`2b14c13d…`; soundness proof in `sat/README.md`) and three independent encodings not committed (CNF/LRAT `8d76eab2…`/
`9ea81e17…`, `0ba68e66…`/`e16c2956…`, `28c788f5…`/`9cf38a94…`). Reviews re-checked all four with their own checkers and
encodings (the signotope clauses are not needed), and two reviews certified P(8,4,8) at 23 points by cube splits.

## 5. Constructions for every k and explicit sets for k = 3..14

N_mirror(k) ≥ L(k) for every k ≥ 3, with no axis point for odd k and two for even k (`PROOFS.md` Theorems D and 9.3):
- (a) The far-flat construction, in the slope form of Lemma 5.3, applied to the ETV set R = T_{j−2} ⊕ (… ⊕ (T_1 ⊕ T_0)),
  T_s = G(k−s, s+2) (Lemmas 6.4, 6.5; `code/construct.py`).
- (b) Symmetric blocks (`PROOFS.md` §9): the Erdős–Szekeres blocks T_i = G(k−i, i+2) on a parabola, placed so that μ maps
  block i to block k−2−i; for even k the self-paired middle block of C(k−2,k/2−1) points becomes two axis points
  (`code/mycon.py`). For odd k this is an instance of Valtr's construction for an arbitrary skeleton, which Baek and Balko
  (SoCG 2025, §4) describe without proof, citing Erdős–Szekeres 1960/61 and ETV 1996, with a mirror-symmetric skeleton
  and mirrored clusters; they do not state the mirror case.

So for odd k mirror symmetry reaches 2^(k−2), the value the ES conjecture predicts for all sets. For even k it costs
C(k−2,k/2−1) − 2 points if P(k,k/2,k) holds; this is unconditional for k = 6 (12 < 16) and k = 8 (46 < 64).

| k | file in `sets/` | points | axis | max \|coord\| | SHA-256 | largest convex subset | checks |
|---|---|---|---|---|---|---|---|
| 3 | — (e.g. (0,1), (0,−1)) | 2 | 0 | 1 | — | 2 | trivial |
| 4 | `mirror_S_k4.txt` | 4 | 2 | 2 | `ce7a2b04…` | 3 | A, B |
| 5 | `mirror_S_k5.txt` | 8 | 0 | 28 | `8c4e2918…` | 4 | A, B, L |
| 6 | `mirror_S_k6.txt` | 12 | 2 | 66 | `39a0b847…` | 5 | A, B, L |
| 7 | `mirror_S_k7.txt` | 32 | 0 | 941 | `24533a97…` | 6 | A, B, L |
| 8 | `mirror_S_k8.txt` | 46 | 2 | 2,639 | `0bcade4f…` | 7 | A, B, L |
| 9 | `mirror_S_k9.txt` | 128 | 0 | 30,704 | `df042137…` | 8 | A, B, L |
| 10 | `mirror_S_k10.txt` | 188 | 2 | 88,184 | `c019b1d2…` | 9 | A, B, L |
| 11 | `mirror_S_k11.txt` | 512 | 0 | 905,322 | `7835ecb0…` | 10 | A, B, L |
| 12 | `mirror_S_k12.txt` | 774 | 2 | 2,638,302 | `76ce5501…` | 11 | A, B, L |
| 13 | `blocks_S_k13.txt` | 2048 | 0 | 3.3·10^19 | `55f33e7a…` | 12 | V, K |
| 14 | `mirror_S_k14.txt` | 3174 | 2 | 75,356,730 | `fcc0f71d…` | 13 | A, L |

A: `code/maxconv_a.c` (angular DP, 128-bit; tests all triples for collinearity and the symmetry; re-checks a witness).
B: `code/maxconv_b.c` (cap + cup DP, GMP, O(n^4)). L: `code/lemma_check.py` (checks exactly the slope condition (*) of
Lemma 5.3, implied by H > s(W+2) and sufficient for its proof, then evaluates its bound; general position comes from A).
V: `code/vcheck.c` (cap + cup DP, 128-bit). K: the hypotheses of the block lemma (Lemma 9.1) hold exactly, which proves
the bound without search. Logs: `logs/*_all.log`, `logs/vcheck_k13.log`. `code/test_methods.py`: 300 random sets and
360 small subsets against a brute force, 360 larger subsets across three methods, 0 mismatches. Controls (axis points on
both sides, or an extra mirror pair) give a convex k-gon. `construct.py` and `mycon.py` reproduce the files byte for byte;
the upper halves are `sets/etv_R_k*.txt`.

## 6. Conjecture M and the ETV conjecture; upper bounds for k = 9, 10

By Theorems A, B and C (`PROOFS.md` Theorem D), Conjecture M for k = 2j is equivalent to P(2j,j,2j), i.e.
N(2j,j,2j) = (2^(2j−2) − C(2j−2,j−1))/2, and the odd analogue for k = 2j−1 to P(2j−1,j,2j−1), i.e. N(2j−1,j,2j−1) =
2^(2j−4). Nothing mirror-specific remains. Both follow from the Erdős–Szekeres conjecture for n = k (ETV 1996; Baek's
Theorem 1.5 in the arXiv numbering; reproved as Prop. 7.1); for odd k also directly, as N_mirror(k) ≤ ES(k) − 1. In
Lean, a proof of the ETV bound in the `Configuration` model gives the mirror bound at once through `mirror_even_general`
or `mirror_odd_general`.

The Erdős–Szekeres recursion N(n,a,b) ≤ N(n,a−1,b) + N(n,a,b−1) (Lemma 8.1: the 1935 cups–caps argument with the n-gon
condition carried along), the cups–caps bound and Baek's N(n,4,n) = C(n−1,2) + 1 give N(9,5,9) ≤ 29 + 84 = 113 and
N(10,5,10) ≤ 37 + 120 = 157, hence **128 ≤ N_mirror(9) ≤ 226** and **188 ≤ N_mirror(10) ≤ 316**
(`tools/pascal_bounds.py`). Without Baek's theorem the bounds are 240 and 332 (the note's `prop:mirror` gives 332). A
review proved the bound for k = 9 in Lean: `lean/MirrorNine_append.lean`, appended to `MirrorMain.lean` (concatenation
SHA-256 `d0831d4d…`), proves `C12Check.config_capacity113` (any `Config` without 5-cap and 9-gon has at most 113 points:
one split, Baek's `main 6` and the cups–caps theorem `cap_cup`), its geometric form `capacity113`, and `mirror_nine`,
`mirror_nine_line` (|S| ≤ 226); 38 s, 0 errors, standard axioms (`lean/MirrorNine.out`). For k = 10 the bound 157 was
checked in Lean only in Baek's combinatorial model, on a port that is not committed.

## 7. What is open

- P(9,5,9) (is N(9,5,9) = 64?) and P(10,5,10) (is N(10,5,10) = 93?), so N_mirror(9) ∈ [128, 226] and N_mirror(10) ∈
  [188, 316]; likewise every k ≥ 9. ETV cases settled in the sources inspected: n ≥ a+b−3 (cups–caps), a = 4 or b = 4
  (Baek), and n ≤ 6 (inferred here from ES(5) = 9, ES(6) = 17 (Szekeres–Peters 2006) and Baek's Theorem 1.5; for n = 6
  also Balko–Valtr's SAT computations); Schroeder's (7,5,6) = 25 (Zenodo, 2026) is unreviewed. SAT at 65 or 94 points is
  out of reach, and Baek's method is developed for a = 4 only.
- Whether a 32-point 7-gon-free mirror set with two axis points (15 pairs) exists; Theorem A allows it. Two 25-minute
  annealing runs found none, which proves nothing.
- Neither construction, nor the combinatorial part of Theorem B, is in Lean.

## 8. Literature and credit

**Antecedents.** Baek's theorem and his Lean formalization, adapted in `ErdosSzekeres/Vendor/ETV` (Apache-2.0); the
bridge to real convex polygons (`ErdosSzekeres/Omission/ListGeometry`, `BoundaryGeometry`, `BaekGeometry`) is adapted
from M. Schroeder's archive (MIT; `docs/THIRD_PARTY.md` at the repository root). Balko–Valtr (ENDM 49 (2015) 425–431;
EJC 66 (2017) 13–23): N(4,7,7) = 16 and N(4,8,8) = 22 in their notation (our N(7,4,7), N(8,4,8)), by SAT over
pseudolinear colourings. Erdős–Tuza–Valtr (EJC 17 (1996) 519–532; not accessed, read through Baek, Balko–Valtr and
Baek–Balko): the conjecture, its lower-bound construction (Theorem C), its equivalence with ES (Prop. 7.1).
Erdős–Szekeres 1935 (cups–caps theorem; Lemmas 6.1, 8.1) and 1960/61 (block construction; Lemma 6.2). Valtr's
construction for an arbitrary skeleton (Baek–Balko, SoCG 2025, LIPIcs 332, 13:1–13:15, §4) gives the odd-k lower bound.

**Sources inspected** (1 November 2026; 52 logged searches of arXiv, OpenAlex, Semantic Scholar, Zenodo, OEIS and the
web, `lit/searches.tsv`): Baek 2025 (arXiv v2 read in full) and his Lean repository; Balko–Valtr 2015; Baek–Balko SoCG
2025; Morris–Soltan 2000; Subercaseaux–Mackey–Qian–Heule, arXiv:2506.00224, and E. Mackey's thesis CMU-CS-25-108
(rotations only); Koshelev–Koshka, arXiv:2604.20120, §9.1.2 (axially symmetric sets of 18 or more points contain an
*empty* convex hexagon; ASP, no certificate); Krapivin–Przybocki–Heule, arXiv:2607.02958; Mojarrad–Vlachos 2016 (their
h(m,4) is a different quantity); Schroeder, Zenodo 10.5281/zenodo.22842891; B. C. Dumitru, arXiv:2512.24061 (two search
hits; no symmetric results, see `C2FINAL` §7); `LIT/RELATED.md` (which does not cite Baek 2025); OEIS (4, 12, 46, 188,
774: no entry; 1, 5, 22, 93, 386 is A000346, with no geometric comment).

No matching prior result was found in these sources for: the identities of the Statement, the far-flat lower bound, the
odd-k reduction with axis points, the even construction with two axis points, the equivalences of §6, and the derivation
of N_mirror(7) = 32 and N_mirror(8) = 46 from Baek's theorem. The odd-k lower bound 2^(k−2) itself is an instance of
Valtr's construction (§5). Not inspected: the ETV paper, the journal texts of Baek 2025, Balko–Valtr 2017 and Baek–Balko
2026 (paywalled), and sources not in English. This is not a novelty claim.

**Corrections.** Morris–Soltan print "m(n,k,l) ≤ Σ_{i=n−l}^{k−2} C(k−2,i)" as proved by ETV; with k = l = n this would
give ES(n) ≤ 2^(n−2), so it is false as printed (two copies checked); the lower bound is presumably meant. The sentence
"Baek's theorem is false for pure colorings" in `docs/RELATED_WORK_2026-10-14.md` is wrong as stated: Baek's Theorem 2.7
holds for all colourings with weak gons; only the strong-gon version fails.

## 9. Independent checks

Separate adversarial reviews (1 November 2026) used their own code; their committed files are in `review/`. None
refuted a claim.
- Theorem A and the mirror lemma: read line by line; independent Lean proofs (§2); exact tests on 66,322 caps and 3,679
  random mirror sets. Theorem B: read line by line; `review/FarFlatExtra.lean`; Lemma 5.2 tested on 7,000 random mirror
  sets and on the mirror sets of all 6.74 million x-distinct sets in general position on G×G grids, G = 6, 7, 8; H = 1 or
  axis points on opposite sides make the test fail.
- Lean file: recompiled with the same output; `review/ReplayRepo.lean` re-checks its 497 repository constants in the
  kernel; other reviews replayed all 19,394 constants from an empty environment (no LRAT, CNF or catalog module among
  them) and restated the bounds with Mathlib's `ConvexIndependent` and `Collinear`.
- Baek's proof (arXiv v2) was re-read line by line by three reviews: only typos. Publication confirmed through Crossref
  (DOI 10.1016/j.ejc.2024.104085); the journal numbering of Theorem 1.6 was not checked.
- Explicit sets: two or three independently written exact programs per far-flat set, brute force for k ≤ 8 (none of the
  260,932,815 8-subsets of the 46-point set is convex), byte-for-byte rebuilds. The k = 13 set comes from a review that
  built block sets for k = 3..14 (one DP and the block-lemma hypotheses at k = 13); re-run here with the same output.
- Equivalence with ETV, Prop. 7.1, the Pascal bounds and the k = 5 examples: confirmed.

**Findings, applied in `PROOFS.md`.** N_mirror(8) = 46 is a corollary of Baek's theorem, not a special case; Baek's
paper is published; a loose phrase in Theorem A was reworded; Lemma 6.1 lacked the case of a cap inside the right part;
the 17-point encodings do not need the signotope axioms; `lemma_check.py` does not test general position (A does) and
checks the slope condition (*) rather than H > s(W+2) (both hold for every file).

**Late reports.** The last two reviews also found no error: one re-derived the even identity and re-checked the sets for
k = 10, 12, 14 (two programs, exact structural check of Lemmas 6.4 and 5.3); the other re-checked the block sets for
k = 3..12 of the working notes (not committed here). Their wording fixes (even k ≥ 4, arXiv numbering) are applied.

## Reproduction

From `cloud/es7-2026-10-19/results` (Lean 4.24.0 with the repository's prebuilt Mathlib and the imported modules built,
e.g. `lake build ErdosSzekeres.Omission.BaekGeometry ErdosSzekeres.ConvexCycleCuts`; CaDiCaL 3.0.1; lrat-check):

```sh
(cd ../../.. && for f in lean/MirrorMain lean/FarFlat review/MirrorA review/MirrorCap review/FarFlatExtra review/ReplayRepo
   do lake env lean cloud/es7-2026-10-19/results/MIRRORETV/$f.lean; done)
cat MIRRORETV/lean/MirrorMain.lean MIRRORETV/lean/MirrorNine_append.lean > MirrorNine.lean   # SHA-256 d0831d4d...
(cd ../../.. && lake env lean cloud/es7-2026-10-19/results/MirrorNine.lean)
cd MIRRORETV/code && cc -O2 -o maxconv_a maxconv_a.c && cc -O2 -o longcap longcap.c && cc -O2 -o vcheck vcheck.c \
   && cc -O2 -o maxconv_b maxconv_b.c -lgmp && cd ../..
python3 MIRRORETV/code/construct.py 10 1.0 out        # byte-identical to sets/mirror_S_k10.txt and etv_R_k10.txt
MIRRORETV/code/maxconv_a MIRRORETV/sets/mirror_S_k10.txt; MIRRORETV/code/maxconv_b MIRRORETV/sets/mirror_S_k10.txt
python3 MIRRORETV/code/lemma_check.py MIRRORETV/sets/mirror_S_k10.txt MIRRORETV/sets/etv_R_k10.txt
python3 MIRRORETV/code/mycon.py 13 out/b13.txt         # byte-identical to sets/blocks_S_k13.txt
MIRRORETV/code/vcheck MIRRORETV/sets/blocks_S_k13.txt --mir y --k 13
python3 MIRRORETV/code/test_methods.py 300 MIRRORETV/sets/mirror_S_k10.txt; python3 MIRRORETV/code/negative_controls.py
python3 MIRRORETV/sat/enc.py 17 7 n17_K7.cnf && cadical --lrat --binary=false n17_K7.cnf n17_K7.lrat
lrat-check n17_K7.cnf n17_K7.lrat
python3 MIRRORETV/tools/pascal_bounds.py; python3 MIRRORETV/tools/check_formulas.py
```

`maxconv_b` needs GMP. `lemma_check.py`, `test_methods.py` and `negative_controls.py` call the binaries in `code/`;
`negative_controls.py` writes its control sets to `code/controls/`.
