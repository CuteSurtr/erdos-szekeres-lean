# Task Mii-0: shard 0 of 8, mirror-symmetric 33-point heptagon-free instance, sub-case (ii)

Run of 20 Oct 2026, 02:36–06:16 UTC. **Shard not finished**: 8 of 16 shard cubes are fully
closed, 58.6 % of the shard's weight is closed, and 487 leaves are still open. No SAT leaf
was found. Nothing here is a theorem or a counterexample.

## Where it ran

One cloud container (`env.txt`): 4 vCPUs, 15 GB RAM, Linux 6.18 x86_64, used only by this
task. The container restarted once at about 03:05 UTC. The driver resumed from
`leaves.jsonl`, and only the leaves that were in flight at the restart were re-run
(`logs/run_events.log`).

Tools, built from source (`logs/tool_commits.txt`):

| tool | git commit |
|---|---|
| CaDiCaL 3.0.1 | c60730422e758ef1cebe7aeddf2dda31c996bf04 |
| drat-trim / lrat-check | 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 |
| CnC / march_cu (`make CFLAGS='-O3 -fcommon'`) | 705b60c6491ef2b61988b3ce6ac674be1b90571d |
| cake_lpr (CakeML-verified LRAT checker) | a36874a8b750b43fe4b385b8ddbf5b033e46a3fa |

## CNF

`results/C/scripts/make_cnfs.sh` regenerated every CNF (`logs/make_cnfs.log`, hashes in
`logs/cnf_sha256.txt`).

* `m33k7int.sub.cnf`: 47,002 vars, 515,121 clauses, 2,736 orbit representatives. These
  counts match `results/C/README.md`.
* sha256 `69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d`.
* `results/C` and `results/C2` record no sha256 for this file, so there was nothing to
  compare it with there. It is identical to the sha256 recorded by the sibling shards
  Mii-1…7 that had pushed their `logs/cnf_sha256.txt` by 02:45 UTC.

Validation and controls (`logs/part1_validate_report.json`, `logs/part1_controls.log`)
**passed**. The numbers are identical to C's:

* A1–A4: 1000/1000, 500/500, 200/200 and 100/100; minimum number of 7-gons 25,411.
* Small-k equivalence: 2000/2000 on all rows.
* k = 5 and k = 6 controls: m8k5 is SAT; the m9k5 and m17k6 families are UNSAT, each with
  an LRAT proof that lrat-check verified.
* Positive control: m32k7 and m32k7.sub are SAT under the orientations of the classical
  mirror-symmetric 32-point set.

The encoding itself is still unverified (critique item 4).

## Shard definition (unchanged)

* `march_cu m33k7int.sub.cnf -d 7 -o cubes.icnf` ran in 205 s (`logs/march_d7.log`).
* It produced **128 cubes, 0 refuted leaves**, all of depth 7. The cubes form a complete
  binary partition of the root (checked).
* `cubes.icnf` sha256 `cb32d049e5e4249fd5b57c3ca900feb602ff444fde0873c3fe296fbaaacc8244`
  (`logs/cubes.icnf`). This matches the hash in the other shards' `cubes_sha256.txt` that
  had been pushed.
* Shard 0 is the 16 cubes with line index i ≡ 0 (mod 8): `logs/shard0_cubes.icnf`.

## Method (`shard_run.py`, 4 parallel workers)

* Each leaf is the CNF plus its cube literals as unit clauses, solved from scratch with
  `cadical -q -t 300 --lrat --binary=false`.
* A leaf that runs past 300 s is split with `march_cu -d 6` on CNF + cube. The children are
  the emitted sub-cubes plus any sub-cubes that march_cu refuted itself. The refuted ones
  are rebuilt as the missing siblings in the cube tree, so the children partition the
  parent exactly; this was checked at every split. Every split here emitted 64 cubes and
  refuted 0.
* `leaves.jsonl` holds one record per finished leaf: cube, status, solve time, proof size,
  checker outputs and times, and children for splits. It is also the resume state.
* **LRAT checking.** Task E2 found that stock `lrat-check` (commit 2e3b2dc) accepts an
  empty clause that comes with no hints (`results/E2/logs/lrat_check_soundness.md`). I
  reproduced this (`logs/checker_controls.log`). So every UNSAT proof was checked three
  ways:
  * stock lrat-check;
  * lrat-check with `results/E2/tools/lrat-check-E2.patch` applied;
  * cake_lpr.

  A leaf counts as `lrat_verified` only when the patched lrat-check and cake_lpr both
  accept it. Both reject the bogus control proof; stock lrat-check accepts it. Proofs were
  deleted after checking.
* `decode_verify.py` decodes a SAT model and checks by brute force: the signotope axioms,
  mirror consistency, that the axis point is interior, and convex 7-gons (a DFS pruned by
  4-point convexity). It was tested against the exact `cgon` counter on two random mirror
  sets, with exact agreement (`logs/decode_verify_test.log`). It was never needed, because
  no leaf was SAT.

## Results (`logs/summary.json`)

| | count |
|---|---|
| shard cubes | 16 |
| shard cubes closed at depth 7 without splitting | 1 (index 48, 45 s) |
| splits | 16 (15 at depth 7, 1 at depth 13) |
| UNSAT leaves | 537 |
| UNSAT leaves accepted by patched lrat-check **and** cake_lpr | **537 / 537** (stock lrat-check also 537) |
| SAT leaves | **0** |
| open (unsolved) leaves | 487 (`logs/open_leaves.icnf`) |
| shard cubes fully closed | 8 / 16: indices 0, 8, 16, 24, 32, 40, 48, 64 |
| partially closed | index 56: 63/64 (one depth-13 child timed out and was split; its 64 depth-19 children are open); index 72: 25/64 |
| not started below the split | indices 80, 88, 96, 104, 112, 120 (64 open children each) |
| closed weight | 75/128 of the shard = 75/1024 of the whole instance; open 53/1024 |

* Depth-13 leaves took a mean of 58 s to solve (maximum 212 s), plus about 8 s of checking.
* Text proofs were 73 MB on average and at most 200 MB.
* Each march_cu -d 6 split cost 4–10 min.
* At the observed rate of about 2.5 leaves per minute, the 487 open leaves need about
  3–4 more hours on this machine. That assumes no further timeouts.

## Status

**The shard is not closed.** For the 8 closed shard cubes, the claim is: "CNF
`m33k7int.sub.cnf` + cube is UNSAT", with every leaf below the cube checked by the
patched lrat-check and by cake_lpr, and the leaves forming an exact partition of the
cube. That is a claim about this CNF only. The encoding is not formally verified, so it is
not a theorem.

To resume: rerun `shard_run.py` with the same arguments, pointing it at this
`leaves.jsonl` (finished leaves are skipped).
