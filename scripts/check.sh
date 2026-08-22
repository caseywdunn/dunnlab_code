#!/usr/bin/env bash
# Structural checks for the dunnlab-code plugin and docs site.
#
# Fast, free, and offline except for --links. Run before opening a PR:
#     ./scripts/check.sh
#     ./scripts/check.sh --links     # also verify external URLs resolve
#
# Exits non-zero if any check fails, so it can gate CI.

set -uo pipefail
cd "$(dirname "$0")/.."

CHECK_LINKS=0
[[ "${1:-}" == "--links" ]] && CHECK_LINKS=1

pass=0; fail=0; skip=0
ok()   { printf '  \033[32m✓\033[0m %s\n' "$1"; pass=$((pass+1)); }
bad()  { printf '  \033[31m✗\033[0m %s\n' "$1"; fail=$((fail+1)); }
skip_() { printf '  \033[33m–\033[0m %s (skipped)\n' "$1"; skip=$((skip+1)); }
head_() { printf '\n\033[1m%s\033[0m\n' "$1"; }

# ---------------------------------------------------------------- manifests
head_ "Manifests"

if command -v claude >/dev/null 2>&1; then
  if out=$(claude plugin validate . --strict 2>&1); then
    ok "claude plugin validate --strict"
  else
    bad "claude plugin validate --strict"; echo "$out" | sed 's/^/      /'
  fi
else
  skip_ "claude plugin validate — claude not on PATH"
fi

for f in .claude-plugin/plugin.json .claude-plugin/marketplace.json assets/settings.json; do
  if python3 -c "import json,sys; json.load(open('$f'))" 2>/dev/null; then
    ok "$f parses as JSON"
  else
    bad "$f is not valid JSON"
  fi
done

# plugin.json and the marketplace entry must agree on version, or
# `claude plugin tag` refuses and installs pick up the wrong number.
pv=$(python3 -c "import json;print(json.load(open('.claude-plugin/plugin.json'))['version'])" 2>/dev/null)
mv=$(python3 -c "import json;print(json.load(open('.claude-plugin/marketplace.json'))['plugins'][0]['version'])" 2>/dev/null)
if [[ -n "$pv" && "$pv" == "$mv" ]]; then
  ok "version agrees across manifests ($pv)"
else
  bad "version mismatch: plugin.json=$pv marketplace.json=$mv"
fi

# ------------------------------------------------------------------- skills
head_ "Skills and commands"

res=$(python3 - <<'PY'
import pathlib, re
bad=[]; CAP=1536; total=0
for p in sorted(pathlib.Path('skills').glob('*/SKILL.md')):
    t=p.read_text()
    if not t.startswith('---'): bad.append(f"{p}: no YAML frontmatter"); continue
    fm=t.split('---',2)[1]
    if not re.search(r'^description:',fm,re.M): bad.append(f"{p}: no description field")
    n=re.search(r'^name:\s*(\S+)',fm,re.M)
    if n and n.group(1)!=p.parent.name:
        bad.append(f"{p}: name '{n.group(1)}' != directory '{p.parent.name}'")
    m=re.search(r'description: >?\s*\n?(.*?)(?=\n\w[\w-]*:|\Z)',fm,re.S)
    if m:
        d=' '.join(m.group(1).split()); total+=len(d)
        if len(d)>CAP: bad.append(f"{p}: description {len(d)} chars > {CAP}")
print(total)
for b in bad: print(b)
PY
)
total=$(echo "$res" | head -1)
rest=$(echo "$res" | tail -n +2 | grep -v '^$' || true)
if [[ -z "$rest" ]]; then
  ok "skill frontmatter valid (descriptions total ${total} chars)"
else
  while IFS= read -r l; do bad "$l"; done <<< "$rest"
fi

