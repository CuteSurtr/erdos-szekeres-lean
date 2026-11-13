# C6UPPER: the NOT-Y(1,2) half of the encoder-B split (6 November 2026)

**Result (certificate).** The encoder-B base formula `B_m6K8t11.cnf` (SHA-256 `479e31a9…`, `C6UPPER/SHA256SUMS.txt`)
is unsatisfiable on its own, without the reflection unit Y(1,2). The certificate is 64 cake_lpr verdicts
`s VERIFIED UNSAT`, each bound to the SHA-256 of its cube CNF:
- the 32 cubes base + Y(1,2) + pattern, accepted in the hash-bound replay of 6 November
  (`C6UPPER/replay-2026-11-06/results.tsv`, encoder B rows);
- the 32 cubes base + ¬Y(1,2) + pattern, solved and accepted here (`results.tsv`, 32 of 32 ACCEPTED, finished
  2026-11-06 15:40:35 KST, `SUMMARY.txt`).

The patterns are the 2^5 sign patterns of Y(1,3), Y(1,4), Y(2,3), Y(2,4), Y(3,4), so the 64 cubes carry the 2^6
sign patterns of the six variables Y(1,2), …, Y(3,4) (DIMACS variables 1, 2, 3, 10, 11, 18 in
`encb/B_m6K8t11.meta.json`): every assignment satisfies the units of exactly one cube.

**What this changes.** The sixfold upper bound used the reflection lemma (k8_soundness Lemma `k8s:lem:refl`, Y(1,2)
without loss of generality) to drop the half Y(1,2) = false. With this half certified, encoder B's base formula is
unsatisfiable outright, so the sixfold bound via encoder B needs neither that lemma nor the τ part of Lemma
`k8s:lem:affine`. Encoder A (the cross-check) still uses the reflection unit. Nothing else in the chain changes: the
written soundness proof of encoder B (not refereed, gaps G1–G4) and the Lean-checked reduction (`LAYERLEAN`) remain.

## How it was run

- Script `noty12.py` (copy of `/path/to/data/c6upper-noty12-20261106/noty12.py`), systemd user unit
  `c6upper-noty12` (MemoryMax 44G, no swap, Nice 5), 4 CaDiCaL lanes, 1 cake_lpr at a time, beside the budget-64
  campaign; 12:47–15:40 KST.
- Tools, checked by SHA-256 at start and again at the end (`TOOLS_AND_PROOFS.sha256`): CaDiCaL 2.1.3
  `/usr/bin/cadical` `4acf5860…`, cake_lpr `c14ff498…` (the binary of the 6 November replay, rebuilt from
  tanyongkiam/cake_lpr commit 033aad53; see `C6UPPER/replay-2026-11-06/README.md`).
- Base: the replay's regenerated `B_m6K8t11.cnf` (byte-identical to the record). Each cube = header `p cnf 78059
  2387089` + the exact base body + the units −1 and the five pattern literals (the layout of `tools/mkcubes.py` with the
  first unit negated). Cube hashes: `cubes.sha256`.
- Per cube: CaDiCaL `-q --lrat --binary=false` → SHA-256 of the proof → cake_lpr (`--CML_HEAP_SIZE=8000
  --CML_STACK_SIZE=4000`); only the exact line `s VERIFIED UNSAT` counts (cake_lpr exits 0 even when it rejects).
  Accepted proofs were compressed with zstd -3 and kept.
- Cost: 35,411 s of CaDiCaL time (0.8 s to 3,921 s per cube; the 12 phase-order cubes take 2,320–3,921 s, the 20
  cubes whose pattern contradicts transitivity take seconds), 2,471 s of cake_lpr; 56.3 GB of raw proofs, 14.9 GB as
  `.lrat.zst` (16.8 GB for the whole data directory) (kept in the data directory above, not in git; hashes in `results.tsv` column `zst_sha256` and
  `TOOLS_AND_PROOFS.sha256`).

## Checks

1. `verify_cover64.py` (before solving, `verify_cover64.log`): the 32 new cubes and the 32 replay cubes are each the
   exact base plus six units; first unit −Y(1,2) resp. +Y(1,2); 64 distinct patterns; every replay cube's hash equals
   an ACCEPTED encoder-B replay row.
2. `verify_final64.py` (after the run, `verify_final64.log`: **PASS**), stricter and run from the files alone:
   - tool, base and meta hashes as recorded (meta `68b43494…`), the six Y variables distinct and within 1..78059;
   - every cube byte-checked (header, exact base body, six unit lines matching `-?[1-9][0-9]* 0`), the pattern key
     taken from the units themselves, 64 distinct keys;
   - each n-cube: exactly one ACCEPTED row with cake line exactly `s VERIFIED UNSAT` and `cnf_sha256` equal to the
     file's current hash (also equal to `cubes.sha256` written before solving), its `.cake.log` has exactly that one
     s-line, its `.lrat.zst` has the recorded hash and decompresses to the recorded proof hash and size;
   - each c-cube: hash equal to exactly one ACCEPTED encoder-B replay row with that cake line;
   - tool hashes again at the end.
3. Review (in session, before the run finished): the verdict logic, the cover checker (with crafted counterexamples)
   and cake_lpr's DIMACS parser behaviour were attacked; the findings were addressed by `verify_final64.py` (it ties
   the n-cube rows to the files, checks the zstd step and re-checks the tools). Only one instance of `noty12.py` ran
   (`run.log`: one start line after the preparation dry run at 12:46).

## Files

| file | content |
|---|---|
| `noty12.py`, `verify_cover64.py`, `verify_final64.py` | the scripts as run |
| `results.tsv` | one row per cube: units, cnf_sha256, CaDiCaL rc and time, proof sha256 and bytes, verdict, cake line, cake time, zst sha256, date |
| `run.log`, `SUMMARY.txt` | the job log and its last line |
| `verify_cover64.log`, `verify_final64.log` | the two cover/certification checks |
| `cubes.sha256` | the 32 n-cube hashes, written before solving |
| `TOOLS_AND_PROOFS.sha256` | tool hashes and the 32 `.lrat.zst` hashes |
