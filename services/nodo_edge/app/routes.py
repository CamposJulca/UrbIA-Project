# Endpoints principales del nodo_edge

from fastapi import APIRouter, HTTPException
from app.models import LoteLecturas, LecturaRespuesta, ResumenRespuesta
from app.database import get_connection
from app.batch import procesar_lecturas_por_lote

router = APIRouter()

@router.get("/ping", tags=["salud"])
def ping():
    return {"mensaje": "Nodo Edge activo y en funcionamiento"}

@router.post("/telemetria", tags=["lecturas"])
def recibir_lecturas(lote: LoteLecturas):
    """
    Recibe un lote de lecturas y las inserta en la base de datos local.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        for lectura in lote.lecturas:
            cursor.execute("""
                INSERT INTO lecturas_edge (device_id, timestamp, variable, valor)
                VALUES (?, ?, ?, ?)
            """, (
                lectura.device_id,
                lectura.timestamp.isoformat(),
                lectura.variable,
                lectura.valor
            ))
        conn.commit()
        return {"mensaje": f"✅ Se insertaron {len(lote.lecturas)} lecturas"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"❌ Error al insertar lecturas: {e}")
    finally:
        conn.close()

@router.get("/lecturas", response_model=list[LecturaRespuesta], tags=["lecturas"])
def obtener_lecturas(limit: int = 20):
    """
    Devuelve las últimas lecturas registradas.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, device_id, timestamp, variable, valor
            FROM lecturas_edge
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "device_id": row[1],
                "timestamp": row[2],
                "variable": row[3],
                "valor": row[4]
            }
            for row in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Error al obtener lecturas: {e}")
    finally:
        conn.close()

@router.post("/procesar-lote", tags=["procesamiento"])
def procesar_lote():
    """
    Procesa lecturas agrupándolas por device_id y variable, y guarda el resumen.
    """
    resultado = procesar_lecturas_por_lote()
    if "error" in resultado:
        raise HTTPException(status_code=500, detail=resultado["error"])
    return resultado

@router.get("/resumen", response_model=list[ResumenRespuesta], tags=["procesamiento"])
def obtener_resumen(limit: int = 20):
    """
    Devuelve los últimos resúmenes generados.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT id, device_id, variable, promedio, timestamp
            FROM resumen_edge
            ORDER BY timestamp DESC
            LIMIT ?
        """, (limit,))
        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "device_id": row[1],
                "variable": row[2],
                "promedio": row[3],
                "timestamp": row[4]
            }
            for row in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Error al obtener resumen: {e}")
    finally:
        conn.close()
