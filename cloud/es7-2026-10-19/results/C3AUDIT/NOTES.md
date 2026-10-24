# C3AUDIT working notes (in progress)

- 00:44 UTC start. Tools built from source: CaDiCaL c6073042 (3.0.1), cake_lpr a36874a.
- Base CNF rebuilt (`gen_case.py 11 7 none`): header `p cnf 168399 4154921`, sha256 bf0e502e...dd6da. Matches.
- Re-check of 13 wave-1 certified nodes (`tools/recheck.py`, own unit generation, own CNF
  assembly, CaDiCaL --lrat, cake_lpr): 13/13 CNF sha256 equal to the record, 13/13 UNSAT, 13/13
  "s VERIFIED UNSAT" (`logs/recheck_wave1.jsonl`).
- Independent exact test (`tools/indep.py`, `tools/drive.py`) running.
- Independent exact test: geo (units true under own canonicalization, all 2n frames of S and of
  its mirror) m=11: 300 sets, m=7: 300 sets, 0 failures, all 11 top cases hit. Full-CNF SAT
  test (base k=7 + node units + true T/sigma fixed must be SAT): m=4 100, m=5 150, m=6 120 sets
  in class, all SAT. Mutations: reversed 2-orbit order, no sigma swap, mirror without sigma
  flip, one flipped orientation orbit: all detected.
- Own cut check (`tools/mycompose.py`, own tree definition) over all wave-1/2 records: same
  answer as compose.py (24,445 certified, not covered, 6,591 frontier), 0 child-list mismatches
  on 417 prefix nodes.
- Symmetry reduction (results/WRITEUP/MIRROR.md §2) re-derived: correct.
