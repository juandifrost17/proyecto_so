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

ERRORES_CUENTA = (
    ValueError,
    TipoCuentaInvalidoException,
    LimiteCuentasExcedidoException,
    TipoCuentaDuplicadoException,
)

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
        cuenta_karel = banco.asignar_cuenta_nueva(usuario_karel, 1000.0, "ahorros")
        cuenta_maria = banco.asignar_cuenta_nueva(usuario_maria, 500.0, "ahorros")

        logger.info(
            "Datos base cargados | Usuario: %s %s | Cuenta: %s | Tipo: %s | Saldo: %.2f",
            usuario_karel.nombre, usuario_karel.apellido,
            cuenta_karel.numero_cuenta, cuenta_karel.tipo, cuenta_karel.saldo,
        )
        logger.info(
            "Datos base cargados | Usuario: %s %s | Cuenta: %s | Tipo: %s | Saldo: %.2f",
            usuario_maria.nombre, usuario_maria.apellido,
            cuenta_maria.numero_cuenta, cuenta_maria.tipo, cuenta_maria.saldo,
        )
    except ERRORES_CUENTA as error:
        print("Error al cargar datos base: " + str(error))
        logger.error("Error al cargar datos base: %s", error)

    return banco, usuarios


def mostrar_menu():
    print("\n" + "=" * 70)
    print("MENÚ PRINCIPAL - SIMULADOR DE CAJEROS AUTOMÁTICOS")
    print("=" * 70)
    print("1. Crear usuario")
    print("2. Añadir cuenta corriente")
    print("3. Simular retiros concurrentes sobre una misma cuenta")
    print("4. Simular depósitos concurrentes sobre una misma cuenta")
    print("5. Simulación general del cajero (todas las transacciones)")
    print("6. Mostrar estado actual")
    print("7. Salir")


def leer_entrada(mensaje):
    valor = input(mensaje).strip()
    if valor.lower() == "cancelar":
        raise KeyboardInterrupt
    return valor


def contiene_numeros(texto):
    return any(caracter.isdigit() for caracter in texto)


def pedir_nombre():
    while True:
        nombre = leer_entrada("Ingrese el nombre: ")
        if not nombre:
            print("El nombre no puede estar vacío.")
        elif contiene_numeros(nombre):
            print("El nombre no puede contener números.")
        else:
            return nombre


def pedir_apellido():
    while True:
        apellido = leer_entrada("Ingrese el apellido: ")
        if not apellido:
            print("El apellido no puede estar vacío.")
        elif contiene_numeros(apellido):
            print("El apellido no puede contener números.")
        else:
            return apellido


def pedir_cedula(usuarios):
    while True:
        cedula = leer_entrada("Ingrese la cédula: ")
        if not cedula:
            print("La cédula no puede estar vacía.")
        elif not cedula.isdigit():
            print("La cédula debe contener solo números.")
        elif len(cedula) != 10:
            print("La cédula debe tener exactamente 10 dígitos.")
        elif any(usuario.cedula == cedula for usuario in usuarios):
            print("Ya existe un usuario con esa cédula.")
        else:
            return cedula


def pedir_email():
    while True:
        email = leer_entrada("Ingrese el email: ").lower()
        if not email:
            print("El email no puede estar vacío.")
        elif "@" not in email or "." not in email:
            print("Ingrese un email válido.")
        else:
            return email


def pedir_telefono():
    while True:
        telefono = leer_entrada("Ingrese el teléfono: ")
        if not telefono:
            print("El teléfono no puede estar vacío.")
        elif not telefono.isdigit():
            print("El teléfono debe contener solo números.")
        else:
            return telefono


def pedir_fecha_nacimiento():
    while True:
        fecha_texto = leer_entrada("Ingrese la fecha de nacimiento (YYYY-MM-DD): ")
        try:
            fecha_nacimiento = date.fromisoformat(fecha_texto)
            if fecha_nacimiento > date.today():
                print("La fecha de nacimiento no puede ser futura.")
            else:
                return fecha_nacimiento
        except ValueError:
            print("La fecha debe tener formato YYYY-MM-DD.")


def pedir_saldo(mensaje):
    while True:
        saldo_texto = leer_entrada(mensaje)
        try:
            saldo = float(saldo_texto)
            if saldo < 0:
                print("El saldo inicial no puede ser negativo.")
            else:
                return saldo
        except ValueError:
            print("El saldo inicial debe ser numérico.")


def seleccionar_usuario(usuarios):
    if not usuarios:
        print("No hay usuarios registrados.")
        return None

    while True:
        print("\nUsuarios disponibles:")
        for indice, usuario in enumerate(usuarios, start=1):
            print(f"{indice}. {usuario.nombre} {usuario.apellido}")

        try:
            opcion = leer_entrada("Seleccione el usuario: ")
        except KeyboardInterrupt:
            print("Operación cancelada.")
            return None

        if not opcion.isdigit():
            print("Debe ingresar un número válido.")
            continue

        indice = int(opcion) - 1
        if 0 <= indice < len(usuarios):
            return usuarios[indice]

        print("Opción de usuario inválida.")


