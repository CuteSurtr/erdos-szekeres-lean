**Verdict: CONFIRMED** (claim `tspm6-le13`, filed by T4, certification run by T3; verifier V3, 15 November 2026,
14:19-14:28 KST). Label CERTIFIED for |S| = 13 is correct, and |S| ≤ 12 follows by citation: **TS±(6) holds for every
signotope, hence every point set, with at most 13 points.**

# Independent check: TS±(6) for |S| ≤ 13

**Statement checked.** Suppose S is (5,6)-valid, |S| ≤ 13, the rightmost point r ends a 4-cap and the leftmost point l
starts a 4-cap. Then one of the following holds:
- U = S − r has a terminal-safe weak Δ: 4-cap-free, meets every convex pentagon of U, and every 3-cap (a,b,c) inside it
  has (b,c) ending a 4-cap of U;
- V = S − l has an initial-safe weak Δ, the mirror notion.

Definitions: CONJTS_TEST.md §2 and THEORY_1115PM.md §0. The mirror μ maps (i,j,k) to (m−1−k, m−1−j, m−1−i) with the same
sign.

## 1. Soundness of the CNF (read against the definitions; my own argument)

**`t4/ts_cnf.py`** (SHA-256 `caef7805…df`), the one-sided failure CNF.
- The variables 1..286 are the triples in lexicographic order, true = cup.
- The signotope clauses forbid the subsequences +−+ and −+−, which is exactly "at most one sign change".
- "No 5-cap" is the clause "some consecutive triple is a cup". For a signotope, consecutive caps force all caps, so
  every valid S satisfies it.
- cv is defined in both directions (convex 4-set iff s1 = s2 and s3 = s4), and no 6-set is convex.
- Every auxiliary variable is a one-way witness towards its true condition:
  - Z_T → T is a gon of U;
  - R_t → (a,b,c) and (b,c,r) are caps, together with OR R_t (r ends a 4-cap);
  - F_K → K is a 4-cap of U;
  - NB(b,c) → (u,v,b,c) is not a 4-cap for any u < v < b, i.e. (b,c) ends no 4-cap of U;
  - BAD(a,b,c) → cap(a,b,c) and NB(b,c).
- One row per A ⊆ U with |A| ≤ 8: "A has a 4-cap, a bad 3-cap, or misses a gon".
- **A counterexample S, with every auxiliary set to its defining condition, satisfies every clause.**
- Restricting the rows to |A| ≤ |U| − 4 loses nothing. A safe weak Δ minus points, down to a 4-point complement,
  is still a safe weak Δ, because no pentagon fits in 4 points.

**`t4/lr_cnf.py`** (SHA-256 `3e24db5b…1a`) adds a second copy.
- In it, each triple variable t is replaced by μ(t), and the auxiliary variables are shifted by 2,794.
- Copy 2 is therefore the one-sided CNF evaluated on S′(t) = S(μ(t)), which is the mirror of S.
- An initial-safe weak Δ of V corresponds exactly to a terminal-safe weak Δ of μ(V) = S′ − r′.
- l starts a 4-cap of S iff r′ ends a 4-cap of S′, and S′ is valid iff S is.
- So a TS± counterexample satisfies both copies. The auxiliaries are disjoint, so the full CNF is satisfiable.
  **UNSAT ⟹ TS±(6) at |S| = 13.**

## 2. Regeneration

- `ts_cnf.py 6 13` regenerates T4's `ts/ts6_m13.cnf` byte-identically (`dacd4886…`).
- `lr_cnf.py ts/ts6_m13.cnf 13` gives exactly `0bbee2d5f22333bb459dac6989ebbf9491cd33dc907092ded136efe047e45074`, the
  certified CNF with 5,588 variables and 49,132 clauses. It equals both `t4/ts/tspm6_m13.cnf` and `t3/cnf/tspm6_m13.cnf`.
- Note: lr_cnf.py writes its source path into the first comment line. Run from another directory, the hash differs
  only in that line (body checked identical with `cmp`).

## 3. Certificate, re-run independently

