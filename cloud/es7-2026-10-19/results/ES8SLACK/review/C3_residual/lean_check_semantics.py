#!/usr/bin/env python3
"""Literal Python transcription of the Lean `check` function of the coupled templates, applied to
the candidate maps found inside the three 33-hole witnesses (template_instances_out.json).

Transcribed definitions (ErdosSzekeres/Omission at the repository root):
  Domains.Contains s z          := z.2 <= s.getD (z.1-1) 0
  ResidualDomains.grid          := [(x+1,y+1) | x<4, y<6]
  ResidualDomains.difference a b:= grid.filter (Contains b z && !Contains a z)
  ResidualDomains.boundingBox   := present iff difference nonempty; x/y min/max of the difference
  CycleSigns.Safe ab bc ac want := !ab.present || !bc.present || !ac.present ||
                                   (want ? bc.xmax <= ab.xmin : bc.ymax <= ab.ymin)
  CycleSigns.CheckTriple t a b c:= Safe(t a b,t b c,t a c,T) & Safe(t a c,t c b,t a b,F) &
                                   Safe(t b a,t a c,t b c,F) & Safe(t b c,t c a,t b a,T) &
                                   Safe(t c a,t a b,t c b,T) & Safe(t c b,t b a,t c a,F)
  Coupled.Allowed s i j z       := Contains(shape(s j)) z & !Contains(shape(s i)) z & z != (1,6)
  Coupled.emptyCheck s i j      := grid.all (!Allowed s i j z)
  check s := emptyTests.all emptyCheck & domainTests.all (!Allowed s i j (a,b)) &
             positiveTests.all (CheckTriple computedTable (s i) (s j) (s l))
  shape id := ResidualCatalog.catalog.getD id []   (parsed from ResidualCatalogData.lean)
The template theorem `hole_bound` (Lean-checked in the maintained library / experiment bundles)
turns Injective s & Compatible s (implied by check s = true via check_sound) into the row
"image(s) contains a hole" for every actual residual configuration.
Usage: python3 -I lean_check_semantics.py
"""
import ast, gzip, json, random, re

import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = _os.path.dirname(_os.path.dirname(HERE))  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
R = ROOT
E = R + '/experiments'
OM = R + '/ErdosSzekeres/Omission'
TEMPLATES = {
    'Base': OM + '/CoupledTemplate.lean', 'Second': OM + '/CoupledTemplateSecond.lean',
    'Third': OM + '/CoupledTemplateThird.lean', 'Fourth': OM + '/CoupledTemplateFourth.lean',
    'Fifth': OM + '/CoupledTemplateFifth.lean', 'Nine': OM + '/CoupledTemplateNine.lean',
    'Sixth': E + '/omission-residual32-sixth-variants-2026-10-10/SixthTemplate.lean',
    'SixthRelaxed': E + '/omission-residual32-sixth-relaxed-2026-10-10/SixthRelaxedTemplate.lean'}

cat_txt = open(OM + '/ResidualCatalogData.lean').read()
catalog = ast.literal_eval(re.search(r'def catalog : List \(List Nat\) := (\[\[.*?\]\])\s*$', cat_txt, re.M | re.S).group(1))
assert len(catalog) == 154
json_states = json.loads(gzip.decompress(open(E + '/omission-residual32-rank-global-2026-10-10/source-2650.json.gz', 'rb').read()))['states']
catalog_eq_json = (catalog == json_states)

def getD(s, k):
    return s[k] if 0 <= k < len(s) else 0

def contains(s, z):
    return z[1] <= getD(s, z[0] - 1)

GRID = [(x + 1, y + 1) for x in range(4) for y in range(6)]

def box(a, b):
    sa, sb = catalog[a], catalog[b]
    d = [z for z in GRID if contains(sb, z) and not contains(sa, z)]
    if not d:
        return (False, 0, 0, 0, 0)
    return (True, min(z[0] for z in d), max(z[0] for z in d), min(z[1] for z in d), max(z[1] for z in d))

