from datetime import date
from usuario import Usuario
from banco import Banco
from gestor_transacciones import GestorTransacciones
from simulacion_cajero import SimulacionCajero
from excepciones import (SaldoInsuficienteException, MontoInvalidoException, TipoCuentaInvalidoException, LimiteCuentasExcedidoException, TipoCuentaDuplicadoException)

def main():
    banco = Banco(nombre="Banco Nacional")

    usuario_karel = Usuario(
        nombre="Karel",
        apellido="Gonzalez",
        cedula="0912345678",
        email="karel@linux.com",
        fecha_nacimiento=date(2006, 11, 3),
        telefono="0991234567"
    )

    usuario_maria = Usuario(
        nombre="Maria",
        apellido="Lopez",
        cedula="0987654321",
        email="maria@linux.com",
        fecha_nacimiento=date(2000, 5, 15),
        telefono="0997654321"
    )

    try:
        banco.asignar_cuenta_nueva(usuario_karel, saldo_inicial=150.0, tipo="ahorros")
        banco.asignar_cuenta_nueva(usuario_karel, saldo_inicial=50.0, tipo="corriente")
        banco.asignar_cuenta_nueva(usuario_maria, saldo_inicial=200.0, tipo="ahorros")
    except (TipoCuentaInvalidoException, LimiteCuentasExcedidoException, TipoCuentaDuplicadoException) as e:
        print("Error al inicializar cuentas: " + str(e))
        return

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
        numero_origen = usuario_karel.cuentas[0].numero_cuenta
        numero_destino = usuario_maria.cuentas[0].numero_cuenta
        
        cuenta_origen = banco.obtener_cuenta(numero_origen)
        cuenta_destino = banco.obtener_cuenta(numero_destino)
        
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
    for cuenta in usuario_karel.cuentas:
        print("  Cuenta " + cuenta.tipo.capitalize() + " (" + cuenta.numero_cuenta + "):")
        for tx in cuenta.historial_transacciones:
            print("    -> " + tx)

    print("\nHistorial de " + usuario_maria.nombre + ":")
    for cuenta in usuario_maria.cuentas:
        print("  Cuenta " + cuenta.tipo.capitalize() + " (" + cuenta.numero_cuenta + "):")
        for tx in cuenta.historial_transacciones:
            print("    -> " + tx)

if __name__ == "__main__":
    main()