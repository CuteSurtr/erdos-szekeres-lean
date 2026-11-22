# N66 level-15 cube campaign: status (final)

**Every leaf has an accepted certificate (cover complete): N66 <= 54 follows (as N66 <= 55 did at level 14); needs an independent check before it is stated.** Written by `W/p2c15_driver.py` at 13:07:08 KST, 22 November 2026 (final); plan and labels in `README.md` of this folder. W = `/home/jay/research/data/n66-20261113`; per-cube files in `W/p2/c15/<id>/it<k>/`; machine status `W/p2/c15/campaign_status.json`.

## Allocation

- Driver p2c15_driver.py (copy of p2c14_driver_r7.py; r4/r5 rules A1 P1-P3 with the time limits x 3: band >= 4 gets 7,200 s, else 3,600 s; MemoryMax 6500M; pre-split of band-6/7 cubes; A1 split order): cube units `esr-n66-c15-<id>`: 1 thread each (CPUQuota 98 %), MemorySwapMax 0, nice 10, RuntimeMaxSec ending by 08:00 KST 24 Nov. At most 8 at a time (now 8; memguard slot penalty 0). No new cube while the disk has less than 120 GB free. Partial files of timed-out runs: deleted (owner OK).
- Each start also needs room: running cubes reserved at 3,300 MB each, n66 track + 3,300 <= n66 budget - 200 MB and all research units + 3,300 <= total - 500 MB (budgets from the running memguard: (27000, 30000)), and 0.98 free thread under the 16-thread cap (summed CPUQuota of active esr-* units).
- The cake_lpr step runs inside the cube unit after CaDiCaL exits (p2_cert.sh -> p2_cake.py, unchanged; heap tiers 2000/3200/4500/5500 MB).
- Driver unit `esr-n66-drv15`: CPUQuota 6 %, MemoryMax 300M. Calibration leaves from `W/p2/cal15` are adopted only through accept().

## Cover argument

- Split states 25 12 16 29 17 37, sel_s = 988541 + s; o = occupied = +sel_s, h = hole = -sel_s; cube ids list the six signs in that order, then `_<s><o|h>` for every re-split state. The 64 sign patterns are all assignments of the six variables, so their disjunction is a tautology.
- Unit propagation on the 79 SB clauses refutes 8 of the 64 (all with 25 h, 29 o, 37 h): hhhohh, hhhooh, hhoohh, hhoooh, hohohh, hohooh, hooohh, hooooh. They run through the same pipeline; like every cube they count only with their own accepted certificate.
- A cube whose CaDiCaL run reaches its time limit is replaced by its children c AND s occupied, c AND s hole, s = the first state of 40 52 46 44 45 39 32 30 20 57 14 53 38 47 33 19 50 58 62 35 23 49 not in c (A1 order since r4; corrected 16 Nov after CN issue 6). The two children cover the parent, so the leaves always cover the 2^6 split.
- Leaves now: 105; exact leaf cover check: COVER_OK.
- Accepted certificates: 105 of 105 leaves. Cover by accepted certificates (cube literals read from each verify.json): COVER_OK.
- Acceptance (level-14 README section 6, with L = 15): cert.json and verify.json ALL_OK; cake.out has the exact line `s VERIFIED UNSAT`; L = 15; W = range(70); the 27-pair SB list of b14h2; the cube field of layout, verify and cert equals the cube; 0 unclassified clauses; trim.cnf SHA-256 recomputed by the driver. Rows are justified by template_cert66 without cube assumptions.

## Counts

certified: 105, split: 41

## Cubes (priority order)

