"""Mock test of p2_driver.step(): level-12 UNSAT by a batch slot, certificate, level-13 opening, memory rule."""
import sys, os, json, shutil, importlib.util, datetime
T = '/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/47493978-8997-4f78-83c2-501528c83121/scratchpad/drvtest'
shutil.rmtree(T, ignore_errors=True); os.makedirs(T + '/p2/s12'); os.makedirs(T + '/p2/b12e/it3')
spec = importlib.util.spec_from_file_location('drv', '/home/jay/research/data/n66-20261113/p2_driver.py')
d = importlib.util.module_from_spec(spec); spec.loader.exec_module(d)
os.chdir(T)
d.W = T; d.CERTJ = T + '/n66_certified.json'; d.README = T + '/README.md'; d.STATEF = T + '/p2/driver_state.json'; d.LOGF = T + '/p2/driver.log'
open(d.README, 'w').write('<!-- STATUS -->\nold\n<!-- /STATUS -->\n## 9.\n')
ACTIVE = {'s12a', 's12c', 's12e'}; LAUNCHED = []; MEM = [5000]
d.active = lambda u: u in ACTIVE
d.my_units = lambda: ['nov13c-n66-' + u + '.service' for u in sorted(ACTIVE)]
d.threads_used = lambda: float(len(ACTIVE))
d.anon_mb = lambda: MEM[0]
d.cpu_free = lambda: 8
def fake_launch(u, cmd, mem, est, quota=100, quiet=False):
    if d.threads_used() + 1 > d.MAXT: return False
    LAUNCHED.append((u, cmd)); ACTIVE.add(u); return True
d.launch = fake_launch
def fake_stop(u): ACTIVE.discard(u); d.log(f'stopped {u}')
d.stop = fake_stop
d.now = lambda: datetime.datetime(2026, 11, 14, 1, 0, 0)
d.cfg = lambda: {'slot_order': ['e', 'c', 'g', 'a', 'd', 'b'], 'next_level_slots': ['e', 'c', 'g']}
S = {'levels': {'12': {'status': 'running', 'slots': {
        'a': {'warm': 'w', 'seed': 1, 'tauclose': False, 'k': 0, 'type': 'lazy', 'launched': True, 'unit': 's12a'},
        'c': {'warm': 'w', 'seed': 3, 'tauclose': True, 'k': 0, 'type': 'batch', 'launched': True, 'unit': 's12c'},
        'e': {'warm': 'w', 'seed': 5, 'tauclose': True, 'k': 0, 'type': 'batch', 'sb': True, 'launched': True, 'unit': 's12e'}}}}}
S['certified'] = {'11': {'bound': 58, 'holes_at_least': 12, 'label': 'CERTIFIED', 'time': 't', 'cnf_sha256': 'x', 'lrat_sha256': 'y', 'what': 'w'}}
# 1. nothing happened yet: no launches expected (all slots active or parked)
d.step(S); assert LAUNCHED == [], LAUNCHED
# 2. batch slot e reports UNSAT with a certdir
json.dump({'activated': [], 'certdir': 'p2/b12e/it3', 'L': 12}, open('p2/s12/e_L12.json', 'w'))
d.step(S)
lv = S['levels']['12']; print('after UNSAT:', lv['status'], lv.get('certdir'), lv.get('winner_unit'), sorted(ACTIVE))
assert lv['status'] == 'UNSAT' and lv['winner_unit'] == 's12e' and ACTIVE == {'s12e'}, ACTIVE
assert '13' in S['levels'] and list(S['levels']['13']['slots']) == ['e', 'c', 'g']
# 3. next step: level 13 slots launch while the winner certifies (cert_active true -> only 'a' unless memory allows)
MEM[0] = 6000
d.step(S); print('launched:', [u for u, _ in LAUNCHED])
assert [u for u, _ in LAUNCHED] == [], LAUNCHED   # cert active: non-'a' slots wait (memory reserve)
# 4. the certificate step needs room -> a level-13 search unit is stopped (not the winner)
json.dump({'need_mb': 3000}, open('p2/b12e/it3/need_room.json', 'w'))
d.step(S); print('after need_room:', sorted(ACTIVE))
assert 's12e' in ACTIVE
os.remove('p2/b12e/it3/need_room.json')
# 5. certificate finished
json.dump({'ALL_OK': True, 'W_size': 70, 'cube': [], 'bound': 57, 'holes_at_least': 13, 'time': 'tt', 'trim_cnf_sha256': 'aa', 'trim_lrat_sha256': 'bb',
           'certdir': T + '/p2/b12e/it3', 'trim_cnf_clauses': 10, 'kinds': {}, 'final_verify66': {'kinds': {}}, 'full_cnf_sha256': 'cc',
           'trim_lrat_bytes': 1, 'used': {'used_rows': 3}}, open('p2/b12e/it3/cert.json', 'w'))
ACTIVE.discard('s12e'); MEM[0] = 3000
d.step(S); CUR_T=[0]
for _ in range(3):
    d.CUR["last_search_launch"]=0; d.step(S)
print('certified file bound:', json.load(open(d.CERTJ))['bound'], 'launched:', [u for u, _ in LAUNCHED], 'active:', sorted(ACTIVE))
assert json.load(open(d.CERTJ))['bound'] == 57
assert 's13e' in ACTIVE and 's13c' in ACTIVE and 's13g' in ACTIVE, ACTIVE
print(open(d.README).read()[-600:])
print(open(d.LOGF).read()[-900:])
S['levels']['13']['status'] = 'UNSAT'; S['levels']['13']['state'] = 'x'; S['levels']['13']['certdir'] = 'p2/b13g/it1'; S['levels']['13']['cert_launched'] = True
os.makedirs('p2/b13g/it1', exist_ok=True)
json.dump({'ALL_OK': True, 'W_size': 70, 'cube': [], 'bound': 56, 'holes_at_least': 14, 'time': 't3', 'trim_cnf_sha256': 'a3', 'trim_lrat_sha256': 'b3',
           'certdir': 'p2/b13g/it1', 'trim_cnf_clauses': 1, 'kinds': {}, 'final_verify66': None, 'full_cnf_sha256': 'c3', 'trim_lrat_bytes': 1, 'used': {'used_rows': 0}}, open('p2/b13g/it1/cert.json', 'w'))
d.step(S)
txt = open(d.README).read(); print(txt[:300])
assert 'N66 ≤ 56 CERTIFIED' in txt.split('<!-- /STATUS -->')[0] and json.load(open(d.CERTJ))['bound'] == 56
print('DRIVER MOCK TEST OK')
