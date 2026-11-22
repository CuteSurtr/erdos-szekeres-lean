# Reviewer: rebuild the gate README as it stood when data/prereg-readme.sha256 was taken (21:16:56), from the
# worker's own Write/Edit tool calls in its session transcript, and compare the sha256 with the recorded one.
import json, sys, hashlib
tr, target, cutoff = sys.argv[1], sys.argv[2], sys.argv[3]   # cutoff: ISO UTC timestamp string prefix compare
ops = []
for line in open(tr):
    try: o = json.loads(line)
    except Exception: continue
    ts = o.get('timestamp', '')
    msg = o.get('message') or {}
    cont = msg.get('content')
    if not isinstance(cont, list): continue
    for c in cont:
        if c.get('type') != 'tool_use': continue
        inp = c.get('input', {})
        name = c.get('name')
        fp = inp.get('file_path', '')
        if name in ('Write', 'Edit') and fp == target:
            ops.append((ts, name, inp))
        elif name == 'Bash' and 'README.md' in inp.get('command', '') and ('>' in inp.get('command', '') or 'sed -i' in inp.get('command', '')):
            ops.append((ts, 'Bash', inp))
txt = None
for ts, name, inp in ops:
    print(ts, name, (inp.get('command', '')[:160].replace('\n', ' ') if name == 'Bash' else ''))
for ts, name, inp in ops:
    if ts > cutoff: break
    if name == 'Write': txt = inp['content']
    elif name == 'Edit':
        old, new = inp['old_string'], inp['new_string']
        assert txt is not None and old in txt, ('edit does not apply', ts)
        txt = txt.replace(old, new) if inp.get('replace_all') else txt.replace(old, new, 1)
if txt is not None:
    h = hashlib.sha256(txt.encode()).hexdigest()
    print('rebuilt README at cutoff', cutoff, 'sha256', h, 'bytes', len(txt.encode()))
    open(sys.argv[4], 'w').write(txt)
