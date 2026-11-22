# Review of n66-l15-rows (independent reviewer, slot rv5, track ag)

Started 22 Nov 2026, 22:47 KST. Work directory (the only place this reviewer writes):
`/home/jay/research/data/formalize-20261122/n66-l15-rows/review`. Units: `esr-ag-rv5-<job>`, one at a time.
Nothing outside this directory is edited. Deliverable: `VERIFY_n66-l15-rows.md` (here).

## Plan (milestones)

| R | content | state |
|---|---|---|
| R0 | read the house rules, FORMAL README, LEAN_STATUS, worker README/DESIGN, n66-level15 and n66-rowsvalid reviews | done 22:47 |
| R1 | static checks (own code): source audit, own reverse-rename diff vs n66-rowsvalid, own parse of the RowsD* constants vs rows_used15.txt, chunk/just pairing, LEAN_PATH one-provider check, freshness, exe provenance (IR C vs olean), module-name clash check for the co-import | **done** 23:00 (all pass; own_rows15.json, own_fresh.json, own_diff_copies.txt) |
| R2 | ONE Lean compile (unit esr-ag-rv5-axioms, no -o): #check / #print of the statement pieces, own hand-unfolded restatement, kernel facts, own kernel negative control (positive form), #eval dump of R1_15 (COMPUTED cross-check), #print axioms | **done** 23:02 (lean_rc 0, 18 s, cgroup peak 816 MB; review_compile.log) |
| R3 | own E1 re-print of the cube trims with the frozen exe n66r15print (unit esr-ag-rv5-e1c), own leaf map, compare with trim.cnf and the recorded hashes; controls | **done** 23:12 (105/105 MATCH byte for byte, E2 records 105/105, controls 5/5 PASS; e1c_*) |
| R4 | own E1 re-print of certificates with the frozen exe r15rowprint (unit esr-ag-rv5-e1r), incl. T208 `st 208` | **done** 23:30 (628/628 byte-identical to VB's CNFs; T208 st = VB's trimmed CNF 349b6c6c; 4/4 controls) |
| R5 | own cake_lpr sample on certificates (unit esr-ag-rv5-cake), exact line grep, negative control | **done** 23:31 (13/13 certificates incl. T208 trimmed, 4/4 cube trims ACCEPT; 2/2 negative controls rejected) |
| R6 | write VERIFY_n66-l15-rows.md | **done** 23:39 |

## Status
- 22:47 started.
- 23:39 VERIFY file final (advisor's wording fixes: 56 axiom lines; supporting-theorem paragraph; not-re-run list; worker source manifest 148/148).
- 23:37 R4-R6 done. Verdict: statement faithful; label confirmed (Lean-checked modulo CubesUnsat105R and RowCertsUnsat under E1-E6); co-import compile not re-run (static check only).
- 23:12 R3 done: 105/105 trims byte-identical (own code), E2 record lines 105/105, 5/5 controls. R4 (unit e1r) running, then R5 (unit cake) via review/driver.sh.
- 23:02 R1, R2 done: all static checks pass; the one compile is rc 0 with standard axioms only; restatements accepted; both own kernel negative controls evaluate to false; #eval dump of R1_15 = rows_used15.txt.
