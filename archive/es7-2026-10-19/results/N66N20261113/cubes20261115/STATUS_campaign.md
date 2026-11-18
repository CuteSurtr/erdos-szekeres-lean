# N66 level-14 cube campaign: status (final)

**Every leaf has an accepted certificate (cover complete): N66 <= 55 follows by README section 2; needs an independent check before it is stated.** Written by `W/p2c14_driver_r7.py` at 04:28:08 KST, 18 November 2026 (final); plan and labels in `README.md` of this folder. W = `/home/jay/research/data/n66-20261113`; per-cube files in `W/p2/c14/<id>/it<k>/`; machine status `W/p2/c14/campaign_status.json`.

## Allocation

- Resume r7 (driver copy p2c14_driver_r7.py, session of 18 Nov; rules of r4/r5 = A1 proposals P1, P2, P3: band >= 4 gets 2,400 s and MemoryMax 5G, else 1,200 s and 4.1G; pre-split of band-6/7 cubes; A1 split order): cube units `esr-n66-cube-<id>`: 1 thread each (CPUQuota 98 %), MemorySwapMax 0, nice 10, RuntimeMaxSec ending by 17:59 KST 18 Nov. At most 5 at a time (now 5; memguard slot penalty 0). No new cube while the disk has less than 120 GB free. Partial files of timed-out runs are kept (uncompressed in r7; the owner deleted the older partial files on 16 Nov).
- Each start also needs room: running cubes reserved at 3,300 MB each, n66 track + 3,300 <= n66 budget - 200 MB and all research units + 3,300 <= total - 500 MB (budgets from the running memguard: (17000, 24000)), and 0.98 free thread under the 16-thread cap (summed CPUQuota of active esr-* units).
- The cake_lpr step runs inside the cube unit after CaDiCaL exits (p2_cert.sh -> p2_cake.py, unchanged). p2_mem.wait_room counts only `nov13c-n66-*` units, so for `esr-n66-*` units it never waits; the driver gate above is what keeps the track inside its budget.
- Driver unit `esr-n66-driver-r7`: CPUQuota 6 % (5 x 98 % + 6 % = 4.96 threads), MemoryMax 300M. Per-cube CaDiCaL limit 1,200 or 2,400 s by band (HEURISTIC), shorter near the deadline; no cube starts later than 17:59 - 600 s - 300 s (18 Nov).

## Cover argument

- Split states 25 12 16 29 17 37, sel_s = 988541 + s; o = occupied = +sel_s, h = hole = -sel_s; cube ids list the six signs in that order, then `_<s><o|h>` for every re-split state. The 64 sign patterns are all assignments of the six variables, so their disjunction is a tautology.
- Unit propagation on the 79 SB clauses refutes 8 of the 64 (all with 25 h, 29 o, 37 h): hhhohh, hhhooh, hhoohh, hhoooh, hohohh, hohooh, hooohh, hooooh. They run through the same pipeline; like every cube they count only with their own accepted certificate.
- A cube whose CaDiCaL run reaches its time limit is replaced by its children c AND s occupied, c AND s hole, s = the first state of 40 52 46 44 45 39 32 30 20 57 14 53 38 47 33 19 50 58 62 35 23 49 not in c (A1 order since r4; corrected 16 Nov after CN issue 6). The two children cover the parent, so the leaves always cover the 2^6 split.
- Leaves now: 132; exact leaf cover check: COVER_OK.
- Accepted certificates: 132 of 132 leaves. Cover by accepted certificates (cube literals read from each verify.json): COVER_OK.
- Acceptance (README section 6): cert.json and verify.json ALL_OK; cake.out has the exact line `s VERIFIED UNSAT`; L = 14; W = range(70); the 27-pair SB list of b14h2; the cube field of layout, verify and cert equals the cube; 0 unclassified clauses; trim.cnf SHA-256 recomputed by the driver. Rows are justified by template_cert66 without cube assumptions.

## Counts

certified: 132, split: 68

## Cubes (priority order)