def seleccionar_cuenta(banco):
    cuentas = banco.listar_cuentas()
    if not cuentas:
        print("No existen cuentas registradas.")
        return None

    while True:
        print("\nCuentas disponibles:")
        for indice, cuenta in enumerate(cuentas, start=1):
            print(
                f"{indice}. Cuenta {cuenta.tipo} | Número: {cuenta.numero_cuenta} | "
                f"Saldo actual: ${cuenta.saldo:.2f}"
            )

        try:
            opcion = leer_entrada("Seleccione la cuenta: ")
        except KeyboardInterrupt:
            print("Operación cancelada.")
            return None

        if not opcion.isdigit():
            print("Debe ingresar un número válido.")
            continue

        indice = int(opcion) - 1
        if 0 <= indice < len(cuentas):
            return cuentas[indice]

        print("Opción de cuenta inválida.")


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
                f"  - Cuenta {cuenta.tipo.capitalize()} | Número: {cuenta.numero_cuenta} | "
                f"Saldo: ${cuenta.saldo:.2f}"
            )
            if not cuenta.historial_transacciones:
                print("      Historial: sin movimientos.")
            else:
                print("      Historial:")
                for movimiento in cuenta.historial_transacciones[-5:]:
                    print("        -> " + movimiento)


def crear_usuario(banco, usuarios):
    print("\nCREACIÓN DE USUARIO")
    print("Escriba 'cancelar' en cualquier momento para volver al menú.")

    nuevo_usuario = None

    try:
        nuevo_usuario = Usuario(
            nombre=pedir_nombre(),
            apellido=pedir_apellido(),
            cedula=pedir_cedula(usuarios),
            email=pedir_email(),
            fecha_nacimiento=pedir_fecha_nacimiento(),
            telefono=pedir_telefono(),
        )

        saldo_inicial = pedir_saldo("Ingrese el saldo inicial de la cuenta de ahorros: ")
        usuarios.append(nuevo_usuario)
        nueva_cuenta = banco.asignar_cuenta_nueva(nuevo_usuario, saldo_inicial, "ahorros")

        print(
            f"Usuario creado con éxito: {nuevo_usuario.nombre} {nuevo_usuario.apellido} | "
            f"Cuenta de ahorros creada: {nueva_cuenta.numero_cuenta} | "
            f"Saldo inicial: ${nueva_cuenta.saldo:.2f}"
        )

        logger.info(
            "Usuario creado | Nombre: %s %s | Cédula: %s | Email: %s | Cuenta ahorros: %s",
            nuevo_usuario.nombre,
            nuevo_usuario.apellido,
            nuevo_usuario.cedula,
            nuevo_usuario.email,
            nueva_cuenta.numero_cuenta,
        )

    except KeyboardInterrupt:
        print("Creación de usuario cancelada.")
        logger.info("Creación de usuario cancelada por el usuario")
    except ERRORES_CUENTA as error:
        print("No se pudo crear el usuario: " + str(error))
        logger.error("No se pudo crear el usuario: %s", error)
        if nuevo_usuario is not None and nuevo_usuario in usuarios:
            usuarios.remove(nuevo_usuario)


def anadir_cuenta_corriente(banco, usuarios):
    print("\nAÑADIR CUENTA CORRIENTE")
    print("Escriba 'cancelar' en cualquier momento para volver al menú.")

    try:
        usuario = seleccionar_usuario(usuarios)
        if usuario is None:
            return

        saldo_inicial = pedir_saldo("Ingrese el saldo inicial: ")
        nueva_cuenta = banco.asignar_cuenta_nueva(usuario, saldo_inicial, "corriente")

        print(
            f"Cuenta corriente creada con éxito para {usuario.nombre}. "
            f"Número: {nueva_cuenta.numero_cuenta} | "
            f"Saldo inicial: ${nueva_cuenta.saldo:.2f}"
        )

        logger.info(
            "Cuenta creada | Usuario: %s %s | Cuenta: %s | Tipo: %s | Saldo inicial: %.2f",
            usuario.nombre,
            usuario.apellido,
            nueva_cuenta.numero_cuenta,
            nueva_cuenta.tipo,
            nueva_cuenta.saldo,
        )

    except KeyboardInterrupt:
        print("Creación de cuenta corriente cancelada.")
        logger.info("Creación de cuenta corriente cancelada por el usuario")
    except ERRORES_CUENTA as error:
        print("No se pudo crear la cuenta corriente: " + str(error))
        logger.error("No se pudo crear la cuenta corriente: %s", error)


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
            crear_usuario(banco, usuarios)
        elif opcion == "2":
            anadir_cuenta_corriente(banco, usuarios)
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