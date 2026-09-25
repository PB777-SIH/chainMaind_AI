import { useMemo, useState } from 'react'
import { motion } from 'framer-motion'
import { X } from 'lucide-react'
import { blobPath, scatterPoints, tracePaths } from './dieShapes'
import { dieRegions } from '../../lib/regionData'
import './DieSilhouette.css'

const STATUS_COLOR = { ok: '#4ff2a0', warn: '#f5a623', critical: '#ff4d5e' }

export default function DieSilhouette({ regionKey, entities, onClose }) {
  const [tab, setTab] = useState('facilities')
  const region = dieRegions[regionKey]
  const regionEntities = useMemo(
    () => (entities || []).filter((e) => e.region === regionKey),
    [entities, regionKey]
  )
  const path = useMemo(() => blobPath(regionKey), [regionKey])
  const traces = useMemo(() => tracePaths(regionKey, 7), [regionKey])
  const scatter = useMemo(() => scatterPoints(regionKey, regionEntities.length), [regionKey, regionEntities.length])

  if (!region) return null
  const avgRisk = regionEntities.reduce((sum, e) => sum + e.risk_score, 0) / (regionEntities.length || 1)

  return (
    <motion.div className="die-panel" initial={{ opacity: 0, scale: 0.94, y: 12 }} animate={{ opacity: 1, scale: 1, y: 0 }} exit={{ opacity: 0, scale: 0.96, y: 8 }} transition={{ duration: 0.35, ease: [0.16, 1, 0.3, 1] }}>
      <button className="die-close" onClick={onClose} aria-label="Close region view"><X size={16} /></button>
      <div className="die-header">
        <div className="eyebrow">{region.node}</div>
        <h3>{region.label}</h3>
      </div>
      <div className="die-body">
        <div className="die-art">
          <svg viewBox="0 0 400 400" className="die-svg">
            <defs>
              <radialGradient id={`grad-${regionKey}`} cx="50%" cy="45%" r="65%">
                <stop offset="0%" stopColor="rgba(79,242,160,0.22)" />
                <stop offset="100%" stopColor="rgba(79,242,160,0.02)" />
              </radialGradient>
            </defs>
            <path d={path} fill={`url(#grad-${regionKey})`} stroke="#4ff2a0" strokeWidth="1.4" />
            {traces.map((t, i) => (
              <path key={i} d={`M ${t.x1} ${t.y1} Q ${t.xb} ${t.yb} ${t.x2} ${t.y2}`} fill="none" stroke="rgba(79,242,160,0.35)" strokeWidth="1" />
            ))}
            {regionEntities.map((e, i) => {
              const [x, y] = scatter[i] || [200, 200]
              return (
                <g key={e.id}>
                  <circle cx={x} cy={y} r="9" fill={STATUS_COLOR[e.status]} opacity="0.18" />
                  <circle cx={x} cy={y} r="4" fill={STATUS_COLOR[e.status]} />
                </g>
              )
            })}
          </svg>
          <div className="die-stat">
            <span className="die-stat-label">avg risk_score</span>
            <span className="die-stat-value mono">{avgRisk.toFixed(2)}</span>
          </div>
        </div>
        <div className="die-info">
          <div className="die-tabs">
            <button className={tab === 'facilities' ? 'active' : ''} onClick={() => setTab('facilities')}>Facilities</button>
            <button className={tab === 'timeline' ? 'active' : ''} onClick={() => setTab('timeline')}>Timeline</button>
          </div>
          {tab === 'facilities' ? (
            <ul className="die-list">
              {regionEntities.map((e) => (
                <li key={e.id}>
                  <span className={`status-dot ${e.status}`} />
                  <span className="die-list-name">{e.name}</span>
                  <span className="die-list-type mono">{e.type}</span>
                  <span className="die-list-risk mono">{e.risk_score.toFixed(2)}</span>
                </li>
              ))}
            </ul>
          ) : (
            <ul className="die-timeline">
              {region.events.map((ev, i) => (
                <li key={i}>
                  <span className="die-timeline-year mono">{ev.year}</span>
                  <span className="die-timeline-text">{ev.text}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </motion.div>
  )
}