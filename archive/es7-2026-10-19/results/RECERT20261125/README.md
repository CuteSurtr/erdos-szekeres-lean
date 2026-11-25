# RECERT20261125: Linux re-certification of the C4, C5 and D2 formulas (25 November 2026)

**Status: CERTIFIED (es-research §2) for the three formulas below, on this Linux machine, with the proofs kept.**
Before this, the three formulas had cake_lpr verdicts from the Mac only: proofs from CaDiCaL 3.0.1 checked by the macOS
cake_lpr build `2fee767a…`, whose build was never reproduced from source, some cake logs without hashes, and proofs
outside this machine (adversarial audit of 25 Nov; RESULTS.md labels lowered in 09e430d09). Those verdicts remain as
earlier evidence. No result statement changes; what changes is the evidence label of the step each formula carries.

## Statement

Each formula is unsatisfiable:

| result | formula (regenerated) | SHA-256 (= record) | record |
|---|---|---|---|
| C5 (4-fold, 32 points, heptagon) | `c4_n32L_cuts.cnf`, 183,470,218 B, `p cnf 287296 5272500` | `2aa18f1e89152959c13adec575d3fda4a01b0dedaef2388984ba6fe6bfdb78d1` | C4CUT `final.json` |
| C4 (5-fold, 35 points, heptagon) | `c5_n35L.cnf`, 283,069,961 B | `90dea1cf87d3d8500dffff9d9741e84abc9babe4e1ac4e32035448ce7c0668a8` | SYM5 `sha256.txt` |
| D2 (7-fold, octagon) | `B_m7K8t10.cnf`, 67,820,434 B | `b4d290176cb675c61ecbcf70380cc520aabf093d00e2572328a0975ae2d296e2` | C7UPPER `SHA256SUMS.txt:18` |

The meaning of each formula (its encoder and soundness argument) is that of its record, unchanged: C4 and C5 rest on
written encoder arguments (reviewed, not refereed); D2's encoder B is Lean-checked (FORMAL20261122/sevenfold,
`EncB.Geo7.sevenfold_es8_of_text`), whose label reads "Lean-checked modulo the cake_lpr verdict ... and ENCBLEAN's trust
items E1, E3-E6"; the verdict is now also the Linux one below.

## Method (pre-registered in `PLAN.md` before any solving)

1. `tools/regen.sh`: each formula regenerated from the repository's own generator (`SYM5/symcnf_layers.py 35 7 5`;
   `SYM5/symcnf_layers.py 32 7 4` plus the six cuts of `C4CUT/cuts.jsonl` appended exactly as `C4CUT/c4final.sh` does;
   `C7UPPER/gen_b.py 7 8 10`; for D2 also, as pre-registered, the Lean printer `encb_dimacs twin-base 7 8 10`
   (ENCBLEAN exe `3d43fa8b…`, 8.3 s: the text is byte-identical to gen_b.py's, sha256 `b4d29017…`, and cake_lpr
   c14ff498's parse-and-print of it equals it line for line, header included; `data/d2_lean_print_time.txt`); all five hashes (three formulas, the C5 base `c3933d9a…` and `cuts.jsonl` `3852ece5…`)
   MATCH the records (`data/regen.log`).
2. `tools/run_certify.sh`: the house script `.claude/skills/es-research/scripts/certify_cnf.sh` per formula, each CNF
   re-hashed first: CaDiCaL 2.1.3 `--lrat=true --binary=false`, then cake_lpr `c14ff49853e89043…` (`--CML_HEAP_SIZE`
   8000 / 4500 / 4000); the verdict counts only on the exact line `s VERIFIED UNSAT`.

## Results (`data/certify.jsonl`, `data/run.log`, `data/*.cake.out`)

| formula | CaDiCaL | LRAT bytes | LRAT SHA-256 | cake_lpr | verdict | kept proof (`.lrat.zst`) SHA-256 |
|---|---|---|---|---|---|---|
| `c4_n32L_cuts` | 40 s | 1,061,805,442 | `841bb779a5d674957932d604077a98591bd6854a22e64775459d8b5f2264ab4d` | 29 s | `s VERIFIED UNSAT` | `92e76dbe…` |
| `c5_n35L` | 63 s | 1,818,055,668 | `df331f70109609d1fd42828c3c38efcd3f015a709bbb565e62594d1a3f8784b2` | 57 s | `s VERIFIED UNSAT` | `e46225c8…` |
| `B_m7K8t10` | 538 s | 1,678,550,246 | `17707d6c60f3a7b2…` (full in certify.jsonl) | 36 s | `s VERIFIED UNSAT` | `717b67db…` |

Each `.cake.out` holds exactly the one line `s VERIFIED UNSAT`; the binding of each verdict to its CNF and LRAT is the
JSON line that certify_cnf.sh writes after hashing both (`data/certify.jsonl`), as for every certification here.

## Files

- Proofs (kept, zstd -3): `~/research/data/resolve-sym-20261125/out/*.lrat.zst` (SHA-256 in `data/proofs_zst.sha256`;
  240 MB, 365 MB and 451 MB). The regenerated CNFs: `~/research/data/resolve-sym-20261125/cnf/`.
- `tools/regen.sh`, `tools/run_certify.sh`, `PLAN.md`; `data/` as listed above (CaDiCaL log tails included).

## What remains

- An independent re-run of these proofs (house rule: keep each proof until an independent check has re-run it).
- C4 and C5: Lean encoders (the owner's scope "302 + SAT results' encoders"); D2: nothing beyond this verdict.

## Resume

```bash
cd ~/research/data/resolve-sym-20261125 && bash regen.sh && bash run_certify.sh    # regenerate, then certify
```
