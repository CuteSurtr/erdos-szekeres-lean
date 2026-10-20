#!/usr/bin/env python3
"""Prepare results/FINAL/READY.json and the V3E work list at a commit Zf where no wave case has an open cube.

usage: make_ready.py REPO ZF OUTDIR [--skip LIST:SHARDS:N ...]

1. Runs gfrontier3.py at ZF (scratchpad copy) and requires 278 wave cases with no open cube.
2. Runs build_worklist_e.py at ZF: the acceptance manifest exactly as V3B step 2 builds it (verify/v3 at
   bdf319c), and the V3E work list (manifest records with no VERIFIED leaf record at ZF, minus the --skip
   records of running machines).
3. Writes OUTDIR/READY.json and OUTDIR/README_FINAL.md (for results/FINAL/) and leaves the V3E files in OUTDIR/e/.
"""
import argparse, hashlib, json, os, subprocess, sys
ap = argparse.ArgumentParser()
ap.add_argument('repo'); ap.add_argument('zf'); ap.add_argument('out')
ap.add_argument('--skip', action='append', default=[])
a = ap.parse_args()
a.out = os.path.abspath(a.out); a.repo = os.path.abspath(a.repo)
HERE = os.path.dirname(os.path.abspath(__file__))
C3 = os.path.dirname(HERE)
os.makedirs(a.out, exist_ok=True)
zf = subprocess.run(['git', '-C', a.repo, 'rev-parse', a.zf], capture_output=True, text=True, check=True).stdout.strip()
date = subprocess.run(['git', '-C', a.repo, 'show', '-s', '--format=%cI', zf], capture_output=True, text=True, check=True).stdout.strip()

# 1. frontier
gf = os.path.join(a.out, 'gf_final.json')
r = subprocess.run(['python3', os.path.join(C3, 'w2', 'gfrontier3.py'), zf, gf], cwd=a.repo, capture_output=True, text=True)
print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-500:])
g = json.load(open(gf))
opn = {k: len(v['open']) for k, v in g.items() if v['open']}
assert len(g) == 278, ('wave cases', len(g))
assert not opn, ('open cubes remain', opn)

# 2. manifest and V3E list
e = os.path.join(a.out, 'e')
cmd = ['python3', os.path.join(C3, 'v3e', 'build_worklist_e.py'), a.repo, zf, e]
for s in a.skip:
    cmd += ['--skip', s]
r = subprocess.run(cmd, capture_output=True, text=True)
print(r.stdout[-2500:]); print(r.stderr[-1500:])
assert r.returncode == 0
open(os.path.join(e, 'log.txt'), 'w').write(r.stdout)
M = os.path.join(e, 'M_Z.jsonl')
msha = hashlib.sha256(open(M, 'rb').read()).hexdigest()
mlines = sum(1 for _ in open(M))
cases = sum(1 for _ in open(os.path.join(e, 'C_Z.jsonl')))
ready = {
    'Zf': zf,
    'Zf_date': date,
    'manifest_sha256': msha,
    'manifest_lines': mlines,
    'manifest_cases': cases,
    'frontier': {'wave_cases': len(g), 'wave_cases_without_open_cube': len(g) - len(opn), 'open_cubes': 0,
                 'tool': 'results/WAVE4/scripts/gfrontier3.py'},
    'manifest_method': 'verify/v3 at bdf319c: v3_jsonl_leaves.py ROOT results/WAVEk jtreek for k = 1..4, then '
                       'v3_manifest.py ROOT M.jsonl C.jsonl results/WAVE1 jtree1 results/WAVE2 jtree2 '
                       'results/WAVE3 jtree3 results/WAVE4 jtree4 (as results/V3B/TASK.md step 2)',
}
json.dump(ready, open(os.path.join(a.out, 'READY.json'), 'w'), indent=1)
open(os.path.join(a.out, 'README_FINAL.md'), 'w').write(f"""# FINAL: the commit at which every wave case of mirror sub-case (ii) is closed

`READY.json` names Zf = {zf} ({date}). At Zf, `results/WAVE4/scripts/gfrontier3.py` finds no open cube in any of the {len(g)} wave cases: every top cube of every case is closed by a leaf with a cake_lpr `s VERIFIED UNSAT` record, or split (SPLIT record) into cubes that are, recursively. With the 172 cases closed directly by `results/Mii-S`, all 450 hull cases are closed by the solver runs.

The acceptance manifest at Zf, built exactly as `results/V3B/TASK.md` step 2 does it ({ready['manifest_method']}), has {mlines} lines (leaves in {cases} cases), sha256 {msha}.

This is what the waves claim; the acceptance passes check it from scratch: every leaf re-solved and proof-checked (`results/V3T`, `results/V3A` to `results/V3E`), every case cover checked and the final table built (`results/V3Z`), and the Lean instantiation (`results/V2-L`, `TREE_TASK.md`).
""")
print(json.dumps(ready, indent=1))
