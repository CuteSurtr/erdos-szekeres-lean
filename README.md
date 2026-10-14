# Erdős–Szekeres bounds in Lean

This repository formalizes bounds for the Erdős–Szekeres problem in Lean 4.
It contains proofs of Suk's 2016 bound, the ordinary real-point case of the
Holmsen–Mojarrad–Pach–Tardos (HMPT) 2020 bound, the finite bound
**ES(8) ≤ 312**, and the classical lower bound
$`\mathrm{ES}(n)\ge2^{n-2}+1`$. Together, **65 ≤ ES(8) ≤ 312**.

All results concern finite subsets of the real plane in general position:
no three distinct points are collinear. A convex polygon may contain other
points of the set in its interior.

The [mathematical exposition](math.md) gives the definitions, statements,
and proofs, with references to the corresponding Lean declarations. The
[paper-to-Lean correspondence](docs/PAPER_MAP.md) records which parts of
Suk's and HMPT's papers are formalized and where the proofs use different
intermediate arguments.

## Main results

Write $`\mathrm{ES}(n)`$ for the least number of points that forces a convex
$`n`$-gon. All logarithms below are to base two.

**Suk's bound.** For all sufficiently large $`n`$,

```math
\mathrm{ES}(n)\le
\left\lfloor 2^{\,n+6n^{2/3}\log_2 n}\right\rfloor.
```

**HMPT's bound.** For every $`\varepsilon>0`$ and all sufficiently large
$`n`$ (depending on $`\varepsilon`$),

```math
\mathrm{ES}(n)\le
\left\lfloor 2^{\,n+(8\sqrt2/3+\varepsilon)\sqrt{n\log_2 n}}\right\rfloor.
```

**Finite octagon bound.** Every set of at least 312 points in general
position contains eight points in convex position.

**Erdős–Szekeres lower bound.** For every $`n\ge3`$ there are $`2^{n-2}`$
points in general position with no $`n`$ points in convex position. Hence
$`\mathrm{ES}(n)\ge2^{n-2}+1`$; for octagons, 64 points do not suffice and
$`\mathrm{ES}(8)\ge65`$.

The following declarations have complete proofs. Names in the table are
relative to the namespace `ErdosSzekeres`.

| Result | Main declaration | Source |
| --- | --- | --- |
| Suk | `Suk.theorem2016` | [Suk/Asymptotic.lean](ErdosSzekeres/Suk/Asymptotic.lean) |
| HMPT | `HMPT.theorem2020` | [HMPT/Asymptotic.lean](ErdosSzekeres/HMPT/Asymptotic.lean) |
| ES(8) ≤ 312 | `Omission.forces_convex_octagon_312` | [Final312/Final.lean](experiments/omission-final312-2026-10-13/Final312/Final.lean) |
| ES(8) ≤ 313 (earlier) | `Omission.forces_convex_octagon_313` | [Final313/Final.lean](experiments/omission-final313-2026-10-11/Final313/Final.lean) |
| ES(8) ≤ 314 (earlier) | `Omission.forces_convex_octagon_314` | [FinalCover314B61FusedR31Fused.lean](experiments/omission-global-assembly-2026-10-10/FinalCover314B61FusedR31Fused.lean) |
| ES(n) ≥ 2^(n-2) + 1 | `not_forcesConvexNGon_two_pow`, `conjecturedBound_le_of_forces` | [LowerBound/Construction.lean](ErdosSzekeres/LowerBound/Construction.lean) |
| ES(8) ≥ 65 | `octagon_lower_bound`, `sixtyFive_le_esNumber_eight` | [LowerBound/Construction.lean](ErdosSzekeres/LowerBound/Construction.lean), [LowerBound/Number.lean](ErdosSzekeres/LowerBound/Number.lean) |

The ES(8) ≤ 312 file also provides `Omission.convex_octagon_of_card_ge_312`, which
states the result directly for finite subsets of $`\mathbb R^2`$.

The lower bound shows that the formalized conjecture, `ErdosSzekeresConjecture`,
is equivalent to $`\mathrm{ES}(n)=2^{n-2}+1`$ for all $`n\ge3`$
(`erdosSzekeresConjecture_iff_isLeast`, `erdosSzekeresConjecture_iff_esNumber`).
Raising the lower bound for octagons above 65 would disprove that conjecture.

The asymptotic theorems do not assert the displayed estimates for every
small $`n`$. HMPT's extensions to pseudo-configurations and convex bodies
are outside the scope of this formalization.

## Comparison with the literature

As of **14 October 2026**, our search of the literature and public preprints
(see the [survey](docs/RELATED_WORK_2026-10-14.md)) found no earlier general
bound as strong as **ES(8) ≤ 312**; the best published value is 408
(Mojarrad–Vlachos 2016). To the best of our knowledge, it is a new best-known
upper bound for ordinary real planar point sets in general position. This is a dated literature assessment, not
a guarantee of priority or a claim of external peer review.

