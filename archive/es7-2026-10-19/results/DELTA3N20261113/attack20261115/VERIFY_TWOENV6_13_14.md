**Verdict: CONFIRMED** (claim `twoenv6-13-14`, filed by T3; verifier V3, 15 November 2026, 16:03-16:25 KST). Label
CERTIFIED: TWO-ENV#(6), hypothesised form, holds for every signotope with |S| = 13 and with |S| = 14.

**Caveat on |S| = 14:** the cake_lpr re-run that counts for m = 14 was made by the **main session**, not by V3.
- My own re-run at heap 300 MB, the most my 400 MB budget allows, stopped with "CakeML heap space exhausted." and
  gave no verdict.
- The main session's run used heap 1500 MB on the same proof. I inspected its output (§3): exactly one verdict line,
  all hashes equal, exit 0.
- For m = 13 my own re-run also gave the exact line.

# Independent check: TWO-ENV#(6) at |S| = 13 and 14

**Statement.** Suppose S is (5,6)-valid, r ends a 4-cap and l starts a 4-cap. Then U = S − r has an ENV# Δ, or V = S − l
has a mirror-ENV# Δ.
- An ENV# Δ is a weak Δ of U with (b,c) ∈ ↑P4(U) for every 3-cap a<b<c inside it.
- A mirror-ENV# Δ is an ENV# Δ of the x-reflection of V. In original labels: every 3-cap a<b<c inside has (a,b) in the
  up-closure of the pairs starting a 4-cap of V, under the reflected order:
  - cup: (i,j) ⊑ (i,k) ⊑ (j,k);
  - cap: the reverse.

  I re-derived this translation from the reflection (i,j,k) ↦ (m−1−k, m−1−j, m−1−i), which keeps the sign.
- Definitions: ROUND6.md "Definitions", candidates.md K2′, and the definitions field of claim twoenv6-m15.

## 1. Encoder soundness (`t3/tools/tenv_compact.py`, SHA-256 `4c408fe7…c573`; my own reading)

The base is the usual one: signotope, no 5-cap via consecutive triples, cv ↔ convex 4-set, no convex 6-set.
- **B(X)** is defined for every X not containing both l and r.
  - For |X| = 5: B(X) → X is convex.
  - For |X| ≥ 6: B(X) → OR over the first 6 elements v of B(X − v). If X contains a gon G, one of its first 6
    elements is outside G, so the canonical B satisfies this.
- **Each side W** is processed in its own order: right W = 0..12 increasing, left W = 13..1 decreasing.
  - u(c,d) ⇐ "(a,b,c,d) is a 4-cap", so u ⊇ P4 of the side.
  - Four clauses per triple make u up-closed under the side's ⊑, with cup and cap steps as defined.
  - So any model has u ⊇ ↑P4, and the canonical u = ↑P4 satisfies every u-clause.
- **Bad(D)** for 3 ≤ |D| ≤ |W| − 4, in the side's order:
  - |D| = 3: cap and ¬u(last pair);
  - |D| = 4: (D is a 4-cap via f) or some 3-subset is Bad;
  - |D| ≥ 5: OR over the first 5 elements v of Bad(D − v).

  The canonical meaning is "D contains a 4-cap or a 3-cap whose last pair, in the side's order, is outside ↑P4", and
  the canonical assignment satisfies these clauses.
- **Hypotheses:** R_t → cap(abc) ∧ cap(bcr) with OR R_t, and L_t → cap(lab) ∧ cap(abc) with OR L_t.
- **Rows:** for each side and each D ⊆ W with |D| ≤ |W| − 4, the clause Bad(D) ∨ B(W − D). Absent literals have
  canonical value false.
- **Soundness:** a counterexample with canonical auxiliaries satisfies every clause, so UNSAT ⟹ the statement at m.
- **Completeness of the row restriction:** a solution minus points, down to a 4-point complement, is still a solution.

## 2. Regeneration

`tenv_compact.py 6 13` and `6 14` give exactly the claimed CNFs:

| CNF | SHA-256 | variables / clauses | rows |
|---|---|---|---|
| te6_m13 | `1fe964af9fbf6793c4a524de948bb8b04d83667f37af1613caf999609165c496` | 15,117 / 45,131 | 7,594 |
| te6_m14 | `66da85a3994be90f6bc84d9940d7334786b297d462b6f2e6c6db4630af9ef812` | 29,863 / 78,413 | 15,628 |

## 3. Certificates

