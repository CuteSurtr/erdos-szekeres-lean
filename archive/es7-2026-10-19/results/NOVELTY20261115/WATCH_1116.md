# WATCH_1116: literature watch of 16 November 2026 (track LIT)

**Status: COMPLETE (bounded check), 16 Nov 2026, 18:25-18:43 KST.** No unit was started; no file outside this record
and the work directory below was written.
**Rigor: evidence only (bounded, read-only web check).** "Nothing new" means only "not found in this check"; it is
never a priority claim.

**Verdict in one line.** Nothing found since the 16 Nov 03:10 check changes a verdict of
[LOWERBOUND_EV_CHECK.md](LOWERBOUND_EV_CHECK.md) or [README.md](README.md):
- the newest public ES(8) upper bound is still Schroeder's 319 (Zenodo v1 only);
- the Mon 16 Nov arXiv announcement has nothing on Erdős–Szekeres;
- the two AI-agent repositories have been silent since 7 Oct and 20 Oct.

The full texts of the Baek–Balko (JCTA) and Balko–Valtr (EJC 2017) journal versions could not be read. Both exist only
on ScienceDirect, which answers automated clients with a CAPTCHA page (HTTP 403). The DDSZ journal version is behind a subscription. The open versions add one
"related" source for E2 (Baek–Balko §6.3) and confirm the existing wording. Nothing was filed in the claims folder:
there is no new result, counterexample or correction.

Scope (set by the wave-B plan): the sources that [LOWERBOUND_EV_CHECK.md](LOWERBOUND_EV_CHECK.md) and
[README.md](README.md) left unread.
1. arXiv announcements of Mon 16 Nov 2026 (math.CO, cs.CG, cs.DM, math.MG): Erdős–Szekeres, happy ending, convex
   position, cups and caps, order types, signotopes, saturation.
2. Schroeder's Zenodo record 22842891 (versions API); erdosproblems.com/107.
3. Public activity since 15 Nov in gotrevor/es7-ladder and GLitchfield/erdos-szekeres-convex-poly (read-only).
4. Journal versions: Baek–Balko (JCTA 2026), Damásdi–Dong–Scheucher–Zeng (Eur. J. Combin. 131 (2026) 104236),
   Balko–Valtr (Eur. J. Combin. 2017), for anything that changes the verdicts of LOWERBOUND_EV_CHECK.md.

Privacy: no request contained the owner's name, e-mail, GitHub user or the repository name.

## Verdicts

| # | source | checked (KST) | verdict |
|---|---|---|---|
| 1 | arXiv 16 Nov announcements (the only one out before 00:30 KST 17 Nov) | 18:26 | **nothing new** |
| 2a | Zenodo 22842891 versions; Schroeder's companion page | 18:28 | **nothing new** (still v1 only; 81 / 319) |
| 2b | erdosproblems.com/107 and its forum thread | 18:29 | **nothing new** (last edited 11 Apr 2026; newest comment 29 Dec 2025) |
| 3a | gotrevor/es7-ladder | 18:31 | **nothing new** (newest commit 7 Oct 2026) |
| 3b | GLitchfield/erdos-szekeres-convex-poly | 18:31 | **nothing new** (newest commit 20 Oct 2026) |
| 4a | Baek–Balko, JCTA 222 (2026) 106195 (CC-BY) | 18:33-18:38 | **full text not read** (ScienceDirect shows a CAPTCHA to automated clients; no other copy). From what is open: **nothing that changes a verdict**; one "related" addition for E2 (§6.3 heuristic) |
| 4b | DDSZ, EJC 131 (2026) 104236 | 18:36-18:38 | **not openly readable** (subscription). arXiv v3 (6 Oct 2025, after acceptance) re-checked: **nothing new**, verdicts stand |
| 4c | Balko–Valtr, EJC 66 (2017) 13-23 | 18:34-18:37 | **full text not read** (only on ScienceDirect, which turns automated clients away; the 2024 Wayback snapshot holds only the abstract). Extended abstract and data page: **nothing that changes a verdict**; the EV check's Balko–Valtr statements are confirmed |

## Details

### 1. arXiv, announcement of Monday 16 November 2026

- **Timing.** arXiv announces at 20:00 US Eastern, i.e. 10:00 KST. The Mon 16 Nov listing was the newest one during
  this check; the Tue 17 Nov listing appears at 10:00 KST on 17 Nov, after this track ends.
