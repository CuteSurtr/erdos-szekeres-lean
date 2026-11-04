# Adversarial soundness review, 4 November 2026

Scope: `C6UPPER`, `C7UPPER`, the layer lemma in `SYM5`, and the relevant `ROT456` validation code, at base commit `44530b46fef0632bf8d8829c9bb5d694e271fb30`. Paths below are relative to the results directory. This file reviews the mathematical reduction and source; certificate replay outcomes belong to the accompanying replay report.

**Written proof (reviewed, not refereed):** no blocking mathematical error was found in the reduction or the two encoders for `(m,K,t)=(6,8,11)` and `(7,8,10)`. The qualifications below affect claims about exact validation and implementation independence. This review does not turn a sample of replayed proofs into a complete replay of every sixfold cube.

## Findings and repairs

| Severity | Location | Finding, counterexample, or repair |
|---|---|---|
| Major: rigor label | `ROT456/tests/test_reflect.py:1`, `ROT456/tests/rv.py:3`, `rv.py:10`, `rv.py:40`, `rv.py:45`, `C6UPPER/encb/test_b_sets.py:1`; contextual claims in `C6UPPER/README.md` §2 and §3b | The scripts called “exact” evaluate square roots with 90-digit `Decimal` arithmetic, choose sectors with binary64 `atan2`, and compare phases as floats. Thresholds reject small margins but no interval/error proof is supplied. These runs establish numerical evidence unless independently certified; this is not evidence that their particular verdicts are wrong. Repair: exact cyclotomic/rational sign arithmetic and exact ray ordering, or rigorous interval enclosures that exclude zero for every decision. For sixfold weights use the integer coordinates described below. The reflection argument itself is unaffected. |
| Major: independence scope | `C6UPPER/README.md:102`, `:157`; `C6UPPER/encb/gen_b2.py:3`, `:24`, `:36`, `:45`; `C6UPPER/encb/test_b_sets.py:12`, `:17`, `:20` | “Different canonical forms” is false: the canonical representatives agree identically. The advertised direction-major `pid` is unused; actual tuple enumeration is layer-major. Moreover the B real-set test computes orientations through A's `Enc`, `assign`, and `o`. Repair the description to “separate implementations of the same mathematical encoding, with different angular computation, recurrence direction, and variable allocation; shared canonical representatives and some validation code.” For an independent real-set test evaluate the determinant of each B-map triple directly. This is a trust-base correction, not a counterexample to either formula. |
| Minor: proof exposition | `C7UPPER/gen.py:38`–`:45`, compared with `:169`–`:171`; `C6UPPER/encb/gen_b2.py:107`–`:110` | The written angular dichotomy omits the unavoidable same-layer antipodal boundary case for even `m`. Such a triple has the centre on a segment and is neither a strict centre-containing triangle nor contained in an open half-plane. The code correctly emits no angular clause. Repair: explicitly state this third case and its deliberate omission. It weakens the formula and cannot exclude a real configuration. |
| Minor: misleading comments | `C6UPPER/encb/gen_b2.py:167`, `:171` (also `C7UPPER/gen_b.py`) | The displayed `F <= condition` inequalities reverse the implications actually emitted. `[F,-o]` means `o => F`, and an extension antecedent implies the longer chain. Repair the comments to these implications. The emitted clauses and the least-fixpoint proof use the correct direction. |
| Minor: stated open values | `C6UPPER/README.md:166` | “54, 60, or in between” overlooks the orbit count. A nontrivial even-order rotational set in general position excludes the centre, so its cardinality is a multiple of six. Conditional on the stated lower and upper bounds, the maximum is either 54 or 60. Repair the wording. |
| Minor: checker invocation hardening | `C6UPPER/tools/verify_cover.py:19`–`:31` | Validation is expressed with Python `assert`. Under `python3 -O` an empty cube directory reaches the success message. The prescribed ordinary `python3 -I` invocation retains assertions, so this does not invalidate that replay. Repair a future checker by using explicit failing conditions, or add an unconditional startup rejection of `not __debug__`; record the actual invocation and interpreter flags. |

**Evidence only:** source review cannot establish the historical authorship or development independence of two files. It can establish absence of imports between the generators and the concrete algorithmic differences. The findings above do not assert copying.

## Layer and general-position reduction

**Written proof (reviewed, not refereed).** Delete the rotation centre if present. Every remaining point has a free orbit of size `m`; the hull vertex set is invariant. If a hull contained at least two orbits, its at least `2m >= K` vertices would contain `K` points in convex position. Consequently every nonempty hull is one regular `m`-gon. General position puts every remaining point strictly inside that polygon; induction gives the nested layers. This uses genuine Euclidean rotational symmetry and the hypothesis `K <= 2m`. It cannot be applied to `(m,K)=(3,8)`.

