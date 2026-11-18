**Verdict: CONFIRMED at the label COMPUTED, with three wording exceptions** (claim `s1-v11-skiplist`, filed by S1;
verifier VS, 15 November 2026, 19:40-19:47 KST). The diffs, the too-big record, the 75 open contexts, the test-packet
copy and the c600s1 events all check with VS's own code. Exceptions:
(1) `inputs/b35s20-v600` is not a full byte copy of `b35s20-v143`. `rows.txt` and `extra.json` are byte-identical,
but `manifest.json` (9,796 B) was not copied; neither the finder nor `append_cuts_v2.py` reads it.
(2) "c143s2 logged 36 too-big attempts in its first 26 min" cannot be re-derived, because too-big events carry no time.
The "0 closes" part holds: the log had no `closed` event at all at 19:4x, with 71 too-big events by then.
(3) The list of behavioural changes in (a) leaves out three things. One is the new standalone mode `--too-big-only`,
which continue34_v11 never passes. The other two are that the witness-grace / stop-witnesses counter now counts WITNESS
lines of both logs, and that the RSS/swap guard and the stop cover both workers; the extra worker is terminated when
the frontier worker ends. None of these touches the claimed context selection.

# VERIFY_V11: run_tree_v6 / continue34_v11 skip list (claim s1-v11-skiplist)

## (a) Tool diffs

- `diff -u run_tree_v5.py run_tree_v6.py` and `diff -u continue34_v10.py continue34_v11.py` were regenerated. Apart from
  the two header lines (path and time) they are identical to `pm1115/s1/run_tree_v5_v6.diff` and
  `continue34_v10_v11.diff`; VS's copies are `vs_run_tree_v5_v6.diff` and `vs_continue34_v10_v11.diff`.
- VS read both diffs line by line.
  - continue34_v11 adds a docstring and the arguments `--extra-cap` and `--extra-threads`. It calls `run_tree_v6.py`
    instead of v5, passing the two extra arguments only when `--extra-cap` > 0. Nothing else changed.
  - run_tree_v6, frontier `--ctx`: the open contexts of `contexts.json` that have no ctx file and no TOO_BIG line with
    nodes_so_far above `--max-ctx-nodes` (the maximum per context is used). An empty list is passed as `--ctx=-1`.
  - run_tree_v6, extra worker: it gets the open contexts with cap < recorded ≤ extra cap, using the same command with
    its own thread count and `--max-ctx-nodes=<extra cap>`. It starts after the frontier worker's `start` event.
  - After the run, run_tree_v6 appends one TOO_BIG line per too-big event of both logs (tags `<tag>` and `<tag>.x`). It
    writes the new receipt fields (`sel`, `extra`, `too_big_recorded`). WITNESS events of both logs go through the
    unchanged exact row check.
  - The additions not listed in the claim are exception (3) above.
