# Certificates for the symmetric Erdős–Szekeres results

Revised 1 November 2026 (UTC). This file records every retained proof of the symmetric results in
`WRITEUP/SYMMETRIC.md`: the case it proves, the generator and command, the hashes, the tools and the checker verdicts.
It also says which proofs were not retained. Paths are relative to `cloud/es7-2026-10-19/results`.

The proofs are too large for Git. They are kept compressed in local archives on the machine that produced them, under
`<repository root>/proof-archives/`, outside Git:
- `es7-symmetry` (29 October, with `MANIFEST.md` and `manifest.json`): mirror34, mirror33, c5, c3hex, central34-cover
  and central34-hull;
- `es7-c4-32-cuts-2026-11-01`: c4cut-final (the CNF with the six cuts and its proof, the cuts, the map, the scripts, the
  logs and `SHA256SUMS`);
- `es7-central34-pilot-resolve-2026-11-01`: the 7 pilot re-solves (central34-pilot-resolve), one proof per unit;
- `es7-central34-resample-2026-11-01`: the 34 resample units (central34-resample), one proof per unit;
- `es7-central34-pilot-orbits-2026-11-01`: the 58 P8 pilot orbits (central34-pilot-orbits), one proof per unit;
- `es7-central34-local-2026-11-01`: the local-record units (central34-local), 44 of 65 proofs by 1 November 2026, 19:43 UTC
  (job still running);
- `es7-central34-lanespot-2026-11-01`: the lane spot check (central34-lanespot), 81 of 242 proofs by the same time
  (job still running);
- `es7-c3-indispensable-2026-11-01`: the 204 indispensable threefold σ-cube pieces (c3-indispensable), one proof per
  piece, with `MANIFEST.jsonl`;
- `es8-mirror46-2026-11-01`: two certificates for the mirror-symmetric octagon bound (`ES8SYM` §4), not used by the
  ES(7) results (last section).

For the re-solves the SHA-256 of each archive file and of its proof are in the record files (`C2FINAL`, `C2RECHECK`,
`C3PIECES`).

A later public release of the archives would need the owner's decision. Every archive file decompresses (`zstd -d`) to
the exact original bytes; the SHA-256 of both is listed here or in the named record file. Log paths in the entries are
paths inside the archive. Copies of most logs are in `SYMZ`, `SYM5`, `C4CUT` and `C2FINAL`; the c3hex log is in the
archive only.

## Tools (`tools/`)

| file | SHA-256 | origin |
|---|---|---|
| cadical | `e12ecc8ce8a489394a2b7411e3fa264f037e4ceb2e615bab534158e19d04ac01` | CaDiCaL 3.0.1, commit c6073042, built locally (arm64) |
| lrat-check | `f20462121defbc631f34850e06d5c0428ea4fecc4c890e6b755fd8e9bf9f534d` | drat-trim lrat-check 2e3b2dc with `lrat-check-E2.patch` |
| cake_lpr | `2fee767af4478ed817f8bdf6feea5866e5e59f1f67c2a4477e98ee961612881d` | cake_lpr a36874a8, CakeML-verified checker, arm8 build; heap is set with `--CML_HEAP_SIZE=<MB>` (the environment variable is ignored by this build) |
| lrat-check-E2.patch | `52721abdfb25b9beabc918f361230441c2f3eade72b7db4ab2a9f4811c91eac4` | patch fixing the upstream hintless-empty-clause defect (see `E2`) |

Scripts that set the heap only through the environment variable ran cake_lpr at its default heap of 4,096 MiB:
`SYM5/check.sh` (the L1 check and the failed P1 run below) and `C3U2/tools/controls.py` (`C3SPOT` and the threefold
pieces).

## mirror34

**Case.** Mirror-symmetric sets: 34 points in general position, 17 mirror pairs, no point on the axis, no 7 points in convex position (Theorem 2b).

**Hypotheses and soundness.** Encoding SYMZ/zcnf.py (axis-free branch identical to zcnf_v1.py): chirotope of the 34 points plus Z = (0,1,0); soundness proof in SYMZ/README.md.

**Generator.** zcnf_v1.py (sha256 8fb8a3ab6364214bb575d36b96366a512bbac6e0ab3e49891dd6c05a24a35a3d). Command: `python3 zcnf_v1.py mirror 17 7 -o m_t17k7.cnf --map m_t17k7.json` (regenerated 2026-10-29 with an identical SHA-256). The final `zcnf.py` writes the same clauses with one extra field in the comment line (SHA-256 `1b61bf2f2144c90a0f9cecc33903d1ad400864f4b2885a7353cf5e38fde92825`); the proof was also accepted on that file.

