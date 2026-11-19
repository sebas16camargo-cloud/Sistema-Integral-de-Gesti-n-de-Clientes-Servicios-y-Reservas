"""Simulación de 12 operaciones (válidas e inválidas) de Software FJ."""
from software_fj.gestor import GestorFJ
from software_fj.logger import log
from software_fj.servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala


def main():
    g = GestorFJ()
    log.info("===== INICIO DE LA SIMULACIÓN =====")

    # 1-3: clientes (válido, email inválido, parámetro faltante)
    ana = g.registrar_cliente(nombre="Ana Pérez", documento="1020304050",
                              email="ana@correo.com", telefono="3101234567")
    g.registrar_cliente(nombre="Luis Gómez", documento="12345678",
                        email="correo-malo", telefono="3001112233")
    g.registrar_cliente(nombre="Marta Ruiz", documento=None,
                        email="marta@correo.com", telefono="3009998877")
    carlos = g.registrar_cliente(nombre="Carlos Díaz", documento="987654321",
                                 email="carlos@correo.com", telefono="3205556677")

    # 4-6: servicios (2 válidos, 1 inválido, 1 más válido)
    sala = g.agregar_servicio(ReservaSala, "Sala Innovación", 50000, 10, True)
    g.agregar_servicio(AlquilerEquipo, "Portátil", -100, 2)  # tarifa inválida
    equipo = g.agregar_servicio(AlquilerEquipo, "Proyector", 15000, 2, True)
    asesoria = g.agregar_servicio(AsesoriaEspecializada, "Arquitectura",
                                  80000, "Cloud", "senior")

    print("\n--- Catálogo (polimorfismo) ---")
    for s in g.servicios:
        print(" ", s.describir())

    # 7-12: reservas y operaciones
    r1 = g.crear_reserva(ana, sala, 3)                  # válida
    g.crear_reserva(ana, sala, 20)                      # duración inválida
    g.crear_reserva("no-es-cliente", sala, 2)           # cliente inválido
    equipo.disponible = False
    g.crear_reserva(carlos, equipo, 5)                  # servicio no disponible
    equipo.disponible = True
    r2 = g.crear_reserva(carlos, asesoria, 2)           # válida

    g.confirmar(r1)
    g.confirmar(r1)                                     # doble confirmación (error)
    total1 = g.procesar(r1, descuento=0.10)
    g.cancelar(r1)                                      # cancelar procesada (error)
    g.procesar(r2)                                      # sin confirmar (error)
    g.confirmar(r2)
    total2 = g.procesar(r2)
    g.procesar(r2)                                      # ya procesada (error)

    print("\n--- Resultados ---")
    print(f"Total reserva 1 (con 10% desc.): ${total1:,.2f}")
    print(f"Total reserva 2: ${total2:,.2f}")
    print(f"Costo sala 3h solo IVA: ${sala.calcular_costo_con_iva(3):,.2f}")
    print(f"Costo sala 3h sin extras: ${sala.calcular_costo(3):,.2f}")
    for r in g.reservas:
        print(" ", r.describir())

    log.info("===== FIN DE LA SIMULACIÓN (el sistema continuó estable) =====")


if __name__ == "__main__":
    main()
