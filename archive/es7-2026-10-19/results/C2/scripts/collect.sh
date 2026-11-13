#!/bin/bash
# Copy C2 logs and sets from the work directory into results/C2.  usage: collect.sh <workdir> <resultsdir>
W="$1"; R="$2"
for r in i_hull ii_interior; do
  mkdir -p "$R/logs/cnc_$r"
  for f in cnc.log latest.json state.json closed.txt; do [ -f "$W/runs/$r/$f" ] && cp "$W/runs/$r/$f" "$R/logs/cnc_$r/"; done
  cp "$W"/runs/$r/model-* "$R/logs/cnc_$r/" 2>/dev/null
  [ -f "$W/runs/lrat_$r.jsonl" ] && cp "$W/runs/lrat_$r.jsonl" "$R/logs/cnc_$r/lrat_new_cubes.jsonl"
done
cp "$W/runs/lrat_inherited_i.jsonl" "$R/logs/cnc_i_hull/lrat_inherited_cubes.jsonl" 2>/dev/null
cp "$W/runs/lrat_inherited_ii.jsonl" "$R/logs/cnc_ii_interior/lrat_inherited_cubes.jsonl" 2>/dev/null
cp "$W/runs/progress_30min.jsonl" "$R/logs/cnc_progress_30min.jsonl" 2>/dev/null
mkdir -p "$R/logs/anneal" "$R/sets"
for d in m33 m32; do for f in "$W"/ann/$d/*.log "$W"/ann/$d/*.scan; do [ -f "$f" ] && cp "$f" "$R/logs/anneal/${d}_$(basename "$f")"; done; done
cat "$W"/ann/m32/*.zero > "$R/sets/heptagon_free_mirror32_found.txt" 2>/dev/null
cat "$W"/ann/m33/*.best > "$R/sets/anneal33_best_states.txt" 2>/dev/null
du -sh "$R"
