# Utilidad para medir tiempos de ejecución

# app/utils/timer.py

import time
from functools import wraps

def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"⏱️ Función '{func.__name__}' ejecutada en {end - start:.2f} segundos.")
        return result
    return wrapper
