#!/bin/bash
# macOS: open the memorial every day at 7:00 AM and at login.
# Undo: launchctl unload ~/Library/LaunchAgents/com.sangso.zhugeliang.plist && rm that file
set -e
dir="$(cd "$(dirname "$0")" && pwd)"
chmod +x "$dir/open-sangso.sh"
plist="$HOME/Library/LaunchAgents/com.sangso.zhugeliang.plist"
mkdir -p "$HOME/Library/LaunchAgents"

cat > "$plist" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key><string>com.sangso.zhugeliang</string>
  <key>ProgramArguments</key>
  <array><string>/bin/bash</string><string>$dir/open-sangso.sh</string></array>
  <key>RunAtLoad</key><true/>
  <key>StartCalendarInterval</key>
  <dict><key>Hour</key><integer>7</integer><key>Minute</key><integer>0</integer></dict>
</dict>
</plist>
EOF

launchctl unload "$plist" 2>/dev/null || true
launchctl load "$plist"
echo "Installed: daily 7:00 AM + at login."
"$dir/open-sangso.sh" --force
