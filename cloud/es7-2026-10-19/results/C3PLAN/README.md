# C3PLAN: what it would take to close the 3-fold class

Task: `TASK.md` (commit 3d83517), H = 1.25 h on one 4-core VM (`env.txt`), 2026-10-21 00:44–01:59 UTC.
Full answers with sources: `PLAN.md`.

- **Measured so far** (`stats.tsv`, `scripts/stats.py`; wave 1 + wave 2 records at the last pull):
  the closed / partial / untouched counts are in `PLAN.md` §1. No SAT anywhere. All of H6(1,0) is
  closed. The hard roots are the s = σ_a = 1 top cases, above all the one-orbit layer-2 roots there:
  none closed, up to 4,299 open nodes each, and 80/80 single-below-single depth-3 nodes timed out.
  Checking costs as much as solving.
- **Total cost with the current method** (`scripts/estimate.py`, `estimate.txt`): see `PLAN.md` §2.
  The mid value is about 3,000 core-h solve + check (about 1,010 machine-hours of the 4-core VMs at
  3 jobs). The range is 2,000–7,500 core-h unless the heaviest H3 Knuth walk is representative, in
  which case it is about 8.7·10^5. H3 has no wave data at all.
- **Cheaper:** (a) a mirror reduction below every H6 case (Lemma H6M, proof in `PLAN.md` §3a,
  0 failures on 3,900 exact-coordinate sets, `scripts/validate_mirror_h6.py`) keeps 81 of 153 layer-2
  options per H6 case and brings the mid value to about 1,900 core-h (range 1,200–5,100). (b) σ-cube splitting of
  timed-out nodes (`scripts/sigma_cubes.py`, `logs/sigma_cubes.jsonl`, every UNSAT checked by
  lrat-check E2 and cake_lpr): mixed, with 1 of 3 hard nodes closed at 16.6× less cost than its
  layer split and 2 of 3 left with open cubes. (c) Pre-splitting single-below-single nodes.
- **Next wave:** `PLAN.md` §4. First audit and implement H6M plus a σ-cube pilot, then close all
  s = 0 cases, an H3 pilot, then the s = 1 strata. The plan also states which results would show
  that the method cannot finish.
