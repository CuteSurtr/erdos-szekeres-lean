#!/bin/bash
# build_self.sh: compile the vendored geometric modules (verbatim ENCBLEAN geo sources, logs/geo_vendor.sha256)
# and this package's Geo7 modules against Mathlib only (LEAN_PATH LP_SELF: no olean of ENCBLEAN's builds).
# Requires tools/build_std.sh first (EncB, EncBO oleans in olean/).
set -u
W=/home/jay/research/data/formalize-20261122/sevenfold
cd "$W/src" && sha256sum -c --quiet "$W/logs/geo_vendor.sha256" || { echo "vendored geo sources changed"; exit 1; }
cd "$W"
echo "=== build_self $(date -Is)" >> "$W/logs/build.log"
exec "$W/tools/lc.sh" self ErdosSzekeres.Definitions ErdosSzekeres.Orientation ErdosSzekeres.Basic \
  ErdosSzekeres.OrientationGeometry ErdosSzekeres.Suk.TriangleOrder ErdosSzekeres.Suk.BaseChart \
  ErdosSzekeres.Suk.BaseOrder ErdosSzekeres.Suk.FourPoint ErdosSzekeres.Suk.SupportingLines \
  ErdosSzekeres.Suk.OrientationClique ES8Geo.KeyOrder ES8Geo.Capstone2 ES8Geo.OrbitConsistency ES8Geo.Orbit \
  ES8Geo.Interface ES8Geo.Labelling Geo7.PolarData Geo7.ArcData Geo7.LayerLab Geo7.LayerBasic Geo7.Perturb \
  Geo7.ModelOfLab Geo7.Main7
