# X → CLIP → MAP: Event Photo → Transactional GIS Page Standard

**Version 1.0 — September 2026 · Owner: @alexdolbun (Aleksei Dolgikh) · UnicornsMap.com / $UM-Radar**

This document describes the production standard used by the $UM-Radar autonomous ingest
pipeline to turn a real-life event photo (organizer/stage/group shot, X post) into a
fully transactional, multilingual, GIS-pinned event page on UnicornsMap.com — without
ever breaking existing routes (additive-only rule).

---

## 1. Pipeline Overview

```
X post (seed URL + pbs.twimg.com media)
  → fetch https media (full resolution)
  → PHOTO-QAA gate (real organizer/stage photo only)
  → fact verification (≥2 independent sources per claim; multilingual where applicable)
  → face-clip every roster person (organizer-published headshots preferred; Haar-cascade
     clipping for stage photos, manual name→tile QA)
  → watermark ingest copy ($UM-Radar)
  → CDN upload (zo.space assets, /images/events/<slug>/…)
  → additive worker node (CORE_EVENTS) + founder relation edge
  → SSR page /radar/<slug> + /events/<slug> + 20-language cluster
  → feeds (events.json, geo.json, geojson.json, relations.json, x402/catalog.json)
  → sitemap + EVENT_GIS_UNIFIED_DATA.json record
  → live HTTP verification (200s across the board)
```

## 2. PHOTO-QAA Gate (hard gate — no exceptions)

A photo may only be ingested when it passes all of:

- **REAL-2**: it is a real photograph of the actual event (organizer-published poster,
  stage/screen shot, or confirmed attendee capture) — never AI-generated imagery.
- Official event branding is visible and attributable.
- Faces are either organizer-published headshots (preferred) or clippable stage tiles.
- Occluded/blurred body-shots are excluded from the roster and kept only as evidence.

If the gate fails → log only, do not publish (`publish_x=false`).

## 3. OSINT Canon

1. **No invented attendees, titles, net worths, or deals.** Roster = officially
   agenda-confirmed / organizer-poster names only.
2. **HANDLE_UNKNOWN** where an X handle or affiliation is unverified — never guess.
3. **Month-precision dates** when the exact day is unpublished (`"date": "2026-08"`).
4. **Real venue coordinates only** (OSM relation / venue page). When the exact venue is
   unpublished, use the city centroid and mark `venue: "<city> (exact venue unpublished)"`.
5. **Name disambiguation**: cross-check name + org + role + city before connecting
   entities; flag collisions.
6. **Public links stay on unicornsmap.com** (affiliate links: Bankr do-follow).

## 4. Worker Node Contract (additive CORE_EVENTS node)

```js
"<event-slug>": {
  slug: "<event-slug>",
  title: "<EN title>",                       // required by /events SSR
  sub: "<one-line meta>",
  desc: "<OSINT profile — verified facts only>",
  img / banner: "<CDN banner URL>",
  city, country, date, venue, lat, lng,      // GIS pin
  currencies: ["SAR","USD","USDC"],          // local currency first
  languages: [/* 20-lang cluster */],
  x402Price: 4.99,                           // USDC on Base
  site: "<official site>",
  sources: [ { url, label } ],               // ≥2 independent incl. official where possible
  photos: [ { src, alt, caption } ],
  speakers: [ { name, org, role, handle, confidence, photo, note } ],
  tr: { ja: {title, desc}, zh: {title, desc}, /* … */ }
}
```

Plus exactly one founder edge in the alexdolbun relations array:

```js
{ name: "<event-slug>", relation: "UnicornsMap.com $UM-Radar founder-indexed event edge
  (<cycle id>) — <event summary>; radar coverage edge, no attendance asserted",
  type: "osint_index" }
```

**Guard rails**: `node --check` before deploy; deploy only via
`wrangler deploy --config wrangler-deploy.toml`; never remove or rewrite existing nodes;
duplicate edges are a bug — one edge per event.

## 5. Page Rails (SSR, delivered by the worker)

- `/radar/<slug>` and `/events/<slug>` — server-rendered, unique `<title>` per locale.
- `/[lang]/radar/<slug>` for 20 locales; native `tr` titles for ja/zh at minimum.
- hreflang cluster (20 languages + x-default), canonical, OG + Twitter cards, JSON-LD.
- x402 rails: `x402payment = 1 · <price> USDC → full event dossier ·
  POST /v1/x402/upload with x402-payment header · HNWI $99/mo /v1/x402/alpha/feed`.
- Bankr affiliate (do-follow): `https://bankr.bot?ref=um-radar`,
  terminal refCode `RN982CZZ-BNKR`.

## 6. Feed Consistency Checklist (post-deploy verification)

| Feed | Check |
|---|---|
| `/api/radar/events.json` | count +1, new slug present |
| `/api/radar/geo.json` | new pin present (real coords) |
| `/api/radar/geojson.json` | new feature present |
| `/api/radar/relations.json` | exactly one new founder edge |
| `/api/x402/catalog.json` | new row at x402Price |
| `/api/radar/search.json?q=<term>` | new page is a top hit |
| sitemap.xml | 3 URLs (en/ja/zh at minimum) |
| homepage | 200, unbroken |

## 7. CDN Layout

```
/images/events/<slug>/banner.jpg
/images/events/<slug>/speakers-grid-wm.jpg
/images/events/<slug>/speakers/<slug>-01-<person>.jpg   # one clip per roster person
```

All assets verified HTTP 200 before page deploy; watermarked ingest copy only.

## 8. Unified Data Record

Every ingested event appends a record to `EVENT_GIS_UNIFIED_DATA.json`
(schema sample in `docs/SCHEMA-sample.json`) so downstream GIS/agent pipelines
can consume one canonical event graph.

## 9. Worked Examples (live)

- `unicornsmap.com/radar/wikiexpo-hk-2026` — WikiEXPO Hong Kong 2026 prediction-markets panel
- `unicornsmap.com/radar/smf-connect-2026` — SMF Connect Riyadh (Saudi Media Forum)
- `unicornsmap.com/radar/emergence-2026-sydney` — EMERGENCE 2026 Sydney
