import { useCallback, useEffect, useState } from 'react'
import {
  detectEmergency,
  getState,
} from '../api/emergencyApi'
import { makeInitialState } from '../utils/stateFormat'
export function useEmergencyAgent() {
  const [state, setState] = useState(makeInitialState)
  const refreshState = useCallback(async () => {
    const data = await getState()
    setState(data)
  }, [])

  useEffect(() => {
    refreshState()
    const id = setInterval(refreshState, 700)
    return () => clearInterval(id)
  }, [refreshState])

  const onEmergencyChange = useCallback(async (emergency) => {
    await detectEmergency(emergency)
    await refreshState()
  }, [refreshState])

  return {
    state,
    actions: {
      onEmergencyChange,
    },
  }
}
