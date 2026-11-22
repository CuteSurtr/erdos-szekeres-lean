# VERIFY n66enc-recheck: independent review (rebuild + soundness)

Reviewer slot rv4, 22 Nov 2026, 17:14–18:12 KST. The review used only its own code: `tools/prep.py`, `tools/run.sh`,
`tools/post.py`, `tools/driver.sh` and `tools/launch.sh`. The worker's `recheck.py` and `cu_check.sh` were read but
never run. All compute ran in unit `esr-ag-rv4-n66v1` (1 thread, MemoryMax 3000M, MemorySwapMax 0, nice 10,
RuntimeMaxSec 3 h), started at 17:30:12 once `cpu_free.sh` showed a free thread. Files were written only in this
directory. There were no git writes and no Lean builds.

## Verdict

**Every byte-identity check of the item holds with the frozen exe `98d121ba…aa46`.** This review re-ran each check
with its own driver: leaf map, EAGER, FULL for leaf 131, the 132 trims, both negative controls, and FULL for leaves
0–26 (plus the rest of the extension, §5).

- There is no mismatch anywhere.
- Every printed SHA-256 also equals the worker's recorded value.

All eight claims are confirmed. Two need wording fixes:

- the run count in frozen-exe-identity is wrong;
- in memory-measured, one figure is an estimate.

Label: **COMPUTED** (deterministic program runs compared with files and recorded hashes). That label holds for every
claim except the single estimated memory figure (§3.7). No claim rests on a cake_lpr proof, so no cake_lpr re-run
was due. E2 stays as in the encoder review.

| key | verdict | basis (own runs unless stated) |
|---|---|---|
| frozen-exe-identity | **confirmed** (fix the count) | 3 copies hash to `98d121ba…`, the same as M9; all 268 worker records carry it; this review checked it before each of its own runs |
| leaf-map | **confirmed** | `n66print leaves` = campaign `lits` for 132/132 leaves; `leaf_order.txt` is a permutation of the 132 certified cubes |
| eager-match-frozen | **confirmed** | rc 0; 1,489,581 lines and 75,331,749 bytes; equal under `cmp` to bytes [22, 75,331,771) of `cert.cnf`; SHA-256 `27b6b910…` |
| full131-match-frozen | **confirmed** | rc 0; stderr exact; `cmp` equal; SHA-256 = 2 fresh hashes = 3 records; inputs rebuilt independently are byte-identical |
| trims-132-match-frozen | **confirmed** | 132/132: rc 0; `cmp` equal; SHA-256 = fresh hash = 4 records each; 125 distinct texts; 8 UP-refuted leaves share one text; total 1,183,383,419 bytes; clause counts equal |
| controls | **confirmed** | (2) and (3) reproduced, SHA-256 equal to the worker's; (1) checked by reading and the log only |
| memory-measured | **confirmed** (label one figure) | measured numbers match the records; own RSS measurements agree; no guard stop; the 79.1 % figure is an estimate |
| fullall-extension-partial | **confirmed** | own FULL 0–26: 27/27 MATCH; worker records: 27 MATCH at or before 17:12:53, and 131/131 at 17:34:08 |

## 1. What was re-derived, and how

- **`tools/prep.py`** (Python, run inside the unit, done before the first exe start) derives the expected values:
  - expected values for all 132 leaves:
    - trim hashes from all four sources, parsed independently: campaign_status.json, cert.json, verify.json, and
      the table of STATUS_campaign.md;
    - trim clause counts from three sources;
    - full hashes from cert.json, campaign_status.json and layout.json;
    - layout fields;
    - the state file's `activated` list and layout `row_list`, serialized and hashed per leaf.
  - **The FULL inputs for leaf 131, rebuilt independently.** `act.txt` is the state file's `activated` list in file
    order, written as `a b c d` lines. `rows.txt` is built from `mono/rows_1832.json` itself, as the supports with
    d = 1, sorted, which is p2_write.py's rule. It is not taken from layout `row_list`; this review checked that it
    equals `row_list`.
  - **The EAGER byte range.** Layout `eager` = [1, 1489581]. Reading the file gives a 22-byte header
    `p cnf 1647808 9436588\n` (equal to layout `vars` and `clauses`), followed by 75,331,749 bytes for the next
    1,489,581 lines. The segment's SHA-256 (hashlib) is `27b6b910…7ff4`.
  - The two negative-control inputs.