| file | bytes | SHA-256 | archive | archive bytes | archive SHA-256 | round trip |
|---|---:|---|---|---:|---|---|
| CNF (p cnf 838032 16642456) | 620,842,936 | `b175eac0e7c000f533506ea6931774f4969a0e0415011ba0c4fb47e7f09a6c5b` | `mirror34/m_t17k7.cnf.zst` | 76,834,682 | `33e5f6be15198ac65f01522f0595ade524a2a4a068e4a5fe21002172d0c6f06e` | verified |
| LRAT proof | 4,373,364,691 | `98e4d02a8f1e1e301603b9672dfe2c4e61e6659f14c2b5edc9e74bd31d4c6537` | `mirror34/mr34_def.lrat.zst` | 728,136,784 | `39e93b6e2909efb3950bfdc32489864a37dd1b6f9fc48d0580c950cf0a85ac04` | verified |

**Solver.** `cadical -t 43200 --lrat --binary=false m_t17k7.cnf mr34_def.lrat: s UNSATISFIABLE, c exit 20, 442.65 s`

**Checkers.**
- `lrat-check m_t17k7.cnf mr34_def.lrat: c VERIFIED, exit 0, 58 s (and 50 s on the regenerated CNF)`
- `cake_lpr --CML_HEAP_SIZE=30000 --CML_STACK_SIZE=4000 m_t17k7.cnf mr34_def.lrat: s VERIFIED UNSAT, exit 0, 268 s (and 314 s on the regenerated CNF)`
- independent audit 2026-10-29: lrat-check replay, exit 0, 45.45 s, hashes matched (its log is not in the repository)
- replay with hash-bound logs (`REPLAY`): hash stage only (`AUDIT3` §5 row 1); neither checker re-run by 1 November 2026, 19:43 UTC (cake_lpr heap 30,000 MiB)

**Logs.** `mirror34/cad_mr34_def.out`, `mirror34/chk_mr34_def_lrat-check.out`, `mirror34/chk_mr34_def_cake_lpr.out`, `mirror34/chk_mr34_final_*.out`, `mirror34/cad_mr34_sat.out (second configuration --sat, UNSAT in 304.81 s, no proof written)`

## mirror33

**Case.** Mirror-symmetric sets: 33 points in general position, 16 mirror pairs and exactly one point on the axis, no 7 points in convex position (Theorem 2a, single-certificate proof).

**Hypotheses and soundness.** Encoding SYMZ/zcnf.py with one axis point; soundness proof in SYMZ/README.md.

**Generator.** zcnf.py (sha256 13d6c162a617cff6f4c164d6c921efef18ee58df0e913f6fe98f63b5213a0989). Command: `python3 zcnf.py mirror 16 7 --axis 1 -o m_t16k7a1.cnf --map m_t16k7a1.json`

| file | bytes | SHA-256 | archive | archive bytes | archive SHA-256 | round trip |
|---|---:|---|---|---:|---|---|
| CNF (p cnf 695928 14080656) | 518,452,724 | `e45464edd52e06a31de4bbb664f444789540bad19039989679d76f7173739d02` | `mirror33/m_t16k7a1.cnf.zst` | 64,372,401 | `8298fabacd7489ec746971396d2d50ec33b09de909c095845d8af3218dc0787f` | verified |
| LRAT proof | 4,120,793,950 | `e1b2689d071a0b218f2c9be13a813f48bd3ea0fcd1e2fc1476a2549523ede1e4` | `mirror33/m33_def.lrat.zst` | 727,457,726 | `01f477fb1bcc9b160475da71749a04235ba03e920c086b3a2bb5cd15b54aa64a` | verified |

**Solver.** `cadical -t 43200 --lrat --binary=false m_t16k7a1.cnf m33_def.lrat: s UNSATISFIABLE, c exit 20, 964.37 s`

**Checkers.**
- `lrat-check m_t16k7a1.cnf m33_def.lrat: c VERIFIED, exit 0, 52 s`
- `cake_lpr --CML_HEAP_SIZE=30000 --CML_STACK_SIZE=4000 m_t16k7a1.cnf m33_def.lrat: s VERIFIED UNSAT, exit 0, 320 s`
- replay with hash-bound logs (`REPLAY`): hash stage only (`AUDIT3` §5 row 1); neither checker re-run by 1 November 2026, 19:43 UTC (cake_lpr heap 30,000 MiB)

**Logs.** `mirror33/cad_m33_def.out`, `mirror33/chk_m33_def_lrat-check.out`, `mirror33/chk_m33_def_cake_lpr.out`

## c5-angle

**Case.** Fivefold rotation: 35 points (7 orbits, centre not in the set), no 7 points in convex position; angle normal form.

**Hypotheses and soundness.** Encoding SYM5/symcnf.py, identical to ../tools/symmetric/symcnf.py (SYM5/README.md, §1-2).

