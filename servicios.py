"""Servicios base y especializados con cálculo polimórfico de costos."""
from abc import ABC, abstractmethod

from entidades import Entidad
from excepciones import (
    CalculoInconsistenteError,
    ParametroFaltanteError,
    ServicioInvalidoError,
)


class Servicio(Entidad, ABC):
    IVA = 0.19

    def __init__(self, nombre=None, tarifa_hora=None, disponible=True):
        super().__init__()
        if not nombre:
            raise ParametroFaltanteError("El servicio requiere un nombre")
        try:
            tarifa = float(tarifa_hora)
        except (TypeError, ValueError) as e:
            raise ServicioInvalidoError(f"Tarifa inválida: {tarifa_hora!r}") from e
        if tarifa <= 0:
            raise ServicioInvalidoError("La tarifa por hora debe ser mayor a 0")
        self._nombre = nombre
        self._tarifa_hora = tarifa
        self.disponible = disponible

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_hora(self):
        return self._tarifa_hora

    @abstractmethod
    def validar_parametros(self, horas) -> None:
        """Valida los parámetros propios del servicio."""

    @abstractmethod
    def _costo_base(self, horas: float) -> float:
        """Costo sin impuestos ni descuentos (cada servicio lo define)."""

    def calcular_costo(self, horas, impuesto=0.0, descuento=0.0) -> float:
        """Calcula el costo aplicando validación, impuesto y descuento."""
        self.validar_parametros(horas)
        if not 0 <= impuesto <= 1 or not 0 <= descuento < 1:
            raise CalculoInconsistenteError("Impuesto/descuento fuera de rango")
        total = self._costo_base(horas) * (1 + impuesto) * (1 - descuento)
        if total < 0:
            raise CalculoInconsistenteError("Se obtuvo un costo negativo")
        return round(total, 2)

    def calcular_costo_con_iva(self, horas) -> float:
        return self.calcular_costo(horas, impuesto=self.IVA)

    def calcular_costo_con_descuento(self, horas, descuento) -> float:
        return self.calcular_costo(horas, self.IVA, descuento)


class ReservaSala(Servicio):
    def __init__(self, nombre, tarifa_hora, capacidad, aire_acondicionado=False):
        super().__init__(nombre, tarifa_hora)
        if not isinstance(capacidad, int) or isinstance(capacidad, bool) or capacidad < 1:
            raise ServicioInvalidoError("La capacidad debe ser un entero positivo")
        self.capacidad = capacidad
        self.aire = aire_acondicionado

    def validar_parametros(self, horas):
        if not isinstance(horas, (int, float)) or isinstance(horas, bool) or not 0 < horas <= 12:
            raise ServicioInvalidoError("Una sala se reserva entre 0 y 12 horas")

    def _costo_base(self, horas):
        extra = 1.10 if self.aire else 1.0
        return self.tarifa_hora * horas * extra

    def describir(self):
        return (f"Sala '{self.nombre}' (cap. {self.capacidad}, "
                f"{'con' if self.aire else 'sin'} A/C) - ${self.tarifa_hora:,.0f}/h")


class AlquilerEquipo(Servicio):
    def __init__(self, nombre, tarifa_hora, cantidad, seguro=False):
        super().__init__(nombre, tarifa_hora)
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad < 1:
            raise ServicioInvalidoError("La cantidad de equipos debe ser mayor o igual a 1")
        self.cantidad = cantidad
        self.seguro = seguro

    def validar_parametros(self, horas):
        if not isinstance(horas, (int, float)) or isinstance(horas, bool) or not 0 < horas <= 72:
            raise ServicioInvalidoError("Un equipo se alquila entre 0 y 72 horas")

    def _costo_base(self, horas):
        base = self.tarifa_hora * horas * self.cantidad
        return base + (base * 0.05 if self.seguro else 0)

    def describir(self):
        return (f"Alquiler de {self.cantidad}x '{self.nombre}'"
                f"{' con seguro' if self.seguro else ''} - ${self.tarifa_hora:,.0f}/h")


class AsesoriaEspecializada(Servicio):
    NIVELES = {"junior": 1.0, "senior": 1.5, "experto": 2.0}

    def __init__(self, nombre, tarifa_hora, especialidad, nivel="junior"):
        super().__init__(nombre, tarifa_hora)
        if nivel not in self.NIVELES:
            raise ServicioInvalidoError(f"Nivel inválido: {nivel!r}")
        if not especialidad:
            raise ParametroFaltanteError("La asesoría requiere una especialidad")
        self.especialidad = especialidad
        self.nivel = nivel

    def validar_parametros(self, horas):
        if not isinstance(horas, (int, float)) or isinstance(horas, bool) or not 0.5 <= horas <= 8:
            raise ServicioInvalidoError("Una asesoría dura entre 0.5 y 8 horas")

    def _costo_base(self, horas):
        return self.tarifa_hora * horas * self.NIVELES[self.nivel]

    def describir(self):
        return (f"Asesoría '{self.nombre}' en {self.especialidad} "
                f"(nivel {self.nivel}) - ${self.tarifa_hora:,.0f}/h")
