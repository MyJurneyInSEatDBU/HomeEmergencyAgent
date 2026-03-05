const API = '/api'
async function request(path, options = {}) {
  const res = await fetch(`${API}${path}`, options)
  return res.json()
}
export function getState() {
  return request('/state')
}
export function detectEmergency(emergency) {
  return request('/detect', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ emergency }),
  })
}
