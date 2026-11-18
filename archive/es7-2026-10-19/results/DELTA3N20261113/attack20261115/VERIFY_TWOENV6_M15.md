**Verdict: CONFIRMED** (claim `twoenv6-m15`, verifier V1, 15 November 2026, 16:06 KST). TWO-ENV#(6) in the hypothesised
form holds for every signotope with 15 points (CERTIFIED: T3's cake_lpr run; V1 checked the encoder, regenerated the CNF,
matched the proof hash and tested the CNF semantically, but did **not** re-run cake_lpr, whose 1,300 MB heap exceeds V1's
400 MB budget). With the other sizes it holds for all signotopes and all point sets; |S| = 14 is covered by T3's direct
certificate with the same encoder (checked here), not by `tspm6-14` (V2: NOT CONFIRMED). [superseded 15 Nov pm (C1
issue 4; note by H1, not by V1): V2 changed `tspm6-14` to CONFIRMED at 16:53:54; the direct certificate still covers 14,
so this verdict is unaffected]

# VERIFY_TWOENV6_M15: TWO-ENV#(6), hypothesised form

## Claim checked (filed by T3)

If S is (5,6)-valid with |S| = 15, r ends a 4-cap and l starts a 4-cap, then U = S − r has an ENV# Δ or V = S − l has a
mirror-ENV# Δ. `te6_m15.cnf` (encoder `t3/tools/tenv_compact.py 6 15`) is UNSAT with a cake_lpr-accepted LRAT. Other
sizes: ≤ 12 from `env6-le11`, 13 and 14 from TS±(6) by lemma L2 (and directly with the same encoder), ≥ 16 vacuous. So
TWO-ENV#(6) is true for all signotopes, strictly weaker than TS±(6) (false at 15) and still implies LR(6).

## Definitions

TWO-ENV#(n): `pm1115/t4/candidates.md` K2′ (here with both hypotheses). ENV# Δ: `ROUND6.md` Definitions. Mirror-ENV#:
ENV# of the reflected V (labels reversed, signs kept; caps stay caps).

## 1. Encoder soundness (`tenv_compact.py`, SHA-256 `4c408fe7…c573`), checked by reading

Put every auxiliary variable at its intended value for a counterexample S:
- base (signotope axioms, consecutive no-5-cap, cv ↔ convex 4-set, no convex 6-set): satisfied by a valid signotope
  (consecutive caps give all-triples caps in a signotope);
- B(X) = "X contains a convex pentagon" (X not containing both l and r): for |X| ≥ 6 the clause B(X) → ∨ B(X − v) over
  the first n = 6 elements holds, since a 5-point gon misses one of any 6 elements;
- per side, in that side's order (right: increasing labels on U; left: decreasing labels on V, where `cup(a,b,c)` is the
  sorted triple's sign, correct because reflection keeps caps): u = ↑P4 of the side satisfies "4-cap (a,b,c,d) ⟹ u(c,d)"
  and the four closure clauses per triple (cup: (j,k) ⊑ (i,k) ⊑ (i,j); cap: (i,j) ⊑ (i,k) ⊑ (j,k));
- Bad(D) = "D contains a 4-cap or a 3-cap whose last side-ordered pair is not in u": the size-3 clauses, f = "D is a
  4-cap" with the size-4 recursion, and the size-≥5 recursion over the first 5 elements all hold (a witness of ≤ 4 points
  survives removing one of 5);
- each row "Bad(D) ∨ B(W − D)" (|D| ≤ 10) holds iff D is not an ENV# Δ of that side, true in a counterexample; absent
  literals are false anyway; dropping rows keeps soundness;
- hypotheses R_t → (a,b,c,r) a 4-cap, OR R; L_t → (l,a,b,c) a 4-cap, OR L: satisfied.
So UNSAT ⟹ the statement at m for all signotopes. Correct.

## 2. CNF and certificate (`t3/cert/te6/`)

- `tenv_compact.py 6 15` regenerates `t3/cnf/te6_m15.cnf` byte for byte: SHA-256
  `fde81f37b7460eff9d37b9578ed44113540b307e2f65334be5bdc22f1979777d` (`p cnf 59075 137991`, 31,828 rows).
