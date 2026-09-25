# ChainMind AI — Frontend

Vite + React frontend for the ChainMind AI semiconductor supply-chain risk
platform. Built against **mock data that mirrors your real backend payload
shapes exactly**, so swapping in the FastAPI layer later is a data-source
change, not a rebuild.

## Run it

```bash
npm install
npm run dev
```

Then open the printed local URL. `npm run build` produces a production
bundle in `dist/`.

> This project was authored in a sandboxed environment with no package
> registry access, so `npm install` has not been run or build-verified here.
> Every `.jsx`/`.js` file has been syntax-checked with `tsc --allowJs`, and
> the mock data module has been executed directly with Node to confirm the
> data shapes are internally consistent — but please run `npm install &&
> npm run dev` as your first step and flag anything that doesn't come up
> clean.

## What's here

```
src/
  components/
    globe/    GlobeScene.jsx       — the 3D globe (react-globe.gl), reused on
                                      both the landing page and Analyst Mode
    die/      DieSilhouette.jsx    — the "zoomed in" region view
    ticker/   AlertTicker.jsx      — live intelligence feed
    stats/    StatsGrid.jsx        — materials + fused-risk cards (Recharts)
    chat/     ChatPanel.jsx        — the RAG assistant
    layout/   NavBar.jsx
  pages/
    Landing.jsx      — hero globe, ticker+chat split, stats, reroute spotlight
    AnalystMode.jsx   — full chat + globe workspace (route: /analyst)
  lib/
    mockData.js       — all mock data, shaped exactly like your backend contract
```

## Design decisions worth knowing about

**Palette.** Near-black substrate (`--bg-void`), deep pine-green panels
(`--bg-panel`), one reserved "trace" green (`--signal`) for anything live or
active. Amber and red are used *only* for elevated/critical status — never
decoratively — so a glance at any panel tells you severity, not just style.
All tokens live in `src/styles/theme.css`.

**Type.** IBM Plex Mono for headlines, numbers, timestamps, and anything
"spec-sheet"-like (this mirrors how process nodes and die markings actually
get labeled in the industry). Inter for body copy, where mono would hurt
readability.

**Region "die" silhouettes, not literal maps.** When you click a globe node,
it doesn't crossfade into a traced country border — it reveals a
procedurally generated, chip-die-style silhouette (`components/die/`) with
facility markers and a timeline, in the same visual language as the chips
the platform tracks. This was a deliberate choice, not just a shortcut: real
topojson map data means shipping a geo dataset and fetching it at runtime,
and it also visually clashes with the "circuit board" material language of
the globe itself. The die shapes are procedurally generated from a seed
string (`components/die/dieShapes.js`) — no external map data, and no two
regions look alike. If you'd rather have literal geographic borders later,
that's a contained swap inside `DieSilhouette.jsx`.

**Globe interaction.** Built on `react-globe.gl` (Three.js underneath):
freely draggable 360°, gentle auto-rotate when idle, hover tooltips per
node, pulsing red rings on any `status: "critical"` entity, and
`globeRef.current.pointOfView(...)` for the "zoom in" camera move on click.

**Chat ↔ globe wiring.** `ChatPanel` resolves a query against
`resolveChatQuery()` in `mockData.js` and returns which node(s) it's talking
about. Both pages lift that up and call `globeRef.current.flyTo(entity)`, so
asking about TSMC in the chat visibly flies the camera there — this is the
`current_node_context` behavior from your data contract, wired end to end
even on mock data.

## Wiring to the real backend

Everything is intentionally centralized so this is a small diff, not a
rewrite:

1. **`src/lib/mockData.js`** — replace the exported arrays with `fetch()` /
   WebSocket calls into your FastAPI layer once it exists. Keep the same
   field names (`risk_score`, `impact_score`, `commodity_scarcity_index`,
   etc.) and every component below keeps working unchanged.
2. **`ChatPanel.jsx`** — the `setTimeout(...)` block in `send()` is the one
   place to swap for a real call, e.g.:
   ```js
   const res = await fetch('/api/chat', {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify({ query: q, node_context: currentNodeId }),
   })
   const result = await res.json() // { response, cited_sources, current_node_context }
   ```
3. **Live ticker / globe** — for real-time alerts, a WebSocket pushing new
   `Alert Objects` (per `ingestor.py`) is the natural fit; `AlertTicker`
   already renders whatever array it's given, so it's a subscribe-and-set
   State change in the parent page.

## Known gaps / next passes

- No FastAPI layer exists yet — see above.
- The die-silhouette facility markers are placed deterministically but
  **not** at real geographic positions within the region (see design note
  above).
- Mobile layout is handled down to ~640px; a phone-first pass on the
  Analyst Mode split view would be worth a dedicated look once real data's
  flowing in.
