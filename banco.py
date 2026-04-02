import threading
import random as r
from cuenta_billetera import CuentaBilletera
from excepciones import (
    UsuarioNoEncontradoException,
    AliasDuplicadoException,
    TipoCuentaInvalidoException,
    LimiteCuentasExcedidoException,
    TipoCuentaDuplicadoException,
)


class Banco:
    def __init__(self, nombre: str):
        self.nombre = nombre
        self.cuentas = {}
        self.mutex = threading.Lock()

    def registrar_cuenta(self, cuenta: CuentaBilletera):
        with self.mutex:
            if cuenta.numero_cuenta in self.cuentas:
                raise AliasDuplicadoException("La cuenta " + cuenta.numero_cuenta + " ya existe.")
            self.cuentas[cuenta.numero_cuenta] = cuenta

    def obtener_cuenta(self, numero_cuenta: str) -> CuentaBilletera:
        with self.mutex:
            if numero_cuenta not in self.cuentas:
                raise UsuarioNoEncontradoException(
                    "La cuenta " + numero_cuenta + " no se encuentra registrada."
                )
            return self.cuentas[numero_cuenta]

    def listar_cuentas(self):
        with self.mutex:
            return list(self.cuentas.values())

    def asignar_cuenta_nueva(self, usuario, saldo_inicial: float, tipo: str) -> CuentaBilletera:
        if usuario is None:
            raise ValueError("El usuario no puede ser nulo.")
        if saldo_inicial < 0:
            raise ValueError("El saldo inicial no puede ser negativo.")

        tipo = tipo.strip().lower()
        if tipo not in ["ahorros", "corriente"]:
            raise TipoCuentaInvalidoException("Tipo de cuenta inválido: " + tipo)

        with self.mutex:
            if len(usuario.cuentas) >= 2:
                raise LimiteCuentasExcedidoException(
                    "El usuario " + usuario.nombre + " ya alcanzó el límite de cuentas permitido."
                )
            if usuario.tiene_cuenta_tipo(tipo):
                raise TipoCuentaDuplicadoException(
                    "El usuario " + usuario.nombre + " ya posee una cuenta de " + tipo + "."
                )
            if tipo == "corriente" and not usuario.tiene_cuenta_tipo("ahorros"):
                raise TipoCuentaInvalidoException(
                    "No se puede crear una cuenta corriente sin tener primero una cuenta de ahorros."
                )

            nuevo_numero = str(r.randint(1000000000, 9999999999))
            while nuevo_numero in self.cuentas:
                nuevo_numero = str(r.randint(1000000000, 9999999999))

            nueva_cuenta = CuentaBilletera(
                numero_cuenta=nuevo_numero,
                saldo_inicial=saldo_inicial,
                tipo=tipo,
                titular=f"{usuario.nombre} {usuario.apellido}",
            )
            self.cuentas[nuevo_numero] = nueva_cuenta
            usuario.cuentas.append(nueva_cuenta)
            return nueva_cuenta

    def __str__(self):
        with self.mutex:
            return "[Banco: " + self.nombre + " | Cuentas: " + str(len(self.cuentas)) + "]"