# The README and the architecture doc both enumerate skills. They drift.
for doc in README.md dev_docs/plugin-architecture.md; do
  missing=""
  for d in skills/*/; do
    s=$(basename "$d")
    grep -q "$s" "$doc" || missing="$missing $s"
  done
  if [[ -z "$missing" ]]; then ok "$doc lists every skill"; else bad "$doc missing:$missing"; fi
done

# ---------------------------------------------------------------- regressions
head_ "Known-bad strings"

# Each of these was a real error fixed in the 0.3.0 docs pass. They are cheap
# to reintroduce by copy-paste, so they are asserted against here.
declare -A FORBIDDEN=(
  ["docs.anthropic.com"]="moved to code.claude.com (301)"
  ["claude plugin add"]="not a real subcommand"
  ["claude login"]="it is 'claude auth login'"
  ["example-skill"]="skill does not exist"
  ["dunnlab-review"]="skill is named dunnlab-codereview"
  ["data-analysis.md"]="page does not exist"
)
# A line that mentions one of these on purpose — documentation explaining
# what the old mistake was — opts out with a `check-ignore` marker.
for s in "${!FORBIDDEN[@]}"; do
  hits=$(grep -rn --fixed-strings "$s" \
        --include='*.md' --include='*.json' --include='*.sh' \
        --exclude-dir=.git --exclude-dir=workshops \
        --exclude='check.sh' --exclude='CHANGELOG.md' . 2>/dev/null \
        | grep -v 'check-ignore' || true)
  if [[ -z "$hits" ]]; then ok "no '$s' (${FORBIDDEN[$s]})"
  else bad "found '$s' — ${FORBIDDEN[$s]}"; echo "$hits" | sed 's/^/      /'; fi
done

# Bouchet purges scratch at 30 days; McCleary and Misha at 60. A bare "60 day"
# outside those two sections is almost certainly the old wrong figure.
b60=$(grep -rn "60 day\|60-day" skills/dunnlab-hpc/SKILL.md assets/settings.json 2>/dev/null \
      | grep -iv "mccleary\|misha\|grace\|palmer\|radev" || true)
if [[ -z "$b60" ]]; then ok "no stray 60-day scratch claims (Bouchet is 30)"
else bad "possible stale 60-day scratch claim"; echo "$b60" | sed 's/^/      /'; fi

# ------------------------------------------------------------------- docs
head_ "Docs site"

python3 - <<'PY' > /tmp/navcheck 2>&1
import pathlib, re
rows=[]
for p in sorted(pathlib.Path('docs').glob('*.md')):
    fm=p.read_text().split('---',2)[1]
    t=re.search(r'^title:\s*(.+)$',fm,re.M); n=re.search(r'^nav_order:\s*(\d+)',fm,re.M)
    if not t or not n: print(f"BAD {p}: missing title or nav_order"); continue
    rows.append((int(n.group(1)), p.name))
orders=[r[0] for r in rows]
if len(set(orders))!=len(orders): print("BAD duplicate nav_order values:", sorted(orders))
if sorted(orders)!=list(range(1,len(orders)+1)): print("BAD nav_order not contiguous from 1:", sorted(orders))
idx=(pathlib.Path('docs/index.md')).read_text()
for _,name in rows:
    if name=='index.md': continue
    if name not in idx: print(f"BAD docs/index.md does not link {name}")
PY
if [[ -s /tmp/navcheck ]]; then
  while IFS= read -r l; do bad "${l#BAD }"; done < /tmp/navcheck
else
  ok "nav_order contiguous, unique, and every page linked from index"
fi

# internal relative links and same-file anchors
res=$(python3 - <<'PYEOF'
import pathlib,re

def anchors(path):
    """Heading anchors a file offers as link targets.

    Strip fenced and inline code FIRST: a '# comment' inside a bash block is
    not a heading, and counting it would let a bad anchor resolve."""
    t = path.read_text()
    clean = re.sub(r'```.*?```','',t,flags=re.S); clean = re.sub(r'`[^`]*`','',clean)
    a = [re.sub(r'[^a-z0-9 -]','',h.lower()).replace(' ','-') for h in re.findall(r'^#+ +(.+)$',clean,re.M)]
    return set(a) | set(re.findall(r'id="([^"]+)"', t))

cache = {}
def anchors_cached(p):
    if p not in cache: cache[p] = anchors(p)
    return cache[p]

bad = []
for p in pathlib.Path('.').rglob('*.md'):
    if '.git' in p.parts or 'workshops' in p.parts: continue
    t = p.read_text()
    clean = re.sub(r'```.*?```','',t,flags=re.S); clean = re.sub(r'`[^`]*`','',clean)
    for m in re.finditer(r'\]\(([^)]+)\)', clean):
        tgt = m.group(1)
        if tgt.startswith(('http','mailto:')): continue
        path, _, anc = tgt.partition('#')
        target = (p.parent/path) if path else p
        if path and not target.exists():
            bad.append(f"{p}: broken link -> {path}"); continue
        # Cross-file anchors matter most during a restructure, when a section
        # moves between pages and every link into it silently rots.
        if anc and anc not in anchors_cached(target):
            bad.append(f"{p}: broken anchor -> {tgt}")
for b in bad: print(b)
PYEOF
)
if [[ -z "$res" ]]; then ok "internal links and anchors resolve"
else while IFS= read -r l; do bad "$l"; done <<< "$res"; fi

# Bracketed text with no target is not a link -- it renders as literal
# brackets. This is how an unfinished table-of-contents entry escapes the
# link checker entirely, since there is no target for it to resolve.
res=$(python3 - <<'PYEOF'
import pathlib, re
bad = []
for p in pathlib.Path('docs').rglob('*.md'):
    t = p.read_text()
    clean = re.sub(r'```.*?```', '', t, flags=re.S); clean = re.sub(r'`[^`]*`', '', clean)
    for i, line in enumerate(clean.split('\n'), 1):
        # a [label] not followed by (target), [ref], or a :  definition
        for m in re.finditer(r'(?<!\!)\[([^\]\[]*)\](?![\(\[:])', line):
            label = m.group(1)
            # Legitimate bracket uses that are not links: task-list checkboxes,
            # numeric footnote markers, and GitHub alert syntax.
            if label.strip() in ('', 'x', 'X'): continue
            if label.isdigit(): continue
            if label.startswith('!'): continue
            bad.append(f"{p}:{i}: '[{label}]' has no link target")
for b in bad: print(b)
PYEOF
)
if [[ -z "$res" ]]; then ok "no bracketed text without a link target"
else while IFS= read -r l; do bad "$l"; done <<< "$res"; fi

# ------------------------------------------------------------------- links
if [[ $CHECK_LINKS -eq 1 ]]; then
  head_ "External links"
  urls=$(grep -rhoE 'https?://[^ )>"`,]+' --include='*.md' --include='*.json' \
         --exclude-dir=.git --exclude-dir=workshops . 2>/dev/null \
         | sed 's/[.]$//' | grep -v '\${' | grep -v localhost | sort -u)
  n=0; broke=0
  while read -r u; do
    [[ -z "$u" ]] && continue
    n=$((n+1))
    code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 20 -A 'Mozilla/5.0' "$u")
    # 403/429 are bot protection, not dead links
    case "$code" in
      2*|3*|403|429) ;;
      *) echo "      HTTP $code  $u"; broke=$((broke+1)) ;;
    esac
  done <<< "$urls"
  if [[ $broke -eq 0 ]]; then ok "$n external URLs reachable"; else bad "$broke of $n URLs unreachable"; fi
fi

# ------------------------------------------------------------------ summary
printf '\n\033[1m%d passed, %d failed, %d skipped\033[0m\n' "$pass" "$fail" "$skip"
[[ $fail -eq 0 ]] || exit 1
