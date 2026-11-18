"""Phase 2: run cake_lpr on <dir>/trim.cnf, <dir>/trim.lrat with a heap that fits the n66 memory budget.
cake_lpr keeps its heap resident, so the heap is the memory it takes.  Tiers 2000, 3200, 4500, 5500 MB; before each
attempt p2_mem.wait_room checks that (other n66 units + heap + 300 MB) <= 8200 MB, waiting up to 2 h (writing
need_room.json, which makes p2_driver.py stop a search unit).  A tier is skipped after "heap space exhausted".
Output: <dir>/cake.out (stdout of the last attempt), <dir>/cake.err, <dir>/cake_attempts.json.
usage: p2_cake.py <dir> <own unit name>"""
import sys, os, json, subprocess, time
import p2_mem
d, me = sys.argv[1], sys.argv[2]
CAKE = os.path.expanduser('~/.local/bin/cake_lpr')
att = []
for heap in (2000, 3200, 4500, 5500):
    if not p2_mem.wait_room(heap + 300, d, me):
        att.append({'heap': heap, 'result': 'no room in the n66 memory budget after 2 h'}); continue
    t = time.time()
    r = subprocess.run(['/usr/bin/time', '-v', CAKE, f'--CML_HEAP_SIZE={heap}', '--CML_STACK_SIZE=1024', os.path.join(d, 'trim.cnf'), os.path.join(d, 'trim.lrat')],
                       capture_output=True, text=True)
    open(os.path.join(d, 'cake.out'), 'w').write(r.stdout); open(os.path.join(d, 'cake.err'), 'w').write(r.stderr)
    ok = 's VERIFIED UNSAT' in r.stdout.splitlines()
    rss = [l.split(':')[-1].strip() for l in r.stderr.splitlines() if 'Maximum resident' in l]
    att.append({'heap': heap, 'verified': ok, 'seconds': round(time.time() - t, 1), 'max_rss_kb': rss[0] if rss else None, 'tail': (r.stdout + r.stderr)[-200:] if not ok else ''})
    json.dump(att, open(os.path.join(d, 'cake_attempts.json'), 'w'), indent=1)
    if ok: break
    if 'heap space exhausted' not in (r.stdout + r.stderr): break     # a real verification failure: do not retry
json.dump(att, open(os.path.join(d, 'cake_attempts.json'), 'w'), indent=1)
print(json.dumps(att))
