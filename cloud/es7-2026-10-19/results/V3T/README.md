# V3-T: review, test and first use of the verify/v3 acceptance scripts (mirror sub-case (ii))

## Failures: none
No leaf verdict was SAT, REJECTED or TIMEOUT, and no cover verdict was NOT_COVERED. All 2,655
records in the four `check_*.jsonl` files have the verdict VERIFIED, and
`scripts/aggregate.py` found no problem other than leaves that were not yet checked (time limit).

## Setup
- Branch `es7-cloud`. One VM with 4 cores and 15 GB RAM (`env.txt`). Run from 07:54 to 10:50 UTC.
- Tools (`tools.txt`), built from source:
  - CaDiCaL 3.0.1, commit c60730422e75, installed as /opt/bin/cadical;
  - cake_lpr, commit a36874a8b750 (`make cake_lpr`), installed as /opt/bin/cake_lpr. Its
    `cake_lpr.S` sha256 is 2f3af32d…b7d4a, and the bundled example prints `s VERIFIED UNSAT`.
- I regenerated F (`gen_etv.py 33 7 7 7 --mirror`, then `mirgen.py --interior --yflip-unit`). Its
  sha256 is 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d, which matches.
  Header: `p cnf 47002 515121`.
- verify/v3 versions:
  - My fixes are a3e5d17 (Fix 1) and f3b07a7 (Fix 2).
  - Other sessions later committed 7c6d70c (new helper `v3_jsonl_leaves.py`) and bdf319c (opt-in
    `--skip-leaves` and `--skip-covers` flags). The newest verify/v3 commit is bdf319c.
  - Runs sub1 to sub3 used v3_check.py at f3b07a7. Run sub4 used bdf319c without the new flags; its
    behaviour is the same as f3b07a7.
  - v3_manifest.py has not changed since 8f98073.
  - I did not review `v3_jsonl_leaves.py`. None of my runs used it.

## Review (`REVIEW.md`)
I found two BUGs. Each could let something unproved be accepted, and I fixed each with one commit
(`verify/v3/CHANGES.md`).
- **BUG-1: shared work paths.**
  - `WORK/leaf-<idx>` and `WORK/cover-<case>` were unique only within one process.
  - Two processes that share `--work` and have overlapping idx can overwrite each other's CNF and
    proof between the CaDiCaL step and the cake_lpr step. Renumbered sub-manifests do overlap.
  - When that happens, one leaf's VERIFIED verdict is recorded for another leaf.
  - Fix: one `tempfile.mkdtemp` directory per job.
- **BUG-2: resume and output keyed by idx alone.**
  - On resume, a record was reused if `(kind, idx)` matched. So reusing OUT with a different
    manifest kept the verdict that belonged to a different leaf.
  - A cover record made for an older leaf set was also kept.
  - Leaf records did not contain their literals, so records from different machines could only
    be joined by idx.
  - Fix: leaf records carry `lits` and cover records carry `leaves_sha256`, and resume matches on
    them. The acceptance join (`scripts/aggregate.py`) works by (case, lits) and also recomputes
    each leaf's CNF sha256.

I found seven RISKs. None of them can cause a wrong acceptance:
- v3_check does not validate the manifest's literals. A literal 0 ends up REJECTED, but only
  because the clause count no longer matches.
- cake_lpr runs with no timeout.
- Transient failures (OOM, a full disk) are recorded as REJECTED and are never retried.
- When a job raises an exception, its work directory is left behind.
- Memory and disk use with 4 large proofs at once.
- The manifest only scans directories exactly 2 levels below the wave directory.
- RISK-7, which happened during this run: OUT was a tracked file and `git pull --autostash`
  replaced it. The running process kept writing to the deleted inode. I recovered the records from
  `/proc`, then resumed with OUT outside the repository. Records can be lost this way; none can be
  added.

The NOTEs record what I checked and found sound:
- the case cube is pinned by its sha;
- F is pinned by its sha;
- the verdict comes from the exact cake_lpr line;
- the header counts are correct;
- the shortcuts that skip a proof are sound;
- the parse is strict;
- dirname/sha case assignment was checked against all 450 names;
- merge and dedup work.

## Mutation tests (`mutations.log`): all ended as required
| test | result |
|---|---|
| M1: U_L13 manifest with 1 of 128 leaves removed | cover NOT_COVERED (rc 10). Control with all 128: cover VERIFIED |
| M2: leaves.icnf whose last line lacks ` 0`, lacks the final newline, or both; extra line `a 5 -5 0` | each directory reported as a problem; manifest exits 1; only the intact copy is used |
| M3: F with one clause removed (header kept / header adjusted) | `base CNF sha256 mismatch`, exit 1, no records |
| M4: stub cake_lpr printing `s NOT VERIFIED`, nothing, `s VERIFIED UNSAT junk`, or killed | REJECTED every time. Control with the real cake_lpr: VERIFIED |
| M5: cases.icnf with one cube changed (literal negated / literal dropped) | `case CNF sha256 mismatch for U_L2-6`, exit 1, no records |
| M6: U_L13 split over WA/U_L13_a (lines 1–70) and WB/U_L13.s1 (lines 51–128, literals reversed) | 148 lines become 128 leaves; 20 of them list both sources; the set equals W31's; cover VERIFIED |
| M7 (Fix 2): resume with a rotated manifest into the same OUT | cover and leaf 0 re-checked; a second run adds nothing; no work dirs left |
| M8 (RISK-1): hand-made record with literal 0 | REJECTED (CaDiCaL "too many clauses") |

