"""Nonvacuous End3-root controls with an (n-1)-cup present."""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time
import traceback
from rooted_controls import check


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args(); assert not args.out.exists()
    started = time.monotonic(); result = {}
    try:
        cases = {}
        for n in (5, 6, 7, 8):
            k = n-1
            # A k-cup, plus a strict interior point above the chord from
            # its second vertex to its rightmost vertex. Multiples of4
            # for base heights and the extra height4k-1 ensure GP here.
            p = sorted([(4*i, 4*i*i) for i in range(k)] + [(6, 4*k-1)])
            r = check(p, n)
            assert r['admissible'] and r['maxima']['cup'] == k
            assert r['branch'] == 'root_End3'
            cases[f'n{n}_longcup_End3_root'] = r
        result = dict(status='PASS', cases=cases)
    except BaseException:
        result.update(status='FAIL', traceback=traceback.format_exc()); raise
    finally:
        result['elapsed_seconds'] = time.monotonic()-started
        result['peak_rss_kib'] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        result['source_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        helper = Path(__file__).with_name('rooted_controls.py')
        result['helper_sha256'] = hashlib.sha256(helper.read_bytes()).hexdigest()
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open('x') as f:
            json.dump(result, f, indent=2); f.write('\n')
        print(json.dumps({k: v for k, v in result.items() if k != 'cases'}))


if __name__ == '__main__':
    main()
