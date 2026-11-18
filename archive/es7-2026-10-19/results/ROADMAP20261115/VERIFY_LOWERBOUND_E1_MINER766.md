**Verdict: CONFIRMED** (claim `lb-e1-miner766`, filed by track E1; verifier VS, 15 November 2026, 19:57-20:23 KST;
the side fact "30-point subsets exist in 10,002 of the sets" was confirmed at 20:50, see its section). Label EXACT for the mined subsets holds. VS's own code, written
from the definitions, finds **no** 31-point subset without a 6-cup and a 6-cap in any sweep direction of any of the
10,593 listed sets. No set is free of 6-chains as a whole in any direction. All 10,593 sets are realized 32-point sets
in general position without a convex heptagon. This is weak negative evidence only; N(7,6,6) = 30 stays open.

# VERIFY_LOWERBOUND_E1_MINER766: the (7,6,6)@31 seed miner over the realized 32-point pools

## Method (own code `vs_miner.cpp`, GMP exact integers; written without reading `miner.cpp`)

- **Sets.** Each line `name x0 y0 …` is read with arbitrary-size integers (some coordinates have 114 bits). The code
  computes the exact orientation sign of every triple and checks that none is zero. It counts the convex 7-subsets by
  backtracking with the 4-point test (no point inside the triangle of the other three).
- **Sweep orders.**
  - Start at u = (cos ε, sin ε), ε → 0+: sort by x, then by y.
  - Apply the swaps of all pairs whose critical direction (the normal of p_j − p_i, taken in the open upper half-plane)
    lies in (0, π), sorted by angle with exact cross products. Equal angles are grouped as simultaneous swaps.
  - Every swapped pair is checked to be adjacent (0 failures).
  - The last order is dropped when it equals the reverse of the first. In every case where no pair has equal x, it does.
  - The half circle suffices: the opposite direction reverses the order, which swaps cups and caps, and the pair
    (6, 6) is symmetric.
- **Hit test per order.**
  - Find one 6-chain C (a 6-cup or 6-cap), by DP over consecutive triples of the sweep order. For points in a sweep
    order the signs form a signotope, so consecutive triples of one sign give every triple that sign.
  - If there is no C, the order is a "0-point hit". Otherwise test each x ∈ C: if S − x has no 6-cup and no 6-cap,
    it is a 1-point hit. Every hitting point must lie in C, so this search is complete.

## Results (unit `esr-agv-vs-miner1`, 20:01:32-20:21:38, CPUQuota 15 %; `mode1.out`)

| item | result |
|---|---|
| sets | 10,593: `miner_list7.txt` (SHA-256 `830886e2…`, 10,457 lines) + `miner_list7_f2.txt` (`171ec8eb…`, 136 lines); 10,593 distinct names |
| points / general position / convex heptagons | 32 in every set / 10,593 in general position / **0 convex 7-subsets in every set** |
| sweep directions | **5,218,410** distinct orders in all (the record's count is 5,218,410) |
| 0-point hits (no 6-chain at all) | **0** |
| 1-point hits (a 31-point subset with no 6-cup and no 6-cap) | **0** |

## Provenance (own comparison with the repository files, `vs_provenance.py`)

- `mirror32` and `sym7_32` equal `SYMMAX/mirror_32points.txt` and `SYM2/sym7_32points.txt`.
- The 8,537 pool lines equal `inputs/distinct_K7*.txt` line by line (5,354 + 510 + 459 + 732 + 608 + 700 + 174).
- The 136 F2 lines equal the files in `F2/data/sets32/*.pts`.
- The 1,911 near-full deletions equal line i of `inputs/nearfull_p2c|p2d.txt` minus point v, giving 273 bases × 7.
- The 7 AE33 deletions equal AE33 minus point v. AE33 is `alphaevolve_pts.json` `points_7`, read as exact fractions and
  scaled by the lcm of the denominators.
- With `vs_oct list … 7` (VERIFY_LOWERBOUND_E1_OCTDEL65), each of the 274 bases has exactly **one** convex heptagon,
  and its 7 vertices are exactly the deleted points (274/274).

## Controls (`selftest_miner.py`, K = 4 on 60 random 7-11-point sets)

- The 2,182 enumerated orders are pairwise distinct, and none is the reverse of another.
- 24,000 random exact directions without ties: the resulting order or its reverse was enumerated every time.
- Brute force over all 4-subsets reproduces the 1-point-hit flag of every order (18 positive cases among them). It also
  reproduces the 2-point flag (293 positive cases).

## Side fact "(30-point such subsets exist in 10,002 of the sets.)"

**CONFIRMED** (unit `esr-agv-vs-miner2`, 20:22-20:49, `vs_miner2 all_sets.txt 6 2` with `VS_STOP2=1`; output
`mode2any.out`, SHA-256 `dd19f7c246eaa8b40e43e2c6cdbd49a8299f75e4a55dfd7d762732d49e110ae9`).

- The run is the same scan plus a complete 2-point search (x in a 6-chain C of S, y in a 6-chain of S − x). It stops
  at a set's first direction with a 2-point hit.
- **10,002** sets have a direction with a 30-point subset that has no 6-cup and no 6-cap. The other **591** were
  scanned over all their directions and have none.
- This run again found 0 one-point and 0 zero-point hits.
- The record's total of 1,138,393 directions with 2-point hits was not counted: the run stops at the first hit of each
  set, and the total is not part of the claim.

## Not checked

The filer's miner and its own self-tests were not re-run. D2's walk states are not stored and were not part of the claim.

## Files (`/home/jay/research/data/roadmap-20261115/pm1115/vs/lb-e1-miner766/`)

| file | SHA-256 |
|---|---|
| `vs_miner.cpp` | `4a4f2c0cbab7181faf7dbe0e3c42a80a5c575e26ab78bf81aad913f5612b5c9b` |
| `vs_miner2.cpp` (same, with an option to stop at the first 2-point hit) | `b43b3682bd7ad54b6ceeb7cc5753e153a1ff635f637fa7d9b017e56ffb430b1c` |
| `selftest_miner.py` | `7ab177031dad98946f86ef63d5a1b61cf58822c1d051b4fc5fc79785fe226a91` |
| `vs_provenance.py` | `ad2a9b5b3186ef7d983350a59c143cbeb2c1ca5f383b5849bd3f0fb80996483d` |
| `all_sets.txt` (the two lists concatenated) | `84e88f7e8e182aafa2f7748cd82d02473460f3eae8342d0101debd1b1c87f5cb` |
| `mode1.out` (one line per set) | `e78386f33f57699b940a15203d9d80307981dfadf7e7c4ee2793272111224062` |

Rerun: `g++ -O2 -o vs_miner vs_miner.cpp -lgmpxx -lgmp; ./vs_miner all_sets.txt 6` (about 190 CPU-s). No git action;
no repository file other than this one was written.
