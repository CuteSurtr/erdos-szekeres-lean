import sys, json, importlib.util
sys.argv=[sys.argv[0]]+sys.argv[1:]
spec=importlib.util.spec_from_file_location('bfp','<six10-work-dir>/main/bfp.py'); B=importlib.util.module_from_spec(spec); spec.loader.exec_module(B)
L=B.lit_table()
for mp, flips in [('models/c11000_e9871dd0.json',[3096]),('models/c10000_08e6fb6f.json',[4674]),('models/c10000_08e6fb6f.json',[4187]),('models/c10000_08e6fb6f.json',[4674,4187])]:
    tv=set(json.load(open(mp)))
    for v in flips: tv^={v}
    keys,viol=B.rows_for_model(tv,L)
    print(mp, 'flip', flips, 'GP violations after flip:', len(viol), flush=True)
