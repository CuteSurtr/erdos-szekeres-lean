#!/usr/bin/env python3
"""Deterministically append the48proved supports to the frozen2598catalog."""
from pathlib import Path
import gzip,hashlib,json
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
BASE=ROOT/'experiments/omission-residual32-2598-primal-2026-10-10/source-2598.json.gz'
sha=lambda b:hashlib.sha256(b).hexdigest()
def build():
 raw=gzip.decompress(BASE.read_bytes());assert sha(raw)=='01d4fde13ae0ca43427540a3d529e7e29b875936332af2cc4ef7d423edee469b';source=json.loads(raw);rows=json.loads((HERE/'rows.json').read_text())['rows'];assert len(source['constraints'])==2598 and len(rows)==48
 source['constraints'] += [{'support':r['support'],'rhs':r['rhs']} for r in rows]
 source['research_sixth_relaxed_binding']=[{'family_row':i,'source_row':2598+i,'support':r['support'],'rhs':r['rhs'],'ordered_mapping':r['map']} for i,r in enumerate(rows)]
 return (json.dumps(source,separators=(',',':'))+'\n').encode()
if __name__=='__main__':
 raw=build();archive=gzip.compress(raw,mtime=0);(HERE/'source-2646.json.gz').write_bytes(archive)
 m={'scope':'Ordered literal row catalog; geometric validity of appended48rows is proved in SixthRelaxedProof.Root. No global32-hole exclusion.','base_reference':str(BASE.relative_to(ROOT)),'base_archive_sha256':sha(BASE.read_bytes()),'base_uncompressed_sha256':'01d4fde13ae0ca43427540a3d529e7e29b875936332af2cc4ef7d423edee469b','rows_reference':'rows.json','rows_sha256':sha((HERE/'rows.json').read_bytes()),'generator_sha256':sha(Path(__file__).read_bytes()),'source_reference':'source-2646.json.gz','source_archive_sha256':sha(archive),'source_uncompressed_sha256':sha(raw),'states':154,'prefix_rows':2598,'added_rows':48,'rows':2646}
 (HERE/'catalog-manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(json.dumps(m,indent=2))
