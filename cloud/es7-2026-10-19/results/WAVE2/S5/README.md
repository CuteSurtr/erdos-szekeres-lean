# WAVE2 / S5: sub-case (ii) hull cases taken from the back of the W32/W33 lists

**My 34 cases are all closed: 6 by S5, 28 by W32/W33.** No case was started and left
unclosed, and every case was reached. No SAT answer appeared, and cake_lpr rejected no proof.

## Where it ran
One cloud VM, 4 cores, 15 GB RAM (`env.txt`), 2026-10-20 10:35 to 10:57 UTC.

Tools (`tools.txt`):
- CaDiCaL c6073042 (3.0.1);
- march_cu from CnC 705b60c6, built with `-fcommon`;
- cake_lpr a36874a8 (`cake_lpr.S` sha256 2f3af32d…72b7d4a). Its bundled example prints `s VERIFIED UNSAT`.

No drat-trim was used.

## sha256 checks
- F was regenerated (gen_etv.py + mirgen.py --interior --yflip-unit) and gives `69c1dc8f…ffff932d`: OK.
- Each case CNF from `hullsplit.py case` matches `cnf_sha256` in `results/Mii-S/cases.jsonl` (listed in `tools.txt`).
- The first record of each `leaves.jsonl` holds `case` and `case_sha256`.

## Cases closed by S5

| case | method | verified leaves | open | solve s | check s | top cubes (sha256) | covercheck |
|---|---|---|---|---|---|---|---|
| U11_L6 | whole case | 1 (`a 0`) | 0 | 75.5 | 10.7 | – | s COVERED 1 |
| U5_L11 | whole case | 1 (`a 0`) | 0 | 118.6 | 11.0 | – | s COVERED 1 |
| U4-16_L | whole case | 1 (`a 0`) | 0 | 61.1 | 18.2 | – | s COVERED 1 |
| U13_L5 | whole case | 1 (`a 0`) | 0 | 106.9 | 22.7 | – | s COVERED 1 |
| U9_L4 | cubes (driver) | 117 | 0 | 618.1 | 359.3 | 117, 10 refuted by march (40b590be…) | s COVERED 117 |
| U15_L4 | cubes (driver) | 128 | 0 | 436.3 | 350.8 | 128 (e8291cb3…, same as W33's top.icnf) | s COVERED 128 |

Solve and check times are summed over the leaves. For U9_L4 and U15_L4 the 120 s whole-case
attempt timed out first. In both of them every top cube closed within the 300 s cap, so nothing
was split.

### Notes on the closed cases
- **U9_L4:** the "10 refuted" cubes are still in `top.icnf` as full cubes (AUDIT NOTE-2). Each of
  them was solved and proof-checked like any other cube.
- **U13_L5 and U15_L4:** W33 had started these by the time S5 reached them (W33's `top.icnf`
  existed, with 128 open and 0 leaves). U13_L5 was already closed whole by S5. U15_L4 was moved
  to the end of the list and then run, because nothing else was left.

## Cases skipped because they were closed elsewhere (28)
- **W32 (15 cases):** U13_L12, U12_L11, U15_L10, U6-13_L, U_L4-12, U_L4-16, U8_L16, U_L2-8, U14_L4,
  U6_L14, U16_L10, U16_L6, U15_L11, U15_L5, U14_L9.
- **W33 (13 cases):** U8_L7, U7_L5, U6_L9, U6_L4, U5_L12, U5_L6, U4_L15, U4_L11, U3_L15, U12_L5,
  U11_L4, U10_L4, U9_L7.
  - The last four were only "started" at 10:37. W33 closed them by 10:47, before S5 reached them.

The rule for "closed": a non-empty `leaves.icnf`, and an `open.icnf` with no `a` lines
(`scripts/status.py`, run against a fresh pull).

## Cases started but not closed
None.

## Cases not reached
None.

## Method
- `scripts/runner.py` takes the cases in the given order. Before each case it runs
  `git pull --rebase --autostash` and checks whether another machine has closed or started it.
- `scripts/whole.sh` makes the whole-case attempt:
  `cadical --lrat --binary=false -q -t 120`, then `cake_lpr`. Only the exact line
  `s VERIFIED UNSAT` counts.
- Otherwise the driver runs:
  `close_march.py CASE.cnf S5/<case> --name <case> --depth 7 --timeout 300 --split-depth 6 --jobs 4 --hours H`.
- The first four whole-case attempts ran in parallel, ahead of the runner, and so did the
  attempts for U4-16_L and U13_L5.
  - For U11_L6 the runner also ran its own attempt. Both attempts were UNSAT and passed cake_lpr;
    the recorded times are from the runner's run.
- Logs: `runner.log` and `whole.log`.

Driver: `close_march.py` is F2's adaptation of the W19 driver, plus one guard. `driver.diff`
records what was checked:
- (a) every solver and checker job gets its own `tempfile.mkdtemp` directory;
- (b) `leaves.icnf` and `open.icnf` are written to a temporary file and renamed into place;
- (c) the first `leaves.jsonl` record holds `case` and `case_sha256`;
- BUG-1: a leaf counts only with `s VERIFIED UNSAT`.

The S5 guard: if march_cu refutes a cube while splitting it (`a 0`, AUDIT NOTE-1), the cube is
recorded as NOSPLIT and stays open. Without the guard, frontier() would loop forever. The guard
never triggered in this run.

Every `leaves.icnf` line has the form `a l1 .. lk 0`. The set of its cubes equals the set of
records with `status == "UNSAT"` and `cake_lpr == "s VERIFIED UNSAT"` in `leaves.jsonl`. Leaves
are full cubes (top cube plus split suffixes) over F's variables. No CNF or LRAT file is committed.
