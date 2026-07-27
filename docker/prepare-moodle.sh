#!/usr/bin/env bash
# Prepares the Moodle source for the Docker demo (macOS/Linux).
#
#   bash docker/prepare-moodle.sh [/path/to/moodle]
#
# Why this exists: the Moodle code folder holds ~29,000 files. Copying those
# individually across Docker's file-sharing boundary is slow (especially on
# macOS). Packing them into a single tarball here lets the container extract it
# internally, which is far faster.
#
# Reads MOODLE_SRC from .env unless a path is given as the first argument.
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(dirname "$script_dir")"

source_dir="${1:-}"

if [ -z "$source_dir" ] && [ -f "$repo_root/.env" ]; then
  source_dir="$(grep -E '^[[:space:]]*MOODLE_SRC[[:space:]]*=' "$repo_root/.env" \
    | tail -n1 | cut -d= -f2- | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')"
fi

if [ -z "$source_dir" ]; then
  echo "ERROR: MOODLE_SRC not set. Add it to .env or pass the path as an argument." >&2
  exit 1
fi

if [ ! -f "$source_dir/version.php" ]; then
  echo "ERROR: '$source_dir' does not look like a Moodle code folder (no version.php)." >&2
  exit 1
fi

dist_dir="$script_dir/moodle-dist"
mkdir -p "$dist_dir"
out_file="$dist_dir/moodle-src.tar.gz"

echo "Packing Moodle source..."
echo "  source : $source_dir"
echo "  output : $out_file"
echo "This takes a minute or two."

tar --exclude='.git' -czf "$out_file" -C "$source_dir" .

echo "Done: $out_file ($(du -h "$out_file" | cut -f1))"
echo
echo "Now start the full demo with:"
echo "  docker compose -f docker-compose.yml -f docker-compose.moodle.yml up -d"