- **`tools/run.sh`** (bash and coreutils) runs one exe at a time. Before each start it checks the gate (YIELD absent,
  Tctl < 86 C, ag-track anon + 2400 MB ≤ 8000 MB) and that `sha256sum` of `bin/n66print` equals the frozen hash.
  - Each run is: `time -o … n66print ARGS | tee fifo1 fifo2 | { cmp OPTS - REF; cat >/dev/null; }`.
    - `fifo1` feeds `sha256sum` and `fifo2` feeds `wc -l -c`.
    - The `cat` drains the pipe, so the hash and counts always cover the whole output, even after a mismatch.
  - The exit code and maxrss come from GNU time.
  - The unit's anon + shmem is sampled every 0.2 s.
  - The fresh reference hash comes from coreutils `sha256sum REF`. For extension leaves this step is skipped: it is
    implied by `cmp` equality together with the printed hash.
- **`tools/post.py`** computes the verdict for each claim (`out/summary.json`).
- **Comparator selftest** (`selftest/`, fake exe, before the real runs). Each variant gave the expected `cmp` code,
  hash and counts:
  - equal;
  - one byte changed: `cmp` byte 12, and the hash is of the whole changed stream;
  - short; long;
  - eager-style segment equal;
  - over-long segment: `cmp -n` passes, and only the byte count catches it, which `post.py` checks;
  - exit 3: recorded as rc 3;
  - stdout capture.

## 2. Inputs (SHA-256, computed by this review)

| input | SHA-256 | equals the claim |
|---|---|---|
| `../n66enc/build/bin/n66print`, `../bin/n66print`, `bin/n66print` | `98d121bad04264221de66e583db0df08f4431d1093b4b7a05114316accccaa46` | yes, and = M9 summary `exe_sha256` |
| `p2/c14/campaign_status.json` | `3ec0bc50c2d9d54084ae58517fd2ee7ec0bd823d90d2183aa862ff3cc9ffb1c9` | yes |
| `../n66enc/tools/leaf_order.txt` | `3ad57b870d356f2c5fe9c8fc941b2f42785f4175eff6612e98834fb249780a69` | yes |
| `cubes20261115/STATUS_campaign.md` | `61570bbe8a49fac41f9028d612843a8f48ad32fdc3278c9c9f576e81ac001a0d` | yes |
| `hhhhhh/it1/cert.cnf` | `f9620834edd34b727d63d17ccf455629af64b78df49679b44c0f017df29bf82c` (hashlib and coreutils) | yes |
| `hhhhhh/it1/layout.json` | `19b7de9678277614ed6aab07647b717577181a47621d3613c645469687292ff6` | yes |
| `hhhhhh/it1/cert.json` | `ab7836694f4c59367260af00dd50a8007eab7d530a1c441acdd6ffd42b3faf59` | yes |
| `p2/c14/hhhhhh.json` (state) | `7cb2e17c57857f7b73e6e2678a4b4a7881ace9a0e83653f7e10de1bc2f0a85de` | yes |
| `mono/rows_1832.json` | `80bec1b4f3d6fa0aab34b35fb85f4d1c03866af98f225fe76b3c3082e6b61f33` | = Rows.lean comment |
| own `ctl/hhhhhh/act.txt` | `071ccaf177e513903404ae0702974d1f7f060ad9f317717bccf897362f647f29` | = worker `ctl/hhhhhh/act.txt` = encoder `ctl/act_hhhhhh.txt` |
| own `ctl/hhhhhh/rows.txt` | `3f629bf104b1e11cb07126c0934cba56ae9ae7d9fe550699183c2e58d852289f` | = worker `ctl/hhhhhh/rows.txt` = encoder `ctl/rows1832.txt` |
| worker artefacts: `out/stage1.jsonl`, `out/trims.jsonl`, `out/trims.tsv`, `logs/cu_check.log`, `tools/recheck.py` | `79798fdd…`, `c97edf19…`, `d1c0211c…`, `2aa0f4e2…`, `b3f60708…` | yes, all five |
| worker `out/fullall.jsonl`, `out/status_fullall.json`, `logs/fullall.log` (read after its unit ended, 17:34:08) | `a19efb8b117c5e366891df7ca23f27ad5155bd98c0cee736d5d516d1fd561be3`, `760107ac72afeba9933e64abbdb6ee521516ded04661866c9da528762b900cc5`, `e79191f623b50ad15de6f24304141000e74e512acebc30be40c3ec6613f65185` | (no claimed hash) |

