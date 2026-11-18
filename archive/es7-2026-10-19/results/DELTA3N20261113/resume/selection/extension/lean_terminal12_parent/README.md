# Fresh parent replay of the twelve-point real obstruction

**PROVED, Lean; both fresh parent stages PASS.** All19 finished modules
were rebuilt, with59 explicit axiom reports using only standard axioms.
The parent rechecked all source, prerequisite and project-cache hashes,
expected declaration lists, diagnostics, clean resource exits and logs.

The main theorem is
`Delta3.Terminal12.RealBridge.terminal12_real_obstruction` in
[T12Real.lean](../lean_terminal12/T12Real.lean). It concerns the actual
twelve-point real set: distinct x coordinates, general position, no
five-cap, no convex hexagon, and no terminal-safe subset meeting every
real convex pentagon. The geometric bridge leaves no external geometric
assumption for this existence statement. The global minimum12 lower
bound still relies on the separately audited finite certificates; it
is not a Lean theorem in this packet.

The finite stage rebuilt14 modules with32 audits in10.085 seconds,
maximum RSS621268KiB. See [finite/data/result.json](finite/data/result.json).
The real stage rebuilt five further modules with27 audits; see
[real/data/result.json](real/data/result.json) for timings and all hashes.
Both fresh runs used one CPU, no swap and finite systemd runtimes.
Finite RSS guard1300MiB/MemoryMax1800M and real guard2000MiB/MemoryMax2600M
were separately allocated within the unchanged verifier budget.

The main source SHA-256 is
`71021255ae73bc9057d6909aba812f0385e989cbcc5fd47be781e9d101fb02cf`.
The frozen real manifest SHA-256 is
`e1ad05f14c742d6e5a1117fac8f141bcdb51563293317148b1c929fc28aecb7a`.
Fresh logs/receipts and worker freeze snapshots are retained under
`finite/data/` and `real/data/`. The original worker and fifteen-point
packets remain unchanged. Replay uses the frozen `T12replay_finite.py`
then `T12replay_real.py`, each with a fresh prefix and allocated resources.
