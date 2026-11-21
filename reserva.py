"""Modelo de reserva con cliente, servicio, duración y estado."""
from enum import Enum

from cliente import Cliente
from entidades import Entidad
from excepciones import (OperacionNoPermitidaError, ReservaInvalidaError,
                          ServicioNoDisponibleError, SoftwareFJError )
from logger import log
from servicios import Servicio


class Estado(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    PROCESADA = "Procesada"
    CANCELADA = "Cancelada"


class Reserva(Entidad):
    def __init__(self, cliente, servicio, horas):
        super().__init__()
        if not isinstance(cliente, Cliente):
            raise ReservaInvalidaError("La reserva requiere un Cliente válido")
        if not isinstance(servicio, Servicio):
            raise ReservaInvalidaError("La reserva requiere un Servicio válido")
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"'{servicio.nombre}' no está disponible")
        try:
            servicio.validar_parametros(horas)
        except SoftwareFJError as e:
            raise ReservaInvalidaError(f"Duración inválida ({horas})") from e
        self._cliente = cliente
        self._servicio = servicio
        self._horas = horas
        self._estado = Estado.PENDIENTE

    @property
    def estado(self):
        return self._estado

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    def confirmar(self):
        if self._estado is not Estado.PENDIENTE:
            raise OperacionNoPermitidaError(
                f"No se puede confirmar una reserva {self._estado.value}")
        self._estado = Estado.CONFIRMADA
        log.info(f"Reserva #{self.id} confirmada")

    def cancelar(self):
        if self._estado in (Estado.PROCESADA, Estado.CANCELADA):
            raise OperacionNoPermitidaError(
                f"No se puede cancelar una reserva {self._estado.value}")
        self._estado = Estado.CANCELADA
        log.info(f"Reserva #{self.id} cancelada")

    def procesar(self, descuento=0.0) -> float:
        """Procesa la reserva y devuelve el costo total (try/except/else/finally)."""
        total = None
        try:
            if self._estado is not Estado.CONFIRMADA:
                raise OperacionNoPermitidaError(
                    "Solo se procesan reservas confirmadas")
            total = self._servicio.calcular_costo(
                self._horas, self._servicio.IVA, descuento)
        except SoftwareFJError as e:
            raise OperacionNoPermitidaError(
                f"No se pudo procesar la reserva #{self.id}") from e
        else:
            self._estado = Estado.PROCESADA
            log.info(f"Reserva #{self.id} procesada. Total: ${total:,.2f}")
            return total
        finally:
            log.info(f"Intento de procesamiento de reserva #{self.id} finalizado")

    def describir(self):
        return (f"Reserva #{self.id} [{self._estado.value}] {self._cliente.nombre} -> "
                f"{self._servicio.nombre} x {self._horas}h")