**Written proof (reviewed, not refereed).** For even `m`, any noncentral point and its antipode make a collinear triple with the centre. Thus a general-position set with a noncentral orbit cannot include the centre. Sixfold sets of size above 60 therefore have at least eleven orbits. For sevenfold symmetry, nine orbits plus the centre have only 64 points, so any set of at least 65 points has ten noncentral orbits. Removing the centre and surplus inner layers preserves octagon-freeness.

**Written proof (reviewed, not refereed).** Generic phases can be obtained without assuming that the centre is originally in general position with the noncentral points. There are finitely many nonzero triple determinants of the original set. Their signs, all strict nesting inequalities, and hence the order type and absence of a convex octagon persist in some neighbourhood of the orbit-angle vector. Bad phase equalities form a finite union of proper affine hyperplanes in that neighbourhood; avoid them while keeping the outer orbit fixed. For odd `m` no orbit itself has an antipodal pair. For even `m`, equal phases in distinct orbits are already forbidden by general position: one point in the inner orbit and the two antipodal outer points would be collinear. The code does not try to remove same-orbit antipodes for even `m`.

## Orientation variables and angular rules

**Written proof (reviewed, not refereed).** Rotation preserves orientation, and the literal permutation sign supplies the correct sign for each ordered triple. A stabilizer of an unordered triple cannot induce a transposition: that would fix one noncentral point under a nonidentity rotation. The only nonidentity possibility is a 3-cycle, which is even. Thus using one signed variable for each triple orbit is consistent, including the threefold stabilizers present when `m=6`.

**Written proof (reviewed, not refereed).** The phase-order clauses forbid the two directed triangle cycles in a tournament, which is equivalent to a strict total order. Every angular clause enumerates the orders of only the layers appearing in its triple. A uses adjacent order comparisons, with the global transitivity clauses supplying the others; B uses all pair comparisons. Both sets of premises select the same local phase pattern.

**Written proof (reviewed, not refereed).** For odd `m`, the point direction is `psi_i + (2k+h_i) pi/m`, with `h_i=0` exactly when `H(i)` is true, and its antipode adds `m` to that integer cell index. For even `m`, use `psi_i + k 2pi/m`, and add `m/2` for the antipode. Comparing integer cell indices and phase ranks determines the circular order exactly. B implements these comparisons directly. Three alternating point/antipode pairs characterize the centre strictly inside the triangle; otherwise a nondegenerate pattern has three consecutive point directions in one open half-plane. Coincident point/antipode keys in the even case are intentionally skipped.

**Written proof (reviewed, not refereed).** In the open-half-plane case, write the direction gaps as `x,y>0`, `x+y<pi`, and reciprocal radii as `u`. When the angularly middle point is on the outermost of the three layers,

`u_a sin(y) - u_b sin(x+y) + u_c sin(x)`

is at least `u_b [sin(x)+sin(y)-sin(x+y)]`, and the bracket equals `4 sin(x/2) sin(y/2) sin((x+y)/2)>0`. This proves the asserted orientation without assuming equal radii or restricting the layer gaps. Strict nesting gives the required weak ordering of reciprocal radii. The centre-containing orientation rule follows because the circularly ordered triangle encloses the centre.

**Evidence only / implementation trust:** A classifies representative angles with binary64 arithmetic and `eps=1e-9`. Its correctness as executed is not formalized by the real-arithmetic docstring. The representative phases are widely separated for these fixed instances; B's integer classification and exhaustive semantic comparison provide the appropriate independent computational check. The exactness of B's integer pattern computation should be distinguished from the floating arithmetic in the real-set tests.

**Written proof (reviewed, not refereed).** Nesting units for the single edge `(i,0),(i,1)` suffice: rotating them supplies every outer polygon edge and every point of each inner orbit. Simplification uses only the emitted angular/nesting units. A constant true orientation can safely be removed from an implication antecedent; an antecedent known false can safely discard the whole implication. B retains true literals but makes the same safe false-antecedent deletion.

## Chains and every convex octagon

**Written proof (reviewed, not refereed).** Fix `p=(i,0)`. Every other point of layers `>=i` is strictly on the inner side of the tangent to the radius-`r_i` circle at `p`. Its ray from `p` therefore belongs to an open angular interval of length less than `pi`; different rays are distinct by general position. Positive `orient(p,q_s,q_{s+1})` makes these rays strictly increase, so a chain cannot repeat a vertex even though the recurrence stores only its last or first pair.

