# VERIFY_RERUNS_1115EV: second-party cake_lpr re-runs of kept Δ proofs (track VB, 15 November 2026 evening)

**Verdict: CONFIRMED, 10 of 10 (19:03 KST).** For each of the ten kept proofs below, a fresh cake_lpr run by track VB
printed exactly one line, `s VERIFIED UNSAT`, and the CNF SHA-256, the SHA-256 of the decompressed LRAT stream and its
byte count are equal to the producer's recorded values. Label of each CNF's unsatisfiability: **CERTIFIED** (CaDiCaL
2.1.3 LRAT, `c Version 2.1.3` in all ten producer logs, accepted by cake_lpr; now by two parties).

- **New:** V1's lemma-free base(5,6,16) CNF `v1_base_m16.cnf` had no cake_lpr acceptance before (V1's runs at heap 250 and
  300 MB ran out of heap, so it was COMPUTED only). It is now **CERTIFIED** (heap 2000 MB, 29 s).
- **Second party:** ROOT(6) CNFs m = 7…14 (the main session's proofs) and T1's base(5,6,16) proof had only their
  producers' cake_lpr verdicts (C1, open items). Both now have an independent fresh run.

What this does not show: the meaning of each CNF (encoder soundness) is the producers' and earlier verifiers' work
(ROOT6_MAIN.md, VERIFY_ROOT6_M16_VACUOUS.md: V1 regenerated the ROOT(6) CNFs byte-identically and read the encoder).
This file checks the certificates only. Written by track VB (verifier), 19:00-19:10 KST. This file is new; no other file
of the record was edited.

## 1. What is re-run and why

C1's final issue list (`/home/jay/research/data/roadmap-20261115/pm1115/c1/ISSUES.md`, open items) and the handoff
STATUS20261115_1900 ("Resume", item 3) list these kept proofs as missing a second-party cake_lpr run
(paths relative to `/home/jay/research/data/roadmap-20261115/`):

| label | CNF | LRAT (zstd) | what rests on it |
|---|---|---|---|
| `root6_m7` … `root6_m14` | `round6/mainsession/root6/cnf/root6_m<m>.cnf` | `round6/mainsession/root6/cert/root6_m<m>.lrat.zst` | ROOT(6) decided for ≤ 14 points; LR(6) ≤ 14 |
| `t1_valid56_m16` | `pm1115/t1/base16/valid56_m16.cnf` | `pm1115/t1/base16/cert/valid56_m16.lrat.zst` | base(5,6,16): every "≥ 16 is vacuous" step |
| `v1_base_m16` | `pm1115/v1/root6-m16-vacuous/v1_base_m16.cnf` | `pm1115/v1/root6-m16-vacuous/cert/v1_base_m16.lrat.zst` | V1's own lemma-free base(5,6,16) encoding |

Recorded values compared against: `round6/mainsession/root6/cert/certify.jsonl`, `pm1115/t1/base16/cert/certify.jsonl`,
`pm1115/v1/root6-m16-vacuous/cert/certify.jsonl` (fields `cnf_sha256`, `lrat_sha256`, `lrat_bytes`).

## 2. Method

- Own wrapper `bin/recake_vb.sh` (work dir V = `/home/jay/research/data/roadmap-20261115/pm1115/vb/`): the LRAT is
  streamed `zstd -dc proof.zst | teehash.py FIFO` into `~/.local/bin/cake_lpr --CML_HEAP_SIZE=2000 CNF FIFO`; nothing is
  decompressed to disk. `bin/teehash.py` (own, 12 lines) computes the SHA-256 and the byte count of the whole
  decompressed stream while feeding the FIFO.
- Pass = cake_lpr's stdout is exactly one line and it is `s VERIFIED UNSAT` (`grep -cx` = 1 and `wc -l` = 1), the stream
  SHA-256 and byte count equal the recorded LRAT hash and size, the CNF SHA-256 equals the recorded CNF hash, and the
  stream writer exited 0. Comparison by `bin/compare_rerun.py` (own), output `rerun/compare1.txt`: "ALL PASS".
- Unit `esr-agv-vb-rerun1` (19:00:42-19:03:28): CPUQuota 100 %, MemoryMax 2700M, MemorySwapMax 0, nice 10,
  RuntimeMaxSec 3600; one cake_lpr at a time (`bin/runjobs.sh rerun/jobs1.txt`).
- Controls (19:00, foreground, heap 300): the wrapper on `root6_m7` gave the exact line and the recorded stream hash;
  the `root6_m9` proof against the `root6_m8` CNF and a 1,500-byte truncation of the `root6_m9` proof gave **no**
  verdict line (cake_lpr exit code 0 both times; messages "clause index unavailable: 2548" and "failed to parse line").
  So the exit code is no evidence and the grep is what decides, as the house rules say.

## 3. Results

All ten: stdout = the single line `s VERIFIED UNSAT`; CNF hash, stream hash and stream bytes = recorded (all "eq").

| label | CNF SHA-256 | LRAT stream SHA-256 | LRAT bytes | cake_lpr stdout | max RSS MB / wall s | start |
|---|---|---|---|---|---|---|
| `root6_m7` | `94ea6486b8b2cbeeaf622d8f64a17dcdb87bcfd537c6286451d88b4363a4a3e2` | `0af50c932d4430a225c06d7eb85ccd614f0c5758bb4c4e4ee5fe9c112c99d977` | 394 | 1 line, `s VERIFIED UNSAT` | 9 / 0.0 | 19:00:42 |
| `root6_m8` | `b9404ef00e0d6391a585a8db7012e73077e78a645571b264656eba652e25cc70` | `98106c08404a3dd67489f8948d5fd4414dfd97a80dcdda30ad09cf6a8318ee6e` | 496 | 1 line, `s VERIFIED UNSAT` | 9 / 0.0 | 19:00:42 |
| `root6_m9` | `2cc8e9d6d10cfba4fa339609f1939217e86e3308827db3641c7b3f3ab01b70d3` | `ea72c3f945ccff057a477802d133d954a7e0dc6e135883d1d63477b19ab4263b` | 2,471 | 1 line, `s VERIFIED UNSAT` | 11 / 0.0 | 19:00:42 |
| `root6_m10` | `fc89445d9187313969498bdf6d5ac962c580d61bbc80371c04f190b1634afc5e` | `011009062d1587ed44b2a5b433ca6717e5e080301b8b9470b4b27681f2474a5e` | 134,186 | 1 line, `s VERIFIED UNSAT` | 21 / 0.0 | 19:00:42 |
| `root6_m11` | `5649a71d91893d62156a1192450eeea5032968b101c76dabde0ddb7a29e82764` | `93cdc86cac5d4a1f1f78632602adda6ffe2a9f2232133e0a39d4d41e9ee85743` | 4,260,885 | 1 line, `s VERIFIED UNSAT` | 187 / 0.1 | 19:00:42 |
| `root6_m12` | `17a7fc7fe45739fb8cb9e48f97ad8c4eeec2ee740205832613f08a7cab47b1db` | `b028d0a413079163dc5e0df9479a69c76015f8b0bc3f2d7e956227577a1ec8f5` | 70,613,977 | 1 line, `s VERIFIED UNSAT` | 2,003 / 2.6 | 19:00:42 |
| `root6_m13` | `59046c71e984ea1a661ee690181529fb308e495945d55d38bcf7564dbaf892c2` | `921c6991a147a6941d688923647056aebcb7f3cc581466591574c0eb4b59cc25` | 547,264,401 | 1 line, `s VERIFIED UNSAT` | 2,005 / 15.2 | 19:00:45 |
| `root6_m14` | `242a448eb88dff48a0ad8fa3132ede1d5c7b3109a3103a3eb516acf62ca2df0e` | `7ee18f7598f52a9999ecb48adb300f44bba08dbb25e7afeacf4b341f21e9b130` | 2,945,935,220 | 1 line, `s VERIFIED UNSAT` | 2,005 / 86.8 | 19:01:01 |
| `t1_valid56_m16` | `1a556b6e800dd06e86c1ef5bdc39f520d59b9d045a42b097018b0de8f0abff6c` | `61337761006cd1410261fc653f3a8bf9a8aad6ff2135e260795cbb046af6a5a7` | 953,140,079 | 1 line, `s VERIFIED UNSAT` | 2,005 / 30.7 | 19:02:28 |
| `v1_base_m16` | `3e67b59a288e11e618fbb613cc6f99bb02a48dbb8b05fae22f431a8eeaf78381` | `e8e76e6c813a546fe32a8da6368c87da61a80ba2eac8a2e6588991487a1eb86f` | 904,430,025 | 1 line, `s VERIFIED UNSAT` | 2,005 / 29.4 | 19:02:59 |

Notes:
- V1's `certify.jsonl` records the verdict "REJECTED or incomplete" for `v1_base_m16` only because cake_lpr ran out of
  heap at 250/300 MB; the proof file is the same (stream hash and bytes equal its `lrat_sha256`/`lrat_bytes`; the
  `.zst` hash `652ff485…` equals V1's `SHA256SUMS.v1`). With heap 2000 MB it is accepted.
- cake_lpr's resident set is about the heap (2.0 GB) for every LRAT above 70 MB, independent of the proof size.
- SHA-256 of the kept `.zst` files (for later re-runs): `rerun/zst_sha256.txt`.

## 4. Consequences (labels unchanged where they were already CERTIFIED)

- ROOT(6) for 7 ≤ m ≤ 14 (CNF level): CERTIFIED, now re-run by a second party. The statements that rest on these CNFs
  (ROOT(6) decided; LR(6) ≤ 14 via ROOT(6)) keep their labels; their remaining dependence is on the encoder argument.
- base(5,6,16) UNSAT: CERTIFIED by two independent encodings, T1's `valid56_m16.cnf` (re-run here) and V1's lemma-free
  `v1_base_m16.cnf` (accepted for the first time here). The DELTA2N proof of base(5,6,16) was deleted earlier, so these
  two kept proofs are the evidence for "≥ 16 points is vacuous".

## 5. Files and hashes (V = `/home/jay/research/data/roadmap-20261115/pm1115/vb/`)

| file | SHA-256 |
|---|---|
| `bin/recake_vb.sh` | `3b4de010c019650af38be8af63b60e1c98d6055adbfe6f6f6474124b0193e2eb` |
| `bin/teehash.py` | `c3be2b96c71e930ac2dda759749c9f9b46c02c08221b33d161c9332573509118` |
| `bin/runjobs.sh` | `c6c507ed957fbb7b207bb5dc2703d04d619759221e7e1aad36c395e9a9ec4fc7` |
| `bin/compare_rerun.py` | `6e1fb95cf60ddddd41a6ce669db9dbcee59563797c1b1ebf821d3b3a4c30616f` |
| `rerun/jobs1.txt` | `53d29e0e03b8e066195864ce6b7589786adb1d6e4dd5c7b7775fc5c940c91dfa` |
| `rerun/rerun.jsonl` (10 lines) | `022acf84925b4a4218bcffbba8df6b310e1f6a3edbb21ed28db065f6f5ca3c83` |

Per label: `rerun/<label>.cake.out` (all ten byte-identical, SHA-256 `c680d3bd…`, the 17 bytes `s VERIFIED UNSAT\n`),
`rerun/<label>.cake.err` (max RSS and wall time), `rerun/<label>.stream` (stream hash and bytes). Controls in
`logs/selftest/`. No proof was produced, moved or deleted.

## 6. What remains

- Nothing for these ten proofs.
- T1's LRR(7) m = 15 proof (23.7 GB LRAT) has one cake_lpr acceptance (main session, heap 4,500 MB, 19:04); a
  second-party run needs a heap of about 4.5 GB, above VB's 2,000 MB cap (VERIFY_LRR7_M15.md). Not done. The DELTA2N proofs of strong (5,8) at 15 (CB(8) at 15) and of base(5,6,16) were deleted
  earlier and can only be re-solved (not done here).

## 7. Resume

```bash
V=/home/jay/research/data/roadmap-20261115/pm1115/vb
systemd-run --user --unit=esr-agv-vb-rerun1 -p CPUQuota=100% -p MemoryMax=2700M -p MemorySwapMax=0 -p RuntimeMaxSec=3600 \
  --nice=10 --working-directory=$V /bin/bash $V/bin/runjobs.sh $V/rerun/jobs1.txt $V/rerun
python3 -I $V/bin/compare_rerun.py $V/rerun/rerun.jsonl
```

## 8. Side checks (21:10 KST): two of C1's "unfiled EXACT items"

Done with VB's own code while verifying claims d1-c1six and lp0-7-real-2ext (exact integer orientations from the
coordinates; exhaustive subset enumeration):

- **T1's real 15-point ROOT(6) counterexamples** (`pm1115/t1/root6_real15.json` and the 21 files
  `pm1115/t1/real/m15_it*_real.json`): 22 files, **21 distinct order types** (VB's canonical form up to relabelling and
  reflection; `root6_real15.json` has the order type of `m15_it8_real.json`, the model it realizes). Every one is
  (5,6)-valid, its rightmost point r ends a 4-cap, and r lies in no weak Δ (0 of the 2^14 subsets A of S − r give a weak
  Δ A + r). **EXACT**: so the 20 further sets that C1 lists as unfiled are real ROOT(6) counterexamples, as T1 said.
  (Code and output: `vb/claims/d1-c1six/control.py`, `control.out`.)
- **R7's `pm1115/r7/div17/real/m17_it3_s1.json`** (17 points): (5,7)-valid, r ends a 4-cap, r lies in no weak Δ (0 of the
  2^16 subsets). **EXACT**: a real 17-point ROOT(7) counterexample. (Code: `vb/claims/lp0-7-real-2ext/vb_lp0.py`, part A;
  the same holds for T1's m17_it4/5/6_real and R7's root7_real17.)
- Not checked: V2's CONJ-TS′(6) at 14.
