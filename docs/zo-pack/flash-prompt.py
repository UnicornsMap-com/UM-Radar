#!/usr/bin/env python3
"""Build a cache-stable DeepSeek Flash request: frozen prefix + variable payload.

Usage: python3 flash-prompt.py <role> <payload-file> [out.json]
role = classify | i18n | fx | schema_fill
Prefix is loaded byte-for-byte; payload goes AFTER it, never before.
"""
import hashlib, json, sys, pathlib

FROZEN = "6099571b26e306219d974b2f6bfcaaf08d33b84ac1baa9357041d3bd90496a89"
HERE = pathlib.Path(__file__).resolve().parent
MODEL = "deepseek-flash"

def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    role, payload_path = sys.argv[1], sys.argv[2]
    out = sys.argv[3] if len(sys.argv) > 3 else f"/tmp/flash-{role}-request.json"

    prefix_bytes = (HERE / "05-FLASH-SYSTEM-PREFIX.txt").read_bytes()
    got = hashlib.sha256(prefix_bytes).hexdigest()
    if got != FROZEN:
        print(f"FAIL: prefix mutated (frozen {FROZEN}, actual {got})", file=sys.stderr)
        return 1

    payload = pathlib.Path(payload_path).read_text(encoding="utf-8")
    request = {
        "model": MODEL,
        "system": prefix_bytes.decode("utf-8"),
        "messages": [{"role": "user", "content": payload}],
        "response_format": {"type": "json_object"},
        "prefix_sha256": got,
        "role": role,
    }
    pathlib.Path(out).write_text(json.dumps(request, ensure_ascii=False), encoding="utf-8")
    print(out)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
