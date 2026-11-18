"""verify_nosplit.py on many records of a jsonl (pure Python: signotope axioms, class, all partitions)."""
import sys, json, subprocess, os, tempfile
ok = tot = 0
for line in open(sys.argv[1]):
    d = json.loads(line); tot += 1
    fd, fn = tempfile.mkstemp(suffix='.json', dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tmp')); os.close(fd)
    json.dump({'a': d['a'], 'b': d['b'], 'n': d['n'], 'sig': d['sig']}, open(fn, 'w'))
    r = subprocess.run([sys.executable, 'verify_nosplit.py', fn], capture_output=True, text=True); os.remove(fn)
    ok += ('valid strong splits: 0' in r.stdout and 'valid FL(' in r.stdout)
print(f'{ok} of {tot} abstract counterexamples re-verified by the pure-Python brute force (valid configuration, 0 splits)')
