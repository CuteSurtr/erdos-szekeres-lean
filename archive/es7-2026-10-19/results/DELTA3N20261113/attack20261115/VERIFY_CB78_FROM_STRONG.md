**Verdict: CONFIRMED** (claim `cb78-from-strong`, verifier V1, 15 November 2026, 15:27 KST). The implication strong ⟹ CB
is correct (PROVED). CB(7) for |S| ≤ 13 and CB(8) for |S| ≤ 14 are now CERTIFIED twice: by the DELTA2N records and by V1's
own lemma-free re-certification with kept proofs. **CB(8) at |S| = 15 rests on the DELTA2N record alone** (cake_lpr
verdict recorded, CNF regenerates byte for byte, proof deleted, never re-run; V1 could not re-run it within its budget).

# VERIFY_CB78_FROM_STRONG: CB(7) and CB(8) at small sizes from the certified strong form

## Claim checked (filed by T3)

CB(8) holds for every signotope (hence every point set) with |S| ≤ 15, and CB(7) for |S| ≤ 13, because D(5,n; strong)
implies CB(n) and DELTA2N20261113 certified the strong form for (5,8) at m = 7..15 and for (5,7) at m = 6..13.

## Definitions

- CB(n) (`pm1115/t4/candidates.md` K3): every (5,n)-valid S has a weak Δ that contains no (n−1)-cup.
- Strong form (`DELTA2N20261113/README.md` §2; `tools/eager_cert.py` docstring): Δ has no 4-cap, every convex
  (n−1)-set meets Δ, and no convex (n−1)-set lies inside Δ. Convex k-set: every 4-subset x<y<z<w has
  σ(xyz) = σ(xyw) and σ(xzw) = σ(yzw). k-cup: consecutive triples all '+' (in a signotope, then every triple is '+').

## 1. The implication (checked by hand)

A strong Δ is a weak Δ (no 4-cap, meets every gon). An (n−1)-cup is a convex (n−1)-set: all its triples are '+', so
for every 4-subset all four signs are '+' and the rule holds. A strong Δ contains no convex (n−1)-set, hence no (n−1)-cup,
so it is a CB Δ. For m ≤ n − 2 there is no convex (n−1)-set and Δ = ∅ works for both forms. Correct. On the real
controls below every strong Δ is also a CB Δ (asserted).

## 2. The cited certificates (`DELTA2N20261113/data/cnf_hashes.tsv`)

Rows present, each `UNSAT` with cake_lpr `s VERIFIED UNSAT`, allow/must `None`, reduced `None`/`False`:
- (5,7) strong, `grid`, m = 6, 7, …, 13 (8 rows);
- (5,8) strong, `grid`, m = 7, …, 14 (8 rows; `upper` rows exist for 9-12 as a second encoding), and `late` m = 15.

**Regeneration** (`v1_regen.py`, which imports `Enc` from the recorded `eager_cert.py` and writes the CNF without
solving): all 16 `grid` CNFs and the `late` m = 15 CNF are **byte-identical** to the recorded SHA-256 (`v1_regen.out`).
Reading `eager_cert.py`: the base forbids 4-tuple sign patterns with two changes, consecutive 5-caps, and convex n-gons
as weak (c,d)-gons; Y_K → K is a 4-cap, Q4 → convex 4-set, Z_G → G convex (one-way); the row for Δ is "some 4-cap in Δ,
or a convex (n−1)-set in the complement, or (strong) a convex (n−1)-set in Δ". A counterexample with the witnesses at
their exact values satisfies every clause, so UNSAT ⟹ every valid signotope has a strong Δ. The LRAT proofs of these
rows were deleted after the verdict (as the claim says), and `VERIFY_D1.md` shows that DELTA2N's verifier re-ran only the
(4,n) and (5,5) strong chains, not (5,7) or (5,8).

## 3. V1's own re-certification (independent encoder, proofs kept)

`v1_strong_cnf.py` (SHA-256 `94d274e2c2b7d6976dd802aca6ac3d1aeb1173d8087b345216a52d501e426a0c`), written from the
definitions with no lemma: 8 forbidden full sign patterns per 4-tuple; no 5-cap as "one of the 10 triples is a cup";
e_Q ↔ convex(Q); Y_K → all 4 triples of K are caps; Z_G → every 4-subset of G convex; no convex n-set; one row per Δ ⊆ [m]
(all 2^m). Soundness: a valid signotope without a strong Δ, with e, Y, Z exact, satisfies every clause.

