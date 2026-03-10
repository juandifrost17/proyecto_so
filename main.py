from datetime import date
from cuenta_billetera import CuentaBilletera
from usuario import Usuario
from banco import Banco
from gestor_transacciones import GestorTransacciones
from simulacion_cajero import SimulacionCajero
from excepciones import SaldoInsuficienteException, MontoInvalidoException

def main():
    banco = Banco(nombre="Banco Nacional")

    cuenta_karel = CuentaBilletera(numero_cuenta="1020304050", saldo_inicial=150.0)
    cuenta_maria = CuentaBilletera(numero_cuenta="5060708090", saldo_inicial=200.0)

    banco.registrar_cuenta(cuenta_karel)
    banco.registrar_cuenta(cuenta_maria)

    usuario_karel = Usuario(
        nombre="Karel",
        apellido="Gonzalez",
        cedula="0912345678",
        email="karel@linux.com",
        fecha_nacimiento=date(2006, 11, 3),
        telefono="0991234567",
        cuenta=cuenta_karel
    )

    usuario_maria = Usuario(
        nombre="Maria",
        apellido="Lopez",
        cedula="0987654321",
        email="maria@linux.com",
        fecha_nacimiento=date(2000, 5, 15),
        telefono="0997654321",
        cuenta=cuenta_maria
    )

    print("=" * 60)
    print("SIMULACIÓN DE CAJEROS AUTOMÁTICOS")
    print("=" * 60)
    print("Banco: " + str(banco))
    print("Estado inicial:")
    print("  " + str(usuario_karel))
    print("  " + str(usuario_maria))
    print("\n--- Fase 1: Operaciones concurrentes (retiros, depósitos, consultas) ---\n")

    cajeros = []
    for i in range(1, 4):
        cajero = SimulacionCajero(id_cajero=i, usuario=usuario_karel, banco=banco)
        cajeros.append(cajero)
        cajero.start()

    for cajero in cajeros:
        cajero.join()

    print("\n--- Fase 2: Transferencia entre cuentas (doble bloqueo) ---\n")

    try:
        cuenta_origen = banco.obtener_cuenta("1020304050")
        cuenta_destino = banco.obtener_cuenta("5060708090")
        GestorTransacciones.transferir(cuenta_origen, cuenta_destino, 30.0)
        print("Transferencia de $30.0 de Karel a Maria -> Éxito")
    except SaldoInsuficienteException as e:
        print("Error en transferencia: " + str(e))
    except MontoInvalidoException as e:
        print("Error en transferencia: " + str(e))

    print("\n" + "=" * 60)
    print("RESULTADO FINAL")
    print("=" * 60)
    print("Banco: " + str(banco))
    print("  " + str(usuario_karel))
    print("  " + str(usuario_maria))

    print("\nHistorial de " + usuario_karel.nombre + ":")
    for tx in usuario_karel.cuenta.historial_transacciones:
        print("  -> " + tx)

    print("\nHistorial de " + usuario_maria.nombre + ":")
    for tx in usuario_maria.cuenta.historial_transacciones:
        print("  -> " + tx)

if __name__ == "__main__":
    main()