- **Listings read** (`/list/<cat>/new?show=2000`, all entries with abstracts, fetched 18:26 KST):

  | category | new | cross-lists | replacements |
  |---|---:|---:|---:|
  | math.CO | 29 (2611.17357-2611.18518) | 10 | 29 |
  | cs.CG | 0 | 0 | 2 |
  | cs.DM | 2 | 3 | 5 |
  | math.MG | 5 | 1 | 11 |

  cs.CG really had no new entry that day: its `/recent` page shows "Mon, 16 Nov 2026" with no entries.
- **Keyword scan** of every title and abstract (Szekeres, happy ending, convex position, cup/cap, order type,
  signotope, pseudoline, Bruhat, saturation, monotone path, ordered hypergraph, k-gon, hexagon/heptagon/octagon,
  general position): two hits, neither relevant.
  - arXiv:2611.17465, D. Poliakova, "Dimension bounds for higher Bruhat orders" (math.CO, new). Abstract: "We study
    the Dushnik-Miller dimension of higher Bruhat orders." Rank-3 signotopes are the elements of B(n,2), so this is
    the same object family, but the paper is about poset dimension. **Not relevant** to any project claim.
  - arXiv:2608.16127 (replacement), a Brualdi–Hoffman–Turán problem for odd wheels; "saturation" occurs only as
    "edge-spectral supersaturation". Not relevant.
  - The "Erdős" hits are the Erdős box problem (2611.17378), distinct subset sums (2611.17360), the Kleitman diameter
    theorem and random graphs.
- **arXiv site search**, sorted by announcement date (queries: Szekeres; signotope; happy ending; convex position;
  order type point; cups caps; saturation convex; convex polygon points general position). The index already holds
  16 Nov entries (IDs up to 2611.18299). No hit announced on 16 Nov concerns Erdős–Szekeres. The newest
  Erdős–Szekeres-type item is still 2610.28305 (20 Oct 2026, permutation patterns), as on 16 Nov at 03:10.
- **Verdict: nothing new.**

### 2. Schroeder's preprint and erdosproblems.com/107

- **Zenodo versions API** (`/api/records/22842891/versions?allversions=true&size=25`, 18:28 KST): `total: 1`. The
  only version is record 22842891, version "1", created and updated 2026-09-19T10:16 UTC. Files: `erdos_szekeres_upper_bounds_v1.pdf`
  (199,668 bytes, md5 f05d6b634f9cfe7e2d00074bc4524770) and `es7_es8_bounds_81_319_v1.zip` (240,352,401 bytes, md5
  a33769084584e44dbfaf26c7230dd13f). `/versions/latest` redirects to 22842891; a search on the concept id 22842890
  also returns one record.
- **Zenodo search** for new records (title "Szekeres", title "happy ending", description "convex heptagon", "convex
  octagon", "Erdős–Szekeres", "Erdos-Szekeres", newest first): nothing after 19 Oct 2026 (23485633, three and four
  dimensions, already known).
- **Schroeder's companion page** (18:29): still "Preprint · Version 1 · 19 September 2026", "We prove ES(7) ≤ 81 and
  ES(8) ≤ 319". The URLs `erdos_szekeres_upper_bounds_v2.pdf` and `_v3.pdf` next to the v1 PDF return HTTP 404.
- **erdosproblems.com/107** (18:29): "This page was last edited 11 April 2026." Comments (2), Proof claims (0), Proof
  expositions (0). The forum thread (`/forum/thread/107`) shows the same two comments (11 Dec and 29 Dec 2025, plus a
  deleted post of 29 Dec 2025) and "The ability to post new comments has been suspended."
- **Verdict: nothing new.** The newest public ES(8) upper bound is still Schroeder's 319.

### 3. The two public AI-agent repositories (GitHub REST API, unauthenticated, 18:30-18:31 KST)

- **gotrevor/es7-ladder.** `pushed_at` 2026-10-07T02:39:29Z (unchanged). Newest commit 2026-10-07T01:01:33Z,
  5da8c255b3 "PLAN: human-proof campaign closed below 1%". No commit since 1 Nov, no issue, no repository event.
  The account's other public activity since 15 Nov is automated daily pushes (about 08:01 UTC) to the forks
  `mathlib4`, `formal-conjectures` and `combinatorial-games`; the newest own repository is `positional-games`
  (4 Nov, Maker-Breaker games). Nothing on Erdős–Szekeres.
