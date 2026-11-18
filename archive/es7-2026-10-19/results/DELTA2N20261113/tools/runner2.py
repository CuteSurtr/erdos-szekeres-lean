"""Sequential queue runner (one process at a time).  Takes the first line of queue.txt, runs it, repeats; exits when empty."""
import subprocess, time, os, sys
Q = sys.argv[1] if len(sys.argv) > 1 else 'queue.txt'
while True:
    lines = [l for l in open(Q).read().splitlines() if l.strip()]
    if not lines: break
    cmd = lines[0]
    with open(Q + '.tmp', 'w') as f: f.write('\n'.join(lines[1:]) + ('\n' if len(lines) > 1 else ''))
    os.replace(Q + '.tmp', Q)
    t = time.time()
    with open(Q + '.log', 'a') as f: f.write('%s START %s\n' % (time.strftime('%H:%M:%S'), cmd))
    r = subprocess.run(cmd, shell=True)
    with open(Q + '.log', 'a') as f: f.write('%s END rc=%d %.0fs %s\n' % (time.strftime('%H:%M:%S'), r.returncode, time.time() - t, cmd))
