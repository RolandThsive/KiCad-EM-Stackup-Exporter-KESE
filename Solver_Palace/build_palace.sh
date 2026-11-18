#!/usr/bin/env bash
# Build Palace v0.19.0 from source into Solver_Palace/install, as the committed program was built: AWS Labs' release
# (github.com/awslabs/palace, tag v0.19.0, commit ca9a6a2), with no_parmetis.patch applied so that nothing in it is
# ParMETIS (whose licence forbids redistribution and limits use to non-profit research), with the AMS iterative
# solver (hypre) and no sparse direct solver, in double precision, without OpenMP or a GPU. WITH_MUMPS=1 adds MUMPS,
# ordered by METIS (the patch builds it without ParMETIS), but that was not tried: MUMPS's source is downloaded from
# mumps-solver.org, which the test machine's network refused.
#
# Needs: git, CMake 3.27 or newer, GCC with gfortran, Open MPI, OpenBLAS, zlib and patchelf. On Ubuntu 24.04:
#   sudo apt install git cmake build-essential gfortran openmpi-bin libopenmpi-dev libopenblas-dev zlib1g-dev \
#                    pkg-config patchelf
# About an hour on four cores and 3 GB of disk while it builds.
#
#   bash Solver_Palace/build_palace.sh                  # from the branch's root
#   JOBS=8 WORK=/data/palace bash Solver_Palace/build_palace.sh
#   LOCAL_PATCHES=1 bash Solver_Palace/build_palace.sh  # where github.com's commit and compare links are refused
#
# WORK keeps the source and the build where you say (default: a temporary folder, removed afterwards). Palace's build
# downloads a few patches for MFEM and hypre from github.com's commit and compare links; where a network refuses
# those (the test machine's did), LOCAL_PATCHES=1 makes the same diffs with git from the upstream repositories instead.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TAG=v0.19.0
COMMIT=ca9a6a2d1e64a410229c3d7538507e5eae975cc6
REPO=https://github.com/awslabs/palace.git
JOBS="${JOBS:-$(nproc)}"
WORK="${WORK:-}"
if [ -z "$WORK" ]; then
  WORK="$(mktemp -d)"
  trap 'rm -rf "$WORK"' EXIT
fi
SRC="$WORK/palace"
mkdir -p "$WORK"

if [ ! -d "$SRC/.git" ]; then
  git clone -q --branch "$TAG" --depth 1 "$REPO" "$SRC"
fi
[ "$(git -C "$SRC" rev-parse HEAD)" = "$COMMIT" ] || { echo "Palace $TAG is not commit $COMMIT"; exit 1; }
git -C "$SRC" checkout -q -- .
git -C "$SRC" apply "$HERE/no_parmetis.patch"

EXTRA=()
if [ "${LOCAL_PATCHES:-0}" = 1 ]; then
  # The diffs Palace would download, made with git from MFEM's and hypre's repositories and stored under the
  # SHA-256 Palace expects (git formats a diff's headers a little differently from github.com, so the files are the
  # same changes but not the same bytes), and a download_patch that takes them from there.
  CACHE="$WORK/patch-cache"
  mkdir -p "$CACHE" "$WORK/repos" "$WORK/archives"
  [ -d "$WORK/repos/mfem" ] || git clone -q --filter=blob:none https://github.com/mfem/mfem.git "$WORK/repos/mfem"
  [ -d "$WORK/repos/hypre" ] || git clone -q --filter=blob:none https://github.com/hypre-space/hypre.git "$WORK/repos/hypre"
  python3 - "$SRC" "$WORK/repos" "$CACHE" <<'PY'
import re, subprocess, sys
src, repos, cache = sys.argv[1:]
for dep in ('MFEM', 'HYPRE'):
    s = open(f'{src}/cmake/External{dep}.cmake').read()
    repo = f'{repos}/{dep.lower()}'
    for m in re.finditer(r'download_patch\(\s*\S+\s+"[^"]+"\s+(\S+)\s+"([^"]+)"\s+(\w+)\s*\)', s):
        name, url, sha = m.groups()
        if 'raw.githubusercontent.com' in url:
            continue                      # served from raw.githubusercontent.com, which Palace fetches itself
        if '/compare/' in url:
            a, b = re.search(r'compare/(\w+)\.\.\.(\w+)\.diff', url).groups()
            cmd = ['git', '-C', repo, 'diff', f'{a}...{b}']
        elif '.patch' in url:             # a commit's .patch?full_index=1
            c = re.search(r'commit/(\w+)\.patch', url).group(1)
            cmd = ['git', '-C', repo, 'format-patch', '-1', '--full-index', '--stdout', c]
        else:
            c = re.search(r'commit/(\w+)\.diff', url).group(1)
            cmd = ['git', '-C', repo, 'diff', f'{c}^', c]
        open(f'{cache}/{sha}', 'wb').write(subprocess.run(cmd, capture_output=True, check=True).stdout)
        print('patch', name)
