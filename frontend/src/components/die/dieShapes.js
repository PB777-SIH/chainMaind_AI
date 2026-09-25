// Regions render as etched "die" silhouettes instead of literal
// cartography — every shape below is procedurally generated from a
// seed string, so it's original artwork, not traced map data.

function hashSeed(str) {
  let h = 0
  for (let i = 0; i < str.length; i++) {
    h = (h * 31 + str.charCodeAt(i)) | 0
  }
  return h
}

function mulberry32(seed) {
  let s = seed
  return function () {
    s |= 0
    s = (s + 0x6d2b79f5) | 0
    let t = Math.imul(s ^ (s >>> 15), 1 | s)
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}

export function blobPath(seed, opts = {}) {
  const { points = 12, size = 150, irregularity = 0.38, cx = 200, cy = 200 } = opts
  const rand = mulberry32(hashSeed(seed))
  const angleStep = (Math.PI * 2) / points
  const pts = []
  for (let i = 0; i < points; i++) {
    const angle = i * angleStep
    const r = size * (1 - irregularity / 2 + rand() * irregularity)
    pts.push([cx + Math.cos(angle) * r, cy + Math.sin(angle) * r])
  }
  let d = `M ${pts[0][0].toFixed(1)} ${pts[0][1].toFixed(1)} `
  for (let i = 0; i < points; i++) {
    const curr = pts[i]
    const next = pts[(i + 1) % points]
    const mid = [(curr[0] + next[0]) / 2, (curr[1] + next[1]) / 2]
    d += `Q ${curr[0].toFixed(1)} ${curr[1].toFixed(1)} ${mid[0].toFixed(1)} ${mid[1].toFixed(1)} `
  }
  d += 'Z'
  return d
}

// deterministic scatter of points inside the die, used to place
// facility markers without pretending to be real coordinates
export function scatterPoints(seed, count, { cx = 200, cy = 200, radius = 110 } = {}) {
  const rand = mulberry32(hashSeed(seed + '-scatter'))
  const out = []
  for (let i = 0; i < count; i++) {
    const angle = rand() * Math.PI * 2
    const r = Math.sqrt(rand()) * radius
    out.push([cx + Math.cos(angle) * r, cy + Math.sin(angle) * r])
  }
  return out
}

export function tracePaths(seed, count = 6, { cx = 200, cy = 200, size = 150 } = {}) {
  const rand = mulberry32(hashSeed(seed + '-trace'))
  const lines = []
  for (let i = 0; i < count; i++) {
    const angle = rand() * Math.PI * 2
    const r1 = size * 0.15
    const r2 = size * (0.55 + rand() * 0.4)
    const bendAngle = angle + (rand() - 0.5) * 0.6
    const bendR = (r1 + r2) / 2
    lines.push({
      x1: cx + Math.cos(angle) * r1,
      y1: cy + Math.sin(angle) * r1,
      xb: cx + Math.cos(bendAngle) * bendR,
      yb: cy + Math.sin(bendAngle) * bendR,
      x2: cx + Math.cos(angle) * r2,
      y2: cy + Math.sin(angle) * r2,
    })
  }
  return lines
}
