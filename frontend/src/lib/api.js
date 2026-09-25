const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

async function request(path, options = {}) {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.detail || `Request failed: ${res.status}`)
  }
  return res.json()
}

export function getEntities() {
  return request('/api/entities')
}
export function getAlerts(limit = 20) {
  return request(`/api/alerts?limit=${limit}`)
}
export function getMaterials() {
  return request('/api/materials')
}
export function getGraphRisk(targetEntity = 'TSMC') {
  return request(`/api/graph-risk?target_entity=${encodeURIComponent(targetEntity)}`)
}
export function postScenario(disruptedNode, targetNode = 'Apple') {
  return request('/api/scenario', {
    method: 'POST',
    body: JSON.stringify({ disrupted_node: disruptedNode, target_node: targetNode }),
  })
}
export function postChat(query, context = {}) {
  return request('/api/chat', {
    method: 'POST',
    body: JSON.stringify({ query, context }),
  })
}

// your backend returns full ISO timestamps, not "11m ago" — this bridges that
export function timeAgo(isoString) {
  if (!isoString) return ''
  const mins = Math.round((Date.now() - new Date(isoString).getTime()) / 60000)
  if (mins < 1) return 'just now'
  if (mins < 60) return `${mins}m ago`
  const hrs = Math.round(mins / 60)
  if (hrs < 24) return `${hrs}h ago`
  return `${Math.round(hrs / 24)}d ago`
}