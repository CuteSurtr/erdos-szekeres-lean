# AUDIT2 A4 report: the sub-case (ii) verification pipeline

Auditor A4, 2026-10-21 00:33–01:15 UTC, budget 1.75 h, 4 cores / 15 GB (`env.txt`). Branch es7-cloud,
TASK.md at 852bee7, branch head during the audit ff5a7a92. Reviewed `verify/v3/` (no diff between
92746ac = old bdf319c and HEAD), `results/V3Z/scripts/aggregate_final.py`, and the 78 record files it reads.

## Verdict
I found nothing that breaks the claim. Re-running the aggregation gives the same result: 278 of
278 wave cases accepted, 73,880 of 73,880 leaves, and no SAT record. Every record it relies on is
internally consistent. I re-solved and re-checked 98 leaves and 15 covers from scratch, and all of
them came back `s VERIFIED UNSAT` with the recorded CNF sha256. There are two findings about the
trust base. Neither affects the recorded data.

## Findings (most serious first)

1. **aggregate_final.py does not re-derive cover records, it trusts their `verdict` field.** Weakens the trust base. Not exploited by the data.
   `results/V3Z/scripts/aggregate_final.py:45-46,71-73` keys cover records by (case, leaves_sha256) and accepts if all of them say `VERIFIED`. It never checks the record's `cnf_sha256` against the cover CNF (cube units + negated manifest leaves). It never checks `rc == 20` or `cake_lpr == "s VERIFIED UNSAT"`. For a record carrying the note "the empty cube is a leaf", it never checks that the manifest leaf list really contains `[]`. Leaf records get the CNF sha check (`:98-104`) but also no `cake_lpr`/`rc` check (`:88`).
   Evidence (mutation test, `NOTES.md`): I dropped one leaf from case U_L12-free example U12_L4 (127 of 128 leaves; real CaDiCaL says this cover CNF is SATISFIABLE). Then I added (a) a cover record with the empty-cube note, or (b) a cover record with `cnf_sha256` = 0…0 and `cake_lpr` = "". In both cases aggregate_final.py printed `cases 1 accepted 1`.
   Why the claim still holds: `v3_check.py:143-160` only writes these records honestly (VERIFIED iff the exact line; the note only when an empty leaf exists). I checked every record the acceptance uses (`scripts/recaudit.py`):
   - all 187 non-trivial cover records for the final leaf sets have rc 20, the exact line, and a cnf_sha256 equal to the cover CNF I rebuilt;
   - all 190 note-trivial cover records belong to the 138 cases whose leaf list is exactly `[[]]`;
   - all 75,459 VERIFIED leaf records have rc 20, the exact line and proof_bytes > 0.
   Suggested fix (not applied): in the aggregate, recompute the cover CNF sha and require it, require the exact `cake_lpr` line and rc 20 for leaves and covers, and accept the note only if `[]` is among the leaves.

2. **aggregate_final.py does not pin F or the case cubes.** Cosmetic.
   `:21-27` reads F from the path it is given without checking sha256 69c1dc8f…, and zips cases.jsonl with cases.icnf without checking the count or `cnf_sha256`. A wrong F or a wrong cube can only make leaf shas mismatch, because v3_check pinned both, so the risk is non-acceptance, not false acceptance. I checked separately that all 450 cubes rebuild to `cases.jsonl` cnf_sha256, and that cases.icnf/cases.jsonl have not changed since their first commit (99ba29fa).

3. **Minor observations.** Cosmetic or liveness only.
   - `v3_check.py:112-114` ignores cake_lpr's exit code and stderr. The single REJECTED record, U4_L in `results/V3A/V07/out.jsonl` (rc 20, 160 MB proof, empty cake_lpr output, probably out of memory), has no diagnostic. The same leaf has a separate VERIFIED record.
   - cake_lpr has no timeout (V3T RISK-2).
   - `summary.md` / `tools.txt` cite pre-rewrite hashes (bdf319c, 14447d0d5, ff29bc68). They translate via COMMIT_MAP to 92746ac, 06c1f798c and 569b763f.

