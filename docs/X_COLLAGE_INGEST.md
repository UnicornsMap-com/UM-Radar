# X collage → UnicornsMap GIS OSINT ingest

North star: almost-autonomous [UnicornsMap.com](https://unicornsmap.com) $UM-Radar GIS OSINT alpha for onchain upside (2026–2036+).

## Pipeline
1. Discover `@alexdolbun` posts with `$UM` / UnicornsMap / collage / GIS face-grid media.
2. Fetch **https** media URLs only (never private box paths).
3. Face-clip every detectable person (evidence-only names/handles).
4. Upsert unique `/radar/{slug}` SSR pages — 20 langs, hreflang, live `$UM` Dex/mcap, x402, Bankr.
5. Map pin with **real GIS coords** (event venue or person city — never random).
6. Index search + edges (`alexdolbun` ↔ person/event).
7. Cloudflare Worker rails: additive entity/event/search updates only.

## Seed
- Post: https://x.com/alexdolbun/status/2021725800886632924
- Media: https://pbs.twimg.com/media/HA6c5AiXgAAo30D.jpg

## Guardrails
- Additive only — no App.tsx smash, no SPA redeploy as the fix.
- Never invent people, valuations, or coordinates.
- Prefer SLM triage for classify/translate; heavy waves on Zo GLM.
- OSS agents: implement against `schemas/*.schema.json` and open PRs.