**Generator.** symcnf.py (sha256 a8056da0c403e529ffaa2c80feffe12de7647d7dc26a641f58150a1b6faaa746). Command: `python3 symcnf.py 35 7 5 -o c5_n35.cnf --map c5_n35.json`

| file | bytes | SHA-256 | archive | archive bytes | archive SHA-256 | round trip |
|---|---:|---|---|---:|---|---|
| CNF (p cnf 401464 7923909) | 283,069,260 | `ead55228944c920a9ab26eaab98ae0f9963ecf69f651323a664e813715450dbb` | `c5/c5_n35.cnf.zst` | 37,230,654 | `b8595f81cb20e14aa85ac6e1f37f479225d99f00cbb5715fae51b812c3924aab` | verified |
| LRAT proof | 2,793,662,637 | `eff67c0f4e9b3f29d676b2d7fc5c50700a09923dad71050950ae68b9e6ee9484` | `c5/P1.lrat.zst` | 538,942,678 | `6c4812b4acf2734d7e5fab51e395fb576bf19e51ae65e815f1051a212b785a81` | verified |

**Solver.** `cadical -t 7200 --lrat --binary=false c5_n35.cnf P1.lrat: s UNSATISFIABLE, c exit 20, 414.72 s`

**Checkers.**
- `lrat-check c5_n35.cnf P1.lrat: c VERIFIED, exit 0, 22 s`
- `cake_lpr --CML_HEAP_SIZE=30000 --CML_STACK_SIZE=4000 c5_n35.cnf P1.lrat: s VERIFIED UNSAT, exit 0, 66 s`. The first run, at the default heap of 4,096 MiB, ran out of heap (`chk_P1_cake_lpr_heap12000.out`; the file name records a setting that never took effect). No committed script runs the 30,000 MiB check.
- replay with hash-bound logs (`REPLAY`): hash stage only (`AUDIT3` §5 row 1); neither checker re-run by 1 November 2026, 19:43 UTC (cake_lpr heap 30,000 MiB)

**Logs.** `c5/cad_P1.out`, `c5/chk_P1_*.out`

## c5-layer

**Case.** Fivefold rotation: 35 points, no 7 points in convex position; layer normal form (seven nested pentagons).

**Hypotheses and soundness.** Encoding SYM5/symcnf_layers.py and the layer lemma (SYM5/README.md).

**Generator.** symcnf_layers.py (sha256 71b2d7e7a778e2552a6aedc183129465bab8ad12677783ee6e7b343b6f1de58e) importing symcnf.py. Command: `python3 symcnf_layers.py 35 7 5 -o c5_n35L.cnf --map c5_n35L.json`

| file | bytes | SHA-256 | archive | archive bytes | archive SHA-256 | round trip |
|---|---:|---|---|---:|---|---|
| CNF (p cnf 401464 7924027) | 283,069,961 | `90dea1cf87d3d8500dffff9d9741e84abc9babe4e1ac4e32035448ce7c0668a8` | `c5/c5_n35L.cnf.zst` | 37,230,888 | `503a7ff18ba65dadd04b895987df4667f9b59445dffd4872d616dcc085179de8` | verified |
| LRAT proof | 1,812,130,098 | `8625b321d58ed231924ffd22ffd730fde91314c898b835ea182848c9100d39f4` | `c5/L1.lrat.zst` | 305,442,395 | `de461bad09ee857218b3204ef1971ed9e15fc58420c403354843008fcedd707e` | verified |

**Solver.** `cadical -t 7200 --lrat --binary=false c5_n35L.cnf L1.lrat: s UNSATISFIABLE, c exit 20, 54.35 s`

**Checkers.**
- `lrat-check c5_n35L.cnf L1.lrat: c VERIFIED, exit 0, 14 s`
- `cake_lpr c5_n35L.cnf L1.lrat`, at the default heap of 4,096 MiB (`SYM5/check.sh` set the heap only in the environment; peak footprint 4,101 MiB): `s VERIFIED UNSAT, exit 0, 56 s`
- independent audit 2026-10-29: lrat-check replay, exit 0, 18.1 s; CNF hash regenerated
- replay of 1 November with hash-bound logs: lrat-check `c VERIFIED` (`AUDIT3` §5 row 1); full replay with both
  checkers (`REPLAY`, 17:59–18:01 UTC): lrat-check `c VERIFIED`, `cake_lpr --CML_HEAP_SIZE=8000` `s VERIFIED UNSAT`,
  input hashes equal to this entry before and after the checks

**Logs.** `c5/cad_L1.out`, `c5/chk_L1_*.out`

Also archived: L2.lrat (sha256 dfbb6b60dcebd6bc402d76cf14bffb368d0627936939c474bd9060f95f15647c), a second proof of the same CNF from the --unsat configuration (59.84 s). It was first checked in the replay of 1 November: lrat-check `c VERIFIED`, with a hash-bound log (`AUDIT3` §5 row 1); cake_lpr had not been run on it by 1 November 2026, 19:43 UTC. It is not needed, since P1 and L1 each settle the case.

