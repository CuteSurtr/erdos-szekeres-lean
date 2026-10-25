# C3W6 / P12: W6.tsv shard 12 of 44, 3 lanes, cap 900

**Result: 71 of my 94 units were run to an outcome. 53 were certified, 15 timed out at 900 s, and 3 were still running when the lanes were killed at END. The other 23 were not reached. No SAT, no proof rejection, no memory problem, and no unit ended early without a certificate.**

## Setup

- Task: `results/C3W6/TASK.md` at c5260b44, with V = P12, LIST = W6.tsv, j = 12, N = 44, H = 4.5.
- One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`). Start 05:31:33 UTC, END 09:46:33 UTC (start + 4.5 h − 15 min). Lanes started 05:35:17 and were killed (whole process groups) at 09:46:33.
- Tools (`tools.txt`): a worktree of cad4e050 at `/opt/c3u2`, TOOLS = `.../results/C3U2/tools`, used unmodified. CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8 (its example gives `s VERIFIED UNSAT`), and drat-trim lrat-check 2e3b2dc with the E2 patch. Sanity test: LRAT `3 0 0` on {1},{-1} is rejected by both checkers and `3 0 1 2 0` is accepted by both.
- Base CNF: `gen_case.py 11 7 none` gives header `p cnf 168399 4154921` and sha256 `bf0e502e…6da`, which matches.
- Units: W6.tsv rows with row ≡ 12 (mod 44), which is 94 units (`units.tsv`). Lane k ran positions ≡ k (mod 3) (`lane0.sh`–`lane2.sh`). Each unit ran `close_tree.py base out{k}.jsonl U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02`. Nothing was seeded, and `compose.py` was not run.
- `out.jsonl` holds the records of lane 0, then lane 1, then lane 2: 53 certified UNSAT records, 15 UNKNOWN (cap 900) records and 15 split records. Driver log tails are in `driver{k}.log.tail`.

## Totals

| stratum | units | certified | timeout 900 | killed at END | not reached |
|---|---|---|---|---|---|
| H3/two | 76 | 53 | 15 | 3 | 5 |
| H6(1,1)/one | 2 | 0 | 0 | 0 | 2 |
| H6(2,1)/one | 3 | 0 | 0 | 0 | 3 |
| H6(3,1)/one | 3 | 0 | 0 | 0 | 3 |
| H6(4,0)/one | 1 | 0 | 0 | 0 | 1 |
| H6(5,0)/one | 3 | 0 | 0 | 0 | 3 |
| H6(5,1)/one | 4 | 0 | 0 | 0 | 4 |
| H6(5,1)/two | 2 | 0 | 0 | 0 | 2 |
| **all** | **94** | **53** | **15** | **3** | **23** |

| prior | units | certified | timeout 900 | killed at END | not reached |
|---|---|---|---|---|---|
| timeout300 | 29 | 17 | 6 | 0 | 6 |
| presplit | 57 | 32 | 8 | 2 | 15 |
| never_ran | 8 | 4 | 1 | 1 | 2 |

Units were taken in file order, so all the one-orbit and H6(5,1)/two units (near the end of my list) are among the 23 not reached.

## Solve times of the 53 certified units

The minimum was 52.7 s, Q1 257.9 s, the median 535.3 s, Q3 750.8 s, p90 829.9 s and the maximum 881.9 s. **35 of the 53 were certified above 300 s.** Each check (lrat-check plus cake_lpr) took at most 111.6 s, 4,028 s in all. All 53 have `c VERIFIED` and `s VERIFIED UNSAT`.

Each of the 15 timeouts at 900 s got its layer split record (51 children each), with the children left unsolved, as intended. The three units killed at END have no record and are still open:
`0s0_4s1-5s0__1s1-2s0-3s0-6s1-7s1-8s0`, `0s0_4s1-6s0__1s0-2s0-3s1-5s0-7s0-8s1`, `0s0_4s1-7s0__1s1-2s1-3s1-5s0-6s0-8s1`. No checker was killed, so there are no `none` records to re-check.

## SAT / rejections / incidents

- SAT: none.
- PROOF NOT ACCEPTED: none, so there is no `recheck.jsonl`.
- No memory problem: free memory never went below about 6 GB.
- No unit ended in under 72 s without a certificate. The shortest solve, 52.7 s, was certified.

## Per unit

(pos = position in `units.tsv` from 0; split = the layer split written after a timeout)

```
pos	row	node	stratum	prior	result	solve_s	check_s	split
0	12	0s0_1s0-10s0__2s1-3s1-4s1-5s1-6s0-7s1	H3/two	timeout300	certified	437.4	82.7	
1	56	0s0_1s0-2s0__3s1-4s0-5s1-6s0-7s1-8s1	H3/two	presplit	certified	52.7	66.6	
2	100	0s0_1s0-2s1__3s0-4s1-5s1-6s1-7s1-8s0	H3/two	timeout300	certified	817.2	103.6	
3	144	0s0_1s0-3s1__2s1-4s0-5s1-6s0-7s0-8s0	H3/two	timeout300	certified	780.7	94.5	
4	188	0s0_1s0-4s1__2s1-3s0-5s0-6s1-7s0-8s0	H3/two	timeout300	certified	696.7	102.3	
5	232	0s0_1s0-5s1__2s1-3s0-4s1-6s1-7s1-8s0	H3/two	timeout300	certified	654.5	88.9	
6	276	0s0_1s0-7s0__2s1-3s0-4s0-5s1-6s0-8s0	H3/two	timeout300	certified	265.6	68.3	
7	320	0s0_1s1-2s0__3s0-4s1-5s0-6s0-7s0-8s1	H3/two	timeout300	certified	698.8	90.0	
8	364	0s0_1s1-2s0__3s1-4s1-5s1-6s1-7s0-8s1	H3/two	timeout300	certified	739.9	83.9	
9	408	0s0_1s1-5s0__2s1-3s0-4s0-6s0-7s1-8s0	H3/two	timeout300	certified	421.7	77.0	
10	452	0s0_1s1-5s1__2s0-3s1-4s0-6s0-7s0-8s1	H3/two	presplit	certified	252.9	76.8	
11	496	0s0_1s1-5s1__2s1-3s1-4s1-6s1-7s0-8s1	H3/two	presplit	certified	576.3	69.7	
12	540	0s0_1s1-7s1__2s1-3s1-4s1-5s0-6s0-8s1	H3/two	timeout300	certified	751.8	90.7	
13	584	0s0_1s1-8s0__2s1-3s0-4s0-5s1-6s0-7s1	H3/two	presplit	certified	184.6	61.8	
14	628	0s0_1s1-8s1__2s1-3s0-4s1-5s1-6s0-7s0	H3/two	timeout300	certified	664.6	85.5	
15	672	0s0_1s1-9s1__2s1-3s0-4s0-5s1-6s1-7s0	H3/two	never_ran	certified	798.7	73.5	
16	716	0s0_2s0-3s1__1s0-4s1-5s0-6s0-7s1-8s0	H3/two	presplit	certified	803.9	93.8	
17	760	0s0_2s0-3s1__1s1-4s1-5s1-6s1-7s1-8s0	H3/two	presplit	timeout900	900.1	None	split children=51
18	804	0s0_2s0-4s1__1s1-3s0-5s1-6s0-7s1-8s0	H3/two	presplit	timeout900	900.2	None	split children=51
19	848	0s0_2s0-5s0__1s0-3s1-4s0-6s1-7s1-8s0	H3/two	presplit	certified	110.0	55.7	
20	892	0s0_2s0-5s1__1s0-3s0-4s1-6s0-7s0-8s1	H3/two	timeout300	certified	820.1	90.7	
21	936	0s0_2s0-5s1__1s1-3s1-4s0-6s1-7s0-8s1	H3/two	timeout300	timeout900	900.2	None	split children=51
22	980	0s0_2s0-6s1__1s1-3s0-4s0-5s0-7s1-8s1	H3/two	timeout300	certified	716.0	92.4	
23	1024	0s0_2s0-7s0__1s0-3s0-4s1-5s1-6s1-8s1	H3/two	presplit	certified	218.1	61.6	
24	1068	0s0_2s0-7s0__1s1-3s1-4s1-5s0-6s1-8s1	H3/two	presplit	certified	285.0	64.7	
25	1112	0s0_2s0-7s1__1s1-3s0-4s0-5s1-6s1-8s1	H3/two	presplit	certified	532.5	89.0	
26	1156	0s0_2s0-8s0__1s1-3s0-4s0-5s1-6s0-7s1	H3/two	presplit	certified	462.7	76.2	
27	1200	0s0_2s1-3s0__1s0-4s1-5s0-6s0-7s1-8s0	H3/two	timeout300	certified	813.0	87.9	
28	1244	0s0_2s1-3s0__1s1-4s1-5s1-6s1-7s1-8s0	H3/two	timeout300	timeout900	900.1	None	split children=51
29	1288	0s0_2s1-3s1__1s1-4s0-5s1-6s0-7s1-8s0	H3/two	presplit	certified	128.5	59.0	
30	1332	0s0_2s1-4s0__1s0-3s1-5s1-6s0-7s1-8s1	H3/two	timeout300	timeout900	900.1	None	split children=51
31	1376	0s0_2s1-5s0__1s0-3s0-4s1-6s0-7s0-8s0	H3/two	presplit	certified	566.3	75.8	
32	1420	0s0_2s1-5s0__1s1-3s1-4s0-6s1-7s0-8s0	H3/two	presplit	certified	875.9	92.6	
33	1464	0s0_2s1-6s0__1s1-3s0-4s0-5s0-7s0-8s0	H3/two	presplit	certified	468.8	65.7	
34	1508	0s0_2s1-6s1__1s0-3s0-4s1-5s1-7s0-8s0	H3/two	presplit	certified	483.3	73.4	
35	1552	0s0_2s1-6s1__1s1-3s1-4s1-5s0-7s0-8s0	H3/two	presplit	certified	535.3	77.3	
36	1596	0s0_2s1-7s0__1s1-3s0-4s1-5s1-6s0-8s0	H3/two	never_ran	certified	749.8	91.3	
37	1640	0s0_2s1-7s1__1s1-3s1-4s0-5s0-6s1-8s0	H3/two	never_ran	certified	606.1	80.7	
38	1684	0s0_2s1-8s1__1s1-3s0-4s0-5s1-6s1-7s1	H3/two	presplit	certified	845.2	83.9	
39	1728	0s0_2s1-9s0__1s0-3s1-4s0-5s0-6s1-7s1	H3/two	presplit	certified	222.1	62.7	
40	1772	0s0_2s1-9s0__1s1-3s1-4s1-5s1-6s1-7s1	H3/two	presplit	certified	346.9	68.0	
41	1816	0s0_3s0-4s1__1s1-2s0-5s1-6s0-7s1-8s1	H3/two	presplit	timeout900	900.2	None	split children=51
42	1860	0s0_3s0-5s0__1s0-2s1-4s0-6s1-7s1-8s1	H3/two	presplit	certified	149.0	52.3	
43	1904	0s0_3s0-5s1__1s0-2s0-4s1-6s0-7s1-8s1	H3/two	timeout300	timeout900	900.2	None	split children=51
44	1948	0s0_3s0-5s1__1s1-2s1-4s1-6s0-7s0-8s1	H3/two	timeout300	timeout900	900.2	None	split children=51
45	1992	0s0_3s0-6s0__1s1-2s0-4s0-5s1-7s0-8s1	H3/two	presplit	certified	125.2	50.6	
46	2036	0s0_3s0-6s1__1s0-2s1-4s0-5s0-7s0-8s1	H3/two	timeout300	certified	820.2	111.6	
47	2080	0s0_3s0-6s1__1s1-2s1-4s1-5s1-7s0-8s1	H3/two	never_ran	timeout900	900.1	None	split children=51
48	2124	0s0_3s0-7s0__1s1-2s0-4s1-5s0-6s0-8s1	H3/two	presplit	certified	225.4	55.9	
49	2168	0s0_3s0-7s1__1s0-2s1-4s0-5s1-6s0-8s1	H3/two	presplit	timeout900	900.2	None	split children=51
50	2212	0s0_3s0-8s0__1s0-2s1-4s0-5s1-6s1-7s1	H3/two	presplit	certified	279.5	62.8	
51	2256	0s0_3s0-8s1__1s0-2s1-4s0-5s1-6s1-7s0	H3/two	timeout300	certified	650.2	76.7	
52	2300	0s0_3s1-4s0__1s0-2s1-5s0-6s1-7s0-8s0	H3/two	timeout300	timeout900	900.2	None	split children=51
53	2344	0s0_3s1-4s1__1s0-2s0-5s0-6s0-7s0-8s0	H3/two	presplit	certified	180.3	57.9	
54	2388	0s0_3s1-4s1__1s1-2s0-5s1-6s1-7s0-8s0	H3/two	presplit	certified	111.3	47.8	
55	2432	0s0_3s1-5s0__1s0-2s1-4s1-6s0-7s0-8s0	H3/two	presplit	certified	881.9	90.5	
56	2476	0s0_3s1-5s1__1s0-2s0-4s0-6s1-7s0-8s0	H3/two	presplit	certified	194.8	55.6	
57	2520	0s0_3s1-5s1__1s1-2s1-4s0-6s0-7s0-8s0	H3/two	presplit	certified	281.7	65.3	
58	2564	0s0_3s1-7s0__1s1-2s0-4s1-5s0-6s1-8s0	H3/two	never_ran	certified	836.3	88.5	
59	2608	0s0_3s1-7s1__1s1-2s1-4s1-5s1-6s0-8s0	H3/two	timeout300	certified	571.9	75.8	
60	2652	0s0_3s1-8s0__1s1-2s0-4s1-5s0-6s0-7s1	H3/two	presplit	certified	502.5	67.5	
61	2696	0s0_4s0-5s1__1s0-2s1-3s0-6s1-7s0-8s1	H3/two	presplit	timeout900	900.1	None	split children=51
62	2740	0s0_4s0-6s1__1s0-2s0-3s0-5s0-7s0-8s1	H3/two	presplit	certified	617.3	63.2	
63	2784	0s0_4s0-6s1__1s1-2s0-3s1-5s1-7s0-8s1	H3/two	presplit	timeout900	900.2	None	split children=51
64	2828	0s0_4s0-7s0__1s0-2s1-3s1-5s0-6s0-8s1	H3/two	presplit	certified	263.0	61.5	
65	2872	0s0_4s0-7s1__1s0-2s0-3s1-5s1-6s1-8s0	H3/two	presplit	timeout900	900.1	None	split children=51
66	2916	0s0_4s0-7s1__1s1-2s1-3s1-5s0-6s1-8s0	H3/two	presplit	certified	875.9	86.1	
67	2960	0s0_4s1-5s0__1s1-2s0-3s0-6s1-7s1-8s0	H3/two	never_ran	killed_at_END			
68	3004	0s0_4s1-6s0__1s0-2s0-3s1-5s0-7s0-8s1	H3/two	presplit	killed_at_END			
69	3048	0s0_4s1-6s0__1s1-2s1-3s0-5s1-7s0-8s1	H3/two	presplit	timeout900	900.2	None	split children=51
70	3092	0s0_4s1-6s1__1s1-2s0-3s0-5s0-7s0-8s1	H3/two	presplit	not_reached			
71	3136	0s0_4s1-7s0__1s0-2s0-3s1-5s1-6s0-8s1	H3/two	presplit	not_reached			
72	3180	0s0_4s1-7s0__1s1-2s1-3s1-5s0-6s0-8s1	H3/two	presplit	killed_at_END			
73	3224	0s0_5s0-6s0__1s1-2s0-3s0-4s1-7s0-8s1	H3/two	presplit	not_reached			
74	3268	0s0_5s0-6s1__1s0-2s1-3s0-4s0-7s0-8s1	H3/two	presplit	not_reached			
75	3312	0s0_5s0-6s1__1s1-2s1-3s1-4s1-7s0-8s1	H3/two	presplit	not_reached			
76	3356	0s0-1s1_5__2s0-3s0-4s0-6s0-7s0-8s0	H6(1,1)/one	timeout300	not_reached			
77	3400	0s0-1s1_5__2s1-3s1-4s0-6s1-7s0-8s0	H6(1,1)/one	timeout300	not_reached			
78	3444	0s0-2s1_4__1s1-3s1-5s0-6s0-7s0-8s0	H6(2,1)/one	timeout300	not_reached			
79	3488	0s0-2s1_5__1s1-3s0-4s1-6s0-7s0-8s1	H6(2,1)/one	timeout300	not_reached			
80	3532	0s0-2s1_6__1s0-3s1-4s0-5s1-7s1-8s1	H6(2,1)/one	timeout300	not_reached			
81	3576	0s0-3s1_4__1s0-2s1-5s0-6s0-7s1-8s1	H6(3,1)/one	timeout300	not_reached			
82	3620	0s0-3s1_5__1s0-2s0-4s0-6s1-7s1-8s1	H6(3,1)/one	presplit	not_reached			
83	3664	0s0-3s1_5__1s1-2s1-4s0-6s0-7s1-8s1	H6(3,1)/one	presplit	not_reached			
84	3708	0s0-4s0_6__1s0-2s1-3s1-5s1-7s1-8s1	H6(4,0)/one	presplit	not_reached			
85	3752	0s0-5s0_6__1s0-2s0-3s0-4s1-7s1-8s0	H6(5,0)/one	presplit	not_reached			
86	3796	0s0-5s0_6__1s1-2s1-3s0-4s0-7s1-8s0	H6(5,0)/one	presplit	not_reached			
87	3840	0s0-5s0_7__1s0-2s1-3s1-4s1-6s1-8s0	H6(5,0)/one	presplit	not_reached			
88	3884	0s0-5s1_1__2s0-3s1-4s1-6s0-7s0-8s0	H6(5,1)/one	presplit	not_reached			
89	3928	0s0-5s1_2__1s0-3s0-4s0-6s1-7s0-8s0	H6(5,1)/one	presplit	not_reached			
90	3972	0s0-5s1_2__1s1-3s1-4s0-6s0-7s0-8s0	H6(5,1)/one	presplit	not_reached			
91	4016	0s0-5s1_6__1s1-2s1-3s1-4s1-7s0-8s1	H6(5,1)/one	never_ran	not_reached			
92	4060	0s0-5s1_1s1-10s1__2s1-3s0-4s1-6s1-7s1-8s1	H6(5,1)/two	never_ran	not_reached			
93	4104	0s0-5s1_7s0-9s1__1s0-2s1-3s1	H6(5,1)/two	presplit	not_reached			
```