Translate `p` to the origin. Every segment joining consecutive rays remains in the cone between them and has strictly increasing polar angle: along the segment the angular derivative has the positive sign of the determinant of its endpoints. Nonadjacent such cones have disjoint angular interiors. Together with the two end segments to `p`, this proves the fan polygon is simple. The recurrence gives every internal left turn; the angular order gives the turns at the first point, last point, and `p`. A simple polygon with all strict turns left is strictly convex. Thus a seven-point chain with `p` is a convex octagon.

The forward and backward recurrences both start at chains of length two. Every longer-chain implication is justified by appending or prepending one positive-angular-order point with a left turn. Assign chain variables exactly according to genuine chain existence (equivalently their least fixpoint). A forbidden final extension would give the convex octagon above, so an octagon-free real configuration satisfies all chain clauses.

Conversely, choose an outermost-layer vertex of any convex octagon and rotate it to `(i,0)`. All other vertices are in layers `>=i` and occur in increasing angular order at that pivot. Their consecutive triples turn left, so the recurrence detects them. This completeness direction is useful for testing, but the upper-bound inference requires only the previous soundness direction.

## Reflection units and the cube cover

**Written proof (reviewed, not refereed).** Reflection in the axis through `(0,0)` maps each nonzero normalized phase `theta_i` to `2pi/m-theta_i`, after relabelling within its orbit. It preserves layers, general position, and convex position. For even `m`, it reverses the strict `psi` order, so exactly one of a configuration and its reflection satisfies `Y(1,2)`. For odd `m`, it exchanges the two open halves `(0,pi/m)` and `(pi/m,2pi/m)`, so exactly one satisfies `H(1)` after the generic perturbation. The operation need not be an existing symmetry of the original set: it produces another allowed configuration. Layer indices must not be permuted because they encode radial order.

**Written proof (reviewed, not refereed).** The thirty-two five-bit sign patterns are a tautological cover of all assignments to the five chosen `Y` variables, even without any geometric interpretation or transitivity. Appending the common `Y(1,2)` unit therefore makes UNSAT of every cube imply UNSAT of the base plus that unit. Transitivity leaves twelve realizable phase orders and twenty impossible patterns, but discarding the latter is unnecessary because their certificates are retained.

**Written proof (reviewed, not refereed).** With assertions enabled, `verify_cover.py` checks the exact base body prefix, adjusted header, six appended units, variable order, sign-derived filename, and all thirty-two distinct patterns. It does not independently prove that the supplied metadata names geometrical phase variables, nor parse/count the base's DIMACS clauses; fresh generation, inspection of each encoder's map, and the proof checker provide those links. Encoder B's map has a different schema and must be converted explicitly to the `Y` dictionary expected by the cube tool, preserving its values. The sampled proof replays must use these freshly rebuilt cube bodies, not only archived base formulas or historical logs.

## Concrete check of the canonical-form claim

**Exact computation, replayed 4 November 2026.** The actual `canon` function was extracted from B's syntax tree and compared with A's canonical representatives over every unordered triple at both certificate dimensions. No clauses or solvers were involved; the check took under one second on one core.

| Instance | Triples compared | Triple orbits | Canonical mismatches |
|---|---:|---:|---:|
| `m6K8t11` | 45,760 | 7,634 | 0 |
| `m7K8t10` | 54,740 | 7,820 | 0 |

Run from the results directory:

```sh
python3 -I - <<'PY'
import ast, importlib.util, pathlib
root = pathlib.Path('.')
spec = importlib.util.spec_from_file_location('a', root / 'C7UPPER/gen.py')
a = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)
tree = ast.parse((root / 'C6UPPER/encb/gen_b2.py').read_text())
main = next(n for n in tree.body
            if isinstance(n, ast.FunctionDef) and n.name == 'main')
f = next(n for n in main.body
         if isinstance(n, ast.FunctionDef) and n.name == 'canon')
code = compile(ast.fix_missing_locations(ast.Module(body=[f], type_ignores=[])),
               'canon', 'exec')
for m, t in [(6, 11), (7, 10)]:
    env = {'m': m}
    exec(code, env)
    e = a.Enc(m, 8, t)
    bad = 0
    for tri, (ca, parity) in e.canon.items():
        cb = tuple(i*m+k for i, k in env['canon']([divmod(x, m) for x in tri]))
        bad += ca != cb
    print(m, t, len(e.canon), len(e.tvar), bad)
    assert bad == 0
PY
```

**Written proof (reviewed, not refereed).** This equality also follows structurally. The lexicographically least rotated layer-major triple must give one of its points sector zero; otherwise rotating the least-layer point to zero improves the tuple. B examines all three vertex-to-zero rotations, so it includes A's minimizer. The algorithm used to find that representative differs; the representative itself does not.