- `te6_m15.cake.out` is exactly `s VERIFIED UNSAT`; CaDiCaL log `c Version 2.1.3`, `s UNSATISFIABLE`.
- `zstd -dc te6_m15.lrat.zst | sha256sum` = `87f7f7de804e267abe5319b259af8a385a04358223c192f4c4e31b5f956268d8`,
  2,953,348,221 bytes, equal to `certify.jsonl` and the claim.
- cake_lpr **not re-run** by V1 (budget).

## 3. Semantic test of the actual CNF with V1's own code (`v1_te_eval.py`)

V1 builds the canonical assignment in the encoder's variable layout from its own computations (`v1lib`: signs, convex
4-sets, gon masks, ↑P4 of U, and ↑P4 of the reflected order type for the left side) and evaluates every clause of
`te6_m15.cnf`. The soundness argument predicts: violated clauses = rows of the true ENV# Δs of U plus rows of the true
mirror-ENV# Δs of V (|D| ≤ 10), counted independently by exhaustive enumeration:

| set | ENV# Δs of U | mirror-ENV# Δs of V | violated | match |
|---|---|---|---|---|
| tspm6_m15 (the TS±(6) model) | 526 | 124 | 650 | yes |
| root6_m15 (abstract ROOT(6) failure) | 0 | 206 | 206 | yes |
| t1/root6_real15 (real) | 0 | 201 | 201 | yes |
| t1/real/m15_it21_real (real) | 0 | 179 | 179 | yes |
| root6_real15 reflected | 201 | 0 | 201 | yes |
| m15_it10_real reflected | 203 | 0 | 203 | yes |

So the base, the B, u, Bad and hypothesis families are satisfied by these sets and the rows are violated exactly for the
true solutions, on both sides. In particular V1's ↑P4 (covering steps from ROUND6) agrees with the encoder's closure
rules in both orders.

## 4. The other sizes

- |S| ≤ 12: `env6-le11` (V2 CONFIRMED): ENV#(6) holds for every valid U with |U| ≤ 11, so the right side works.
- |S| = 13: TS±(6) for |S| ≤ 13 (`tspm6-le13`, V3 CONFIRMED) with L2: TS± ⟹ TWO-ENV# (`t4-lemmas`, V2 CONFIRMED); also
  directly: `te6_m13.cnf` regenerates from `tenv_compact.py 6 13` (`1fe964af…c496`), `te6_m13.cake.out` has the exact
  line once, decompressed LRAT `f988e0df…5f85`, 407,379,827 bytes, equal to `certify.jsonl`.
- |S| = 14: `tspm6-14` was **NOT CONFIRMED** by V2 (incomplete) [superseded 15 Nov pm (C1 issue 4; note by H1): CONFIRMED
  by V2 since 16:53:54]. But T3's direct run (16:01) covers it: `te6_m14.cnf`
  regenerates from `tenv_compact.py 6 14` (`66da85a3994be90f6bc84d9940d7334786b297d462b6f2e6c6db4630af9ef812`),
  `te6_m14.cake.out` is exactly `s VERIFIED UNSAT`, CaDiCaL 2.1.3, decompressed LRAT
  `663d3e5ff8f4833af03b1d63504aa4ee5b78312a201ba6f3758cad518b28168e`, 1,823,924,534 bytes, equal to `certify.jsonl`
  (cake_lpr not re-run by V1).
- |S| ≥ 16: no (5,6)-valid signotope (`root6-m16-vacuous`, CONFIRMED).
- So the hypothesised TWO-ENV#(6) holds for every (5,6)-valid signotope and every point set. TS±(6) fails at 15
  (`tspm6-m15-abstract`, V3 CONFIRMED), so TWO-ENV#(6) is strictly weaker; by L2 it implies LR(6).

## Not checked

cake_lpr re-runs of the m = 13, 14, 15 proofs (kept as zstd; heap ≥ 1,300 MB needed); the non-hypothesised K2′ form.

## Files (`/home/jay/research/data/roadmap-20261115/pm1115/v1/twoenv6-m15/`)

`v1_te_eval.py` (`4afa1d8687de10739c24f3499caf605421c0dd91434d57461baf7ac720c3c91c`), `v1_te_eval.out` (`869c0fa3…77c7fb`),
`regen_te6_m15.cnf`, `lrat_sha256.txt`, `lrat13_sha256.txt`, `lrat14_sha256.txt` (and byte counts). No git action, no
unit, no other repository file written.
