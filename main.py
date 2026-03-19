from datetime import date
from banco import Banco
from usuario import Usuario
from gestor_transacciones import GestorTransacciones
from simulacion_cajero import SimulacionCajero
from excepciones import (
    TipoCuentaInvalidoException,
    LimiteCuentasExcedidoException,
    TipoCuentaDuplicadoException,
)
from bitacora import configurar_bitacora, logger


def crear_datos_base():
    banco = Banco(nombre="Banco Nacional")

    usuario_karel = Usuario(
        nombre="Karel",
        apellido="Gonzalez",
        cedula="0912345678",
        email="karel@linux.com",
        fecha_nacimiento=date(2006, 11, 3),
        telefono="0991234567",
    )

    usuario_maria = Usuario(
        nombre="Maria",
        apellido="Lopez",
        cedula="0987654321",
        email="maria@linux.com",
        fecha_nacimiento=date(2000, 5, 15),
        telefono="0997654321",
    )

    usuarios = [usuario_karel, usuario_maria]

    try:
        cuenta_karel = banco.asignar_cuenta_nueva(usuario_karel, saldo_inicial=1000.0, tipo="ahorros")
        cuenta_maria = banco.asignar_cuenta_nueva(usuario_maria, saldo_inicial=500.0, tipo="ahorros")
        logger.info(
            "Datos base cargados | Usuario: %s %s | Cuenta: %s | Tipo: %s | Saldo: %.2f",
            usuario_karel.nombre,
            usuario_karel.apellido,
            cuenta_karel.numero_cuenta,
            cuenta_karel.tipo,
            cuenta_karel.saldo,
        )
        logger.info(
            "Datos base cargados | Usuario: %s %s | Cuenta: %s | Tipo: %s | Saldo: %.2f",
            usuario_maria.nombre,
            usuario_maria.apellido,
            cuenta_maria.numero_cuenta,
            cuenta_maria.tipo,
            cuenta_maria.saldo,
        )
    except (TipoCuentaInvalidoException, LimiteCuentasExcedidoException, TipoCuentaDuplicadoException) as error:
        print("Error al cargar datos base: " + str(error))
        logger.error("Error al cargar datos base: %s", error)
    return banco, usuarios


def mostrar_menu():
    print("\n" + "=" * 70)
    print("MENÚ PRINCIPAL - SIMULADOR DE CAJEROS AUTOMÁTICOS")
    print("=" * 70)
    print("1. Crear usuario")
    print("2. Crear cuenta")
    print("3. Simular retiros concurrentes sobre una misma cuenta")
    print("4. Simular depósitos concurrentes sobre una misma cuenta")
    print("5. Simulación general del cajero (todas las transacciones)")
    print("6. Mostrar estado actual")
    print("7. Salir")


def seleccionar_usuario(usuarios):
    print("\nUsuarios disponibles:")
    for indice, usuario in enumerate(usuarios, start=1):
        print(f"{indice}. {usuario.nombre} {usuario.apellido}")
    opcion = input("Seleccione el usuario: ").strip()
    if not opcion.isdigit():
        print("Debe ingresar un número válido.")
        return None
    indice = int(opcion) - 1
    if indice < 0 or indice >= len(usuarios):
        print("Opción de usuario inválida.")
        return None
    return usuarios[indice]


def seleccionar_cuenta(banco):
    cuentas = banco.listar_cuentas()
    if not cuentas:
        print("No existen cuentas registradas.")
        return None
    print("\nCuentas disponibles:")
    for indice, cuenta in enumerate(cuentas, start=1):
        print(
            f"{indice}. Cuenta {cuenta.tipo} | Número: {cuenta.numero_cuenta} | Saldo actual: ${cuenta.saldo:.2f}"
        )
    opcion = input("Seleccione la cuenta: ").strip()
    if not opcion.isdigit():
        print("Debe ingresar un número válido.")
        return None
    indice = int(opcion) - 1
    if indice < 0 or indice >= len(cuentas):
        print("Opción de cuenta inválida.")
        return None
    return cuentas[indice]


