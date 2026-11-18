# Independent audit of the maximal-set shortcut

**COMPUTED: the real 12-point counterexample to the maximality strengthening
is independently confirmed by exact integer geometry.** The new clause
family has a sound canonical-assignment argument and passes a positive
control on this actual witness. No LRAT certificate or global minimality
claim is made. This configuration has a working weak Delta.

The proposed statement says **every** inclusion-maximal four-cap-free R
hits every convex hexagon in a set with no five-cap and no convex heptagon.
The verified R below is one counterexample to that universal choice of R.
It does not prevent a different subset from working.

## Exact real witness

Input: [retained real-star.json](results/real-star-input.json), copied from
`/home/jay/research/data/delta3-codex-20261113/resume/pool/maximal/real-star.json`.
[`audit_real_star.py`](audit_real_star.py) uses this audit's own Python-integer
determinants, monotone hulls and direct subset scans. It imports no parent
geometry checker, minimizer, SAT model, optimizer, or lattice implementation.

| Independently checked quantity | Result |
|---|---:|
| Integer points, strictly increasing x | 12 |
| Nonzero orientation determinants | 220 |
| Minimum absolute determinant | 215,315,157 |
| Four-caps, hull and all-triple definitions agreeing | 25 |
| Five-caps | 0 |
| Convex hexagons | 54 |
| Convex heptagons | 0 |
| Inclusion-maximal four-cap-free subsets | 65 |
| Such maximal subsets missing at least one hexagon | 4 |
| Working weak Delta, all 4,096 masks scanned directly | 1,526 |

The supplied sets, with zero-based indices, are
`R={0,1,4,5,6,10}` and `H={2,3,7,8,9,11}`. They partition the 12 points.
R contains no four-cap. H is a convex hexagon and R is disjoint from H.
For each point outside R, the saved blocker is a four-cap in R plus that
point; all four triple determinants in every row are strictly negative:

| Added point | Independently validated saved blocker |
|---|---|
| 2 | {0,1,2,4} |
| 3 | {0,1,3,4} |
| 7 | {0,1,6,7} |
| 8 | {0,1,8,10} |
| 9 | {0,5,6,9} |
| 11 | {4,5,10,11} |

Thus every one-point enlargement contains a four-cap. Any larger strict
superset contains such an enlargement, proving inclusion-maximality.
The audit also enumerated every possible blocker independently, rather than
only evaluating the supplied choices.

**The singleton Delta={8} hits every one of the 54 convex hexagons.** It is
automatically four-cap-free. This explicitly demonstrates that weak Delta
holds on the very configuration that refutes the maximality shortcut.

Full coordinates, orientation signs, all cap and target families, blocker
determinants, all maximal masks and all working Delta masks are retained in
[real_star_audit.json](results/real_star_audit.json), with input and code
hashes. The extraction's coordinates and red/blue membership were checked
against the parent's 22-point search record. The geometric conclusion rests
on checking the 12-point set itself, not on trusting that larger record.
The audit does not assert minimum size among all possible counterexamples.

## New clause family: independently derived semantics

Reviewed source: `../pool/maximal_cnf.cpp`, SHA-256
`7ee7d13e21416e30a70efe671a7270e8b1b73d73346abf7a13ef74609f0583db`.
Its included old encoder has hash
`b953e14fc7d0840712bbf63f502e00c7342cbd1cdb9ef3ed548759e8ae8aa12c`.
No gap was found in this family.

1. The included `base()` supplies signotope packets, no five-cap, and no
   convex n-gon. It adds no orientation fixing or symmetry clauses.
2. On four sorted vertices, the first and last consecutive triple signs
   both negative force the entire packet negative. The clause containing
   those two positive signs and the four negative membership literals is
   therefore exactly the prohibition of an all-red four-cap.
3. A cap flag implies those two negative signs. A point-specific witness
   implies a cap containing that point and membership of the other three
   vertices in R. The disjunction of red membership with all such witnesses
   ensures that every point outside R creates a four-cap when added. The
   four-cap-free premise ensures this is precisely inclusion-maximality.
4. A selected target implies that all its four-subsets are convex and all
   its vertices are outside R. The one-way quad implications implement the
   two packet equalities for convexity. Requiring some target thus gives a
   convex (n-1)-set disjoint from R. These are existence flags; no reverse
   implications are needed for soundness.

Conversely, given valid signs and an actual maximal R missing a target,
assign red membership exactly, each cap flag its cap truth value, each
point witness its actual cap-and-red truth value, every quad its convexity
truth, and every target its convex-and-blue truth. Every displayed
implication and required disjunction then holds. This constructs the
canonical assignment and proves completeness. Together the two directions
encode exactly the existence of a bad maximal R in the abstract model,
not the absence of every working Delta.

[`audit_maximal_formula.py`](audit_maximal_formula.py) compiled that source
independently into the audit scratch directory, generated its n7/m12 CNF,
constructed the assignment solely from the verified coordinates and R,
and satisfied **all 48,226 clauses on 4,126 variables**. No solver was used
for this check. [maximal_formula_audit.json](results/maximal_formula_audit.json)
records source, binary and CNF hashes. The CNF hash is
`1c404431d3494ff55c1258ba1daae7da3ee90ccbd9ded06eeaa03b038c9e0444`.

## Scope and resources

The initial coordinate control took 0.031 seconds with 17,604 KiB peak RSS,
a 400 MiB address-space limit, one CPU/thread, a six-second CPU limit and
an external eight-second SIGKILL deadline. The fresh compile and canonical
CNF control took 0.794 seconds under 400 MiB, one CPU and an external
20-second deadline. No long job or user unit was launched; no parent files
were edited and no proof checker was run.

The previous abstract 10-point star and its unsuccessful 300-start
realization search remain search artifacts. Failure of that heuristic
search is not a proof of nonrealizability, and the real negative result
above does not depend on those signs or attempts.

Reproduce with the research venv Python and `-B`, running
`audit_real_star.py` under `timeout -s KILL 8s`, then
`audit_maximal_formula.py` under `timeout -s KILL 20s`. Both write only the
assigned audit directories. Only the latter recompiles source; neither
installs software or invokes a solver.
