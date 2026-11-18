# Preserved non-results and process failures

- The 400 seeded m16 samples of the ETV42 fixture all had repair cost zero
  at every root. They do not support a universal theorem. Inputs and every
  exact outcome are retained in scratch (`samples8*`).
- The coarse rational rotation probe tested 196 distinct order/reflection
  cases; only 23 were (5,7)-valid. All outcomes, including forbidden-cap or
  collinearity rejections, are retained in scratch (`rotations*`).
- The simple integer projections tested 368 cases; 13 were (5,7)-valid.
  All outcomes are retained in scratch (`simple-projections*`).
- The two-clone n8 probe tested 2,205 geometries; 466 were (5,8)-valid.
  All rejected geometries and their exact rejection counts remain in scratch
  (`two-clones-n8*`). A rejected candidate is never used as a valid fixture.
- One diagnostic attempted to read `rightmost-n8-audit.json` while its bounded
  producer was still running, and exited with FileNotFoundError. The check
  itself completed normally afterwards. That diagnostic produced only n7
  information and no n8 claim. No timeout or OOM occurred.
- The initial C++ compilation emitted a misleading-indentation warning in
  the output-only `ids` function. The compiled logic is unchanged by that
  formatting issue; the original compilation log is preserved.

No finder UNSAT result or incomplete proof is used; no SAT solver has been
run by this track.
