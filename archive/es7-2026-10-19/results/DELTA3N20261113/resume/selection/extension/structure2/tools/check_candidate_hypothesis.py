"""Check the common-representative hypothesis using the independent DP."""
import hashlib
import json
from pathlib import Path
import sys
from verify_structure2 import signs_of, ranks_by_subsets, maxgon

root=Path(__file__).resolve().parents[1]
out=Path(sys.argv[1]);assert not out.exists()
p=json.loads((root/'data/initial_profiles.json').read_text())['fixtures']['terminal18']['P']
signs=signs_of(p);idx=list(range(len(p)));beta=ranks_by_subsets(signs,idx)
L5={i for i in idx if beta[i]==5};region=L5|{10}
without_top=maxgon(signs,[i for i in idx if i not in L5])
without_region=maxgon(signs,[i for i in idx if i not in region])
assert without_top==6 and without_region==5 and beta[10]==4
result=dict(status='PASS',L5=sorted(L5),p=10,p_rank=beta[10],
            complement_L5_maxgon=without_top,complement_region_maxgon=without_region,
            conclusion='Every hexagon missed by L5 contains p=10, and such hexagons exist.',
            helper_sha256=hashlib.sha256((root/'tools/verify_structure2.py').read_bytes()).hexdigest(),
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
