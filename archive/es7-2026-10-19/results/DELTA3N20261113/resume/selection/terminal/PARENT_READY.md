# Frozen 18-point terminal-selection packet ready

**Final update:** the parent independently confirmed the geometry, full CNF,
core and all-X witness in `../data/parent_obstructions.json`. Its fresh
core proof is now accepted by cake_lpr (`s VERIFIED UNSAT`); see
`data/certification/result.json`. The pending-certificate wording below is
the original handoff, preserved to distinguish finder and certification.
All probes have stopped; the input packet and its hashes are unchanged.

**COMPUTED real n=7 counterexample to terminal-rank selection.** Zero of
262,144 colorings satisfy the stronger condition. No LRAT certificate has
been claimed by this track. The parent can freshly certify either CNF below.

- `data/witness.core.cnf`: 18 variables, **108 clauses** (35 negative
  rank-three cap triples, 73 positive whole hexagons).
  SHA-256 `5318a34178cd3aa6acb9f83de54f4e9510b0a968a98fc0c8eb40b20ce135d0dd`.
- `data/witness.terminal.cnf`: 18 variables, 736 clauses (115 four-caps,
  219 rank-three cap triples, 402 hexagons).
  SHA-256 `bdcd89c25dc74e94f576f6dfcc0548e6849a67d441fec5956698296a83bfc2eb`.
- `data/core.json` gives every actual core triple/polygon and source clause
  index; the core is a checked subformula of the full coordinate formula.
- `data/witness.json` gives all coordinates, n, source hash/index mapping,
  and the actual ordinary weak Delta **A={0,5,6,7,8}**.
- `data/exact_check.json`: no five-cap or heptagon; complete hull/chain
  clause comparison; 8,149 ordinary weak Deltas, no terminal-safe Delta.
- `data/deletion_controls.json`: all 18 single-point deletions admit a
  checked terminal-safe Delta. This is not global size-minimality.

**The weaker envelope criterion holds here for all X>xmax.** Precisely
4,057 weak Deltas satisfy it on the entire half-line, including the same A.
Its only cap triples are (0,5,6) and (0,5,7), both of terminal rank three.
Both terminal lines are strictly below the line of ambient four-cap
(6,7,14,17) for every X>=758070: their margins at 758070 and the slope
differences are positive exact rationals in `data/all_X_direct_proof.json`.
`data/witness.envelope.json` also gives exhaustive counts and representative-X
checks. Thus this failure does not refute favorable envelope selection.

Consequently this U cannot yield the parent's proposed rooted obstruction:
for every rightmost r preserving five-cap-freeness, A+r is a weak Delta.
This holds regardless of whether U+r satisfies the no-heptagon premise.
No extensive rooted cell scan is needed for this fixture.

Proof still needed for CERTIFIED: fresh parent CaDiCaL LRAT, retained proof,
and cake_lpr's literal `s VERIFIED UNSAT`, with hashes, plus a separate
coordinate/clause audit. `SOUNDNESS.md` supplies the written encoder argument.
All scratch trajectories and negative/invalid pool cases are preserved.