| id | holes | UP | status | started | wall s | conflicts | note |
|---|---|---|---|---|---|---|---|
| hhhhhh | 6 |  | certified |  |  |  | trim.cnf 51c01ff239241963ac0d2b318341cdda26d9a1b75320668dff3148a9c1f91e95; rows 423 |
| hhhohh | 5 | yes | certified | 11:06:06 | 47.6 |  | trim.cnf 93548e48070ecd84d62a45419e5b1d6fff7dd55d8fd5913197da7ddf0954f25d; rows 0; peak 501 MB |
| hohohh | 4 | yes | certified | 11:06:10 | 47.1 |  | trim.cnf 93548e48070ecd84d62a45419e5b1d6fff7dd55d8fd5913197da7ddf0954f25d; rows 0; peak 500 MB |
| hhoohh | 4 | yes | certified | 11:06:13 | 47.9 |  | trim.cnf 93548e48070ecd84d62a45419e5b1d6fff7dd55d8fd5913197da7ddf0954f25d; rows 0; peak 501 MB |
| hhhooh | 4 | yes | certified | 11:06:17 | 47.2 |  | trim.cnf 93548e48070ecd84d62a45419e5b1d6fff7dd55d8fd5913197da7ddf0954f25d; rows 0; peak 501 MB |
| hooohh | 3 | yes | certified | 11:07:08 | 46.9 |  | trim.cnf 93548e48070ecd84d62a45419e5b1d6fff7dd55d8fd5913197da7ddf0954f25d; rows 0; peak 501 MB |
| hohooh | 3 | yes | certified | 11:07:11 | 47.2 |  | trim.cnf 93548e48070ecd84d62a45419e5b1d6fff7dd55d8fd5913197da7ddf0954f25d; rows 0; peak 500 MB |
| hhoooh | 3 | yes | certified | 11:07:14 | 47.5 |  | trim.cnf 93548e48070ecd84d62a45419e5b1d6fff7dd55d8fd5913197da7ddf0954f25d; rows 0; peak 499 MB |
| hooooh | 2 | yes | certified | 11:07:18 | 47.5 |  | trim.cnf 93548e48070ecd84d62a45419e5b1d6fff7dd55d8fd5913197da7ddf0954f25d; rows 0; peak 501 MB |
| ohhhhh | 5 |  | certified | 11:08:09 | 1164.0 | 2830441 | trim.cnf a79d5c866e074a762b068e8ce9067e6c71d83f40703d696e62912813f4cc6863; rows 555; peak 2181 MB |
| hohhhh | 5 |  | certified |  |  |  | trim.cnf 94e77505a91b020dfaa59f911388cabb51386a0f582724148f6799a32bb217f4; rows 571 |
| hhohhh | 5 |  | certified | 11:08:12 | 754.8 | 1281443 | trim.cnf 64968d79ab6f209e058fb74d284210f455d78bf0d41ca6b7ad92a0299cbe06b1; rows 597; peak 2567 MB |
| hhhhoh | 5 |  | certified | 11:08:15 | 828.9 | 1669275 | trim.cnf 7c376a6d512fb23ac61b3a41358a6d67979999e6a34a318f24ddb5bc3d876029; rows 595; peak 2411 MB |
| hhhhho | 5 |  | certified | 11:08:19 | 1159.9 | 2574458 | trim.cnf a0a3f2e413787dfcc3932d671073b99ec9a52b1a44639260a5584f29ecee69ed; rows 1077; peak 2600 MB |
| oohhhh | 4 |  | certified | 11:20:59 | 2278.1 | 7240878 | trim.cnf fbd6d99e596747c647acf6f77e26eec4383d1dcedded49e5f3a4a3f47648b052; rows 569; peak 2197 MB |
| ohohhh | 4 |  | certified | 11:22:21 | 2193.9 | 7196315 | trim.cnf 1f2d566c66a45a0c4bd4ef7bbc92d84d4e90da68780896133fa24df606e90781; rows 676; peak 2286 MB |
| ohhohh | 4 |  | certified | 11:27:49 | 1370.3 | 3207133 | trim.cnf c1a9f385526565fd9fba650dc47c0bae792cc7cf974683799072476aa5ba103f; rows 702; peak 2533 MB |
| ohhhoh | 4 |  | certified | 11:27:53 | 1941.4 | 6183841 | trim.cnf 582244202d9b089350494042fe2b90b648f26b753afc6cf989374cc0df0c9c06; rows 624; peak 2411 MB |
| ohhhho | 4 |  | certified | 11:50:53 | 2892.9 | 9611840 | trim.cnf 73637359d33e8a6a92099ca61027060aef2b196af803e24b741de7158cd8ce02; rows 1410; peak 2349 MB |
| hoohhh | 4 |  | certified | 11:59:14 | 1047.5 | 2186250 | trim.cnf d31349bd8d360901e7c34570fdf0bbc13861b8bb1d0adab51bebcae6c678b0bf; rows 725; peak 2584 MB |
| hohhoh | 4 |  | certified | 11:59:17 | 1658.6 | 4514217 | trim.cnf 149a8c9e10e0e53b95ca18f5d3b201b4203ed1f5830324148734ad85a367d394; rows 784; peak 3156 MB |
| hohhho | 4 |  | certified | 12:00:39 | 2339.9 | 7134485 | trim.cnf b40083ef4dd9c7383e82d14fc26fa09b9d47d2b9914fcdf93a4581ead688c6b7; rows 1212; peak 2663 MB |
| hhohoh | 4 |  | certified | 12:16:57 | 1492.8 | 3844921 | trim.cnf 4c8603af686d8af641bb46a4152a190f3c9ce0f2577d951c0de296b4fcb197ef; rows 657; peak 3148 MB |
| hhohho | 4 |  | certified | 12:27:19 | 2309.1 | 6814335 | trim.cnf c17850bd5942d7a2b213cf9db6b0d15c49aded41ffdf1e5518417663c5cf5805; rows 1266; peak 2655 MB |
| hhhoho | 4 |  | certified | 12:39:29 | 1460.7 | 3810796 | trim.cnf 465f87a3bcb587ce4e150e53b7a9057b82b4c238e554338b7f32536e99f92b12; rows 806; peak 2381 MB |
| hhhhoo | 4 |  | certified | 12:40:04 | 2689.2 | 8653839 | trim.cnf cda14be48fdda6621fed6a79e5e1558404e838941f8b945f758489a93530047d; rows 1076; peak 2655 MB |
| oohhoh_40h | 4 |  | certified | 14:06:34 | 2240.6 | 7183842 | trim.cnf f710d82dcc461ae14dde35eb1d55c1820b283308689f3cfad077aa3a2799ad74; rows 509; peak 3125 MB |
| oohhoo_40h_52h | 4 |  | certified | 21:24:36 | 3479.9 | 8388573 | trim.cnf 89b0568df7791cc5f6cad1c9bf64d1584cbb741974a10ac79011942e56a3c7f1; rows 947; peak 3156 MB |
| ohohoo_40h_52h | 4 |  | certified | 23:25:09 | 3288.1 | 7810055 | trim.cnf fcae9b07d13b4c7f73b4b190265ea89b5d3ec99d6322af8d9eee3e18c3cc66f4; rows 850; peak 3224 MB |
| ooohhh | 3 |  | certified | 12:42:12 | 3390.9 | 13017800 | trim.cnf afe7501991b5be7fbbb600f54162019ce178beffde764caa9d4954b34af43046; rows 861; peak 2661 MB |
| oohohh | 3 |  | certified | 13:04:13 | 2634.0 | 8311140 | trim.cnf aed09bf6def654ffd7438eda30404b9bcd32bf30d7f8b0ddedd16e2f323d5703; rows 870; peak 2422 MB |
| oohhoh | 3 |  | split | 13:06:05 | 3613.6 | 15259815 | split on 40; peak 2643 MB |
| oohhho | 3 |  | certified | 13:25:12 | 6834.7 | 24856267 | trim.cnf b405153755064d8a4c688c2b258daf1b7c55db4dc93046e0f956fd1c0994354f; rows 1539; peak 2772 MB |
| ohoohh | 3 |  | certified | 13:39:12 | 2567.2 | 7901404 | trim.cnf c1330a4762e90c70d326f21316fe930287ca5837151caccbf14374b4b46a7bf1; rows 875; peak 2408 MB |
| ohohoh | 3 |  | certified | 13:48:33 | 4078.6 | 15618838 | trim.cnf 4227ece075d91d69ecf8d718fb3a049a04825bb946f212c2af32573a0057d706; rows 864; peak 3255 MB |
| ohohho | 3 |  | certified | 14:22:23 | 6501.3 | 23918397 | trim.cnf 604f240f3203bc4f324eb652d77b1eeeeffbaa9e77069919800cf94b4f2b8a5d; rows 1968; peak 2768 MB |
| ohhooh | 3 |  | certified | 14:44:19 | 1718.2 | 5343426 | trim.cnf da9886cced9c3385801a0fd12c455f9dba8f727694a2e12aed3c70150b172fe7; rows 842; peak 2464 MB |
| ohhoho | 3 |  | certified | 14:57:02 | 2826.5 | 10035725 | trim.cnf 3bdcd2ccce975b111fc73fe52c54a28cfbf3a76abc50f1d9899b4d81b48b8c1c; rows 1836; peak 2465 MB |
| ohhhoo | 3 |  | certified | 15:13:23 | 6459.9 | 24726507 | trim.cnf 3f23c5e28dabbbb6cbc847d8e2963945a07a86527adc1f8a38130a5c33d06e90; rows 1596; peak 2312 MB |
| hoohoh | 3 |  | certified | 15:19:55 | 2003.3 | 7008350 | trim.cnf ed9f87d7e466ac9aa24773316f6fe9e60647cfa9640769f8f0e5e288f8d4ba39; rows 1169; peak 2569 MB |
| hoohho | 3 |  | certified | 15:44:32 | 3363.7 | 12811158 | trim.cnf 8a77d7a58349b6f6afca9ea62b4711a612eeba6fc6204e7ef56da225990a3cf1; rows 1617; peak 2699 MB |
| hohoho | 3 |  | certified | 15:53:38 | 2722.7 | 9818516 | trim.cnf 09f244176875d7aaba3a31af8be23942b1d41df1a71ffa2a46a691a458b6b52c; rows 944; peak 2595 MB |
| hohhoo | 3 |  | certified | 16:11:31 | 4972.7 | 18151256 | trim.cnf 6f837dbd3438f8e31a0a1c8783625f9ab1f1b04ab94f7c48cf74057213a16c8f; rows 1508; peak 3195 MB |
| hhooho | 3 |  | certified | 16:39:30 | 3088.5 | 10851600 | trim.cnf 9709bc60a4f93bf8c710fe5e0f6d75b45699f36349f0337c811f65c11f20802a; rows 1006; peak 2642 MB |
| hhohoo | 3 |  | certified | 16:41:07 | 5717.4 | 19133761 | trim.cnf dc29e479b15ec6dbdfaeb0ec1c79c0e844550fc93920939353992de0ad2a85f5; rows 1598; peak 3182 MB |
| hhhooo | 3 |  | certified | 17:01:51 | 2471.0 | 7965007 | trim.cnf b6c367644e4f3325ca71077ff9fd79b612fc14ba499789e9fe53290417f0ff21; rows 974; peak 2294 MB |
| oohhoh_40o | 3 |  | certified | 17:31:23 | 4213.9 | 12559230 | trim.cnf d8a79acbceae975e9d72713cbf28f91cbc63e98c5dae2252bdf5a759150d8d4d; rows 765; peak 3207 MB |
| ooohho_40h | 3 |  | certified | 20:57:39 | 6512.0 | 20678676 | trim.cnf 592813ce5c114ba4e6de28fd4f4a4009d2c5bf9f857a25d1248099cca6b49c1e; rows 1038; peak 2669 MB |
| oohoho_40h | 3 |  | certified | 21:28:51 | 4056.7 | 11498371 | trim.cnf 5118d6e8b0f271b3ffb9fef1b147354dd7c3ce22c0ea9138df25bba3721286f0; rows 1201; peak 2603 MB |
| oohhoo_40h | 3 |  | split | 19:23:48 | 7219.6 | 22297028 | split on 52; peak 2586 MB |
| ohooho_40h | 3 |  | certified | 22:18:13 | 3871.8 | 10639791 | trim.cnf 65833f0d943cbefc4ce852824ae1c5a66493c068ad94d0a0a777ee87140e9cbb; rows 1230; peak 2469 MB |
| ohohoo_40h | 3 |  | split | 21:24:39 | 7218.9 | 22822088 | split on 52; peak 2637 MB |
| hoohoo_40h | 3 |  | certified | 22:34:54 | 4393.2 | 12480441 | trim.cnf 34dba670148010d22bfea591c0cbbe6bc39682d69b8ce28fe04f4570d137b19c; rows 1065; peak 3149 MB |
| oohhoo_40h_52o | 3 |  | certified | 22:23:00 | 6996.7 | 18629916 | trim.cnf cd818c3d380f3acf26aa36d7d7981061d24efbbb61d73b9379c03839667352e8; rows 1226; peak 3240 MB |
| ohohoo_40h_52o | 3 |  | certified | 23:48:40 | 5847.9 | 15874764 | trim.cnf 25a5aa9b12466e560a1605fc10a3d55f458b636b83707b28bce9a96d11cf202c; rows 990; peak 3207 MB |
| ooohoo_40h_52h | 3 |  | certified | 03:49:21 | 4553.7 | 11198104 | trim.cnf ce8bad2f31943dc33518a77c2e7dad7956665303fef9e2d661fb5ffba29074bc; rows 1374; peak 2616 MB |
| ooohho_40o_52h | 3 |  | certified | 05:49:48 | 4854.1 | 9480219 | trim.cnf 3ad5f313a2f7cdf58374ac6096a1d6b4ad92950fc8f4e95d13c972cb0167b66f; rows 1191; peak 2628 MB |
| oohhoo_40o_52h | 3 |  | certified | 05:55:57 | 6182.2 | 12526973 | trim.cnf d158fa3dfe6614fdd4a52fb4d2922a7a0d9bd71686f9ddbdc0dec784e5913038; rows 1244; peak 3223 MB |
| ohohoo_40o_52h | 3 |  | certified | 05:56:19 | 5793.8 | 12032336 | trim.cnf aff8c1d68e6a5c6c596f1a9b1b096443546715df50e773ec1e6900cee4333abb; rows 1160; peak 3229 MB |
| ooohoo_40h_52o_46h | 3 |  | certified | 08:29:11 | 4174.8 | 9279539 | trim.cnf 30a754351ec007c4257ab56c236660212351bc2989c8227411acac1d5752bea3; rows 1272; peak 3213 MB |
| oohhoo_40o_52o_46h | 3 |  | certified | 09:04:14 | 4914.2 | 10212154 | trim.cnf d9bf0e58cb15db4c7fc605fda5b7ce52386ba0ccac6b608ba070416aab7b917f; rows 1081; peak 2676 MB |
| ohohoo_40o_52o_46h | 3 |  | certified | 09:11:50 | 4107.9 | 8733767 | trim.cnf 5a9a16d7d333cb7cfe2db702b3ce8f55f48758c51cb4c90e7b3a6dcabde73c61; rows 1025; peak 3130 MB |
| oooohh | 2 |  | certified | 17:35:04 | 4893.6 | 15057643 | trim.cnf 6301283bed509e3d1ce3d31e85fb582e6da01d1479333e455333e707de75aee7; rows 1302; peak 2354 MB |
| ooohoh | 2 |  | certified | 17:43:23 | 7703.7 | 27441498 | trim.cnf 86e5e8337211d6bf09168d04cc76e4810a098d45099d8940a923faed3166ac31; rows 1140; peak 3384 MB |
| ooohho | 2 |  | split | 18:17:02 | 7220.6 | 27740720 | split on 40; peak 2742 MB |
| oohooh | 2 |  | certified | 18:42:05 | 4578.5 | 13250409 | trim.cnf 7961e5af744fe3b4a762fb8ef54fbe31ac9095048ab9872a1e52d70ad1c44efb; rows 1206; peak 3215 MB |
| oohoho | 2 |  | split | 18:57:08 | 7217.0 | 24891661 | split on 40; peak 2826 MB |
| oohhoo | 2 |  | split | 19:52:51 | 7217.0 | 23292579 | split on 40; peak 2742 MB |
| ohoooh | 2 |  | certified | 20:12:27 | 4550.7 | 12672887 | trim.cnf 0bffdc5871b4895f562981d5351e9b12b5b4e71e18c78c77c02416cee6daf0f7; rows 1260; peak 3196 MB |
| ohooho | 2 |  | split | 20:17:24 | 7219.5 | 24893849 | split on 40; peak 2766 MB |
| ohohoo | 2 |  | split | 19:23:52 | 7217.9 | 24203210 | split on 40; peak 2612 MB |
| ohhooo | 2 |  | certified | 19:23:55 | 4188.0 | 12044229 | trim.cnf 8b8a854b4561b1310753378c2a6c6de9515c705206c1d30dbd5c5255fc2b83f8; rows 1751; peak 2819 MB |
| hoooho | 2 |  | certified | 19:23:58 | 5596.2 | 17479103 | trim.cnf 29568948c943369669bcb6ddb2d5070ffc1f7be824524022be459428a9cab3cb; rows 1207; peak 3176 MB |
| hoohoo | 2 |  | split | 20:34:18 | 7218.4 | 25899206 | split on 40; peak 2794 MB |
| hohooo | 2 |  | certified | 20:57:52 | 5922.5 | 16085435 | trim.cnf 7e4a504bd5085864667dcbbda8288cf8a000a19bedd42bbcacd859aeaf063f90; rows 1314; peak 3236 MB |
| hhoooo | 2 |  | certified | 22:37:17 | 7747.9 | 21703163 | trim.cnf 4cf42a9d961d180d6c4e372b4b59238c10d67030ed9b7987b6364decbccee7f5; rows 1225; peak 3246 MB |
| ooooho_40h | 2 |  | certified | 00:20:25 | 6021.1 | 19967748 | trim.cnf 39fe21cca123a2416474c1d39fa28c59af407d6b191a8b438393ab423d761c2c; rows 1417; peak 2847 MB |
| ooohoo_40h | 2 |  | split | 00:20:29 | 7216.7 | 28762595 | split on 52; peak 2782 MB |
| oohooo_40h | 2 |  | certified | 00:47:07 | 4200.5 | 12522004 | trim.cnf 9a1113080998e9d37f6dd4e9d96652dcf24f0f4e8cbe9e69fddb08db6f75e94c; rows 1557; peak 3197 MB |
| ohoooo_40h | 2 |  | certified | 01:26:44 | 4560.7 | 13867320 | trim.cnf 9372e76545cf57b70efd6ceb3c247cd76b31ab2056856f7e7d96de9a1e339496; rows 1687; peak 3244 MB |
| ooohho_40o | 2 |  | split | 03:49:24 | 7215.2 | 20349434 | split on 52; peak 2398 MB |
| oohoho_40o | 2 |  | certified | 03:49:28 | 6461.1 | 14736401 | trim.cnf fceb4e4a21580566893db371226ba41c9acfef3da551067d787f36def09f0323; rows 1660; peak 2706 MB |
| oohhoo_40o | 2 |  | split | 03:49:31 | 7214.6 | 17785757 | split on 52; peak 2633 MB |
| ohooho_40o | 2 |  | certified | 03:56:41 | 7212.7 | 16607266 | trim.cnf 0fe8c7a5487be54b7c30ed9a6ac2da6dab7ffac5b0361cfbec10400927775de7; rows 1925; peak 2686 MB |
| ohohoo_40o | 2 |  | split | 03:55:52 | 7214.1 | 17548901 | split on 52; peak 2786 MB |
| hoohoo_40o | 2 |  | certified | 04:06:02 | 7954.9 | 18422663 | trim.cnf c043ee30d57fa51cc296b75d1f7d087606b48f9cdba7540ef7330eaf346534a5; rows 1606; peak 3251 MB |
| hooooo_40h | 2 |  | certified | 11:39:49 | 3571.2 | 10413926 | trim.cnf c9feba1190e7b15428f57dd3f3f0eaa8ccbf52da76feec376528934d0afb8784; rows 1042; peak 3245 MB |
| oooooo_40h_52h | 2 |  | certified | 05:05:45 | 2997.0 | 4113837 | trim.cnf 5016e9f55c395a9ad9e0a29790a83ff754036a01bb329ae4f99f07056ed486b5; rows 1395; peak 2527 MB |
| ooooho_40o_52h | 2 |  | certified | 05:37:48 | 5121.0 | 9371639 | trim.cnf b9cb1fc994dbb45a01f13071e06ab80706c48216f895e4003cd499c581d5362e; rows 1571; peak 3203 MB |
| ooohoo_40o_52h | 2 |  | certified | 05:49:52 | 7492.9 | 17093352 | trim.cnf 9a19070d16182de3fe37148d14a4ae94244347ec1c6ead2b93085d3db104da03; rows 1690; peak 3253 MB |
| oohooo_40o_52h | 2 |  | certified | 05:57:41 | 3239.1 | 5412222 | trim.cnf cbcc73dd2b16bf25d4991b880e553b42f96ea940a38525e0bafbc8ec5fb59b13; rows 1464; peak 2687 MB |
| ohoooo_40o_52h | 2 |  | certified | 06:19:29 | 3888.8 | 7280381 | trim.cnf f35c3e402b60ab92c311d84ac79353e6ea2953a15ebab351dd3dfae32dbdc5b9; rows 1537; peak 3177 MB |
| ooohoo_40h_52o | 2 |  | split | 06:28:30 | 7220.5 | 20893527 | split on 46; peak 2849 MB |
| ooohho_40o_52o | 2 |  | certified | 06:51:59 | 7081.2 | 16120223 | trim.cnf 7c3fef6fe5cf4758d4169c1e9c9b0b0f5452098fa08fe6fe196ce84b3e182c55; rows 1486; peak 2663 MB |
| oohhoo_40o_52o | 2 |  | split | 07:03:38 | 7221.4 | 17458592 | split on 46; peak 2750 MB |
| ohohoo_40o_52o | 2 |  | split | 07:11:11 | 7219.0 | 18373484 | split on 46; peak 2742 MB |
| oooooo_40o_52h_46h | 2 |  | certified | 07:24:38 | 2222.2 | 2721568 | trim.cnf 0228c1280e2079eb19ad0a1a6204a145bc976007509167e152d6b5aa79b9095a; rows 1637; peak 2771 MB |
| oooooo_40h_52o_46h | 2 |  | certified | 07:33:27 | 2717.8 | 4033427 | trim.cnf 42e89a2a788eecc4248a46cae1bce718d9597cf1fabd0ed55fbac13341351cd4; rows 1632; peak 2704 MB |
| ooooho_40o_52o_46h | 2 |  | certified | 07:39:26 | 4453.0 | 8516925 | trim.cnf 212f691b2814fb50c152d3f32f46b94a88a932ea55ffd02836cecbef71b82b3b; rows 1597; peak 3184 MB |
| ooohoo_40o_52o_46h | 2 |  | certified | 07:55:28 | 6010.8 | 13328042 | trim.cnf aa99ea90ddd7fe13713ce87b650d4cd281cbd6593902442ac7df89eab8560322; rows 1478; peak 3247 MB |
| oohooo_40o_52o_46h | 2 |  | certified | 08:01:58 | 3109.4 | 5159011 | trim.cnf 6f4c871d95677398c34fab5e77ed8e0bdb21bdc9bb8f2c94b3c38a98f71b9ceb; rows 1433; peak 2793 MB |
| ohoooo_40o_52o_46h | 2 |  | certified | 08:18:58 | 3426.8 | 5955145 | trim.cnf 2ac6fc43ab101fc84e5758f21de0348de33419df12f1a2da169b29b47520becc; rows 1549; peak 3213 MB |
| ooohoo_40h_52o_46o | 2 |  | certified | 08:50:36 | 7249.7 | 17843982 | trim.cnf e326108f0b4a11f68da65dec6cffea0a0d87160561e4715c27507cf7ca653530; rows 1383; peak 2508 MB |
| oohhoo_40o_52o_46o | 2 |  | certified | 09:16:30 | 5631.3 | 12093418 | trim.cnf 6a80c74ba027bf48493d4581b0b29f4112bb4669d7247493ebf765c57e3f6707; rows 1523; peak 3234 MB |
| ohohoo_40o_52o_46o | 2 |  | certified | 09:31:00 | 5150.5 | 11929020 | trim.cnf a6234e3addfb69f60ec831d9bb21ad84a1f538fd0d5c416816023566ac096dcd; rows 1381; peak 2710 MB |
| oooooo_40o_52o_46h_44h | 2 |  | certified | 08:53:59 | 2592.2 | 3127895 | trim.cnf 2a199b9f8198323456ce15b290fa83a8b714d0684a7529c189040f5807fccb3b; rows 1689; peak 2721 MB |
| oooooo_40o_52h_46o_44h | 2 |  | certified | 08:54:19 | 2189.7 | 2452650 | trim.cnf c84b4ab55190be3680a53d5bb408b457df397e068b6eb5e026ddd9dbc9fa948c; rows 1674; peak 2775 MB |
| oooooo_40h_52o_46o_44h | 2 |  | certified | 09:36:13 | 2191.5 | 3072834 | trim.cnf 5e046f5843c700e0780cf812018e05d3d5b1d36e3ec8d69f46d579542312f071; rows 1452; peak 2756 MB |
| oooooh | 1 |  | certified | 09:37:35 | 6179.5 | 16619331 | trim.cnf 05ced6291e67e30e785cf1d7b3e55f37165c02893a178ac8e71681e7ed7f7081; rows 1691; peak 2775 MB |
| ooooho | 1 |  | split |  |  |  | split on 40 |
| ooohoo | 1 |  | split |  |  |  | split on 40 |
| oohooo | 1 |  | split |  |  |  | split on 40 |
| ohoooo | 1 |  | split |  |  |  | split on 40 |
| hooooo | 1 |  | split | 09:39:11 | 7218.2 | 24259626 | split on 40; peak 2824 MB |
| oooooo_40h | 1 |  | split |  |  |  | split on 52 |
| ooooho_40o | 1 |  | split |  |  |  | split on 52 |
| ooohoo_40o | 1 |  | split |  |  |  | split on 52 |
| oohooo_40o | 1 |  | split |  |  |  | split on 52 |
| ohoooo_40o | 1 |  | split |  |  |  | split on 52 |
| hooooo_40o | 1 |  | certified | 11:48:39 | 4677.7 | 18126978 | trim.cnf 4d256e44c7ee99bd489eaeae427c867925992efe4c184e970ea13967fdbb7990; rows 1381; peak 2657 MB |
| oooooo_40o_52h | 1 |  | split |  |  |  | split on 46 |
| oooooo_40h_52o | 1 |  | split |  |  |  | split on 46 |
| ooooho_40o_52o | 1 |  | split |  |  |  | split on 46 |
| ooohoo_40o_52o | 1 |  | split |  |  |  | split on 46 |
| oohooo_40o_52o | 1 |  | split |  |  |  | split on 46 |
| ohoooo_40o_52o | 1 |  | split |  |  |  | split on 46 |
| oooooo_40o_52o_46h | 1 |  | split |  |  |  | split on 44 |
| oooooo_40o_52h_46o | 1 |  | split |  |  |  | split on 44 |
| oooooo_40h_52o_46o | 1 |  | split |  |  |  | split on 44 |
| ooooho_40o_52o_46o | 1 |  | certified | 10:13:01 | 5060.4 | 10433790 | trim.cnf 6fc4de0eb3a170d3a2bf08ea9bb7e47d8ae55e7ce10029be54b8a4d3b67bd831; rows 2185; peak 2936 MB |
| ooohoo_40o_52o_46o | 1 |  | certified | 10:20:49 | 7026.2 | 17382800 | trim.cnf 6a44cc133bc9c8e9101b9668920422ff22c84d142060ecf395a05dec8f493a10; rows 2097; peak 3254 MB |
| oohooo_40o_52o_46o | 1 |  | certified | 10:26:33 | 3464.5 | 5950090 | trim.cnf 28bf62e62aeb40e71dc12589166ede5531046e24a6c48a6ca75d9d32150f79e6; rows 1889; peak 2420 MB |
| ohoooo_40o_52o_46o | 1 |  | certified | 10:51:01 | 3829.4 | 6866120 | trim.cnf 57d176815fdb370defb547fd4f7039a5442e93256322060d2054062ae8b0e65e; rows 1973; peak 3241 MB |
| oooooo_40o_52o_46o_44h | 1 |  | certified | 10:52:07 | 3372.3 | 5117901 | trim.cnf 53350e0f1c29d6490c2eeff7a58c7b54f17108e5a895aa6a08882d692701d60a; rows 1711; peak 3258 MB |
| oooooo_40o_52o_46h_44o | 1 |  | certified | 10:57:19 | 2432.8 | 3017994 | trim.cnf 05c8f1c19fce562fc1c30b3763d4c9ad28993812e15ee06d535434298531e290; rows 2005; peak 2806 MB |
| oooooo_40o_52h_46o_44o | 1 |  | certified | 11:21:16 | 1870.0 | 1695947 | trim.cnf cf360c787fbf21334f2a0c3933140f5acdf68e93a4572486b06b3b6443638835; rows 1752; peak 2777 MB |
| oooooo_40h_52o_46o_44o | 1 |  | certified | 11:24:42 | 2671.8 | 3682803 | trim.cnf af4dd15ae1562e43207b0b6ae8efd32719ffab708f5ea7a9cc36ea367586ca4e; rows 1658; peak 2579 MB |
| oooooo_40o_52o_46o_44o_45h | 1 |  | certified | 11:37:56 | 1386.5 | 874830 | trim.cnf 8128d6d961a71ad8488a3a63c0c2e6d2aa11f7dcc6530549809ee4b68c02d836; rows 1561; peak 2815 MB |
| oooooo_40o_52o_46o_44o_45o_39h | 1 |  | certified | 11:38:16 | 1354.3 | 802918 | trim.cnf 0f75e41f396b080de6c4ecd54e3d6844a2c99e5f38c96e76237c97b5c5acd242; rows 1770; peak 2818 MB |
| oooooo | 0 |  | split |  |  |  | split on 40 |
| oooooo_40o | 0 |  | split |  |  |  | split on 52 |
| oooooo_40o_52o | 0 |  | split |  |  |  | split on 46 |
| oooooo_40o_52o_46o | 0 |  | split |  |  |  | split on 44 |
| oooooo_40o_52o_46o_44o | 0 |  | split |  |  |  | split on 45 |
| oooooo_40o_52o_46o_44o_45o | 0 |  | split |  |  |  | split on 39 |
| oooooo_40o_52o_46o_44o_45o_39o | 0 |  | certified | 11:52:34 | 1156.6 | 653589 | trim.cnf b7cdd8f9e70ed6e509e270df0019bfa6613f5c6f0ffd8d3588f3c597e6e69408; rows 2032; peak 2979 MB |

