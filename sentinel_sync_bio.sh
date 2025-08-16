#!/usr/bin/env bash
set -euo pipefail
SRC="$HOME/OneDrive/Projects/heartbound-bio"
DST="$HOME/Repos/heartbound-bio"
[ -d "$DST/.git" ] || { rm -rf "$DST"; git clone https://github.com/isaacbland1/heartbound-bio.git "$DST"; }
rsync -a --delete --exclude '.git/' --exclude '.gitignore' "$SRC"/ "$DST"/
ASKPASS="$(mktemp)"; printf '%s\n' '#!/usr/bin/env bash' 'cat ~/OneDrive/System/github_token.txt' > "$ASKPASS"
chmod +x "$ASKPASS"; export GIT_ASKPASS="$ASKPASS"
cd "$DST"
git config user.name "Sentinel Bot"
git config user.email "bot@sentinel.local"
git add -A
git commit -m "Sentinel sync: $(date -u '+%Y-%m-%dT%H:%M:%SZ')" || true
git push origin main
rm -f "$ASKPASS"
