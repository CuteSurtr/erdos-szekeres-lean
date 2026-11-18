"""Phase 2 memory helper (n66 track budget 9 GB, anonymous memory + swap, counted by the session guard).
others_mb(me): anonymous memory of the other nov13c-n66-* units (cgroup memory.stat), in MB.
wait_room(mb, d, me, limit=8200, maxwait=7200): wait until others + mb <= limit; while waiting write d/need_room.json
(p2_driver.py then stops a search unit).  Returns True if there is room."""
import glob, os, json, time
BASE = '/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice'
def others_mb(me):
    tot = 0
    for p in glob.glob(BASE + '/nov13c-n66-*.service'):
        if os.path.basename(p) == f'{me}.service': continue
        try:
            for line in open(p + '/memory.stat'):
                if line.startswith('anon '): tot += int(line.split()[1]) // 1048576; break
        except OSError: pass
    return tot
def wait_room(mb, d, me, limit=8200, maxwait=7200):
    t0 = time.time(); nr = os.path.join(d, 'need_room.json')
    while others_mb(me) + mb > limit and time.time() - t0 < maxwait:
        json.dump({'need_mb': mb, 'others_mb': others_mb(me), 'since': t0}, open(nr, 'w'))
        time.sleep(30)
    if os.path.exists(nr): os.remove(nr)
    return others_mb(me) + mb <= limit