- T3's log `tspm6_m13.cadical.log` shows `c Version 2.1.3`, `s UNSATISFIABLE`, 71.09 s and `c exit 20`.
- T3's `cake.out` has the exact line, as does `certify.jsonl`.
- **My own re-run** (`cake_rerun.sh`) ran in unit `esr-agy-v3-cakets` (CPUQuota 15 %, MemoryMax 400M, swap 0),
  14:21:12-14:23:50.
  - It streamed the kept proof `tspm6_m13.lrat.zst` through a FIFO into cake_lpr (SHA-256 `c14ff498…`) with
    `--CML_HEAP_SIZE=300`.
  - The output is exactly one line, `s VERIFIED UNSAT`, with exit 0, peak RSS 313 MB and 146 s of wall time.
  - The decompressed LRAT has 520,270,484 bytes and SHA-256
    `5583aea84144849e5a26d98f765ff667e6f9ab046c4c5b4e06d33fa1f08e678c`, both equal to the claim.
- The proof file was not modified.

## 4. My own semantic controls (`v3_ts_controls.py`, unit `esr-agy-v3-tsctl`, 14:23:55-14:26:45): 162/162 PASS

For each real 13-point set (exact integer orientations), my code computes the ground truth by brute force over all
4,096 subsets: validity, r ends a 4-cap, l starts a 4-cap, nTS = # terminal-safe weak Δs of U, and
nIS = # initial-safe weak Δs of V. It then fixes the 286 triple variables of the **certified CNF** to S's signs and runs
CaDiCaL on copy 1, on copy 2 and on the full CNF. Each SAT model was re-checked exactly against every clause.

| sets | ground truth | copy 1 / copy 2 / full | count |
|---|---|---|---|
| the three real CONJ-TS′(6) sets (cts6real) | nTS = 0, nIS = 78 / 354 / 63 | SAT (model checked) / UNSAT / UNSAT | 3 |
| their x-mirrors | nTS > 0, nIS = 0 | UNSAT / SAT (model checked) / UNSAT | 3 |
| root6_real15 and m15_it26_real with two interior points deleted (all 2 × 78) | valid, r ends and l starts a 4-cap, nTS > 0, nIS > 0 | UNSAT / UNSAT / UNSAT | 156 |

- Every verdict equals the brute-force prediction.
- The SAT controls show, on actual real instances, that copy 1 admits right-side failures and copy 2 (the μ-renamed copy)
  admits left-side failures. That is the soundness direction.
- The full CNF is satisfiable exactly when both copies are, since the auxiliaries are disjoint. Its UNSAT verdict
  therefore means no 13-point S fails on both sides.

## 5. Sizes ≤ 12 and the other remarks

- **|S| ≤ 12.** CONJ-TS′(6) is CERTIFIED at sizes 7-12 by the round-4 main encoder (CONJTS_TEST.md §5.3; sizes ≤ 7 are
  trivial). It is also CERTIFIED at 4-12 by that round's verifier's lemma-free encoder, whose cake re-runs that verifier
  did (§5.4). The one-sided form has the same hypotheses minus "l starts a 4-cap", so it implies TS±(6) at each size.
  I did not re-run those certificates.
- **"First size where the one-sided form fails."** That is claim cts6-real-13, CONFIRMED by V1.
- **"TS± ⟹ LR."** That is claim t4-lemmas L2, CONFIRMED by V2. Neither was re-checked here.
- **TS±(6) at 14 and 15.** Open. T4 has CNFs ready, but no verdict exists.

## Code and outputs (`/home/jay/research/data/roadmap-20261115/pm1115/v3/tspm6-le13/`)

| file | SHA-256 |
|---|---|
| `v3_ts_controls.py` | `e6aa6cd9d45b6ee3c628984e57833af9a8e3c0cc23d872cdb3574c51dab6ae93` |
| `controls.jsonl` (162 rows plus summary) | `ca12afcca4eac8cfd08d1d2f864b3c7dbf368810cdec132d91906c01f7cfe519` |
| `control_args.txt` | `7b2eb56721820ea6616c91a7d617d7834ec2eeaeb7e1f8e0e79559b9ae2ad135` |
| `cake_rerun.sh` | `ce7ed0730b0e215cb20ec589da9a797a373f6f81270fb376125898ec3a58bdc5` |
| `cake/cake.out` | `c680d3bd38a04c7beee7d54999f8f00b43051f75a53cf2bd170ae0cc5f99eb5f` |

The `cake/` folder also holds `cnf.sha256`, `lrat.sha256` and `lrat.bytes`. `regen/` holds the regenerated CNFs.
