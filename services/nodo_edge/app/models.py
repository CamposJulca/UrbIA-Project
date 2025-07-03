# Definición de modelos y esquemas de base de datos

from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class Lectura(BaseModel):
    device_id: str = Field(..., description="Identificador del dispositivo")
    timestamp: datetime = Field(..., description="Timestamp en formato ISO 8601")
    variable: str = Field(..., description="Nombre de la variable medida (e.g., temperatura)")
    valor: float = Field(..., description="Valor medido")

class LoteLecturas(BaseModel):
    lecturas: List[Lectura] = Field(..., description="Lista de lecturas a insertar")

class LecturaRespuesta(BaseModel):
    id: int
    device_id: str
    timestamp: str
    variable: str
    valor: float

class ResumenRespuesta(BaseModel):
    id: int
    device_id: str
    variable: str
    promedio: float
    timestamp: str