| | te6_m13 | te6_m14 |
|---|---|---|
| T3's CaDiCaL log | 2.1.3, `s UNSATISFIABLE`, exit 20 | 2.1.3, `s UNSATISFIABLE`, exit 20 |
| T3's cake.out | exact line | exact line |
| streamed LRAT bytes and SHA-256 (V3) | 407,379,827, `f988e0df…5f85` = claim | 1,823,924,534, `663d3e5f…168e` = claim |
| **V3 cake_lpr re-run** (unit `esr-agy-v3-cakete6`, heap 300, FIFO) | **`s VERIFIED UNSAT`, exactly 1 line**, exit 0, RSS 313 MB | "CakeML heap space exhausted.", exit 1, no verdict (budget limit) |
| **main-session re-run** (`round6/mainsession/te6recake/`, `recake_generic.sh`, heap 1500, FIFO, 16:06 / 16:08) | exactly 1 line, exit 0, same CNF, zst and LRAT hashes | **exactly 1 line**, exit 0, same CNF hash, zst hash (`0111da0d…398d`, equal to the kept file) and LRAT hash |

The proofs were not modified.

**Process note.** My first launch of the re-run unit had a mistyped (non-ASCII) unit name. I stopped it within seconds
and relaunched it as `esr-agy-v3-cakete6`. Its partial outputs were my own and were deleted.

## 4. My own semantic controls (`v3_te_controls.py`, unit `esr-agy-v3-tectl`, 16:19:42-16:22:50): 188/188 PASS

**Ground truth.** For real point sets (exact integer orientations), my brute force lists every right solution (ENV# Δ
of U) and every left solution (mirror-ENV# Δ of V). The left side is computed twice:
- in original labels with the reflected order;
- by literally reflecting the labels and reusing the right-side code.

The two agree on every set.

**CNF test.** On the **certified CNF**, with S's triple signs fixed, two runs per set:
- (a) all rows kept: expect UNSAT;
- (b) exactly the rows of the true solutions (|D| ≤ |W| − 4) deleted: expect SAT, with the model re-checked exactly
  against every remaining clause.

Test (b) shows on each instance that every non-solution row is satisfiable by the canonical witnesses. That is the
soundness direction. Rows were located by the encoder's documented order: rows come last, right side then left side,
by size and in `combinations` order.

| CNF | sets | right / left solutions | (a) | (b) |
|---|---|---|---|---|
| te6_m13 | the 3 real CONJ-TS′(6) sets, their 3 mirrors, and 2 × 78 two-point deletions of root6_real15 and m15_it26_real | 11-665 / 118-665 | UNSAT 162/162 | SAT with checked model 162/162 |
| te6_m14 | 2 × 13 one-point deletions of the same two real 15-point sets | 5-34 / 146-389 | UNSAT 26/26 | SAT with checked model 26/26 |

The right-side count for lattice-hyp, 208, equals the ENV# count of VERIFY_ATN_MAIN.md.

## 5. The sentence "TWO-ENV#(6) for all signotopes, without tspm6-14"

The derivation holds by size, given its parts:

| sizes | source |
|---|---|
| \|S\| ≤ 12 | ENV#(6) for \|U\| ≤ 11: claim env6-le11, CONFIRMED by V2. It gives the right side directly, without the hypotheses. |
| \|S\| = 13 and 14 | this claim |
| \|S\| = 15 | twoenv6-m15, CONFIRMED by V1 at 16:07 |
| \|S\| ≥ 16 | vacuous: root6-m16-vacuous, CONFIRMED by V1 |

It does not use tspm6-14. I did not re-check the cited claims.

## Files (`/home/jay/research/data/roadmap-20261115/pm1115/v3/twoenv6-13-14/`)

| file | SHA-256 |
|---|---|
| `v3_te_controls.py` | `321fd7334f5d7d484a76b2cc3bcb008f2519202535edbc4fe0e8b2ecb5facc01` |
| `controls13.jsonl` | `2f5185dc4c917174b56e7e0194846fa520263caca262e886df4e596d1e183361` |
| `controls14.jsonl` | `81605bbc6b51363c4122ab712a883863b47c365934857aa9bef3b19049df31a6` |
| `args13.txt` | `7b2eb56721820ea6616c91a7d617d7834ec2eeaeb7e1f8e0e79559b9ae2ad135` |
| `args14.txt` | `b4908d67b4a406a0a4dcb00af9e579060e46205b5343839163c7260510d9e135` |
| `cake_rerun.sh` | `9e01bcbec3376f8e7bb9c7cba5735a9436fba84b4004f40a9f08e12da48e5155` |
| `cake/te6_m13.cake.out` | `c680d3bd…` (the exact line) |
| `cake/te6_m14.cake.out` | `aa0ea685…` (the heap error) |

`regen/` holds the regenerated CNFs.
