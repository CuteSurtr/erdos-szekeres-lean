# v3: from-scratch acceptance check for mirror sub-case (ii) wave results

The wave VMs ran 36 separately modified copies of `close_march.py` (Haudit RISK-3), so their
"closed" claims are not accepted as they stand. A case closed by leaves is accepted only when:

1. every leaf, taken from the union of all shards' `leaves.icnf` files and parsed strictly,
   is re-solved from a CNF rebuilt here (F + the case cube + the leaf, case part pinned by the
   cnf_sha256 in `results/Mii-S/cases.jsonl`) and cake_lpr prints `s VERIFIED UNSAT`; and
2. the cover CNF {case cube units} + {not leaf} is UNSAT with a cake_lpr-verified proof.

- `v3_manifest.py ROOT OUT_MANIFEST OUT_CASES results/WAVE1 [more wave dirs]`: assigns every
  leaves directory to a case (case_sha256 in leaves.jsonl and the directory name must agree),
  rejects malformed lines, and numbers the distinct (case, leaf) pairs.
- `v3_check.py --root ROOT --base F.cnf --manifest M --shard I --nshards N --out OUT`:
  checks the leaves with idx = I mod N and the covers of the cases at position I mod N.
  Each job uses its own work directory. The run is resumable.

Not yet reviewed or tested by an independent agent.