| id | holes | UP | status | started | wall s | conflicts | note |
|---|---|---|---|---|---|---|---|
| hhhhhh | 6 |  | certified | 05:50:37 | 234.2 | 109509 | trim.cnf da037243e51599d602777df0aac2443f25e65248a4adc45246ecf45ab555553d; rows 392 |
| hhhohh | 5 | yes | certified | 05:59:17 | 45.1 |  | trim.cnf 06250f3407be9aa6d7a43d3f3c225a3d232e107bcef3cbb484f8ce7be662ab06; rows 0; peak 499 MB |
| hohohh | 4 | yes | certified | 05:59:20 | 45.4 |  | trim.cnf 06250f3407be9aa6d7a43d3f3c225a3d232e107bcef3cbb484f8ce7be662ab06; rows 0; peak 497 MB |
| hhoohh | 4 | yes | certified | 06:00:09 | 46.9 |  | trim.cnf 06250f3407be9aa6d7a43d3f3c225a3d232e107bcef3cbb484f8ce7be662ab06; rows 0; peak 497 MB |
| hhhooh | 4 | yes | certified | 06:00:13 | 46.9 |  | trim.cnf 06250f3407be9aa6d7a43d3f3c225a3d232e107bcef3cbb484f8ce7be662ab06; rows 0; peak 497 MB |
| hooohh | 3 | yes | certified | 06:01:02 | 50.3 |  | trim.cnf 06250f3407be9aa6d7a43d3f3c225a3d232e107bcef3cbb484f8ce7be662ab06; rows 0; peak 498 MB |
| hohooh | 3 | yes | certified | 06:01:05 | 51.1 |  | trim.cnf 06250f3407be9aa6d7a43d3f3c225a3d232e107bcef3cbb484f8ce7be662ab06; rows 0; peak 498 MB |
| hhoooh | 3 | yes | certified | 06:01:54 | 47.4 |  | trim.cnf 06250f3407be9aa6d7a43d3f3c225a3d232e107bcef3cbb484f8ce7be662ab06; rows 0; peak 496 MB |
| hooooh | 2 | yes | certified | 06:02:13 | 45.0 |  | trim.cnf 06250f3407be9aa6d7a43d3f3c225a3d232e107bcef3cbb484f8ce7be662ab06; rows 0; peak 496 MB |
| ohhhhh | 5 |  | certified | 06:02:47 | 529.8 | 601323 | trim.cnf f4ed31b1c2c2b11d353a63cc086d63238c49873c634df0b7e230fa25c96cf427; rows 537; peak 2474 MB |
| hohhhh | 5 |  | certified | 06:03:06 | 405.9 | 307741 | trim.cnf a3b1cc463cade60cdccc54a562e273dbe557067e856a01e780d9054fda60f4fc; rows 543; peak 2182 MB |
| hhohhh | 5 |  | certified | 06:10:02 | 404.5 | 304216 | trim.cnf b2df3fab3470e23e5ab2f557e8f52f76b36f0aa9cca646109916fb24148ece01; rows 557; peak 2357 MB |
| hhhhoh | 5 |  | certified | 06:12:02 | 370.1 | 335006 | trim.cnf 6c2076079b922e06d55ddd3f40cb358528069971b684cc7e822e96670e74d66d; rows 605; peak 2316 MB |
| hhhhho | 5 |  | certified | 06:16:58 | 573.2 | 632967 | trim.cnf 2197e250693fb9f289086bce02def5b5fa164ed217bcfbdec57dd32c84fd6270; rows 1153; peak 2309 MB |
| ohohho_23h_49h | 5 |  | certified | 13:12:22 | 561.1 | 644710 | trim.cnf c69ccc192accd9349c3cac73ea5b6e29ea5465464f903ab50a31c786aa83a3cb; rows 1139; peak 2511 MB |
| oohhhh | 4 |  | certified | 06:18:23 | 896.4 | 1659315 | trim.cnf 2cfd5245366ff0bb8b548bb95070d4d19df40fe1b1881d9f6aea4b97a7d828e5; rows 646; peak 2479 MB |
| ohohhh | 4 |  | certified | 06:26:57 | 846.4 | 1554898 | trim.cnf ce461d2088b60e3d57aeaebe25d179708ef620ce07c58128b9d2d26cb358d7c5; rows 668; peak 2206 MB |
| ohhohh | 4 |  | certified | 06:34:06 | 614.8 | 745994 | trim.cnf 662816b28ce9b4ff4f573a6e1376d83f0ac9dc84606734b9037151870296ccd0; rows 754; peak 2236 MB |
| ohhhoh | 4 |  | certified | 06:41:47 | 842.2 | 1369240 | trim.cnf ade600c5536be38932228cff766f6f938db7d28f1268293d75f835a1e89f4e61; rows 687; peak 2495 MB |
| ohhhho | 4 |  | certified | 06:44:56 | 1221.2 | 2145649 | trim.cnf 6529d3e1e6b2eef5a9769f31cb9e2a64c722a3c058c7b8c5bbbd7b901d41366c; rows 1414; peak 2259 MB |
| hoohhh | 4 |  | certified | 06:45:15 | 570.7 | 469287 | trim.cnf 6dfc85318407c9aced860d618bd5e0efb8f328dc164f4f367646a018fbe51b31; rows 843; peak 2392 MB |
| hohhoh | 4 |  | certified | 06:57:17 | 812.2 | 1049444 | trim.cnf acdac32079fab7e6550ea5d60e8d188f0f9299bfd232b35992ea0a868e9dca9b; rows 692; peak 3156 MB |
| hohhho | 4 |  | certified | 07:11:21 | 997.6 | 1613478 | trim.cnf f06d3c60f3289a8fa4f34c6f2a82666f0f7bcf887c0d280b622aa836d4bf2160; rows 1286; peak 2582 MB |
| hhohoh | 4 |  | certified | 07:28:56 | 754.5 | 931398 | trim.cnf 422a3f17b59b90f414911282d8ab1915f6fb8b10435957de83679e18621baff9; rows 678; peak 3139 MB |
| hhohho | 4 |  | certified | 07:36:20 | 1029.1 | 1516821 | trim.cnf 743c2e2977b8214e8a5e20889c922a1088a905bde8d9d9767af2afbf86d4f62b; rows 1418; peak 2571 MB |
| hhhoho | 4 |  | certified | 07:49:05 | 672.6 | 886021 | trim.cnf fbd1ae5cb7aef79e217dcef0e82608d51a1c168fb5f9fd7df82f01f3a4cf45d6; rows 830; peak 2319 MB |
| hhhhoo | 4 |  | certified | 08:00:46 | 1072.9 | 1850877 | trim.cnf 15aeef7a17efd20897e9c38c763843f9555f1c37b645cd4f494033f63a26008c; rows 1185; peak 2497 MB |
| oohhoh_23h | 4 |  | certified | 08:42:31 | 798.3 | 1258411 | trim.cnf 34c151d02a9a11fbbb325a39b0f0d8076548225a871bda511a1201673694b75b; rows 730; peak 2399 MB |
| oohhho_23h | 4 |  | certified | 08:52:08 | 1034.7 | 1972451 | trim.cnf 70ed97914d325e3cfccc5e6e9a9efcb031292413a5df8f58eb5897db273f9df5; rows 1362; peak 2629 MB |
| ohohho_23h | 4 |  | split | 09:23:07 | 368.7 | 483833 | split on 49; peak 2594 MB |
| ohhoho_23h | 4 |  | certified | 13:12:26 | 577.6 | 778705 | trim.cnf bc8442a3a6926f5ae519673de3300d37fd90578e8c753870bf11a1f0a76474ca; rows 1520; peak 2226 MB |
| ohhhoo_23h | 4 |  | certified | 13:12:29 | 1001.2 | 1998697 | trim.cnf cab1ec8831ed0f51f97b1864d3971fc6f78c37a3d5930a932aa2bdf2f9dc2e8a; rows 1359; peak 2306 MB |
| hohhoo_23h | 4 |  | certified | 13:50:21 | 1069.8 | 1409392 | trim.cnf d3dc5237797451c7270ac6484bd8bc9bb56a5a7d64028ab15204c3edcc865d9b; rows 1419; peak 2336 MB |
| hhohoo_23h | 4 |  | certified | 14:17:52 | 1086.2 | 1355629 | trim.cnf 5c32ef7957f4262c662d3d6009a317122c1a5529b522aa390c99dd88fc211d2a; rows 1294; peak 2500 MB |
| ohohho_23h_49o | 4 |  | certified | 13:12:33 | 826.2 | 1271143 | trim.cnf 759e5afb36677da634cb36678ac081efc3f0bd726a084392e11d18e49d182dc6; rows 1307; peak 2616 MB |
| oohhoh_23o_49h | 4 |  | certified | 14:24:01 | 991.8 | 1326211 | trim.cnf c33367b8eb6b33f7857a54c46b355c57383c8c3e61d4e1d78882cd5b1d3123eb; rows 610; peak 2224 MB |
| oohhho_23o_49h | 4 |  | certified | 14:29:39 | 1096.0 | 1535503 | trim.cnf 2869392551abc91d08d96235b0be82e1e7af4df33f5d8e2b104843e5cec33b8e; rows 1335; peak 2490 MB |
| ohohho_23o_49h | 4 |  | certified | 14:29:58 | 1058.9 | 1416190 | trim.cnf 76720f3eaf5d50db87689bdeb9f427d8c46a1a791d93b426126c964dcf5cd786; rows 1448; peak 2439 MB |
| ohhhoo_23o_49h | 4 |  | certified | 14:31:17 | 1077.2 | 1523589 | trim.cnf ed69757585a21211aa9eeefd2103b56008cc4c794ecc3bfe8839d537212e2bb0; rows 1293; peak 2296 MB |
| hohhoo_23o_49h | 4 |  | certified | 14:57:14 | 980.3 | 1326857 | trim.cnf 98e9971f380ef8e716332cf23ffef42932d8a583db70f21baf4a7cff165786b2; rows 1150; peak 2363 MB |
| hhohoo_23o_49h | 4 |  | certified | 15:01:52 | 1024.7 | 1378756 | trim.cnf 23306abc62a40c45e0c9b6df68b36b08d570bd80e7c7a27d80ecf13adc647d4f; rows 1212; peak 2566 MB |
| ooohho_23h_49h | 4 |  | certified | 16:34:34 | 998.5 | 1227890 | trim.cnf 1bf15541bfdcce2718bf860f3855bf1edd6f04ef534bc9438d0430e483389bfb; rows 1265; peak 2488 MB |
| oohhoo_23h_49h | 4 |  | certified | 17:07:42 | 1124.8 | 1711217 | trim.cnf 74ca6281acf65d8ff7fbb6fcf593aeac58e9fd01c2c19babaa778c3eb20a925d; rows 1294; peak 2485 MB |
| ohohoo_23h_49h | 4 |  | certified | 17:32:40 | 1104.2 | 1757099 | trim.cnf 2cdbad8f4ee81c95237f55be8e9ac42c9d54199d8a06a5081e573e47244cee3c; rows 1185; peak 2421 MB |
| oohhho_23o_49o_44h | 4 |  | certified | 15:08:33 | 1256.8 | 1739463 | trim.cnf 7022338701c482746c611da4e9b9347a59ec13cf380fe611ab968a9e5bf0cb3b; rows 1036; peak 2573 MB |
| ohohho_23o_49o_44h | 4 |  | certified | 15:09:38 | 1205.0 | 1645674 | trim.cnf a4f74deac4aea985ef4df2b865a2fbfbec82df1291c20235fed390f095ce906f; rows 1109; peak 2439 MB |
| ohhhoo_23o_49o_44h | 4 |  | certified | 15:34:47 | 1215.8 | 1757560 | trim.cnf cdf45177b4ed8266675d5923b052400946f085a9184fa652a6577fbf65a59ff4; rows 1000; peak 2480 MB |
| oohhoo_23h_49o_44h | 4 |  | certified | 17:39:50 | 1267.6 | 1962582 | trim.cnf 25d5709833b76947197e0c720c4417183b39f7dfad94603101d6afb51a82a346; rows 921; peak 2604 MB |
| ohohoo_23h_49o_44h | 4 |  | certified | 18:02:11 | 1085.7 | 1770446 | trim.cnf 09eaf7f4b3ea24f02eb195f8b784274afcb8ca64e0a0f17a112b3abb20c7447d; rows 971; peak 2474 MB |
| ooohhh | 3 |  | certified | 08:05:49 | 1485.4 | 2711143 | trim.cnf eaf17517f00d3fc66c3ea542e06850e42c3ec09b31e3f9b45ffa251a0a6efd3d; rows 1034; peak 2328 MB |
| oohohh | 3 |  | certified | 08:21:58 | 1264.2 | 2014146 | trim.cnf b591c12ca269031435f7b588534b11137004bfd4a36c42d030ea541954bda3e3; rows 858; peak 2569 MB |
| oohhoh | 3 |  | split | 08:22:01 | 1213.1 | 3497409 | split on 23; peak 2548 MB |
| oohhho | 3 |  | split | 08:31:34 | 1216.8 | 3244346 | split on 23; peak 2453 MB |
| ohoohh | 3 |  | certified | 08:43:43 | 1096.2 | 1849598 | trim.cnf 1ababa5fcbb22112bbab2c8c1763a72f57143a881294bd8f33772a260751796b; rows 993; peak 2208 MB |
| ohohoh | 3 |  | certified | 08:56:25 | 1422.2 | 3604561 | trim.cnf 6ea976558f2382ac54b83160d1f615237f7f22246d6063fe5c9990330d3df7e5; rows 1004; peak 3251 MB |
| ohohho | 3 |  | split | 09:02:43 | 1213.0 | 3804976 | split on 23; peak 2528 MB |
| ohhooh | 3 |  | certified | 09:10:08 | 787.5 | 1196101 | trim.cnf 562aa43412a5b0a2a5c39a382039b613f1b2eb6d9cc102f14a69dfd9292a3083; rows 1008; peak 2249 MB |
| ohhoho | 3 |  | split | 09:21:30 | 462.4 | 708164 | split on 23; peak 2647 MB |
| ohhhoo | 3 |  | split | 09:23:52 | 321.5 | 347745 | split on 23; peak 2478 MB |
| hoohoh | 3 |  | certified | 13:22:07 | 969.2 | 1585024 | trim.cnf 58b9cbef638d979b0a5bfdd8fefa7fd6993008e775cf553c582774b9a28c095a; rows 1045; peak 3186 MB |
| hoohho | 3 |  | certified | 13:22:10 | 1475.1 | 2708522 | trim.cnf eab777fc10e196dfa6523ab19412f4798a093d5a2be8b486f97ebd36f28c014d; rows 1845; peak 2674 MB |
| hohoho | 3 |  | certified | 13:26:55 | 1239.1 | 2319148 | trim.cnf 547e3325f38096e0609133d840fdcfb771b8d5a81572384557f17fce7d3a5266; rows 979; peak 2374 MB |
| hohhoo | 3 |  | split | 13:29:57 | 1213.5 | 2890532 | split on 23; peak 2507 MB |
| hhooho | 3 |  | certified | 13:38:52 | 1436.9 | 2487918 | trim.cnf ff6174e18028d463351446a6d5a894ffe6a231f36d22687efafc66126c8d7468; rows 1165; peak 2311 MB |
| hhohoo | 3 |  | split | 13:48:58 | 1213.7 | 2817666 | split on 23; peak 2547 MB |
| hhhooo | 3 |  | certified | 13:49:02 | 1133.7 | 1878498 | trim.cnf a231a4b67f1bd11724d9b504978f0acc0b9b92da8b5911f5cdedc066c1a9b054; rows 1163; peak 2483 MB |
| oohhoh_23o | 3 |  | split | 13:57:27 | 1213.4 | 3297439 | split on 49; peak 2529 MB |
| oohhho_23o | 3 |  | split | 14:03:44 | 1213.9 | 2725281 | split on 49; peak 2282 MB |
| ohohho_23o | 3 |  | split | 14:09:19 | 1213.6 | 2702634 | split on 49; peak 2519 MB |
| ohhoho_23o | 3 |  | certified | 14:09:23 | 1258.6 | 1856956 | trim.cnf 55707dd3f3d5e6989e827b4ad2d3542ee6666be9af052173418b1eaf7a6b2b66; rows 1921; peak 2407 MB |
| ohhhoo_23o | 3 |  | split | 14:09:27 | 1213.9 | 2386736 | split on 49; peak 2644 MB |
| hohhoo_23o | 3 |  | split | 14:36:53 | 1215.2 | 2363884 | split on 49; peak 2618 MB |
| hhohoo_23o | 3 |  | split | 14:41:28 | 1214.9 | 2420035 | split on 49; peak 2592 MB |
| oooohh_23h | 3 |  | certified | 16:08:46 | 1053.3 | 1094080 | trim.cnf 246257db75e5f9e8c231bd01f38ff98b8f57af7f965154a13582fe2551d3fb37; rows 994; peak 3196 MB |
| ooohoh_23h | 3 |  | certified | 16:14:11 | 1321.4 | 1675714 | trim.cnf a676c9207506230872a58658605982bd03761cd4f79f77a0f4629f1a2d4dee9e; rows 1062; peak 2554 MB |
| ooohho_23h | 3 |  | split | 16:14:15 | 1215.2 | 2609397 | split on 49; peak 2530 MB |
| oohooh_23h | 3 |  | certified | 16:16:22 | 1324.9 | 1744438 | trim.cnf 6ac58a4a6f4fca838ab193d42a9970b0b8361112139ce129422ada369de1b84e; rows 967; peak 2548 MB |
| oohoho_23h | 3 |  | certified | 16:25:04 | 1397.9 | 2107260 | trim.cnf 3c8cd435ffd12e38937d0e33b54106d0c748bc2ec049f897b0cf5f10a9a72819; rows 1798; peak 2482 MB |
| oohhoo_23h | 3 |  | split | 16:47:23 | 1214.3 | 2593029 | split on 49; peak 2388 MB |
| ohoooh_23h | 3 |  | certified | 16:59:35 | 1148.4 | 1524298 | trim.cnf 178a45c22bef3d8d246232a1ce0be547965edfa044e86925582f966b9e59e8ee; rows 981; peak 2541 MB |
| ohooho_23h | 3 |  | certified | 17:09:47 | 1246.5 | 1962203 | trim.cnf 2f8ab7d4863a6502e9015b848fef07961a8b9230093cc38b6803f0a9882cae78; rows 1706; peak 2458 MB |
| ohohoo_23h | 3 |  | split | 17:12:24 | 1214.3 | 2776655 | split on 49; peak 2624 MB |
| ohhooo_23h | 3 |  | certified | 17:24:00 | 1019.8 | 1379619 | trim.cnf 552e2f80090fad1ecb6116851adf8ee3c14d64839cb2e514958b175c818e45c0; rows 1732; peak 2481 MB |
| hoooho_23h | 3 |  | certified | 17:47:33 | 1156.1 | 1357208 | trim.cnf 78244927ca439840cfc999da5178a9b9a6f305426cd20bc8607499a0401cf208; rows 1155; peak 3182 MB |
| hoohoo_23h | 3 |  | certified | 17:50:53 | 1376.3 | 1943461 | trim.cnf 8afc710fb47970ac064e3ee4d6d4270850f2336d9e0cb8b1344d3a7351be4465; rows 1760; peak 2633 MB |
| hohooo_23h | 3 |  | certified | 18:22:18 | 904.8 | 1222039 | trim.cnf b135e363971f3e6f8b3ff2bef1b8283f75eb73a34b6d51e3723f1d8daedcf122; rows 1127; peak 2514 MB |
| hhoooo_23h | 3 |  | certified | 18:54:01 | 1030.9 | 1514924 | trim.cnf 8e065835260280c5030eeeda29eda9aaa631f51bab1a84efc0811e8160aec472; rows 1031; peak 2510 MB |
| oohhoh_23o_49o | 3 |  | certified | 14:48:12 | 1590.5 | 2389018 | trim.cnf 441bff02f001acb4c4e58899dffcda510aeb3e636a068b9a6c28ddec97096313; rows 861; peak 3181 MB |
| oohhho_23o_49o | 3 |  | split | 14:48:16 | 1214.3 | 2398447 | split on 44; peak 2282 MB |
| ohohho_23o_49o | 3 |  | split | 14:49:16 | 1214.5 | 2265570 | split on 44; peak 2528 MB |
| ohhhoo_23o_49o | 3 |  | split | 15:14:16 | 1215.1 | 2399868 | split on 44; peak 2285 MB |
| hohhoo_23o_49o | 3 |  | certified | 15:15:53 | 1666.7 | 2357743 | trim.cnf 60ebadd6d05f9ec386f931e057ce87cd8d9968759d9b9f4c287bab4bd865fa10; rows 1346; peak 3162 MB |
| hhohoo_23o_49o | 3 |  | certified | 15:19:33 | 1651.5 | 2482607 | trim.cnf f2292ed7efc0a5158643ce2a38544b66b50b3e4dfdd0173d0afa4b41aa2aa654; rows 1364; peak 3137 MB |
| ooohho_23h_49o | 3 |  | certified | 16:37:10 | 1517.1 | 2241381 | trim.cnf a40ddcb2aad75d4a9dcc967f495dc9e8723e2b9ae4bcf82c4adeb189f7642159; rows 1496; peak 2565 MB |
| oohhoo_23h_49o | 3 |  | split | 17:19:22 | 1213.9 | 2714480 | split on 44; peak 2383 MB |
| ohohoo_23h_49o | 3 |  | split | 17:41:40 | 1214.4 | 2621606 | split on 44; peak 2548 MB |
| ooohoh_23o_49h | 3 |  | certified | 18:54:04 | 1032.9 | 1671220 | trim.cnf 22aea8fae311c0c53de1d4f502f9e8c3b2ff496a9fcb2cbd4ec53b5b58a6f52f; rows 793; peak 2382 MB |
| ooohho_23o_49h | 3 |  | certified | 18:54:08 | 1436.7 | 2458141 | trim.cnf 8631227bcd31bcd73dad3b6de099812acc3795c84cb7e9a10b43fa9388618ef8; rows 1411; peak 2697 MB |
| oohhoo_23o_40h | 3 |  | certified | 19:53:22 | 2308.8 | 4634808 | trim.cnf b161075a968dd59ab5c02d0f01b774cf57300616137e25d72df284fcba0d239f; rows 1267; peak 3231 MB |
| ohohoo_23o_40h | 3 |  | certified | 20:22:08 | 2099.2 | 4041353 | trim.cnf 55f3871e34842177aabb9ea31f60fce88bcc642504426bfa7aff146ed08b8453; rows 1278; peak 3254 MB |
| ooohoo_40h_52h | 3 |  | certified | 21:44:13 | 1822.3 | 2481385 | trim.cnf db176dc6d1e886e53582f771622264fa7b37d2b7020ca29504a722164bbd4a1e; rows 1463; peak 3235 MB |
| oohhho_23o_49o_44o | 3 |  | certified | 15:31:06 | 1285.4 | 1566726 | trim.cnf 7486896b66d770e1867ddc2fc63b43b9b7331bc184ba3936a9d84cf971352719; rows 1373; peak 2506 MB |
| ohohho_23o_49o_44o | 3 |  | certified | 15:31:10 | 1296.6 | 1581113 | trim.cnf 5d3456a3ef9d3d1f5390673f7c1d4f8390f0d96738c18e936a4ceabaf100cc0a; rows 1363; peak 2454 MB |
| ohhhoo_23o_49o_44o | 3 |  | certified | 15:44:46 | 1155.4 | 1512111 | trim.cnf ca1049e6c15cab467a83e93059791ac6a0015ea8f8a3a70c4f9596a68c5b99c7; rows 1382; peak 2646 MB |
| oohhoo_23h_49o_44o | 3 |  | certified | 17:51:54 | 1353.8 | 1907858 | trim.cnf fc15cdf32fd47e2c1735da1b7c6a95d19cfaad8452f00bab3273d3e7a0203321; rows 1500; peak 2542 MB |
| ohohoo_23h_49o_44o | 3 |  | certified | 18:07:37 | 1215.5 | 1818770 | trim.cnf 44e838bb7b8bbe8e2e0d144c426af39744300c59d06a72485a5ae73adae118a7; rows 1358; peak 2670 MB |
| oohhoo_23o_40o_52h | 3 |  | certified | 18:19:34 | 1634.8 | 2219334 | trim.cnf 6bca865070c1aadf1901b9de77ed560cdc36525df79c80d8c8882eff7074ac95; rows 1275; peak 3189 MB |
| ohohoo_23o_40o_52h | 3 |  | certified | 18:19:37 | 1522.0 | 2163194 | trim.cnf c406474273c5eef12338831e20a8177e425191b3ecbf0ebc5c2d24425934b0d0; rows 1329; peak 3254 MB |
| ooohoo_40h_52o_46h | 3 |  | certified | 18:19:40 | 1639.8 | 2482062 | trim.cnf e4efb8bb4708a8cf33b24f47b979abfa010ad8d8b8385c14223f023448e1250f; rows 1335; peak 3122 MB |
| oooohh | 2 |  | split | 15:48:19 | 1215.5 | 3003234 | split on 23; peak 2513 MB |
| ooohoh | 2 |  | split | 15:53:51 | 1214.0 | 3240444 | split on 23; peak 2403 MB |
| ooohho | 2 |  | split | 15:53:55 | 1214.1 | 2586730 | split on 23; peak 2586 MB |
| oohooh | 2 |  | split | 15:55:56 | 1215.0 | 2853782 | split on 23; peak 2355 MB |
| oohoho | 2 |  | split | 16:04:39 | 1214.3 | 2194199 | split on 23; peak 2608 MB |
| oohhoo | 2 |  | split | 16:26:53 | 1213.9 | 2088152 | split on 23; peak 2415 MB |
| ohoooh | 2 |  | split | 16:39:12 | 1213.7 | 2688229 | split on 23; peak 2566 MB |
| ohooho | 2 |  | split | 16:49:18 | 1214.0 | 2480036 | split on 23; peak 2682 MB |
| ohohoo | 2 |  | split | 16:51:54 | 1214.2 | 2387622 | split on 23; peak 2594 MB |
| ohhooo | 2 |  | split | 17:03:34 | 1215.0 | 2866860 | split on 23; peak 2468 MB |
| hoooho | 2 |  | split | 17:27:14 | 1214.1 | 3240727 | split on 23; peak 2643 MB |
| hoohoo | 2 |  | split | 17:30:35 | 1213.5 | 2814212 | split on 23; peak 2336 MB |
| hohooo | 2 |  | split | 18:01:51 | 1213.8 | 3196629 | split on 23; peak 2649 MB |
| hhoooo | 2 |  | split | 18:14:38 | 1174.2 | 2996227 | split on 23; peak 2622 MB |
| oooohh_23o | 2 |  | certified | 18:14:41 | 1495.7 | 2470008 | trim.cnf 18f7be2f133aa2047f0a977b9b7c608a1397e12c5db5b03ef8a6937d73364a01; rows 1415; peak 2272 MB |
| ooohoh_23o | 2 |  | split | 18:20:59 | 793.2 | 1804087 | split on 49; peak 2677 MB |
| ooohho_23o | 2 |  | split | 18:28:24 | 348.8 | 305267 | split on 49; peak 2539 MB |
| oohooh_23o | 2 |  | certified | 18:54:11 | 1348.3 | 1968853 | trim.cnf 2b07ceae340b604bf30f5e59fe77967c16756893da794050788844955844a79e; rows 1199; peak 3252 MB |
| oohoho_23o | 2 |  | certified | 19:12:46 | 2263.1 | 4329616 | trim.cnf 1f41ef9f6273129914052c75935c4e0ae013793a03f78f0798a9536e5e3dde4d; rows 2147; peak 2657 MB |
| oohhoo_23o | 2 |  | split | 19:12:50 | 2415.6 | 6807760 | split on 40; peak 2503 MB |
| ohoooh_23o | 2 |  | certified | 19:17:25 | 1405.7 | 1882809 | trim.cnf 89256d99aec5772aa14d87445ff205eac7bc60eaac6060583b373d4eb8735187; rows 1224; peak 3161 MB |
| ohooho_23o | 2 |  | certified | 19:19:14 | 2305.7 | 4722363 | trim.cnf 708be908fecd028d10b67fc1901e9aef23e41643e02717703d1244cb549e8569; rows 2246; peak 2710 MB |
| ohohoo_23o | 2 |  | split | 19:41:43 | 2414.2 | 6956575 | split on 40; peak 2526 MB |
| ohhooo_23o | 2 |  | certified | 19:52:17 | 1301.5 | 1978757 | trim.cnf 34f54ec3354842bbdb6e55290b1019624f4e3889b2309971c78b6f1656bc0cf0; rows 1970; peak 2425 MB |
| hoooho_23o | 2 |  | certified | 19:59:32 | 1838.0 | 3510875 | trim.cnf 264b533cc33378c120565fccfd009acb8eb2a443fcd96ccf35d62bc922848f76; rows 1524; peak 2553 MB |
| hoohoo_23o | 2 |  | certified | 20:14:44 | 2288.8 | 4885994 | trim.cnf 27cf861c238d1fbe4154c0c7b5cec0812d45f597ea072da6da755ec0f8ac9ee7; rows 1973; peak 3127 MB |
| hohooo_23o | 2 |  | certified | 20:31:31 | 1655.4 | 2905868 | trim.cnf 6eda77fde55b8524915183945c5dbef9ed91c53adcce56978c4891c69963b7d7; rows 1345; peak 2367 MB |
| hhoooo_23o | 2 |  | certified | 20:33:50 | 2132.6 | 4112020 | trim.cnf d2ebf8f1b0fba727761336c3e54600eeeda8a128cfebde67f775005768076c42; rows 1391; peak 3229 MB |
| ooooho_40h | 2 |  | certified | 20:55:02 | 2402.6 | 4537667 | trim.cnf 25dbf4e89b1eb227392672d6570123f98a85b56d2c9bd1053a0e4be2940477ec; rows 1877; peak 2344 MB |
| ooohoo_40h | 2 |  | split | 20:58:44 | 2413.3 | 7274391 | split on 52; peak 2690 MB |
| oohooo_40h | 2 |  | certified | 20:59:08 | 2074.5 | 3143644 | trim.cnf 30dd3e4b871c2fb5216fcb26aeb6ba58cfbdf7634c0b8460bf76bcfe9ba6fc1a; rows 1792; peak 2560 MB |
| ohoooo_40h | 2 |  | certified | 21:00:40 | 2192.4 | 3304582 | trim.cnf 820892856026ed19cf288fcdf161e8ab8fa1e7131de6bddc47e867f1a49f1dc4; rows 1864; peak 3221 MB |
| ooohoh_23o_49o | 2 |  | certified | 21:11:13 | 1902.9 | 2982618 | trim.cnf daec448e152ab2f6e6bdb36f7b6fe44a27ebcf203bf309f6d4dc7adb3793cc3e; rows 1262; peak 2540 MB |
| ooohho_23o_49o | 2 |  | certified | 21:35:15 | 2628.4 | 4874661 | trim.cnf a804c60557a5be9ebd4b7e2b599b526927490f9d86e5ed5124f7212a78cd46da; rows 2056; peak 3159 MB |
| oooooo_40h_52h | 2 |  | certified | 21:35:19 | 1257.2 | 1065480 | trim.cnf bc6092099226633ff609c386a84a69f04e0a17b622193211d82da41f55645bdd; rows 1869; peak 2188 MB |
| ooooho_40o_52h | 2 |  | certified | 21:39:07 | 1807.3 | 2132239 | trim.cnf 7dcb23273a4918b10bec835498670b701db2cb4c392528ad1870e615e866bb2f; rows 1876; peak 2404 MB |
| ooohoo_40o_52h | 2 |  | certified | 21:39:10 | 2359.3 | 3939931 | trim.cnf 3f577a8cbf924c68700e05dc0646d2465cd34c25815625b1ed2c1b933079e2c7; rows 1925; peak 2721 MB |
| oohooo_40o_52h | 2 |  | certified | 21:56:57 | 1341.0 | 1283924 | trim.cnf bd3a5553a012722d387e53653975e509cc1db87e523f7134724f3d7322b737cd; rows 1665; peak 2648 MB |
| ohoooo_40o_52h | 2 |  | certified | 22:10:24 | 1380.7 | 1724575 | trim.cnf d8862810d36d50d17d74bf6d1c4042947455b3a4a1a64c67791bedac44035496; rows 1768; peak 3173 MB |
| oohhoo_23o_40o | 2 |  | split | 22:15:44 | 1109.1 | 2274287 | split on 52; peak 2466 MB |
| ohohoo_23o_40o | 2 |  | split | 22:20:06 | 846.4 | 1466661 | split on 52; peak 2482 MB |
| ooohoo_40h_52o | 2 |  | split | 22:20:09 | 846.6 | 1625245 | split on 46; peak 2454 MB |
| oooooo_40o_52h_46h | 2 |  | certified | 22:20:13 | 912.7 | 654135 | trim.cnf 6e350e4450d4ca4d74e815a8f809cce1bd0114dfbc2d7b1378080b1090116d91; rows 1847; peak 2664 MB |
| oooooo_40h_52o_46h | 2 |  | certified | 18:19:44 | 1222.3 | 1106703 | trim.cnf 781ee3ef58a47cf2c52384e401af716c0d4ad8313f346f11cabd5ae419b28f34; rows 1783; peak 2753 MB |
| ooooho_40o_52o_46h | 2 |  | certified | 18:19:47 | 1760.5 | 2115306 | trim.cnf 1047037b0d2f42b59475852ff8c74bef9c550e92627b8443e6488184fae3ca6a; rows 1839; peak 3185 MB |
| ooohoo_40o_52o_46h | 2 |  | certified | 02:24:09 | 1947.9 | 3296532 | trim.cnf bda02fe3bd459800b8983e60fd7d4193b4ffddce9be7a3debcdf7213a8750377; rows 1705; peak 2465 MB |
| oohooo_40o_52o_46h | 2 |  | certified | 02:24:12 | 1287.8 | 1282190 | trim.cnf e469f0456fd8d10f4623e0399763ee7eb121e095e30e4b2f33b8d7c6c723a73d; rows 1768; peak 3198 MB |
| ohoooo_40o_52o_46h | 2 |  | certified | 02:24:16 | 1236.7 | 1563701 | trim.cnf 80e0006b7b26c7a1bbfdade079ffef06309ea8924453422296d9148984fec4fb; rows 1795; peak 2653 MB |
| oohhoo_23o_40o_52o | 2 |  | certified | 02:24:19 | 2279.3 | 4108227 | trim.cnf 7a4249d4e66aaaff3e17b0c8435c8d9e5ec638151d62a314b96b3baa78b0b743; rows 1876; peak 2362 MB |
| ohohoo_23o_40o_52o | 2 |  | certified | 02:24:22 | 1943.1 | 3556821 | trim.cnf 3ff66ad1b57789cf58c906c6953e55d2886fce405f836f119d7597af3a5e2197; rows 1764; peak 3254 MB |
| ooohoo_40h_52o_46o | 2 |  | certified | 02:45:33 | 2406.6 | 4367296 | trim.cnf ca922e2d6be6ad4cfc44eb5e7f3d1c590241e6403c1cb32529dc98c855eac729; rows 1662; peak 2606 MB |
| oooooo_40o_52o_46h_44h | 2 |  | certified | 02:46:22 | 1213.3 | 813459 | trim.cnf fbf89bd030507d5e193f72250b258dcc028b2b0903565d3f6ef8d7744c9f0577; rows 1678; peak 2748 MB |
| oooooo_40o_52h_46o_44h | 2 |  | certified | 02:59:26 | 1142.5 | 650387 | trim.cnf 76d527e6d1631b8517f56b96b3135081b711ed1195827df314e94066e58de889; rows 1706; peak 2735 MB |
| oooooo_40h_52o_46o_44h | 2 |  | certified | 02:59:30 | 1140.9 | 812649 | trim.cnf e856b47be9697c3121505c6d78cfa1bbbb01abb4889330772b2fcfe7ee723b70; rows 1636; peak 2675 MB |
| oooooh | 1 |  | certified | 03:04:05 | 2137.2 | 3922391 | trim.cnf 07579f384fc42a1b1c565c668b633fe79ff0ebef8daf6e1c14921b350780b0c1; rows 1812; peak 3212 MB |
| ooooho | 1 |  | split |  |  |  | split on 40 |
| ooohoo | 1 |  | split |  |  |  | split on 40 |
| oohooo | 1 |  | split |  |  |  | split on 40 |
| ohoooo | 1 |  | split |  |  |  | split on 40 |
| hooooo | 1 |  | certified | 03:07:03 | 2747.8 | 5939881 | trim.cnf f507ed18861f84dfcee0f67792798292966c6454b3ca25a3572abf135c9051d6; rows 1680; peak 3243 MB |
| oooooo_40h | 1 |  | split |  |  |  | split on 52 |
| ooooho_40o | 1 |  | split |  |  |  | split on 52 |
| ooohoo_40o | 1 |  | split |  |  |  | split on 52 |
| oohooo_40o | 1 |  | split |  |  |  | split on 52 |
| ohoooo_40o | 1 |  | split |  |  |  | split on 52 |
| oooooo_40o_52h | 1 |  | split |  |  |  | split on 46 |
| oooooo_40h_52o | 1 |  | split |  |  |  | split on 46 |
| ooooho_40o_52o | 1 |  | split |  |  |  | split on 46 |
| ooohoo_40o_52o | 1 |  | split |  |  |  | split on 46 |
| oohooo_40o_52o | 1 |  | split |  |  |  | split on 46 |
| ohoooo_40o_52o | 1 |  | split |  |  |  | split on 46 |
| oooooo_40o_52o_46h | 1 |  | split |  |  |  | split on 44 |
| oooooo_40o_52h_46o | 1 |  | split |  |  |  | split on 44 |
| oooooo_40h_52o_46o | 1 |  | split |  |  |  | split on 44 |
| ooooho_40o_52o_46o | 1 |  | certified | 03:19:11 | 2004.6 | 2640786 | trim.cnf cda8afdca30ee1fca8f516a70ba11c195c4fe35cfc0d30ab436530c0946fa1aa; rows 2321; peak 3194 MB |
| ooohoo_40o_52o_46o | 1 |  | certified | 03:19:16 | 2596.4 | 4406952 | trim.cnf 47acc15166614e472cae340a97f52ab9ef2d4f4d933ed98e5188268de7403d8b; rows 2383; peak 3250 MB |
| oohooo_40o_52o_46o | 1 |  | certified | 03:27:20 | 1631.5 | 1591001 | trim.cnf 2ea2b9d8b8c10530bcaa54eecf0c22bccef087c6e9a08d302bd0a7a320d28678; rows 2059; peak 2718 MB |
| ohoooo_40o_52o_46o | 1 |  | certified | 03:41:41 | 1682.9 | 1808962 | trim.cnf c5d6dd9a73f97113d492e7e59fc069b279ddf50f277a6633e6f33f107a8a7b51; rows 2415; peak 3244 MB |
| oooooo_40o_52o_46o_44h | 1 |  | certified | 03:53:44 | 1565.4 | 1380901 | trim.cnf 2d0bb5d43b0b65005a9c2e990867e66370ffe18f90caa2d6e1fee9e16acdd86b; rows 2206; peak 2395 MB |
| oooooo_40o_52o_46h_44o | 1 |  | certified | 03:53:48 | 1242.2 | 842133 | trim.cnf 5d9aa641633f9225091375920c4b5151e6a3ea2ad5ae94a42a99b514126ebe04; rows 2395; peak 2323 MB |
| oooooo_40o_52h_46o_44o | 1 |  | certified | 03:57:22 | 994.6 | 478158 | trim.cnf c64b65440b36ef8cdff4c33c7e45575a3eb021076e96b5fb5c7802abd8468f46; rows 2041; peak 2743 MB |
| oooooo_40h_52o_46o_44o | 1 |  | certified | 04:04:35 | 1321.1 | 1039350 | trim.cnf 43660438e1d46cbec0899e76cc3b3751c68f800f6271226422c8732c178f9d2d; rows 1979; peak 2617 MB |
| oooooo_40o_52o_46o_44o_45h | 1 |  | certified | 04:10:47 | 766.8 | 243967 | trim.cnf 715952694e3f5c9818c7c5a9485f9a4a507bae1d98202a59dd6b19e15808f843; rows 1810; peak 2380 MB |
| oooooo_40o_52o_46o_44o_45o_39h | 1 |  | certified | 04:14:21 | 812.1 | 287708 | trim.cnf 9ceb6ac6840572daa990a5a459b87af2f7f6619ceffeac7b7d31e573dc254bb2; rows 2243; peak 2767 MB |
| oooooo | 0 |  | split |  |  |  | split on 40 |
| oooooo_40o | 0 |  | split |  |  |  | split on 52 |
| oooooo_40o_52o | 0 |  | split |  |  |  | split on 46 |
| oooooo_40o_52o_46o | 0 |  | split |  |  |  | split on 44 |
| oooooo_40o_52o_46o_44o | 0 |  | split |  |  |  | split on 45 |
| oooooo_40o_52o_46o_44o_45o | 0 |  | split |  |  |  | split on 39 |
| oooooo_40o_52o_46o_44o_45o_39o | 0 |  | certified | 04:15:00 | 766.0 | 195497 | trim.cnf cb89aead97d2fc4543e2afecfed7d71ea2f6f8a40920307de588b59345f3d719; rows 1974; peak 2883 MB |

