# VERIFY_DELTA2N_RECERT1119: re-certification of the 15-point frontier of weak Conj(7) and weak Conj(8)

**Re-certification (main session, 19 Nov 2026, 16:05–16:31 KST).** It addresses SYNTHESIS (ROADMAP20261115) §2.2
item 3: "This is the conjecture's only computational support, and its LRATs were deleted before any re-run."

**Verdict: CONFIRMED.** Both 15-point weak cases are CERTIFIED again.
- The CNFs are byte-identical to the record's.
- The regenerated LRAT proofs are bit-identical to the deleted 13 Nov proofs: their SHA-256 equal `cnf_hashes.tsv`.
- cake_lpr printed `s VERIFIED UNSAT` exactly once each.

Work directory (not in Git): `/home/jay/research/data/delta-recert-20261119`.

## Method

1. **CNFs.** `eager_cert.py a n m weak --nocert --tl 1 [--keep] --out cnf` is the record's encoder, copied unchanged
   (SHA-256 `055ea8ab…`). The CNF hashes were compared with `data/cnf_hashes.tsv`.
2. **Certification.** `cad_stream_cert.sh CNF cert WALL HEAP` (SHA-256 `a85ae56d…`; T1118's streaming tool, unchanged):
   - CaDiCaL 2.1.3 writes the LRAT into a FIFO;
   - the stream is hashed (SHA-256) and compressed by zstd on the fly, so no raw proof touches the disk;
   - after exit 20, cake_lpr reads the decompressed proof through a FIFO, and that stream is hashed again;
   - only `s VERIFIED UNSAT` exactly once, with equal stream hashes, counts.
3. Units: `esr-dlt-n7m15`, `esr-dlt-n8` (CPUQuota 100 % each, MemoryMax 4.5 G, MemoryHigh 4 G).

## Results

| case | CNF SHA-256 (= record) | clauses | CaDiCaL | LRAT SHA-256 (stream = record of 13 Nov) | cake_lpr | stored proof |
|---|---|---|---|---|---|---|
| weak (5,7), m = 15 | `b53d6fb04f30282fdce933846fd0026cf4cb2d9d2490ae78989575b2853787b1` | 232,916 | UNSAT, 1,328 s | `10ed769ff449a10ef05696d6f3e5639bc0ab9e6fa125868bc6aaabe24cbfd004` | `s VERIFIED UNSAT` (1 line), 162 s | `cert/a5_n7_m15_weak.lrat.zst`, 1.25 GB (raw 5.93 GB) |
| weak (5,8), m = 15 | `228120eefd868a689c0de199d2a9cee55e190150353fcd8dcdd6c1a044207dbb` | 421,676 | UNSAT, 220 s | `05636cc8257ed7377b079b757f009e23f9e7b75e39945ac610ba37e7bb82e334` | `s VERIFIED UNSAT` (1 line), 14 s | `cert/a5_n8_m15_weak.lrat.zst`, 140 MB (raw 557 MB) |

The record's statements are again CERTIFIED: weak Conj(7) and weak Conj(8) have no counterexample with at most 15
points, for all signotopes and hence for all point sets.

## New frontier attempts (running at 16:31)

| case | CNF SHA-256 | clauses | unit | status |
|---|---|---|---|---|
| weak (5,8), m = 16 | `d6d340863685d92eb9fdcdc1a7a46b957a39b085af5190c0330adc90aa51f181` | 778,924 | `esr-dlt-n8` (wall limit 30,000 s) | running |
| weak (5,7), m = 16 | `8bbb72d50bb446dbc6ebe0e1f363668555ab28032d894677edc9f5d5b6f23411` | 398,544 | `esr-dlt-n7m16` (wall limit 28,800 s) | running |

A `s VERIFIED UNSAT` on either would extend the frontier to 16 points (new). A timeout decides nothing.

**Result (16:59): weak (5,8) at m = 16 is CERTIFIED.** CaDiCaL said UNSAT after 2,798 s. cake_lpr printed
`s VERIFIED UNSAT` exactly once in 178 s (heap 3,500 MB).
- LRAT SHA-256 `68c70856c1618ec85ab2151b484ba77ddc3b69462e52ddbaa51c65d5e11f8168` (= the stream hash).
- Kept as `cert/a5_n8_m16_weak.lrat.zst` (1.23 GB; SHA-256 `d05d5efe…`).

**New frontier: weak Conj(8) has no counterexample with at most 16 points**, for all signotopes and hence for all
point sets. Weak (5,7) at m = 16 is still running.

**Regeneration result (17:40): 356 of 356 "CERTIFIED, REPRODUCED".** Every other proof of this record was regenerated
with a stream SHA-256 equal to the 13 Nov record and accepted again by cake_lpr. With the two 15-point cases above,
all 358 certified proofs of DELTA2N are again on disk (zstd, `regen/cert/` and `cert/`), and none differs from the
deleted original.

## Regeneration of all other proofs of this record (started 16:48, unit `esr-dlt-regen`)

- **Tool.** `regen_delta.py` (SHA-256 `2b90dbf6…`). It covers every row of `cnf_hashes.tsv` with cake_lpr
  `s VERIFIED UNSAT` and a recorded LRAT hash: 358 rows, minus the two 15-point cases above, leaves 356.
  - The CNF is taken from the 13 Nov work directory if a file with the recorded SHA-256 exists. That holds for 355 of
    the 358; the other 3 are large strong-form CNFs, rebuilt by `eager_cert.py` with a hash check.
  - The proof is streamed through `cad_stream_cert.sh`. Proofs run smallest first; only the zstd copies are kept
    (`regen/cert/`).
  - Verdicts: "CERTIFIED, REPRODUCED" = cake_lpr `s VERIFIED UNSAT` exactly once, stream hash equal, and the proof
    SHA-256 equal to the 13 Nov record.
- **Progress at 16:50:** 330 of 356 done, all 330 "CERTIFIED, REPRODUCED", so far all proofs under 0.05 GB raw. The
  larger ones follow (largest 2.64 GB raw); results in `regen/results.jsonl`.

## Observation

The solver is deterministic. CaDiCaL 2.1.3 on the same CNF and options reproduced the deleted proofs bit for bit, six
days after the first run and under a different machine load. A proof whose hash is recorded can
therefore be regenerated and re-checked on demand. See `ES306N20261119/DISK_POLICY_PROPOSAL.md`.

## Next frontier: weak (5,8) at m = 17 (started 22:28)

- **CNF.** `eager_cert.py 5 8 17 weak --nocert --tl 1 --keep --out cnf`, the record's encoder, unchanged:
  24,888 variables, 1,386,080 clauses, SHA-256 `7d3ebaba5200114f41f20204b7b6800d1ee57b3dfb51e568431ecd224c807cb9`.
- **Control.** The same command at m = 16 reproduces the certified CNF's SHA-256 `d6d34086…`. The encoder is
  deterministic.
- **Run.** `cad_stream_cert.sh cnf/a5_n8_m17_weak.cnf cert 57600 6000` (unit `esr-dlt-n8m17`, 1 thread; CaDiCaL
  limit 16 h; cake_lpr heap 6,000 MB).
- Only `s VERIFIED UNSAT` exactly once, with equal stream hashes, would extend the frontier to 17 points. A timeout
  decides nothing.

**Result (20 Nov 00:30): weak (5,7) at m = 16 is undecided (no verdict).** CaDiCaL reached its 28,800 s limit
(exit 0 = limit) after 39,094,815 conflicts, peak RSS 682 MB; the unit ended with status 2 from the queue script.
- No claim follows. The weak Conj(7) frontier stays at 15 points (CERTIFIED above).
- The partial proof `cert/a5_n7_m16_weak.partial.lrat.zst` (14.9 GB) is **not a proof**. CaDiCaL cannot resume
  from it, and a re-run with the same options repeats the first 8 h bit for bit. Deleting it needs the owner's OK.
- For comparison, m = 15 → 16 took (5,8) from 220 s to 2,798 s (×12.7) but (5,7) from 1,328 s to more than
  28,800 s (more than ×21.7).

**Result (20 Nov 14:28): weak (5,8) at m = 17 is undecided (16 h limit).** CaDiCaL reached its 57,600 s limit
(`c UNKNOWN`, exit 0 = limit) after 31,639,152 conflicts and 56,996 s process time, peak RSS 1,188 MB; the unit ended
with status 2 from the queue script.
- No claim follows. The weak Conj(8) frontier stays at 16 points (CERTIFIED above).
- The partial proof `cert/a5_n8_m17_weak.partial.lrat.zst` (13.7 GB; stream SHA-256 `31655b67…`) is **not a proof**.
  It is outside the level-15 cube disk policy; deleting it needs the owner's OK (open, with the m = 16 partial above).
- m = 16 → 17 for (5,8): from 2,798 s to more than 57,600 s (more than ×20.6).
