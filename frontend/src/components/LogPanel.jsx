export function LogPanel({ logs }) {
  return (
    <section className="panel">
      <h2 className="title">Command Log</h2>
      <div className="log">
        {logs.length === 0 && <div>No events yet.</div>}
        {logs.map((item, idx) => (
          <div key={idx}>{item}</div>
        ))}
      </div>
    </section>
  )
}
