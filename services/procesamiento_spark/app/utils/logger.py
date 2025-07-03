# Logger básico para auditoría interna

import logging
import os

# Crea un logger con configuración básica
def get_logger(name: str = "spark_job") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            '[%(asctime)s] %(levelname)s in %(name)s: %(message)s'
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        file_handler = logging.FileHandler(f"{log_dir}/{name}.log")
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger
