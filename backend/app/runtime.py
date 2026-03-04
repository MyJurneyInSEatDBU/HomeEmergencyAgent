import asyncio

from .engine import simulate_step
from .operations import detect
from .state import make_state


class AgentRuntime:
    def __init__(self) -> None:
        self.state = make_state()
        self.state_lock = asyncio.Lock()
        self.simulation_task: asyncio.Task | None = None
    async def simulation_loop(self) -> None:
        while True:
            async with self.state_lock:
                simulate_step(self.state)
            await asyncio.sleep(0.6)
    async def start(self) -> None:
        self.simulation_task = asyncio.create_task(self.simulation_loop())
    async def stop(self) -> None:
        if self.simulation_task:
            self.simulation_task.cancel()
            try:
                await self.simulation_task
            except asyncio.CancelledError:
                pass

    async def get_state(self) -> dict:
        async with self.state_lock:
            return self.state

    async def detect(self, emergency: str) -> dict:
        async with self.state_lock:
            return detect(self.state, emergency)
