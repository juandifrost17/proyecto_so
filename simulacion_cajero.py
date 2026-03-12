import threading
import time
import random
from gestor_transacciones import GestorTransacciones
from excepciones import SaldoInsuficienteException, MontoInvalidoException

class SimulacionCajero(threading.Thread):
    def __init__(self, id_cajero, usuario, banco):
        super().__init__()
        self.id_cajero = id_cajero
        self.usuario = usuario
        self.banco = banco

    def run(self):
        if not self.usuario.cuentas:
            print("Cajero " + str(self.id_cajero) + " | Error: El usuario " + self.usuario.nombre + " no tiene cuentas.")
            return

        operaciones = ["retiro", "deposito", "consulta"]
        for _ in range(3):
            tipo = random.choice(operaciones)
            monto = round(random.uniform(10.0, 100.0), 2)
            cuenta_seleccionada = random.choice(self.usuario.cuentas)

            try:
                cuenta = self.banco.obtener_cuenta(cuenta_seleccionada.numero_cuenta)

                if tipo == "retiro":
                    saldo_actual = GestorTransacciones.retirar(cuenta, monto)
                    print("Cajero " + str(self.id_cajero) + " | " + self.usuario.nombre + " (" + cuenta.tipo + ") | Retiro $" + str(monto) + " -> Éxito. Saldo: $" + str(round(saldo_actual, 2)))
                elif tipo == "deposito":
                    saldo_actual = GestorTransacciones.depositar(cuenta, monto)
                    print("Cajero " + str(self.id_cajero) + " | " + self.usuario.nombre + " (" + cuenta.tipo + ") | Depósito $" + str(monto) + " -> Éxito. Saldo: $" + str(round(saldo_actual, 2)))
                elif tipo == "consulta":
                    saldo_actual = GestorTransacciones.consultar(cuenta)
                    print("Cajero " + str(self.id_cajero) + " | " + self.usuario.nombre + " (" + cuenta.tipo + ") | Consulta -> Saldo: $" + str(saldo_actual))

            except SaldoInsuficienteException as e:
                print("Cajero " + str(self.id_cajero) + " | " + self.usuario.nombre + " (" + cuenta_seleccionada.tipo + ") | Error: " + str(e))
            except MontoInvalidoException as e:
                print("Cajero " + str(self.id_cajero) + " | " + self.usuario.nombre + " (" + cuenta_seleccionada.tipo + ") | Error: " + str(e))

            time.sleep(random.uniform(0.1, 0.5))