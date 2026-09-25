import { motion } from 'framer-motion'
import { Line, LineChart, ResponsiveContainer } from 'recharts'
import './StatsGrid.css'

function colorFor(status) {
  if (status === 'critical') return '#ff4d5e'
  if (status === 'warn') return '#f5a623'
  return '#4ff2a0'
}

export default function StatsGrid({ materials, graphRisk }) {
  return (
    <div className="stats-grid">
      {materials.map((m, i) => {
        const data = m.series.map((v, idx) => ({ idx, v }))
        const color = colorFor(m.status)
        return (
          <motion.div
            key={m.ticker}
            className="stat-card"
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.45, delay: i * 0.06 }}
          >
            <div className="stat-card-top">
              <div>
                <div className="mono stat-ticker">{m.ticker}</div>
                <div className="stat-name">{m.name}</div>
              </div>
              <div className={`stat-pct mono ${m.pct_change >= 0 ? 'up' : 'down'}`}>
                {m.pct_change >= 0 ? '+' : ''}
                {m.pct_change.toFixed(1)}%
              </div>
            </div>

            <div className="stat-spark">
              <ResponsiveContainer width="100%" height={44}>
                <LineChart data={data}>
                  <Line
                    type="monotone"
                    dataKey="v"
                    stroke={color}
                    strokeWidth={2}
                    dot={false}
                    isAnimationActive={false}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>

            <div className="stat-bars">
              <div className="stat-bar-row">
                <span>scarcity index</span>
                <div className="stat-bar-track">
                  <div
                    className="stat-bar-fill"
                    style={{ width: `${m.commodity_scarcity_index * 100}%`, background: color }}
                  />
                </div>
                <span className="mono">{m.commodity_scarcity_index.toFixed(2)}</span>
              </div>
              <div className="stat-bar-row">
                <span>econ score</span>
                <div className="stat-bar-track">
                  <div
                    className="stat-bar-fill"
                    style={{ width: `${m.econ_score * 100}%`, background: 'var(--ink-faint)' }}
                  />
                </div>
                <span className="mono">{m.econ_score.toFixed(2)}</span>
              </div>
            </div>
          </motion.div>
        )
      })}

      <motion.div
        className="stat-card fused-card"
        initial={{ opacity: 0, y: 16 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        transition={{ duration: 0.45, delay: materials.length * 0.06 }}
      >
        <div className="eyebrow">fusion_engine.py</div>
        <div className="fused-score mono">{graphRisk.total_fused_risk.toFixed(2)}</div>
        <div className="stat-name">Total fused risk score</div>
        <div className="fused-weights">
          {Object.entries(graphRisk.weights).map(([k, v]) => (
            <div key={k} className="fused-weight-row">
              <span>{k}</span>
              <div className="stat-bar-track">
                <div className="stat-bar-fill" style={{ width: `${v * 100}%`, background: 'var(--signal)' }} />
              </div>
              <span className="mono">{Math.round(v * 100)}%</span>
            </div>
          ))}
        </div>
      </motion.div>
    </div>
  )
}
