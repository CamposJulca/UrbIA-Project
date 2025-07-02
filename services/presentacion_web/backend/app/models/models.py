# backend/app/models/models.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DeviceInfo(BaseModel):
    id: str
    name: str
    type: Optional[str] = None
    label: Optional[str] = None

class SensorReading(BaseModel):
    ts: int  # Timestamp en milisegundos desde epoch
    variable: str
    value: float

    @property
    def formatted_timestamp(self) -> str:
        return datetime.fromtimestamp(self.ts / 1000).strftime("%Y-%m-%d %H:%M:%S")
