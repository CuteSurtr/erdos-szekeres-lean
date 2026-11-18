# Independent specialized rooted-family audit

**Written soundness/projection argument confirmed; exact controls COMPUTED.**
No error was found in the reviewed specialized family. Canonical real
n7/m16 and n8/m16 assignments passed every non-pool clause, and their false
pool clauses matched exactly the rooted working masks in the reduced range.
Five small real controls also passed 2,907 existential auxiliary queries.
This is an encoder review, not a certificate for any specialized search.

Reviewed source `../rooted_fast.cpp` SHA-256:
`540c60ca6657b8234d601b1289518d743f59935ea3d8ca7c9149d3125af8b744`.
Its inherited `../../compact/compact_cnf.cpp` SHA-256 is
`1964e17b777fd7b7a973f12b2911c003a050047f13a621f523a9f98c6e31d553`.
The geometry is inherited from the earlier compact audit, rather than
treated as established by the parent's new description. Both m16 generated
geometric prefixes were checked byte-for-byte against the controlled compact
formula. The argument below independently derives the new family.

## Projection and size range

Let r be the largest x-label, U=S−r, and write a rooted Delta as D=A∪{r}
with A⊆U. A four-cap in D either avoids r, giving an old four-cap in A,
or contains r, giving three old vertices in A that form a four-cap with r.
These two possibilities exhaust every four-cap; they do not presume that
A is maximal or that a particular choice of A works.

For a<b<c<r, the four-set sign packet is abc, abr, acr, bcr. The inherited
at-most-one-change axiom implies that two negative endpoints force the
whole packet negative. Thus the clauses saying a three-set witness implies
negative abc and bcr entail precisely the required root-containing cap.
For an old four-set a<b<c<d, the same argument applies to abc and bcd.
Reverse implications for these witness variables are unnecessary.

At old size three, `root_bad_contains` is the root-cap witness just
described. At size four it implies either its `old_fourcap` witness or one
of **all four** size-three deletion flags. This covers all root-cap triples
and the old four-cap itself. At size greater than four it implies one of
five one-vertex-deletion children. Every obstruction uses at most four old
vertices, so among any five distinct deleted vertices at least one lies
outside that obstruction. Hence at least one selected child retains it.
The source's `children` function deletes each vertex from the original
mask, not successively from a shrinking mask.

Induction on size proves both needed properties: a true flag entails an
actual obstruction, and assigning every flag its actual obstruction value
satisfies all these implications simultaneously. Size decreases strictly;
there is no cyclic support. All four-set children were allocated at size
three, and later mask children have smaller numerical masks and size at
least four, so the loop order supplies every referenced flag.

Every target containing r is already hit. Only old convex (n−1)-sets need
be considered in U−A. At size n−1 their flags alias the inherited exact Q
variables. Above that size, `old_target_contains` implies one of n deletion
children. Any (n−1)-set omits at least one of those n vertices. The same
descent and canonical-assignment argument therefore gives exact existential
containment semantics, despite the one-way clauses.

The root-preserving argument in [VERIFY_ROOTED.md](VERIFY_ROOTED.md) reduces
working D to 3≤|D|≤m−n+2: grow smaller solutions to three, and shrink larger
ones while keeping r so the complement has n−2 vertices. Consequently the
old selected range is **2≤|A|≤m−n+1**. Its old complements have size at most
m−3, exactly `bmax`. All recursive children stay inside their allocated
ranges. A missing flag below its obstruction's minimum size means false.
At m=n+1, every A has size two and its complement has size n−2; the failure
clauses are empty, correctly excluding a rooted counterexample.

Each final clause is `root_bad_contains(A) OR target_contains(U−A)`.
By witness soundness, satisfying all such clauses forces every retained
rooted D to fail. Conversely, if every retained rooted D fails, assigning
all flags their actual values satisfies every clause simultaneously.
Together with the range proof, the orientation projection is therefore
exactly failure of rooted Delta existence. No symmetry, orientation pin,
cube, or coordinate restriction is introduced by this executable. Its
checked parameter domain is 5≤n≤8 and n+1≤m≤16.

## Independent exact controls

[check_rooted_fast.py](check_rooted_fast.py) uses only this audit's own
integer oracle from [check_rooted.py](check_rooted.py), not a parent checker.
It enumerates caps by all-triple determinant signs and convex subsets by
integer hull arithmetic, verifies distinct x/general position and absence
of five-caps and forbidden n-gons, and enumerates all rooted masks. It
checks complete variable-map domains and every emitted clause.

| Map kind | Independent canonical interpretation |
|---|---|
| `orientation` | Positive exact determinant of the increasing triple |
| `convex` | Every vertex of the subset lies on its strict convex hull |
| `root_bad_contains` | A four-cap lies in the old subset together with r |
| `old_fourcap` | The old four-set itself is a four-cap |
| `old_target_contains` | An old target polygon is contained in the subset |