## 3. Per claim

### 3.1 frozen-exe-identity: confirmed; the count needs a fix

- `sha256sum` gave `98d121ba…aa46` at 17:29 for the original, the worker's copy and this review's copy, and again at
  the start (17:31:30) and end of this review's run (`out/exe_hashes.tsv`). That hash equals `exe_sha256` in
  `../n66enc/logs/m9_hash_binding.tsv.summary.json`.
  - The build the encoder review flagged, `9b818289…`, appears in `../n66enc/logs/full_check.log`.
- **Worker records.** `stage1.jsonl` has 4 records, `trims.jsonl` 133 and `fullall.jsonl` 131: 268 in total.
  Every one has `exe_sha256` = the frozen hash. `status_stage1.json` has `exe_sha256_end` and
  `original_sha256_end` = frozen. The first line of `cu_check.log` shows the frozen hash.
  - By reading `recheck.py`: `exe_sha()` is called, and aborts on any other hash, before every spawn (lines 183,
    257, 277, 300 and 318) and at each stage's start and end.
  - `cu_check.sh` hashes the exe once, before its four runs, not before each one.
- **This review's runs.** All ran on `bin/n66print`, with its hash checked before each start (`runs.tsv` column 3).
- **Required fix.** The claim says "each of the 270 runs … (leaves, eager, full x28, 132 trims, 2 controls; plus 4
  runs in cu_check)", but:
  - that breakdown sums to 164, which was the state at 17:12:53;
  - the number 270 fits 4 + 133 + 129 + 4. That is fullall with 129 records, which held from 17:33:44 to
    17:33:56, plus the cu_check runs. So it looks like a later snapshot mixed with the earlier breakdown;
  - the final count is 268 records (4 + 133 + 131), plus the 4 cu_check runs under a single hash.
  - The claim should state 268 + 4 with the final breakdown: leaves, eager, full ×132, 132 trims, 2 controls.
- "Same hash at 17:12" for the original: this review cannot re-observe a past hash. It is consistent with the
  review's own hashes at 17:29 and 17:31.

### 3.2 leaf-map: confirmed

`n66print leaves` exited 0. It printed 132 lines (5,418 bytes, SHA-256 `e4d237cb…`, kept as `tmp/leaves/stdout`).
Line i is exactly `i` followed by `s:b` for the campaign `lits` of cube `leaf_order.txt[i]`, in campaign order,
for every i. The `leaf_order.txt` file has 132 distinct ids, and sorted it equals the sorted ids with status
`certified`, of which there are 132 (68 cubes have status `split`).

### 3.3 eager-match-frozen: confirmed

- `n66print eager` exited 0 with empty stderr.
- It printed 1,489,581 lines and 75,331,749 bytes. `cmp --ignore-initial=0:22 --bytes=75331749 - cert.cnf` found
  them equal, and the byte count equals the segment length exactly.
- The printed SHA-256 (coreutils) is `27b6b91009e6b782d051dba0bedfbdecd5e309acb79de9f2182dcd5f74007ff4`. That
  equals the hashlib hash of the segment, the claim, and the worker's record.
- The segment is lines 2..1,489,582, and it ends with a newline.
- **Nit, not blocking.** In `cu_check.sh`, the `rc=${PIPESTATUS[0]}` inside `echo "…$(X eager | sha256sum)…"`
  reports the parent shell's previous pipeline, not the exe's exit code. A bash test confirmed this. So the
  "rc=0" lines in `cu_check.log` say nothing about the exe's exit code. The exit codes are established by the
  worker's wait4 records and by this review's GNU time records, which show rc 0 for both runs.

