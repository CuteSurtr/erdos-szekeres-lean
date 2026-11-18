**Verdict: CONFIRMED** (claim `root7-m17-abstract`, verifier V1, 15 November 2026, 14:01 KST). Label supported: EXACT, for
the abstract signotope only. Realizability was not tested (the claim says so too). The CNF was not regenerated (see §1).

# VERIFY_ROOT7_M17: ROOT(7) fails on an abstract 17-point (5,7)-valid signotope

## Claim checked (filed by T3)

The CaDiCaL 2.1.3 model of `root7_m17.cnf` (round-6 encoder `root_cnf.py 7 17`, SHA-256 `44626ab2…58f154d5`) decodes to
a signotope S on 0..16 with no 5-cap and no convex 7-gon; r = 16 ends a 4-cap (109 four-caps end at r); U = S − r has no
weak Δ A (4-cap-free, meeting every convex hexagon of U) with A + r 4-cap-free. On the same S: CONJ-TS′(7) fails at
|S| = 17 (0 terminal-safe weak Δs); ENV#(7) fails at |U| = 16 (S − r) and |U| = 17 (S); weak D(5,7) holds on S (7,736
weak Δs, e.g. {0,2,4,5}); l = 0 starts 25 four-caps, S − l has 3,741 left-rooted and 3,263 initial-safe weak Δs, so the
rooted left-or-right disjunction LRR(7) holds on S.

## Definitions (from the records)

`ROUND6.md` "Definitions" (ROOT, ENV#, P4, ⊑, ↑P4, weak Δ; gon = convex (n−1)-gon, here hexagon); `CONJTS_TEST.md` §2
(terminal-safe); `VERIFY_ATN_MAIN.md` (mirror form); `DELTA2N20261113/README.md` §2 (signotope, convex k-set by the
4-subset rule).

## 1. Model and CNF (`v1_model_check.py`, own code)

- `t3/cnf/root7_m17.cnf` SHA-256 `44626ab284896424e7d1d271f4c6bec94921305053f415298e3928bd58f154d5` (equals the claim);
  header `p cnf 13448 251616`, comment `ROOT(7) failure, |S|=17, rows=63019` (63,019 = Σ_{k≤11} C(16,k), the encoder's
  row count for n = 7, m = 17).
- Log `t3/runs/r7m17_s1.log` (`ef88d01d…`): `s SATISFIABLE`, `--seed=1`. A token-stream parser reads every clause:
  **all 251,616 clauses are satisfied** by the v-lines, and all 13,448 variables are assigned.
- Variables 1..680 decode (true = '+') to exactly the sign string of `t3/models/root7_m17_s1.json` (`8d6bedc1…`).
- Not done: regenerating the 108 MB CNF with `root_cnf.py 7 17` (the Python encoder needs about 1 GB, over V1's budget).
  The mathematical claim does not depend on it: every property below is computed from the decoded signs alone.

## 2. Exhaustive check (`v1/lib/v1_forms.py` with `v1lib.py`, own code, written before reading T3's tools)

k-caps by "every triple a cap" (consecutive form asserted equal); convexity by the 4-subset rule with the cap/cup split
asserted equal; all 2^17 subsets of S, 2^16 of U = S − r and 2^16 of S − l enumerated.

| quantity | V1 | claim / T3 |
|---|---|---|
| signotope violations / 5-caps / convex 7-gons | 0 / 0 / 0 | 0 / 0 / 0 |
| 4-caps / ending at r / starting at l = 0 | 163 / 109 / 25 | 163 / 109 / 25 |
| convex hexagons in S / U / S − l | 229 / 205 / 192 | 229 / 205 / 192 |
| **rooted weak Δs of U (ROOT at r)** | **0** | 0 |
| terminal-safe weak Δs of U (CONJ-TS′) | 0 | 0 |
| ENV# Δs, U = S (P4 19, ↑P4 30) / U = S − r (P4 9, ↑P4 16) | 0 / 0 | 0 / 0 |
| weak Δs of S (weak D(5,7)), minimum example | 7,736, {0,2,4,5} | 7,736, {0,2,4,5} |
| weak Δs of U / of S − l | 9,562 / 6,637 | — |
| left-rooted / initial-safe weak Δs of S − l | 3,741 / 3,263 | 3,741 / 3,263 |
| same via the reflected order type (4-caps at r′ / rooted / terminal-safe) | 25 / 3,741 / 3,263 | — |

So S is a (5,7)-valid signotope whose rightmost point ends a 4-cap and for which ROOT(7) fails; CONJ-TS′(7) fails at
|S| = 17 and ENV#(7) fails at |U| = 16 and 17; weak D(5,7) and both mirror forms hold, so LRR(7) holds on S.

## 3. Consistency control against the certified ranges (`v1_sub_controls.py`)

ROOT(7) is CERTIFIED for |S| ≤ 14 and ENV#(7) for |U| ≤ 13 (`ROUND6.md`), so they must hold on sub-signotopes of S.
15 random 14-point subsets keeping r = 16 as the rightmost point: r ends a 4-cap in all 15, and each has 257-928 rooted
weak Δs. 15 random 13-point subsets: each has 306-1,646 ENV# Δs. No conflict with the certificates.

## 4. Comparison with T3 (read after §1-§3)

`t3/runs/root7_m17_s1.forms.json` (`980e1efb…`) and `tools/decode.py`, `check_model.py` (plus `check_forms.py`,
`t3lib.py`, read for an earlier claim). Same definitions; every count in T3's output equals V1's. T3's model check reads
one clause per line; V1's parses the token stream; both find 0 violated clauses.

## Not checked

- Realizability of S by points (open; not claimed).
- ROOT(7) at 15 and 16 points (undecided in the records; this witness has 17).

## Code and outputs (`/home/jay/research/data/roadmap-20261115/pm1115/v1/`)

| file | SHA-256 |
|---|---|
| lib/v1lib.py | `bfeed7ee2837629d9f82a8069fb7023f0ac2a3c4ce967e19c65c8d3680d3d577` |
| lib/v1_forms.py | `2cd184a78a1e8f1192f1a0fafb647b7a9544e6593a4deab06c0fde1aa94b6ae8` |
| root7-m17-abstract/v1_model_check.py | `76bc2f8695a8f2460d1f294e1e38d56bee31e36ce4f5da49a9c1d85b09503b4d` |
| root7-m17-abstract/v1_sub_controls.py | `779c80aad82381cba248a496db6376650bd2128a4bbbe19ff5f24fbeb592a164` |
| root7-m17-abstract/v1_forms.out | `ddc640b58391d1367ae48deda908bd9cb5f97da4076fbd920ac8d7d4b5e81509` |
| root7-m17-abstract/v1_model_check.out | `307f9109b61243309d2e6c5880847171dd0c8950fc3bcc11262ca9780c325a86` |
| root7-m17-abstract/v1_sub_controls.out | `c736b0eafcf6a103c97eac80395181481440b75f02505fb2967892762e56b9a9` |

Rerun (seconds, one thread): `python3 -I v1_model_check.py <cnf> <log> <json> 17`; `venv python -I lib/v1_forms.py
<json> 7`; `venv python -I v1_sub_controls.py <json> 7`. No git action, no unit, no other repository file written.
