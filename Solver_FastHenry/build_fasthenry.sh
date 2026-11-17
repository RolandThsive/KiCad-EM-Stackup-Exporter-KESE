#!/usr/bin/env bash
# Build FastHenry 3.0.1 from source into Solver_FastHenry/install/bin, as the committed binary was built:
# FastFieldSolvers' Linux/Unix release (github.com/ediloren/FastHenry2, branch master, commit 363e43e), its x64
# configuration, compiled with -O3 and -fcommon (GCC 10 and newer need -fcommon for its shared globals).
# Needs git, make and a C compiler; about ten seconds. SRC=... keeps the source where you say (default: a temporary
# folder, removed afterwards).
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
COMMIT=363e43e
REPO=https://github.com/ediloren/FastHenry2.git
SRC="${SRC:-}"
if [ -z "$SRC" ]; then
  SRC="$(mktemp -d)"
  trap 'rm -rf "$SRC"' EXIT
fi
if [ ! -d "$SRC/.git" ]; then
  git clone -q "$REPO" "$SRC"
fi
cd "$SRC"
git checkout -q "$COMMIT"
bash config x64
make fasthenry CFLAGS="-O3 -DFOUR -m64 -fcommon" > build.log 2>&1 || { tail -30 build.log; exit 1; }
mkdir -p "$HERE/install/bin"
cp bin/fasthenry "$HERE/install/bin/fasthenry"
"$HERE/install/bin/fasthenry" -h 2>&1 | grep -i 'version' || true
echo "installed $HERE/install/bin/fasthenry"
