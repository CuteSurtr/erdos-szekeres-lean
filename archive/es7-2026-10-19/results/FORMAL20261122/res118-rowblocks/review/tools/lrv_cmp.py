#!/usr/bin/env python3
"""After the audit compile: (a) the rows the interpreter printed from the olean (LRV_ROWS* lines of logs/audit.log)
equal, row by row and in order, the rows the exe lists (data/exe_lists.txt, `rowprint list B`); (b) the interpreter's
`rowText` of row U 0 (data/interp_U0.cnf, written by the compile) equals the exe's bytes for `rowprint row U 0`;
(c) a summary of the axiom lines and errors of the log. COMPUTED. Writes argv[1] (JSON)."""
import hashlib, json, re, subprocess, sys

V = '/home/jay/research/data/formalize-20261122/res118-rowblocks/review'
EXE = '/home/jay/research/data/formalize-20261122/res118-rowblocks/build/bin/rowprint'
log = open(V + '/logs/audit.log').read()


def grab(tag):
    m = re.search(rf'^{tag} (.*)$', log, re.M)
    return m.group(1) if m else None


def lists(s):
    return [[int(x) for x in re.findall(r'\d+', g)] for g in re.findall(r'\[([^\[\]]*)\]', s[1:-1])]


exe = {}
for line in open(V + '/data/exe_lists.txt'):
    B, i, supp = line.split()
    exe.setdefault(B, []).append([int(x) for x in supp.split(',')])
rep = {}
for B in 'PQUA':
    s = grab(f'LRV_ROWS{B}')
    ol = lists(s) if s else None
    rep[f'olean_{B}_rows'] = len(ol) if ol is not None else None
    rep[f'olean_eq_exe_{B}'] = ol == exe[B]
rep['lengths_line'] = grab('LRV_LENGTHS')
u0 = grab('LRV_U0')
rep['U0'] = u0
try:
    interp = open(V + '/data/interp_U0.cnf', 'rb').read()
    exe_u0 = subprocess.run([EXE, 'row', 'U', '0'], capture_output=True, check=True).stdout
    rep['interp_U0_sha'] = hashlib.sha256(interp).hexdigest()
    rep['exe_U0_sha'] = hashlib.sha256(exe_u0).hexdigest()
    rep['interp_U0_bytes'] = len(interp)
    rep['interp_eq_exe_U0'] = interp == exe_u0
except OSError as e:
    rep['interp_U0'] = repr(e)
    rep['interp_eq_exe_U0'] = False
ax = re.findall(r"^'([^']+)' (depends on axioms: \[([^\]]*)\]|does not depend on any axioms)", log, re.M)
rep['axiom_lines'] = len(ax)
std = {'propext', 'Classical.choice', 'Quot.sound'}
rep['nonstandard'] = [(n, a) for n, _, a in ax if a and not set(x.strip() for x in a.split(',')) <= std]
rep['axioms'] = {n: (a if a else 'none') for n, _, a in ax}
rep['errors'] = re.findall(r'^.*error.*$', log, re.M)[:40]
rep['end_marker'] = 'LRV_END' in log
rep['ok'] = (all(rep[f'olean_eq_exe_{B}'] for B in 'PQUA') and rep.get('interp_eq_exe_U0') is True
             and not rep['nonstandard'] and not rep['errors'] and rep['end_marker'])
json.dump(rep, open(sys.argv[1], 'w'), indent=1)
print(json.dumps({k: v for k, v in rep.items() if k != 'axioms'}, indent=1))
