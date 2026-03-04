from fastapi import APIRouter

from .runtime import AgentRuntime
from .schemas import DetectEvent


def create_router(runtime: AgentRuntime) -> APIRouter:
    router = APIRouter()

    @router.get("/state")
    async def get_state():
        return await runtime.get_state()

    @router.post("/detect")
    async def detect_emergency(payload: DetectEvent):
        return await runtime.detect(payload.emergency)

    return router
