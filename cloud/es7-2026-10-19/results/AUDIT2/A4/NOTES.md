# AUDIT2 A4 working notes (verification pipeline)

Start 2026-10-21 00:33 UTC, budget 1.75 h. Branch es7-cloud, TASK.md at 852bee7.

## Reproductions (all match)
- F regenerated per results/V3Z/tools.txt: sha256 69c1dc8f…932d, header `p cnf 47002 515121`.
- Manifest rebuilt at Zf = 06c1f798c (old 14447d0d5) with verify/v3 at HEAD (no diff to 92746ac):
  M.jsonl sha256 e01af167…83b5 (73880 lines), C.jsonl sha256 3fff4486…4411 = results/V3Z/cases_final.jsonl.
- Record-file list at HEAD ff5a7a92 (find + grep '"kind"') is identical to results/V3Z/aggregate_inputs.txt (78 files).
- aggregate_final.py re-run at HEAD: output tsv and problems.txt byte-identical to accepted_final.tsv / problems.txt:
  278 of 278 accepted, 73880 of 73880 leaves, 0 SAT records, one NOTE (REJECTED U4_L record next to VERIFIED).

## Independent record audit (scripts/recaudit.py)
- All 450 cubes of cases.icnf rebuild to cases.jsonl cnf_sha256.
- Record shapes in the 78 files: only v3_check shapes (post BUG-1/BUG-2 fix: every leaf record has lits).
- Every VERIFIED leaf record (75459) has rc 20, cake_lpr exactly `s VERIFIED UNSAT`, proof_bytes > 0. No contradiction-shortcut leaf records.
- Every non-trivial cover record used (187 records, 140 cases) has rc 20, exact cake_lpr line, and cnf_sha256 equal to the cover CNF I rebuilt from cube + final manifest leaves.
- 190 trivial cover records ("the empty cube is a leaf"): all for the 138 cases whose leaf list is exactly [[]]; for these the empty leaf's CNF is the case CNF itself.
- 9 NOT_COVERED records (V3A) are all for older, smaller leaf sets (leaves_sha256 differs from final); expected.
- REJECTED U4_L record: rc 20, cake_lpr output empty (crash/OOM, 160 MB proof); another record VERIFIED.
- Haudit/t5_all172.jsonl: 172 distinct direct cases, exact cake line, cnf_sha256 = cases.jsonl; manifest cases = the 278 OPEN cases; disjoint, union = 450.

## Mutation tests of aggregate_final.py
- Manifest U12_L4 with one leaf dropped (127 leaves, real CaDiCaL: cover CNF SATISFIABLE) +
  (a) a forged cover record with the "empty cube is a leaf" note, or (b) a cover record with cnf_sha256 = 0…0 and cake_lpr "":
  aggregate_final.py prints "accepted 1". The aggregate trusts cover records' verdict field; it does not re-derive the cover CNF hash, the cake_lpr line, or the empty-leaf condition. (Real data checked above: no such record is used.)
