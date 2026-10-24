# FIX1: hardened acceptance scripts and 3-fold drivers

Task `TASK.md` with H = 2.0 and Z = 640a56c2. Run on 2026-10-21 from 04:39 UTC, on one 4-core
15 GB VM (`env.txt`). Branch es7-cloud. Tools were built here:
- CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04;
- cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`; the bundled example
  prints `s VERIFIED UNSAT`);
- lrat-check from drat-trim 2e3b2dc with `results/E2/tools/lrat-check-E2.patch`.

None of the fixes changes a result. The v2 acceptance accepts exactly what V3Z accepted, and
the new `compose.py` gives the same counts on every 3-fold record. The fixes close the holes
that let forged or malformed records pass.

## 1. Mirror acceptance: `aggregate_final_v2.py` (AUDIT2/A4 findings 1 and 2)

It is a copy of `results/V3Z/scripts/aggregate_final.py`. All the changes are extra checks, and
they are listed in its docstring:
- **(v2-1) Pinned inputs.** F must have sha256 `69c1dc8f…932d`. `results/Mii-S/cases.jsonl` must
  have sha256 `5b58b4c6…5225` and `cases.icnf` must have `6b6f0946…b742`, with 450 lines each. All
  450 case CNFs (F + cube units, built as `verify/v3/v3_check.py` at 92746ac builds them) must hash
  to that case's `cnf_sha256`. Otherwise the script prints `FATAL …` and exits 2.
- **(v2-2) Leaf records.** A leaf record is used only if it has verdict VERIFIED, `rc == 20`,
  `cake_lpr` exactly `s VERIFIED UNSAT`, and a `cnf_sha256` equal to the leaf CNF rebuilt here.
  A leaf whose literals contradict its case cube is accepted without a record, because its CNF
  has x and −x as units. The script counts such leaves; there are 0.
- **(v2-3) Cover records.** The script rebuilds the cover CNF exactly as v3_check `cover_job`
  writes it: the cube units, then one clause ¬leaf per manifest leaf, with header
  `p cnf max(nv, |lit|) N`. A VERIFIED cover record must then have the right `nleaves`, `rc == 20`,
  the exact line, and that `cnf_sha256`. The alternative is the note "the empty cube is a leaf",
  and it is accepted only when the manifest's leaf list for that case is exactly `[[]]`. As
  before, every cover record for (case, leaves_sha256) must be VERIFIED, and in v2 each one must
  also pass this test.

**Run at the branch head** (`scripts/run_agg_v2.sh`). The inputs are the 78 files of
`results/V3Z/aggregate_inputs.txt`. The same `find` at the head gives the same list. F was
regenerated (sha256 69c1dc8f…, matches). M.jsonl was rebuilt at Zf 06c1f798c (pre-rewrite
14447d0d) with the jtrees under ROOT, as in `results/V3Z/inputs.txt`: sha256 e01af167…83b5 and
73,880 lines, both equal READY.json. C.jsonl equals `cases_final.jsonl`.
- **v2: 278 of 278 cases accepted, 73,880 of 73,880 leaves, 0 SAT records, 0 contradiction
  leaves** (`agg/problems_v2.txt`). `agg/accepted_v2.tsv` is **byte-identical to
  `results/V3Z/accepted_final.tsv`**. The only listed item is the known NOTE, a REJECTED U4_L
  record next to a VERIFIED one. So every leaf and cover record that the acceptance relies on
  passes the stricter tests.
- The old script, run again at the head, gives output byte-identical to `accepted_final.tsv` and
  `problems.txt`.

**Mutation tests** (`scripts/mutate_agg.py` → `agg/mutation.txt`). Case U12_L4 has 128 leaves.
With the last leaf dropped, real CaDiCaL says the cover CNF is **SATISFIABLE**.

| test | old | v2 |
|---|---|---|
| control: real U12_L4 manifest and records | accepted 1 | accepted 1 |
| **A4 (a)**: leaf dropped + forged cover with the empty-cube note | **accepted 1** | accepted 0: note but leaf list not `[[]]` |
| **A4 (b)**: leaf dropped + forged cover, cnf_sha256 0…0, cake_lpr "" | **accepted 1** | accepted 0: cake_lpr '' |
| (c) leaf dropped + forged cover with the right cnf_sha256 but cake_lpr "" | accepted 1 | accepted 0 |
| (d) leaf dropped + forged cover with right sha and line but rc 10 | accepted 1 | accepted 0: rc 10 |
| (f) every record of one leaf with cake_lpr "" (verdict still VERIFIED) | accepted 1 | accepted 0, leaf not verified |
| (f') the same with rc 10 | accepted 1 | accepted 0 |
| (g) F with one extra clause | accepted 0 (sha mismatches) | FATAL, exit 2 (F sha256) |

v2 rejects both of A4's mutations, and the four extra ones.

## 2. 3-fold tools: `results/C3T/tools` (C3AUDIT findings 1, 2 and 4)

The details and all test outputs are in `results/C3T/README.md`. In short:
- **close_node / close_tree.** Every solve record now has `proof_sha256` (the LRAT file the
  checkers read, hashed before it is deleted) and `cadical_args`. No other field changed.
  - The small instances were m = 5, 6, 7 with k = 5, 6: 116 certified nodes, including a
    `close_tree` run that splits. Old and new certify the same nodes with the same `cnf_sha256`,
    and every old field agrees.
  - Two new runs give the same `proof_sha256` on all 116.
  - At m = 11, 3 wave-2 nodes were re-solved twice. Their `cnf_sha256` equals the wave records,
    their `proof_bytes` equals the wave records to the byte, and the two `proof_sha256` agree.
- **compose.py.**
  - It pins BASE `bf0e502e…dd6da` and every record's `base_sha256`.
  - Its checks are explicit and survive `python3 -O`. The old script accepted a wrong
    `cnf_sha256` under `-O`, and a wrong `base_sha256` always; the new one rejects both.
  - It sha-checks every certified record.
  - It reports `certified_with_proof_sha256` (0 of 42,602 for the existing waves, as expected).
  - It rejects a wrong base and a record with a wrong `cnf_sha256`.
  - On all 3-fold records of C3WAVE1, C3WAVE2 and C3S0 it gives the same counts as the old
    script: 42,599 certified nodes, not covered, 7,453 frontier nodes (41,750 and 7,717 for the
    `out.jsonl` files alone). All 42,602 certified records match their re-derived CNF sha256.
- **--mirror-h6.** It is in `tree_children` and `compose.py`, off by default and unused by any
  driver. Tests show that with it off the tree is identical to C3-S. With it on, φ matches
  PLAN.md §3a: an involution that keeps 81 of 153 options per H6 case. **Do not use it until
  `results/C3AUDIT2` accepts Lemma H6M.**
- **Node names.** The comments in the copy now give `0s0`, `0s0-2s1`, `0s0_5` and `0s0_3s0-7s1`.

**Future waves should use `results/C3T/tools` at commit ff9b09ee**, the last commit that
changes `tools/`.

## Not fixed
- `results/C3-S/README.md:105` still has the old names. The file is outside this task's
  directories, so it was not edited; the correction is in `results/C3T/README.md`.
- The proofs of the 42,602 existing 3-fold records are gone, and those records carry no
  `proof_sha256`. Re-solving is still the only audit path for them. Test 3 in C3T shows that it
  reproduces the proofs byte for byte.
- `v3_check.py` itself is unchanged, because the task asked only for the aggregate. It still
  ignores cake_lpr's exit code and stderr, and has no cake_lpr timeout (A4 finding 3). v2 makes
  the acceptance independent of the records' `verdict` field.
- The old `compose.py` with its sha check (one full 70 MB hash per node) was run on the same
  records split into 4 file shards: all exit 0, 42,602 certified nodes sha-checked
  (`results/C3T/tests/logs/compose_old_setB_shard*.txt`). Its counts on the whole set were taken
  with `--no-sha` and agree with the new script.

Finished 2026-10-21 about 05:27 UTC, well inside the 2.0 h budget.