## Checked and found sound
- **F**: regenerated per `results/V3Z/tools.txt`. sha256 69c1dc8f…932d, `p cnf 47002 515121`.
- **Manifest**: rebuilt at Zf 06c1f798c with v3_jsonl_leaves.py + v3_manifest.py. `M.jsonl` sha256 e01af167…83b5 (73,880 lines) equals READY.json. `C.jsonl` is byte-identical to `results/V3Z/cases_final.jsonl`.
- **Aggregate re-run at HEAD**: the record-file list equals `aggregate_inputs.txt` (78 files). The output TSV and problem list are byte-identical to `accepted_final.tsv` and `problems.txt` (`aggregate_rerun_problems.txt`).
- **Leaf CNF construction** (`v3_check.py:122-136`): the F body is unchanged, the header is `nv`, `nc + |cube| + |extra|`, and the units are cube literals sorted by |lit|, then the extra leaf literals. The aggregate rebuilds the same bytes and requires equality. My own independent builder (`scripts/spot.py`) gives the same sha for all 98 sampled leaves.
- **The case cube is pinned** against cases.jsonl `cnf_sha256` before any job (`:60-69`). The contradiction shortcut (`:125-128`) is sound, but no used record takes it.
- **Verdict parsing**: VERIFIED only if the first stdout line starting with `s ` is exactly `s VERIFIED UNSAT`, and cake_lpr runs only after CaDiCaL exits 20. V3T mutations M4 cover the stub cases.
- **Resume keys and sharding**: keyed by (kind, idx, case, lits) and (cover, case, leaves_sha256). The aggregate joins by content (case, lits) and recomputed leaves_sha256, so idx, shard and resume state cannot attach a verdict to the wrong leaf. Every record in the 78 files has the post-BUG-1/BUG-2 shape (leaf records carry lits). V3T used f3b07a7/bdf319c, V3A used 7c6d70c, V3B–V3E used bdf319c, all after both fixes.
- **Duplicates**: the manifest dedupes per case by literal set. Several records per leaf are allowed, and a SAT record would block. There are no SAT records anywhere, and no SAT status in any wave leaves.jsonl.
- **Covers**: cube units + {¬leaf}; F is omitted, which makes the requirement stronger. The 9 NOT_COVERED records (V3A) are for older, smaller leaf sets, and none matches a final leaves_sha256.
- **Empty-cube covers**: the 138 cases with leaf list `[[]]`. Each empty leaf's CNF is the case CNF itself, verified with sha = cases.jsonl `cnf_sha256`. The trivial cover is sound.
- **Directory-to-case assignment and v3_jsonl_leaves.py**: neither can cause false acceptance. A leaf assigned to the wrong case is checked against that case's cube, and the cover is over exactly the leaves required. Acceptance depends only on F, cases.icnf and the records, whatever the manifest's provenance.
- **Totals**: the 278 manifest cases are exactly the OPEN cases of cases.jsonl. `results/Haudit/t5_all172.jsonl` has 172 distinct direct cases with the exact line and cnf_sha256 = cases.jsonl. The two sets are disjoint and their union is all 450.
- **Independent re-solve** (CaDiCaL 3.0.1 c6073042 and cake_lpr a36874a8, built here, own scripts, not v3 code; `spot1.jsonl`, `spot2.jsonl`):
  - 98 leaves: 26 U_L2, 20 U3_L, 16 U_L7 (18 of them with recorded solve time 90–224 s), 26 from other cases, and 10 empty-leaf cases;
  - 15 covers, including U_L2 (22,529 leaves), U3_L (11,744) and U_L7 (3,759).
  All of them: rc 20, `s VERIFIED UNSAT`, and a CNF sha256 equal to the V3 record.

## Not checked
- I re-solved only a sample. The other records are trusted as honest outputs of v3_check.py. The records cannot prove that a solver ran; the cnf_sha256 field shows consistency, not execution.
- I did not check the 122 split obligations, the soundness of the encoding, or the Lean side. Those are A1–A3 and A6.
