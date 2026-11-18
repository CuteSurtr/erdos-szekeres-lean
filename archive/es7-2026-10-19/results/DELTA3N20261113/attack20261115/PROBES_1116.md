# LR(7) at 16 by certified cubes, 16 November 2026 (track D, 18:25-00:30 KST)

**Status at 18:45 KST: run in progress; nothing certified yet.** This page is written early and updated after each
milestone. Labels: PROVED / CERTIFIED (CaDiCaL 2.1.3 LRAT, cake_lpr's exact line `s VERIFIED UNSAT`, hashes recorded) /
EXACT / COMPUTED / HEURISTIC. Nothing is rounded up. Work directory (not in Git):
`/home/jay/research/data/roadmap-20261115/pm1115/dn/`. Units `esr-agd-*` (CPUQuota 150 % in total, memory track
`agd`).

## Status table

| piece (claim `d1-lr7m16-split`) | CNF (SHA-256) | cube tree | final cubes | certified | open | CaDiCaL CPU-h | result |
|---|---|---|---|---|---|---|---|
| K3: β(r) = α(l) = 5 | `lrK3_m16.cnf` (`8bc9f335…`) | `cubes/K3_tree.json`, 6 top variables (3 mirror pairs), 36 top cubes (mirror orbits), lookahead depth 4, 351 leaves | 351 (grows when a cube is split) | 0 | 351 | – | running (`esr-agd-k3`, since 18:37) |
| K1: β(r) ≤ 4, α(l) ≤ 4 | `lrK1_m16.cnf` (`0ce89610…`) | `cubes/K1_k3D4.json` (292 leaves, 91 refuted by unit propagation) | – | – | – | – | not started |
| K2: β(r) = 5, α(l) ≤ 4 | `lrK2_m16.cnf` (`59349034…`) | – | – | – | – | – | not started |
| C1(7) at 16: β(r) = 6 | `c1_rcup7_m16.cnf` (`9c7a0da1…`) | – | – | – | – | – | not started |

## Method

- **Cubes.** For a piece with CNF F, a cube is a set of literals on the 560 triple variables (variable v = v-th
  lexicographic triple of 0..15, true = cup). The cube CNF is F with its header clause count raised and one unit clause
  per literal appended (body byte-identical to F). Every cube CNF is solved by CaDiCaL 2.1.3 (`--lrat=true
  --binary=false`, conflict limit), whose LRAT stream is hashed (SHA-256 of the uncompressed bytes) and compressed with
  zstd on the fly; on exit 20 the proof is kept and checked by cake_lpr reading the decompressed stream (re-hashed);
  the cube counts only if cake_lpr prints exactly one line `s VERIFIED UNSAT` and the re-hashed stream equals the proof
  hash. A cube that reaches its conflict limit is split into up to 4 children by a depth-2 unit-propagation lookahead;
  its partial proof is not a proof (kept in `cert/<piece>/partial/`, see "Problems").
- **Tree.** Top level: 6 triple variables V0 forming 3 mirror pairs {t, μt}, μ(a,b,c) = (15−c, 15−b, 15−a); for the
  mirror-invariant pieces K1 and K3 only one assignment of V0 per mirror orbit is kept (36 of 64). Below each top cube a
  lookahead decision tree (`tools/mktree.py`, march-style score on unit propagation). The tree only chooses cubes.

## Cover argument (PROVED, elementary; checked exactly by `tools/cover_check.py`)

1. **Decision-tree part.** Below each top cube c, the final leaves (tree leaves, each split cube replaced by its
   children) are pairwise clashing (two leaves contain complementary literals) and their measures add up exactly:
   Σ 2^−(number of literals beyond c) = 1. Pairwise clashing subcubes of total measure 1 partition the subcube of c, so
   every assignment of the triple variables that extends c extends exactly one leaf. `cover_check.py` checks both
   conditions with integers, and that no leaf repeats a variable.
2. **Mirror part (K1, K3).** Let S be a 16-point failure of the piece (an LR(7) failure with β(r) = α(l) = 5 for K3,
   β(r), α(l) ≤ 4 for K1). The mirror image μS (point i ↦ 15 − i, x ↦ −x) is a signotope with
   x_{abc}(μS) = x_{μ(abc)}(S) (the reflection and the reordering of the three points each reverse the orientation), μ
   maps caps to caps, cups to cups, convex sets to convex sets and weak Δs to weak Δs, and exchanges β(r) and α(l); so μS
   is again a failure of the same piece (this is the argument of `d1-lr7m16-split` for K2, CONFIRMED). If the pattern p
   of S on V0 is not a kept top cube, then the pattern of μS, q(t) = p(μt), is one (`cover_check.py` checks this for all
   64 assignments). So it suffices that no failure has its V0-pattern among the kept top cubes.
3. **Soundness of the CNF** (every failure of the piece extends to a model of F): D1's line-by-line review of
   `lr_compact.py` and `addcup2.py`, confirmed with the reduction claim `d1-lr7m16-split` (VB, 21:16 on 15 Nov).
4. Hence: if every final leaf cube CNF is CERTIFIED UNSAT, the piece has no 16-point failure.

## Files and hashes

- CNFs copied from `d1ev/cnf/` (hashes checked against `d1ev/cnf/SHA256SUMS`, all OK at 18:26).
- Tools (`dn/tools/`): `mktree.py` (cube tree), `mkcube.py` (cube CNF), `cnc.py` (driver: CaDiCaL, proof stream hashing
  and zstd, cake_lpr check, splitting, append-only `events.jsonl`), `cover_check.py` (exact cover and proof-chain check,
  separate code), `la_score.py` (lookahead scores). Copies of D1's `addcup2.py`, `d1check.py`, `cad_cert2.sh`,
  `ctl_cup2.py`. Tool hashes: `dn/runs/SHA256SUMS.tools_1840`.

## Resume commands

```bash
D=/home/jay/research/data/roadmap-20261115/pm1115/dn; PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd $D; export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
# resume a piece (the driver re-reads cert/<piece>/events.jsonl; set the deadlines and RuntimeMaxSec to your window)
systemd-run --user --unit=esr-agd-k3 -p CPUQuota=150% -p MemoryMax=3400M -p MemorySwapMax=0 -p RuntimeMaxSec=<s> \
  --nice=10 --working-directory=$D -E OPENBLAS_NUM_THREADS=1 -E OMP_NUM_THREADS=1 -E MKL_NUM_THREADS=1 \
  $PY -u tools/cnc.py --tree cubes/K3_tree.json --out cert/K3 --workers 2 --conf 500000 --wall 2400 \
  --stop-new <ISO> --hard <ISO> --heap-min 1000 --heap-max 1900 --split-depth 2
# cover and proof-chain check of a piece
python3 tools/cover_check.py cubes/K3_tree.json cert/K3/events.jsonl
```
