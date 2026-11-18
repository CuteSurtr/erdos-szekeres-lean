# VERIFY_LOWERBOUND_LN_DDSZ28_REAL: independent check of claim `lb-ln-ddsz28-real` (track VB, 16 November 2026)

**Verdict: CONFIRMED** (EXACT: own exact integer code, two independent convexity methods, positive controls).

Claim (filed by track L, LOWERBOUND_RUN_1116.md item (1)): S′ = `ln/ddsz/r29s1_S.txt` has the labelled order type and
the x-order of the 28-point DDSZ-type set S = `agl/ddsz/d28_h.txt`; with p = (604, 510), the 29-point set S′ ∪ {p}
(`ln/ddsz/r29s1_Sp.txt`) is in general position and has no convex 7-gon (largest convex subset 6); p's 378 signs
orient(a,b,p) equal X(a,b) of the model `d28_h.model`. Since S is geometrically 7-gon-saturated (claim `lb-e1-ddsz28`,
CONFIRMED earlier), geometric saturation is not an order-type invariant.

Definitions used (the claim's): orient(a,b,c) = sign det(b−a, c−a); convex k-gon = k points in convex position (every
4-subset convex); 4 points in general position are convex iff none lies strictly inside the triangle of the other three;
X(a,b) = [orient(a,b,p) > 0] is model variable 1 + lexicographic rank of (a,b) among a < b < 28.

## Inputs (paths under `/home/jay/research/data/roadmap-20261115/pm1115/`; SHA-256 recomputed here, equal to the claim)

| file | SHA-256 |
|---|---|
| `ln/ddsz/r29s1_Sp.txt` (29 points) | `53fcb719423ef14d6108e3cf30f6d139d9493efc271933e5ab64c019d907b613` |
| `ln/ddsz/r29s1_S.txt` (28 points) | `55a3ce096a55ddc1c3e33c2629519ad0de685f8562be11192c20a4cedcb877b3` |
| `agl/ddsz/d28_h.txt` (= `ln/ddsz/d28_h.txt`) | `726c3a9e9114daa38a54dab2bde0f05bf3a34d29c067d88d2700b7e842e2a35e` |
| `agl/ddsz/d28_h.model` (= `ln/ddsz/d28_h.model`) | `cb0ce33a517f4750bb122eec227e247e97d8933c43671fcd386bcf3cc83977b4` |

## Results (own code: `vb1116/claims/lb-ln-ddsz28-real/`)

| check | result |
|---|---|
| first 28 lines of r29s1_Sp.txt = r29s1_S.txt | yes |
| max \|coordinate\| of S′ ∪ {p} | 1,968,005 < 2^21 |
| collinear triples among the 29 points / among S | 0 of 3,654 / 0 of 3,276 |
| triples a<b<c<28 with different orientation sign in S and S′ | **0 of 3,276** (same labelled order type) |
| x strictly increasing in label order, in S and in S′ | yes, yes (same x-order) |
| x-position of p | 18 points of S′ to its left (between labels 17 and 18), x distinct |
| convex k-subsets of S′ ∪ {p}, method A (C++ brute force over all k-subsets, `bf.cpp`, __int128 determinants) | k=4: 15,625 / 23,751; k=5: 31,582 / 118,755; k=6: 24,125 / 475,020; **k=7: 0 / 1,560,780**; k=8: 0 / 4,292,145 |
| convex k-subsets, method B (Python, exhaustive incremental enumeration of all convex subsets, `vb_check.py`) | 4: 15,625; 5: 31,582; 6: 24,125; none of size 7; **largest convex subset 6** |
| convex k-subsets of S itself (method A) | k=6: 20,183; k=7: 0 (S is heptagon-free, as recorded) |
| p's signs vs the model: pairs a<b<28 with [orient(a,b,p) > 0] ≠ model value of variable 1 + lexrank(a,b) | **0 of 378** (all 378 variables present in the model) |

Positive controls: 10 points (i, i²), i = 0..9 (convex position): method A finds every k-subset convex (k=7: 120 / 120,
k=8: 45 / 45) and method B counts 4: 210, ..., 7: 120, ..., 10: 1; a mixed 10-point set gives intermediate counts
(k=7: 15 / 120). The two methods agree on every count for S′ ∪ {p}.

Conclusion: (a), (b) and (c) of the claim hold as stated, by exact integer computation. Together with the saturation of S
(claim `lb-e1-ddsz28`, CONFIRMED on 15 Nov, not re-checked here), the conclusion "geometric 7-gon saturation depends on
the realization, not only on the order type" follows. Not checked: the search narrative (decoding, the uniqueness of p's
x-position among signotope extensions, `realize_sig.py`); these do not affect the statement.

## Files (`/home/jay/research/data/roadmap-20261115/pm1115/vb1116/claims/lb-ln-ddsz28-real/`)

| file | SHA-256 |
|---|---|
| `vb_check.py` | `9bc1bf62ca9aa69980139bb12a9ff1146366881302fc3d384b3ff7a20939e244` |
| `bf.cpp` | `490d2887482ec977dc92de252585b7e53dad4541bb765abf47be7928df917770` |
| `vb_check.out` | `abf12df203cf0a14743020bf6b397fb13019dc9d4d82ecc92c774317108a2bef` |
| `bf_Sp.out` / `bf_S.out` / `ctrl_bf.out` | `0c946fff…` / `9325e05b…` / `28a92a6b…` |

Re-run (each under a second): `python3 -I vb_check.py r29s1_Sp.txt r29s1_S.txt d28_h.txt d28_h.model`;
`g++ -O2 -std=c++17 -o bf bf.cpp && ./bf r29s1_Sp.txt`.
