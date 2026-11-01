# WAVE1 / W32: 51 sub-case (ii) hull cases (kind "cases")

**All 51 assigned cases are closed.** Every leaf has a cake_lpr `s VERIFIED UNSAT`, and each case's `leaves.icnf`
passes `results/Mii-S/scripts/covercheck.py` (`s COVERED`). No SAT answer appeared.

## Where it ran
One cloud VM, 4 cores, 15 GB RAM (`env.txt`), 2026-10-20 06:55 to 09:50 UTC.

Tools (`tools.txt`):
- CaDiCaL c6073042 (3.0.1);
- march_cu from CnC 705b60c6, built with `-fcommon`;
- cake_lpr a36874a8; the bundled example prints `s VERIFIED UNSAT`.

No drat-trim was used.

## sha256 checks
- `m33k7int.sub.cnf` was regenerated (gen_etv.py + mirgen.py, as in make_cnfs.sh) and gives `69c1dc8f…ffff932d`: OK.
- `verify/ii_wave1.json` gives `6df36dab…00901c72e`: OK.
- All 51 case CNFs from `hullsplit.py case` match both the W32 entry and cases.jsonl (`case_hashes.txt`). Every record in `leaves.jsonl` repeats the case CNF sha256.

## Method (`scripts/run_w32.py`; the original is `scripts/close_march.orig.py`)
Cases run in the listed order on one shared pool of 4 workers. A lower list index has priority.

1. Plain `cadical --lrat -t 60` on the whole case. An UNSAT counts only after cake_lpr prints `s VERIFIED UNSAT`; the leaf is then the empty cube `a 0`.
2. Otherwise, `march_cu CASE.cnf -d 7 -o top.icnf`. The file is kept, and its sha256 is recorded in the `top` record and listed below.
3. Each top cube runs `cadical --lrat -t 300` and every UNSAT is checked with cake_lpr. A timeout is split with `march_cu -d 6`.

Changes from close_march.py:
- one pool shared across cases;
- the direct 60 s step;
- resume from leaves.jsonl;
- `leaves.icnf` lists only cake_lpr-verified leaves; `open.icnf` lists what is still open;
- CPU time per subprocess, taken from wait4.

Proofs and CNFs were deleted after checking; none are committed.

The first launch wrote its logs inside the repo, and a `git pull --autostash` replaced those files while they were open. The records already written were recovered from the open file descriptors. The two interrupted top-level marches (U6_L2, U3_L6) were re-run from scratch, and the run was restarted with output outside the repo, which is copied in before each commit. CPU spent by the killed processes is not counted below.

## Per case
Totals:
- 28 cases closed by the direct 60 s run, 23 by cube-and-conquer;
- 1 cube split at depth 6;
- 2841 verified leaves;
- 9.89 CPU hours recorded (solve + check + march).

`verified/UNSAT` counts cake_lpr-verified UNSAT records against all UNSAT records. Every top.icnf also passes covercheck as a partition.

