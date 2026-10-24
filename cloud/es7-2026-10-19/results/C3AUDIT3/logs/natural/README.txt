Natural trigger of finding 1 and demonstration of finding 2 (m = 5, k = 6, base gen_case.py 5 6 none).
A: C3U close_tree (95cafa93, via C3U/tests/small.py) root 0s0, --caps 600 --cadopts=-c,1 --jobs 4, no sigma split.
   Prints {"open_frontier": 0}; 52 fully layered nodes timed out and got split records with 0 children (finding 2).
B: same, root 0s0_2, --sigma-split 2.  46 fully layered cube leaves timed out (0 children).
C: those 46 cube leaves solved afterwards (CaDiCaL, no limit; lrat-check E2 + cake_lpr: 46/46 certified),
   as a later close_tree run with the cube leaf as ROOT would do.
compose (sha check on):
   A     : C3U not covered, frontier 52; mycompose frontier 52; brute force 52 holes
   A + C : C3U not covered, frontier 31; mycompose frontier 52; brute force 36 holes
   C3U counts 5 fully layered plain nodes as covered (no uncovered ancestor in its frontier list) although only
   one sigma half of each is certified; brute force: 2 sigma vectors of each unrefuted:
   0s0_2_1_3s0-4s1 (only __1s1-3s0), 0s0_2_1s1-4s0_3 (__1s1-3s1), 0s0_2_3_1s1-4s0 (__1s1-3s0),
   0s0_2_3s0-4s1_1 (__1s0-3s0), 0s0_2_3s1-4s1_1 (__1s1-3s1).
   A + B + C: C3U frontier 31, mycompose 31, brute 31 (the sigma route of 0s0_2 is then complete, so the
   vacuous plain route is not needed there).
