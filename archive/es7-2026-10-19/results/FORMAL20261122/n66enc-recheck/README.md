# n66enc-recheck: byte identity of the N66 encoder with the frozen exe (22 Nov 2026)

Item `n66enc-recheck`, units `esr-ag-n66r-<job>` (1 thread, MemoryMax 3000M). Work directory (the only place this
agent writes): `/home/jay/research/data/formalize-20261122/n66enc-recheck`. No git writes, no Lean builds, nothing
written outside this directory.

## 1. Headline

**22 Nov 17:12 KST. All checks were run with the frozen exe `98d121ba…` only. EAGER: MATCH. FULL for leaf 131
(hhhhhh, 664,235,145 bytes): MATCH. TRIM: MATCH for 132/132 leaves. The leaf map: MATCH. Both negative controls and
the coreutils cross-check pass. No mismatch anywhere. Label: COMPUTED** (deterministic program runs, compared with
files and recorded hashes).

This replaces, for the frozen exe, the worker's M1(a) EAGER_MATCH and M1(b) FULL_MATCH, which the review found had
been computed on a superseded build (`9b818289…`).

Extension (not required): FULL for the other 131 leaves. 27/27 MATCH at 17:12:53 (leaves 0–26). It continues autonomously in unit
`esr-ag-n66r-full2`, slowed by the heat gate: other agents' load holds Tctl at 85–87.5 C. For the current count see
`out/status_fullall.json`.

## 2. Statement checked

The N66 encoder review (`../n66enc/review/VERIFY_n66-encoder_fidelity.md` §2, M1) found that the worker's
EAGER_MATCH and FULL_MATCH were computed on an exe built before the 07:01 link (`full_check.log`: exe `9b818289…`).
The frozen exe is `../n66enc/build/bin/n66print`, SHA-256
`98d121bad04264221de66e583db0df08f4431d1093b4b7a05114316accccaa46`; the M9 summary records the same hash. This
recheck uses that exe only:

- **(a) EAGER:** `n66print eager` = lines 2 .. 1+E of the generator's `hhhhhh/it1/cert.cnf`, where E = 1,489,581
  (layout.json `eager` = [1, 1489581]).
- **(b) FULL:** `n66print full 131 ACT ROWS` = the whole `hhhhhh/it1/cert.cnf`, and its SHA-256 = the recorded
  `full_cnf_sha256` `f9620834…`.
- **(c) TRIM:** `n66print trim i desc/i.txt` = `trim.cnf` of leaf i, and its SHA-256 = the recorded
  `trim_cnf_sha256`, for all 132 leaves.
- **Extension:** (b) for the other 131 leaves. All 132 cert.cnf files are still on disk.

## 3. Model and scope

- A MATCH shows that the frozen exe, fed the same inputs, prints exactly the bytes the Python generator
  (p2_write.py) or the certification pipeline wrote on 15 Nov.
- The `full` mode is a control, not on the trust path of `N66Geo.n66_bound_55_of_cubes`. The theorem needs only
  the trims (trust item E1, review §2).
- cake_lpr was not re-run here, so E2 stays as in the review.
- The descriptor files `../n66enc/desc/*.txt` are untrusted inputs. They can only cause a false MISMATCH, never a
  false MATCH; their SHA-256 values are recorded per leaf.
- The FULL inputs (activated quadruples, rows) are runtime data, as in the worker's control.
- Nothing here changes a label of the N66 record. The encoder theorem stays "Lean-checked modulo `CubesUnsat132`
  and `RowsValid R0`".

## 4. Method

**Driver.** `tools/recheck.py` is this agent's own code; none of the worker's or reviewer's scripts were run.

- The frozen exe is copied to `bin/n66print`.
- The copy is hashed before every exe start. Unless it equals the frozen hash, the run aborts.
- The original is hashed at the start and end of stage 1.

**Comparison.**

- The driver spawns the exe and streams its stdout; the output is never stored.
- The output is compared byte for byte with the reference file while both are hashed (Python hashlib).
- **MATCH** requires all of the following:
  - exit 0 and nonempty output;
  - both streams end at the same byte (for EAGER: the output is the byte segment after the header and has exactly
    E lines);
  - printed SHA-256 = fresh SHA-256 of the reference = every recorded hash, each checked against `^[0-9a-f]{64}$`.
