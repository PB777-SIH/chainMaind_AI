// Region "die" silhouette content — genuinely frontend-only display data,
// not a stand-in for a backend call. Everything else lives in api.js now.

export const dieRegions = {
  taiwan: { label: 'Taiwan — Hsinchu / Kaohsiung Corridor', node: 'N3 / N4 process node', events: [
    { year: '2024', text: 'Fab 18 Phase 3 reaches volume production on N3E.' },
    { year: '2025', text: 'Kaohsiung port automation upgrade begins.' },
    { year: '2026', text: 'Seismic monitoring network expanded island-wide.' },
  ]},
  korea: { label: 'South Korea — Pyeongtaek / Icheon Corridor', node: 'N4 / DRAM', events: [
    { year: '2024', text: 'Samsung Line 4 breaks ground at Pyeongtaek.' },
    { year: '2025', text: 'SK Hynix expands HBM capacity at Icheon.' },
    { year: '2026', text: 'Line 4 reaches qualification yield.' },
  ]},
  netherlands: { label: 'Netherlands — Veldhoven', node: 'EUV / High-NA lithography', events: [
    { year: '2023', text: 'First High-NA EUV system ships to customer fab.' },
    { year: '2025', text: 'Export licensing framework revised.' },
    { year: '2026', text: 'Bookings beat on High-NA order momentum.' },
  ]},
  usa: { label: 'United States — Arizona / Oregon / New York', node: 'N3 / Legacy nodes', events: [
    { year: '2024', text: 'Ocotillo Fab 42 begins risk production.' },
    { year: '2025', text: 'Hillsboro D1X expansion completed.' },
    { year: '2026', text: 'Malta fab adds specialty node capacity.' },
  ]},
  ukraine: { label: 'Ukraine — Odessa Refining Corridor', node: 'Neon gas refining', events: [
    { year: '2022', text: 'War disrupts ~50% of global neon refining capacity.' },
    { year: '2025', text: 'Partial line restart under contested conditions.' },
    { year: '2026', text: 'Second line forced offline; scarcity index spikes.' },
  ]},
  china: { label: 'China — Shanghai Corridor', node: 'Legacy / mature nodes', events: [
    { year: '2024', text: 'Shanghai port throughput hits record volume.' },
    { year: '2025', text: 'Mature-node capacity additions announced.' },
    { year: '2026', text: 'Seasonal typhoon window forces berth closures.' },
  ]},
  australia: { label: 'Australia — Western Quartz Belt', node: 'High-purity quartz', events: [
    { year: '2023', text: 'New reserve certified for semiconductor-grade quartz.' },
    { year: '2025', text: 'Export volumes rise to meet crucible demand.' },
    { year: '2026', text: 'Scarcity index remains low, supply diversified.' },
  ]},
  russia: { label: 'Russia — Norilsk Belt', node: 'Palladium / sputtering targets', events: [
    { year: '2024', text: 'Sanctions regime tightens on metal exports.' },
    { year: '2025', text: 'Alternative sourcing from South Africa ramps.' },
    { year: '2026', text: 'New sanctions package targets palladium directly.' },
  ]},
}

// your backend returns `country`, not the region slug the die-silhouette
// keys off — bridges the two without teaching the backend a frontend concept
const COUNTRY_TO_REGION_SLUG = {
  Taiwan: 'taiwan', 'South Korea': 'korea', Netherlands: 'netherlands',
  USA: 'usa', China: 'china', Ukraine: 'ukraine', Australia: 'australia', Russia: 'russia',
}

export function regionSlugForCountry(country) {
  return COUNTRY_TO_REGION_SLUG[country] || null
}