- fastbb2 (the record's source `FASTBB20261113/tools/fastbb2.cpp`, lines 1719-1723) keeps the context order of the
  master. It uses the `--ctx` list only as a membership filter, so `-1` selects nothing, and the frontier order is the
  v5 order restricted to the list. Each fastbb2 process rewrites master.json and contexts.json at its start, and
  claim files keep two processes off one context. In the test, the frontier and extra lists are disjoint.
- Unchanged: `bin/fastbb2` (mtime 13 Nov 20:32, SHA-256 `39b724a2…`), `cut34_v4.py` (14 Nov 22:57, `906db163…`),
  `probe35_v2.py` (14 Nov 23:20, `b9948e95…`), `append_cuts_v2.py` (14 Nov 22:57, `5f0d1905…`), and the audit/replay
  scripts in `../audit/` (newest 14 Nov 22:57). No earlier record lists their hashes, so "unchanged" rests on the mtimes
  and on the continue34 diff, which touches only the finder call.

## (b) Too-big record (own code `vs_s1check.py`, read-only)

| item | claim | VS |
|---|---|---|
| live-packet receipts present at 19:10 | 45, newest c143s1 18:39:42 | 45 (`bb` = the live packet path; 2 other receipts are for `bb-v9test`), newest c143s1.json 18:39:42 |
| context_too_big events | 3,270 from 43 logs | 3,270. All 45 logs are present (no `.x.log`), and 43 of them contain too-big events |
| record file | TOO_BIG.txt `08a7a1f8…` | VS's reconstruction (tags by name, `.log` then `.x.log`, file order) is **byte-identical** (`too_big_vs.txt`, SHA-256 `08a7a1f8…`) |
| distinct contexts | 232 | 232 |
| open at 19:10 and recorded above 150,000 | 75 | 75 (open = no live ctx file written by 19:10:00; 998 closed then) |
| change since A2's 72 (16:47) | 1044 closed; 1040, 1046, 1061, 1066 new | exactly: A2's list − {1044} ∪ {1040, 1046, 1061, 1066}; live `ctx-1044` written 18:35:21 |

## (c) Test namespace and the first test slice c600s1

- Packet `bb-v11test`. It has 998 ctx files older than the c600s1 start, all byte-identical to the live ones, and their
  set equals the live packet's closed set at 19:10. Its master.txt, master.json and contexts.json equal the live ones
  byte for byte; the live copies last changed at 23:13:12 and 18:52:34, so they are also the 19:10 state. TOO_BIG.txt
  is the file of (b).
- Inputs: see exception (1).
- c600s1 command lines, read from `/proc` (`frontier_cmdline.txt`, `extra_cmdline.txt`):
  - frontier: 1 thread, `--max-ctx-nodes=150000`; extra worker: 1 thread, `--max-ctx-nodes=300000`. Unit
    `esr-ags-v11test` has CPUQuota 150 %, and both `start` events say threads 1.
  - The frontier list has 6,992 contexts (= the `todo` of its start event). It **equals** the definition (open at
    19:10, none recorded above 150,000) in content and order. The extra list (75) equals its definition.
- Frontier events: none names one of the 75. By 19:28 (elapsed ≤ 991 s from the 19:11:29 start), 1069 closed at 245 s
  (its `seconds` = 245.0, so the first close came after 245 s), then 1074-1079 at 404-955 s.
- Extra worker: 0 closed at 357 s (201,333 nodes) and 33 at 789 s (261,085 nodes). Later 51, 80 and 81 closed as well.
  Every extra event is in its list. Contexts 0 and 33 have TOO_BIG lines at 150,001-150,003 in the live rounds
  c134s1-c143s1.
- Live rounds, in time order. "First new close" is the start (elapsed − seconds) of the first closed context that no
  earlier log of the packet had attempted. "Re-attempts" counts the too-big events on contexts recorded too big in
  earlier logs that were logged before that close.

| round | threads | first new close starts at (min) | re-attempts before it | too-big events in the log |
|---|---|---|---|---|
| c139s1 | 4 | 41.3 | 54 | 66 |
| c140s1 | 4 | 45.5 | 60 | 63 |
| c141s1 | 4 | 43.9 | 60 | 72 |
| c142s1 | 4 | 52.9 | 72 | 75 |
| c143s1 | 4 | 53.0 | 73 | 74 |

The claim's "41-53 min" and "54-73 recorded contexts" hold, with the re-attempts counted in log order, since too-big
events have no time field.
- c143s2 (live, started 18:52:33): see exception (2).

## Not checked

The final round and append results that S1 promises in a second claim. The fastbb2 binary was not rebuilt from the
source that was read.

## Files (`/home/jay/research/data/roadmap-20261115/pm1115/vs/s1-v11-skiplist/`)

| file | SHA-256 |
|---|---|
| `vs_s1check.py` | `1f1693d1fd33d1704c02593bd2bc71c4a9db52e22bf8e6158b2b07fdc3d9a1c8` |
| `vs_s1check.json` (all numbers above) | `0a6c2f83f1cc020d56a76508c6bdb3b099e8b2817947120d71c4a5d387808ac3` |
| `too_big_vs.txt` | `08a7a1f8c6d52570cffbdb39ee8253071f8c1f2f14f780ed6d3dd3d4ec639e06` |
| `open_above_150000.txt` | `aaac9eb556a1390cfe3d98d353ff51477991a3a186267eb48d5dba8b2b72a0a8` |
| `frontier_cmdline.txt`, `extra_cmdline.txt` | `bd459336…`, `d01d8290…` |

All reads were read-only: no live or test file was written, and no unit was started (the check ran in the foreground,
1.1 s). No git action.
