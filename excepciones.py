"""Jerarquía de excepciones personalizadas para Software FJ."""


class SoftwareFJError(Exception):
    """Excepción base del sistema Software FJ."""


class ParametroFaltanteError(SoftwareFJError):
    """Se lanza cuando falta un dato obligatorio."""


class ClienteInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos de un cliente no son válidos."""


class ServicioInvalidoError(SoftwareFJError):
    """Se lanza cuando los datos o parámetros de un servicio no son válidos."""


class ServicioNoDisponibleError(SoftwareFJError):
    """Se lanza al intentar reservar un servicio que no está disponible."""


class ReservaInvalidaError(SoftwareFJError):
    """Se lanza cuando los datos de una reserva son inválidos."""


class OperacionNoPermitidaError(SoftwareFJError):
    """Se lanza cuando una acción sobre la reserva no está permitida en su estado actual."""


class CalculoInconsistenteError(SoftwareFJError):
    """Se lanza cuando un cálculo financiero arroja valores fuera de rango."""