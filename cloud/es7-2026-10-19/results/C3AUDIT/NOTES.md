# C3AUDIT working notes (in progress)

- 00:44 UTC start. Tools built from source: CaDiCaL c6073042 (3.0.1), cake_lpr a36874a.
- Base CNF rebuilt (`gen_case.py 11 7 none`): header `p cnf 168399 4154921`, sha256 bf0e502e...dd6da. Matches.
- Re-check of 13 wave-1 certified nodes (`tools/recheck.py`, own unit generation, own CNF
  assembly, CaDiCaL --lrat, cake_lpr): 13/13 CNF sha256 equal to the record, 13/13 UNSAT, 13/13
  "s VERIFIED UNSAT" (`logs/recheck_wave1.jsonl`).
- Independent exact test (`tools/indep.py`, `tools/drive.py`) running.
