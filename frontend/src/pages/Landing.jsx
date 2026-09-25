import { useEffect, useMemo, useRef, useState } from 'react'
import { Link } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { ArrowRight, MousePointerClick } from 'lucide-react'
import GlobeScene from '../components/globe/GlobeScene'
import DieSilhouette from '../components/die/DieSilhouette'
import AlertTicker from '../components/ticker/AlertTicker'
import ChatPanel from '../components/chat/ChatPanel'
import StatsGrid from '../components/stats/StatsGrid'
import { getEntities, getAlerts, getMaterials, getGraphRisk, postScenario } from '../lib/api'
import { regionSlugForCountry } from '../lib/regionData'
import './Landing.css'

export default function Landing() {
  const globeRef = useRef(null)
  const heroRef = useRef(null)
  const [activeRegion, setActiveRegion] = useState(null)
  const [selectedId, setSelectedId] = useState(null)
  const [selectedName, setSelectedName] = useState(null)

  const [entities, setEntities] = useState([])
  const [alerts, setAlerts] = useState([])
  const [materials, setMaterials] = useState([])
  const [graphRisk, setGraphRisk] = useState(null)
  const [scenario, setScenario] = useState(null)
  const [loading, setLoading] = useState(true)
  const [loadError, setLoadError] = useState(null)

  useEffect(() => {
    let cancelled = false
    async function load() {
      try {
        const [entitiesRes, alertsRes, materialsRes, graphRiskRes, scenarioRes] = await Promise.all([
          getEntities(), getAlerts(20), getMaterials(), getGraphRisk('TSMC'),
          postScenario('TSMC', 'Apple').catch(() => null),
        ])
        if (cancelled) return
        setEntities(entitiesRes.map((e) => ({ ...e, region: regionSlugForCountry(e.country) })))
        setAlerts(alertsRes)
        setMaterials(materialsRes)
        setGraphRisk(graphRiskRes)
        setScenario(scenarioRes)
      } catch (err) {
        if (!cancelled) setLoadError(err.message)
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    load()
    return () => { cancelled = true }
  }, [])

  function handleNodeClick(entity) {
    setSelectedId(entity.id)
    setSelectedName(entity.name)
    setActiveRegion(entity.region)
    globeRef.current?.flyTo(entity)
  }

  function closeRegion() {
    setActiveRegion(null)
    setSelectedId(null)
    globeRef.current?.reset()
  }

  function handleAlertSelect(alert) {
    const match = entities.find((e) => e.name.toLowerCase().includes(alert.primary_entity.toLowerCase()))
    if (match) {
      heroRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' })
      handleNodeClick(match)
    }
  }

  function handleAssistantReply(result) {
    if (!result?.current_node_context) return
    const match = entities.find((e) => e.name.toLowerCase() === result.current_node_context.toLowerCase())
    if (match) {
      setSelectedId(match.id)
      setSelectedName(match.name)
      globeRef.current?.flyTo(match, 0.9)
      setTimeout(() => globeRef.current?.reset(), 4500)
    }
  }

  if (loadError) {
    return (
      <div style={{ padding: 60, color: 'var(--ink)' }}>
        <p>Couldn't reach the ChainMind backend ({loadError}).</p>
        <p className="mono">Check uvicorn is running and VITE_API_URL is set correctly.</p>
      </div>
    )
  }

  return (
    <div className="landing">
      <section className="hero" ref={heroRef}>
        <div className="hero-copy">
          <div className="eyebrow">Multi-modal supply chain risk intelligence</div>
          <h1>See the risk<br />before it ships.</h1>
          <p>ChainMind AI fuses geopolitical signal, graph topology, commodity volatility, and satellite verification into one live risk score for the global semiconductor supply chain — then simulates the reroute before the disruption finishes making headlines.</p>
          <div className="hero-actions">
            <Link to="/analyst" className="btn-primary">Enter Analyst Mode <ArrowRight size={15} /></Link>
            <span className="hero-hint"><MousePointerClick size={14} /> drag the globe · click a node to zoom in</span>
          </div>
          <div className="hero-legend">
            <span><span className="status-dot ok" /> nominal</span>
            <span><span className="status-dot warn" /> elevated</span>
            <span><span className="status-dot critical" /> critical</span>
          </div>
        </div>

        <div className="hero-globe">
          <GlobeScene ref={globeRef} entities={entities} routes={[]} selectedId={selectedId} onNodeClick={handleNodeClick} onBackgroundClick={closeRegion} />
        </div>

        <div className="hero-region-slot">
          <AnimatePresence>
            {activeRegion && <DieSilhouette regionKey={activeRegion} entities={entities} onClose={closeRegion} />}
          </AnimatePresence>
        </div>
      </section>

      <section className="split-section">
        <div className="split-col">
          <AlertTicker alerts={alerts} onSelect={handleAlertSelect} />
        </div>
        <div className="split-col chat-col">
          <ChatPanel getContext={() => ({ current_node_context: selectedName })} onAssistantReply={handleAssistantReply} />
        </div>
      </section>

      <section className="stats-section">
        <div className="section-heading">
          <div className="eyebrow">market_tracker.py · fusion_engine.py</div>
          <h2>Materials, markets, and the fused score</h2>
        </div>
        {graphRisk && <StatsGrid materials={materials} graphRisk={graphRisk} />}
      </section>

      {scenario && (
        <section className="reroute-section">
          <motion.div className="reroute-card" initial={{ opacity: 0, y: 20 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true }} transition={{ duration: 0.5 }}>
            <div className="reroute-left">
              <div className="eyebrow">optimizer.py · scenario result</div>
              <h2>TSMC disrupted → Apple's production forecast</h2>
              <p>Running <code className="mono">run_what_if_scenario(disrupted_node="TSMC", target_node="Apple")</code> against the live graph returns <strong>{scenario.optimal_reroute.name}</strong> ({scenario.optimal_reroute.region}) as the lowest-penalty reroute.</p>
              <Link to="/analyst" className="btn-secondary">Run your own scenario <ArrowRight size={14} /></Link>
            </div>
            <div className="reroute-right">
              <div className="reroute-row header"><span></span><span>supplier</span><span>cost×</span><span>geo risk</span><span>penalty</span></div>
              {scenario.alternatives.map((alt, i) => (
                <div key={alt.name} className={`reroute-row ${i === 0 ? 'best' : ''}`}>
                  <span className="reroute-rank mono">{String(i + 1).padStart(2, '0')}</span>
                  <span className="reroute-name">{alt.name}</span>
                  <span className="mono reroute-metric">×{alt.cost_multiplier.toFixed(2)}</span>
                  <span className="mono reroute-metric">{alt.geo_risk.toFixed(2)}</span>
                  <span className="mono reroute-penalty">{alt.penalty_score.toFixed(2)}</span>
                </div>
              ))}
            </div>
          </motion.div>
        </section>
      )}

      <footer className="footer">
        <span className="mono">{loading ? 'Syncing with live backend…' : 'CHAINMIND AI — Phase 1–6 fused into one interface.'}</span>
      </footer>
    </div>
  )
}