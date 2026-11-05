# ROT45CHORD20261105: 5-fold and 4-fold threshold runs with the chord lemma (5 November 2026)

**Target.** These are the m-fold cases of ES(8) = 65 that `ROT456` left open. By the layer lemma, an m-fold symmetric
octagon-free set of at least 65 points contains t nested regular m-gons with t >= 13 (m = 5) or t >= 17 (m = 4).
UNSAT of `gen.py 5 8 13`, resp. `gen.py 4 8 17`, would settle these cases. Earlier runs of these formulas did not
finish: the 5-fold cubes reached about 50 million conflicts in 6.1 h each, and 4-fold was never attempted.

**What changed.** The chord lemma (`CHORD20261105`) adds clauses the encoder lacks:
- 882 new clauses for m = 5 (90 units, 396 binary, 396 ternary);
- 801 new clauses for m = 4 (321 units, 480 binary).

The lemma is a written proof. Every added clause was proved by an independent exact verifier (`CHORD20261105`
§6) and stress-tested.

## Setup (exact inputs; `logs/input_hashes.txt`)

| Instance | Base CNF (SHA-256) | Added clauses | Symmetry unit | Cubes |
|---|---|---|---|---|
| 5-fold, t = 13 (65 points) | `gen.py 5 8 13`, `d7bbb743…` (equals `ROT456`'s) | `chord_m5t13_new.clauses`, `b00bdc9a…` | H(1) = var 8803 (`C7UPPER` §2) | 24 total phase orders of layers 1–4 |
| 4-fold, t = 17 (68 points) | `gen.py 4 8 17`, `4843a9e9…` (equals `ROT456`'s) | `chord_m4t17_new.clauses`, `720ac526…` | Y(1,2) (`C6UPPER` §2) | 12 total orders with psi_1 < psi_2 |

- **Cube files** (`tools/mkcubes_chord.py`) are the base CNF, then the added clauses, then the symmetry unit and the
  six phase-order literals of one total order. The manifests are in `logs/`.
- **Cover.** The remaining sign patterns of Y(1,2), …, Y(3,4) (40 for m = 5, 20 for m = 4) violate transitivity.
  - First run (01:2x KST, `tools/implane.sh`): all 60 were solved UNSAT. That script's verdict was wrong: lrat-check
    is unsound (`LRATCHECK20261105`), and its grep also matched "c NOT VERIFIED". The script then deleted the CNFs
    and proofs. Its table is kept only as a record (`logs/imp_results_old_lratcheck_UNRELIABLE.tsv`).
  - Re-run at 13:0x KST (`tools/mkimpossible.py`, `tools/implane2.sh`): regenerated, solved, and checked by
    **cake_lpr**. CNF, LRAT, solver output, cake_lpr log and SHA-256 are kept for every pattern. Result:
    `logs/imp2_results.tsv`, with hashes in `logs/imp2_hashes/`: **60 of 60 UNSAT, every proof accepted by cake_lpr** (40 five-fold, 20 four-fold).
- **Solver.** CaDiCaL 2.1.3 with text LRAT (`tools/lane.sh`), one core per cube. `lane.sh` would have checked each
  UNSAT proof with lrat-check. That checker is unsound, and since 13:01 KST every proof is checked by cake_lpr (see
  the supervisor below).
- **Scheduling, 01:08–04:25 KST.** A memory-aware scheduler ran up to 30 lanes (`tools/sched*.sh`), with a guard
  against running out of memory (`tools/memguard.sh`). The original cutoff was 05:05.
- **Extension to 16:00 KST** (decided by the author at about 04:20). The lanes were not restarted.
  - Each original lane is `lane.sh -> timeout -> cadical`. Its `timeout` wrapper would have killed the solver at
    05:05.
  - **One lane was lost doing this.** The first attempt killed the wrapper of `cubes4/o1234` with SIGKILL. GNU
    `timeout` gives its child a parent-death signal, so the solver died too, after 3 h 20 min. It was not restarted;
    `logs/results_final_at_commit.tsv` records it as LOST-WRAPPER-KILL.
  - The other 29 wrappers were SIGSTOPped instead. A stopped `timeout` cannot act on its expired timer, and its child
    keeps running. The `lane.sh` parents were left alive and blocked, so no process group became orphaned. All 29
    solvers kept running with their proofs growing (checked).
  - Since 04:25 a detached supervisor (`tools/supervisor.py`, a systemd user service with `KillMode=process` and
    `Restart=on-failure`) manages the run:
    - it verifies each UNSAT proof (`tools/check_wrapper.sh`). In v1 the checker was lrat-check. **Since v2
      (13:01 KST) the verdict is cake_lpr's line "s VERIFIED UNSAT"**, and REJECTED and INTERRUPTED are told
      apart. It records SHA-256 of the CNF, LRAT, solver output and checker log;
    - it pauses the youngest solver under thermal stress (Tctl >= 95 C) or memory pressure, and resumes it afterwards;
    - it keeps at least 400 GB of disk free;
    - it starts the 6 never-started 5-fold cubes only when fewer than 30 solvers run;
    - at 16:00 it terminates unfinished solvers and checks, cleans up the stopped wrappers, records every cube once,
      and writes `final/final_report.md` in the work directory.
  - **Review and v2.** A read-only three-lens review (04:30–04:46 KST) found no defect that could signal a running
    solver. It did find these problems, all fixed in v2 (`tools/supervisor.py`):
    - the lrat-check unsoundness (critical);
    - a disk guard that could kill several solvers in one cycle (v2 pauses first and kills only below 400 GB, one
      per cycle);
    - a fragile cutoff file (v2 keeps the last good value, ignores an earlier value, and needs two consecutive cycles
      past the cutoff);
    - check failures recorded as final (v2 retries INTERRUPTED up to three times);
    - process matching not restricted to this directory (v2 requires cwd = the work directory);
    - no verification after the cutoff (v2 allows a 3-hour grace period for checks only);
    - unverified SAT answers (v2 checks every clause against the model).

    v2 was tested end to end on small real instances, then replaced v1 at 13:01 KST by restarting only the
    supervisor. The 30 solver PIDs were unchanged. User lingering was enabled (`loginctl enable-linger`).
  - **Timeline note.** The interactive session was paused for about 8 hours (04:46–12:59 KST). The detached
    supervisor and solvers ran on. In that time no cube finished, so no proof was checked by the unsound checker.

## Control: the chord lemma on a known-UNSAT instance (evidence, timing)

The `C6UPPER` 11-layer formula (`gen.py 6 8 11`, `542c8a3a…`, byte-identical) was used, with cube c11111. It was
solved on this machine without proofs, under the same load:

| version | result | time |
|---|---|---|
| base + cube (as in `C6UPPER`) | still running at commit time (7,200 s limit) | > 5,290 s |
| base + 642 new chord clauses + cube | UNSAT | 788 s |

## Results

**At the time of this commit (about 04:30 KST) no phase-order cube had finished.** None of the 36 cubes had
reported UNSAT or SAT. The cover's 60 transitivity patterns are refuted and checked (see Setup).
- Final per-cube outcomes are written automatically at 16:00 KST to `final/results_final.tsv` and
  `final/final_report.md` in the work directory (outside Git). They should be copied here and committed after review.
- **No 5-fold or 4-fold bound is claimed.** That needs every phase-order cube UNSAT with an accepted proof, all
  transitivity patterns refuted (done), and the written soundness obligations listed in the final report.
- `cubes4/o1234` was lost, so the 4-fold cover cannot be completed in this run unless that cube is re-run.