## c3-hex-15

**Case.** Threefold rotation, hexagons: 15 points (5 orbits, no centre), no 6 points in convex position.

**Hypotheses and soundness.** Encoding ../tools/symmetric/symcnf.py.

**Generator.** symcnf.py (same file as c5-angle). Command: `python3 symcnf.py 15 6 3 -o c3_n15k6.cnf`

| file | bytes | SHA-256 | archive | archive bytes | archive SHA-256 | round trip |
|---|---:|---|---|---:|---|---|
| CNF (p cnf 1646 126785) | 3,218,440 | `fc089011c5934f6bf63c581b5630712c83fc344e248325c10f71c62e9e99c811` | `c3hex/c3_n15k6.cnf.zst` | 459,623 | `a22b900e7c2b1eb8ac6645de9cd7cd04530b015a26ace87ed91d94bb3b13f927` | verified |
| LRAT proof | 3,344,626 | `659a3db6b2f3e5d2cd1bbc3cda9abf5608213878828f52c1fea028e37d0aa859` | `c3hex/c3_n15k6.lrat.zst` | 855,150 | `18701a0ba6c7755baffc06ba3c354cb5d6687a43011b922ac23193bf11ccc3b3` | verified |

**Solver.** `cadical -q --lrat --binary=false c3_n15k6.cnf c3_n15k6.lrat: s UNSATISFIABLE`

**Checkers.**
- lrat-check: c VERIFIED, exit 0; cake_lpr: s VERIFIED UNSAT (rerun 2026-10-29, c3hex/chk_c3hex.log); lrat-check replayed by `AUDIT3` (A6)

**Logs.** `c3hex/chk_c3hex.log`

## c3-hex-16

**Case.** Threefold rotation, hexagons: 16 points (5 orbits and the centre), no 6 points in convex position.

**Hypotheses and soundness.** Encoding ../tools/symmetric/symcnf.py with --center-in-set.

**Generator.** symcnf.py (same file as c5-angle). Command: `python3 symcnf.py 16 6 3 --center-in-set -o c3_n16k6c.cnf`

| file | bytes | SHA-256 | archive | archive bytes | archive SHA-256 | round trip |
|---|---:|---|---|---:|---|---|
| CNF (p cnf 2256 129171) | 3,293,272 | `15766b1e6e44f9b8f4dcf222ce8440b454d635521dfa0eda7b4759a92836690e` | `c3hex/c3_n16k6c.cnf.zst` | 475,233 | `b4f20ebfca59b6d12200fc91054785852c4e1920d221d16efe7d1b562e0f9517` | verified |
| LRAT proof | 1,858,678 | `1c4c5e37a79d339e4c2bf0280b38fc48f27568f8e284eea08594d9df2bcc318f` | `c3hex/c3_n16k6c.lrat.zst` | 451,192 | `0f2aefe8ba2a2b62385521f3ec299bbf71f837527bdd8b63b6ed4a7c707b729b` | verified |

**Solver.** `cadical -q --lrat --binary=false c3_n16k6c.cnf c3_n16k6c.lrat: s UNSATISFIABLE`

**Checkers.**
- lrat-check: c VERIFIED, exit 0; cake_lpr: s VERIFIED UNSAT (rerun 2026-10-29, c3hex/chk_c3hex.log); lrat-check replayed by `AUDIT3` (A6)

**Logs.** `c3hex/chk_c3hex.log`

## central34-cover

**Case.** Centrally symmetric sets of 34 points: the 136 convex-hull cases of `SYMZ/hullcubes.py` cover the formula
`zcnf.py rot 17 7 --m 2 --hull` (the hull of such a set without a convex 7-gon is a centrally symmetric quadrilateral or
hexagon through the first point). This certifies that the case split is exhaustive. All cases were then refuted
(central34-hull below; parallelograms in `C2P`–`C2P5`), and `C2FINAL` claims the central 34-point theorem.

**Hypotheses and soundness.** The encoding `SYMZ/zcnf.py` (kind `rot`, m = 2, with the centre as an element and the
hull-vertex normal form); written soundness proof in `C2ENC` (`proof.md`), refereed on 1 November.

**Generator.** `python3 zcnf.py rot 17 7 --m 2 --hull -o c34h.cnf --map c34h.json`, then
`python3 hullcubes.py c34h.cnf c34h.json hc34`, which writes `hc34/cubes.txt` and `hc34/cover.cnf` (the formula plus the
negation of every cube).

