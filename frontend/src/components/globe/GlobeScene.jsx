// import { forwardRef, useEffect, useImperativeHandle, useMemo, useRef, useState } from 'react'
// import Globe from 'react-globe.gl'
// import * as THREE from 'three'
// import { entityById } from '../../lib/mockData'
// import './GlobeScene.css'

// const STATUS_COLOR = {
//   ok: '#4ff2a0',
//   warn: '#f5a623',
//   critical: '#ff4d5e',
// }

// const ROUTE_COLOR = {
//   equipment: 'rgba(79, 242, 160, 0.55)',
//   supply: 'rgba(245, 166, 35, 0.55)',
//   shipping: 'rgba(143, 172, 159, 0.4)',
// }

// function useElementSize() {
//   const ref = useRef(null)
//   const [size, setSize] = useState({ width: 0, height: 0 })

//   useEffect(() => {
//     if (!ref.current) return
//     const el = ref.current
//     const observer = new ResizeObserver((entries) => {
//       const { width, height } = entries[0].contentRect
//       setSize({ width, height })
//     })
//     observer.observe(el)
//     return () => observer.disconnect()
//   }, [])

//   return [ref, size]
// }

// const GlobeScene = forwardRef(function GlobeScene(
//   {
//     entities = [],
//     routes = [],
//     selectedId = null,
//     autoRotate = true,
//     onNodeClick,
//     onNodeHover,
//     onBackgroundClick,
//   },
//   ref
// ) {
//   const [containerRef, { width, height }] = useElementSize()
//   const globeApi = useRef(null)

//   useImperativeHandle(ref, () => ({
//     flyTo(entity, altitude = 0.45) {
//       if (!globeApi.current || !entity) return
//       globeApi.current.controls().autoRotate = false
//       globeApi.current.pointOfView({ lat: entity.lat, lng: entity.lng, altitude }, 1100)
//     },
//     reset() {
//       if (!globeApi.current) return
//       globeApi.current.pointOfView({ lat: 18, lng: 60, altitude: 2.1 }, 900)
//       globeApi.current.controls().autoRotate = autoRotate
//     },
//   }))

//   useEffect(() => {
//     if (!globeApi.current) return
//     const controls = globeApi.current.controls()
//     controls.autoRotate = autoRotate
//     controls.autoRotateSpeed = 0.45
//     controls.enableZoom = true
//     controls.minDistance = 160
//     globeApi.current.pointOfView({ lat: 18, lng: 60, altitude: 2.1 })
//     // eslint-disable-next-line react-hooks/exhaustive-deps
//   }, [width, height])

//   const globeMaterial = useMemo(() => {
//     const mat = new THREE.MeshPhongMaterial()
//     mat.color = new THREE.Color('#0a1b13')
//     mat.emissive = new THREE.Color('#04120a')
//     mat.emissiveIntensity = 0.35
//     mat.shininess = 6
//     return mat
//   }, [])

//   const arcsData = useMemo(
//     () =>
//       routes
//         .map((r) => {
//           const s = entityById[r.startId]
//           const e = entityById[r.endId]
//           if (!s || !e) return null
//           return {
//             id: r.id,
//             startLat: s.lat,
//             startLng: s.lng,
//             endLat: e.lat,
//             endLng: e.lng,
//             color: ROUTE_COLOR[r.kind] || ROUTE_COLOR.shipping,
//             kind: r.kind,
//           }
//         })
//         .filter(Boolean),
//     [routes]
//   )

//   const ringsData = useMemo(
//     () =>
//       entities
//         .filter((e) => e.status === 'critical')
//         .map((e) => ({ ...e, color: STATUS_COLOR.critical })),
//     [entities]
//   )