- **GLitchfield/erdos-szekeres-convex-poly.** `pushed_at` 2026-10-20T02:48:36Z (unchanged). Newest commit
  2026-10-20T02:48:35Z, d55c703bd3 "Drop the scoop and keep-internal passages; update references". `updated_at`
  2026-11-13T14:02 comes from a star by another user (a WatchEvent), not from content. No commit since 1 Nov, no issue.
  The account's newest public event is 31 Oct (another repository, `lean-lockstep`).
- **teorth/erdosproblems** (the database behind erdosproblems.com): no commit since 14 Nov; the newest is
  2026-11-12T20:33Z (automated formalization-status update).
- **Verdict: nothing new** in either repository since 15 Nov.

### 4. Journal versions

**Access.** Crossref and OpenAlex metadata (18:33):

| paper | journal record | licence (Crossref) | open copy |
|---|---|---|---|
| Baek–Balko, "The Erdős–Szekeres conjecture revisited" | JCTA 222, art. 106195, issue Aug 2026, online 30 Mar 2026 | CC-BY 4.0 (vor, from 26 Mar 2026) | only on ScienceDirect; not on arXiv (arXiv API: no Baek–Balko entry), not on either author's page (Balko's page links the DOI and slides only) |
| Damásdi–Dong–Scheucher–Zeng, "Saturation results around the Erdős–Szekeres problem" | EJC 131, art. 104236, Jan 2026, online 16 Sep 2025 | Elsevier TDM licence; "© 2025 Elsevier Ltd. All rights are reserved" | arXiv 2312.01223 v3 (6 Oct 2025, latest), SoCG 2024 |
| Balko–Valtr, "A SAT attack on the Erdős–Szekeres conjecture" | EJC 66 (2017) 13-23 | Elsevier open archive (from 1 Dec 2021) | only on ScienceDirect; extended abstract ENDM 49 (2015) 425-431 (EuroComb 2015 PDF); data page |

- **Baek–Balko on ScienceDirect.** The article URL and its PDF URL were requested once each with curl, which sent a
  browser-like User-Agent. Both answered HTTP 403 with the page "Are you a robot? Please confirm you are a human by
  completing the captcha challenge". WebFetch also got 403.
