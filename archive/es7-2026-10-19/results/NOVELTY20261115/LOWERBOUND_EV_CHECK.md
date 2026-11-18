# LOWERBOUND_EV_CHECK: literature check of the evening lower-bound results (16 November 2026)

**Status: complete (bounded search), 16 Nov 2026, 03:10 KST.**
**Rigor: evidence only (bounded literature search).**

- Verdict words are those of [DELTA_PM_CHECK.md](DELTA_PM_CHECK.md):
  - "found": a source states the claim, a stronger one, or something that gives it in one step;
  - "related": a close analogue or the same device;
  - "not found in this search".
- "Not found" is never "new" and never a priority claim.
- Claims are worded as in [LOWERBOUND_RUN_1115EV.md](../ROADMAP20261115/LOWERBOUND_RUN_1115EV.md) and the "Lower bounds" table of
  [STATUS20261115_2300](../STATUS20261115_2300/README.md).
- Nothing was committed, posted or sent.

## Verdict in brief

| claim | statement (short) | verdict | closest source |
|---|---|---|---|
| E1 `lb-e1-octdel65` | the octagon-vertex deletions of the 7 stacking one-octagon 65-point sets (and of AE65) do not extend, at the order-type level | **not found in this search** | AlphaEvolve (arXiv:2511.02864 v3, §38) only reports that near misses with 2^(k−2)+1 points and one convex k-gon exist for k ≤ 8 (background) |
| E2 `lb-e1-stack1592` | none of the 1,592 stacking-family order types extends, at the order-type level | **not found in this search**; related: DDSZ Prop. 14 | see "E2" below. **The plan's open question is answered: neither DDSZ Prop. 14 nor Baek–Balko covers E2.** |
| E3 `lb-e1-absat7` | none of 10,457 heptagon-free 32-point sets extends to 33 points | **related** (must cite): the same check at the same k is public, on different and far fewer sets | GLitchfield EXTENSION.md (171 sets); es7-ladder LOCALITY.md (solver-found abstract models); DDSZ (one realization of the ES construction) |
| E4 `lb-e1-ddsz28` | the 28-point DDSZ-type set is geometrically 7-gon-saturated, while its abstract one-point extension exists | **split.** Geometric half and consequence (a) "saturated ≠ maximum": **found** (DDSZ Thm 4). Abstract half and consequence (b) "abstract non-extendability is strictly stronger than geometric saturation": **not found in this search** | DDSZ Thm 4; related to (b): DDSZ Thm 5 and Problem 24 |
| E5 `lb-e1-miner766` | no 31-point (7,6,6) set inside 10,593 realized 32-point heptagon-free sets | **not found in this search** (nobody reports this negative search) | context: es7-ladder lists P(7,6,6) at 31 points as an open rung; Schroeder v1 Prop. 5.6 gives 30 ≤ C₇ ≤ 49 |
| U1 | a public ES(7) or ES(8) upper bound newer than Schroeder's 81 / 319, posted after 14 Nov 19:20 UTC | **not found in this search** | Zenodo record 22842891 still has one version (v1, 19 Sep 2026) |

## Details

**E2.** DDSZ (Damásdi–Dong–Scheucher–Zeng, "Saturation results around the Erdős–Szekeres problem", arXiv:2312.01223
v3; SoCG 2024; Eur. J. Combin. 131 (2026) 104236) is the closest source.
- **What Prop. 14 says.** Very generic (i+1, n+1−i)-cup-cap-saturated blocks Pᵢ are flattened and placed in small
  discs around (i, i²), under metric conditions I–VI with ε ≫ δ. Then the union is n-gon-saturated.
- **The remark after it.** Maximum (k,l)-cup-cap-free sets are automatically saturated, so "our Proposition 14 implies
  that the construction of Erdős and Szekeres is also n-gon-saturated".