| case | result | method | top cubes | refuted | splits | leaves | verified/UNSAT | open | cover | CPU s | top.icnf sha256 (prefix) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| U6_L2 | closed | march | 124 | 4 | 0 | 124 | 124/124 | 0 | COVERED | 3645 | 15269e00eeff3982 |
| U5-11_L | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 35 | - |
| U5-13_L | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 35 | - |
| U5-15_L | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 35 | - |
| U6-7_L | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 26 | - |
| U6-11_L | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 21 | - |
| U6-16_L | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 21 | - |
| U3_L6 | closed | march | 124 | 4 | 0 | 124 | 124/124 | 0 | COVERED | 3032 | 8bbff1a4e9c440a1 |
| U3_L10 | closed | march | 125 | 1 | 0 | 125 | 125/125 | 0 | COVERED | 1588 | 835687738a2e3910 |
| U3_L14 | closed | march | 128 | 0 | 0 | 128 | 128/128 | 0 | COVERED | 1550 | 551604e27f512b12 |
| U4_L5 | closed | march | 111 | 11 | 0 | 111 | 111/111 | 0 | COVERED | 1597 | 29b7ebaf23fd8c0d |
| U4_L9 | closed | march | 114 | 10 | 0 | 114 | 114/114 | 0 | COVERED | 1034 | 417d6afa34395f1f |
| U4_L14 | closed | march | 119 | 7 | 0 | 119 | 119/119 | 0 | COVERED | 1142 | 298b0633bd718447 |
| U5_L4 | closed | march | 110 | 13 | 0 | 110 | 110/110 | 0 | COVERED | 1654 | cdb511f9d5c8236b |
| U5_L9 | closed | march | 115 | 9 | 0 | 115 | 115/115 | 0 | COVERED | 880 | ce38410e971fd12d |
| U5_L16 | closed | march | 104 | 12 | 0 | 104 | 104/104 | 0 | COVERED | 758 | 9506cc9495bdc51e |
| U6_L8 | closed | march | 116 | 8 | 0 | 116 | 116/116 | 0 | COVERED | 852 | 52a77cf1faa91a1e |
| U6_L12 | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 65 | - |
| U7_L4 | closed | march | 110 | 13 | 0 | 110 | 110/110 | 0 | COVERED | 1230 | ab78504c950125ab |
| U7_L10 | closed | march | 114 | 10 | 0 | 114 | 114/114 | 0 | COVERED | 692 | 85dd99553b5e8990 |
| U7_L15 | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 43 | - |
| U8_L5 | closed | march | 116 | 8 | 0 | 116 | 116/116 | 0 | COVERED | 1049 | ad686cb712c638d7 |
| U8_L12 | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 37 | - |
| U9_L6 | closed | march | 115 | 9 | 0 | 115 | 115/115 | 0 | COVERED | 870 | e921f157188c0537 |
| U9_L13 | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 27 | - |
| U10_L2 | closed | march | 126 | 2 | 0 | 126 | 126/126 | 0 | COVERED | 1964 | c549f757d0feced1 |
| U10_L8 | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 58 | - |
| U10_L13 | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 25 | - |
| U11_L2 | closed | march | 117 | 5 | 0 | 117 | 117/117 | 0 | COVERED | 1826 | 03b22bf1df3d766f |
| U11_L8 | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 42 | - |
| U11_L13 | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 16 | - |
| U12_L4 | closed | march | 128 | 0 | 0 | 128 | 128/128 | 0 | COVERED | 1181 | 0fda9db64109c8ef |
| U12_L10 | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 22 | - |
| U13_L4 | closed | march | 128 | 0 | 0 | 128 | 128/128 | 0 | COVERED | 1149 | 99048f073a1a0d54 |
| U13_L8 | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 32 | - |
| U14_L5 | closed | march | 128 | 0 | 0 | 128 | 128/128 | 0 | COVERED | 968 | c70ddec9d2bfde53 |
| U14_L9 | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 24 | - |
| U15_L5 | closed | march | 128 | 0 | 0 | 128 | 128/128 | 0 | COVERED | 989 | 336e45e475e74f20 |
| U15_L11 | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 16 | - |
| U16_L6 | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 59 | - |
| U16_L10 | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 18 | - |
| U6_L14 | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 58 | - |
| U14_L4 | closed | march | 128 | 0 | 0 | 128 | 128/128 | 0 | COVERED | 1093 | bcbad23d405fb8cb |
| U_L2-8 | closed | march | 122 | 4 | 1 | 185 | 185/185 | 0 | COVERED | 3981 | 0ce62399349d1d72 |
| U8_L16 | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 29 | - |
| U_L4-16 | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 29 | - |
| U_L4-12 | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 36 | - |
| U6-13_L | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 19 | - |
| U15_L10 | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 17 | - |
| U12_L11 | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 19 | - |
| U13_L12 | closed | direct | - | - | 0 | 1 | 1/1 | 0 | COVERED | 15 | - |

`summary.json` holds the full per-case data, including the full top.icnf sha256 values.