//   return (
//     <div ref={containerRef} className="globe-canvas">
//       {width > 0 && (
//         <Globe
//           ref={globeApi}
//           width={width}
//           height={height}
//           backgroundColor="rgba(0,0,0,0)"
//           globeMaterial={globeMaterial}
//           showAtmosphere
//           atmosphereColor="#4ff2a0"
//           atmosphereAltitude={0.16}
//           showGraticules
//           pointsData={entities}
//           pointLat="lat"
//           pointLng="lng"
//           pointColor={(d) => (d.id === selectedId ? '#e9f4ee' : STATUS_COLOR[d.status] || STATUS_COLOR.ok)}
//           pointAltitude={(d) => (d.id === selectedId ? 0.05 : 0.012)}
//           pointRadius={(d) => (d.id === selectedId ? 0.65 : d.status === 'critical' ? 0.5 : 0.36)}
//           pointResolution={16}
//           pointLabel={(d) => `
//             <div style="
//               font-family: 'IBM Plex Mono', monospace;
//               background: #0c1e16;
//               border: 1px solid #2a4f3a;
//               border-radius: 8px;
//               padding: 10px 12px;
//               color: #e9f4ee;
//               font-size: 12px;
//               max-width: 220px;
//               box-shadow: 0 8px 24px rgba(0,0,0,0.45);
//             ">
//               <div style="color:#4ff2a0; font-size:10px; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:4px;">${d.type} · ${d.country}</div>
//               <div style="font-size:13px; font-weight:600; margin-bottom:6px;">${d.name}</div>
//               <div>risk_score <b style="color:${STATUS_COLOR[d.status]}">${d.risk_score.toFixed(2)}</b></div>
//               <div style="color:#8fac9f; margin-top:2px;">click to zoom in →</div>
//             </div>
//           `}
//           onPointClick={(d) => onNodeClick && onNodeClick(d)}
//           onPointHover={(d) => onNodeHover && onNodeHover(d)}
//           ringsData={ringsData}
//           ringLat="lat"
//           ringLng="lng"
//           ringColor={() => (t) => `rgba(255, 77, 94, ${1 - t})`}
//           ringMaxRadius={3.2}
//           ringPropagationSpeed={2.4}
//           ringRepeatPeriod={1000}
//           arcsData={arcsData}
//           arcColor="color"
//           arcAltitude={0.22}
//           arcStroke={0.42}
//           arcDashLength={0.4}
//           arcDashGap={0.6}
//           arcDashAnimateTime={2600}
//           onGlobeClick={() => onBackgroundClick && onBackgroundClick()}
//         />
//       )}
//     </div>
//   )
// })

// export default GlobeScene



import { forwardRef, useEffect, useImperativeHandle, useMemo, useRef, useState } from 'react'
import Globe from 'react-globe.gl'
import * as THREE from 'three'
import { feature } from 'topojson-client'
//import { entityById } from '../../lib/mockData'
import './GlobeScene.css'

const STATUS_COLOR = {
  ok: '#4ff2a0',
  warn: '#f5a623',
  critical: '#ff4d5e',
}

const ROUTE_COLOR = {
  equipment: 'rgba(79, 242, 160, 0.55)',
  supply: 'rgba(245, 166, 35, 0.55)',
  shipping: 'rgba(143, 172, 159, 0.4)',
}

// world-atlas / Natural Earth spells some of our countries differently
// than our own mock data does — this maps our `country` field to every
// spelling we might see in the topojson so the fill/lookup still hits.
const COUNTRY_NAME_VARIANTS = {
  Taiwan: ['Taiwan'],
  'South Korea': ['South Korea', 'Korea, Rep.', 'Republic of Korea'],
  Netherlands: ['Netherlands', 'The Netherlands'],
  USA: ['United States of America', 'United States'],
  China: ['China', "People's Republic of China"],
  Ukraine: ['Ukraine'],
  Australia: ['Australia'],
  Russia: ['Russia', 'Russian Federation'],
}

// countries with no tracked facility still get a faint "etched" green
// wash so the whole globe reads as landmass, not just our watchlist
function riskFillColor(risk) {
  if (risk == null) return 'rgba(79, 242, 160, 0.055)'
  if (risk >= 0.65) return 'rgba(255, 77, 94, 0.42)'
  if (risk >= 0.4) return 'rgba(245, 166, 35, 0.38)'
  return 'rgba(79, 242, 160, 0.3)'
}

function useElementSize() {
  const ref = useRef(null)
  const [size, setSize] = useState({ width: 0, height: 0 })

  useEffect(() => {
    if (!ref.current) return
    const el = ref.current
    const observer = new ResizeObserver((entries) => {
      const { width, height } = entries[0].contentRect
      setSize({ width, height })
    })
    observer.observe(el)
    return () => observer.disconnect()
  }, [])

  return [ref, size]
}

