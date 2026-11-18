"""Only the ten prior a4 real controls, their reflections, and fixed examples."""
import argparse
import hashlib
import json
from pathlib import Path
import time
import traceback
from low_left_probe import analyze


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();assert not args.out.exists();root=Path(__file__).resolve().parents[1]
    start=time.monotonic();r=dict(fixtures={},inputs={})
    try:
        control_path=root.parents[3]/'a4/controls.json'
        controls=json.loads(control_path.read_text())
        r['inputs'][str(control_path)]=hashlib.sha256(control_path.read_bytes()).hexdigest()
        fixtures={}
        for relative in controls['input_sha256']:
            if not relative.startswith('cex/'):continue
            path=root.parents[4]/'DELTA2N20261113/data'/relative
            obj=json.loads(path.read_text());assert obj.get('realized') and 'P' in obj
            r['inputs'][str(path)]=hashlib.sha256(path.read_bytes()).hexdigest()
            fixtures[path.stem]=(obj['P'],obj['n'])
        fixtures['old_seven_point_trimming']=(controls['trimming_obstruction']['points'],5)
        for name,(p,n) in fixtures.items():
            for reflected in (False,True):
                coords=[[-x,y] for x,y in reversed(p)] if reflected else p
                key=name+('_reflected' if reflected else '')
                result=analyze(coords,n)
                r['fixtures'][key]=result or dict(status='OUTSIDE_REMAINING_BRANCH',n=n,m=len(coords))
                if result:
                    print(json.dumps(dict(name=key,n=n,m=len(coords),kindI=result['kindI_count'],kindII=result['kindII_count'],
                        kindII_witness=result['kindII_witness'],neither_level_hits=result['neither_level_hits'])),flush=True)
        r['status']='PASS'
    except Exception:r.update(status='FAIL',traceback=traceback.format_exc());raise
    finally:
        r['elapsed_seconds']=time.monotonic()-start
        r['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        r['finder_sha256']=hashlib.sha256(Path(__file__).with_name('low_left_probe.py').read_bytes()).hexdigest()
        args.out.write_text(json.dumps(r,indent=2)+'\n')
        print(json.dumps({k:v for k,v in r.items() if k not in ('fixtures','inputs')}))


if __name__=='__main__':main()
