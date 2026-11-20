# N66 level-15 cube campaign: status (live)

**N66 <= 54 is NOT decided.** N66 <= 55 (level 14 cube campaign, CERTIFIED) remains the bound. Written by `W/p2c15_driver.py` at 23:49:05 KST, 20 November 2026; plan and labels in `README.md` of this folder. W = `/home/jay/research/data/n66-20261113`; per-cube files in `W/p2/c15/<id>/it<k>/`; machine status `W/p2/c15/campaign_status.json`.

## Allocation

- Driver p2c15_driver.py (copy of p2c14_driver_r7.py; r4/r5 rules A1 P1-P3 with the time limits x 3: band >= 4 gets 7,200 s, else 3,600 s; MemoryMax 6500M; pre-split of band-6/7 cubes; A1 split order): cube units `esr-n66-c15-<id>`: 1 thread each (CPUQuota 98 %), MemorySwapMax 0, nice 10, RuntimeMaxSec ending by 12:00 KST 23 Nov. At most 5 at a time (now 5; memguard slot penalty 0). No new cube while the disk has less than 120 GB free. Partial files of timed-out runs: deleted (owner OK).
- Each start also needs room: running cubes reserved at 3,800 MB each, n66 track + 3,800 <= n66 budget - 200 MB and all research units + 3,800 <= total - 500 MB (budgets from the running memguard: (17000, 21000)), and 0.98 free thread under the 16-thread cap (summed CPUQuota of active esr-* units).
- The cake_lpr step runs inside the cube unit after CaDiCaL exits (p2_cert.sh -> p2_cake.py, unchanged; heap tiers 2000/3200/4500/5500 MB).
- Driver unit `esr-n66-drv15`: CPUQuota 6 %, MemoryMax 300M. Calibration leaves from `W/p2/cal15` are adopted only through accept().

## Cover argument

- Split states 25 12 16 29 17 37, sel_s = 988541 + s; o = occupied = +sel_s, h = hole = -sel_s; cube ids list the six signs in that order, then `_<s><o|h>` for every re-split state. The 64 sign patterns are all assignments of the six variables, so their disjunction is a tautology.
- Unit propagation on the 79 SB clauses refutes 8 of the 64 (all with 25 h, 29 o, 37 h): hhhohh, hhhooh, hhoohh, hhoooh, hohohh, hohooh, hooohh, hooooh. They run through the same pipeline; like every cube they count only with their own accepted certificate.
- A cube whose CaDiCaL run reaches its time limit is replaced by its children c AND s occupied, c AND s hole, s = the first state of 40 52 46 44 45 39 32 30 20 57 14 53 38 47 33 19 50 58 62 35 23 49 not in c (A1 order since r4; corrected 16 Nov after CN issue 6). The two children cover the parent, so the leaves always cover the 2^6 split.
- Leaves now: 93; exact leaf cover check: COVER_OK.
- Accepted certificates: 51 of 93 leaves. Cover by accepted certificates (cube literals read from each verify.json): not complete.
- Acceptance (level-14 README section 6, with L = 15): cert.json and verify.json ALL_OK; cake.out has the exact line `s VERIFIED UNSAT`; L = 15; W = range(70); the 27-pair SB list of b14h2; the cube field of layout, verify and cert equals the cube; 0 unclassified clauses; trim.cnf SHA-256 recomputed by the driver. Rows are justified by template_cert66 without cube assumptions.

## Counts

