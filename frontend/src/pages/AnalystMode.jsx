import { useEffect, useRef, useState } from 'react'
import { AnimatePresence } from 'framer-motion'
import GlobeScene from '../components/globe/GlobeScene'
import DieSilhouette from '../components/die/DieSilhouette'
import ChatPanel from '../components/chat/ChatPanel'
import { getEntities, getMaterials, getGraphRisk } from '../lib/api'
import { regionSlugForCountry } from '../lib/regionData'
import './AnalystMode.css'
import BackHomeButton from '../components/layout/BackHomeButton'

export default function AnalystMode() {
  const globeRef = useRef(null)
  const [activeRegion, setActiveRegion] = useState(null)
  const [selectedId, setSelectedId] = useState(null)
  const [contextLabel, setContextLabel] = useState(null)
  const [entities, setEntities] = useState([])
  const [materials, setMaterials] = useState([])
  const [graphRisk, setGraphRisk] = useState(null)

  useEffect(() => {
    let cancelled = false
    async function load() {
      try {
        const [entitiesRes, materialsRes, graphRiskRes] = await Promise.all([
          getEntities(), getMaterials(), getGraphRisk('TSMC'),
        ])
        if (cancelled) return
        setEntities(entitiesRes.map((e) => ({ ...e, region: regionSlugForCountry(e.country) })))
        setMaterials(materialsRes)
        setGraphRisk(graphRiskRes)
      } catch (err) {
        console.error('[ChainMind] Analyst Mode failed to load live data:', err)
      }
    }
    load()
    return () => { cancelled = true }
  }, [])

  function handleNodeClick(entity) {
    setSelectedId(entity.id)
    setActiveRegion(entity.region)
    setContextLabel(entity.name)
    globeRef.current?.flyTo(entity)
  }

  function closeRegion() {
    setActiveRegion(null)
    setSelectedId(null)
    globeRef.current?.reset()
  }

  function handleAssistantReply(result) {
    setContextLabel(result?.current_node_context || null)
    if (!result?.current_node_context) return
    const match = entities.find((e) => e.name.toLowerCase() === result.current_node_context.toLowerCase())
    if (match) {
      setSelectedId(match.id)
      globeRef.current?.flyTo(match, 1.1)
    }
  }

  return (
    <div className="analyst">
      <div className="analyst-chat">
        <ChatPanel 
          getContext={() => ({ 
            current_node_context: contextLabel,
            total_fused_risk: graphRisk?.total_fused_risk,
            materials: materials,
            active_entity_data: entities.find(e => e.name === contextLabel) || null,
            system_entities: entities.map(e => ({ name: e.name, status: e.status, risk: e.risk_score }))
          })} 
          onAssistantReply={handleAssistantReply} 
        />
      </div>
      <div className="analyst-right">
        <div className="analyst-context-bar">
          <span className="eyebrow">current_node_context</span>
          <span className="mono context-value">{contextLabel || 'global — no node selected'}</span>
        </div>
        <div className="analyst-globe">
          <GlobeScene ref={globeRef} entities={entities} routes={[]} selectedId={selectedId} onNodeClick={handleNodeClick} onBackgroundClick={closeRegion} />
          <AnimatePresence>
            {activeRegion && <DieSilhouette regionKey={activeRegion} entities={entities} onClose={closeRegion} />}
          </AnimatePresence>
        </div>
        <div className="analyst-mini-stats">
          <div className="mini-stat">
            <span className="eyebrow">total_fused_risk</span>
            <span className="mono mini-stat-value">{graphRisk ? graphRisk.total_fused_risk.toFixed(2) : '—'}</span>
          </div>
          {materials.slice(0, 4).map((m) => (
            <div className="mini-stat" key={m.ticker}>
              <span className="eyebrow">{m.ticker}</span>
              <span className={`mono mini-stat-value ${m.pct_change >= 0 ? 'up' : 'down'}`}>{m.pct_change >= 0 ? '+' : ''}{m.pct_change.toFixed(1)}%</span>
            </div>
          ))}
        </div>
      </div>
      <BackHomeButton />
    </div>
  )
}