| file | bytes | SHA-256 | archive | archive bytes | archive SHA-256 | round trip |
|---|---:|---|---|---:|---|---|
| CNF (cover.cnf) | 621,058,015 | `bb60facb223788fb57291c73abfacd6deaa1eccd82ad2be9f50d36292959a60f` | `central34/cover.cnf.zst` | 76,790,623 | `7920297253a16ea5bda7fe5cfe045f24ade116622918ff0c96856ebf84ff3e89` | verified |
| LRAT proof | 3,833,946,210 | `3255391a5fd28472f48b286660eab67234d0094736df0d4f8c2d48b5eeb20aef` | `central34/hc34_coverL.lrat.zst` | 599,321,920 | `c38e458064a592b1c0b4bb65338b7af60c4848c875e09a6addcc19524eefd461` | verified |

**Solver.** `cadical -t 3000 --lrat --binary=false cover.cnf hc34_coverL.lrat: s UNSATISFIABLE, 186.54 s`

**Checkers.**
- `lrat-check cover.cnf hc34_coverL.lrat: c VERIFIED, exit 0, 50 s`
- `cake_lpr --CML_HEAP_SIZE=20000 --CML_STACK_SIZE=4000 cover.cnf hc34_coverL.lrat: s VERIFIED UNSAT, exit 0, 448 s` (the command is in no committed script; the log's peak footprint of 20,030 MiB agrees)
- replay with hash-bound logs (`REPLAY`): hash stage only (`AUDIT3` §5 row 1); neither checker re-run by 1 November 2026, 19:43 UTC (cake_lpr heap 20,000 MiB)

**Logs.** `central34/cad_hc34_coverL.out`, `central34/chk_hc34_cover_lrat-check.out`, `central34/chk_hc34_cover_cake_lpr.out`, `central34/cubes.txt`, `central34/canonical.txt`; copies in `C2FINAL/evidence/central34-cover/`

## central34-hull

**Case.** Centrally symmetric sets of 34 points: the hexagonal-hull cases `H<a>-<b>` of `C2C34/hullcubes.py`.
Each case CNF is the base `c34h_final.cnf` (`zcnf.py rot 17 7 --m 2 --hull`, SHA-256
`b0061e908bff80e6a597f31a6fec1d91e8504aebc09b0bcf41c2ff21604d8ff1`) plus the hull cube of the case as unit clauses
(`C2C34/cubes.txt`).

**Records.** Per case, `C2C34/logs/hex_cases.tsv` lists the case CNF SHA-256, the proof size and SHA-256, the archive
SHA-256 and round trip, and the lrat-check and cake_lpr verdicts. Archive files are `central34-hull/<case>.lrat.zst`.

**Solver.** `cadical -t 3600 --lrat --binary=false <case>.cnf <case>.lrat` (CaDiCaL 3.0.1).

**Checkers.** `lrat-check <case>.cnf <case>.lrat` at solve time, and `cake_lpr --CML_HEAP_SIZE=16000 --CML_STACK_SIZE=4000`
on the decompressed archive copy, with a CNF rebuilt by the same command but not hashed (`C2C34/hchecker.sh`).

**Counts.**

```
hexagonal-hull cases with proofs: 120 run, 120 UNSAT, lrat-check VERIFIED 120, archive round trip 120, cake_lpr VERIFIED 120
canonical hexagonal cases UNSAT: 24/24; cake_lpr on canonical: 24/24
all hexagonal cases UNSAT: 120/120; missing: []
solve time: min 291 s, median 687 s, max 1562 s; proofs total 524.3 GB
```

**Re-check on hash-checked files (started 1 November).** For each case: rebuild the case CNF and require the recorded
SHA-256; require the recorded archive SHA-256; decompress and require the recorded proof size and SHA-256; run
lrat-check and cake_lpr (heap 8,000 MiB, 16,000 MiB if exhausted) on exactly these files. Result (finished 1 November,
17:59 UTC): 120 of 120 cases with all hashes equal and both verdicts, cake_lpr at 8,000 MiB in every case. Script and
records: `C2RECHECK`.

## c4cut-final

**Case.** Fourfold rotation: 32 points (8 orbits, centre not in the set), no 7 points in convex position (`C4CUT`).

**Hypotheses and soundness.** Encoding `SYM5/symcnf_layers.py` with m = 4 (layer lemma; written soundness argument,
reviewed in `C4CUT/review`), plus six cut clauses, each justified by a Grassmann–Plücker final-polynomial certificate on
the inner 12 points that uses no symmetry (exact verification: `C4CUT/verify_cuts.py`).

**Generator.** `python3 SYM5/symcnf_layers.py 32 7 4 -o c4_n32L.cnf --map c4_n32L.json` (base `p cnf 287296 5272494`,
SHA-256 `c3933d9a571d3912fc009b3cd331e18097ae9d44639018ca6923a6ed7931e68e`; map `f72b186e…`), then one clause per line
of `C4CUT/cuts.jsonl` (SHA-256 `3852ece5c7c5496a9bc0d5576e9894ddc182ed847b20b51102dc0a46df54c7de`) appended by
`C4CUT/c4final.sh`.

| file | bytes | SHA-256 | archive | archive bytes | archive SHA-256 | round trip |
|---|---:|---|---|---:|---|---|
| CNF (p cnf 287296 5272500) | 183,470,218 | `2aa18f1e89152959c13adec575d3fda4a01b0dedaef2388984ba6fe6bfdb78d1` | `c4_n32L_cuts.cnf.zst` | 24,321,041 | `3dcb89217439565c9421d6ee7063f47983c6fcdcd67cd50a31c1c92323f39922` | ok |
| LRAT proof | 1,040,775,249 | `6e1199aa2ecd80dc7edbad9c16dba8aac1c69e9d9f20a1bf9eeb61a1196ba9c4` | `c4cuts.lrat.zst` | 191,694,745 | `0bf2d79e208f2d4db83e5c7f6db9de3c67c01121c6b11cc8f10fbe2577b45548` | ok |

**Solver.** `cadical -t 3600 --lrat --binary=false c4_n32L_cuts.cnf c4cuts.lrat: s UNSATISFIABLE, c exit 20, 29.35 s` (CaDiCaL 3.0.1 c6073042, named in the log; the checker binaries are not named in the records)

**Checkers.** lrat-check `c VERIFIED`; `cake_lpr --CML_HEAP_SIZE=8000 --CML_STACK_SIZE=4000`: `s VERIFIED UNSAT`. Only
these verdict lines were kept (`C4CUT/final.json`); the raw checker output was not. Replay of 1 November with
hash-bound logs: lrat-check `c VERIFIED` (`AUDIT3` §5 row 1). Full replay with both checkers (`REPLAY`, 18:01–18:02
UTC): lrat-check `c VERIFIED`, cake_lpr (heap 8,000 MiB) `s VERIFIED UNSAT`, input hashes equal to this entry.

**Logs.** `cad_c4cuts.out`, `final.json`, `c4cut.log`, `SHA256SUMS` (the archive also holds `cuts.jsonl`, the map and the
scripts; its `verify_cuts.py` is the version from before the review).

## central34-pilot-resolve

**Case.** The seven units of the P8 pilot whose records had no CNF hash: `P8_cover` and the subcases `P8_1-3`,
`P8_2-4-11`, `P8_2-12-15`, `P8_3-4-5`, `P8_3-4-15` and `P8_9-13-15` (`C2FINAL` §4).

**Records.** `C2FINAL/pilot/out.jsonl`, one line per unit: CNF SHA-256 (required to equal the hash rebuilt as
`C2P/tools/lane.py` builds it), proof size and SHA-256, both verdicts (cake_lpr heap 8,000 MiB), archive file, size and
SHA-256, round trip. Script: `C2FINAL/pilot/resolve.py`.

**Counts.** 7 of 7 UNSAT, both checkers accept, round trips verified. The six subcases reproduced the proof SHA-256
recorded by the pilot; the cover's CNF (`8851e2ac…`) differs from the pilot's in clause order only.

## central34-resample

**Case.** Central 34-point units re-solved to test the records (`C2FINAL` §5): 2 reproducibility tests, the random sample
of 24 units (`C2FINAL/sample/sample.txt`, seed 20261101) and a second draw of 8 hexagonal units (`extra_sample.txt`,
seed 20261102).

**Records.** `C2FINAL/sample/out.jsonl` (the 2 tests, then the 24 sample units) and `extra_out.jsonl`: CNF SHA-256
compared with the record, proof size and SHA-256 compared with the record, both verdicts, archive file, size and SHA-256,
round trip. Script: `C2FINAL/sample/reproduce.py`.

**Counts.** 34 of 34 UNSAT with the recorded CNF hash, both checkers accept, round trips verified. 33 proofs equal the
recorded ones byte for byte. `P8_1-10` (CNF `163f52ea…`, record `C2P2/M02`) gave a different proof: 9,952,275,647 bytes,
SHA-256 `e98aa3ee…`, archive `P8_1-10.lrat.zst` `2e701cb3…`.

## central34-pilot-orbits

**Case.** The 58 orbits of P8 closed in the pilot, whose cake_lpr check had run on a rebuilt CNF that was not hashed
(`C2C34/p8/checker.sh`). Each unit is re-solved on a CNF that must have the recorded hash, both checkers are run, and the
proof is archived with a round trip.

**Counts** (finished 1 November, 17:33 UTC). 58 of 58 UNSAT with the recorded CNF hash, both checkers accept (cake_lpr
heap 8,000 MiB), round trips verified. All 58 proofs equal the recorded ones byte for byte. Records and script:
`C2RECHECK`.

## central34-local

**Case.** The 60 orbit representatives and the P1–P5 covers that rest only on records of the local Mac lanes
(`C2P*/LOCAL*`), which keep no record of the tools used. Same method as above; proofs archived with round trips in
`es7-central34-local-2026-11-01`.

**Counts** (job still running). 44 of 65 by 1 November 2026, 19:43 UTC: all UNSAT with the recorded CNF hash,
both checkers accept (cake_lpr heap 8,000 MiB), round trips verified, and all 44 proofs equal the recorded ones byte
for byte. Records and script: `C2RECHECK`.

## central34-lanespot

**Case.** A lane-stratified spot check of the central records (`AUDIT3` §5 row 8): one unit from each of the 242 lanes
of `C2P`–`C2P5` that no earlier re-solve had reached (281 lanes have certified records; central34-resample and
central34-local reached 38, and `C2P/LOCAL_L3`, whose pieces close no orbit, is left out). Same method as above;
proofs archived with round trips in `es7-central34-lanespot-2026-11-01`.

**Counts** (job still running). 81 of 242 by 1 November 2026, 19:43 UTC, from 81 different lanes: all UNSAT with
the recorded CNF hash, both checkers accept (cake_lpr heap 8,000 MiB), round trips verified, and all 81 proofs equal
the recorded ones byte for byte. Records and script: `C2RECHECK`.

## c3-indispensable

**Case.** The 204 threefold pieces certified only by records in σ-cube format that the `C3FINAL` cover cannot do
without (84 from `C3SIG2`, 120 from `C3W3S`). All 204 CNF hashes were rebuilt from the records. Each piece is re-solved,
both checkers are run and the proof is archived; σ-cube records carry no proof hash, so a re-solve is compared by proof
size only.

**Counts** (finished 1 November, 18:22 UTC). 204 of 204 UNSAT on CNFs with the recorded hash, both checkers accept
(cake_lpr heap 6,000 MiB), round trips verified. 200 proofs have the recorded size; the other 4 are different proofs,
accepted by both checkers. Records and script: `C3PIECES`; the archive's `MANIFEST.jsonl` gives the archive, proof and
CNF SHA-256 of each piece.

## Replay of the retained certificates

A replay kit lists 191 retained certificates. For each it requires the archive, proof and CNF SHA-256 recorded here or in
the named records, then runs lrat-check and cake_lpr on exactly those files, with logs that state the hashes, commands
and exit codes. Done on 1 November: the hash stage for all 191, and lrat-check on the 18 proofs under 2 GB, all
`c VERIFIED` (`AUDIT3` §5 row 1); among them c5 L1 and L2, c3hex-15 and -16, c4cut-final, 2 pilot and 11 resample
units. Full replay
with both checkers on 1 November (17:59–18:02 UTC): c5 L1, c3hex-15, c3hex-16 and c4cut-final, each with the recorded
archive, proof and CNF SHA-256 before and after the checks, lrat-check `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`
(heap 8,000 MiB for L1 and c4cut-final, 2,000 MiB for c3hex). Not run by 1 November 2026, 19:43 UTC: mirror33,
mirror34 and c5 P1 (cake_lpr heap 30,000 MiB each), the cover (20,000 MiB) and L2 (8,000 MiB). Kit, plan and logs:
`REPLAY`.

## Reproduction

1. Decompress: `zstd -d <name>.zst` and compare `shasum -a 256` with the table or record.
2. Or regenerate the CNF with the stated generator and command (`SYMZ`, `SYM5`, `C2C34`, `C4CUT`, `../tools/symmetric`) and compare its SHA-256.
3. Check: `lrat-check <cnf> <proof>` must print `c VERIFIED`; `cake_lpr --CML_HEAP_SIZE=<MB> <cnf> <proof>` must print `s VERIFIED UNSAT`. The heap used is given in each entry; none of the recorded runs used more than 30,000 MiB.
4. Optionally re-solve with the stated CaDiCaL command; CaDiCaL is deterministic for a fixed binary, formula and options, but a re-solve may produce a different proof file on another build.

## Not in the archive

- Threefold 33-point exclusion: the LRAT proofs of its 116,883 pieces were deleted after both checkers accepted them at solve time; 26,436 records carry the proof's SHA-256. The records, the composition and its Lean bookkeeping, and a 2,120-piece random re-solve are in the repository (`C3FINAL`, `C3LEAN`, `C3SPOT`). The regeneration plan is below.
- Central 34-point theorem, parallelogram part: the proofs of the 2,385 UNSAT records were deleted after both checks. The units re-solved since then have archived proofs (above). See the section on the central theorem below.
- Mirror 33-point proof chain of 2026-10-21 (Lean): its CNF facts have recorded cake_lpr verdicts; the proof files were not retained. The proof mirror33 above is a retained certificate for the same case, with a written (not Lean) soundness proof of its encoding.

## The threefold 33-point exclusion: what is and is not retained

**What is retained.** The 116,883 certified records (`C3FINAL/compose_files.txt`):
- each with the CNF hash of its piece and the verdicts of lrat-check and cake_lpr recorded at solve time;
- 26,436 of them also with the SHA-256 of their LRAT proof.

**What is not.** The proofs themselves were deleted after checking.

**What has been checked again.**
- The double composition, which re-derives every piece's CNF hash and covers all 910 roots (`C3FINAL`; also
  replayed by an independent audit), and its Lean check: the 73,567 leaves of one cut cover the 910 roots (`C3LEAN`).