## Exact sixfold arithmetic repair

**Written proof (reviewed, not refereed).** If the cyclotomic weights are `w_0,...,w_5`, define

`X=2w_0+w_1-w_2-2w_3-w_4+w_5`, `Y=w_1+w_2-w_4-w_5`.

The Euclidean point is `(X/2,sqrt(3)Y/2)`. Orientation signs are the signs of ordinary integer determinants of the `(X,Y)` pairs; squared-radius order compares `X^2+3Y^2`; cross-product signs compare rays and identify sector membership. Reflection is `Y -> -Y`. Therefore the sixfold example, its mirror, and their phase-order unit can all be checked without any floating arithmetic. Reading B's triple map directly also removes dependence on A's orbit-sign conversion. This section supplies the repair argument; whether it was executed is stated in the accompanying validation report.

## Orbit-counting rule and open-case implications

**Written proof (reviewed, not refereed).** A finite order-`m` rotational set has `mt+e` points with `e` zero or one. For target `2^(m-1)`, even `m` forces `e=0`, so `m` must divide a power of two, hence be a power of two. Odd `m>1` cannot divide that target, so `e=1` and `2^(m-1)=1 mod m`: precisely odd primes and odd base-two Fermat pseudoprimes. Conversely, with the indicated orbit count, generic angles/radii give general position (include the centre only in the odd case). This is size compatibility alone, not a guarantee of octagon-freeness or of an extremal construction. The cited Lean work is not rerun in this review.

**Evidence only: suggested experiments.** For fivefold cubing, split actual orientation variables supported on the outer layers, or the remaining outer `H` bits, and compare matched small solver budgets before committing to a full partition. Such binary branching needs no added geometric lemma: both signs cover all assignments. Do not impose an extra global phase-order unit alongside `H(1)` merely because both are individually reflection-normalizable; one reflection cannot generally normalize both simultaneously. The exact 56-point test is necessary for proposed geometric clauses but is not by itself their universal soundness proof.

**Evidence only: suggested experiments.** At sixfold ten layers, a final-polynomial contradiction for one abstract model excludes that model, not all models at sixty points. A CEGAR cut must retain the exact signs used by the polynomial and an exact positive certificate; it can then be negated as a clause and tested on the 54-point example and mirror. Small orbit-reduced or two-layer supports are a reasonable initial search, but failure to find such a certificate says nothing about realizability. For fourfold seventeen layers the same chain model remains sound. For threefold symmetry, allow convex layers with either one or two orbits (three or six vertices); restricting every layer to one triangle would lose possible octagon-free sets.

### A threefold relaxation without the layer lemma

**Written proof (reviewed, not refereed):** a direct alternative is to omit `fam_nest` entirely and interpret the indices as decreasing **orbit radii**, rather than convex layers. Independent sufficiently small changes to orbit radii and phases preserve every nonzero original triple determinant and hence the absence of convex octagons. Choose such a perturbation with all orbit radii distinct and generic phases, relabel by decreasing radius, and rotate the largest orbit to `theta_0=0`.

In `C7UPPER/gen.py`, the angular rule uses only `r_b >= r_a,r_c` for the angularly middle point: convex-hull nesting never enters that inequality. At pivot `(i,0)`, every point in the suffix has radius at most `r_i`; all except the pivot are strictly inside the tangent half-plane. Therefore the chain argument remains sound, and any convex octagon is captured by choosing a vertex on its maximum-radius orbit. Phase transitivity, orbit canonicalization, and the odd reflection unit likewise make no nesting assumption. Literal simplification is still justified if `forced` contains only emitted angular units.

**Written proof (reviewed, not refereed):** source inspection finds no other dependence on convex-layer nesting in these families. Thus omitting the nesting family gives a sound radius-ordered relaxation for `(m,K,t)=(3,8,22)` despite `8>2m`. A threefold set of at least 65 points must have at least 22 noncentral orbits, so UNSAT of that relaxation would exclude the threefold threshold. This is a proposed reduction, not a generated formula or a solver result in this review. Before using it for a certificate, validate the modified implementation on the known 61-point example and adversarial configurations with two orbits in the same convex layer. Hull batches of three or six vertices could supply additional independently justified constraints later.

**Exact computation, replayed in this review:** the empty-directory counterexample for the original cover checker under `python3 -I -O` was reproduced (`logs/original_cover_optimized_counterexample.log`). The separate `strict_cover.py` accepted both actual 32-cube covers and rejected missing/body/unit/header mutants even with optimization enabled. The certified checker source was left unchanged.