certified: 51, queued: 38, running: 4, split: 29

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
| oohhoo_40h | 3 |  | running | 21:53:30 |  |  | peak 2663 MB |
| ohooho_40h | 3 |  | certified | 22:18:13 | 3871.8 | 10639791 | trim.cnf 65833f0d943cbefc4ce852824ae1c5a66493c068ad94d0a0a777ee87140e9cbb; rows 1230; peak 2469 MB |
| oooohh | 2 |  | certified | 17:35:04 | 4893.6 | 15057643 | trim.cnf 6301283bed509e3d1ce3d31e85fb582e6da01d1479333e455333e707de75aee7; rows 1302; peak 2354 MB |
| ooohoh | 2 |  | certified | 17:43:23 | 7703.7 | 27441498 | trim.cnf 86e5e8337211d6bf09168d04cc76e4810a098d45099d8940a923faed3166ac31; rows 1140; peak 3384 MB |
| ooohho | 2 |  | split | 18:17:02 | 7220.6 | 27740720 | split on 40; peak 2742 MB |
| oohooh | 2 |  | certified | 18:42:05 | 4578.5 | 13250409 | trim.cnf 7961e5af744fe3b4a762fb8ef54fbe31ac9095048ab9872a1e52d70ad1c44efb; rows 1206; peak 3215 MB |
| oohoho | 2 |  | split | 18:57:08 | 7217.0 | 24891661 | split on 40; peak 2826 MB |
| oohhoo | 2 |  | split | 19:52:51 | 7217.0 | 23292579 | split on 40; peak 2742 MB |
| ohoooh | 2 |  | certified | 20:12:27 | 4550.7 | 12672887 | trim.cnf 0bffdc5871b4895f562981d5351e9b12b5b4e71e18c78c77c02416cee6daf0f7; rows 1260; peak 3196 MB |
| ohooho | 2 |  | split | 20:17:24 | 7219.5 | 24893849 | split on 40; peak 2766 MB |
| ohohoo | 2 |  | running | 22:37:04 |  |  | peak 2709 MB |
| ohhooo | 2 |  | running | 22:46:57 |  |  | peak 2894 MB |
| hoooho | 2 |  | running | 23:23:18 |  |  | peak 2661 MB |
| hoohoo | 2 |  | queued |  |  |  |  |
| hohooo | 2 |  | queued |  |  |  |  |
| hhoooo | 2 |  | queued |  |  |  |  |
| ooooho_40h | 2 |  | queued |  |  |  |  |
| ooohoo_40h | 2 |  | queued |  |  |  |  |
| oohooo_40h | 2 |  | queued |  |  |  |  |
| ohoooo_40h | 2 |  | queued |  |  |  |  |
| ooohho_40o | 2 |  | queued |  |  |  |  |
| oohoho_40o | 2 |  | queued |  |  |  |  |
| oohhoo_40o | 2 |  | queued |  |  |  |  |
| ohooho_40o | 2 |  | queued |  |  |  |  |
| oooooo_40h_52h | 2 |  | queued |  |  |  |  |
| ooooho_40o_52h | 2 |  | queued |  |  |  |  |
| ooohoo_40o_52h | 2 |  | queued |  |  |  |  |
| oohooo_40o_52h | 2 |  | queued |  |  |  |  |
| ohoooo_40o_52h | 2 |  | queued |  |  |  |  |
| oooooo_40o_52h_46h | 2 |  | queued |  |  |  |  |
| oooooo_40h_52o_46h | 2 |  | queued |  |  |  |  |
| ooooho_40o_52o_46h | 2 |  | queued |  |  |  |  |
| ooohoo_40o_52o_46h | 2 |  | queued |  |  |  |  |
| oohooo_40o_52o_46h | 2 |  | queued |  |  |  |  |
| ohoooo_40o_52o_46h | 2 |  | queued |  |  |  |  |
| oooooo_40o_52o_46h_44h | 2 |  | queued |  |  |  |  |
| oooooo_40o_52h_46o_44h | 2 |  | queued |  |  |  |  |
| oooooo_40h_52o_46o_44h | 2 |  | queued |  |  |  |  |
| oooooh | 1 |  | queued |  |  |  |  |
| ooooho | 1 |  | split |  |  |  | split on 40 |
| ooohoo | 1 |  | split |  |  |  | split on 40 |
| oohooo | 1 |  | split |  |  |  | split on 40 |
| ohoooo | 1 |  | split |  |  |  | split on 40 |
| hooooo | 1 |  | queued |  |  |  |  |
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
| ooooho_40o_52o_46o | 1 |  | queued |  |  |  |  |
| ooohoo_40o_52o_46o | 1 |  | queued |  |  |  |  |
| oohooo_40o_52o_46o | 1 |  | queued |  |  |  |  |
| ohoooo_40o_52o_46o | 1 |  | queued |  |  |  |  |
| oooooo_40o_52o_46o_44h | 1 |  | queued |  |  |  |  |
| oooooo_40o_52o_46h_44o | 1 |  | queued |  |  |  |  |
| oooooo_40o_52h_46o_44o | 1 |  | queued |  |  |  |  |
| oooooo_40h_52o_46o_44o | 1 |  | queued |  |  |  |  |
| oooooo_40o_52o_46o_44o_45h | 1 |  | queued |  |  |  |  |
| oooooo_40o_52o_46o_44o_45o_39h | 1 |  | queued |  |  |  |  |
| oooooo | 0 |  | split |  |  |  | split on 40 |
| oooooo_40o | 0 |  | split |  |  |  | split on 52 |
| oooooo_40o_52o | 0 |  | split |  |  |  | split on 46 |
| oooooo_40o_52o_46o | 0 |  | split |  |  |  | split on 44 |
| oooooo_40o_52o_46o_44o | 0 |  | split |  |  |  | split on 45 |
| oooooo_40o_52o_46o_44o_45o | 0 |  | split |  |  |  | split on 39 |
| oooooo_40o_52o_46o_44o_45o_39o | 0 |  | queued |  |  |  |  |

