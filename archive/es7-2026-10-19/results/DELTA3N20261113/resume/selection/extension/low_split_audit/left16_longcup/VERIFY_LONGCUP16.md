# Independent left16 long-cup augmentation — PASS

**COMPUTED:** the entire compact16 base, new CNF family and appended map
are independently rebuilt. **PROVED (written):** every real T7(L) failure
in the base domain has a six-cup and canonically satisfies the augmentation.
No propositional equivalence with the unaugmented abstract formula is
asserted. No solver or LRAT replay was run for this audit.

## Inherited domain and independently rebuilt base

The base has n7,left size16 and encodes failure of T7(L) for x-ordered GP
L with no four-cap and no convex seven-subset. T7(L) is the disjunction of
a cup transversal of all convex six-subsets, with End3 at every selected
vertex after its first, and a partition into cups B,D with |D|<=5.
The latter alternative is impossible at16 since a cup has at most6 points.

The frozen [low encoder audit](../VERIFY_LOW_SPLIT.md) supplies the generic
direct/compact equivalence, exact containment semantics and canonical real
counterexample projection. Its independent row checker is reused read-only,
with only its scratch destination redirected in memory. The complete new
size16 base instance is rebuilt here:128,297 variables,903,593 clauses,
2,416,241 literals, with every map/CNF byte identical. The original base
and its separate solver run are unchanged. The compact source remains
`1fb043a5d29fa86047ba05cae86fdfb248e6069bc6731c4ee39c181737319303`;
the inherited geometry source remains
`1964e17b777fd7b7a973f12b2911c003a050047f13a621f523a9f98c6e31d553`.

## Exact appended clauses and map

For every six-subset S, introduce z_S with

    z_S iff AND(t_abc : {a,b,c} subset S, a<b<c).

Each definition has20 binary rows `-z_S t_abc` and the reverse row
`z_S -t_1 ... -t_20`. All positive orientation literals are the original
base variables. The final clause is the positive OR of all8,008 flags.
For real GP points, the20 positive triple signs say exactly that S is a
six-cup. Thus the new family requires existence of a six-cup and gives a
unique canonical extension on all its new flags. The reverse row is
checked even though the weaker one-way implication plus OR would already
suffice to assert some all-positive six-subset.

The independent builder enumerates integer six-masks, orders their vertex
tuples and filters the complete560-entry orientation map by membership.
It neither imports nor executes the producer. All8,008 masks occur exactly
once; each has20 distinct orientation children. New IDs are consecutively
128298 through136305, all with map kind `six_cup` and the exact subset mask.
Every old map byte is retained (4,023,642 bytes). Every old CNF body byte
is retained (17,331,407 bytes), with only its header count updated before
the new comment/family. The producer receipt matches independently.

The additions are8,008 variables,168,169 rows and496,496 literals:
21 rows and61 literals per AND definition, then one8,008-literal OR.
The final formula has136,305 variables,1,071,762 rows and2,912,737 literals.
Source/input/map/output hashes are stable before/after. Full streamed
reconstruction hashes agree with the produced CNF and map.

* Base CNF: `2e233545d18e3a9acf9a253b80a102935828bee27c079ba18946dfbd4efd53d8`.
* Base map: `46dfc8217a63d6c4a34ed65316443aff990702e3505f0791c540e67ed52cc220`.
* Augmented CNF: `f23af9d7113dac3f9e4414298b20fb08d8181c279804d36b79e98a66755622b4`.
* Augmented map: `c4e2ec5444906df0e7dbe80e2cb2846d6e38a52ed4c7af6e3c746dcef93049bb`.
* Producer: `168c016a00338dfa2ae0f40129c6af31ce81f13b21a4a82d40d61fd990ecb3f0`.

## Independent proof: cup maximum at most5 implies T7

This argument works for any real x-ordered GP L with no four-cap and
cup maximum c<=5; it needs no cardinality bound or earlier finite terminal
certificate. In any convex hexagon the upper cap has at most3 vertices.
Since the upper cap and lower cup share exactly two endpoints, its lower
cup has at least5 vertices. If c<=4 there are no hexagons, so B=empty
already satisfies T7's first alternative.

