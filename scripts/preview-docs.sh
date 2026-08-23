#!/usr/bin/env bash
# Render the docs site locally and serve it, so you can look at the real HTML
# before it goes anywhere near main.
#
#     ./scripts/preview-docs.sh          # serve at http://localhost:4000/dunnlab_code/
#     ./scripts/preview-docs.sh build    # build only, report and exit
#     ./scripts/preview-docs.sh 8080     # serve on a different port
#
# Runs in Docker, so no Ruby is needed on the host. Gems are cached in a named
# volume, so the first run is slow (a few minutes) and later ones are quick.
#
# GitHub Pages builds this site with its legacy builder, which uses the
# `github-pages` gem — the same gem docs/Gemfile pins. So what you see here is
# close to what gets published, including the remote just-the-docs theme.

set -uo pipefail
cd "$(dirname "$0")/.."
REPO=$(pwd)

IMAGE=ruby:3.3
VOLUME=dunnlab-jekyll-bundle
MODE=serve
PORT=4000

case "${1:-}" in
  build)      MODE=build ;;
  ''|serve)   ;;
  [0-9]*)     PORT=$1 ;;
  *)          echo "usage: $0 [build|serve|<port>]"; exit 2 ;;
esac

command -v docker >/dev/null 2>&1 || {
  echo "docker not found."
  echo "Alternative without Docker: install Ruby, then"
  echo "  cd docs && bundle install && bundle exec jekyll serve"
  exit 1
}

# `bundle install` writes Gemfile.lock into docs/. It is gitignored.
common=(--rm
        -v "$REPO/docs:/site" -w /site
        -v "$VOLUME:/usr/local/bundle")

if [[ "$MODE" == build ]]; then
  echo "Building docs/ with the github-pages gem…"
  docker run "${common[@]}" "$IMAGE" bash -c '
    bundle install --quiet && bundle exec jekyll build -d /tmp/out --trace
  ' || { echo; echo "Build failed — that is the point of this script."; exit 1; }
  echo
  echo "Build succeeded."
  exit 0
fi

echo "Starting Jekyll. First run installs gems and takes a few minutes."
echo
echo "    http://localhost:${PORT}/dunnlab_code/"
echo
echo "Ctrl-C to stop. Edits to docs/ rebuild automatically."
echo

# --force_polling: file-change events do not cross the bind mount reliably.
docker run -it "${common[@]}" -p "${PORT}:4000" "$IMAGE" bash -c '
  bundle install --quiet && exec bundle exec jekyll serve \
    --host 0.0.0.0 --port 4000 --force_polling --incremental
'