## Log (last 40)

```
02:45:32 end ohoooo_40o_52o_46h: certified ok (wall 1236.7 s, conflicts 1563701)
02:45:33 start ooohoo_40h_52o_46o (holes 2, band 5, UP False, limit 2400 s, MemoryMax 5G)
02:46:21 end oohooo_40o_52o_46h: certified ok (wall 1287.8 s, conflicts 1282190)
02:46:22 start oooooo_40o_52o_46h_44h (holes 2, band 5, UP False, limit 2400 s, MemoryMax 5G)
02:58:06 end ooohoo_40o_52o_46h: certified ok (wall 1947.9 s, conflicts 3296532)
02:59:26 end ohohoo_23o_40o_52o: certified ok (wall 1943.1 s, conflicts 3556821)
02:59:26 start oooooo_40o_52h_46o_44h (holes 2, band 5, UP False, limit 2400 s, MemoryMax 5G)
02:59:30 start oooooo_40h_52o_46o_44h (holes 2, band 5, UP False, limit 2400 s, MemoryMax 5G)
03:04:03 end oohhoo_23o_40o_52o: certified ok (wall 2279.3 s, conflicts 4108227)
03:04:05 start oooooh (holes 1, band 5, UP False, limit 2400 s, MemoryMax 5G)
03:07:01 end oooooo_40o_52o_46h_44h: certified ok (wall 1213.3 s, conflicts 813459)
03:07:03 start hooooo (holes 1, band 5, UP False, limit 2400 s, MemoryMax 5G)
03:18:51 end oooooo_40o_52h_46o_44h: certified ok (wall 1142.5 s, conflicts 650387)
03:19:10 end oooooo_40h_52o_46o_44h: certified ok (wall 1140.9 s, conflicts 812649)
03:19:11 start ooooho_40o_52o_46o (holes 1, band 6, UP False, limit 2400 s, MemoryMax 5G)
03:19:16 start ooohoo_40o_52o_46o (holes 1, band 6, UP False, limit 2400 s, MemoryMax 5G)
03:27:19 end ooohoo_40h_52o_46o: certified ok (wall 2406.6 s, conflicts 4367296)
03:27:20 start oohooo_40o_52o_46o (holes 1, band 6, UP False, limit 2400 s, MemoryMax 5G)
03:41:40 end oooooh: certified ok (wall 2137.2 s, conflicts 3922391)
03:41:41 start ohoooo_40o_52o_46o (holes 1, band 6, UP False, limit 2400 s, MemoryMax 5G)
03:53:42 end ooooho_40o_52o_46o: certified ok (wall 2004.6 s, conflicts 2640786)
03:53:44 start oooooo_40o_52o_46o_44h (holes 1, band 6, UP False, limit 2400 s, MemoryMax 5G)
03:53:48 start oooooo_40o_52o_46h_44o (holes 1, band 6, UP False, limit 2400 s, MemoryMax 5G)
03:56:42 end hooooo: certified ok (wall 2747.8 s, conflicts 5939881)
03:57:20 end oohooo_40o_52o_46o: certified ok (wall 1631.5 s, conflicts 1591001)
03:57:22 start oooooo_40o_52h_46o_44o (holes 1, band 6, UP False, limit 2400 s, MemoryMax 5G)
04:04:33 end ooohoo_40o_52o_46o: certified ok (wall 2596.4 s, conflicts 4406952)
04:04:35 start oooooo_40h_52o_46o_44o (holes 1, band 6, UP False, limit 2400 s, MemoryMax 5G)
04:10:46 end ohoooo_40o_52o_46o: certified ok (wall 1682.9 s, conflicts 1808962)
04:10:47 start oooooo_40o_52o_46o_44o_45h (holes 1, band 6, UP False, limit 2400 s, MemoryMax 5G)
04:14:20 end oooooo_40o_52h_46o_44o: certified ok (wall 994.6 s, conflicts 478158)
04:14:21 start oooooo_40o_52o_46o_44o_45o_39h (holes 1, band 6, UP False, limit 2400 s, MemoryMax 5G)
04:14:58 end oooooo_40o_52o_46h_44o: certified ok (wall 1242.2 s, conflicts 842133)
04:15:00 start oooooo_40o_52o_46o_44o_45o_39o (holes 0, band 7, UP False, limit 2400 s, MemoryMax 5G)
04:20:28 end oooooo_40o_52o_46o_44h: certified ok (wall 1565.4 s, conflicts 1380901)
04:23:52 end oooooo_40o_52o_46o_44o_45h: certified ok (wall 766.8 s, conflicts 243967)
04:26:58 end oooooo_40h_52o_46o_44o: certified ok (wall 1321.1 s, conflicts 1039350)
04:28:02 end oooooo_40o_52o_46o_44o_45o_39o: certified ok (wall 766.0 s, conflicts 195497)
04:28:07 end oooooo_40o_52o_46o_44o_45o_39h: certified ok (wall 812.1 s, conflicts 287708)
04:28:08 driver end
```

## Monitor

```bash
cat /home/jay/research/data/n66-20261113/p2/c14/campaign_status.json | head -c 2000
systemctl --user list-units "esr-n66-*"
journalctl --user -u esr-n66-driver -n 30 --no-pager
```
