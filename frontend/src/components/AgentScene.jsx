export function AgentScene({
  emergency,
  phase,
  drone,
  fireIntensity,
  floodLevel,
  materialsInside,
  materialsOutside,
}) {
  const shownInside = Math.min(6, materialsInside)
  const shownOutside = Math.min(6, materialsOutside)
  const flameOpacity = Math.max(0.2, fireIntensity / 100)
  const waveOpacity = Math.max(0.2, floodLevel / 100)

  return (
    <section className="panel scene-panel">
      <h2 className="title">Agent Actions</h2>
      <p className="scene-caption">
        Fire triggers suppression and cleanup. Flood triggers evacuation and local material removal.
      </p>

      <div
        className={`scene ${emergency === 'fire' ? 'scene-fire' : ''} ${emergency === 'flood' ? 'scene-flood' : ''}`}
      >
        <div className="home">
          <div className="roof" />
          <div className="body">
            <div className="door" />
          </div>
        </div>

        {fireIntensity > 0 && (
          <div className="flames" style={{ opacity: flameOpacity }}>
            <span className="flame flame-1" />
            <span className="flame flame-2" />
            <span className="flame flame-3" />
          </div>
        )}

        {floodLevel > 0 && (
          <div className="waves" style={{ opacity: waveOpacity }}>
            <span className="wave wave-1" />
            <span className="wave wave-2" />
            <span className="wave wave-3" />
          </div>
        )}

        <div className={`materials ${phase === 'clearing_materials' ? 'materials-clearing' : ''}`}>
          {Array.from({ length: shownInside }).map((_, idx) => (
            <span key={`inside-${idx}`} className={`crate crate-in crate-${idx + 1}`} />
          ))}
        </div>

        <div className="outside-materials">
          {Array.from({ length: shownOutside }).map((_, idx) => (
            <span key={`outside-${idx}`} className={`crate crate-out out-${idx + 1}`} />
          ))}
        </div>

        <div className="drone-dot" style={{ left: drone.x, top: drone.y }} />
      </div>
      <small className="hint">Drone status: {drone.status}</small>
    </section>
  )
}