## First real use
- **Manifests.**
  - `manifest_f3b07a7.jsonl` and `cases_f3b07a7.jsonl`: 3,998 leaves in 56 cases, 0 problems.
  - At the newer WAVE1 commit 5d0fdff: `manifest_5d0fdff.jsonl` and `cases_5d0fdff.jsonl`, with
    17,574 leaves in 102 cases, 0 problems.
  - Both are under 3 MB, so I committed them with their sha256.
- **Choosing cases.** I took cases where every shard named in `verify/ii_wave1.json` has a
  directory and every directory has an empty `open.icnf`. I spot-checked the READMEs and
  `status.txt`: W19–W24 and W31 say CLOSED, and W33 says CLOSED(whole).
- **The four runs**, all with `--nshards 1 --shard 0 --jobs 4`:
  - sub1: U_L11 and U12_L.
  - sub2: the 38 cases whose single leaf is the empty cube.
  - sub3: the 8 other closed cases at f3b07a7, by increasing leaf count.
  - sub4: closed cases first seen at 5d0fdff. The 10 cases whose single leaf is the empty cube came
    first, then the rest by increasing leaf count. I stopped this run at 10:32 because of the time
    limit.

### Accepted: 68 cases (`accepted.tsv`; all rows in `accepted_all.tsv`)
- Acceptance means cover VERIFIED for the case's full leaf list and every leaf VERIFIED, with its
  CNF sha256 recomputed independently.
- Leaves: 2,469 of 2,469 verified.
- Total time: 28,607 s CaDiCaL and 7,145 s cake_lpr. These totals include the cover checks.
- Per solved leaf, across every leaf solved in these runs (n = 2,581):

  | | median | max |
  |---|---|---|
  | solve | 4.1 s | 281.3 s |
  | check | 2.2 s | 19.2 s |
  | solve + check | 6.4 s | 298.9 s |

- The 20 multi-leaf cases:

  | case | leaves | solve s | check s |
  |---|---|---|---|
  | U_L11 | 128 | 4297 | 745 |
  | U12_L | 191 | 5262 | 820 |
  | U_L13 | 128 | 3113 | 525 |
  | U_L14 | 128 | 2627 | 470 |
  | U10_L7 | 128 | 314 | 267 |
  | U3_L6 | 124 | 1958 | 418 |
  | U3_L10 | 125 | 849 | 306 |
  | U3_L14 | 128 | 754 | 301 |
  | U6_L2 | 124 | 2690 | 463 |
  | U7_L6 | 108 | 400 | 235 |
  | U4-8_L | 108 | 168 | 193 |
  | U4_L5 | 111 | 1053 | 285 |
  | U4_L9 | 114 | 416 | 238 |
  | U5_L10 | 108 | 296 | 218 |
  | U5_L16 | 104 | 163 | 190 |
  | U5_L4 | 110 | 1073 | 286 |
  | U5_L9 | 115 | 395 | 238 |
  | U7_L10 | 114 | 216 | 217 |
  | U7_L4 | 110 | 672 | 254 |
  | U9_L6 | 115 | 368 | 236 |

- The 48 cases whose single leaf is the empty cube (each is a direct re-solve of its case CNF):

  U10_L13, U10_L14, U10_L8, U10_L9, U11_L13, U11_L14, U11_L8, U11_L9, U12_L10, U12_L13, U12_L7,
  U13_L8, U13_L9, U14_L10, U14_L6, U15_L12, U15_L6, U16_L7, U4-15_L, U5-11_L, U5-13_L, U5-15_L,
  U5-8_L, U6-11_L, U6-12_L, U6-16_L, U6-7_L, U6-8_L, U6_L12, U6_L13, U6_L15, U7_L11, U7_L13,
  U7_L15, U7_L16, U8_L12, U8_L13, U9_L13, U9_L14, U_L4-11, U_L4-13, U_L4-6, U_L4-9, U_L5-11,
  U_L5-13, U_L5-15, U_L5-6, U_L5-9.

### Not accepted (incomplete only: no failures)
These are sub4 cases that I had not finished checking when I stopped at the time limit. Their
covers are already VERIFIED. No leaf of theirs failed; the remaining leaves were simply never run.

| case | leaves | verified | WAVE1 dir |
|---|---|---|---|
| U6_L8 | 116 | 112 | W32/U6_L8 |
| U11_L2 | 117 | 0 | W32/U11_L2 |
| U3-6_L | 119 | 0 | W33/U3-6_L |
| U4_L14 | 119 | 0 | W32/U4_L14 |
| U8_L5 | 116 | 0 | W32/U8_L5 |
| U_L2-16 | 117 | 0 | W33/U_L2-16 |

To finish them, resume with the same sub-manifest and OUT:

```
v3_check.py --manifest results/V3T/sub4_5d0fdff.jsonl --out check_sub4_5d0fdff.jsonl --nshards 1 --shard 0
```

Other cases that were closed at 5d0fdff were not started:
- U10_L2, U12_L4, U13_L4, U14_L, U3-12_L, U3-9_L, U4-5_L, U_L10, U_L2-11, U_L2-12, U_L2-14,
  U_L2-5, U_L2-9 (100–128 leaves each);
- U10_L, U6_L, U_L4, U_L2-3, U_L2-4, U_L2-6, U_L2-7 (367–1856 leaves each).

## Files
- `REVIEW.md`: the review findings.
- `mutations.log`: the mutation tests.
- `tools.txt`, `env.txt`: tools and environment.
- `manifest_*.jsonl`, `cases_*.jsonl`, `*.sha256`: the manifests.
- `sub*.jsonl`: the sub-manifests, renumbered.
- `check_sub*.jsonl`: v3_check output. Proof and CNF files were deleted.
- `scripts/aggregate.py`: the acceptance join.
- `aggregate.txt`, `accepted.tsv`, `accepted_all.tsv`: the acceptance results.
