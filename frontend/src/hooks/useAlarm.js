import { useEffect } from 'react'
import { playAlarm } from '../utils/alarm'

export function useAlarm(emergency) {
  useEffect(() => {
    if (emergency === 'none') return undefined
    const id = setInterval(() => playAlarm(emergency), 900)
    return () => clearInterval(id)
  }, [emergency])
}