PY
  python3 - "$SRC/cmake/PatchHelpers.cmake" "$CACHE" <<'PY'
import sys
path, cache = sys.argv[1:]
s = open(path).read()
hook = ('  set(PATCH_FILE "${PATCH_DIR}/${FILENAME}")\n')
local = (hook + f'  if(EXISTS "{cache}/${{SHA256}}")\n'
         '    file(MAKE_DIRECTORY "${PATCH_DIR}")\n'
         f'    file(COPY_FILE "{cache}/${{SHA256}}" "${{PATCH_FILE}}")\n'
         '    list(APPEND ${PATCH_FILES} "${PATCH_FILE}")\n'
         '    set(${PATCH_FILES} "${${PATCH_FILES}}" PARENT_SCOPE)\n'
         '    return()\n'
         '  endif()\n')
assert s.count(hook) == 1
open(path, 'w').write(s.replace(hook, local))
PY
  # the two tag archives Palace downloads from github.com's archive links
  (cd "$WORK/archives"
   [ -f scnlib-4.0.1.zip ] || { git clone -q --depth 1 --branch v4.0.1 https://github.com/eliaskosunen/scnlib.git scnlib &&
     (cd scnlib && git archive --format=zip --prefix=scnlib-4.0.1/ -o ../scnlib-4.0.1.zip HEAD) && rm -rf scnlib; }
   [ -f json-schema-validator-2.4.1.tar.gz ] || { git clone -q --depth 1 --branch 2.4.1 https://github.com/pboettch/json-schema-validator.git jsv &&
     (cd jsv && git archive --format=tar.gz --prefix=json-schema-validator-2.4.1/ -o ../json-schema-validator-2.4.1.tar.gz HEAD) && rm -rf jsv; })
  EXTRA=(-DEXTERN_SCN_URL="$WORK/archives/scnlib-4.0.1.zip"
         -DEXTERN_JSON_SCHEMA_VALIDATOR_URL="$WORK/archives/json-schema-validator-2.4.1.tar.gz")
fi

cmake -S "$SRC" -B "$WORK/build" -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="$WORK/install" \
  -DPALACE_WITH_MUMPS="$([ "${WITH_MUMPS:-0}" = 1 ] && echo ON || echo OFF)" -DPALACE_WITH_SUPERLU=OFF \
  -DPALACE_WITH_STRUMPACK=OFF -DPALACE_WITH_SLEPC=OFF \
  -DPALACE_WITH_ARPACK=ON -DPALACE_WITH_GSLIB=ON -DPALACE_WITH_OPENMP=OFF -DPALACE_WITH_LIBXSMM=OFF \
  -DPALACE_WITH_MAGMA=OFF -DPALACE_WITH_SUNDIALS=OFF "${EXTRA[@]}"
cmake --build "$WORK/build" -j "$JOBS"

BIN="$WORK/install/bin/palace-$(uname -m).bin"
if nm "$BIN" 2>/dev/null | grep -qi 'ParMETIS_V3'; then
  echo "ParMETIS found in $BIN: not installing it"; exit 1
fi
mkdir -p "$HERE/install/bin" "$HERE/install/lib"
cp "$WORK/install/bin/palace" "$BIN" "$HERE/install/bin/"
cp "$WORK/install/lib/libceed.so" "$HERE/install/lib/"
# find libceed beside the program wherever the folder is, and Open MPI where Debian and Ubuntu put it
patchelf --set-rpath '$ORIGIN/../lib:/usr/lib/x86_64-linux-gnu/openmpi/lib' "$HERE/install/bin/$(basename "$BIN")"
"$HERE/install/bin/palace" --version
echo "installed $HERE/install/bin/palace"
