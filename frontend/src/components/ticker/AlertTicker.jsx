import { motion } from 'framer-motion'
import { timeAgo } from '../../lib/api'
import './AlertTicker.css'

function severity(score) {
  if (score >= 0.65) return 'critical'
  if (score >= 0.4) return 'warn'
  return 'ok'
}

export default function AlertTicker({ alerts, onSelect }) {
  return (
    <div className="ticker">
      <div className="ticker-head">
        <span className="status-dot critical" />
        <span className="eyebrow">Live intelligence feed</span>
      </div>
      <div className="ticker-list">
        {alerts.map((a, i) => {
          const sev = severity(a.impact_score)
          return (
            <motion.button key={a.id} className={`ticker-item sev-${sev}`} onClick={() => onSelect && onSelect(a)}
              initial={{ opacity: 0, x: -12 }} whileInView={{ opacity: 1, x: 0 }} viewport={{ once: true }} transition={{ duration: 0.4, delay: i * 0.05 }}>
              <div className="ticker-item-top">
                <span className="ticker-entity mono">{a.primary_entity}</span>
                <span className="ticker-time mono">{timeAgo(a.timestamp)}</span>
              </div>
              <div className="ticker-type">{a.event_type}</div>
              <p className="ticker-summary">{a.summary}</p>
              <div className="ticker-impact">
                <div className="ticker-impact-track">
                  <div className="ticker-impact-fill" style={{ width: `${a.impact_score * 100}%` }} />
                </div>
                <span className="mono ticker-impact-value">{a.impact_score.toFixed(2)}</span>
              </div>
            </motion.button>
          )
        })}
      </div>
    </div>
  )
}