BOX = [[box(a, b) for b in range(154)] for a in range(154)]

def safe(ab, bc, ac, want):
    if not ab[0] or not bc[0] or not ac[0]:
        return True
    return bc[2] <= ab[1] if want else bc[4] <= ab[3]

def check_triple(a, b, c):
    t = lambda u, v: BOX[u][v]
    return (safe(t(a, b), t(b, c), t(a, c), True) and safe(t(a, c), t(c, b), t(a, b), False) and
            safe(t(b, a), t(a, c), t(b, c), False) and safe(t(b, c), t(c, a), t(b, a), True) and
            safe(t(c, a), t(a, b), t(c, b), True) and safe(t(c, b), t(b, a), t(c, a), False))

def allowed(s, i, j, z):
    return contains(catalog[s[j]], z) and not contains(catalog[s[i]], z) and z != (1, 6)

def load(path):
    txt = open(path).read()
    out = {}
    for name in ('emptyTests', 'domainTests', 'positiveTests'):
        m = re.search(r'^def ' + name + r' : List \(Fin (\d+) [^\n]*?:= (\[[^\n]*\])$', txt, re.M)
        out['k'] = int(m.group(1))
        out[name] = [tuple(x) for x in ast.literal_eval(m.group(2))]
    return out

def check(T, s):
    if len(s) != T['k']:
        return False
    e = all(all(not allowed(s, i, j, z) for z in GRID) for i, j in T['emptyTests'])
    d = all(not allowed(s, i, j, (a, b)) for i, j, a, b in T['domainTests'])
    p = all(check_triple(s[i], s[j], s[l]) for i, j, l in T['positiveTests'])
    return e and d and p

T = {n: load(p) for n, p in TEMPLATES.items()}
res = {'catalog_eq_json_states': catalog_eq_json}

# positive control: the 128 kernel-checked Fourth global variants (row-bindings.json) must pass
rb = json.load(open(E + '/omission-residual32-fourth-global-variants-2026-10-10/row-bindings.json'))
rows = rb['rows'] if isinstance(rb, dict) and 'rows' in rb else rb
maps = []
for r in rows:
    m = r.get('mapping')
    maps.append(m)
res['fourth_variants_found'] = len(maps)
res['fourth_variants_all_pass'] = all(m is not None and check(T['Fourth'], m) and len(set(m)) == 13 for m in maps)
# negative control: random injective maps (and the variants with one owner changed) should mostly fail
rng = random.Random(1)
res['random_maps_passing_Fourth'] = sum(check(T['Fourth'], rng.sample(range(154), 13)) for _ in range(2000))
mut_pass = 0; mut_total = 0
for m in maps[:32]:
    for pos in range(13):
        mm = list(m)
        choices = [v for v in range(154) if v not in mm]
        mm[pos] = rng.choice(choices)
        mut_total += 1
        mut_pass += check(T['Fourth'], mm)
res['single_owner_mutants_passing'] = f'{mut_pass}/{mut_total}'

# candidates found inside the witnesses
W = json.load(open(TOP + '/witnesses.json'))['residual_2650_33_hole_witnesses_state0_occupied']
ti = json.load(open(HERE + '/template_instances_out.json'))
cands = []
for key, v in ti['witness_results'].items():
    wi = int(key.split(':')[0][1:]); name = key.split(':')[1]
    for m in v['ordered_maps']:
        holes = set(W[wi])
        viol = [k for k, h in enumerate(W) if not (set(m) & set(h))]
        cands.append({'witness': wi, 'template': name, 'map': m, 'injective': len(set(m)) == len(m),
                      'lean_check_transcription': check(T[name], m),
                      'support': sorted(m), 'witness_occupies_support': not (set(m) & holes),
                      'witnesses_violating_this_row': viol})
res['candidates'] = cands
print(json.dumps(res, indent=1))
json.dump(res, open(HERE + '/lean_check_semantics_out.json', 'w'), indent=1)