const GlobeScene = forwardRef(function GlobeScene(
  {
    entities = [],
    routes = [],
    selectedId = null,
    autoRotate = true,
    onNodeClick,
    onNodeHover,
    onBackgroundClick,
  },
  ref
) {
  const [containerRef, { width, height }] = useElementSize()
  const globeApi = useRef(null)
  const readyRef = useRef(false)
  const initializedRef = useRef(false)
  const resumeTimerRef = useRef(null)
  const [countries, setCountries] = useState([])

  // Real country boundaries (Natural Earth via world-atlas), fetched once
  // in the user's browser at runtime — this is what turns the globe from
  // "lat/long grid" into something people can actually orient themselves on.
  useEffect(() => {
    let cancelled = false

    async function loadCountries() {
      const candidates = [
        'https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json',
        'https://unpkg.com/world-atlas@2.0.2/countries-110m.json',
        'https://unpkg.com/world-atlas@2/countries-110m.json',
      ]
      for (const url of candidates) {
        try {
          const res = await fetch(url)
          if (!res.ok) throw new Error(`${url} -> HTTP ${res.status}`)
          const world = await res.json()
          if (cancelled) return
          const geo = feature(world, world.objects.countries)
          setCountries(geo.features)
          // eslint-disable-next-line no-console
          console.info(`[ChainMind] loaded ${geo.features.length} country boundaries from ${url}`)
          return
        } catch (err) {
          // eslint-disable-next-line no-console
          console.warn(`[ChainMind] country boundary fetch failed for ${url}:`, err)
        }
      }
      // eslint-disable-next-line no-console
      console.error(
        '[ChainMind] Could not load country boundaries from any source — falling back to graticule-only globe.'
      )
    }

    loadCountries()
    return () => {
      cancelled = true
    }
  }, [])

  useImperativeHandle(ref, () => ({
    flyTo(entity, altitude = 0.45) {
      if (!globeApi.current || !entity) return
      globeApi.current.controls().autoRotate = false
      globeApi.current.pointOfView({ lat: entity.lat, lng: entity.lng, altitude }, 1100)
    },
    reset() {
      if (!globeApi.current) return
      globeApi.current.pointOfView({ lat: 18, lng: 60, altitude: 2.1 }, 900)
      globeApi.current.controls().autoRotate = autoRotate
    },
  }))

  useEffect(() => {
    if (!globeApi.current || width === 0) return
    const controls = globeApi.current.controls()
    controls.autoRotate = autoRotate
    controls.autoRotateSpeed = 0.45
    controls.enableZoom = true
    controls.minDistance = 160
    // only snap the camera to the default view once — resizing the
    // window (or a sidebar toggling) shouldn't yank the view away from
    // wherever the user has it rotated to
    if (!initializedRef.current) {
      initializedRef.current = true
      globeApi.current.pointOfView({ lat: 18, lng: 60, altitude: 2.1 })
    }
  }, [width, height, autoRotate])

  // Auto-rotate should spin on its own, but the instant a user grabs the
  // globe it should feel like *their* drag, in whatever direction they
  // move — not a fight against the auto-rotation still running underneath.
  function handleGlobeReady() {
    if (readyRef.current || !globeApi.current) return
    readyRef.current = true
    const controls = globeApi.current.controls()
    controls.addEventListener('start', () => {
      controls.autoRotate = false
    })
    controls.addEventListener('end', () => {
      clearTimeout(resumeTimerRef.current)
      resumeTimerRef.current = setTimeout(() => {
        controls.autoRotate = autoRotate
      }, 1400)
    })
  }

  const globeMaterial = useMemo(() => {
    const mat = new THREE.MeshPhongMaterial()
    mat.color = new THREE.Color('#0a1b13')
    mat.emissive = new THREE.Color('#04120a')
    mat.emissiveIntensity = 0.35
    mat.shininess = 6
    return mat
  }, [])

  // const arcsData = useMemo(
  //   () =>
  //     routes
  //       .map((r) => {
  //         const s = entityById[r.startId]
  //         const e = entityById[r.endId]
  //         if (!s || !e) return null
  //         return {
  //           id: r.id,
  //           startLat: s.lat,
  //           startLng: s.lng,
  //           endLat: e.lat,
  //           endLng: e.lng,
  //           color: ROUTE_COLOR[r.kind] || ROUTE_COLOR.shipping,
  //           kind: r.kind,
  //         }
  //       })
  //       .filter(Boolean),
  //   [routes]
  // )

  const arcsData = useMemo(() => {
    // 1. Create a lookup map from the LIVE entities passed from the backend
    const entityMap = {}
    entities.forEach((e) => {
      entityMap[e.id] = e
    })

    // 2. Map the routes using the live data
    return routes
      .map((r) => {
        const s = entityMap[r.startId]
        const e = entityMap[r.endId]
        if (!s || !e) return null
        return {
          id: r.id,
          startLat: s.lat,
          startLng: s.lng,
          endLat: e.lat,
          endLng: e.lng,
          color: ROUTE_COLOR[r.kind] || ROUTE_COLOR.shipping,
          kind: r.kind,
        }
      })
      .filter(Boolean)
  }, [routes, entities])

  const ringsData = useMemo(
    () =>
      entities
        .filter((e) => e.status === 'critical')
        .map((e) => ({ ...e, color: STATUS_COLOR.critical })),
    [entities]
  )

  // average risk per country, keyed by every spelling that country might
  // show up as in the topojson — this is what colors the "industrial areas"
  const riskByGeoName = useMemo(() => {
    const acc = {}
    entities.forEach((e) => {
      const variants = COUNTRY_NAME_VARIANTS[e.country] || [e.country]
      variants.forEach((name) => {
        if (!acc[name]) acc[name] = { sum: 0, count: 0 }
        acc[name].sum += e.risk_score
        acc[name].count += 1
      })
    })
    const out = {}
    Object.entries(acc).forEach(([name, { sum, count }]) => {
      out[name] = sum / count
    })
    return out
  }, [entities])

  function handlePolygonClick(feat) {
    const match = entities.find((e) => {
      const variants = COUNTRY_NAME_VARIANTS[e.country] || [e.country]
      return variants.includes(feat.properties.name)
    })
    if (match) onNodeClick && onNodeClick(match)
  }

  return (
    <div ref={containerRef} className="globe-canvas">
      {width > 0 && (
        <Globe
          ref={globeApi}
          width={width}
          height={height}
          backgroundColor="rgba(0,0,0,0)"
          globeMaterial={globeMaterial}
          showAtmosphere
          atmosphereColor="#4ff2a0"
          atmosphereAltitude={0.16}
          showGraticules
          onGlobeReady={handleGlobeReady}
          polygonsData={countries}
          polygonCapColor={(feat) => riskFillColor(riskByGeoName[feat.properties.name])}
          polygonSideColor={() => 'rgba(6, 9, 7, 0.35)'}
          polygonStrokeColor={() => '#1c3628'}
          polygonAltitude={0.006}
          polygonsTransitionDuration={900}
          polygonLabel={(feat) => {
            const risk = riskByGeoName[feat.properties.name]
            return `
              <div style="
                font-family: 'IBM Plex Mono', monospace;
                background: #0c1e16;
                border: 1px solid #2a4f3a;
                border-radius: 8px;
                padding: 8px 11px;
                color: #e9f4ee;
                font-size: 12px;
                max-width: 200px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.45);
              ">
                <div style="font-size:12.5px; font-weight:600;">${feat.properties.name}</div>
                ${
                  risk != null
                    ? `<div style="margin-top:4px;">avg risk_score <b style="color:${
                        risk >= 0.65 ? '#ff4d5e' : risk >= 0.4 ? '#f5a623' : '#4ff2a0'
                      }">${risk.toFixed(2)}</b></div>`
                    : ''
                }
              </div>
            `
          }}
          onPolygonClick={handlePolygonClick}
          pointsData={entities}
          pointLat="lat"
          pointLng="lng"
          pointColor={(d) => (d.id === selectedId ? '#e9f4ee' : STATUS_COLOR[d.status] || STATUS_COLOR.ok)}
          pointAltitude={(d) => (d.id === selectedId ? 0.05 : 0.012)}
          pointRadius={(d) => (d.id === selectedId ? 0.65 : d.status === 'critical' ? 0.5 : 0.36)}
          pointResolution={16}
          pointLabel={(d) => `
            <div style="
              font-family: 'IBM Plex Mono', monospace;
              background: #0c1e16;
              border: 1px solid #2a4f3a;
              border-radius: 8px;
              padding: 10px 12px;
              color: #e9f4ee;
              font-size: 12px;
              max-width: 220px;
              box-shadow: 0 8px 24px rgba(0,0,0,0.45);
            ">
              <div style="color:#4ff2a0; font-size:10px; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:4px;">${d.type} · ${d.country}</div>
              <div style="font-size:13px; font-weight:600; margin-bottom:6px;">${d.name}</div>
              <div>risk_score <b style="color:${STATUS_COLOR[d.status]}">${d.risk_score.toFixed(2)}</b></div>
              <div style="color:#8fac9f; margin-top:2px;">click to zoom in →</div>
            </div>
          `}
          onPointClick={(d) => onNodeClick && onNodeClick(d)}
          onPointHover={(d) => onNodeHover && onNodeHover(d)}
          ringsData={ringsData}
          ringLat="lat"
          ringLng="lng"
          ringColor={() => (t) => `rgba(255, 77, 94, ${1 - t})`}
          ringMaxRadius={3.2}
          ringPropagationSpeed={2.4}
          ringRepeatPeriod={1000}
          arcsData={arcsData}
          arcColor="color"
          arcAltitude={0.22}
          arcStroke={0.42}
          arcDashLength={0.4}
          arcDashGap={0.6}
          arcDashAnimateTime={2600}
          onGlobeClick={() => onBackgroundClick && onBackgroundClick()}
        />
      )}
    </div>
  )
})

export default GlobeScene
