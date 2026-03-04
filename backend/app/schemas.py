from pydantic import BaseModel
class DetectEvent(BaseModel):
    emergency: str
