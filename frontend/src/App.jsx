import { useMemo } from 'react'
import { EmergencyControls } from './components/EmergencyControls'
import { AgentScene } from './components/AgentScene'
import { LogPanel } from './components/LogPanel'
import { useEmergencyAgent } from './hooks/useEmergencyAgent'
import { useAlarm } from './hooks/useAlarm'
import { getAlarmText, getStatusClass } from './utils/stateFormat'

export default function App() {
  const { state, actions } = useEmergencyAgent()
  useAlarm(state.emergency)

  const statusClass = useMemo(() => getStatusClass(state.emergency), [state.emergency])
  const alarmText = useMemo(() => getAlarmText(state.emergency), [state.emergency])

  return (
    <div className="app-shell">
      <h1 className="hero-title">Home Emergency Agent</h1>
      <p className="hero-subtitle">Status-aware response for fire and flood with live cleanup animation.</p>
      <div className="app-grid">
        <EmergencyControls
          emergency={state.emergency}
          phase={state.phase}
          fireIntensity={state.fire_intensity}
          floodLevel={state.flood_level}
          materialsInside={state.materials_inside}
          materialsOutside={state.materials_outside}
          statusClass={statusClass}
          alarmActive={state.emergency !== 'none'}
          alarmText={alarmText}
          onEmergencyChange={actions.onEmergencyChange}
        />

        <AgentScene
          emergency={state.emergency}
          phase={state.phase}
          drone={state.drone}
          fireIntensity={state.fire_intensity}
          floodLevel={state.flood_level}
          materialsInside={state.materials_inside}
          materialsOutside={state.materials_outside}
        />
       
        <LogPanel logs={state.logs} />
      </div>
    </div>
  )
}
