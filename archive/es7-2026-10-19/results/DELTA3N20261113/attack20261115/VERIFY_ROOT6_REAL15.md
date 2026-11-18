**Verdict: CONFIRMED** (claim `root6-real-15`, filed by T1; verifier V3, 15 November 2026, 13:37-13:40 KST). Label
EXACT is correct: **ROOT(6) is false for a real 15-point set**, checked from the integer coordinates alone. Every
part of the statement holds.

# Independent check: a real 15-point counterexample to ROOT(6)

**Claim.** The integer point set P in `pm1115/t1/root6_real15.json` (SHA-256 `28c72627…2cf0`) has the following
properties:
- it has 15 points, x strictly increasing and no three collinear;
- it has no 5-cap and no convex hexagon;
- its rightmost point r (index 14) ends a 4-cap, and 37 four-caps contain r;
- U = P − r has no weak Δ A (4-cap-free and meeting every convex pentagon of U) with A + r 4-cap-free;
- counts: 86 four-caps, 37 containing r, 254 convex pentagons in U, 0 rooted weak Δs.

Optional checks requested:
- the file's sign string equals the orientations of P;
- it also equals `cg15/feasible/m15_it8.json`, which is a model of `root6_m15.cnf`.

**Definitions used.** ROOT(n) from [ROOT6_MAIN.md](ROOT6_MAIN.md), with n = 6.
- orient(p,q,r) = (q − p) × (r − p), computed exactly in Python integers.
- For x-sorted a < b < c, the triple is a cap iff orient < 0. A k-cap: every triple is a cap.
- Convex position: no point of the k-set lies strictly inside a triangle of three others. This is tested directly
  on each k-set (Carathéodory, general position), not through a 4-subset table.

## Results (own code, run before reading T1's tools)

| check | result |
|---|---|
| file SHA-256 | `28c72627dbce0438ed4bd36a1bd8904ee2c118087645a94aa9d759b210ce2cf0`, equal to the claim |
| x strictly increasing / collinear triples | yes / 0 of 455 |
| 5-caps | 0 of 3,003 5-sets |
| convex hexagons | 0 of 5,005 6-sets, geometric. A second method, the sign rule s(abc) = s(abd) ∧ s(acd) = s(bcd) on every 4-subset, also gives 0. |
| 4-caps / containing r | 86 / 37, equal to the claim |
| convex pentagons of U | 254 by both methods, equal to the claim |
| **rooted weak Δs, exhaustive over all 2^14 subsets of U** | **0**, equal to the claim. For information: U has 992 weak Δs without the condition on r. |
| sign string of the file = orientations of P | yes. Its SHA-256 is `ac822a46…161b`, equal to the claim. |
| sign string = `cg15/feasible/m15_it8.json` | yes |
| m15_it8 is a model of `root6_m15.cnf` (`6bd7e8b9…be7`) | yes. I set every auxiliary variable to its defining condition, in root_cnf.py's variable order (convex 4-sets, gons of U, rooted triples, 4-caps of U). The resulting full assignment falsifies 0 of the 58,503 clauses. |

**Positive control.** For each p in U, P − p is a real (5,6)-valid 14-point set in which r still ends a 4-cap. ROOT(6) is
CERTIFIED for m ≤ 14 (ROOT6_MAIN.md), so each of these must have a rooted solution. My search finds 13-48 per p, in all
14 cases. So the search does find solutions where they must exist, and P is point-minimal for the failure. Together with the
certificates, 15 is the exact threshold for real sets.

**Comparison with T1's tools** (read after my run).
- `t1/tools/indep_coords.py` (`e4edd44d…253a`) tests convex position by hull size with Andrew's monotone chain. That
  is a third method, different from both of mine.
- `t1/tools/t1lib.py` `root_check` (`255b5248…3a`) works from the signs, using chirotope triangle containment.
- The claimed counts 86 / 37 / 254 / 0 equal mine. No difference to explain.

**Extra, not part of the claim.** At 13:38, `t1/real/` held 21 files `m15_it*_real.json`, not the 13 named in the
claim, because the CEGAR run continues. My checker reports a ROOT(6) failure for all 21:
- each has x increasing, no collinear triple, 0 five-caps, 0 hexagons and 0 rooted weak Δs;
- 78-88 four-caps, 29-39 of them containing r;
- 254 or 262 convex pentagons in U.

These extra sets were not filed as claims, so they are listed here only as my check's output (`v3_extra.out`).

**Scope.**
- The statement concerns this point set only. ROOT(6) was the rooted form that survived on S19′ and on the real
  13-point CONJ-TS′(6) sets (ROOT6_MAIN.md), and it is now refuted for point sets at n = 6.
- No implication for weak D(5,6), weak D(5,7), weak D(5,8) or any ES bound is claimed or checked here.

## Code and outputs (`/home/jay/research/data/roadmap-20261115/pm1115/v3/root6-real-15/`)

| file | SHA-256 |
|---|---|
| `v3_root_real_check.py` (main check plus control, 0.5 s) | `b26b36f7a322801f301c5448b45798a1dcdcf8184e56143cb915d3ddc8fbef43` |
| `v3_root_real_check.out.json` | `a4db2afad0ad5b172f2378d91e5a22d36dce41b3c4e8251a2d1e557ec669fd2d` |
| `v3_extra.py` (sign-rule cross-check; the 21 extra files) | `253011e790f713def51a117f57c3b14f6b75bf48d5def456525f72932c09573a` |
| `v3_extra.out` | `a01242d376433bd6014bf5a4fc5fcb4de452ce51d6cbe3e9f40941e848f5cedb` |

Input: `cg15/feasible/m15_it8.json` file SHA-256 `c208e734…89b3`.

Re-run: `python3 -I v3_root_real_check.py $T1/root6_real15.json $T1/cg15/feasible/m15_it8.json
<root6_m15.cnf>`, with `T1=/home/jay/research/data/roadmap-20261115/pm1115/t1` and the CNF at
`round6/mainsession/root6/cnf/root6_m15.cnf`.
