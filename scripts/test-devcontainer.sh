#!/usr/bin/env bash
# Build the hardened devcontainer exactly as dunnlab-devcontainer scaffolds it,
# and run the skill's own validation table against the image.
#
# The three files are extracted from SKILL.md rather than kept as a separate
# copy, so this always tests what the skill actually ships. Requires Docker.
#
#     ./scripts/test-devcontainer.sh [workdir]

set -uo pipefail
cd "$(dirname "$0")/.."
REPO=$(pwd)
WORK="${1:-$(mktemp -d)}"
IMAGE=dunnlab-devcontainer-test

command -v docker >/dev/null 2>&1 || { echo "docker not found"; exit 1; }

mkdir -p "$WORK/.devcontainer"
python3 - "$REPO" "$WORK" <<'PY'
import re, sys, pathlib
repo, work = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
out = work / '.devcontainer'
t = (repo / 'skills/dunnlab-devcontainer/SKILL.md').read_text()

def block(heading, lang):
    i = t.index(heading)
    m = re.search(r'```' + lang + r'\n(.*?)\n```', t[i:], re.S)
    if not m:
        sys.exit(f"could not extract {lang} block after {heading!r}")
    return m.group(1) + '\n'

(out / 'devcontainer.json').write_text(block('#### 1. `.devcontainer/devcontainer.json`', 'json'))
(out / 'Dockerfile').write_text(block('#### 2. `.devcontainer/Dockerfile`', 'dockerfile'))
(out / 'init-firewall.sh').write_text(block('##### Locked-down variant (default)', 'bash'))
PY
[ $? -eq 0 ] || exit 1

pass=0; fail=0
ok()  { printf '  \033[32m✓\033[0m %-26s %s\n' "$1" "${2:-}"; pass=$((pass+1)); }
bad() { printf '  \033[31m✗\033[0m %-26s %s\n' "$1" "${2:-}"; fail=$((fail+1)); }

echo "Pre-build checks"
python3 -c "import json;json.load(open('$WORK/.devcontainer/devcontainer.json'))" 2>/dev/null \
  && ok "devcontainer.json valid" || bad "devcontainer.json invalid JSON"

# The skill warns that awk's $4/$5 must survive being written to disk. If a
# tool interpolates them away, the firewall silently resolves no addresses
# and the default-deny policy blocks everything.
grep -q 'awk .\$4 == "A" {print \$5}' "$WORK/.devcontainer/init-firewall.sh" \
  && ok "awk \$4/\$5 preserved" || bad "awk variables were stripped"

echo "Building image"
if docker build -t "$IMAGE" "$WORK/.devcontainer" > "$WORK/build.log" 2>&1; then
  ok "docker build"
else
  bad "docker build"; tail -30 "$WORK/build.log"; exit 1
fi

echo "Image checks"
run() {
  local label="$1"; shift
  local expect="$1"; shift
  local out; out=$(timeout 180 docker run --rm "$IMAGE" "$@" 2>&1 | tail -1)
  if [[ "$out" == *"$expect"* ]]; then ok "$label" "$out"; else bad "$label" "got: $out"; fi
}
run "Claude Code installed" "Claude Code" claude --version
run "Node.js is v20"        "v20"         node --version
run "Git delta installed"   "delta"       delta --version
run "Conda installed"       "conda"       conda --version
run "Python available"      "Python"      python --version
run "Shell is zsh"          "/bin/zsh"    bash -c 'echo $SHELL'
run "Workspace writable"    "OK"          bash -c 'touch /workspace/t && rm /workspace/t && echo OK'
run "Firewall script"       "OK"          bash -c 'test -x /usr/local/bin/init-firewall.sh && echo OK'

# The firewall resolves these at container start and drops everything else.
# A domain that stops resolving becomes silently unreachable traffic.
echo "Firewall allowlist resolves"
for d in api.anthropic.com registry.npmjs.org pypi.org conda.anaconda.org repo.anaconda.com; do
  if timeout 60 docker run --rm "$IMAGE" bash -c "getent hosts $d >/dev/null"; then
    ok "$d"
  else
    bad "$d does not resolve — the firewall would block it"
  fi
done

printf '\n\033[1m%d passed, %d failed\033[0m\n' "$pass" "$fail"
echo "Image left as '$IMAGE'; remove with: docker rmi $IMAGE"
[[ $fail -eq 0 ]] || exit 1
