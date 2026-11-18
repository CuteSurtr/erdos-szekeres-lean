**Verdict: CONFIRMED** (claim `cb6-le13`, verifier V2, 15 November 2026, 14:14-14:30 KST). Label CERTIFIED is correct
for m = 7..13. The trivial sizes m ≤ 6 and the cup–cap remark are correct.

# Independent check: CB(6) for every signotope with at most 13 points

**Claim (filed by T4).** Every (5,6)-valid signotope S with |S| ≤ 13 has a weak Δ that contains no 5-cup. For
m = 7..13, `cb_cnf.py 6 m` gives a CNF whose CaDiCaL 2.1.3 LRAT proof cake_lpr accepts. Sizes m ≤ 6 are trivial.

**Definitions.** From `pm1115/t4/candidates.md` §0 and K3, and THEORY_1115PM.md §0:
- k-cap / k-cup: every triple a cap / a cup;
- convex: every 4-subset a<b<c<d has σ(abc) = σ(abd) and σ(acd) = σ(bcd);
- weak Δ: 4-cap-free and meets every convex pentagon (n = 6);
- CB(n): a weak Δ with no (n−1)-cup.

My exact check of the 4-point rule agrees with the triangle-containment test on 20,000 random integer 4-point sets
(6,024 of them non-convex).

## 1. Soundness of T4's encoder (`t4/cb_cnf.py`, SHA-256 `115c94c05d7fe9fd…`, as stated)

I read it line by line. Every clause holds for a counterexample when each auxiliary variable is set to its meaning.
- Signotope: it forbids the patterns s,−s,s on any 3 of the 4 positions, which is equivalent to ≥ 2 sign changes.
- No 5-cap: it uses consecutive triples. This is valid because consecutive caps force all triples to be caps, by the
  4-tuple axiom on (x,y,z,w) with sequence (−,?,?,−).
- cv(Q) ↔ (x_abc = x_abd ∧ x_acd = x_bcd): both directions are encoded, and they are the definition.
- No convex hexagon: some cv(Q) is false.
- The implications Z_T → T convex, F_K → K a 4-cap and W_C → C a 5-cup use consecutive triples, so they are implied by
  the all-triples meanings.
- Rows: D contains a 4-cap, contains a 5-cup, or misses a gon. This holds for every D when S is a counterexample.
- Rows exist only for |D| ≤ m − 4. Dropping clauses cannot break soundness, and the claim's completeness remark is also
  right: a CB Δ minus points stays a CB Δ while its complement has ≤ 4 points.

**Sound.**

## 2. CNFs regenerate byte-identically

`python3 cb_cnf.py 6 m` for m = 7..13 gives files whose SHA-256 equals both `cb/cert/certify.jsonl` and the files on
disk, 7 of 7 (`v2/cb6-le13/regen/regen.sha256`).

## 3. cake_lpr re-run on T4's kept proofs (all 7)

Each `cb6_m<m>.lrat.zst` was streamed (`zstd -dc | tee FIFO | sha256sum`) into `~/.local/bin/cake_lpr` against my
regenerated CNF. Each output was grepped with `grep -x`. The runs were in units `esr-agy-v2-cb6a` / `-cb6b` (CPUQuota 15 %,
MemoryMax 400M).

| m | CNF SHA-256 | LRAT SHA-256 of the stream (= record) | heap MB | peak RSS | exact line |
|---|---|---|---|---|---|
| 7 | `f660d65a…` | `c57932d7…` | 200 | 9 MB | `s VERIFIED UNSAT` |
| 8 | `b7f8f7d7…` | `efbc5e29…` | 300 | 9 MB | `s VERIFIED UNSAT` |
| 9 | `90223b04…` | `e35965e6…` | 300 | 13 MB | `s VERIFIED UNSAT` |
| 10 | `a80d3602…` | `fab76e5e…` | 300 | 28 MB | `s VERIFIED UNSAT` |
| 11 | `62017ffb…` | `f41f2542…` | 300 | 278 MB | `s VERIFIED UNSAT` |
| 12 | `f3fae5c7…` | `9f2792d9…` | 300 | 311 MB | `s VERIFIED UNSAT` |
| 13 | `2dbe9c4c…` | `3008a390bd145ee6…` (846,291,663 B) | 300 | 313 MB | `s VERIFIED UNSAT` (295 s) |

Heap 300 MB was enough for m = 13; T4 used 340.

## 4. Own encoder from the definitions, certified at m = 7..12

The encoder is `v2/cb6-le13/my_cb_cnf.py` (`418ad88b46dafc2de81ca368c718e173e54786bb0372bd0a874dfd8e3498e3ef`). It was
written before reading `cb_cnf.py`.
- The no-5-cap clause and the 4-cap / 5-cup implications use all triples.
- No-hexagon uses one-directional N_Q → "Q non-convex".
- It shares no code with T4.

