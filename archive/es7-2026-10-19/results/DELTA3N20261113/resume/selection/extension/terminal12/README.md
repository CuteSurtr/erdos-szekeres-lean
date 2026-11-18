# A twelve-point terminal-safe obstruction at n=6

**CERTIFIED finite components and independently audited; PROVED minimum
deduction: the global minimum for terminal-safe n6 failure is exactly 12.**
Removing original indices
4,11,13 from the balanced fifteen-point example gives a real set with no
five-cap and no convex hexagon, but no terminal-safe weak Delta for n=6.
It still has 945 ordinary weak Deltas, so weak D(5,6) is not refuted.
Every admissible set of size at most 11 has a terminal-safe Delta. The
explicit through-nine theorem and separate size-ten and size-eleven
certificates establish the lower bound without assuming monotonicity.
The complete independent audit is
[VERIFY_TERMINAL12.md](../terminal12_audit/VERIFY_TERMINAL12.md).

The twelve points, now indexed locally from 0 through 11, are

```text
(0,0), (37,-35), (38,-248), (84,-270), (472,-427),
(653,-757), (665,-793), (666,-717), (683,-718),
(736,-567), (926,-895), (1000,0).
```

There are 14 four-caps, 44 terminal-unprotected cap triples, and 134
convex pentagons. Maximum cap, cup and polygon sizes are 4,5,5. Complete
enumeration of all 4096 selections finds zero terminal-safe Deltas.
Ordinary weak Deltas have minimum size four.

The [192-clause formula](data/3/terminal.cnf) has SHA-256
`25ca75a9eee359ca03ae7f96657128ab03693c03421b1e7e83627f529841890a`.
Its fresh retained [binary LRAT](data/3/certificate/proof.blrat) is
accepted by cake_lpr with exactly `s VERIFIED UNSAT` in
[the log](data/3/certificate/cake.log). Commands and all artifact hashes
are in [the certificate receipt](data/3/certificate/result.json).

[descend15.py](../descend15.py) checked the complements of all four
three-point ordinary Deltas of the fifteen-point example. Each complement
has twelve points and no hexagon. Their terminal-safe selection counts
are respectively 68,28,2,0; only the last one is an obstruction. The
other three are retained as positive controls in this record.

The earlier C++ fixed-geometry encoder independently reconstructed the
negative example using chain dynamic programming and pair-terminal ranks.
Its entire membership clause multiset agrees with the parent's direct
integer-hull enumeration; see [cross-check.json](cross-check.json).
This agreement is separate from the completed worker audit, which
reconstructed all 192 clauses and checked all 4096 memberships, using
exact triangle containment rather than the parent's hull code. It also
reconstructed all generic size-ten/eleven clauses and independently
replayed their proofs and the fixed twelve-point proof with cake_lpr.
The exact finite and real-geometry obstruction now also has a complete
Lean proof, with a fresh [parent replay](../lean_terminal12_parent/README.md).
Its main statement is `Delta3.Terminal12.RealBridge.terminal12_real_obstruction`.
Lean checks existence and every geometric premise of this explicit example;
the global lower bound through11 still uses the separate finite audits.

All probes used one CPU and AS150 MiB; the proof checker used heap64 and
stack32. The tiny certificate run took 1.520 seconds including wrapper
polling and compression. No long unit or extra memory reservation was
needed. The source fifteen-point example and all original evidence remain
unchanged.

## A small explicit refutation

The parent extracted a65-clause irredundant core and an explicit47-node,
24-leaf propositional refutation, replayed by exact clause/unit checks.
Each retained clause has a satisfying assignment when that clause is
deleted. This proves irredundancy, not minimum core size. A fresh cake_lpr
proof of the reduced core is also accepted. See [core/DONE.json](core/DONE.json)
and [core/certificate/result.json](core/certificate/result.json).
The core CNF SHA-256 is
`450bb17403af22a2253a03b4610b14caefab73253d883ddcbd65f780bac95d3a`.
The completed Lean formalization checks this core and its actual geometric
interpretation. The14 finite modules and5 real-bridge modules pass separate
fresh parent replays with only standard axioms. See
[lean_terminal12](../lean_terminal12/README.md) and
[the parent receipt](../lean_terminal12_parent/README.md).