| m16 check | n7 | n8 |
|---|---:|---:|
| Variables | 69,630 | 71,632 |
| Clauses | 206,689 | 264,318 |
| Rooted pool clauses | 30,811 | 27,808 |
| False pool clauses / retained rooted working masks | 4,702 | 4,640 |
| All rooted working masks, including omitted sizes | 4,702 | 4,656 |
| Old four-caps / root-blocker triples | 68 / 3 | 224 / 56 |
| All targets / old targets | 279 / 217 | 168 / 0 |

All non-pool clauses were true. Each pool row's literals were matched to
its independently generated old mask and complement, and false mask lists
equaled those from the independently audited filtered formula. The 16 n8
working masks outside the range were explicitly repaired while retaining
the root. Thus 4,640 is the exact retained count; it is not the count of
all rooted working masks.

The n8/m16 fixture has no old heptagon, so that fixture alone does not
exercise a positive old-target flag. A separate 12-point fixture was formed
from a known ETV42 heptagon support and a later rightmost point, with other
old points added to make twelve. Its validity was then checked from the
integer coordinates, independently of the supplied support description.
It has 15 old heptagons and exercises both kinds of cap obstruction.

| Small real control | Pool / projection queries | False pool clauses | Old targets |
|---|---:|---:|---:|
| n6/m10, actual 15-point fixture subset | 372 | 181 | 22 |
| n7/m12 | 1,474 | 586 | 19 |
| n8/m12, including old heptagons | 1,012 | 682 | 15 |
| n7/m8 boundary | 21 | 21 | 0 |
| n8/m9 boundary | 28 | 28 | 0 |
| Total | **2,907** | | |

Each projection query fixes only the exact coordinate orientation and the
non-pool formula, then asks whether one gated failure clause can be
satisfied with freely chosen auxiliaries. All 2,907 answers agree with
direct hull/subset arithmetic: satisfiable exactly when that rooted mask
fails. Prior gates can be false and do not require other pool clauses.
These checks catch spurious one-way witnesses as well as missing canonical
ones on the tested fixtures. They used the local CaDiCaL195 interface as
finite diagnostics; its UNSAT answers are **not** claimed as certificates.
The written projection proof, not these examples alone, establishes the
general encoding argument.

## Results, provenance and limits

Full coordinates, false masks, repairs, phase counts, CNF/map hashes and
resource receipts are in [fast-real7.json](results/fast-real7.json),
[fast-real8.json](results/fast-real8.json) and
[fast-tiny.json](results/fast-tiny.json). The fresh build is recorded in
[fast-build.json](results/fast-build.json).

| Artifact | SHA-256 |
|---|---|
| Fresh specialized binary | `c39c2f30fe0a5dcf9e376b9ff578b8e14528f5af07f1b6319960b11de8cf6ca1` |
| n7/m16 CNF | `3fe3afb99c7d019a046e7ef61579f62cc603151792e2ee7f9cf431e5e03ce8f0` |
| n7/m16 map | `ac84216f821c98ce440956b6d5244578986917827037f3adffd969597a5af897` |
| n8/m16 CNF | `864fa52fd3d780907dfcba0f80590f80109f30a54937b529f9af66aed55cf61b` |
| n8/m16 map | `9066ef151bb65436f574ac55438e09b134549102a131a86e86490ec3de31b1f7` |

The build and m16 checks used checker SHA-256
`4d9aac3bdfe009e6ff0b513a32804fe99a3881ecd45049bf08ce94d6883cd864`,
preserved in [check_rooted_fast_pre_tiny.py](source/check_rooted_fast_pre_tiny.py).
Only the tiny-fixture assembly was then changed to ensure positive old-target
coverage; the executed tiny/final checker hash is
`aba748f31f31b0d394e6ce6ae2e8dacaf022801fac172433e0d6e3655ea4cbf9`.
The oracle hash for every run is
`ba57f7b11ec37b8f39ac855cf546011614a0f461d485e3595430d68724e6b162`.
Source and binary provenance were checked before each control, and source
hashes were unchanged after each run. No failed control was discarded or
rerun under different conditions.

All controls used one CPU, AS400 MiB, an 18-second CPU limit and external
20-second deadline. The compile used AS500 and took 0.842 seconds with
130,388 KiB peak child RSS. Real controls took 0.741 and 0.959 seconds;
the five tiny controls together took 0.250 seconds. Their maximum wrapper
RSS was 52,760 KiB. No long job was launched by this audit.

The parent reports that specialized n7/m14 and n8/m15 both ended UNKNOWN
after 300 seconds, with archived roundtrips. Those large traces were not
independently replayed or hashed here, and support no new certificate or
Delta conclusion. The ten independently replayed finite certificates in
[VERIFY_ROOTED.md](VERIFY_ROOTED.md) use the original filtered formula.
The specialized review is complete; any future SAT model or UNSAT proof
requires its own result-level check. Terminal/repair candidates are outside
this review. No universal all-size assertion is made.

For later reproduction only, run each mode separately with the research
venv Python under `timeout -s KILL 20s`: `check_rooted_fast.py build`,
`real7`, `real8`, or `tiny`. Generated large CNFs/maps and the binary remain
under `/home/jay/research/data/delta3-codex-20261113/selection/audit/fast`.
