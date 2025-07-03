# Modelo de esquema para métricas procesadas

from pydantic import BaseModel, Field, validator
from typing import Literal
from datetime import datetime


class SensorMetric(BaseModel):
    sensor_id: str = Field(..., description="Identificador único del sensor")
    tipo: Literal["co2", "temperatura", "humedad", "presion", "luz", "ruido"]
    promedio: float = Field(..., ge=0, description="Valor promedio")
    maximo: float = Field(..., ge=0, description="Valor máximo")
    minimo: float = Field(..., ge=0, description="Valor mínimo")
    timestamp: datetime = Field(..., description="Marca temporal de la agregación")

    @validator("maximo")
    def check_maximo(cls, v, values):
        if "minimo" in values and v < values["minimo"]:
            raise ValueError("El valor máximo no puede ser menor que el mínimo.")
        return v

    @validator("promedio")
    def check_promedio(cls, v, values):
        if "minimo" in values and "maximo" in values:
            if not values["minimo"] <= v <= values["maximo"]:
                raise ValueError("El promedio debe estar entre el mínimo y el máximo.")
        return v