- FULL also requires:
  - stderr exactly `leaf i clauses C act A rows R bad 0`, with C, A and R from layout.json;
  - byte count = layout.json `cnf_bytes`.

**Recorded hashes** come only from the campaign files, which were last modified on 18 Nov 04:28 and so predate
today:

- FULL: `cert.json`, `campaign_status.json` and `layout.json`;
- TRIM: `campaign_status.json`, `cert.json`, `verify.json` and the record's `STATUS_campaign.md`.

Nothing is taken from `../n66enc/logs` or `review/`.

**FULL inputs.** The driver's own `mkctl` step (a child process) extracts them:

- the activated quadruples, in file order, from the state file named in layout.json;
- the rows from layout.json `row_list`, which is p2_write.py's clause order.

For hhhhhh both files are byte-identical to the worker's `ctl/act_hhhhhh.txt` and `ctl/rows1832.txt`.

**Leaf map.** `n66print leaves` must give, for every leaf i, the campaign `lits` of cube `leaf_order.txt[i]`, and
`leaf_order.txt` must be a permutation of the 132 certified cubes. The FULL and TRIM pieces rely on this map.

**Gate.** Before every exe start the driver checks three things: YIELD is absent, Tctl < 86 C, and ag-track anon
+ 2400 MB ≤ 8000 MB. It waits, polling every 60 s; YIELD pauses it without limit, heat or memory for up to 45 min.

## 5. Results

### Stage 1 (unit `esr-ag-n66r-s1`, 16:39:54–16:40:13, `out/stage1.jsonl`, `out/status_stage1.json`)

| piece | result | details |
|---|---|---|
| exe | frozen | copy and original `98d121ba…` at start and end |
| leaves | **MATCH** | 132/132 leaves = campaign `lits`; `leaf_order.txt` is a permutation of the 132 certified cubes |
| eager | **MATCH** | 1,489,581 lines and 75,331,749 bytes = lines 2..1,489,582 of `hhhhhh/it1/cert.cnf`; SHA-256 `27b6b91009e6b782d051dba0bedfbdecd5e309acb79de9f2182dcd5f74007ff4` (printed = segment) |
| full:131 (hhhhhh) | **MATCH** | 664,235,145 bytes and 9,436,589 lines, byte-equal to `cert.cnf`; printed hash = fresh file hash = cert.json = campaign_status.json = layout.json = `f9620834edd34b727d63d17ccf455629af64b78df49679b44c0f017df29bf82c`; stderr `leaf 131 clauses 9436588 act 660810 rows 15648 bad 0` |

### Stage 2: trims (unit `esr-ag-n66r-trims`, 16:41:10–16:56:46, `out/trims.jsonl`, `out/trims.tsv`, `out/status_trims.json`)

**132/132 MATCH.** For every leaf i:

- the exe exited 0;
- the printed text is byte-equal to `<certdir>/trim.cnf`;
- printed SHA-256 = fresh hash of `trim.cnf` = campaign_status.json = cert.json = verify.json = `STATUS_campaign.md`;
- the exe hash was the frozen one before the run.

Further facts:

- **125 distinct texts.** The 8 leaves refuted by unit propagation (93, 96, 104, 106, 115, 117, 125, 127) share one
  112-byte text. The 132 texts total 1,183,383,419 bytes.
- **Clause counts.** The count on the exe's stderr equals the campaign `trim_cnf_clauses` for 132/132 leaves.
- **Verdict context** (read from the files, not re-run). For 132/132 certdirs, `cake.out` has the exact line
  `s VERIFIED UNSAT`, and the ALL_OK flags of cert.json and verify.json are set.
- **Consistency only, not evidence.** The (leaf, hash) pairs equal the reviewer's
  `review/trim_sha256_coreutils.tsv`.

### Extension: FULL for the other 131 leaves (`out/fullall.jsonl`, `out/status_fullall.json`, `logs/fullall.log`)

**Pre-screen.** Each leaf is pre-screened; a leaf that fails is OUT_OF_SCOPE, not a mismatch.

- layout.json `L`, `sb_pairs`, `vars` and `W` must equal hhhhhh's, because the exe hard-wires the budget-14
  counter, the 27 SB pairs and `nvHeader`.
- layout `cube` must equal the campaign `lits`.
- The state file's `activated` count, `cube`, `sb_pairs` and `L` must equal layout.json.

**Inputs.** `mkctl` re-extracts the inputs for each leaf and deletes them after the run; their SHA-256 values are
in the record.