- **§1.3** (quoted from the v3 LaTeX by two searchers): "The proof also shows that the original Erdős–Szekeres
  construction in [ES61] is indeed saturated. As far as we know, this is widely believed (for otherwise the
  Erdős–Szekeres conjecture would be disproved immediately) but never been verified in the literature since its
  existence from 1961."
- **What Prop. 14 gives.** Geometric saturation of **one** flattened realization of each ES-type stacking of maximum
  blocks along a cup. A verifier read the v3 LaTeX in full: DDSZ never mention order types, other realizations or
  abstract extensions. E2 is stronger in two ways: it covers every realization, and it covers 1,592 order types. Prop. 14
  does not apply at all to any of these types whose outer arrangement is not a cup (not checked here).
- **Baek–Balko** (SoCG 2025, LIPIcs 332:13; the full text has no "saturat" and no "maximal"). Their Thm 8 says the
  conjecture holds inside decomposable sets. This rules out only extensions that stay decomposable.

**E3.** Two public AI-agent research notes ran the same one-point-extension check at k = 7. The main session re-read
both passages in the files fetched on 16 Nov.
- **GLitchfield**, `docs/research/archive-2026-09-28-to-10-05/claude-extremal-20261005/extension/EXTENSION.md`
  (5 Oct 2026). The file header says "[C] = computed, diagnostic, not Lean". Lines 58-59: "k = 7. The
  heptagon-free-extension SAT search ran on 19 constructions and 152 flip-walk sets, 33 positions each: 5,643 of 5,643
  UNSAT."
- **es7-ladder**, `docs/LOCALITY.md`, lines 47 and 52. One-point extension of solver-found 32-vertex models, "66 tries,
  all UNSAT". Line 52: "The solver-found extremal configurations are **saturated even without the axiom** … The same
  holds at ES(7)'s 32-vertex models." These are abstract models, not realized point sets.
- **Not found:** the project's families (2 symmetric maxima, 7 AE33 deletions, 1,911 near-full deletions, 8,537 pool
  sets), at this scale, with cake_lpr-checked proofs and a written encoder soundness proof.
- **Context.** Szekeres–Peters proved the abstract statement for k = 6 and call k = 7 "out of reach". SMQH §6.2: no
  realizable 32-point 7-gon-free set has 4-fold rotational symmetry.

**E4.** Three verifiers confirmed this from the v3 text.
- **Thm 4 at n = 7** gives a 28-point 7-gon-saturated set, so sat_g(7) ≤ 28 < 32 ≤ ram_g(7). The blocks have sizes
  1+5+8+8+5+1, using the 8-point (4,5)-cup-cap-saturated set of Thm 11 and its mirror image.
- **So the project's E7-1.5 run is a re-check of DDSZ on the project's own coordinates.** The DDSZ guarantee covers
  their construction with ε, δ small enough.
- **Not in DDSZ:** signotopes, order types, or abstract extensions of n-gon-free sets.
- **Nearest to (b):**
  - Thm 5: for monotone paths in arbitrary 2-colourings, the saturation number equals the Ramsey number, "in contrast to
    the geometric setting". This concerns a weaker abstraction, and cups/caps, not k-gons.
  - Problem 24 asks the version for transitive colourings and leaves it open.
  - A remark commented out in the LaTeX source reads: "It would be interesting to consider saturation problems for strong
    or weak $n$-gons."
- **Schroeder v1 §1.1** restates (a) in words, citing DDSZ (related).

**E5.**
- es7-ladder README and PLAN.md §9 list P(7,6,6) at 31 points as an open rung. "P(7,6,6)@30 SAT in 3.0 s"; probes at 31
  points mostly timed out, and the rung is estimated at ≥ 17,000 CPU-h.
- Balko–Valtr: abstract colourings with N^(6,6,7) ≥ 31 exist; none is pseudolinear.
- The project's negative subset search agrees with all of this and is stated nowhere.

**U1.** Three searchers checked these sources; none shows a newer bound.
- The Zenodo versions API for record 22842891 returns total = 1 (v1, 19 Sep 2026). The companion page still says 81 and
  319.
