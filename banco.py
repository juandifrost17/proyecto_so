import threading
from cuenta_billetera import CuentaBilletera
from excepciones import UsuarioNoEncontradoException, AliasDuplicadoException

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
                raise UsuarioNoEncontradoException("La cuenta " + numero_cuenta + " no existe.")
            return self.cuentas[numero_cuenta]

    def listar_cuentas(self) -> list:
        with self.mutex:
            return list(self.cuentas.values())

    def __str__(self):
        with self.mutex:
            texto = "[Banco: " + self.nombre + " | Cuentas: " + str(len(self.cuentas)) + "]"
            return texto