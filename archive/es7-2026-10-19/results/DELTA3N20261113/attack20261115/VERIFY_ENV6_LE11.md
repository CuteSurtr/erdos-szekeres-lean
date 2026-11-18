**Verdict: CONFIRMED** (claim `env6-le11`, verifier V2, 15 November 2026, 14:23-14:32 KST). Label CERTIFIED is
correct for |U| = 5..11; |U| ≤ 4 is trivial, as stated. The "decided except 12 and 13" summary is consistent with the
cited claims, all of which other verifiers have CONFIRMED.

# Independent check: ENV#(6) for every (5,6)-valid signotope with |U| ≤ 11

**Claim (filed by T3).** For |U| = 5..11, round 6's `env_cnf.py 6 m` is UNSAT with a CaDiCaL 2.1.3 LRAT accepted by
cake_lpr. |U| ≤ 4 is trivial.

**Definitions.** ROUND6.md "Definitions used below", with n = 6:
- weak Δ: 4-cap-free and meets every convex pentagon;
- P4(U): pairs (c,d) ending a 4-cap (a,b,c,d);
- the order: for i<j<k, a cup gives (j,k) ⊑ (i,k) ⊑ (i,j), and a cap gives (i,j) ⊑ (i,k) ⊑ (j,k);
- ↑P4: the up-closure of P4 under that order;
- ENV#(6): every valid U has a weak Δ whose every 3-cap a<b<c has (b,c) ∈ ↑P4(U).

## 1. Soundness of round 6's encoder (`round6/envroot/env_cnf.py`, SHA-256 `94eb85691338b4ea…`)

I read it line by line (66 lines). The base clauses are the same as in T4's CB encoder, which I reviewed in
[VERIFY_CB6.md](VERIFY_CB6.md):
- signotope patterns;
- no 5-cap via consecutive triples, valid because consecutive caps force all caps;
- cv ↔ the 4-point rule;
- no convex hexagon;
- Z_T → T convex.

The ENV#-specific parts:
- [x_abc, x_bcd, u_cd]: a 4-cap (a,b,c,d) forces u(c,d), so P4 ⊆ u.
- Four closure clauses per triple, exactly one generating step each: cup (j,k)→(i,k)→(i,j), cap (i,j)→(i,k)→(j,k).
  So u ⊇ ↑P4 in every model, and u := ↑P4 satisfies all of them.
- F_K → K a 4-cap, and W_abc → (a,b,c) a cap and ¬u(b,c).
- Rows for |A| ≤ m − 4: A has a 4-cap, a 3-cap with ¬u, or misses a gon.

A counterexample with u = ↑P4 and every auxiliary variable at its meaning satisfies every clause, so the encoder is
**sound**. Dropping rows (the size bound) cannot break soundness.

## 2. CNFs regenerate byte-identically

`python3 env_cnf.py 6 m` for m = 5..11 gives files whose SHA-256 equals both `t3/cert/env6/certify.jsonl` and the files
on disk, 7 of 7 (`v2/env6-le11/regen/regen.sha256`).

## 3. cake_lpr re-run on T3's kept proofs (all 7)

Each proof was streamed (`zstd -dc | tee FIFO | sha256sum`) into `~/.local/bin/cake_lpr --CML_HEAP_SIZE=300` against
my regenerated CNF, and each output was grepped with `grep -x`. m = 5 ran in the foreground (under 1 s); m = 6..11 ran in
unit `esr-agy-v2-env6a` (CPUQuota 15 %, MemoryMax 400M).

| m | CNF SHA-256 | LRAT SHA-256 of the stream (= record) | peak RSS | exact line |
|---|---|---|---|---|
| 5 | `ee1012b0…` | `78da53a6…` | 7 MB | `s VERIFIED UNSAT` |
| 6 | `becadad8…` | `50608ba8…` | 7 MB | `s VERIFIED UNSAT` |
| 7 | `edf2e33b…` | `26f442cb…` | 9 MB | `s VERIFIED UNSAT` |
| 8 | `eb8edbe8…` | `e94bd96b…` | 12 MB | `s VERIFIED UNSAT` |
| 9 | `913ea1b4…` | `5e746709…` | 24 MB | `s VERIFIED UNSAT` |
| 10 | `5419ee99…` | `cf3ccf40…` | 194 MB | `s VERIFIED UNSAT` |
| 11 | `a5a746b2…` | `0a832842317c3b17…` (62,907,443 B) | 311 MB | `s VERIFIED UNSAT` |

