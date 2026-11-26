# CLEANUP20261126: unnecessary Lean files and an already-uploaded copy deleted (26 Nov 2026)

Owner, 26 Nov: "upload every verified things to my github repo and clean this pc up ... clean up by delete already
uploaded and unnecessary lean files". An AI model was consulted for review (not a person; es-research §7). `receipt.json` (from `receipt.py`)
gives, per deleted target, its file count, bytes and a content digest; `receipt.py check` re-hashed every target right
before deletion.

**Done 26 Nov 2026 13:55:45-13:55:46 KST** (`execute.log`): after commit 13c189ede (this receipt) was on origin/main and
the pushed `receipt.json` equalled the local one, `receipt.py check` re-hashed all 7 targets (7 OK) and they were deleted
(25.97 GB; free space 963 -> 988 GB, `df -B1G`).

| target | files | GB | why it can go | restore |
|---|---|---|---|---|
| `LEANLB20261111/.lake/packages` | 60,177 | 6.41 | duplicate of the repository's Mathlib `f897ebcf` packages | `cp -a <repository>/.lake/packages .lake/` |
| `ENCBLEAN/geo/.lake/packages` | 60,177 | 6.41 | the same | the same, in `ENCBLEAN/geo` (or `lake exe cache get`) |
| `LEANLB7_20261126/.lake/packages` | 60,177 | 6.41 | the same | the same |
| `cleanup-20261125/fv302-regen/export` | 220 | 1.26 | regenerated sources of the 25 Nov regeneration test | verdict in git: `FORMAL20261122/fv302/regen-test/` |
| `cleanup-20261125/s3520-regen/out` | 361 | 1.56 | the same, for s35_20 | `FORMAL20261122/res-slices-fv/regen-test/compare3520.*` |
| `cleanup-20261125/slices-regen/out` | 383 | 1.53 | the same, for the other slices | `res-slices-fv/regen-test/compare_slices.*` |
| `gh-c2-20261125/release/P8_1-9.lrat.zst` | 1 | 2.40 | already on GitHub: private archive repository, release `c2-p8-1-9-2026-11-25` | `gh release download` (C2RECHECK) |

**Why the package copies are redundant** (`compare_pkgs.py` → `pkgs.json`): in each copy, 60,103 of 60,177 files have
the same path, size and SHA-256 as in the repository's `.lake/packages`. None is missing there, none is hard-linked,
and every Lean source and olean is equal. The 62 differences in each copy are Lake bookkeeping that records its own paths (20
`.trace`/`.setup.json` files) and `.git` internals (42 in the three record copies). No module of the ES(8) ≤ 302 import
closure lives in these copies, so the repository's `.lake` is never written.

**Restore tested on 26 Nov:** LEANLB7_20261126's copy was deleted, restored with `cp -a` from the repository (4 s), and
then `lake build` replayed in 3.3 s (no fetch, no rebuild; `leanlb7_restore_build.log`) and `scripts/audit7.sh`
printed AUDIT PASS (`leanlb7_restore_audit.log`). That restored copy is the one deleted here.
The check columns of RESULTS rows C7, D4 and D1 and the READMEs of LEANLB7_20261126, LEANLB20261111 and ENCBLEAN now
start with the restore step.

**Second set (owner-approved in the 26 Nov wrap-up)**, receipt `receipt2.json` (from `receipt2.py`):

| target | files | GB | why it can go | restore |
|---|---|---|---|---|
| `tools/e810-lean/research/hall-reduction/.lake/packages` (#810 project) | 60,176 | 6.42 | duplicate of the same Mathlib `f897ebcf` (`pkgs.json`: 60,075 equal files, none missing; the rest Lake bookkeeping and `.git` internals) | `cp -a <repository>/.lake/packages .lake/` |
| `bal186-20261119/zrow/b70zs54/occ` | 118 | 18.71 | resumable state of the stopped exploratory budget-70 finder: 98 of 16,384 contexts, no witness, no result claimed; the owner does not want the 301 search restarted. `PLAN.md`, `steps.log` and `occ.out` stay | none (a new run starts from zero) |

**Kept:** everything the ES(8) ≤ 302 theorem imports (`closure3.tsv`: about 281 GB of oleans), the trees and inputs
that regenerate its chunk sources, every kept SAT proof, `cleanup-20261125/fv304-regen` (its verdict is only in prose),
and (after the second set) nothing else.

**Trees upload (owner-approved, 26 Nov)**, files in `trees-upload/`: the four archives described in `NOTES.md`
(`b69zs54`, `b67`, `es308-runs-inputs`, `ctx-manifests`; 46 parts of at most 1900 MiB, 85,899,868,160 bytes in all) were
uploaded to the private archive repository, release `trees-302-20261126`, from 14:21:33 to 16:05:02 KST (`run.log`,
`upload_trees.sh`). GitHub's SHA-256 digest of every part equals the local one (`verify.tsv`: 46 OK, 0 BAD).
`remote.tsv` lists every asset with GitHub's digest; the four `.list` files, `NOTES.md` and `SHA256SUMS` also match
their local copies. The number of entries in each list equals `find | wc -l` over its source directories (32,634;
8,212; 52,650 + 439; 32,619 + 3,640). The originals stay on this machine (keep-set). Only the temporary tar parts were
deleted, at 16:07:01, after the check (`delete_parts.log`; free space 931 -> 1011 GB, `df -B1G`). `NOTES.md` calls
`<name>.list` "the tar's verbose file list"; it is the plain list of member names, one per line.