### 3.4 full131-match-frozen: confirmed

`n66print full 131 ctl/hhhhhh/act.txt ctl/hhhhhh/rows.txt` (own inputs) gave:

- exit code 0;
- stderr exactly `leaf 131 clauses 9436588 act 660810 rows 15648 bad 0`, which matches layout `clauses`, the
  `activated` count and the length of `row_list`;
- 664,235,145 bytes, equal to layout `cnf_bytes` and to the file size from `stat`;
- 9,436,589 lines, which is `clauses` + 1;
- `cmp` equal with `cert.cnf`.

The printed SHA-256 equals all of the following: the coreutils fresh hash of the file, the hashlib fresh hash
(prep), and the recorded hashes in cert.json `full_cnf_sha256`, campaign_status.json `full_cnf_sha256` and
layout.json `cnf_sha256`. The value is `f9620834…bf82c`. The rebuilt inputs are byte-identical to the worker's and
the encoder's files (§2), and the rows come from `rows_1832.json` itself, not from layout.

### 3.5 trims-132-match-frozen: confirmed

For each leaf i, the frozen exe ran `trim i ../n66enc/desc/i.txt` (`out/runs.tsv` rows `trim:*`). All 132 leaves
gave:

- exit code 0;
- `cmp` equal with `<certdir>/trim.cnf`;
- printed SHA-256 = the coreutils fresh hash of `trim.cnf` = all four recorded values, each parsed by this review;
- byte count = the file size from `stat`;
- stderr `leaf i [cube] clauses N`, with the cube equal to the campaign `lits`, and N equal to the campaign's
  `trim_cnf_clauses`, cert.json `trim_cnf_clauses` and verify.json `clauses`;
- line count = N + 1.

Further facts:

- **Distinct texts.** There are 125.
- **The 8 leaves refuted by unit propagation.** Leaves 93, 96, 104, 106, 115, 117, 125 and 127 share the 112-byte
  text `06250f34…ab06`. These are exactly the leaves whose campaign entry has `up_refuted` set.
- **Total size.** The 132 texts total 1,183,383,419 bytes.
- **Agreement with the worker.** For each of the 132 leaves, the printed SHA-256 and byte count equal the worker's
  record.

### 3.6 controls: confirmed. Items (2) and (3) reproduced; item (1) checked by reading only.

- **(2) negfull:131.** This review built its own act file with the last quadruple dropped. Its SHA-256,
  `e5b3c4e6…`, equals the worker's. Running it gave:
  - exit code 0;
  - stderr `leaf 131 clauses 9436576 act 660809 rows 15648 bad 0`;
  - 664,234,239 bytes;
  - `cmp`: `differ: byte 20, line 1`. That is 1-based, so it is the worker's 0-based byte 19, inside the header's
    clause count;
  - printed SHA-256 `b694e6a4d5d0cd822d18acadcbf4c9b8ffe2914121711d0faf1034356099de31`. That equals the worker's
    record and differs from `f9620834…`.
- **(3) negtrim:131.** This review built its own descriptor with `E 15` changed to `E 16`. Its SHA-256,
  `510f8e4a…`, equals the worker's. Running it gave:
  - exit code 0;
  - 1,669,718 bytes;
  - `cmp`: `differ: byte 21, line 2`. That is 1-based, so it is the worker's 0-based byte 20;
  - printed SHA-256 `7b4e6eb2f79acbd783b5bbc3396681a486fdde23f082b36ceef1b229a6d59dda`. That equals the
    worker's record and differs from `da037243…`.
- **(1) The selftest.** Not run, because the lens forbids running the worker's scripts. Read from `recheck.py`
  lines 193–228, it has 14 checks:
  - 10 listed cases:
    - whole file: equal, one byte changed, shorter and longer;
    - body mode: prefix of 1 line, prefix of 2 lines, changed and longer;
    - 9 MB equal, and 9 MB with one byte changed;
  - and 4 further checks: the fresh whole-file hash, empty output, nonzero exit, and a missing record together with
    the extra-condition flag.
  - The checks match the claim's list. `logs/selftest.log` and `logs/stage1.log` say `selftest PASS (14 cases)`.
