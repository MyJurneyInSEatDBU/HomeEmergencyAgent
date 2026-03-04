export function playAlarm(emergency) {
  try {
    const ctx = new (window.AudioContext || window.webkitAudioContext)()
    const oscillator = ctx.createOscillator()
    const gainNode = ctx.createGain()

    oscillator.type = emergency === 'flood' ? 'sawtooth' : 'square'
    oscillator.frequency.value = emergency === 'flood' ? 520 : 880
    gainNode.gain.value = 0.07

    oscillator.connect(gainNode)
    gainNode.connect(ctx.destination)

    oscillator.start()
    setTimeout(() => oscillator.stop(), 600)
  } catch {
    // Ignore audio errors from unsupported devices/browsers.
  }
}
