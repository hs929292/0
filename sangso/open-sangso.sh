#!/bin/bash
# macOS: opens today's memorial once per day. Pass --force to open again.
dir="$(cd "$(dirname "$0")" && pwd)"
stamp="$dir/.last-shown"
today="$(date +%F)"

if [ "$1" != "--force" ] && [ -f "$stamp" ] && [ "$(cat "$stamp")" = "$today" ]; then
  exit 0
fi
echo "$today" > "$stamp"
open "$dir/index.html"