- **The worker's comparator logic, read.** The body mode requires the output to be a byte prefix of the body, with
  exactly E lines and a final newline. The whole mode detects both a shorter and a longer output. Both are sound.

### 3.7 memory-measured: confirmed, with one figure to be labelled an estimate

- **The worker's numbers, recomputed from its records:**
  - trims maximum 2,407,652 KiB (trim:45), which is 2,351.2 MiB or 78.37 % of 3000 MiB;
  - full 131: 2,368,720 KiB (77.11 %);
  - leaves 2,311,432 KiB and eager 2,311,484 KiB;
  - extension maximum: 2,369,132 KiB at or before 17:12:53, and 2,369,148 KiB at the end;
  - `status_trims.json` memory.peak 3,147,825,152 bytes, including page cache.
  - All match the claim.
- **This review's own measurements** of the same runs (GNU time maxrss):
  - trims maximum 2,407,524 KiB (78.37 %);
  - full 131: 2,368,868 KiB;
  - leaves 2,308,068 KiB and eager 2,308,508 KiB.
  - The largest sampled anon + shmem of the unit was 2,402,988 KiB (78.22 %), with a bash and coreutils driver.
- **No guard stop.** There is no `MEMGUARD_STOPPED_esr-ag-n66r-*` file in the worker's directory. The journal shows
  `esr-ag-n66r-s1`, `-trims`, `-cu` and `-full2` ending normally (with "Consumed …" lines). `esr-ag-n66r-full` ended
  with a plain stop at 17:07:41 and no kill lines, as the worker reported.
  - The guard log itself was **not** read, because the running `esr-memguard-1122d` writes it (hard rule 4). So
    "only LIFT lines" is checked by this other evidence, not by the log.
- **Required wording/label fix.** "At the trim peak the unit's anon … about 2,372 MiB (79.1 %)" is an estimate
  (2,351 + 21 MiB, arithmetic correct). Under §2 it is HEURISTIC, not COMPUTED. The claim does say "estimated, not
  sampled", so that is honest, but it should not sit under the COMPUTED label. The 2,334 MiB sample is a single past
  observation and cannot be re-observed. The review's own sample at full 131 was 2,312 MiB with a lighter driver,
  which is consistent.
- **Observation.** memory.peak, 3,147,825,152 bytes for the trims and 3,148,021,760 for fullall, lies 2.1–2.3 MB
  above 3000 MiB. This is possible because the guard lifts memory.max to `max` and sets memory.high = 3000M. It is
  page cache only. The guard's metric (anon + shmem + swap) stayed at about 2.35–2.4 GB. This is not an OOM risk,
  but it is worth knowing.

### 3.8 fullall-extension-partial: confirmed

- **This review's own FULL runs of leaves 0–26** gave 27/27 MATCH.
  - Each run used this review's own input files. For all 132 leaves, prep checked that the leaf's `activated` and
    `row_list` serialize to exactly hhhhhh's bytes. The leaves differ only in their cube units and in the header's
    clause count, which confirms the worker's remark.
  - Each run had: rc 0; stderr equal to `leaf i clauses C act 660810 rows 15648 bad 0`, with C from that leaf's
    layout; `cmp` equal with that leaf's `cert.cnf`; and printed SHA-256 equal to the three recorded values, which
    agree with each other.
  - Byte count = layout `cnf_bytes` = the file size from `stat`, and lines = C + 1.
- **The worker's records**, read only after `esr-ag-n66r-full2` ended at 17:34:08: 27 records timed at or before
  17:12:53, which are exactly leaves 0–26, all MATCH, each with the frozen hash. The final `status_fullall.json`
  shows pieces 131, MATCH 131, and no OUT_OF_SCOPE.
  - For every piece both ran, this review's printed SHA-256 and byte count equal the worker's.
- **Scope.** The prep pre-screen found all 132 leaves in scope: L, vars, W, SB pairs, cube = lits, activated count,
  and `cnf_bytes` = size.

