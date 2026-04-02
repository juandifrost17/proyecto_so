from datetime import date
import random
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

CAJEROS_SISTEMA = [
    {"id": 1, "nombre": "Cajero 1", "ubicacion": "Centro"},
    {"id": 2, "nombre": "Cajero 2", "ubicacion": "Urdesa"},
    {"id": 3, "nombre": "Cajero 3", "ubicacion": "Kennedy"},
    {"id": 4, "nombre": "Cajero 4", "ubicacion": "Samborondón"},
    {"id": 5, "nombre": "Cajero 5", "ubicacion": "Alborada"},
    {"id": 6, "nombre": "Cajero 6", "ubicacion": "Vía a la Costa"},
]


def crear_datos_base():
    banco = Banco(nombre="Sistema Bancario")

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
            "Datos base cargados | Usuario: %s %s | Cuenta: %s | Tipo: %s | Saldo inicial: %.2f",
            usuario_karel.nombre,
            usuario_karel.apellido,
            cuenta_karel.numero_cuenta,
            cuenta_karel.tipo,
            cuenta_karel.saldo,
        )
        logger.info(
            "Datos base cargados | Usuario: %s %s | Cuenta: %s | Tipo: %s | Saldo inicial: %.2f",
            usuario_maria.nombre,
            usuario_maria.apellido,
            cuenta_maria.numero_cuenta,
            cuenta_maria.tipo,
            cuenta_maria.saldo,
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
    print("5. Simulación general de transacciones")
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
                f"{indice}. Titular: {cuenta.titular} | Cuenta {cuenta.tipo.capitalize()} | "
                f"Número: {cuenta.numero_cuenta} | Saldo actual: ${cuenta.saldo:.2f}"
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


def seleccionar_cajeros_participantes():
    cantidad = random.randint(3, 5)
    return random.sample(CAJEROS_SISTEMA, cantidad)


def mostrar_resumen_cajeros(participantes):
    print("\n" + "=" * 70)
    print("CAJEROS REGISTRADOS EN EL SISTEMA")
    print("=" * 70)
    print(f"Total de cajeros registrados: {len(CAJEROS_SISTEMA)}")
    for cajero in CAJEROS_SISTEMA:
        print(f"- {cajero['nombre']} | Ubicación: {cajero['ubicacion']}")
    print()
    print(f"Cajeros participantes en esta ejecución: {len(participantes)}")
    for cajero in participantes:
        print(f"  * {cajero['nombre']} | Ubicación: {cajero['ubicacion']}")
    print("=" * 70)


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
                f"Titular: {cuenta.titular} | Saldo: ${cuenta.saldo:.2f}"
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
            "Usuario creado | Nombre: %s %s | Cédula: %s | Email: %s | Cuenta: %s | Tipo: %s | Saldo inicial: %.2f",
            nuevo_usuario.nombre,
            nuevo_usuario.apellido,
            nuevo_usuario.cedula,
            nuevo_usuario.email,
            nueva_cuenta.numero_cuenta,
            nueva_cuenta.tipo,
            nueva_cuenta.saldo,
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
            f"Cuenta corriente creada con éxito para {usuario.nombre} {usuario.apellido}. "
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


def obtener_montos_retiro(saldo_actual, cantidad_cajeros):
    if saldo_actual <= 0 or cantidad_cajeros <= 0:
        return [1.0] * max(cantidad_cajeros, 1)

    total_a_retirar = round(saldo_actual * 0.45, 2)
    pesos = [random.uniform(0.8, 1.4) for _ in range(cantidad_cajeros)]
    suma_pesos = sum(pesos)

    montos = []
    acumulado = 0.0
    for indice, peso in enumerate(pesos):
        if indice == cantidad_cajeros - 1:
            monto = round(total_a_retirar - acumulado, 2)
        else:
            monto = round(total_a_retirar * (peso / suma_pesos), 2)
            acumulado += monto
        montos.append(max(monto, 1.0))

    diferencia = round(total_a_retirar - sum(montos), 2)
    montos[-1] = round(max(montos[-1] + diferencia, 1.0), 2)
    return montos


def obtener_montos_deposito(cantidad_cajeros):
    return [round(random.uniform(40.0, 180.0), 2) for _ in range(cantidad_cajeros)]


def simular_retiros(banco):
    print("\nSIMULACIÓN DE RETIROS CONCURRENTES")
    participantes = seleccionar_cajeros_participantes()
    mostrar_resumen_cajeros(participantes)

    cuenta = seleccionar_cuenta(banco)
    if cuenta is None:
        return

    montos = obtener_montos_retiro(cuenta.saldo, len(participantes))
    print(f"\nCuenta seleccionada: {cuenta.descripcion_corta()}")
    print(
        f"Se lanzarán {len(participantes)} cajeros sobre la misma cuenta para evidenciar el mutex."
    )
    print("Montos de retiro predefinidos: " + ", ".join(f"${monto:.2f}" for monto in montos))
    print(f"Saldo inicial antes de la simulación: ${cuenta.saldo:.2f}\n")
    logger.info(
        "Inicio simulación de retiros concurrentes | Cuenta: %s | Titular: %s",
        cuenta.numero_cuenta,
        cuenta.titular,
    )

    cajeros = []
    for meta_cajero, monto in zip(participantes, montos):
        cajero = SimulacionCajero(
            id_cajero=meta_cajero["id"],
            banco=banco,
            modo="predefinido",
            cuenta=cuenta,
            operacion="retiro",
            monto=monto,
            demora_critica=1.0,
            ubicacion=meta_cajero["ubicacion"],
        )
        cajeros.append(cajero)
        cajero.start()

    for cajero in cajeros:
        cajero.join()

    print("CONSULTA FINAL DESPUÉS DE LOS RETIROS")
    GestorTransacciones.consultar(cuenta, actor="Sistema", mostrar_mutex=True)
    logger.info(
        "Fin simulación de retiros concurrentes | Cuenta: %s | Saldo final: %.2f",
        cuenta.numero_cuenta,
        cuenta.saldo,
    )


def simular_depositos(banco):
    print("\nSIMULACIÓN DE DEPÓSITOS CONCURRENTES")
    participantes = seleccionar_cajeros_participantes()
    mostrar_resumen_cajeros(participantes)

    cuenta = seleccionar_cuenta(banco)
    if cuenta is None:
        return

    montos = obtener_montos_deposito(len(participantes))
    print(f"\nCuenta seleccionada: {cuenta.descripcion_corta()}")
    print(
        f"Se lanzarán {len(participantes)} cajeros sobre la misma cuenta para evidenciar el mutex."
    )
    print("Montos de depósito predefinidos: " + ", ".join(f"${monto:.2f}" for monto in montos))
    print(f"Saldo inicial antes de la simulación: ${cuenta.saldo:.2f}\n")
    logger.info(
        "Inicio simulación de depósitos concurrentes | Cuenta: %s | Titular: %s",
        cuenta.numero_cuenta,
        cuenta.titular,
    )

    cajeros = []
    for meta_cajero, monto in zip(participantes, montos):
        cajero = SimulacionCajero(
            id_cajero=meta_cajero["id"],
            banco=banco,
            modo="predefinido",
            cuenta=cuenta,
            operacion="deposito",
            monto=monto,
            demora_critica=1.0,
            ubicacion=meta_cajero["ubicacion"],
        )
        cajeros.append(cajero)
        cajero.start()

    for cajero in cajeros:
        cajero.join()

    print("CONSULTA FINAL DESPUÉS DE LOS DEPÓSITOS")
    GestorTransacciones.consultar(cuenta, actor="Sistema", mostrar_mutex=True)
    logger.info(
        "Fin simulación de depósitos concurrentes | Cuenta: %s | Saldo final: %.2f",
        cuenta.numero_cuenta,
        cuenta.saldo,
    )


def simulacion_general(banco):
    print("\nSIMULACIÓN GENERAL DE TRANSACCIONES")
    cuentas = banco.listar_cuentas()

    if len(cuentas) < 2:
        print("Se recomienda tener al menos 2 cuentas para ver transferencias en la simulación general.")

    participantes = seleccionar_cajeros_participantes()
    mostrar_resumen_cajeros(participantes)

    print(
        f"Se ejecutará la simulación con {len(participantes)} cajeros disponibles. "
        "Cada uno realizará operaciones aleatorias de retiro, depósito, consulta y transferencia.\n"
    )
    logger.info("Inicio simulación general de transacciones")

    cajeros = []
    for meta_cajero in participantes:
        cajero = SimulacionCajero(
            id_cajero=meta_cajero["id"],
            banco=banco,
            modo="aleatorio",
            iteraciones=3,
            demora_critica=0.8,
            ubicacion=meta_cajero["ubicacion"],
        )
        cajeros.append(cajero)
        cajero.start()

    for cajero in cajeros:
        cajero.join()

    print("Simulación general finalizada.")
    logger.info("Fin simulación general de transacciones")


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