- **No further attempt.** The CAPTCHA was not attempted and no browser was started (this is a compute-free track, and a
  browser would carry its own profile's cookies). A later request to the Balko–Valtr article page was blocked by this
  session's permission check and was not retried.
- **Wayback Machine.** It has no snapshot of the Baek–Balko article. For Balko–Valtr, the CDX index shows ScienceDirect
  answering the archive's crawler with 403 on 12 May 2025, 1 Dec 2025 and 5 Oct 2026. Its one 200 snapshot (16 Apr 2024)
  holds only the abstract ("Under an Elsevier user license open archive"; the full text loads by script).

**4a. Baek–Balko (JCTA).** Read instead: the journal abstract (OpenAlex), the journal reference list (Crossref), the
SoCG 2025 version (LIPIcs 332:13, CC-BY, PDF of 15 pages, read for the passages below) and Balko's 82-slide talk.
- **Same results as SoCG.** The journal abstract is word for word the SoCG abstract, up to one comma.
- **Reference list.** The journal version cites 27 works. The SoCG version cites 24. The journal adds exactly three:
  - Biere et al., CaDiCaL/Kissat at the SAT Competition 2020;
  - Hubard–Montejano–Mora–Suk, "Order types of convex bodies" (Order, 2011);
  - Marić, the fast formal proof of the conjecture for at most 6 points (J. Autom. Reason., 2019).

  It cites neither DDSZ nor any other saturation paper, nor Schroeder, SMQH or Heule–Scheucher. This is indirect
  evidence only.
- **SoCG passages that bear on the verdicts (quoted from the PDF):**
  - Thm 8 and the remark after it: "every decomposable set of more than Σ_{i=k−a+2}^{u} C(k−2, i−2) points contains an
    a-cap, a u-cup, or k points in convex position. In particular, since every non-empty subset of a decomposable set
    is decomposable, we obtain, by choosing a = u = k, that every subset of more than 2^{k−2} points from a
    decomposable set contains k points in convex position." Decomposable (§4): "|P| = 1 or … P can be partitioned
    into two decomposable sets A and B such that A is deep below B." The class is closed under subsets, not under
    adding a point. **So E2's reading stands**: Thm 8 excludes only extensions that stay decomposable.
  - §2.3: "A natural candidate for a counterexample is a subset of the point sets that were used by Erdős–Szekeres …
    However, we prove that it is impossible to find a counterexample to Erdős–Szekeres Conjecture by restricting
    ourselves to these sets."
  - §3: "In our computer experiments, we were not able to find a signotope on at least 1 + Σ … vertices that would
    contain neither a red copy of P_a^3, nor a blue copy of P_u^3, nor a weak k-gon. … Such a generalization is
    equivalent to a conjecture of Goodman and Pollack [12]." This is already used in LOWERBOUND_EV_CHECK. The SoCG
    text names no parameters for these experiments.
  - §6.3, **not mentioned in LOWERBOUND_EV_CHECK:** "We implemented a simple program in Matlab based on a non-linear
    optimization solver to find as large (X, Y)-blow-up of a given point set as possible. … we used a solver based on a
    genetic algorithm that does not guarantee finding a true optimum solution. … we obtained many examples of 2^{k−2}
    points for various choices of S and k up to 20. Even though there is some freedom in choosing X and Y, the size of
    the (X, Y)-blow-up never exceeded 2^{k−2}." Their blow-up lemma (Lemma 14) is said to generalize "all previously
    known constructions".
- **Verdict.** Nothing changes a verdict of LOWERBOUND_EV_CHECK, as far as the open versions show. E2 gains one
  "related" source: §6.3 is a heuristic search for larger sets inside the blow-up family. It is not about one-point
  extensions, not at the order-type level and not certified, so E2 stays **not found in this search**.
- **Unconfirmed.** The JCTA full text may say more than SoCG §3 about the signotope experiments (parameters, solver)
  and about order types (the new Hubard et al. citation). A person with a browser should check these two places
  (item 1 of "What remains").

**4b. DDSZ (EJC).** The journal text is behind a subscription, so it was not read.
- arXiv v3 was submitted on 6 Oct 2025, after the journal record was created (16 Sep 2025). It is the newest open
  version, so most likely the accepted manuscript. This is an inference, not checked against the journal PDF.
- The v3 source was fetched (`src_v3.tar.gz`) and its `main.tex` was searched (119,120 characters). Occurrences:
  - "order type", "order-type", "realiz", "signotope", "pseudo": **0**;
  - "abstract": 6, all on the abstract (hypergraph) saturation number of monotone paths, Thm 5 /
    `thm:sat_p`;
  - "strong $n$-gon": 2, both inside the commented-out remark already quoted in LOWERBOUND_EV_CHECK ("It would be
    interesting to consider saturation problems for strong or weak $n$-gons.").
- The journal abstract (OpenAlex) matches v3: "The proof also shows that the original Erdős–Szekeres construction is
  indeed saturated. … In contrast to the geometric setting, we show that this abstract saturation number is always
  equal to the corresponding Ramsey number."
- **Verdict: nothing new.** E2 (DDSZ verifies one realization) and E4 (geometric half found in DDSZ Thm 4, abstract
  half not found) stand.

**4c. Balko–Valtr (EJC 2017).** Read instead: the ENDM 2015 extended abstract (EuroComb 2015 PDF), the data page
`kam.mff.cuni.cz/~balko/ES_SAT/` ("Last update: 28.11.2016") and the talk slides.
- Extended abstract, Thm 2.1: "We have ÊS(7) > 32 and ÊS(8) > 64." Also: "We found colorings that give N̂(5,6,7) ≥ 26,
  N̂(5,7,7) ≥ 27, N̂(6,6,7) ≥ 31, N̂(6,7,7) ≥ 32, and even N̂(7,7,7) ≥ 33. We also obtained the bound N̂(4,8,8) ≥ 23 that
  provides a counterexample to Conjecture 3.3 and to the Peters–Szekeres conjecture for k = 8."
- On pseudolinear (= signotope) colorings: "Considering only pseudolinear colorings in our experiments, we verified
  Conjecture 3.1 in the cases a = 4, u = k = 7 and a = 4, u = k = 8. That is, we have N(4, 7, 7) = 16 and
  N(4, 8, 8) = 22. For pseudolinear colorings, all our results matched the values from Conjecture 3.1." Final
  remarks: the pseudolinear Peters–Szekeres question and the Goodman–Pollack conjecture "remain open".
- The data page lists the colorings (K³₁₇ … K³₃₃ for 7-gons, K³₂₃ for 8-gons, K³₃₀ for 9-gons) and the generator.
- So the Balko–Valtr statements in LOWERBOUND_EV_CHECK hold as written: refutation at k = 7 and k = 8, N̂(6,6,7) ≥ 31,
  and the found colorings are not pseudolinear (implied by the last quote).
- The extended abstract says nothing on saturation or on one-point extensions of realized sets.
- **Verdict:** nothing changes a verdict. The full EJC version stays unread.

**Other checks on citing works.** Crossref, OpenAlex and Semantic Scholar list **0** citing works for both DDSZ
(journal) and Baek–Balko (journal), as in the 03:10 check. As then, this coverage is clearly incomplete.

## Consequences for wording

- **E2 (`lb-e1-stack1592`).** Unchanged: **not found in this search**. When related work is cited, add Baek–Balko
  §6.3 to DDSZ Prop. 14 and Baek–Balko Thm 8. §6.3 is a heuristic genetic-algorithm search for (X, Y)-blow-ups larger
  than 2^{k−2} (k ≤ 20, none found); it is not a one-point extension test and not at the order-type level.
- **E1, E3, E4, E5, U1.** Unchanged.
- **The "Why the level matters" paragraph.** Confirmed against the Balko–Valtr extended abstract: refutation at k = 7
  and k = 8; the pseudolinear (signotope) experiments matched the conjectured values at (4,7,7) and (4,8,8).

## Files

Work directory: `/home/jay/research/data/roadmap-20261115/watch-20261116/`. Everything there was fetched read-only
on 16 Nov 2026, 18:26-18:38 KST, about 7 MB in total.

| file | what | SHA-256 |
|---|---|---|
| `arxiv-new/new_math.CO.html` | arXiv math.CO /new, Mon 16 Nov | `d26b3b14573007d5d2c03738cb17cb666f5168d4e3d024fabf67319a6f3762a8` |
| `arxiv-new/new_cs.CG.html` | arXiv cs.CG /new | `90d73523afd74276d351a6dbcd2a39cb619e73738d5ebd12e95fca9780759a54` |
| `arxiv-new/new_cs.DM.html` | arXiv cs.DM /new | `a88a053359e2b41ccd9b972ffb72cef3c860a7206048dd780eb1cc9cb79ad248` |
| `arxiv-new/new_math.MG.html` | arXiv math.MG /new | `634b714341300cf1115a8fd4e118bdf68a424a8e6ce4907940605481c385b33d` |
| `arxiv-new/recent_cs.CG.html` | arXiv cs.CG /recent | `659d92066579e4ef7f23eae4303b04144375df8755ce1ece6331aa9bd00be51a` |
| `zenodo/versions.json` | Zenodo versions API, record 22842891 | `63493fb25c9a73f629ebafb81d14b932020381cfebceeabc2626a16b6ae8b269` |
| `zenodo/record.json` | Zenodo record 22842891 | `bcfccd81563f354554544e4464f635cd5028603610afe28d9dc2f84d103cee82` |
| `schroeder/companion.html` | Schroeder's companion page | `62cfbd5bf63d077987dc43dad637c5239afd039e22da33e5e2a92eeec4909b42` |
| `erdosproblems/p107.html` | erdosproblems.com/107 | `6c1e0efc373b01be3a992c9cf093624c822d246d0bf3de753f0c91945a3d1cf2` |
| `erdosproblems/t107.html` | forum thread 107 | `4c31d2b7c4582529bd586c35883466825816c53b79c655a6e640e51c269c402d` |
| `github/repo_gotrevor_es7-ladder.json` | GitHub repo metadata | `a98c6558e807417b151fadc58a470b7ab5c0df176ef7f9fea2d510280ccefa7f` |
| `github/repo_GLitchfield_erdos-szekeres-convex-poly.json` | GitHub repo metadata | `7f9557519f8e3364eeb3e11cadd9679fa58404b5330be843ac87c4a3daba6c0c` |
| `journals/crossref_10.1016_j.jcta.2026.106195.json` | Crossref, Baek–Balko JCTA (licence, 27 references) | `7f2c2c35b3e3aadda21935209332f693b924dca328219d19822462e7f875fe39` |
| `journals/openalex_10.1016_j.jcta.2026.106195.json` | OpenAlex, Baek–Balko JCTA (abstract) | `40c01e3576a37992e351222d6573400e25140b163ecab3e152eabf8fed33b01a` |
| `journals/crossref_10.1016_j.ejc.2025.104236.json` | Crossref, DDSZ EJC | `32b2dfa6c9e226092507b96c9a7eeeddde1f30cee53b33957927ca96eaf051cc` |
| `journals/openalex_10.1016_j.ejc.2025.104236.json` | OpenAlex, DDSZ EJC (abstract) | `bdbd7337ac99a5ba2692fa61b869223ec8a34b325c78610afc46753c2ea23116` |
| `journals/crossref_10.1016_j.ejc.2017.06.010.json` | Crossref, Balko–Valtr EJC | `408f345d7bf27ac346143ec80a1e50c1e2307a7dca2976aa923b633a4147ee97` |
| `journals/bb_socg/socg.pdf` | Baek–Balko SoCG 2025 (LIPIcs 332:13) | `fec52a974558c0a76e9e72e6f60dc0b6c65ee690d21acc3a8febd23bf9fbaf8f` |
| `journals/bb_socg/slides.pdf` | Balko's talk slides | `c13c5561f15058b5a4e49e93b44fec0c5d60d1780f9e69b0647535b0b418e818` |
| `journals/ddsz/src_v3.tar.gz` | DDSZ arXiv v3 source | `fd33fbdb20e2159521f90b128894d7c977ba953e6edf3effc52bc27634ca014f` |
| `journals/bv2017/endm1938.pdf` | Balko–Valtr ENDM 2015 extended abstract | `e5aff12d152faa0708bc641335302920439d3d4652914c5510bddf7e8211b5c1` |
| `journals/bv2017/es_sat.html` | Balko–Valtr data page | `42a1f678863274ac649881ef3d977e8744f1d4258003e2f2fe96bf180895e7c7` |
| `journals/bv2017/wb_20240416.html` | Wayback snapshot of the EJC 2017 page (abstract only) | `18a2d303bc847bb23c3bb9c8fdbd0a650248c9b6ef2e5a2d21b04caf48747a13` |

The parser used for the arXiv listings is `watch-20261116/tools/parse_list.py` (SHA-256
`5894310ee8ac2a78f19835cda3d906a4ad3b6a3a80573aeb5db32a7a42280db9`; keyword list as in §1).

## What remains

1. **The full texts of Baek–Balko (JCTA 222, 106195; CC-BY) and Balko–Valtr (EJC 66, 13-23; open archive).** Each
   needs a person to open it in a browser at `https://doi.org/10.1016/j.jcta.2026.106195` and
   `https://doi.org/10.1016/j.ejc.2017.06.010`. In JCTA, look at:
   - the open-problems section (signotope experiments: which (a, u, k) and N, which solver);
   - the sentence that cites Hubard–Montejano–Mora–Suk, "Order types of convex bodies";
   - any statement on one-point extensions or saturation.
2. **The DDSZ journal PDF** (subscription). Its only expected differences from arXiv v3 are copy edits.
3. **arXiv announcements of Tue 17 Nov and later.** The Tue 17 Nov listing appears at 10:00 KST on 17 Nov, after this
   track ends. Re-run the four `/list/<cat>/new` fetches and the keyword scan (Resume below).
4. Out of scope tonight and still unread, as listed in LOWERBOUND_EV_CHECK: Aichholzer–Krasser on abstract order-type
   extension, Schroeder's proof archive, and the remaining GLitchfield documents.

## Resume

```bash
W=/home/jay/research/data/roadmap-20261115/watch-20261116
for c in math.CO cs.CG cs.DM math.MG; do
  curl -sS -A "Mozilla/5.0 (literature-watch)" -o $W/arxiv-new/new_${c}_$(date +%m%d).html "https://arxiv.org/list/$c/new?skip=0&show=2000"
  python3 -I $W/tools/parse_list.py $W/arxiv-new/new_${c}_$(date +%m%d).html | grep -v 'hits=\[\]'
done
curl -sS "https://zenodo.org/api/records/22842891/versions?allversions=true&size=25" | python3 -I -c 'import json,sys; print(json.load(sys.stdin)["hits"]["total"])'
curl -sS https://api.github.com/repos/gotrevor/es7-ladder | python3 -I -c 'import json,sys; print(json.load(sys.stdin)["pushed_at"])'
curl -sS https://api.github.com/repos/GLitchfield/erdos-szekeres-convex-poly | python3 -I -c 'import json,sys; print(json.load(sys.stdin)["pushed_at"])'
```

Use unauthenticated requests: `gh` would identify the owner's GitHub account.