- arXiv November listings of cs.CG, math.CO, cs.DM and math.MG, up to the Fri 13 Nov announcement: nothing relevant.
- erdosproblems.com/107: last edited 11 Apr 2026, comment posting suspended.
- es7-ladder: last push 7 Oct. GLitchfield: last activity 20 Oct.
- So ES(8) ≤ 310 (Lean-checked) and the ≤ 308 chain (unrefereed) are still not found in public.

## Consequences for wording

- **E2.** State it as a strengthening of DDSZ's remark: DDSZ verify one realization of the ES construction; the
  certificates here cover every realization of 1,592 stacking order types. Cite Prop. 14 and the §1.3 sentence.
- **E3.** Cite GLitchfield EXTENSION.md and es7-ladder LOCALITY.md as earlier public runs of the same check at k = 7.
  What is added here is scale, certified proofs and the soundness proof.
- **E4.** Present the 28-point saturation as a re-check of DDSZ Thm 4. Only the abstract extension, and hence the gap
  between abstract and geometric saturation, was not found.
- **Why the level matters for E1-E3.** Balko–Valtr have abstract 2-colourings that refute Peters–Szekeres at k = 8, and
  abstract 33-vertex 7-gon-free configurations; none is pseudolinear. Non-extendability statements like E1-E3 therefore
  depend on the order-type (signotope) level of the encoder. Baek–Balko found no signotope counterexample; they note
  that the signotope version is equivalent to a conjecture of Goodman and Pollack.
- **Bounds.** None of E1-E5 changes a bound. By the E4 calibration they remain weak evidence for ES(7) = 33 and
  ES(8) = 65.

## Method and coverage

- **Workflow.** `novelty-evening-1115` (run `wf_eeaa6709-1ec`, 31 min). Four read-only searchers, each with its own
  approach:
  - papers read in full text;
  - citers and recent arXiv;
  - sites and semantic search;
  - an adversarial prior-art attacker.
  Together they ran 231 queries. Three verifiers then opened every source a searcher marked "states/implies", plus two
  checks fixed in advance (DDSZ Prop. 14; Baek–Balko): 13 checks on 3 sources, all opened, all quotes confirmed.
- **Limits.**
  - arXiv API timeouts and HTTP 429; Google Scholar blocked.
  - The citer lists for DDSZ and Baek–Balko from Semantic Scholar, OpenAlex and OpenCitations were empty, which is
    clearly incomplete. A paper that discusses saturation only in its body would be missed.
  - Quotes the searchers marked "secondary" (WebFetch summaries) were not re-checked, apart from the two E3 passages.
- **Unread:**
  - the Baek–Balko JCTA 2026 full version;
  - the DDSZ journal version (arXiv v3 was read);
  - the Balko–Valtr EJC 2017 full version;
  - Aichholzer–Krasser on abstract order-type extension;
  - Schroeder's proof archive;
  - arXiv announcements of Mon 16 Nov 2026;
  - the remaining GLitchfield documents.

## Files (`/home/jay/research/data/roadmap-20261115/novelty-ev-20261116/`)

| file | SHA-256 |
|---|---|
| `workflow_result.json` (all searcher and verifier outputs, verbatim) | `751fc35e30b7ea44930663b5058ae080cf8326b6d93d3b71dd39faf0e666dbc2` |
| `GLitchfield_EXTENSION_20261116.md` (as fetched) | `9fa4291060bd4fbe3dd6d138d014a0ddaa3c970af1597e08969669c5983479d0` |
| `es7-ladder_LOCALITY_20261116.md` (as fetched) | `a2af6a6383e18c617773ec508f6045577cba9993190cd72bfdbf757e7cdfe594` |

Per-agent journal: `~/.claude/projects/-home-jay-research-lean-erdos-szekeres-lean/1e71bc06-5c09-4f54-ae48-3fca76aaa352/subagents/workflows/wf_eeaa6709-1ec/journal.jsonl`.
