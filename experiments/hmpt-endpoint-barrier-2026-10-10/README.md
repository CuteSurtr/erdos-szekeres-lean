# Endpoint obstruction for the current HMPT entropy criterion

[`HMPT/EndpointBarrier.lean`](../../ErdosSzekeres/HMPT/EndpointBarrier.lean) closes
one precise boundary case in the repository's analysis of the existing entropy
interface. For every fixed `c > 0`, it proves

```text
normalizedBudget c (8√2/3) n < 0  for all sufficiently large n.
```

Together with the earlier strict-below theorem, the new
`budget_eventually_negative_at_or_below_published` covers every coefficient
`C ≤ 8√2/3` at every fixed positive scale. This concerns the exact
`normalizedBudget` definition in `HMPT/Asymptotic.lean`. **It is not a lower
bound for Erdős–Szekeres numbers, an obstruction to other arguments, or a
claim about the new factorial counting criterion.** It does not contradict
the formalized HMPT theorem, which includes an arbitrary positive epsilon.

The finite theorem `normalizedBudget_neg_at_endpoint` has the explicit
sufficient conditions `n ≥ 9` and `c² log₂n ≥ 1`. With
`m = ceil(c sqrt(n log₂n))`, they imply `m² ≥ n`, hence
`log₂m ≥ (log₂n)/2`. The input exponent satisfies `d ≥ 4m+1`. Writing
`S = sqrt(n log₂n)`, the leading part of the unnormalized slack is at most

```text
3m (8√2/3) S − 16m² − 2S² = −(4m − √2 S)² ≤ 0.
```

The retained endpoint and rounding losses make the full slack strictly
negative. The proof uses the actual natural ceiling and the existing
geometric input exponent; it does not assume their asymptotic approximations.

The five theorem roots pass Lean and depend only on `propext`,
`Classical.choice`, and `Quot.sound`; see [axiom-audit.txt](axiom-audit.txt)
and [validation.json](validation.json). The underlying published coefficient
and proof are from [HMPT, final arXiv v3](https://arxiv.org/abs/1710.11415).
This artifact analyzes the repository's explicit implementation of that
argument; no literature-priority claim is made.
