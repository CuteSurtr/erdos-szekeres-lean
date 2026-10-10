#!/usr/bin/env python3
"""Two negative controls without editing any frozen input."""
import copy,json,unittest,gzip
import check
class Controls(unittest.TestCase):
 def test_missing_contradiction_rejected(self):
  core=json.loads((check.HERE/'augmented.json').read_text());cnf=(check.HERE/'augmented.cnf').read_text();proof=(check.HERE/'augmented.lrat').read_text().splitlines();last=int(proof[-1].split()[0]);proof[-1]=f'{last} 0 0'
  with self.assertRaisesRegex(ValueError,'no contradiction'):check.check_rup(core,cnf,'\n'.join(proof)+'\n')
 def test_repeated_owner_rejected(self):
  core=json.loads((check.HERE/'augmented.json').read_text());rows=json.loads((check.HERE/'rows.json').read_text())['rows'];source=json.loads(gzip.decompress((check.ROOT/'experiments/omission-residual32-2598-primal-2026-10-10/source-2598.json.gz').read_bytes()));bad=copy.deepcopy(rows);bad[0]['map'][1]=bad[0]['map'][0]
  with self.assertRaisesRegex(ValueError,'Injective map'):check.check_rows(core,bad,source)
if __name__=='__main__':unittest.main()