I ran the house `certify_cnf.sh` (CaDiCaL 2.1.3 + cake_lpr, heap 300, proofs kept as zstd in `v2/cb6-le13/cert/`):

| m | my CNF SHA-256 | LRAT bytes / SHA-256 | verdict |
|---|---|---|---|
| 7 | `406794b5…` | 0 (the CNF contains the empty row \|D\| = 3: any 3 points are a CB Δ when m = 7) | `s VERIFIED UNSAT` |
| 8 | `d08021e0…` | 1,882 / `7f810d26…` | `s VERIFIED UNSAT` |
| 9 | `eea61d3a…` | 13,580 / `c6a3c684…` | `s VERIFIED UNSAT` |
| 10 | `f259f5aa…` | 463,065 / `a7b3a3b7…` | `s VERIFIED UNSAT` |
| 11 | `a72e77d8…` | 14,265,092 / `9e1dd85a…` | `s VERIFIED UNSAT` |
| 12 | `80df4389…` | 118,319,779 / `6e0d3063…` | `s VERIFIED UNSAT` |

Full hashes are in `v2/cb6-le13/cert/certify.jsonl` (`671d0fdf…` at 14:31).

**Addendum 15:27: own encoder at m = 13 is also certified.** Unit `esr-agy-v2-cb6own13c` (CPUQuota 15 %, MemoryMax 400M)
ran the house `certify_cnf.sh` on `cnf/v2cb6_m13.cnf`:
- CNF SHA-256 `c850f05112e8f8b7bbaa3f239f3c3c6ff601745d883b94b67d95e8ab35854e76`;
- CaDiCaL 2.1.3: exit 20, 929 s;
- LRAT: 844,957,766 bytes, SHA-256 `2529d50b72490a873c70ebf4c23ee2ea091f863eca48f5e4735f438900aa33eb`, kept as
  `cert/v2cb6_m13.lrat.zst`;
- cake_lpr at heap 300: **`s VERIFIED UNSAT`** (`grep -x`, 240 s, peak RSS 313 MB).

So V2's own encoder, which shares no code with T4's, now certifies CB(6) at every size m = 7..13.
- certify.jsonl now ends with this line (file SHA-256 `f5999c9f…`).
- Two earlier attempts at m = 13 were stopped by V2 to free its budget for other claims. Their partial LRATs were V2's
  own non-proof outputs and were deleted; their logs are kept as `*.stopped-1435` and `*.stopped-1502`.

**Semantic control of my encoder** (`control_my_cb.py`, `5bf45e28…`). The signs of a fixed set were added as units, and
the result was compared with a brute-force CB count over all 2^m subsets (convexity cross-checked by two tests). It
agreed in all 14 runs:
- q = 5: UNSAT on d6_11, d6_12, m11_1, lattice-hyp, root6_m15 and the real m15_it10 and m15_it22. The brute force found
  145-615 CB Δs.
- q = 4 (CB2): SAT exactly on the three 15-point sets, which have 0 CB2 Δs, and UNSAT on the four smaller sets, which
  have CB2 Δs.

## 5. Other parts of the statement

- **m ≤ 6.** Any m − 4 points (∅ if m ≤ 4) leave 4 points, so no pentagon is missed, and ≤ 2 points contain no 4-cap
  and no 5-cup. Correct. m = 7 is just as trivial: any 3 points work, which is the empty row above.
- **Remark.** A set with no 4-cap and no (n−1)-cup has at most C((n−1)+4−4, n−3) = C(n−1,2) points (Erdős–Szekeres
  cup–cap). The rest S − Δ has no 5-cap and no gon, so CB(8) ⟹ M(5;8) ≤ 21 + M(5;7). Correct.
  - "Between weak and strong": a CB Δ is a weak Δ, and a Δ with no gon contains no (n−1)-cup.
  - The word "new" is a novelty statement, which I did not check.
- **"Hence every point set".** x-sorted point sets in general position give signotopes with the same caps, cups and
  convex sets.

## Files

- Folder: `/home/jay/research/data/roadmap-20261115/pm1115/v2/cb6-le13/`.
- Code: `run_job.sh` (`2d8f3841…`), `v2lib.py` (`7c8b1ee0…`).
- `results.jsonl` (`244fd162…`) has one line per run, with heap, peak RSS, stream hash and exact-line count.
- Logs: `replay/m<m>.cake.out`, `cert/*.cake.out`.
- Rerun:

```bash
cd /home/jay/research/data/roadmap-20261115/pm1115/v2/cb6-le13
./run_job.sh replay 300 7 8 9 10 11 12 13     # T4's proofs; as a unit with MemoryMax >= 400M
./run_job.sh own 300 7 8 9 10 11 12           # own encoder (generate first: python my_cb_cnf.py 6 m cnf/v2cb6_m<m>.cnf)
```