- So far every leaf's act and rows files are byte-identical to hhhhhh's (`071ccaf1…`, `3f629bf1…`).
- So the leaves differ only in their cube units and in the header's clause count, and this extension mainly tests
  each leaf's cube units.

**Runs.**

- Unit `esr-ag-n66r-full` (16:57:32–17:06:34) checked full:0–4: 5/5 MATCH.
  - This agent stopped it during a gate wait, so that the coreutils cross-check could run with only one exe
    alive.
  - It resumed as `esr-ag-n66r-full2` (from 17:08:25, RuntimeMaxSec 4 h), which skips finished leaves.
- At 17:12:53, full:0–26 gave **27/27 MATCH**, with no OUT_OF_SCOPE so far (exe max RSS 2,369,132 KiB).

### Memory (MemoryMax 3000M = 3000 MiB; 80 % = 2400 MiB = 2,457,600 KiB)

| run | exe child max RSS (wait4) |
|---|---|
| leaves | 2,311,432 KiB |
| eager | 2,311,484 KiB |
| full 131 | 2,368,720 KiB (77.1 %) |
| trims (max of 132) | 2,407,652 KiB = 2,351 MiB (**78.4 %**, 49 MiB under the 80 % line) |
| extension (max so far, 27 leaves) | 2,369,132 KiB |

- Those figures are for the exe alone. The unit also holds the driver.
- One sample during full 131 showed unit anon 2,334 MiB (77.8 %), about 21 MiB above the exe's RSS.
- At the trim peak the unit's anon was therefore about 2,372 MiB (79.1 %, about 28 MiB under the line). It was not
  sampled at that moment.
- cgroup `memory.peak` was 3,147,825,152 bytes; that figure **includes page cache** from the files read. The guard
  set memory.high = 3000M, so page cache is reclaimed there.
- The guard log (`~/research/data/memguard-20261119.log`) has only `LIFT` lines for the `n66r` units and no `STOP`.
  There is no `MEMGUARD_STOPPED_*` file here.
- The heat gate paused the trims 9 times at Tctl 86.0–87.0 C, and the run resumed by itself.

## 6. Controls

- **Selftest** (`recheck.py selftest`, run at the start of stage 1): 14 synthetic cases give the expected
  verdicts. They cover equal streams, one byte changed, a shorter and a longer output, body prefix, a 9 MB
  multi-chunk stream, empty output, a nonzero exit, a missing record, and the extra-condition flag.
- **negfull:131: CONTROL_OK.** With the last activated quadruple dropped, the exe exits 0 with `bad 0`, but the
  output differs (first at byte 19, in the header). Its SHA-256 `b694e6a4…` ≠ `f9620834…`.
- **negtrim:131: CONTROL_OK.** With descriptor line 1 changed from `E 15` to `E 16`, the exe exits 0 with a
  different text (first difference at byte 20, line 2). Its SHA-256 `7b4e6eb2…` ≠ `da037243…`.
- **Coreutils cross-check** (unit `esr-ag-n66r-cu`, 17:07:49–17:08:16, `tools/cu_check.sh`, `logs/cu_check.log`).
  It is independent of the Python comparator, and it checks the frozen exe hash first.
  - EAGER: `n66print eager | sha256sum` = `tail -n +2 cert.cnf | head -n 1489581 | sha256sum` = `27b6b910…`, exit
    0. `cmp` reports EQUAL.
  - FULL: `n66print full 131 ctl/hhhhhh/act.txt ctl/hhhhhh/rows.txt | sha256sum` = `sha256sum cert.cnf` =
    `f9620834…`, exit 0. `cmp` reports EQUAL.
  - The `tail: Broken pipe` lines in the log come from `head` closing the pipe early.

## 7. Files and hashes

