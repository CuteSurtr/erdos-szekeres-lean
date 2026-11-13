"""Augment existing Baek block supports (restricted to occupied states of each 33-hole
vector) by occupied states while a two-level cap compression survives."""
import sys, json, random
sys.argv=['x','0']
exec(open('block_greedy.py').read().split('R = ROOT')[0])
R = ROOT + 'cloud/es7-2026-10-19/results/'
w = json.load(open(R + 'ES8SLACK/witnesses.json'))['residual_2650_33_hole_witnesses_state0_occupied']
t = json.load(open(R + 'ES8SLACK/review/C3_residual/template_closure_probe_out.json'))['milp']['holes']
vecs = [set(x) for x in w] + [set(t)]
blocks = [973] + list(range(1165, 1187))
rng = random.Random(7)
found = []
for vi, H in enumerate(vecs):
    occ = [i for i in range(n) if i not in H]
    best = 0
    for b in blocks:
        for coord in (0,):
            Sset = [i for i in C[b]['support'] if i not in H]
            for rep in range(3):
                X = list(Sset); cand = [i for i in occ if i not in X]; rng.shuffle(cand)
                for x in cand:
                    bad, _ = conflicts(X + [x], coord)
                    if not bad: X.append(x)
                best = max(best, len(X))
                if len(X) >= 23:
                    found.append({'vector': vi, 'block': b, 'support': sorted(X)})
                    print(f'vector {vi} block {b}: compressible occupied support of size {len(X)} -> VIOLATED BAEK ROW', flush=True)
                    break
    print(f'vector {vi}: best augmented compressible occupied support {best}', flush=True)
json.dump(found, open('block_augment_out.json', 'w'))