If c=5, let beta(v) be the longest cup ending at v and take
B={v:beta(v)=5}. Every hexagon's right endpoint lies in B, by the preceding
lower-chain argument. It remains to prove that B is a cup and has the
required endpoint property.

For any a<b in B, take a maximum cup ending ...p,a. The penultimate p
exists. If p,a,b were a cup, increasing consecutive slopes would append
b to that five-cup, contradicting c=5. Thus p,a,b is a cap, so b ends an
ambient three-cap. In particular every B vertex after its first has End3;
the first vertex is not required to have it.

If a<b<d in B formed a cap, the same p would give cap p,a,b. Together with
cap a,b,d, decreasing consecutive slopes make p,a,b,d a four-cap in L,
contrary to the premise. Hence B contains no cap triple and is a cup.
It meets every hexagon and satisfies the endpoint condition, proving T7.

Consequently a real T7 failure has cup maximum at least6. In the base
no-seven-gon domain a seven-cup is impossible, so its maximum is exactly6.
In particular it contains one of the six-subsets represented by a new
flag. This independently supplies the reduction cited by the producer's
reference to [structure2/low_split.md](../../structure2/low_split.md).

## Whole projection and possible future conclusion

Given any real16-point T7 failure in the stated base domain, assign the
canonical exact geometric/containment flags of the audited compact base.
Those satisfy the old failure formula by its generic soundness proof.
Set each new z_S to its actual six-cup truth value. All exact AND clauses
hold, and the final OR holds by the preceding real-geometric lemma.
Thus every such real counterexample yields an augmented CNF model.

This does not prove that every abstract base model has a satisfying
extension: the reduction uses real cup chains, polygons and no-four-cap.
No abstract-model equivalence is needed or claimed. An accepted matching
UNSAT proof, together with this audit and the written lemma, would establish
T7 at **exactly left16**, without assuming six-cup existence as an extra
hypothesis in that final geometric theorem. The <=5-cup branch is already
settled by the lemma. No accepted proof is supplied in this packet.

Only after that finite proof could the explicit previously certified
through15 chain extend to through16. An all-left conclusion would still
need the separate capacity bound. The singleton-right-block obligations
in general low-split corollaries also remain as previously stated. No
unrestricted full14 terminal theorem, weak-Delta theorem or ES claim is
made here.

## Controls and limits

Every one of the8,008 AND gates is truth-tested with all children true,
each single child false and all children false, with both flag values:
352,352 gate assignments. The final OR is checked on all-false and on
first/last one-hot assignments. All rows and map entries are also compared
literally, so no gate or child position is inferred from sampled output.

Independent exact real controls use only our frozen determinant/triangle/
cup-rank routines, not the producer or a parent checker. Newly constructed
10- and15-point fixtures have no four-cap/no-seven-gon and cup maxima4
and5. Their endpoint ranks are cross-checked by enumerating cup subsets.
The10-point set has no hexagon and B=empty works. The15-point set has410
hexagons; B={10,11,12,13,14} is a verified Option1 cup. Its first vertex10
does not have End3, while11–14 do, exercising the necessary exemption.

A separate real16-point fixture, using only coordinates from the older
left16 data, has no four-cap/no-seven-gon, cup maximum6 and300 hexagons.
Exactly73 new flags are true; every168,169 appended row holds canonically.
The first six-cup is {0,1,2,6,7,8}. Its positive Option1 selector
{0,3,4,9,11} is independently verified. This is a positive geometry control,
not a purported model of the old counterexample-failure clauses.

The full audit took3.434s, peak RSS61,540KiB, one CPU, AS300MiB,
wall20/CPU19, affinity5,nice10. It completed before07:52:16KST. Packaging
uses AS150 in accordance with the parent's upcoming capacity reservation;
no audit compute remains active during that reservation. No solver, cake,
compilation, long unit, extra heap, git, deletion or external action occurred.
All earlier packets stay frozen. Commands, results, source/receipt snapshots
and exact controls are retained; future runs need new exclusive outputs.
