# C3AUDIT2 notes

- 04:39 UTC start; env.txt pushed.
- Re-derived Lemma H6M (PLAN.md 177-218) step by step: correct (see REPORT.md section 1).
- Base CNF WLOG: only `sb` (sigma_0 = 0), results/C3a/c3cnf.py:22,148.
- tools/mirror_h6_test.py (own exact Eisenstein-coordinate test, no repo imports): 14,000 H6 sets,
  68,234 layers, 0 failures; all mutations caught. Run: m=7 seed 11 (2000), m=9 seed 12 (2000),
  m=11 seeds 13, 14 (5000 each), 4 processes in parallel, under a minute.
- tools/check_kept.py: option-level counts and h6m_kept column: 293/293 and 588/588 agree.
