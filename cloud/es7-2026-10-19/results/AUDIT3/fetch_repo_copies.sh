#!/bin/bash
# Restore the byte-identical copies of repository files that the audit scripts import or read.
# They were not committed twice; this copies them from the repository and checks each SHA-256.
# Run from cloud/es7-2026-10-19/results:  bash AUDIT3/fetch_repo_copies.sh
set -eu
ok=0; bad=0
put() {  # destination (under AUDIT3) <- source (under results), expected sha256
  mkdir -p "AUDIT3/$(dirname "$1")"; cp "$2" "AUDIT3/$1"
  if [ "$(shasum -a 256 "AUDIT3/$1" | cut -d" " -f1)" = "$3" ]; then ok=$((ok+1)); else echo "SHA-256 MISMATCH: $1 <- $2"; bad=$((bad+1)); fi
}
put A2_threefold/vendor/c3cnf.py C3a/c3cnf.py cf73093932ef3914c33e7e909e6cf4f97f6b0b0ac30997d2050afa9508e53b3a
put A2_threefold/vendor/hullcase.py C3U2/tools/hullcase.py 2a1ce4070974a38738dedc5b31a32da77813e51cd6b3ba2c0a79d3c89fe8a3c3
put A2_threefold/vendor/compose_C3U2.py C3U2/tools/compose.py 3c4d544f1c8626cd93d5181f0b76e3d1a031731e2a324308dd19853296b28f3e
put A2_threefold/verify_F3/vendor/c3cnf.py C3a/c3cnf.py cf73093932ef3914c33e7e909e6cf4f97f6b0b0ac30997d2050afa9508e53b3a
put A2_threefold/verify_F3/vendor/hullcase.py C3-S/tools/hullcase.py d393bdeb91ae1a9a2e6ca411608d27f5e628e1ddd19451af8b1cd6975546aa4a
put A3_mirror/verify_A3-F3/zcnf_copy.py SYMZ/zcnf.py 13d6c162a617cff6f4c164d6c921efef18ee58df0e913f6fe98f63b5213a0989
put A3_mirror/verify_A3-F3/zcnf_v1_copy.py SYMZ/zcnf_v1.py 8fb8a3ab6364214bb575d36b96366a512bbac6e0ab3e49891dd6c05a24a35a3d
put A4_fivefold_layers/enc/symcnf.py SYM5/symcnf.py a8056da0c403e529ffaa2c80feffe12de7647d7dc26a641f58150a1b6faaa746
put A4_fivefold_layers/enc/symcnf_layers.py SYM5/symcnf_layers.py 71b2d7e7a778e2552a6aedc183129465bab8ad12677783ee6e7b343b6f1de58e
put A4_fivefold_layers/verify_A4-1/symcnf.py SYM5/symcnf.py a8056da0c403e529ffaa2c80feffe12de7647d7dc26a641f58150a1b6faaa746
put A4_fivefold_layers/verify_A4-1/symcnf_layers.py SYM5/symcnf_layers.py 71b2d7e7a778e2552a6aedc183129465bab8ad12677783ee6e7b343b6f1de58e
put A4_fivefold_layers/verify_A4-2/enc/symcnf.py SYM5/symcnf.py a8056da0c403e529ffaa2c80feffe12de7647d7dc26a641f58150a1b6faaa746
put A4_fivefold_layers/verify_A4-2/enc/symcnf_layers.py SYM5/symcnf_layers.py 71b2d7e7a778e2552a6aedc183129465bab8ad12677783ee6e7b343b6f1de58e
put A4_fivefold_layers/verify_A4-3/enc/symcnf.py SYM5/symcnf.py a8056da0c403e529ffaa2c80feffe12de7647d7dc26a641f58150a1b6faaa746
put A4_fivefold_layers/verify_A4-3/enc/symcnf_layers.py SYM5/symcnf_layers.py 71b2d7e7a778e2552a6aedc183129465bab8ad12677783ee6e7b343b6f1de58e
put A4_fivefold_layers/verify_A4-4/scripts/verify_cuts_copy.py C4CUT/verify_cuts.py 0cc29fb1ed753d9026d5a1a014afe3616097625f343b8c06174c9b4a4ee82cd2
put A6_certificates/verify_A6-3/scripts/verify_cuts_repo.py C4CUT/verify_cuts.py 0cc29fb1ed753d9026d5a1a014afe3616097625f343b8c06174c9b4a4ee82cd2
put A6_certificates/verify_A6-3/data/cuts.jsonl C4CUT/cuts.jsonl 3852ece5c7c5496a9bc0d5576e9894ddc182ed847b20b51102dc0a46df54c7de
put A6_certificates/verify_A6-4/gen/symcnf.py SYM5/symcnf.py a8056da0c403e529ffaa2c80feffe12de7647d7dc26a641f58150a1b6faaa746
put A6_certificates/verify_A6-4/gen/symcnf_layers.py SYM5/symcnf_layers.py 71b2d7e7a778e2552a6aedc183129465bab8ad12677783ee6e7b343b6f1de58e
put A7_examples/repo_copy/build_sym2.py SYM2/build.py 02c924cebbb969a0b28dfbbe19ff043ff6e446fe1d73458c54141d23534bb398
put A7_examples/verify_A7-2/build_copy.py SYM2/build.py 02c924cebbb969a0b28dfbbe19ff043ff6e446fe1d73458c54141d23534bb398
put A7_examples/project_checkers_on_copies/code/verifyg.py SYMMAX/verifyg.py 8c38a1fd1d805625d2b9384ad757346b57b41e05284b13c706bb93234e724f80
put A7_examples/project_checkers_on_copies/code/verify5.py SYMMAX/verify5.py 11b755f5726437da975a458daf6aeae94b6053bc2f92817b508a866f58d1a1fe
put A7_examples/project_checkers_on_copies/code/brute.c SYMMAX/brute.c f84b9227a4aeea41e54f16df8ea6229fe407639da893d9f9f4badf71054743df
put A7_examples/project_checkers_on_copies/code/convex.py SYMMAX/convex.py cf14264f0bdaca53e8434e097711f3ca631748c0549ee9c64f8e9a6f4e3f4cdf
put A7_examples/project_checkers_on_copies/data/c3_27points.txt SYMMAX/c3_27points.txt 4fa6a01ad1915b31e67d008865a2eb2265544ebc6f56cc7c56484f49eda426dd
put A7_examples/project_checkers_on_copies/data/c3_30points.txt SYMMAX/c3_30points.txt c57cc5676a9ce0cac3dee8cdd9379a6339b8071c62c510f6f7e9ab86cb398889
put A7_examples/project_checkers_on_copies/data/c3_31points.txt SYMMAX/c3_31points.txt f02201938dc5a52b85fc5854abf7dabc7a4a92e56eafcbd8f4dfcabbff7b6d01
put A7_examples/project_checkers_on_copies/data/c4_28points.txt SYMMAX/c4_28points.txt 86d4e0bf800197f224f942b6648fedece339a3e835ee7ddcc7acd1252bf5288d
put A7_examples/project_checkers_on_copies/data/c5_30points.txt SYMMAX/c5_30points.txt f709fb9022624f25117efa75959bfe731bdd149af9e546b6fee431b83b81ec44
put A7_examples/project_checkers_on_copies/data/c5_31points.txt SYMMAX/c5_31points.txt 4f1e2e6351a76f3844e1810ef669bf57d8dbfabb3aaa350dbecfc0ea7d9e3af8
put A7_examples/project_checkers_on_copies/data/c5_31minus_centre.txt SYM5/c5_31minus_centre.txt b9932fe3327feb59a87d57bfe0e38d4a9b688aff6bccb194d9253e404039257f
put A7_examples/project_checkers_on_copies/data/c6_30points.txt SYMMAX/c6_30points.txt 40745fe61e5bd7a80d2fb0bd89fcaac98ad6b9ab4c945a2ee7a6c51b1fb76700
put A7_examples/project_checkers_on_copies/data/k6_c2_16points.txt SYMMAX/k6/c2_16points.txt 0acbd38bba7e720868cdbe0b754bd469936d2f502f8e1809afef8ef68f28dec2
put A7_examples/project_checkers_on_copies/data/k6_c3_13points.txt SYMMAX/k6/c3_13points.txt 40e1309cbc537723204fbf844ab94aa0fbe42f356d2ee1c88607dc2b8d87d911
put A7_examples/project_checkers_on_copies/data/k6_c4_16points.txt SYMMAX/k6/c4_16points.txt 8fbd03efd20276041a586c240b3eee54e8d901fca5bc7c83b14cd5835279ed3c
put A7_examples/project_checkers_on_copies/data/k6_c5_16points.txt SYMMAX/k6/c5_16points.txt 53e14a5aa4499fe55205fe17b20dc69f24cd16ea87df2e98af5cc61d9cc40eaf
put A7_examples/project_checkers_on_copies/data/k6_mirror_12points.txt SYMMAX/k6/mirror_12points.txt 2a206f670d992b689743630dd38b2fe46047084b0511a035ff2224161204ffd7
put A7_examples/project_checkers_on_copies/data/mirror_32points.txt SYMMAX/mirror_32points.txt 255e2390694b7fbbd29556ee41a96454221d5f60bcb8da9249a822ef1c69f217
put A7_examples/project_checkers_on_copies/data/sym7_32points.txt SYM2/sym7_32points.txt 7246a30aa9669c9cae70328209c2020ae6487e6662af1cad9fe98a858ef6e074
echo "$ok copies restored, $bad mismatches"; [ "$bad" -eq 0 ]