## 4. Own encoder from the definitions, certified at m = 5..11

The encoder is `v2/env6-le11/my_env_cnf.py` (`44b689c99a094a6a4e04602ff8fb7941cffd8d41b36bb3de1a73a1ec63ce0bdb`). It was
written before reading `env_cnf.py`, and it shares no code with it.
- 4-caps, 5-caps and 4-cap → u use all triples.
- No-hexagon is one-directional.
- P4 ⊆ u, closure of u under the four step types, and G_abc → (a,b,c) a cap ∧ ¬u(b,c).

I ran the house `certify_cnf.sh` (CaDiCaL 2.1.3 + cake_lpr, heap 300, proofs kept as zstd in `v2/env6-le11/cert/`):

| m | my CNF SHA-256 | LRAT bytes / SHA-256 | verdict |
|---|---|---|---|
| 5 | `a30d78cd…` | 0 (the CNF has an empty row: one point is an ENV# Δ when \|U\| = 5) | `s VERIFIED UNSAT` |
| 6 | `5efb3163…` | 0 (empty row: any 2 points work when \|U\| = 6) | `s VERIFIED UNSAT` |
| 7 | `b1c70d86…` | 591 / `248bf4dd…` | `s VERIFIED UNSAT` |
| 8 | `bcea5227…` | 5,376 / `9f1155f5…` | `s VERIFIED UNSAT` |
| 9 | `049a6a2f…` | 223,327 / `c90332f8…` | `s VERIFIED UNSAT` |
| 10 | `d446e408…` | 4,487,932 / `5fa7c5f3…` | `s VERIFIED UNSAT` |
| 11 | `72c5527d…` | 65,546,018 / `79cf52b0…` | `s VERIFIED UNSAT` |

Full hashes are in `v2/env6-le11/cert/certify.jsonl` (`6b057037…`).

**Semantic control of my encoder** (`control_my_env.py`, `317fc5e8…`). The signs of a fixed set U were added as units,
and the result was compared with a brute-force ENV# count over all 2^|U| subsets. ↑P4 was built by search from the
definitions, and convexity was cross-checked by two tests. It agreed in 6 of 6 runs:
- UNSAT where ENV# Δs exist:
  - d6_11 − r (10 points): 84 Δs;
  - lattice-hyp − r (12 points): 208, the record's number;
  - flat-hyp (13 points): 1,431, the record's number;
  - m11_1 (11 points): 120.
- **SAT** where none exist: the real m15_it10 − r and the abstract root6_m15 − r (14 points each, 0 ENV# Δs).

## 5. The rest of the statement

- **|U| ≤ 4.** There is no convex pentagon, so A = ∅ works. Correct. (|U| = 5, 6 are just as trivial: see the empty
  rows above.)
- **"Hence every point set".** x-sorted point sets in general position give signotopes with the same caps, convex sets
  and order.
- **"Decided except at 12 and 13".** This holds given the other results:
  - ENV#(6) fails at |U| = 14 and 15: claims `env6-fails-root6m15` (V1 CONFIRMED) and `env6-real-14-15` (V3 CONFIRMED).
    My own T4-lemma check also found 0 ENV# Δs for U = S − r on root6_m15 and on all 21 real 15-point sets.
  - |U| ≥ 16 is vacuous: no (5,6)-valid signotope has 16 points, from base(5,6,16) UNSAT in DELTA2N, re-certified in
    claim `root6-m16-vacuous` (V1 CONFIRMED).
  - The note "|U| = 12 not solved in 45-52 s" is T3's; I did not re-run it.

## Files

- Folder: `/home/jay/research/data/roadmap-20261115/pm1115/v2/env6-le11/`.
- Code: `run_job.sh` (`f724645c…`), `v2lib.py` (`7c8b1ee0…`).
- `results.jsonl` (`00e450fd…`) has one line per run.
- Logs: `replay/m<m>.cake.out`, `cert/*.cake.out`.
- Rerun:

```bash
cd /home/jay/research/data/roadmap-20261115/pm1115/v2/env6-le11
./run_job.sh replay 300 5 6 7 8 9 10 11   # T3's proofs (as a unit, MemoryMax >= 400M)
./run_job.sh own 300 5 6 7 8 9 10 11      # own CNFs: python my_env_cnf.py 6 m cnf/v2env6_m<m>.cnf
```
