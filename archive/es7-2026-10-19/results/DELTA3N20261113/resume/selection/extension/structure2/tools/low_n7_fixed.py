"""One of four predesignated old a4n7 left blocks; one short job each."""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import time
import traceback
from low_left_probe import analyze


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--line',type=int,choices=range(1,5),required=True)
    ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();assert not args.out.exists()
    source=Path('/home/jay/research/data/etvthy-20261113/pool_a4n7.jsonl')
    start=time.monotonic();out={}
    try:
        lines=source.read_text().splitlines();obj=json.loads(lines[args.line-1])
        out['source_row']=obj;out['source_line']=args.line
        result=analyze(sorted(obj['P']),7)
        out['result']=result or dict(status='OUTSIDE_REMAINING_BRANCH')
        out['status']='PASS'
        if result:print(json.dumps({k:v for k,v in result.items() if k not in ('cap_triples','targets')}),flush=True)
    except Exception:out.update(status='FAIL',traceback=traceback.format_exc());raise
    finally:
        out['elapsed_seconds']=time.monotonic()-start
        out['peak_rss_kib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        out['input_path']=str(source);out['input_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
        out['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        out['finder_sha256']=hashlib.sha256(Path(__file__).with_name('low_left_probe.py').read_bytes()).hexdigest()
        args.out.write_text(json.dumps(out,indent=2)+'\n')
        print(json.dumps({k:v for k,v in out.items() if k not in ('result','source_row')}))


if __name__=='__main__':main()
