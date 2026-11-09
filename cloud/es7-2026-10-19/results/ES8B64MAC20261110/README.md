# ES8B64MAC20261110: the Mac share of the budget-64 search is finished, and how to bring it to Linux

**The Mac closed all 2,047 contexts of its share (positions 2,040–4,096) with exact replay and no witness. With the
1,982 Linux contexts, 4,029 of 4,096 are closed. On 10 November the Mac also closed positions 1,950–2,039 (89
contexts), where the 67 open contexts very probably lie. No bound below 311 is claimed.** These are search results of
`run_context.py`. They count towards ES(8) ≤ 310 only after the frozen pipeline of
`experiments/omission-compact-checker-2026-11-05/logs/es310/OPERATOR.md` has exported, compiled and assembled all
4,096 contexts and `assemble_final310.sh` reports `VERIFIED` in real mode.

The Mac result files **cannot be copied into the Linux `runs/` as they are**. That copy was the merge step written
on 7 November (`ES8UPPER20261105`, "To merge the two machines"); the section "Found on 10 November" below says why
it fails, and this record supersedes it. Use `tools/import_mac_runs.py` instead.

## The Mac share (7–8 November)

- Driver `ES8UPPER20261105/tools/mac_campaign.py`, 15 workers at nice 10. It ran from 21:39:50 KST on 7 November to
  20:32:27 KST on 8 November (22 h 53 min). The setup and its input hashes are in `ES8UPPER20261105/README.md`
  ("Mac share").
- **2,047 of 2,047 contexts closed.** The 10 pilot contexts in the range that Linux had already closed were
  skipped.
  - Every result has status closed, replay ok and minimum margin 1. No leaf is over budget.
  - 3,675,083 budget-64 nodes and 1,838,565 leaves, 8.82 times the 416,621 budget-63 record nodes of these
    contexts.
  - 1,182,893 CPU-s (328.6 CPU-h), at 0.322 CPU-s per node.
  - Every result records Python 3.14.10 and highspy 1.15.1.
- The driver log has one driver start, 2,047 job starts with no context started twice, 2,047 closures with
  `replay True`, no `ERROR` line and no witness.

## Totals with Linux

- Linux closed 1,982 contexts before its stop at 18:26 KST on 7 November (`ES8UPPER20261105`). Ten of them lie in
  the Mac's range, so Linux closed 1,972 of positions 1–2,039.
- **4,029 of 4,096 are closed, and 67 are open.** This count is arithmetic on the two records. All 67 lie at
  positions 1,733–2,039, the range that the last Linux export (1,744 contexts) does not cover. Only the Linux
  `runs/` directory shows which 67 they are. About 30 were in flight at the stop, and the rest were never started.
- Linux started contexts in campaign order. With about 30 in flight, its frontier was near position 2,003, so the
  open contexts are most likely near positions 1,970–2,039.

## Gap run on the Mac (10 November, from 03:34:58 KST)

- `campaign/floor` was lowered from 2,040 to 1,950 and the same driver was restarted with no job alive. It runs
  positions 1,950–2,039, 89 contexts (position 1,968 is a pilot context Linux has exported). Linux skips every
  context it finds closed, so this saves the Linux machine that work. Contexts that Linux closed too are skipped
  at import ("linux_has"), so nothing is overwritten.
- **Result: 89 of 89 closed** by 05:15:35 KST (1 h 41 min). Every position from 1,950 to 2,039 except 1,968 is
  covered.
  - Every result has status closed, replay ok with every leaf checked, minimum margin 1, and pending 0. No leaf is
    over budget.
  - 269,827 budget-64 nodes and 134,958 leaves, 8.90 times the 30,315 budget-63 record nodes of these contexts.
  - 82,366 CPU-s (22.9 CPU-h). No `ERROR` line and no witness.
- Whether these 89 cover all 67 open contexts shows only at the Linux import: `closed_in_campaign_runs` is then
  4,096. Any context they miss, the Linux campaign runs when it resumes.

## Found on 10 November: the Mac files need one field rewritten

A result file records the absolute path of `pbb_strong.py` in `rules.pbb_strong`, and the Mac files record a Mac
path. Two frozen scripts use that path:
- `export_es310.py` hashes the file at that path (`global_inputs`). A missing file raises `RefuseAll`
  ("pbb_strong.py (...) or run_context.py missing"), and the whole export run is refused.
- `merge_es310.py` refuses when the contexts in scope record more than one `pbb_strong` path. So a copy of the
  file placed at the Mac path on Linux would not help either.

The frozen scripts must not change (OPERATOR.md, "Never during the run"). `tools/import_mac_runs.py` therefore
rewrites the data instead, on Linux, at import:
- It sets `rules.pbb_strong` of each imported result to the one path the Linux results record. That file must
  exist there with sha256 `2aa90df2…`.
- Nothing else changes. Before the edit it checks that `json.dumps(..., indent=1)`, the writer of
  `run_context.py:168`, reproduces the Mac bytes exactly; after the edit it checks that only that one field
  differs. The tree `.json.gz` is copied byte for byte.