**Control** (`v1_strong_control.py`, output `v1_strong_control.out`): on the real (5,7)-valid `round6/atn/d7_13_real.json`
and (5,8)-valid `d8_15_real.json`, the canonical assignment violates exactly as many clauses as there are strong Δs
(2,317 of 2,535 weak Δs; 11,534 of 12,176), counted independently by brute force; nothing else is violated. (The weak
counts equal `VERIFY_ATN_MAIN.md`.)

**Certification** (unit `esr-agy-v1-strong`, CPUQuota 15 %, MemoryMax 400M, 15:04-15:18 KST; house `certify_cnf.sh`,
heap 250 MB; `cert/certify.jsonl`, SHA-256 `042d4d0e…`): every CNF UNSAT, each `cake.out` with exactly one line
`s VERIFIED UNSAT`:

| n | m | CNF SHA-256 (prefix) | LRAT bytes | LRAT SHA-256 (prefix) | CaDiCaL s / cake s |
|---|---|---|---|---|---|
| 7 | 6-12 | `d853c558`, `1bdc4e01`, `143ab9de`, `64b4ce22`, `40ddfa52`, `e0621eb5`, `90bfb54c` | 285 … 5,921,781 | `4a86cb7a`, `ac426a73`, `a486be15`, `bc16d580`, `4c0fccd1`, `9f9fe529`, `6f0ddc89` | ≤ 3 / ≤ 2 |
| 7 | 13 | `c7fb4b1a232578e2` | 416,064,138 | `f380b7a5507653dd` | 477 / 106 |
| 8 | 7-13 | `a85aa213`, `e8e89771`, `eee01b82`, `a7476515`, `e3bff86b`, `1d6eda07`, `539ae5a1` | 665 … 4,770,312 | `ee47f19f`, `370ee988`, `7c8d4be3`, `aaf98425`, `49e32947`, `3b482d16`, `9509eae3` | ≤ 3 / ≤ 2 |
| 8 | 14 | `3159b987012a6a67` | 116,325,579 | `f0447a2956d6b4b8` | 165 / 45 |

Full hashes in `cert/certify.jsonl` and `mycnf/SHA256SUMS`; proofs kept as `cert/*.lrat.zst`.

**(5,8) at m = 15 was not re-run by V1:** the recorded proof was 872,603,540 bytes and needed cake_lpr heap 900 MB; on a
comparable 904 MB proof V1's cake_lpr ran out of heap at 250 and 300 MB (see `VERIFY_ROOT6_M16_VACUOUS.md`), and V1's
budget is 400 MB.

## Conclusion

- CB(7) holds for every signotope and every point set with |S| ≤ 13: CERTIFIED (record + V1's own kept certificates).
- CB(8) holds for |S| ≤ 14 the same way; at |S| = 15 it is CERTIFIED by the DELTA2N record only (its proof is gone; an
  outside re-run needs regenerating `eager_cert.py 5 8 15 strong` and cake_lpr with heap about 900 MB or more).
- Open, as the claim says: CB(8) at 16-22 and CB(7) at 14-15 (the strong form itself timed out at (5,7), m = 14).
  [superseded 15 Nov pm (C1 issue 13; note by H1, not by V1): this understates the open ranges. By claim w1-cb-window
  (V3 CONFIRMED) a vertex-critical counterexample has at most 58 points for CB(8) and 31 for CB(7), so the open windows
  are 16-58 and 14-31]

## Files (`/home/jay/research/data/roadmap-20261115/pm1115/v1/cb78-from-strong/`)

| file | SHA-256 |
|---|---|
| v1_strong_cnf.py | `94d274e2c2b7d6976dd802aca6ac3d1aeb1173d8087b345216a52d501e426a0c` |
| v1_strong_control.py / .out | `3f63f789…a19a` / `74a3e705…efad` |
| v1_regen.py / .out | `9e99edc1…f922` / `61bb0ae0…6aa4` |
| run_cert.sh | `9038f76150cf29c0154fa5b19e6c763a87724ebd37f150d292d4095adae2acc1` |

No git action; unit stopped (finished 15:18); no other repository file written.