## 4. Not checked / limits

- cake_lpr was not re-run. No claim here rests on a proof, so E2 is unchanged.
- The descriptors were not regenerated. A descriptor can only cause a false mismatch, never a false match.
- The guard log was not read (rule 4, see §3.7).
- The worker's selftest was not run (lens).

## 5. Extension tail (beyond the claims)

This review's unit finished at 18:07:45. It completed all 268 planned pieces. For every one, the exe SHA-256 was
checked before the start and equalled the frozen hash; the exe hash at the start and at the end is in
`out/exe_hashes.tsv`.

- **FULL for all 132 leaves.** Leaf 131 plus the extension 0–130: 132/132 MATCH. Every run had rc 0, `cmp` equal
  with the leaf's own `cert.cnf`, the printed SHA-256 equal to its three recorded values, and stderr equal to the
  layout values.
- **Agreement with the worker.** There are 267 pieces where both runs carry a printed hash: eager, full ×132,
  trim ×132, and the 2 controls. In all 267, this review's printed SHA-256 and byte count equal the worker's
  record.
  - The `leaves` piece has no printed hash in the worker's record. The worker compared it by parsing, and this
    review did the same.
- **Unit totals.** The unit's largest exe RSS during FULL was 2,369,328 KiB (77.13 %). Its cgroup memory.peak was
  3,147,902,976 bytes, including page cache, which is the same effect as in §3.7.
  - There is no MEMGUARD_STOPPED file in this directory.
  - The journal reports "Consumed 35min 36s CPU time over 37min 33s wall clock time".
- **This covers the worker's extension result.** The worker's final 131/131 is beyond its claim, and this review
  reproduced it.

## 6. Files (this directory)

`tools/prep.py` `330c600e…`, `tools/run.sh` `3237177b…`, `tools/post.py` `c4b41a02…`, `tools/driver.sh` `a756a1fa…`,
`tools/launch.sh` `da5d3429…`, `out/expected.json` `83d71724…`, `out/plan.tsv` `f8ba2937…`.

| file | SHA-256 |
|---|---|
| `out/runs.tsv` (one line per run: name, time, exe hash, rc, maxrss, wall, printed hash, lines, bytes, cmp code, cmp text, fresh ref hash, stderr, sampled anon, pipestatus, gate) | `464c376830dc81062cf5225ee0a16de533d29ed954c20d4165b1c792dac4db72` |
| `out/summary.json` (post.py) | `b052d198ab9b0c0ce5f620367493581d45bb73ac64515dc080cf32ea68e51280` |
| `out/exe_hashes.tsv` | `a2207d1e6267f11540db779975597d5bb67463ef65465c535bf21c1cf0072481` |
| `logs/run.log` | `cd5d443b7f94191aca327f7c21aae678d688f9beba24f0b1e6a1924b7914360c` |
| `tmp/leaves/stdout` | `e4d237cb991a96b74370926c017498102d2e3bd579d6f526914143cbb5e2e536` |

Other contents:

- `selftest/`: the comparator selftest (fake exe, plan, runs);
- `tmp/<piece>/`: the time, err, cmp, sha, wc and anon files of each run;
- `ctl/`: this review's FULL and control inputs (§2).

**Recipe for an independent re-check.**

1. `bash tools/launch.sh esr-ag-rv4-<new>` (or move `out/runs.tsv` away first to re-run everything).
2. `python3 -I tools/post.py`.

Single checks by hand:

- **EAGER:** `bin/n66print eager | cmp --ignore-initial=0:22 --bytes=75331749 - <cert.cnf>`. Expect EQUAL, plus
  `| wc -c` = 75,331,749.
- **FULL:** `bin/n66print full 131 ctl/hhhhhh/act.txt ctl/hhhhhh/rows.txt | cmp - <cert.cnf>`.
- **TRIM:** `bin/n66print trim i ../../n66enc/desc/i.txt | cmp - <certdir>/trim.cnf`.

Run each of these in a unit with MemoryMax ≥ 3000M; the exe's RSS is about 2.3–2.4 GB.
