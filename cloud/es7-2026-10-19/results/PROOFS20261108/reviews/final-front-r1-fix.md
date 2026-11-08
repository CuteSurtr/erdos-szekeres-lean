# Front matter fix, final pass, round 1

Files edited: `proofs.tex` and `preamble.tex` (paths relative to STAGE). `bibliography.tex` is unchanged. Snapshot of the
previous versions: `snapshots/final-r1-pre/` (proofs.tex, preamble.tex, bibliography.tex). No section file, section map
or `appendix_map.tex` was edited, and `tools/make_appendix.py` was not run.

Result: 3 findings; 3 fixed, 0 declined. No statement environment was touched and no label was added, removed or
renamed, so the maps need no change. The Lean declarations behind the new claims were re-read in REPO (commit
`7e32ee259`): `ErdosSzekeres.Suk.convexPosition_of_strict_supports` (`ErdosSzekeres/Suk/SupportingLines.lean:28`),
`ErdosSzekeres.Omission.Configuration` (`ErdosSzekeres/Omission/Realization.lean:9`) and `Configuration.HasCap`
(`ErdosSzekeres/Omission/Realization.lean:64`).

## Per finding

### 1. [minor] proofs.tex:91, "Works cited": citation forms — fixed

Check. All inline citations in the current section files:
- author with title: R. T. Rockafellar (ll.tex:88), W. Rudin (fd.tex:1197, lg.tex:164), J. Baek (mb.tex, Source item; sa.tex:416),
  P. Erdős and G. Szekeres (mb.tex, cups-caps theorem);
- author with arXiv number: B. Dumitru (sr.tex, arXiv:2512.24061), Subercaseaux, Mackey, Qian and Heule (sr.tex,
  arXiv:2506.00224), J. Baek (sr.tex, arXiv:2206.04260);
- author alone: "M.~Schroeder's archive" (mb.tex:47, the only mention of the archive in the sections);
- by name, without authors: Lean 4 and Mathlib (e.g. fd.tex:5-6).
No other published work is cited in the sections (searched for author names, "et al", journal abbreviations,
"op. cit."), so "the References list them" stays true. The finding is right.

The finding's suggested wording ("by author together with title or arXiv number, or by name") would leave the
Schroeder case to "by name", which reads as the name of a work. The new wording names that case separately.

- Old: `The sections cite published works inline, by author and title; the References list them. They are: Lean~4`
- New: `The sections cite published works inline, by author together with title or arXiv number, by author alone or by`
  `name; the References list them. They are: Lean~4`

The source line is split in two, so that the following lines stay byte-identical. Rendered (p.4): "The sections cite
published works inline, by author together with title or arXiv number, by author alone or by name; the References
list them."

Left unchanged: the header comment of `bibliography.tex` (line 1) also says "The sections cite them inline, by author and
title". It is a source comment, not rendered, and outside the finding, so under the byte-identical rule it was not
touched. A later pass may want to align it.

### 2. [minor] proofs.tex:39-42, "Treated here": main-library restatements outside fd and mb — fixed

Check. `\leanref` entries in statement heads that cite a main-library file (`\leanref{...}{ErdosSzekeres/...}`) occur in
fd (31), mb (35), mm (2) and sr (1), and in no other section (the maps agree):
- mm.tex:148, `mm:def:config`: `ErdosSzekeres.Omission.Configuration` (`Realization.lean:9`) and
  `ErdosSzekeres.Omission.Configuration.HasCap` (`Realization.lean:64`). `MIRRORETV/lean/MirrorMain.lean` uses both
  (e.g. `capacity16`, line 1529).
- sr.tex:638, `sr:lem:supports`: `ErdosSzekeres.Suk.convexPosition_of_strict_supports` (`SupportingLines.lean:28`),
  the same declaration as `fd:lem:strict-supports`. `SYMLEAN/SymmetricReduction.lean:511` applies it.
Hashes: sr's Sources list gives `ErdosSzekeres/Suk/SupportingLines.lean: 6a8e12677685`, and mm's Sources list gives
`ErdosSzekeres/Omission/Realization.lean (ae4970e0808e...)`. Both match `shasum -a 256` of the REPO files.
For each of fd, mb, sr and mm, every main-library file cited in its statement heads appears in its own Sources list with
a SHA-256 prefix (checked file by file). So "these four sections list the main-library files concerned, with their
hashes" is true. The finding is right.

- Old: `(Section~\ref{mb:sec}); these two sections list the main-library files concerned, with their hashes.`
- New: `(Section~\ref{mb:sec}); a few such declarations are also restated in Sections~\ref{sr:sec} and~\ref{mm:sec}. These`
  `four sections list the main-library files concerned, with their hashes.`

Rendered (p.3): "...with their bridge files (Section 10); a few such declarations are also restated in Sections 7 and 9.
These four sections list the main-library files concerned, with their hashes." (Section 7 = sr, Section 9 = mm.)
`sr:sec` and `mm:sec` were already referenced in the same paragraph. These claims were re-checked after the build
against the live sr.tex and mm.tex, which other fixers were editing at the time, and still hold.

### 3. [minor, typography] "names-pace" in cb — fixed in the preamble

Check. `\showhyphens` with the document's font setup (amsart, T1, lmodern, no babel) gives `names-pace names-paces`
under the default patterns. With the exception it gives `name-space name-spaces` (also `Name-space`). In build doc-r2
the break "In C3L/C3Encoding/Gen.lean, names-|pace C3:" occurs in Section 11 (cb's coverage list of the C3L files).
The finding is right.

- Old (preamble.tex:42-43): `\makeatother` followed by a blank line.
- New: inserted directly after that `\makeatother` (end of the statement-tolerance block):
  `% Hyphenation exceptions (not macros): the default patterns would break ``namespace'' as ``names-pace''.`
  `\hyphenation{name-space name-spaces}`

This is a TeX primitive (hyphenation exception), not a macro and not a package. Typewriter text (`\lean`, `\dirn`,
`\texttt`) is not hyphenated at all, so it is unaffected. Rendered (p.149): "In C3L/C3Encoding/Gen.lean, name-|space
C3: ...". No other paragraph re-flows because of the exception (see the control builds below).

## Compile check

Whole document from STAGE into `build/final-front-r1`: live sections at about 21:49, the existing `appendix_map.tex`, and
three passes of `nice -n 15 pdflatex -interaction=nonstopmode -output-directory=build/final-front-r1 proofs.tex`.
- every pass exits 0;
- errors 0, lines containing "Warning" 0, undefined references or citations 0, multiply defined labels 0;
- overfull boxes 0 (so 0 above 1pt);
- underfull hbox 187 (76 with badness 10000);
- 188 pages; no page ends with a heading (the Scope section runs from p.3 to p.4, with "Evidence outside Lean" split
  2+2 lines across the page break).

Control builds (`build/final-front-r1-ctl-pre` and `build/final-front-r1-ctl-post`): one frozen copy of the live
sections and appendix, built once with the snapshot front files and once with the edited ones. Both have 188 pages, so
the extra page against doc-r2 (187) comes from concurrent section edits (ar, cb, ec, mm, pc and sr changed after the
snapshot). Pages whose text differs between the two controls: 3 and 4 (the two edited sentences), then a shift of about two lines inside
Section 1 that ends on p.7, and p.149 (the hyphenation). No other page differs.

Scratch: `build/final-front-r1-hyph/` (the `\showhyphens` test).
