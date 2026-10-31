# W25 — wave 1, mirror sub-case (ii), entry kind "cases": U3_L, U_L16, U16_L

**Result: all three cases are still OPEN.** No SAT. Every UNSAT leaf was checked with cake_lpr and
got `s VERIFIED UNSAT`; drat-trim's lrat-check was not used.

## Where it ran
One cloud VM, 4 cores, 15 GB RAM (`env.txt`), 2026-10-20 06:56–10:56 UTC. Solver run 06:59–10:25 UTC.
Tools, their commits and the sha256 checks are in `checks.txt`:
- cadical c6073042 (3.0.1);
- march_cu at CnC 705b60c6, built with -fcommon;
- cake_lpr a36874a8 (bundled example prints `s VERIFIED UNSAT`).

## sha256 checks (all match)
- regenerated base `m33k7int.sub.cnf`: 69c1dc8f…932d;
- `verify/ii_wave1.json`: 6df36dab…c72e;
- case CNFs from `hullsplit.py case`: U3_L 7ab00d97…f823, U_L16 edd50c27…c9a, U16_L 49f74507…5ab4.

## Method
`close_w25.py` is a modified copy of `results/Mii-S/scripts/close_march.py`; the original is kept here as
`close_march.orig.py`. The changes:
- The three cases share one pool of 4 workers, served in the listed order.
- Each case first gets plain `cadical -t 60`.
- After that it follows the close_march recipe: march_cu -d 7 top cubes, then `cadical --lrat -t 300`, a march_cu -d 6 split on timeout, and cake_lpr on every UNSAT.
- It is resumable. SPLIT records carry their children in `subs`, and the top cubes are in `top.icnf`.
- A cube not started before the 10:25 deadline stays open.

`finalize.py` rebuilds `leaves.icnf` (only cake_lpr-verified leaves) and `open.icnf` from `leaves.jsonl` + `top.icnf`.

Run note: the run first wrote its records inside the repo. A `git pull --rebase --autostash` replaced those
files on disk, while the running process kept writing to the old, deleted files. The records were then copied out
of /proc every 60 s. The last minute before exit was lost: 10 leaves verified in that minute have no record,
so they are **not** counted and remain in open.icnf. Restarts should use an OUTROOT outside the git checkout.

## Per case
| case | plain 60 s | top cubes (march -d 7) | top.icnf sha256 | verified leaves | splits | open cubes | cake_lpr | CPU h |
|---|---|---|---|---|---|---|---|---|
| U3_L | UNKNOWN | 128, 0 refuted (258 s) | efac91c0d58cf4f8f1b160c32198ef0e642965c026a834944716c9cdb1da4d23 | 530 (60 top + 470 sub) | 70 (68 top, 2 depth-13) | 4008 | 530/530 VERIFIED | 13.32 |
| U_L16 | UNKNOWN | 128, 0 refuted (447 s) | b2e212791eb528a06ae00791a40c8f25e2e8dc4504a6f88c148e189ed7ef948d | 0 | 0 | 128 | — | 0.14 |
| U16_L | UNKNOWN | 128, 0 refuted (319 s) | 21faf15aa62d83c5c45a7d82a38cb9ae1469967e3547140533236b9de05dfd07 | 0 | 0 | 128 | — | 0.11 |

`covercheck.py` results:
- each top.icnf: COVERED;
- each leaves.icnf alone: NOT COVERED, as expected for an open case;
- leaves.icnf + open.icnf: COVERED (U3_L 4538 cubes, U_L16 and U16_L 128 each).

So open.icnf is exactly what remains of each case.

Cost observations for U3_L:
- 60 of the 128 top cubes closed, in about 150–200 s each with proofs up to 222 MB.
- 68 top cubes timed out at 300 s. Each was split into 64 children (about 85 s of march_cu).
- The children close in about 20 s each, plus about 3 s for cake_lpr.
- Remaining work: about 3,950 children at about 23 s each, roughly 25 core-h. The est_core_h of 12.7 for this machine was far too low.

U_L16 and U16_L only got their plain try and their top cubes, because U3_L was first in the order.

## Resume
`close_w25.py OUTROOT U3_L=... U_L16=... U16_L=...` with the leaves.jsonl/top.icnf from here copied into
OUTROOT/<case>/ re-queues exactly the cubes in open.icnf.
