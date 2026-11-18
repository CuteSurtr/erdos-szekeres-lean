"""Assemble README.md of the record from the static parts in W and the result files."""
import subprocess, sys, os, json, re
W = os.path.dirname(os.path.abspath(__file__))
def run(script):
    return subprocess.run([sys.executable, os.path.join(W, script)], capture_output=True, text=True, cwd=W).stdout
tables = run('mk_tables.py').split('\n\n')
decided, restricted, thr = tables[0].strip(), tables[1].strip(), tables[2].strip()
refuted = run('mk_refuted.py').strip()
def rd(fn):
    p = os.path.join(W, fn)
    return open(p).read() if os.path.exists(p) else ''
head = rd('readme_head.md'); s23 = rd('readme_static_2_3.md'); s4 = rd('readme_static_4.md'); s5 = rd('readme_static_5.md')
s6 = rd('readme_static_6.md'); s7 = rd('readme_static_7.md'); s89 = rd('readme_static_8_9.md')
lem = ' '.join(l.strip() for l in rd('lemma_check.log').splitlines() if l.strip()) or 'not finished'
s6 = s6.replace('LEMMACHECK_PLACEHOLDER', lem)
s4 = s4.replace('DECIDED_TABLE_PLACEHOLDER', decided)
s7 = s7.replace('REFUTED_TABLE_PLACEHOLDER', refuted)
online = '\n'.join('  - ' + l.strip() for l in rd('online.log').splitlines() if l.strip().startswith('online game'))
s4 = s4.replace('ONLINE_LOG_PLACEHOLDER', online)
out = '\n'.join([head, s23, s4, s5, s6, s7, s89])
vp = os.path.join(W, 'readme_vars.json')
if os.path.exists(vp):
    for _ in range(2):
        for k, v in json.load(open(vp)).items(): out = out.replace(k + '_PLACEHOLDER', v)
open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(W, 'README.preview.md'), 'w').write(out)
print('written', len(out), 'chars')
