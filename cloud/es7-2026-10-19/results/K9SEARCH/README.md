# K9SEARCH: 8-fold symmetric sets without a convex 9-gon (k = 9), 4 November 2026

**Outcome.** No 8-fold 128-point set without a convex 9-gon was found. The best size stays 120. Since 8-fold sets have
8t points, the next possible size is 128.

**Exact computation.** The 128-point near miss is `sets/k9_128_final.pts` (SHA-256 `b06ba08b…`).
- **Structure.** 16 orbits of 8 points, with integer Z[ζ8] coefficients.
- **General position.** All 341,376 orientations are nonzero. Three methods agree: exact arithmetic in Q(√2), 2^-300
  interval arithmetic, and Z[√2] coordinates.
- **Counts.** It has exactly 1136 convex 9-gons and no convex 10-gon. Both convex-k-gon dynamic programs of the
  repository's checker agree.
- **Where the 9-gons are.** Every convex 9-gon uses the outermost orbit and all five orbits of the next radial group.
  None uses the innermost orbit.

**Exact computation: a second 120-point set.** `sets/f_del0.pts` (SHA-256 `804f85e1…`) is the 128-point set without
its outer orbit.
- It is 8-fold symmetric with 120 points and no convex 9-gon (largest convex subset 8), and all orientations are
  nonzero.
- Its radial groups are 5+4+3+2 plus a tiny inner orbit, where the earlier record (`PRIMEFOLD`) has 1+4+4+3+2+1. They
  are different configurations; that they are non-equivalent order types was not checked separately.

**Evidence only.** The search ran about 1.2 CPU-hours of insertion scans and annealing, which stalled at 1136–1300
convex 9-gons. A stalled search proves nothing about 128.

**Files.**
- `sets/`: the point sets.
- `logs/`: the certificate logs.
- `tools/`: `anneal8.c`, `cert.sh` and `pts2cfg.py`. The checkers are unchanged copies from
  `PRIMEFOLD/check120/producer/`.
- **Archive.** The full certificate directory, with orientation tables and search runs, is archived (zstd, round trip
  verified) in `proof-archives/final-2026-11-04-k9`.

**Reproducibility.** The annealing binaries were built from intermediate versions of `anneal8.c`, so the runs are not
bit-reproducible. The certificates are reproducible from the `.pts` files.
