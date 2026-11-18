# VERIFY_NOV_BV_WEAK_STRONG: verdict on claim nov-bv-weak-strong (verifier VS, 18 November 2026, 02:45-02:48 KST)

**Verdict: CONFIRMED (EXACT), with two limits.** All numbers of (a) and (b) were reproduced with VS's own code, written
from the definitions and not from NOV's checker:
- path restrictions;
- weak-witness counts;
- no strong gon;
- the ETV7SAT colouring.

"No strong gon" was confirmed by two independent VS methods. The limits:
- VS checked the local copies NOV downloaded at 02:39; it did not re-fetch them from the Balko-Valtr page.
- The quotations from the Balko-Valtr paper and from Baek-Balko were not checked against the papers. The definition in
  `generator.cpp` was read and agrees with the claim: `findGons` splits each k-subset's interior vertices between the
  red and the blue path, so only strong gons are forbidden.

## Definitions (as in the claim)

- Lexicographic triples i<j<l. Balko-Valtr files hold one value per line: 1 = red = cap, 0 = blue = cup.
  `generator.cpp` numbers the triples lexicographically, forbids red paths with negative literals and blue paths with
  positive ones.
- ETV7SAT file: `triples_positive` = cup = blue.
- A monotone c-path on m vertices has every consecutive triple of colour c; m = 2 means any pair.
- Weak k-gon: a red path on a vertices and a blue path on u vertices, with the same first and last vertices,
  a + u = k + 2, and a, u ≥ 2. A strong k-gon also has disjoint interiors.

## Checks (V = `/home/jay/research/data/roadmap-20261115/pm1115/vs1118/nov-bv/`)

1. **Path DP and witnesses** (`V/vs_gons.py`).
   - For every pair x<y, the vertex-count sets of red and blue paths from x to y come from a DP over paths ending in an
     edge.
   - Weak witnesses are the (x, y, a, u) with a ∈ R[x][y], u ∈ B[x][y] and a + u = k + 2.
   - For each witness, all red and all blue paths are enumerated explicitly; a strong gon is a pair with disjoint
     interiors.

   | file | N | k | longest red | longest blue | weak witnesses | strong gons |
   |---|---|---|---|---|---|---|
   | 7Gon4Red_17.txt | 17 | 7 | 3 | 6 | 1: (0,10,3,6) | 0 |
   | 7Gon5Red6Blue_26 | 26 | 7 | 4 | 5 | 1: (18,25,4,5) | 0 |
   | 7Gon5Red_27 | 27 | 7 | 4 | 6 | 6 | 0 |
   | 7Gon6Red6Blue_31 | 31 | 7 | 5 | 5 | 2 | 0 |
   | 7Gon6Red_32 | 32 | 7 | 5 | 6 | 7 | 0 |
   | 7Gon_33 | 33 | 7 | 6 | 6 | 10 | 0 |
   | 8Gon4Red_23 | 23 | 8 | 3 | 7 | 2: (6,22,3,7), (7,22,3,7) | 0 |
   | 9Gon4Red_30.txt | 30 | 9 | 3 | 8 | 1: (13,29,3,8) | 0 |
   | ETV7SAT colouring27_nosig.json | 27 | 7 | 4 (cap) | 6 (cup) | **0** | 0 |

   - Everything equals the claim: 3/4/4/5/5/6/3/3, 6/5/6/5/6/6/7/8, 1/1/6/2/7/10/2/1, and 0 for ETV7SAT.
   - The claim's example is VS's first witness: red (18,22,23,25) with blue (18,19,23,24,25) in 7Gon5Red6Blue_26.
   - So the ETV7SAT 27-vertex colouring is not Balko-Valtr's 27-vertex colouring, which has 6 weak witnesses.
2. **Independent brute force for strong gons** (`V/vs_strong_bf.cpp`, C++, `strong_bf.log`).
   - It tries every k-subset and every split of its k−2 interior vertices into red and blue parts, i.e. the
     generator's own gon definition.
   - All eight files have **0 strong gons**.
   - Its longest red and blue paths, from a separate DP, equal those of check 1.
3. **Consistency with the project's weak-gon results.** The colourings that those statements constrain do contain weak
   gons of the required types:
   - 26 vertices: a (4,5) weak heptagon, as ETV7SAT item 3 requires;
   - 17 (a = 4), 23 and 30 vertices: weak gons with a = 3.
4. **Controls** (`V/vs_gon_controls.py`, seed 7, `controls.log`).
   - 300 realizable colourings: random integer point sets of 8-12 points, red = orient < 0, with k = 5 or 6.
   - In every one, four answers agree: weak k-gon (check 1), strong k-gon (check 1), strong k-gon (check 2), and an exact
     point-in-triangle brute force for k points in convex position. The longest red path also equals the longest cap
     found by brute force.
   - Outcomes: 281 with a gon, 19 without.
   - **0 mismatches.**
   - A hand-made 4-vertex colouring has a weak (3,4) 5-gon whose paths share an interior vertex, and both programs find
     0 strong 5-gons.
5. **Hashes.**
   - The local data files match the claim's SHA-256 prefixes: generator.cpp a56a2dfb, 7Gon4Red_17.txt 60b4d1f0,
     7Gon5Red6Blue_26 9135c5ef, 7Gon5Red_27 8e2a4573, 7Gon6Red6Blue_31 c9b1fec7, 7Gon6Red_32 efa71b33, 7Gon_33 afe3cce3,
     8Gon4Red_23 9203f46d, 9Gon4Red_30.txt a9b32770.
   - colouring27_nosig.json has SHA-256 b42aebe4…b9633d484.

## Files

`V/vs_gons.py` (fed99a83…a013), `V/vs_strong_bf.cpp` (ab11b87e…561b), `V/vs_gon_controls.py` (9d421ac7…b6b),
`V/vs_gons_result.json` (a472cc37…5f87, every witness with example paths), `V/strong_bf.log`, `V/controls.log`.
