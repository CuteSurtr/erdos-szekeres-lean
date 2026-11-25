# resolve-sym-20261125: Linux re-certification of D2, C4 and C5 (PRE-REGISTRATION, 25 Nov 2026 ~16:45 KST)

**Why.** RESULTS.md labels D2 (7-fold octagon), C4 (5-fold heptagon) and C5 (4-fold heptagon) CERTIFIED, but their
proofs came from CaDiCaL 3.0.1 on the Mac and were checked by a macOS cake_lpr build (2fee767a…) whose provenance was
never checked; some cake logs name no input and carry no hashes (sat-encoders-map, 25 Nov). es-research §2 defines
CERTIFIED as a CaDiCaL 2.1.3 LRAT proof accepted by cake_lpr (`s VERIFIED UNSAT`) with hashes recorded. The payloads
are on the Mac only (the private backup holds just their inventory). The generators and the recorded CNF hashes are in
this repository, so each formula can be regenerated here, matched byte for byte, and certified here.

## Formulas (each must match its recorded SHA-256 before any solving; mismatch = stop and report)

| result | command (repo-relative, archive/es7-2026-10-19/results/) | recorded CNF sha256 | Mac CaDiCaL 3.0.1 |
|---|---|---|---|
| C4 (5-fold, 35 points) | `python3 SYM5/symcnf_layers.py 35 7 5 -o c5_n35L.cnf --map c5_n35L.json` | `90dea1cf87d3…c0668a8` (SYM5/sha256.txt) | 54 s |
| C5 (4-fold, 32 points) | `python3 SYM5/symcnf_layers.py 32 7 4 -o c4_n32L.cnf --map c4_n32L.json` (base `c3933d9a…`), then `C4CUT/c4final.sh` steps that append the six cuts of `C4CUT/cuts.jsonl` (`3852ece5…`) | `2aa18f1e…` (C4CUT README, 183,470,218 B) | 29 s, 4.1 GB |
| D2 (7-fold, 65 points) | `python3 C7UPPER/gen_b.py` with the (7, 8, 10) arguments of `C7UPPER/repro.sh`, cross-checked with the Lean printer `encb_dimacs twin-base 7 8 10` (exe `3d43fa8b…`) | `b4d290176cb6…d296e2` (C7UPPER/SHA256SUMS.txt:18) | 802 s, 1.6-1.7 GB |

## Method

- `.claude/skills/es-research/scripts/certify_cnf.sh CNF OUTDIR HEAP --keep` (CaDiCaL 2.1.3, `--lrat=true
  --binary=false`; cake_lpr c14ff498…; the verdict counts only on the exact line `s VERIFIED UNSAT`; proof kept as
  `.lrat.zst`; one JSON line per formula with CNF and LRAT SHA-256 in `certify.jsonl`).
- Units `esr-vfy-rs-<name>` (memguard track vfy 20,000 MB), CPUQuota 100 %, MemorySwapMax 0, nice 10, one at a time,
  started only when s35_20's Root join is finished (the esr total of 36,000 MB must keep its margin), MemoryMax 10G,
  RuntimeMaxSec 14400, cake heap 4000 MB (C4 L1 needed the default 4,096 MiB on the Mac; D2 replayed at 4000 in 40 s).
- HEURISTIC: C4 and C5 a few minutes each; D2 15-60 min (CaDiCaL 2.1.3 may be slower than 3.0.1); proofs 1.6-2 GB
  text each before zstd; total under 2 h. If a solve exceeds its deadline: stop, report, no label change.
- Optional E3 evidence for D2 (the Lean route): cake_lpr's parse-and-print run on the 67.8 MB text, compared with cmp.

## Outcome and labels

- Per formula: CNF sha256 = record, `s VERIFIED UNSAT`, proof kept (zstd) → that formula is CERTIFIED in the §2 sense
  on this machine. The results' labels change only after the advisor consult; the Mac verdicts stay recorded as
  earlier evidence (CaDiCaL 3.0.1, macOS cake_lpr).
- C4/C5 encoder soundness stays a written argument until a Lean encoder exists; D2 is already Lean-checked modulo this
  one verdict (FORMAL20261122/sevenfold), so its Lean label then rests on a Linux CERTIFIED verdict.
