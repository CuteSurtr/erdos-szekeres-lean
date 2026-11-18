# VERIFY_LOWERBOUND_E1_DDSZ28: verdict on claim lb-e1-ddsz28 (verifier VB, 15 November 2026, 20:12-20:15 KST)

**Verdict: CONFIRMED** at the claimed labels: (1) EXACT, (2) CERTIFIED computation with exactly checked realizability
clauses and PROVED soundness, (3) EXACT. All three parts were checked with VB's own code; the certificate of (2) was
re-checked by a fresh cake_lpr run. Not checked: that the 8-point block is the set of DDSZ's Theorem 11 (no comparison
with the paper) and D2's satcount sweep (COMPUTED in the claim; not needed for (2)).

## Claim (E1, filed 20:06)

S = `agl/ddsz/d28_h.txt`, 28 points built by `ddsz28.py` (L = 3,000,000, A = 30, B = 1) as an instance of the DDSZ
construction for n = 7. (1) S is in general position and has no convex 7-gon. (2) S is geometrically 7-gon-saturated:
`d28_h_geo.cnf` = `l1enc S 7` + 1,084 realizability clauses (1,075 triple and 9 parallel-pair clauses, each excluding a
sign pattern that no open cell has) is UNSAT, cake_lpr one `s VERIFIED UNSAT`. (3) The plain `l1enc S 7` is SAT: the
model `d28_h.model` satisfies all 30,108 clauses and its sign vector is realized by no point. The same canonical order
type for all 10 parameter choices (a-j); `l1enc`'s CNF byte-identical for a and h.

## Checks (work dir V = `/home/jay/research/data/roadmap-20261115/pm1115/vb/claims/lb-e1-ddsz28/`)

1. **The set.** VB rebuilt S from the stated formula with own code (blocks at L·(i, i²), i = 1..6: a point, the 5-cap,
   the 8-point block, its mirror, the 5-cup, a point; map (x, y) ↦ L(i, i²) + (30x, y)): byte-identical to `d28_h.txt`
   (SHA-256 `726c3a9e…`). The 5-cap and 5-cup blocks are a 5-cap and a 5-cup (exact orientations). VB's `geochk7`
   (`__int128`): 28 distinct points, general position, largest subset in convex position 6, and its convex-7-gon count
   is 0. **(1) confirmed.**
2. **The geometric CNF** (`V/vb_ddsz.py`, own code, exact integers):
   - `l1enc S 7` built by VB from L1's source (binary `60fee0ce…`) is byte-identical to E1's `d28_h.cnf` (`p cnf 378
     30108`, SHA-256 `79fd77b6…`), and these 30,108 clauses are exactly the first 30,108 clauses of `d28_h_geo.cnf`
     (`p cnf 378 31192`, SHA-256 `5f655526…`).
   - The other 1,084 clauses have at most 3 literals each. For each clause VB forms the excluded pattern (the negation of
     every literal: open half-planes s·orient(a,b,p) > 0 of lines through two points of S) and tests its emptiness with
     Motzkin's transposition theorem over the minimal supports (an antiparallel pair with μC_i + C_j ≥ 0, or a positively
     spanning triple with Σλ_iC_i ≥ 0, λ = the 2×2 determinants): **all 1,084 patterns are empty** (9 by a pair, 1,075 by a
     triple, exactly the claim's split). So every clause holds for every real p in general position.
   - Controls of the emptiness test: 20,000 random integer points p, each with a 3-literal pattern made of p's own signs:
     never called empty (0 false positives); 500 triangles of S with "p beyond all three edge lines", and the
     opposite-sides pattern on one line: called empty 500/500 and 500/500.
   - Soundness: for real p in general position with no convex 7-gon through p, X(a,b) = [orient(a,b,p) > 0] satisfies
     `l1enc S 7` (ABSAT8_INDEPENDENT §3 for k = 7; VB re-derived the k-generic reading in VERIFY_LOWERBOUND_E1_ABSAT7.md
     §5) and the 1,084 extra clauses (above). So UNSAT ⇒ every such p lies on a convex 7-gon through p.
   - **Fresh cake_lpr** (unit `esr-agv-vb-cake-ddsz28`, 20:14:46, heap 400 MB, LRAT streamed from
     `cert/d28_h_geo.lrat.zst`): stdout exactly `s VERIFIED UNSAT`; CNF SHA-256 `5f6555262d9932c0468401bf1a083d620c00c9ee12e3e237f016043bdcc56f82`
     and LRAT stream SHA-256 `7df0950113c33d053496171872ee567fe0dd9355b445bb2f83b70b7de130c8fc` (14,327 bytes) equal to
     `cert/certify.jsonl`. CaDiCaL log: `c Version 2.1.3`, `s UNSATISFIABLE`. **(2) confirmed.**
3. **The SAT model.** `d28_h.model` (`s SATISFIABLE`, 378 values) satisfies all 30,108 clauses of `d28_h.cnf` (VB's
   clause-by-clause check). It violates 178 of the 1,084 extra clauses, each of whose excluded patterns VB showed to be
   empty, so the model's sign vector is realized by no point p for these coordinates. **(3) confirmed.**
4. **Parameter choices.** The 10 instances `d28_a.txt` … `d28_j.txt` (27-75-bit coordinates) are all in general position
   and have **one** canonical order type (VB's Python-integer canonicalizer: hull vertex × chirality, smallest sign
   string). VB's `l1enc` CNFs for a and h are byte-identical, and equal to E1's `d28_a.cnf.zst` contents.
5. **Reading.** (2) and (3) together show that this S is geometrically saturated while the order-type-level ABSAT CNF is
   satisfiable, so ABSAT UNSAT (which gives saturation of every realization) is strictly stronger than geometric
   saturation of one realization, as the claim says. Nothing about maximality is claimed or checked.

## Files (V as above)

| file | SHA-256 |
|---|---|
| `V/vb_ddsz.py` | `aee5e13c6c53459769b84358d1f5cf05ea730fcf48b843c5b088fb09248a2f28` |
| `V/vb_ddsz.out` | `c07d5b7e4357354bfa6db0a6b9b26d7f6d6de027c5f51640bc9c745500029061` |
| `V/vb_ddsz_posctl.out` | `89bfe52da57b9e283e7fb99fd4f2b39ad76e23406bd91a38dfededec7c4f0cc6` |
| `V/vb_ddsz_canon.out` (canonical types + formula rebuild) | `c10ca0bc04d7fc2b3f6a4ae3ee754c9ca07173b21561b977f0bcd8a83e66dfd6` |
| `V/vb_d28_h.cnf` (VB's `l1enc S 7`) | `79fd77b6f97b9d9227f4b1a4b835fc33306c3cb4d4e5824949dca0ca3ce84008` |
| `V/cake/rerun.jsonl` | `bb724c5e0d57d6011c4d054e5e1f527b245003acb7025005bd4127c376594e7e` |

No proof was produced, moved or deleted; E1's files were only read.
