#!/usr/bin/env bash
# HIT-CACHE GUARD — fails if SYSTEM_PREFIX_V20260912 was mutated.
set -euo pipefail
FROZEN="6099571b26e306219d974b2f6bfcaaf08d33b84ac1baa9357041d3bd90496a89"
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ACTUAL="$(sha256sum "$DIR/05-FLASH-SYSTEM-PREFIX.txt" | awk '{print $1}')"
if [ "$ACTUAL" != "$FROZEN" ]; then
  echo "FAIL: prefix mutated" >&2
  echo "  frozen: $FROZEN" >&2
  echo "  actual: $ACTUAL" >&2
  exit 1
fi
echo "OK: SYSTEM_PREFIX_V20260912 byte-identical ($ACTUAL)"
# the prefix must terminate with exactly one newline and hold no timestamps/slugs
grep -qE '[0-9]{4}-[0-9]{2}-[0-9]{2}T' "$DIR/05-FLASH-SYSTEM-PREFIX.txt" && { echo "FAIL: timestamp inside prefix" >&2; exit 1; } || true
echo "OK: no timestamps, no slug leakage"
