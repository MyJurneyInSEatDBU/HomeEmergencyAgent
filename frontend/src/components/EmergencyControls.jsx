const emergencyOptions = [
  { value: 'none', label: 'None' },
  { value: 'fire', label: 'Fire' },
  { value: 'flood', label: 'Flood' },
]
export function EmergencyControls({
  emergency,
  phase,
  fireIntensity,
  floodLevel,
  materialsInside,
  materialsOutside,
  statusClass,
  alarmActive,
  alarmText,
  onEmergencyChange,
}) {
  return (
    <section className="panel controls-panel">
      <h2 className="title">Emergency Input</h2>

      <label className="field-label" htmlFor="status-select">Status</label>
      <div className="status-row">
        <select
          id="status-select"
          className="status-select"
          value={emergency}
          onChange={(e) => onEmergencyChange(e.target.value)}
        >
          {emergencyOptions.map((option) => (
            <option key={option.value} value={option.value}>{option.label}</option>
          ))}
        </select>
        <span className={`status-pill ${statusClass}`}>{emergency}</span>
      </div>
      {alarmActive && <div className="alarm">{alarmText}</div>}
      <div className="phase-box">Agent phase: <strong>{phase}</strong></div>

      <div className="meter-wrap">
        <div className="meter-row">
          <span>Fire intensity</span>
          <span>{fireIntensity}%</span>
        </div>
        <div className="meter">
          <div className="meter-fill meter-fire" style={{ width: `${fireIntensity}%` }} />
        </div>
      </div>

      <div className="meter-wrap">
        <div className="meter-row">
          <span>Flood level</span>
          <span>{floodLevel}%</span>
        </div>
        <div className="meter">
          <div className="meter-fill meter-flood" style={{ width: `${floodLevel}%` }} />
        </div>
      </div>

      <div className="material-count">
        Materials inside: {materialsInside} | outside: {materialsOutside}
      </div>
    </section>
  )
}
