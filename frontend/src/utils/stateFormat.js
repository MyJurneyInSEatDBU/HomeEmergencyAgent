export function makeInitialState() {
  return {
    emergency: 'none',
    phase: 'idle',
    last_action: 'none',
    last_message: 'none',
    fire_intensity: 0,
    flood_level: 0,
    materials_inside: 0,
    materials_outside: 0,
    drone: { x: 26, y: 180, target_x: 26, target_y: 180, status: 'idle' },
    metrics: { water_cycles: 0, evac_cycles: 0 },
    logs: [],
  }
}

export function getStatusClass(emergency) {
  if (emergency === 'fire') return 'status-fire'
  if (emergency === 'flood') return 'status-flood'
  return 'status-normal'
}

export function getAlarmText(emergency) {
  if (emergency === 'fire') return 'HELP HELP - FIRE DETECTED'
  if (emergency === 'flood') return 'HELP HELP - FLOOD DETECTED'
  return ''
}