## Log (last 40)

```
09:36:13 start oooooo_40h_52o_46o_44h (holes 2, band 5, UP False, limit 7200 s, MemoryMax 6500M)
09:37:33 end oooooo_40o_52o_46h_44h: certified ok (wall 2592.2 s, conflicts 3127895)
09:37:35 start oooooh (holes 1, band 5, UP False, limit 7200 s, MemoryMax 6500M)
09:39:10 end ooohoo_40h_52o_46h: certified ok (wall 4174.8 s, conflicts 9279539)
09:39:11 start hooooo (holes 1, band 5, UP False, limit 7200 s, MemoryMax 6500M)
10:13:00 end oooooo_40h_52o_46o_44h: certified ok (wall 2191.5 s, conflicts 3072834)
10:13:01 start ooooho_40o_52o_46o (holes 1, band 6, UP False, limit 7200 s, MemoryMax 6500M)
10:20:48 end ohohoo_40o_52o_46h: certified ok (wall 4107.9 s, conflicts 8733767)
10:20:49 start ooohoo_40o_52o_46o (holes 1, band 6, UP False, limit 7200 s, MemoryMax 6500M)
10:26:32 end oohhoo_40o_52o_46h: certified ok (wall 4914.2 s, conflicts 10212154)
10:26:33 start oohooo_40o_52o_46o (holes 1, band 6, UP False, limit 7200 s, MemoryMax 6500M)
10:51:00 end oohhoo_40o_52o_46o: certified ok (wall 5631.3 s, conflicts 12093418)
10:51:01 start ohoooo_40o_52o_46o (holes 1, band 6, UP False, limit 7200 s, MemoryMax 6500M)
10:52:06 end ooohoo_40h_52o_46o: certified ok (wall 7249.7 s, conflicts 17843982)
10:52:07 start oooooo_40o_52o_46o_44h (holes 1, band 6, UP False, limit 7200 s, MemoryMax 6500M)
10:57:18 end ohohoo_40o_52o_46o: certified ok (wall 5150.5 s, conflicts 11929020)
10:57:19 start oooooo_40o_52o_46h_44o (holes 1, band 6, UP False, limit 7200 s, MemoryMax 6500M)
11:21:15 end oooooh: certified ok (wall 6179.5 s, conflicts 16619331)
11:21:16 start oooooo_40o_52h_46o_44o (holes 1, band 6, UP False, limit 7200 s, MemoryMax 6500M)
11:24:40 end oohooo_40o_52o_46o: certified ok (wall 3464.5 s, conflicts 5950090)
11:24:42 start oooooo_40h_52o_46o_44o (holes 1, band 6, UP False, limit 7200 s, MemoryMax 6500M)
11:37:55 end ooooho_40o_52o_46o: certified ok (wall 5060.4 s, conflicts 10433790)
11:37:56 start oooooo_40o_52o_46o_44o_45h (holes 1, band 6, UP False, limit 7200 s, MemoryMax 6500M)
11:38:15 end oooooo_40o_52o_46h_44o: certified ok (wall 2432.8 s, conflicts 3017994)
11:38:16 start oooooo_40o_52o_46o_44o_45o_39h (holes 1, band 6, UP False, limit 7200 s, MemoryMax 6500M)
11:39:48 end hooooo: split  (wall 7218.2 s, conflicts 24259626)
11:39:49 start hooooo_40h (holes 2, band 4, UP False, limit 7200 s, MemoryMax 6500M)
11:48:37 end oooooo_40o_52o_46o_44h: certified ok (wall 3372.3 s, conflicts 5117901)
11:48:39 start hooooo_40o (holes 1, band 5, UP False, limit 7200 s, MemoryMax 6500M)
11:52:33 end oooooo_40o_52h_46o_44o: certified ok (wall 1870.0 s, conflicts 1695947)
11:52:34 start oooooo_40o_52o_46o_44o_45o_39o (holes 0, band 7, UP False, limit 7200 s, MemoryMax 6500M)
11:55:12 end ohoooo_40o_52o_46o: certified ok (wall 3829.4 s, conflicts 6866120)
12:01:05 end oooooo_40o_52o_46o_44o_45o_39h: certified ok (wall 1354.3 s, conflicts 802918)
12:01:21 end oooooo_40o_52o_46o_44o_45h: certified ok (wall 1386.5 s, conflicts 874830)
12:09:26 end oooooo_40h_52o_46o_44o: certified ok (wall 2671.8 s, conflicts 3682803)
12:11:57 end oooooo_40o_52o_46o_44o_45o_39o: certified ok (wall 1156.6 s, conflicts 653589)
12:18:30 end ooohoo_40o_52o_46o: certified ok (wall 7026.2 s, conflicts 17382800)
12:39:50 end hooooo_40h: certified ok (wall 3571.2 s, conflicts 10413926)
13:07:07 end hooooo_40o: certified ok (wall 4677.7 s, conflicts 18126978)
13:07:08 driver end
```

## Monitor

```bash
cat /home/jay/research/data/n66-20261113/p2/c15/campaign_status.json | head -c 2000
systemctl --user list-units "esr-n66-*"
journalctl --user -u esr-n66-drv15 -n 30 --no-pager
```
