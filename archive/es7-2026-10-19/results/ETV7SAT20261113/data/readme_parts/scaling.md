Observations:
- **Top of the ladder (with rows, exactly N).** `--nosig`: N = 41 → 293,228 conflicts (227 s);
  N = 38 → 3,086,289 (1,279 s); N = 37 → @@N37@@. `--sigmax 1 --link`: N = 41 → 275,838 (397 s);
  N = 40 → 573,706 (685 s). So the signotope packets do not reduce the number of conflicts here, they
  only make each conflict more expensive (about 700 conflicts/s against 1,300–2,400), and the cost
  grows by a factor of about **2.2–2.9 per point** (41 → 38: ×10.5 in three steps; 38 → 37: ×2.9).
- **Near the threshold** the growth is steeper: in the 35-state catalog ×2.4 and ×3.8 for the last two
  steps (28 → 27 → 26), ×3.5 on average over the last four.
- **Extrapolation to N = 27** from N = 37: between 8.8 M × 2.2¹⁰ ≈ 2 × 10¹⁰ and 8.8 M × 3.5¹⁰ ≈ 2 × 10¹²
  conflicts. Below N = 37 the signotope-free model must become satisfiable somewhere (it is at N = 27,
  §7), so the geometric proof has to carry signotope packets, at 450–700 conflicts/s on one thread:
  roughly **1 to 170 CPU-years**, with an LRAT proof of about 15 TB to several PB at the measured
  0.7–2.7 kB per conflict. That is not a certificate anyone can check with cake_lpr.
  This is an extrapolation over 10 steps from 5 data points: HEURISTIC, the exponent is the whole
  uncertainty.
- The position-indexed encoder is worse: it does not solve the 35-state instance (n = 26) at all in
  16 minutes, and for hexagons its cost *increases* with the number of points (§4.1).

Conclusion: with the present model, ETV(7; 5, 7) = 26 needs a new idea, not more CPU. The rows S1–B2
only count; what is missing is structural information about near-extremal T (no 6-cup, 20–25 points)
and R (ends of 6-cups) and about their interaction (§11).