def mostrar_estado_actual(banco, usuarios):
    print("\n" + "=" * 70)
    print("ESTADO ACTUAL DEL SISTEMA")
    print("=" * 70)
    print(str(banco))
    for usuario in usuarios:
        print(f"\nUsuario: {usuario.nombre} {usuario.apellido}")
        if not usuario.cuentas:
            print("  Sin cuentas registradas.")
            continue
        for cuenta in usuario.cuentas:
            print(
                f"  - Cuenta {cuenta.tipo.capitalize()} | Número: {cuenta.numero_cuenta} | Saldo: ${cuenta.saldo:.2f}"
            )
            if not cuenta.historial_transacciones:
                print("      Historial: sin movimientos.")
            else:
                print("      Historial:")
                for movimiento in cuenta.historial_transacciones[-5:]:
                    print("        -> " + movimiento)


def crear_usuario(usuarios):
    print("\nCREACIÓN DE USUARIO")
    nombre = input("Ingrese el nombre: ").strip()
    apellido = input("Ingrese el apellido: ").strip()
    cedula = input("Ingrese la cédula: ").strip()
    email = input("Ingrese el email: ").strip()
    telefono = input("Ingrese el teléfono: ").strip()
    fecha_texto = input("Ingrese la fecha de nacimiento (YYYY-MM-DD): ").strip()
    try:
        fecha_nacimiento = date.fromisoformat(fecha_texto)
    except ValueError:
        print("La fecha debe tener formato YYYY-MM-DD.")
        return

    for usuario in usuarios:
        if usuario.cedula == cedula:
            print("Ya existe un usuario con esa cédula.")
            return
    nuevo_usuario = Usuario(
        nombre=nombre,
        apellido=apellido,
        cedula=cedula,
        email=email,
        fecha_nacimiento=fecha_nacimiento,
        telefono=telefono,
    )
    usuarios.append(nuevo_usuario)
    print(f"Usuario creado con éxito: {nombre} {apellido}")
    logger.info(
        "Usuario creado | Nombre: %s %s | Cédula: %s | Email: %s",
        nombre,
        apellido,
        cedula,
        email,
    )


def crear_cuenta(banco, usuarios):
    print("\nCREACIÓN DE CUENTA")
    usuario = seleccionar_usuario(usuarios)
    if usuario is None:
        return
    tipo = input("Ingrese el tipo de cuenta (ahorros/corriente): ").strip().lower()
    try:
        saldo_inicial = float(input("Ingrese el saldo inicial: ").strip())
    except ValueError:
        print("El saldo inicial debe ser numérico.")
        return

    try:
        nueva_cuenta = banco.asignar_cuenta_nueva(usuario, saldo_inicial, tipo)
        print(
            f"Cuenta creada con éxito para {usuario.nombre}. Número: {nueva_cuenta.numero_cuenta} | Saldo inicial: ${nueva_cuenta.saldo:.2f}"
        )
        logger.info(
            "Cuenta creada | Usuario: %s %s | Cuenta: %s | Tipo: %s | Saldo inicial: %.2f",
            usuario.nombre,
            usuario.apellido,
            nueva_cuenta.numero_cuenta,
            nueva_cuenta.tipo,
            nueva_cuenta.saldo,
        )
    except (TipoCuentaInvalidoException, LimiteCuentasExcedidoException, TipoCuentaDuplicadoException) as error:
        print("No se pudo crear la cuenta: " + str(error))
        logger.error("No se pudo crear la cuenta: %s", error)


def obtener_montos_retiro(saldo_actual):
    if saldo_actual <= 0:
        return [1.0, 1.0, 1.0]
    total_a_retirar = saldo_actual * 0.45
    monto_1 = round(total_a_retirar * 0.45, 2)
    monto_2 = round(total_a_retirar * 0.35, 2)
    monto_3 = round(total_a_retirar - monto_1 - monto_2, 2)
    return [max(monto_1, 1.0), max(monto_2, 1.0), max(monto_3, 1.0)]


