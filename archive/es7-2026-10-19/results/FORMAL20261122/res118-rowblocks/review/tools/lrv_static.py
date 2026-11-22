#!/usr/bin/env python3
"""Reviewer's static checks (read-only): (a) module-shadow check over the LEAN_PATH roots of the worker's
tools/env_geo.sh: no module (relative .olean path) is provided by two roots; (b) source scan of the worker's Lean
sources and of the ENCBLEAN modules they import, for constructs that would add trust or change meaning.
Writes argv[1] (JSON)."""
import json, os, re, sys

R = '/home/jay/research/lean/erdos-szekeres-lean'
P = R + '/.lake/packages'
TC = '/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0'
ENCB = R + '/archive/es7-2026-10-19/results/ENCBLEAN'
R118 = '/home/jay/research/data/formalize-20261122/res118'
D = '/home/jay/research/data/formalize-20261122/res118-rowblocks'
ROOTS = [P + f'/{p}/.lake/build/lib/lean' for p in
         ['Cli', 'batteries', 'Qq', 'aesop', 'proofwidgets', 'importGraph', 'LeanSearchClient', 'plausible', 'mathlib']]
ROOTS += [R + '/.lake/build/lib/lean', TC + '/lib/lean',
          R + '/experiments/omission-compact-checker-2026-11-05/build/chain311/olean',
          '/home/jay/research/data/bal186-20261119/zrow/leanz/olean', ENCB + '/.lake/build/lib/lean', R118 + '/olean',
          D + '/build/olean']
env = open(D + '/tools/env_geo.sh').read()
m = re.search(r'export LEAN_PATH="([^"]*)"', env)
expanded = m.group(1)
for k, v in [('$P', P), ('$R118', R118), ('$TC', TC), ('$ENCB', ENCB), ('$D', D), ('$R', R)]:
    expanded = expanded.replace(k, v)
assert expanded.split(':') == ROOTS, (expanded.split(':'), ROOTS)  # the roots above are exactly env_geo.sh's
rep = {'roots': ROOTS}
owners = {}
for r in ROOTS:
    for dp, dn, fn in os.walk(r, followlinks=True):
        for f in fn:
            if f.endswith('.olean'):
                rel = os.path.relpath(os.path.join(dp, f), r)
                owners.setdefault(rel, []).append(r)
dups = {k: v for k, v in owners.items() if len(v) > 1}
rep['modules'] = len(owners)
rep['duplicates'] = dups
key_mods = ['RowGeo/Blocks.olean', 'RowGeo/Sound.olean', 'RowGeo/Text.olean', 'RowEnc/Enc.olean',
            'RowEnc/States.olean', 'RowEnc/StatesData.olean', 'Res118/Final.olean', 'Res118/Glue.olean',
            'Res118/Rows.olean', 'EncB/Compose.olean', 'EncB/Render.olean', 'EncB/Dimacs.olean',
            'ErdosSzekeres/Omission/CoupledSemantics.olean', 'ErdosSzekeres/Omission/Partition.olean',
            'Residual32Bridge2650/Rows.olean', 'Transfer.olean', 'LemmaZ.olean', 'ZeroState.olean']
rep['key_module_roots'] = {k: owners.get(k) for k in key_mods}

pat = re.compile(r'\b(sorry|admit|axiom|native_decide|implemented_by|extern|unsafe|opaque|csimp|macro|notation|'
                 r'elab|syntax|instance|attribute|local|set_option|variable|include|noncomputable|private|'
                 r'decide|ofReduceBool|Lean\.ofReduceBool|reduceBool)\b')
srcs = sorted([os.path.join(dp, f) for dp, _, fn in os.walk(D + '/lean') for f in fn if f.endswith('.lean')])
srcs += [ENCB + f'/EncB/{m}.lean' for m in ['Render', 'Dimacs', 'Compose', 'Satisfiable', 'Gen', 'Coded', 'Cover']]
scan = {}
for s in srcs:
    hits = {}
    text = open(s).read()
    # blank out block comments /- ... -/ (docstrings included), keeping line numbers
    text = re.sub(r'/-.*?-/', lambda m: re.sub(r'[^\n]', ' ', m.group(0)), text, flags=re.S)
    for ln, line in enumerate(text.split('\n'), 1):
        code = line.split('--')[0]
        for w in pat.findall(code):
            hits.setdefault(w, []).append(ln)
    scan[s] = {k: (v if len(v) <= 12 else v[:12] + [f'... {len(v)} total']) for k, v in hits.items()}
rep['scan'] = scan
json.dump(rep, open(sys.argv[1], 'w'), indent=1)
print(json.dumps({'modules': rep['modules'], 'duplicates': len(dups), 'dups': list(dups)[:20]}, indent=1))
for s, h in scan.items():
    bad = {k: v for k, v in h.items() if k in ('sorry', 'admit', 'axiom', 'native_decide', 'implemented_by', 'extern',
                                               'unsafe', 'opaque', 'csimp', 'macro', 'notation', 'elab', 'syntax',
                                               'ofReduceBool', 'reduceBool')}
    print(os.path.basename(s), 'BAD' if bad else 'clean', bad if bad else '',
          {k: len(v) for k, v in h.items() if k in ('instance', 'attribute', 'local', 'variable', 'include')})
