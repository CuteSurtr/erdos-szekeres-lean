**Verdict: CONFIRMED** (claim `lp0-7-false-abstract`, verifier V2, 15 November 2026, 17:24-17:27 KST). Label EXACT
(abstract signotope) is correct. LP0(7) is false for the 19-point signotope W. Every number in the statement
reproduces, and so do the stated consequences for H7U(7), LR(7) and weak D(5,7) on W. Realizability of W is open, as
the claim says.

# Independent check: LP0(7) fails for a 19-point signotope

**Definitions.**
- THEORY_1115PM.md §0 and §2.1. LP0(n): if S is (5,n)-valid and r lies in no weak Δ of S, then P0 (the points ending
  no 4-cap) meets every gon. P0 is always 4-cap-free.
- n = 7: a gon is a convex hexagon. k-cap means every triple is a cap. Convex means the 4-point rule, cross-checked
  against the cup/cap split on every hexagon.
- ENV#: as in ROUND6.md.

**Code.** `/home/jay/research/data/roadmap-20261115/pm1115/v2/lp0-7-false-abstract/check_lp0_v2.py`
(`9397432a25aff51b1b6066cdeab4ce281f52d93a68f3d9a3c411d3efa00232ec`), with `v2lib.py` (`7c8b1ee0…`). Its output is
`lp0_check_all.jsonl` (`c57be467…`). It uses only the `signs` string, plus the coordinates of `r7/root7_real17.json`
for the embedding check. Enumeration is exhaustive, with integer bit masks vectorised over all 2^19 subsets. It ran in
about 1 s per file on one thread.

## Results for W = `p2/lp0cex/w19_real17_oonn.json`

The file's SHA-256 is `834da5f8…7a7e7`; the signs string's SHA-256 is `a0e6cecd…4d8d`; there are 969 triples.

- **Validity.** The signotope axiom holds on all 3,876 4-tuples (0 violations). There is no 5-cap and no convex 7-set,
  so W is (5,7)-valid.
- **The 4-caps and P0.** W has 213 four-caps, and **P0 = {0,1,2,3,16,17}**, as stated. r = 18 ends a 4-cap.
- **Hexagons.**
  - W has 714 hexagons. **47 miss P0**, and 37 of those avoid r.
  - {4,5,9,11,12,13} is a convex hexagon inside R¹. The six stated witnesses (1,2,3,4), (1,2,3,5), (0,2,7,9),
    (1,2,3,11), (1,2,3,12) and (0,2,7,13) are all 4-caps of W.
- **Rootability.** W has 13,932 weak Δs. **0 contain r = 18.** 5,833 contain l = 0, as stated, so LR(7) and weak
  D(5,7) hold on W.
- **The embedding.** W restricted to {0,1,4,…,18} has exactly the orientation signs of `r7/root7_real17.json`
  (`d9b5e6c4…`), all 680 triples. In that real set r ends a 4-cap and lies in no weak Δ: 0 of its weak Δs contain r, by
  my own enumeration. Claim `root7-real-17` is V1 CONFIRMED. By Lemma M (claim `t4-lemmas`, V2 CONFIRMED), r is then
  unrootable in W as well. This agrees with the direct count.
- **H7U(7) consequence.** U = W − r has 37 hexagons inside R¹(U). A 4-cap ending before r lies in U, so R¹(U) = R¹(W) − r.
  **ENV#(U) is empty** (0 of 2^18 subsets, exhaustive). This also follows from L2 of `t4-lemmas`.

So LP0(7) fails on W: r lies in no weak Δ, and P0 misses 47 gons.

## The two other listed models (bonus; not part of the statement's numbers)

The embedding was taken from each file's `pattern` field, where `o` marks a point of the real block.

| file | P0 | gons missed by P0 | weak Δs through r / l | ENV#(U) | embeds root7_real17 |
|---|---|---|---|---|---|
| `w19_real17_onnoooooooooooooooo.json` | {0,1,2,11,12,14,16,17} | 2 | 0 / 4,292 | 0 | yes |
| `w19_real17_oononoooooooooooooo.json` | {0,1,2,3,4,16,17} | 21 | 0 / 5,201 | 0 | yes |

Both are valid (0 violations, no 5-cap, no convex 7-set), and both refute LP0(7) as well.

**Not checked.** The search statistics "45 of the 1,530 position patterns, for all 10 blocks tested" (`lp0scan.py`).
