**Verdict: CONFIRMED** (claim `leftsat-r7blocks`, filed by P2; verifier V3, 15 November 2026, 17:33-17:40 KST). Label
CERTIFIED: all 10 known right-hostile (5,7)-valid 17-point blocks are left-saturated. The result is now certified
twice:
- by the filer's CNFs and proofs, whose cake_lpr runs I repeated;
- by **my own independently written CNFs and my own LRAT certificates**.

# Independent check: left saturation of the 10 right-hostile (5,7) blocks

**Statement.** For each block B, no (5,7)-valid signotope contains B together with a point to the left of min B.
Consequences:
- every valid superset of B has the same leftmost point as B;
- left-gluing tests on these blocks are vacuous;
- an LR(7) failure that contains one of these blocks has l(W) = l(B).

The blocks:
- `r7/root7_real17.json` (real);
- `t1/r7c17/feasible/m17_it4_real.json` (real);
- `r7/root7_m17_s1.json`;
- `t4/cegarmodels/r7c17_it{2,3,7,8}.json` and `r7cg17_it{1,2,3}.json`.

## 1. The blocks themselves (own code `v3_leftsat.py`; THEORY_1115PM.md §0, n = 7)

All 10 blocks have 17 points.

| check | result, all 10 blocks |
|---|---|
| signotope violations | 0 |
| 5-caps | 0 |
| convex 7-sets | 0 |
| r ends a 4-cap | yes |
| 4-caps | 161-170 |
| convex hexagons of U | 205-314 |
| **weak Δs of B containing r** (subsets A of U meeting every gon of U with A + r 4-cap-free, all 2^16) | **0**, so right-hostile as stated |

## 2. My own CNFs: written from the definition, CERTIFIED 10/10

Encoding: the new point is label 0, and the block is relabelled 1..17.
- Variables are all 816 triples (true = cup) plus cv for all 3,060 4-subsets.
- Unit clauses fix every block triple.
- The signotope axiom is imposed on every 4-subset.
- **No 5-cap:** for every 5-subset containing 0, at least one of its 10 triples is a cup. This is the all-triples form,
  unlike the filer's consecutive-triple clause; the two are equivalent under the axiom.
- cv(Q) ↔ (s1 = s2 ∧ s3 = s4) on every 4-subset.
- **No convex 7-set:** for every 7-subset containing 0, some cv is false.
- Soundness: a valid extension satisfies everything with cv equal to actual convexity. Subsets of B need no clauses,
  because §1 shows B is valid.
- Size: 3,876 variables and 64,396 clauses.

Certification:
- The house `certify_cnf.sh` ran at heap 300 in unit `esr-agy-v3-leftsat` (CPUQuota 15 %, MemoryMax 400M, swap 0),
  17:35:40-17:36:31.
- **Result: CaDiCaL 2.1.3 UNSAT and cake_lpr exactly one `^s VERIFIED UNSAT$` line, for all 10.**
- LRATs are 706-724 KB, kept as zstd in `cert/`; their SHA-256 are in `cert/certify.jsonl`.

**Controls (own encoder; each SAT model re-checked against every clause and decoded to a (5,7)-valid signotope).**

| block | expected | result |
|---|---|---|
| mirror of root7_real17 | SAT, as the claim says | SAT; 0 falsified clauses; 18-point model valid |
| root7_real17 minus its leftmost point (16 points) | SAT (the deleted point is a witness) | SAT; model valid |
| m17_it4_real minus its leftmost point | SAT | SAT; model valid |

## 3. The filer's certificates (`regen_cake.sh`, unit `esr-agy-v3-lsregen`, 17:37)

- **Regeneration:** all 10 CNFs regenerate byte-identically with `leftsat_cnf.py <block> 7 out`.
  - This needs numpy, so I ran it with the house venv Python (`regen/regen_venv.txt`).
  - The `regen_eq_file=0` column in `regen/regen.tsv` is from a first attempt with system python3, which lacks numpy.
    The generator failed there, so that column is void.
- **Hashes:** each CNF SHA-256 equals `p2/leftsat/cert/certify.jsonl`, and so does each decompressed LRAT SHA-256.
- **My cake_lpr re-run** on each kept proof (heap 300; decompressed copy deleted afterwards): exactly one
  `s VERIFIED UNSAT` line, 10/10.

## 4. The consequences

They follow directly.
- If a valid superset W of B had a point p < min B, then B ∪ {p} ⊆ W would be valid, against §2.
- So min W = min B, and left-gluing CNFs for these blocks are unsatisfiable in their base.

## Files (`/home/jay/research/data/roadmap-20261115/pm1115/v3/leftsat-r7blocks/`)

| file | SHA-256 |
|---|---|
| `v3_leftsat.py` | `c3b10172b4f8feb3c2cde949ef07d927375016a18b320846df8f462218108f14` |
| `v3_modelcheck.py` | `320683a350f641fdf1102ef1d3bef34ddff679ff616ea54a4c4b47dff74cb7ef` |
| `run_all.sh` | `752fac1d…af9` |
| `regen_cake.sh` | `4e9fbaa6…bee` |
| `blocks.jsonl` | `659fa585…7c93` |
| `exact_lines.txt` | `bba86e01…81b7` |
| `cert/certify.jsonl` | `9e034b04…4443` |
| `ctl/modelcheck.jsonl` | `9b16aea4…d8afb8d` |
| `regen/regen.tsv` | `d41ea5d3…87e2` |

The CNFs are in `cnf/` and the kept LRATs in `cert/*.lrat.zst`.
