#!/usr/bin/env sh
# Runs pulsar_guard.py with whichever Python 3 exists (python3 on Linux/macOS, python on Windows Git Bash).
# Passes stdin through and keeps the exit code (2 = block). If no Python exists, the guard is skipped:
# the permission deny rules in settings.json still apply.
dir=$(dirname "$0")
for py in python3 python; do
  if command -v "$py" >/dev/null 2>&1 && "$py" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 9) else 1)' >/dev/null 2>&1; then
    exec "$py" "$dir/pulsar_guard.py" "$@"
  fi
done
echo "pulsar_guard: no Python 3.9+ found; hook skipped" >&2
exit 0