## Log (last 40)

```
16:11:31 start hohhoo (holes 3, band 4, UP False, limit 7200 s, MemoryMax 6500M)
16:39:30 end hohoho: certified ok (wall 2722.7 s, conflicts 9818516)
16:39:30 start hhooho (holes 3, band 3, UP False, limit 3600 s, MemoryMax 6500M)
16:41:06 end hoohho: certified ok (wall 3363.7 s, conflicts 12811158)
16:41:07 start hhohoo (holes 3, band 4, UP False, limit 7200 s, MemoryMax 6500M)
17:01:50 end ohhhoo: certified ok (wall 6459.9 s, conflicts 24726507)
17:01:51 start hhhooo (holes 3, band 3, UP False, limit 3600 s, MemoryMax 6500M)
17:31:23 end hhooho: certified ok (wall 3088.5 s, conflicts 10851600)
17:31:23 start oohhoh_40o (holes 3, band 3, UP False, limit 3600 s, MemoryMax 6500M)
17:35:04 end hohhoo: certified ok (wall 4972.7 s, conflicts 18151256)
17:35:04 start oooohh (holes 2, band 4, UP False, limit 7200 s, MemoryMax 6500M)
17:41:03 driver c15 restarted; state loaded; 5 slots, band limits 3600/7200 s, presplit, A1 order, disk floor 120 GB, delete partials True
17:43:23 end hhhooo: certified ok (wall 2471.0 s, conflicts 7965007)
17:43:23 start ooohoh (holes 2, band 4, UP False, limit 7200 s, MemoryMax 6500M)
18:17:02 end hhohoo: certified ok (wall 5717.4 s, conflicts 19133761)
18:17:02 start ooohho (holes 2, band 5, UP False, limit 7200 s, MemoryMax 6500M)
18:42:05 end oohhoh_40o: certified ok (wall 4213.9 s, conflicts 12559230)
18:42:05 start oohooh (holes 2, band 4, UP False, limit 7200 s, MemoryMax 6500M)
18:57:08 start oohoho (holes 2, band 5, UP False, limit 7200 s, MemoryMax 6500M)
18:57:27 end oooohh: certified ok (wall 4893.6 s, conflicts 15057643)
19:52:50 end ooohoh: certified ok (wall 7703.7 s, conflicts 27441498)
19:52:51 start oohhoo (holes 2, band 5, UP False, limit 7200 s, MemoryMax 6500M)
19:58:50 end oohooh: certified ok (wall 4578.5 s, conflicts 13250409)
20:12:27 start ohoooh (holes 2, band 4, UP False, limit 7200 s, MemoryMax 6500M)
20:17:24 start ohooho (holes 2, band 5, UP False, limit 7200 s, MemoryMax 6500M)
20:17:44 end ooohho: split  (wall 7220.6 s, conflicts 27740720)
20:57:39 end oohoho: split  (wall 7217.0 s, conflicts 24891661)
20:57:39 start ooohho_40h (holes 3, band 4, UP False, limit 7200 s, MemoryMax 6500M)
21:28:50 end ohoooh: certified ok (wall 4550.7 s, conflicts 12672887)
21:28:51 start oohoho_40h (holes 3, band 4, UP False, limit 7200 s, MemoryMax 6500M)
21:53:29 end oohhoo: split  (wall 7217.0 s, conflicts 23292579)
21:53:30 start oohhoo_40h (holes 3, band 4, UP False, limit 7200 s, MemoryMax 6500M)
22:18:12 end ohooho: split  (wall 7219.5 s, conflicts 24893849)
22:18:13 start ohooho_40h (holes 3, band 4, UP False, limit 7200 s, MemoryMax 6500M)
22:37:03 end oohoho_40h: certified ok (wall 4056.7 s, conflicts 11498371)
22:37:04 start ohohoo (holes 2, band 5, UP False, limit 7200 s, MemoryMax 6500M)
22:46:56 end ooohho_40h: certified ok (wall 6512.0 s, conflicts 20678676)
22:46:57 start ohhooo (holes 2, band 5, UP False, limit 7200 s, MemoryMax 6500M)
23:23:18 end ohooho_40h: certified ok (wall 3871.8 s, conflicts 10639791)
23:23:18 start hoooho (holes 2, band 4, UP False, limit 7200 s, MemoryMax 6500M)
```

## Monitor

```bash
cat /home/jay/research/data/n66-20261113/p2/c15/campaign_status.json | head -c 2000
systemctl --user list-units "esr-n66-*"
journalctl --user -u esr-n66-drv15 -n 30 --no-pager
```
