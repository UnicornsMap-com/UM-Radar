# $UM-Radar ZO PACK — v20260912 (FROZEN)

Intake pack for the 15-minute `INTAKE → CLASSIFY → FACT+GEO+FX → CARD+I18N → QAA → DRAFT → VERIFY → PROMOTE` cycle.
**Prod law: additive-only, draft first, promote only on `UM PROMOTE <slug>` after gates G00–G16 pass.**

## Frozen artifact
| item | value |
|---|---|
| system prefix id | `SYSTEM_PREFIX_V20260912` |
| file | `05-FLASH-SYSTEM-PREFIX.txt` (895 bytes) |
| sha256 | `6099571b26e306219d974b2f6bfcaaf08d33b84ac1baa9357041d3bd90496a89` |
| hot model | `deepseek-flash` (DeepSeek V4.1 Flash) |
| frozen | 2026-09-12 (immutable — never reword, reorder, timestamp or version-stamp) |

Variable document payload goes **after** the prefix, never before. Never inject operator chat into the prefix.
Cache-hit input is the unit economics → hit-ratio target **≥0.70**; batch same-role calls so bytes 0..N stay identical.
Off-peak bulk i18n window: 16:00–22:00 Asia/Shanghai.

## Contents
| file | role |
|---|---|
| `00-ZO-CONDUCTOR-INGEST-v2026-09-12.md` | mission, swarm roles, 15-min cycle, output law, cache law |
| `01-CLASSIFIER-TAXONOMY.json` | entity_type / status / sector / personas / lang20 / ccy_core + envelope schema |
| `02-QAA-GATES.json` | gates G00–G16 (fail-closed) + verify table + rollback rule |
| `03-CACHE-CONTRACT.json` | cache rules, pricing ref, anti-patterns |
| `04-UX-CARD-CONTRACT.json` | iPhone-dense card, personas, i18n must-before-promote (en/ja/zh) |
| `05-FLASH-SYSTEM-PREFIX.txt` | **FROZEN** Flash system prefix |
| `06-WORKER-NODE-TEMPLATE.json` | additive worker node shape (copy keys only) |
| `07-ZO-EMAIL-BODY.txt` | original intake email body |
| `FREEZE-MANIFEST-v20260912.json` | freeze record + live-edge verification |
| `SHA256SUMS.txt` | integrity list for every file in this pack |
| `verify-prefix.sh` | HIT-CACHE guard — fails if the prefix was mutated |
| `flash-prompt.py` | builds a cache-stable request (frozen prefix + payload after it) |

## Use
```bash
cd ~/um-radar/zo-pack
./verify-prefix.sh                                  # must print OK before any Flash call
python3 flash-prompt.py classify payload.json       # writes request JSON, prefix verified
sha256sum -c SHA256SUMS.txt                         # integrity of the whole pack
```

## Live edge (verified 2026-09-12, do not invent replacements)
- site `https://unicornsmap.com` (homepage 200)
- `$UM` CA `0x909851A8598f560F2F3B68Bb949D836E7dbb5e93` · payTo `0x211D91beD006f7bB3Eaf97496260a8F905298Cea`
- `GET /api/x402/status` → `edge-v2026-07-01-bankr-cmc` · 5 USDC / Base (unchanged)
- bankr ref `RN982CZZ-BNKR` · whois_until `2036-12-31` · catalog 272 entities / 20 locales
- canon `docs/EVENT-INGEST-STANDARD.md` + `docs/SCHEMA-sample.json`
- live examples `wikiexpo-hk-2026` `smf-connect-2026` `emergence-2026-sydney`

Verify table (green): `/`, `/api/radar/events.json`, `/api/radar/geo.json`, `/api/radar/geojson.json`, `/api/radar/relations.json`, `/api/x402/catalog.json`, `/api/radar/{slug}.json`, `/radar/{slug}`, `/sitemap.xml`.

## Operator commands (email)
`UM INTAKE <url>` · `UM CLASSIFY` · `UM QAA <slug>` · `UM PROMOTE <slug>` · `UM HOLD` · `UM STATUS`

## Edge cases
- Any 4xx/5xx on the homepage or an existing slug → roll back **that change only**, keep the rest.
- Slug collision (`/api/x402/catalog.json`) → rekey or merge, never overwrite.
- `publish_x=false` until the verify table is green; PHOTO-QAA REAL-2 for event photos; `HANDLE_UNKNOWN` when unverified.
- CMC Gravity is a **sidecar** — never auto-post to CoinMarketCap on promote.
