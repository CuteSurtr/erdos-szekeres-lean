# sha256 checks (W16)
- base m33k7int.sub.cnf regenerated (gen_etv.py 33 7 7 7 --mirror; mirgen.py --interior --yflip-unit, as in results/C/scripts/make_cnfs.sh):
  69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d  MATCH
- verify/ii_wave1.json: 6df36dab6dc93cec474ee7a795b38716bc19bf2d6064468b9c5e38e00901c72e  MATCH
- entry: {"kind": "shard", "case": "U6_L", "shard": 1, "nshards": 2, "vm": "W16"}
- case U6_L (hullsplit.py case BASE 6 "" U6_L.cnf): 8196f2aef46cc55cd21ba4f3d546d838a47b9e3f4e42d7bc5d4487b759871f14  MATCH
- top cubes: march_cu U6_L.cnf -d 7 -o top.icnf -> 128 cubes, 0 refuted leaves, 182 s;
  top.icnf sha256 6ca82ad4c8db1cc6f3174d10c1ef2f3b726440e90b3ec752fc89ce92e9c5fe63 (copy in U6_L/top.icnf).
  Shard 1 of 2 = lines with odd 0-based index: 64 cubes.
