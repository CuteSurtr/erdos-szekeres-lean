# Reviewer: list the worker's Write/Edit calls outside s3520-gate, and Bash commands with write-like operators that
# name a path outside s3520-gate (for manual inspection).
import json, re, sys
tr = sys.argv[1]
G = '/home/jay/research/data/formalize-20261122/s3520-gate'
wr = re.compile(r'(>>?|\bsed -i|\bcp\b|\bmv\b|\brm\b|\bln\b|\btee\b|\bmkdir\b|\btouch\b|write_text|write_bytes|open\([^)]*[\'"]w)')
n = 0
for line in open(tr):
    o = json.loads(line); ts = o.get('timestamp', '')
    c = (o.get('message') or {}).get('content')
    if not isinstance(c, list): continue
    for x in c:
        if x.get('type') != 'tool_use': continue
        inp = x.get('input', {})
        if x['name'] in ('Write', 'Edit', 'NotebookEdit'):
            fp = inp.get('file_path', '')
            if not fp.startswith(G + '/'): print(ts, x['name'], 'OUTSIDE', fp); n += 1
        elif x['name'] == 'Bash':
            cmd = inp.get('command', '')
            paths = set(re.findall(r'/home/jay/[^\s\'";|&)]+', cmd))
            outside = [p for p in paths if not p.startswith(G)]
            if wr.search(cmd) and outside:
                print('----', ts); print(cmd[:1500]); n += 1
print('flagged', n)