- 2,120 pieces drawn at random and re-solved from scratch with fresh proofs and both checkers (`C3SPOT`). The draw
  excluded the records in σ-cube format.
- The 204 indispensable σ-cube pieces (c3-indispensable above): all 204 re-solved and certified, proofs archived.
- None of this recreates the deleted proofs, and the random re-solve is evidence, not an exhaustive check.

**Regeneration plan.**
1. Rebuild the pinned tools: CaDiCaL c6073042, lrat-check 2e3b2dc with the E2 patch, cake_lpr a36874a8
   (`C3W4/TASK.md`, step 1). Check the base CNF hash `bf0e502e…6cdd6da`.
2. For each certified record, rerun `C3U2/tools/close_tree.py` (cad4e050) on its node with the recorded
   options (the record's `cadical_args`). Use `run_ct.py` from `C3W7/LOCAL2`, as `C3SPOT/lane6.sh` does.
3. Keep every proof compressed (zstd) with its SHA-256. Check it with both checkers.
4. Rerun `C3U2/tests/frontier_cmp.py` on the regenerated records.

Cost: the spot-check took 22.9 solve core-hours plus 7.1 check core-hours for 2,120 pieces, and the last 698 pieces
of the original campaign took 164 core-hours. A full regeneration therefore needs a campaign of the original's size.
Proof storage may reach terabytes before compression.

## The central 34-point theorem: what is and is not retained

**What is retained.** The proofs of the hull cover and of the 120 hexagonal hulls; the 7 pilot and 34 resample
re-solves; the re-solves of 1 November (the 58 pilot orbits; 44 local-record units and 81 lane spot-check units by
1 November 2026, 19:43 UTC). The 2,492 records of `C2P`–`C2P5` and the P8 pilot
(`C2C34/logs/p8_units.tsv`): each of the 2,385 UNSAT records has both verdicts, the proof size and SHA-256 and, apart
from seven pilot records, the CNF hash; the other 107 ran out of time. `C2FINAL` rebuilt all 2,589 recorded CNF hashes
from the base and checks the orbit bookkeeping in Lean.

**What is not.** The proofs of the other parallelogram records were deleted after both checks. Proofs are not always
reproducible: `P6_1-7` has one CNF but two different accepted proofs (`C2FINAL` §5), so a re-solve is checked afresh by
both checkers.

**Regeneration.** Re-solve a unit with `C2FINAL/sample/reproduce.py`, which rebuilds the CNF as `C2P/tools/lane.py`
does, requires the recorded hash, runs both checkers and, with `REPRO_ARCHIVE` set, archives the proof.

## The 2026-10-21 mirror 33-point proof chain

Its Lean statement rests on about 75,000 CNF facts with recorded cake_lpr verdicts (`WRITEUP/MIRROR.md`). The
proof files were not retained. The 33-point proof above (`mirror33`) is a single retained certificate for the same
case. It uses a different encoding whose soundness is a written proof (`SYMZ/README.md`), not a Lean proof.
Theorem 2 also follows from Baek's theorem through the mirror reduction (`WRITEUP/SYMMETRIC.md`, Theorem 2), with no
SAT input; that derivation is Lean-checked in `SYMLEAN/mirror`.

## The mirror-symmetric octagon bound (`es8-mirror46-2026-11-01`)

Not used by the ES(7) results. Two certificates that there is no 23-point set with distinct x-coordinates, in general
position, with no 4-cap and no 8 points in convex position (`ES8SYM` §4); the bound 46 itself is a corollary of Baek's
theorem, Lean-checked in `SYMLEAN/mirror`. The archive holds the two CNFs (encoding A `d7088e45…`, encoding B
`47f4cc18…`), their LRAT proofs compressed with zstd (decompressed `c81ea660…`, 1,848,737,159 bytes, and `46f99989…`,
1,865,183,930 bytes), both encoders, a 46-point set and `SHA256SUMS`. Both proofs: lrat-check `c VERIFIED`, cake_lpr
(heap 3,000 MB) `s VERIFIED UNSAT`. Hashes and logs: `ES8SYM/mirror/`.
