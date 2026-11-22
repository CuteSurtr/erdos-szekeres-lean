# gen_arcdata.py: regenerate src/Geo7/ArcData.lean from ENCBLEAN's ArcBridge.lean (mechanical renames only).
import hashlib, sys
src = '/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/ENCBLEAN/geo/ES8Geo/ArcBridge.lean'
out = '/home/jay/research/data/formalize-20261122/sevenfold/src/Geo7/ArcData.lean'
s = open(src).read()
print('source sha256', hashlib.sha256(s.encode()).hexdigest())
body = 'open ErdosSzekeres ErdosSzekeres.LayerLemma' + s.split('open ErdosSzekeres ErdosSzekeres.LayerLemma', 1)[1]
rep = [('namespace EncB.Geo.Arc', 'namespace EncB.Geo7.Arc'), ('end EncB.Geo.Arc', 'end EncB.Geo7.Arc'),
       ('namespace EncB.Geo\n', 'namespace EncB.Geo7\n'), ('end EncB.Geo\n', 'end EncB.Geo7\n'),
       ('variable {m t : ℕ} {T : Finset Point} {c : Point}', 'variable {m t : ℕ} {c : Point}'),
       ('PolarLabelling m t T c', 'PolarData m t c'), ('PolarLabelling.P', 'PolarData.P'),
       ('PolarLabelling.chi', 'PolarData.chi'), ('PolarLabelling.psiLt', 'PolarData.psiLt'),
       ('{T : Finset Point} {c : Point}', '{c : Point}'), ('labelling_ruleA', 'polar_ruleA'),
       ('labelling_ruleB', 'polar_ruleB'), ('#print axioms EncB.Geo.', '#print axioms EncB.Geo7.')]
for a, b in rep:
    assert a in body, a
    body = body.replace(a, b)
assert 'PolarLabelling' not in body
hdr = open(out).read().split('open ErdosSzekeres ErdosSzekeres.LayerLemma', 1)[0]
new = hdr + body
old = open(out).read()
print('regenerated file identical to the current one:', new == old)