def simular_retiros(banco):
    print("\nSIMULACIÓN DE RETIROS CONCURRENTES")
    cuenta = seleccionar_cuenta(banco)
    if cuenta is None:
        return
    montos = obtener_montos_retiro(cuenta.saldo)
    print("\nSe lanzarán 3 cajeros sobre la MISMA cuenta para evidenciar el mutex.")
    print("Montos de retiro predefinidos: " + ", ".join(f"${monto:.2f}" for monto in montos))
    print(f"Saldo inicial antes de la simulación: ${cuenta.saldo:.2f}\n")
    logger.info("Inicio simulación de retiros concurrentes | Cuenta: %s", cuenta.numero_cuenta)

    cajeros = []
    for indice, monto in enumerate(montos, start=1):
        cajero = SimulacionCajero(
            id_cajero=indice,
            banco=banco,
            modo="predefinido",
            cuenta=cuenta,
            operacion="retiro",
            monto=monto,
            demora_critica=1.0,
        )
        cajeros.append(cajero)
        cajero.start()
    for cajero in cajeros:
        cajero.join()
    print("CONSULTA FINAL DESPUÉS DE LOS RETIROS")
    GestorTransacciones.consultar(cuenta, actor="Sistema", mostrar_mutex=True)
    logger.info("Fin simulación de retiros concurrentes | Cuenta: %s", cuenta.numero_cuenta)


def simular_depositos(banco):
    print("\nSIMULACIÓN DE DEPÓSITOS CONCURRENTES")
    cuenta = seleccionar_cuenta(banco)
    if cuenta is None:
        return
    montos = [50.0, 75.0, 100.0]
    print("\nSe lanzarán 3 cajeros sobre la MISMA cuenta para evidenciar el mutex.")
    print("Montos de depósito predefinidos: " + ", ".join(f"${monto:.2f}" for monto in montos))
    print(f"Saldo inicial antes de la simulación: ${cuenta.saldo:.2f}\n")
    logger.info("Inicio simulación de depósitos concurrentes | Cuenta: %s", cuenta.numero_cuenta)
    cajeros = []
    for indice, monto in enumerate(montos, start=1):
        cajero = SimulacionCajero(
            id_cajero=indice,
            banco=banco,
            modo="predefinido",
            cuenta=cuenta,
            operacion="deposito",
            monto=monto,
            demora_critica=1.0,
        )
        cajeros.append(cajero)
        cajero.start()
    for cajero in cajeros:
        cajero.join()
    print("CONSULTA FINAL DESPUÉS DE LOS DEPÓSITOS")
    GestorTransacciones.consultar(cuenta, actor="Sistema", mostrar_mutex=True)
    logger.info("Fin simulación de depósitos concurrentes | Cuenta: %s", cuenta.numero_cuenta)


def simulacion_general(banco):
    print("\nSIMULACIÓN GENERAL DEL CAJERO")
    cuentas = banco.listar_cuentas()
    if len(cuentas) < 2:
        print("Se recomienda tener al menos 2 cuentas para ver transferencias en la simulación general.")
    print("Se crearán 3 cajeros con operaciones aleatorias: retiro, depósito, consulta y transferencia.\n")
    logger.info("Inicio simulación general del cajero")
    cajeros = []
    for indice in range(1, 4):
        cajero = SimulacionCajero(
            id_cajero=indice,
            banco=banco,
            modo="aleatorio",
            iteraciones=3,
            demora_critica=0.8,
        )
        cajeros.append(cajero)
        cajero.start()
    for cajero in cajeros:
        cajero.join()
    print("Simulación general finalizada.")
    logger.info("Fin simulación general del cajero")


def main():
    configurar_bitacora()
    logger.info("Sistema iniciado")
    banco, usuarios = crear_datos_base()
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            crear_usuario(usuarios)
        elif opcion == "2":
            crear_cuenta(banco, usuarios)
        elif opcion == "3":
            simular_retiros(banco)
        elif opcion == "4":
            simular_depositos(banco)
        elif opcion == "5":
            simulacion_general(banco)
        elif opcion == "6":
            mostrar_estado_actual(banco, usuarios)
        elif opcion == "7":
            print("Saliendo del sistema.")
            logger.info("Sistema finalizado")
            break
        else:
            print("Opción inválida. Intente nuevamente.")


if __name__ == "__main__":
    main()