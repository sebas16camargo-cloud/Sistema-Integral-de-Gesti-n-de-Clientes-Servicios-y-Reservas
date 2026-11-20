"""Configuración del archivo de logs (único uso de archivos del sistema)."""
import logging
from pathlib import Path

RUTA_LOG = Path(__file__).resolve().parent.parent / "logs" / "sistema.log"


def obtener_logger() -> logging.Logger:
    logger = logging.getLogger("sistema")
    if logger.handlers:
        return logger
    logger.setLevel(logging.INFO)
    RUTA_LOG.parent.mkdir(exist_ok=True)
    formato = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")
    archivo = logging.FileHandler(RUTA_LOG, encoding="utf-8")
    archivo.setFormatter(formato)
    consola = logging.StreamHandler()
    consola.setFormatter(formato)
    logger.addHandler(archivo)
    logger.addHandler(consola)
    return logger


log = obtener_logger()
