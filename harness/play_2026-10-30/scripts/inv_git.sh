#!/bin/bash
# r447 item 1, read only: every tether git checkout (worktree or clone) on the box -- path, branch, HEAD, remote, and
# `git --no-optional-locks status --porcelain` (no index refresh written). fresh_r30 (PLAY24's running tree) is skipped.
OUT="$1"; : > "$OUT"
cands=()
for d in /c/Users/Admin/Documents/GitHub/tether /c/Users/Admin/Documents/GitHub/tether-*; do cands+=("$d"); done
for d in /c/TETHER_RUNS/S6_2026-10-19/draft /c/TETHER_RUNS/S6_2026-10-19/wt_before /c/TETHER_RUNS/S6_2026-10-19/wt_c /c/TETHER_RUNS/S6_2026-10-19/wt_ivv; do cands+=("$d"); done
for d in /c/TETHER_RUNS/S6_2026-10-19/split/*; do
  if [ -e "$d/.git" ]; then cands+=("$d"); fi
  for s in "$d"/*; do [ -e "$s/.git" ] && cands+=("$s"); done
done
for d in "${cands[@]}"; do
  case "$d" in *split/fresh_r30*) echo "SKIP $d (PLAY24's running tree, r447)" >> "$OUT"; continue;; esac
  [ -e "$d/.git" ] || continue
  url=$(git -C "$d" remote get-url origin 2>/dev/null)
  br=$(git -C "$d" rev-parse --abbrev-ref HEAD 2>/dev/null)
  hd=$(git -C "$d" rev-parse --short HEAD 2>/dev/null)
  st=$(git -C "$d" --no-optional-locks status --porcelain --untracked-files=normal 2>/dev/null)
  n=$(printf '%s' "$st" | grep -c . )
  echo "REPO $d | branch $br | HEAD $hd | origin ${url:-(worktree of main)} | porcelain lines $n" >> "$OUT"
  [ "$n" -gt 0 ] && printf '%s\n' "$st" | sed 's/^/    /' >> "$OUT"
done
echo "DONE $(date '+%H:%M:%S')" >> "$OUT"