- It never overwrites. A context with any `ctx-<k>-b64.*` file in the Linux `runs/` is skipped.
- It refuses if a `run_context.py` or `campaign.py` process is alive, if a bundle file differs from the bundle's
  `SHA256SUMS`, if any WITNESS file exists, or if a Mac result is not closed with a full replay.
- It appends `ctx, action, gz sha256, Mac result sha256, imported result sha256` per context to
  `<C>/import-mac-runs.tsv`. So each imported result is tied to its Mac original, which stays unchanged on the Mac
  and in the bundle.

**Test on the Mac** (`tools/test_import_mac.sh`, log `logs/test-import-20261110.txt`):
- Three Mac contexts (768, 3850, 4068) were imported into a stand-in campaign directory. The dry run wrote nothing;
  rerunning imported nothing (no-clobber). The imported copy differs from the Mac file in the one `pbb_strong`
  line, and the trees are identical.
- The **frozen** exporter (sha256 `29854a37…`) exported all three with exit 0: 1,924 leaves, every leaf replayed
  twice, minimum margin 1, nothing refused. `merge_es310.py --partial` (`3cbf428b…`) then gave exit 0 with no
  alert.
- Negative control: an unrewritten result whose path does not exist was refused with exit 1, with the message
  above.
- macOS has no `/proc`, so the exporter's live-job scan was given an empty `/proc` (no job was live for these
  contexts). The files were also dated 300 s back to pass its 120 s age check. Neither change touches what is
  checked.

## A driver defect, harmless so far

`mac_campaign.py`'s `alive()` splits `ps` output on spaces, but the Mac work path contains `lean 4 ` with a space.
So it never finds a live job, and `campaign/STATUS` shows `"running": []` while jobs run.
- Within one driver run this is harmless: the driver counts and skips its own children.
- A driver restarted while jobs are alive would start them again. The driver has not been restarted while jobs
  were alive: the log has two driver starts (7 Nov, 10 Nov), both with no job running, and no context started twice.
- **Do not restart the Mac driver while `run_context.py` jobs are alive.**

## Steps on Linux (decisions marked)

1. Copy `<mac-b64-dir>/es8-b64-mac-bundle-20261110.tar` (1,179,786,240 bytes) to the Linux machine; the author
   chooses how. Its sha256 must be
   `36ccce708465af0d3a9072bc606a932515800be3774d578d8cb2dfa58ef6b3d8`. Then `tar xf` it, and inside
   `es8-b64-mac-bundle-20261110/` run `sha256sum -c SHA256SUMS` (4,272 lines, all OK).
2. Check that the campaign is stopped: `systemctl --user is-active es8-b64-campaign` must not say `active`.
3. `python3 -I import_mac_runs.py --bundle <bundle> --campaign <C> --dry-run`. Expect exit 0, and `imported` plus
   `linux_has` equal to the number of bundle contexts.
4. The same command without `--dry-run`. `closed_in_campaign_runs` is printed. It is 4,096 if the Mac gap run
   covered every open context.
5. Resume the campaign as in `<C>/campaign/SHUTDOWN-20261107.txt`. **The author chooses the worker cap.** The
   campaign reruns no closed context. It runs whatever is still open, then logs `ALL 4096 CONTEXTS CLOSED` (gate 1).
6. OPERATOR.md: one A2 cycle to export the contexts not yet exported (about 2,350; the exporter measured
   0.123 s per context plus 0.735 ms per leaf, so about half an hour). Then B1–B4. **The author chooses the Lean job
   count and memory caps.** Full load made the display blink on 7 November.

## Files

- `tools/import_mac_runs.py`: the import, run on Linux (Python standard library only).
- `tools/test_import_mac.sh`: the Mac test above; `logs/test-import-20261110.txt` is its output, with machine paths
  replaced by placeholders.
- `tools/make_bundle.sh`: builds the bundle on the Mac (`runs/` files of every closed context, unchanged, with
  `SHA256SUMS`, `contexts.txt`, the driver log and `import_mac_runs.py`) and its tar.
  - Run at 05:16 KST on 10 November, it gave **2,136 contexts** (2,047 + 89) and 4,272 files, tar sha256
    `36ccce70…`.
  - The bundle was then checked on the Mac. The tar was extracted, `shasum -c` found all 4,272 files OK, and an
    `import_mac_runs.py --dry-run` against an empty stand-in campaign directory found all 2,136 importable. That
    means every result is closed with a full replay and reproduces byte for byte under `json.dumps(indent=1)`.
  - The bundle's `import_mac_runs.py` is identical to `tools/import_mac_runs.py`.
- `logs/bundle-SHA256SUMS`: a copy of the bundle's `SHA256SUMS`: the sha256 of every Mac result and tree, as written
  by the Mac.
- `logs/mac-campaign.log`: the Mac driver log, 7–10 November.
