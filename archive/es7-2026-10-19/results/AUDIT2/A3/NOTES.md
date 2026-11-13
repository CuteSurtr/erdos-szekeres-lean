# AUDIT2 A3 notes (in progress)

Tools: CaDiCaL 3.0.1 (c6073042, built here), cake_lpr a36874a8 (built here), in /opt/build.
Scripts kept here: chk_cover.py, dec_data.py, run1.sh.

1. F rebuilt per V3Z/tools.txt: sha256 69c1dc8f...ffff932d (match).
2. 122 obligation CNFs regenerated with Mii-S/scripts/cover.py from that F: all 122 sha256 equal
   to Mii-S/cover_lrat.jsonl (no missing, no extra obligation).
3. chk_cover.py (own parser, no Mii-S code): every obligation file is F's body verbatim + extra
   clauses, header counts right, all literals in 1..nv; root has 121 distinct blocking clauses;
   the 121 up files' unit sets are exactly the negations of root's clauses (bijection); the
   blocking clauses over all up files negate to exactly the 450 cubes of Mii-S/cases.icnf, each
   once; F + cube sha256 == cases.jsonl cnf_sha256 for 450/450.
4. dec_data.py: decodes V2L/Data.lean the way unpack/decLit do, rebuilds rootCnf, upCnf over
   upTable (zip of upSets, upCubes) with casesOf as filter on caseTable, caseCnf: root 1/1,
   up 121/121, case 450/450 sha256 equal to the cake_lpr-checked / recorded files. 0 zero literals.
5. Lean composition (ClauseCover.lean, Main.lean, Facts.lean, TreeMain.lean, FinalTree.lean)
   read: sound; does not depend on the data being the geometric split.
6. 172 direct cases: Haudit t5_all172 = exactly the direct cases, sha match, s VERIFIED UNSAT.
7. Own re-run of all 122 obligations with cake_lpr: running.