The strongest directly comparable prior announcement we located is
**ES(8) ≤ 319**, Theorem 1.1 of Michael Schroeder's
[*Erdős–Szekeres: Upper Bounds for Convex Heptagons and Octagons*](https://michaelschroeder.ai/research/ErdosSzekeres/erdos_szekeres_upper_bounds_v1.pdf)
(version 1, 19 September 2026). The present bound improves that threshold by
six points. It builds on Schroeder's omission method, state catalogs and
geometric formalization, with additional inequalities and stronger exact
certificates developed here.

Baek and Balko's
[*The Erdős–Szekeres Conjecture Revisited*](https://doi.org/10.1016/j.jcta.2026.106195)
proves the conjectured threshold for decomposable sets and a split-polygon
variant; it does not give the threshold 65 for arbitrary point sets. The
[detailed comparison](math.md#12-literature-comparison) discusses these
distinctions and the reported 324 bound. The result here is a finite
improvement at $`n=8`$; it does not improve Suk's or HMPT's asymptotic bounds.

## Proofs and supporting material

The lower bound is the Erdős–Szekeres construction of 1961. Blocks are
stacked far above or far below one another, and every convex subset of the
union is controlled by its cups and caps in the individual blocks; a fourth
point inside a triangle rules out every other configuration. The proof is
explained in [§1.1 of the exposition](math.md#11-the-classical-lower-bound).
With `--json`, [es_lower_bound_witness.py](scripts/es_lower_bound_witness.py)
prints exact integer coordinates of the 64-point octagon-free witness; it is
a numerical control, not part of the proof.

The asymptotic proofs combine geometric extraction, counting, and explicit
parameter estimates. Their detailed correspondence with the published
arguments is given in the [Suk](docs/SUK.md) and [HMPT](docs/HMPT.md) proof
notes.

The octagon proof uses the omission method. A projective transformation
removes one point and reduces an octagon-free set to two configurations,
called balanced and residual. Geometric inequalities and exact integer
certificates bound their sizes by 189 and 121. Hence the original set has
at most $`1+189+121=311`$ points. The residual bound 121 uses a 2,650-row
catalog of proved geometric inequalities; for a nonempty residual
configuration, geometric rank attainment ensures that state zero is occupied,
and an exact certificate with 437,579 weighted leaves excludes every such
assignment with at most 32 missing states
([313 record](experiments/omission-final313-2026-10-11/README.md)). The
balanced bound 189 uses the 3,131-row balanced catalog and a 93,988-leaf
certificate forcing at least 63 of its 252 states to be missing
([312 record](experiments/omission-final312-2026-10-13/README.md)). Both
records contain the certificates, kernel-check records and reproduction
instructions; the earlier [314 assembly](experiments/omission-global-assembly-2026-10-10/README.md)
used the bounds 190 and 122.

The repository also proves finite refinements of the HMPT counting
criterion and additional geometric omission inequalities. These are
explained in [math.md](math.md); they do not improve HMPT's asymptotic
coefficient.

## Beyond 312

No bound below 312 is claimed here. The 313 and 312 certificates are far
larger than the earlier ones: their complete Lean kernel checks take about
120 and 58 CPU-hours, so they were run on one machine rather than in the
hosted CI workflow; the [313](experiments/omission-final313-2026-10-11/README.md)
and [312](experiments/omission-final312-2026-10-13/README.md) records explain
how to repeat them. A [survey of related work](docs/RELATED_WORK_2026-10-14.md)
places these values next to the published bounds. On the lower side, an
[exact computation](experiments/es8-lower-bound-search-2026-10-11/README.md)
shows that the 64-point lower-bound witness and 1,232 further stacking
constructions cannot be extended to 65 points without a convex octagon;
this does not exclude other 65-point sets. Dated experiment directories
preserve the individual proofs and search records, including unsuccessful
searches; the [remaining-work note](docs/ES8_REMAINING.md) summarizes them.

## Verification

The project uses **Lean 4.24.0** and **Mathlib v4.24.0**, with dependency
revisions pinned in [lake-manifest.json](lake-manifest.json).

```sh
lake exe cache get
lake build --wfail
lake env python3 scripts/check_axioms.py
python3 -m unittest discover -s scripts -v
lake env python3 scripts/check_residual32_continuation.py
```

The finished proofs contain no `sorry` or `admit`. The
[saved library audit](docs/validation/axiom-audit-lower-bound-2026-10-11.txt)
checks 587 named theorems and permits only `propext`, `Classical.choice`,
and `Quot.sound`. The [validation guide](docs/VALIDATION.md) records the
scope of these checks and the separate audits of the finite certificates.

The 313 theorem was kernel-checked on 12 October 2026. Its
[final axiom report](experiments/omission-final313-2026-10-11/final-audit.out)
contains only those same three axioms; the theorem retains no unproved
geometric or arithmetic hypothesis. The
[certificate record](experiments/omission-final313-2026-10-11/README.md)
provides source hashes, per-module check records and reproduction instructions.
A complete rebuild requires roughly 120 CPU-hours.

The commands above and [hosted CI](.github/workflows/ci.yml) build the maintained
library and check the residual continuation. **They do not rebuild the large
313 certificate or all archived 314 certificates.** Their verification is
recorded separately. Some tests require optional solvers or explicit opt-in;
CI enables the required Lean integration checks. Build outputs and local caches
are ignored by Git.

## Attribution and license

The omission method, original state catalogs, projective reduction,
minimum-slope partition and substantial parts of the geometric formalization
derive from Michael Schroeder's
[version-1 archive](https://doi.org/10.5281/zenodo.22842891). These are adapted
foundations of the 313 proof, not independently discovered methods. The
additional omission inequalities, strengthened certificates and their local
Lean verification are described in [math.md](math.md). The 23-point
combinatorial theorem uses Jineon Baek's formal development. Full sources,
adaptations and retained licenses are documented in
[THIRD_PARTY.md](docs/THIRD_PARTY.md); no endorsement by the original authors
is implied.

Original contributions are licensed under [Apache-2.0](LICENSE).
Third-party material retains its own licenses; see [NOTICE](NOTICE) and
[LICENSING.md](docs/LICENSING.md).
