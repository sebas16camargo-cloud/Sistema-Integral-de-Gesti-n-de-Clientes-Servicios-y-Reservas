"""Gestor central: listas internas y operaciones protegidas con logging."""
from cliente import Cliente
from excepciones import SoftwareFJError
from logger import log
from reserva import Reserva


class GestorFJ:
    def __init__(self):
        self.clientes: list[Cliente] = []
        self.servicios: list = []
        self.reservas: list[Reserva] = []

   def _ejecutar(self, descripcion, funcion, *args, **kwargs):
        """Ejecuta una operación y registra si hay error sin detener el programa."""
        try:
            resultado = funcion(*args, **kwargs)
        except SoftwareFJError as e:
            causa = f" | causa: {e.__cause__!r}" if e.__cause__ else ""
            log.error(f"Error en {descripcion}: {type(e).__name__} - {e}{causa}")
            return None
        except Exception as e:
            # Si ocurre un fallo inesperado, que no tumbe la ejecución
            log.critical(f"Fallo no controlado en {descripcion}: {type(e).__name__} - {e}")
            return None
        else:
            log.info(f"{descripcion}: bien")
            return resultado
    def registrar_cliente(self, **datos):
        c = self._ejecutar("Registro de cliente", Cliente, **datos)
        if c:
            self.clientes.append(c)
        return c
      
    def agregar_servicio(self, clase, *args, **kwargs):
        s = self._ejecutar(f"Creación de servicio {clase.__name__}", clase, *args, **kwargs)
        if s:
            self.servicios.append(s)
        return s

    def crear_reserva(self, cliente, servicio, horas):
        r = self._ejecutar("Creación de reserva", Reserva, cliente, servicio, horas)
        if r:
            self.reservas.append(r)
        return r

    def confirmar(self, reserva):
        return self._ejecutar("Confirmación", reserva.confirmar)

    def cancelar(self, reserva):
        return self._ejecutar("Cancelación", reserva.cancelar)

    def procesar(self, reserva, descuento=0.0):
        return self._ejecutar("Procesamiento", reserva.procesar, descuento)
