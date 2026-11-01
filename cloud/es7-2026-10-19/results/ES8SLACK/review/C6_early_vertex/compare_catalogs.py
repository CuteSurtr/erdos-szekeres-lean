import gzip, json, re, sys
import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = _os.path.dirname(_os.path.dirname(HERE))  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
def lean_catalog(path):
    txt = open(path).read()
    m = re.search(r'def catalog : List \(List Nat\) := (\[\[.*?\]\])', txt, re.S)
    return json.loads(m.group(1))
lb = lean_catalog(ROOT + '/ErdosSzekeres/Omission/BalancedCatalogData.lean')
lr = lean_catalog(ROOT + '/ErdosSzekeres/Omission/ResidualCatalogData.lean')
jb = json.load(open(ROOT + '/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json'))['states']
jr = json.loads(gzip.decompress(open(ROOT + '/experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz', 'rb').read()))['states']
print('balanced lean len', len(lb), 'json len', len(jb), 'identical order:', lb == jb)
print('residual lean len', len(lr), 'json len', len(jr), 'identical order:', lr == jr)
print('balanced 0..3:', lb[:4]); print('residual 0,1,2,4,7:', [lr[i] for i in (0,1,2,4,7)])
# also the Lean-side catalogs used by the certificates (support index spaces) are Fin 252 / Fin 154
sys.exit(0 if (lb == jb and lr == jr) else 1)
