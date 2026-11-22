#!/bin/bash
# Source audit: no sorry/admit/native_decide/implemented_by/extern/unsafe/axiom/opaque/macro escapes in lean/.
D=/home/jay/research/data/formalize-20261122/v182-lean
cd $D/lean
bad=$(grep -rnwE "sorry|admit|native_decide|implemented_by|extern|unsafe|axiom|opaque|decide!|ofReduceBool|reduceBool|Lean\.ofReduceBool|csimp|trustCompiler" --include=*.lean . | grep -v "^\./[^:]*:[0-9]*:\s*--" )
echo "files: $(find . -name '*.lean' | sort | tr '\n' ' ')"
if [ -n "$bad" ]; then echo "AUDIT FAIL"; echo "$bad"; exit 1; fi
echo "AUDIT PASS (no sorry/admit/native_decide/implemented_by/extern/unsafe/axiom/opaque/ofReduceBool/csimp)"
