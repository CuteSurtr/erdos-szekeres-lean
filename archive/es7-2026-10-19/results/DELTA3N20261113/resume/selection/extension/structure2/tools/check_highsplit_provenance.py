"""Replay conditional-lift invariants directly, without importing its generator."""
from itertools import combinations
import argparse
import hashlib
import json
from pathlib import Path
import time
from verify_structure2 import signs_of, maxgon, four_caps


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();assert not args.out.exists();start=time.monotonic()
    root=Path(__file__).resolve().parents[1]
    source=root/'data/highsplit_cases.json';all_cases=json.loads(source.read_text())['cases']
    results={};sources={str(source):hashlib.sha256(source.read_bytes()).hexdigest()}
    for name,r in all_cases.items():
        if r['case']!='iii':continue
        p=r['P'];cut=r['cut'];assert cut==len(p)-1
        s=signs_of(p);old=list(range(cut));full=old+[cut]
        c4=four_caps(s,full);c4_old=four_caps(s,old)
        assert c4==c4_old and all(s[a,b,cut]>0 for a,b in combinations(old,2))
        ends={t[-2:] for t in c4}
        for entry in r['selected']:
            A=entry['A'];assert cut in A;B=[v for v in A if v!=cut]
            assert not any(set(A).issuperset(t) for t in c4)
            triples=[t for t in combinations(A,3) if s[t]<0]
            old_triples=[t for t in combinations(B,3) if s[t]<0]
            assert triples==old_triples and all(t[-2:] in ends for t in triples)
            assert maxgon(s,[v for v in old if v not in B])<r['n']-1
            assert maxgon(s,[v for v in full if v not in A])<r['n']-1
        results[name]=dict(status='PASS',m=len(p),right_point=p[-1],
            old_fourcap_count=len(c4_old),all_fourcaps_unchanged=True,
            every_new_triple_is_cup=True,left_maxgon=maxgon(s,old),
            full_maxgon=maxgon(s,full),conditional_selections_checked=len(r['selected']))
    witness=root.parents[1]/'terminal/data/witness.json'
    wp=json.loads(witness.read_text())['P']
    neg=all_cases['terminal18_plus_high_singleton']
    assert neg['P'][:-1]==wp
    sources[str(witness)]=hashlib.sha256(witness.read_bytes()).hexdigest()
    positive_source=root/'data/separator_c3.json';pr=json.loads(positive_source.read_text())
    positive=all_cases['n7_case_iii_terminal_caps']
    assert positive['P'][:-1]==pr['P'] and positive['selected'][0]['A']==pr['A']+[len(pr['P'])]
    sources[str(positive_source)]=hashlib.sha256(positive_source.read_bytes()).hexdigest()
    # This verifies the reduction's invariants, not a fresh terminal18 proof.
    output=dict(status='PASS',scope='Exact conditional-extension and source-identity replay; terminal18 nonexistence uses the earlier audited certificate.',
        critical_cases=results,inputs=sources,elapsed_seconds=time.monotonic()-start,
        source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        helper_sha256=hashlib.sha256(Path(__file__).with_name('verify_structure2.py').read_bytes()).hexdigest())
    args.out.write_text(json.dumps(output,indent=2)+'\n');print(json.dumps(output))


if __name__=='__main__':main()
