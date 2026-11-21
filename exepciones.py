"""Excepciones personalizadas de Software FJ."""


class SoftwareFJError(Exception):
    """Excepción base de todo el sistema."""


class ClienteInvalidoError(Error):
    """Datos del cliente inválidos."""


class ParametroFaltanteError(Error):
    """Falta un parámetro obligatorio."""




class CalculoInconsistenteError(Error):
    """El cálculo de costos produjo un resultado inconsistente."""
