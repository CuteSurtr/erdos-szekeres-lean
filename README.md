# Erdős–Szekeres bounds in Lean

This repository formalizes bounds for the Erdős–Szekeres problem in Lean 4.
It contains proofs of Suk's 2016 bound, the ordinary real-point case of the
Holmsen–Mojarrad–Pach–Tardos (HMPT) 2020 bound, the finite bound
**ES(8) ≤ 314**, and the classical lower bound
$`\mathrm{ES}(n)\ge2^{n-2}+1`$. Together, **65 ≤ ES(8) ≤ 314**.

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

**Finite octagon bound.** Every set of at least 314 points in general
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
| ES(8) ≤ 314 | `Omission.forces_convex_octagon_314` | [FinalCover314B61FusedR31Fused.lean](experiments/omission-global-assembly-2026-10-10/FinalCover314B61FusedR31Fused.lean) |
| ES(n) ≥ 2^(n-2) + 1 | `not_forcesConvexNGon_two_pow`, `conjecturedBound_le_of_forces` | [LowerBound/Construction.lean](ErdosSzekeres/LowerBound/Construction.lean) |
| ES(8) ≥ 65 | `octagon_lower_bound`, `sixtyFive_le_esNumber_eight` | [LowerBound/Construction.lean](ErdosSzekeres/LowerBound/Construction.lean), [LowerBound/Number.lean](ErdosSzekeres/LowerBound/Number.lean) |

The ES(8) ≤ 314 file also provides `Omission.convex_octagon_of_card_ge_314`, which
states the result directly for finite subsets of $`\mathbb R^2`$.

The lower bound shows that the formalized conjecture, `ErdosSzekeresConjecture`,
is equivalent to $`\mathrm{ES}(n)=2^{n-2}+1`$ for all $`n\ge3`$
(`erdosSzekeresConjecture_iff_isLeast`, `erdosSzekeresConjecture_iff_esNumber`).
Raising the lower bound for octagons above 65 would disprove that conjecture.

The asymptotic theorems do not assert the displayed estimates for every
small $`n`$. HMPT's extensions to pseudo-configurations and convex bodies
are outside the scope of this formalization.

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
certificates bound their sizes by 190 and 122. Hence the original set has
at most $`1+190+122=313`$ points. The
[assembly record](experiments/omission-global-assembly-2026-10-10/README.md)
contains the full theorem audit and reproduction instructions.

The repository also proves finite refinements of the HMPT counting
criterion and additional geometric omission inequalities. These are
explained in [math.md](math.md); they do not improve HMPT's asymptotic
coefficient.

## The open bound 313

**ES(8) ≤ 313 is not proved here.** The present route would suffice if the
residual population bound could be reduced from 122 to 121. In the
154-state representation, this means proving that at least 33 states are
missing.

The current research catalog contains 2,650 necessary omission inequalities.
The latest four have [complete Lean certificates](experiments/omission-residual32-rank-certificates-2026-10-10/README.md),
but no complete exclusion of assignments with at most 32 missing states has
been found. A proved normalization lemma also shows why the new cup-rank
bound alone does not strengthen feasibility of the abstract model.

These finite assignments encode necessary geometric conditions; satisfying
them does not establish a realization by points in the plane. The
[remaining-work note](docs/ES8_REMAINING.md) describes the unresolved steps.
Dated experiment directories preserve the individual proofs and search
records, including unsuccessful searches.

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

The commands above build the maintained library and check the residual
continuation. The large archived certificates for 314 have separate
reproduction instructions in the assembly record; they are not all rebuilt
by `lake build`. Some tests require optional solvers or explicit opt-in;
CI enables the required Lean integration checks. Build outputs and local
caches are ignored by Git.

## Attribution and license

The omission method, original state catalogs, and parts of the formal
infrastructure derive from Michael Schroeder's pinned version-1 archive.
The 23-point combinatorial theorem uses Baek's formal development. Full
sources and adaptations are documented in [THIRD_PARTY.md](docs/THIRD_PARTY.md).
No claim of literature priority or a best-known bound is made.

Original contributions are licensed under [Apache-2.0](LICENSE).
Third-party material retains its own licenses; see [NOTICE](NOTICE) and
[LICENSING.md](docs/LICENSING.md).