| file | SHA-256 |
|---|---|
| `bin/n66print` (copy of the frozen exe) | `98d121bad04264221de66e583db0df08f4431d1093b4b7a05114316accccaa46` |
| `tools/recheck.py` | `b3f60708db1a294f5c71f12b0ffb66b510e5d6926d830a8ace59a4c37e879124` |
| `tools/cu_check.sh` | `10a2bc6d148286ad8270ccc7f75d18bf0859b118211c9e93138e4e713e7174d1` |
| `out/stage1.jsonl` | `79798fdd80531e8713bf441ad45315b8bc7287e444ce93c98e0bc63f600111c1` |
| `out/trims.jsonl` (per leaf: desc SHA-256, all recorded hashes, printed hash, RSS) | `c97edf19915564715cad68c111b532e8bfca7338dc9198542712926ab223ffba` |
| `out/trims.tsv` | `d1c0211ce3775f7ed0c082d44f69a0cf2a7f225a04b1f040c5ae9f82a9ad695d` |
| `logs/cu_check.log` | `2aa0f4e21f888affed337d2215e9b2db6111cad1329879f97e53bd53a5f11411` |
| `ctl/hhhhhh/act.txt` (= worker `ctl/act_hhhhhh.txt`) | `071ccaf177e513903404ae0702974d1f7f060ad9f317717bccf897362f647f29` |
| `ctl/hhhhhh/rows.txt` (= worker `ctl/rows1832.txt`) | `3f629bf104b1e11cb07126c0934cba56ae9ae7d9fe550699183c2e58d852289f` |
| input `n66-20261113/p2/c14/hhhhhh/it1/cert.cnf` | `f9620834edd34b727d63d17ccf455629af64b78df49679b44c0f017df29bf82c` |
| input `…/hhhhhh/it1/layout.json` | `19b7de9678277614ed6aab07647b717577181a47621d3613c645469687292ff6` |
| input `…/hhhhhh/it1/cert.json` | `ab7836694f4c59367260af00dd50a8007eab7d530a1c441acdd6ffd42b3faf59` |
| input `…/p2/c14/campaign_status.json` (unchanged at 17:11; mtime 18 Nov 04:28) | `3ec0bc50c2d9d54084ae58517fd2ee7ec0bd823d90d2183aa862ff3cc9ffb1c9` |
| input `…/p2/c14/hhhhhh.json` (state file) | `7cb2e17c57857f7b73e6e2678a4b4a7881ace9a0e83653f7e10de1bc2f0a85de` |
| input `N66N20261113/cubes20261115/STATUS_campaign.md` (mtime 18 Nov 04:28) | `61570bbe8a49fac41f9028d612843a8f48ad32fdc3278c9c9f576e81ac001a0d` |
| input `../n66enc/tools/leaf_order.txt` | `3ad57b870d356f2c5fe9c8fc941b2f42785f4175eff6612e98834fb249780a69` |

`out/fullall.jsonl`, `out/status_fullall.json` and `logs/fullall.log` are still growing, so no hashes are given for
them.

## 8. What remains

- **The FULL extension for leaves 27–130** (unit `esr-ag-n66r-full2`, running).
  - To check it is finished: `cat out/status_fullall.json` should show `pieces` 131 and only MATCH or
    OUT_OF_SCOPE verdicts; `grep -E 'MISMATCH|OUT_OF_SCOPE' logs/fullall.log` lists any exceptions.
  - It can end early, by RuntimeMaxSec or because the gate gave up after 45 min at Tctl ≥ 86 C. Then resume with
    the `fullall` line of §9 under a new unit name.
- **`../n66enc/README.md` and `DESIGN.md`** still state M1(a)/(b) without the caveat that they were computed on the
  old exe. This agent may not edit them. Point to this record instead.
- **Not done here:** cake_lpr was not re-run (E2); the descriptors were not regenerated.

## 9. Resume / re-run

```bash
cd /home/jay/research/data/formalize-20261122/n66enc-recheck
U="-p CPUQuota=100% -p MemoryMax=3000M -p MemorySwapMax=0 --nice=10 --working-directory=$PWD"
systemd-run --user --unit=esr-ag-n66r-<new name> $U -p RuntimeMaxSec=1800  /usr/bin/python3 $PWD/tools/recheck.py stage1
systemd-run --user --unit=esr-ag-n66r-<new name> $U -p RuntimeMaxSec=3600  /usr/bin/python3 $PWD/tools/recheck.py trims
systemd-run --user --unit=esr-ag-n66r-<new name> $U -p RuntimeMaxSec=14400 /usr/bin/python3 $PWD/tools/recheck.py fullall
systemd-run --user --unit=esr-ag-n66r-<new name> $U -p RuntimeMaxSec=900   /bin/bash $PWD/tools/cu_check.sh
```

- Each stage skips the pieces already in `out/<stage>.jsonl`. To re-run a stage from scratch, move that file away
  first.
- Check the start gates first: no YIELD file, and Tctl < 86 C.
