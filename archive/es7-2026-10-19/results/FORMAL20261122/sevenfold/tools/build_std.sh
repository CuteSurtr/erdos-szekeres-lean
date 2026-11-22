#!/bin/bash
# build_std.sh: compile the vendored EncB modules (verbatim ENCBLEAN sources, hashes in logs/encb_vendor.sha256)
# and this package's EncBO modules, in dependency order, into olean/ (Std-only; no olean from outside is used).
set -u
W=/home/jay/research/data/formalize-20261122/sevenfold
cd "$W" && sha256sum -c --quiet logs/encb_vendor.sha256 || { echo "vendored EncB sources changed"; exit 1; }
exec "$W/tools/lc.sh" std EncB.Gen EncB.Dimacs EncB.Coded EncB.Cover EncB.Model EncB.ModelLemmas EncB.SortLemmas \
  EncB.SoundOlit EncB.SoundOrbit EncB.SoundChain EncB.SoundAng EncB.SoundRules EncB.SoundWord EncB.Satisfiable \
  EncB.Render EncB.Compose EncBO.ModelO EncBO.SoundO EncBO.RulesO EncBO.AngO EncBO.SatisfiableO EncBO.Compose7
