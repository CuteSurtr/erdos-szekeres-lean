# Parent certification request: rightmost one-blue repair obstructions

**Final status: FROZEN.** The parent independently confirmed both geometries
and full clause families and freshly certified both full one-blue CNFs.
This track observed `s VERIFIED UNSAT` in both completed cake logs and
matched the frozen input/proof hashes. See README.md, VERIFY_REPAIR.md and
data/PARENT_CERTIFICATES.json. The request below is retained as history.

**Update:** the independent check also confirms **n=8, m=16**, rightmost
r=15, A={7,13,14}, minimum old-blue cost **2**. There are 15,356 full Deltas;
B={2,3} is a minimum-cost positive control. Coordinates are in
`data/two-clones-n8-best.json`, the complete audit in
`data/rightmost-n8-audit.json`. The full CNF is
`data/rightmost-n8-one.cnf`: **16 variables, 277 clauses**, SHA-256
`6517d49858bbaf2ae7cd743fb1d4597f62f8320ad05642a9952ea8ae65950f74`.
Please include this second rightmost case in the parent's certification run.

**COMPUTED, independently reimplemented in Python:** there is a real
(5,7)-valid 14-point configuration with rightmost r=13 and an old weak Delta
A={5,11,12} whose exact minimum old-blue repair cost is **2**. Thus the
one-blue rule fails even for the main rightmost-point induction.

The real integer coordinates are `data/rotation-best.json`. They arise by
an invertible, orientation-preserving affine transformation of the separate
interior-root 14-point example, followed by sorting in the new x-coordinate.
Cap-freeness is rechecked in the new order, not inferred from affine invariance.

`verify.py` uses all-triple cap tests and supporting-edge polygon tests,
different from the C++ finder's consecutive-turn and monotone-hull tests.
It enumerates every full B once, with no SAT solver, and checks the old A.
`data/rightmost-n7-audit.json` records 2,669 full Deltas and their exact cost
histogram. A minimum-cost positive control is included there and as a model
for `data/rightmost-n7-two.cnf`.

Please schedule CaDiCaL 2.1.3 and cake_lpr on:

- `data/rightmost-n7-one.cnf`: **14 variables, 213 clauses**.
- SHA-256: `ef26f775f629af551be837b84e9f106948b4163e674018e9980fd225b5df0edd`.
- `data/rightmost-n8-one.cnf`: **16 variables, 277 clauses**.
- Optional separate interior-root control: `data/arbitrary-n7-one.cnf`.

No solver has been run by this track. The one-blue CNF has a negative clause
for each four-cap, a positive clause for each hexagon, and all negative
pairs on the 10 old-blue vertices. It puts no constraint on the color of r
or retention of A. Therefore its models are exactly the allowed repairs.
All clauses are generated from integer coordinates; family lists, SHA-256,
and a finite branch obstruction are in the matching `*-audit.json` files.
Only cake_lpr's literal `s VERIFIED UNSAT` will support CERTIFIED.

The arbitrary-root original remains in `data/reduced-n7.json`, with r=1,
A={5,6,7}, cost 2. It is not used to imply rightmost-root failure.

A universal positive result is also established in written form: for every
n>=5, every five-cap-free S with |S|<=n+2, and every old weak Delta A,
there is a repair with at most one old-blue selection. This does not need
r extreme or S n-gon-free. The proof is in `THEORY.md` (being finalized).

Written proofs and controls are now final. The full formulas and coordinates
have remained unchanged since handoff. Ordinary and r-selected cost-two
controls are separate in data/controls.json. No further search is pending.
No long units were launched; no git operations or other tracks were edited.
