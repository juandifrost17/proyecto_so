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
        operaciones = ["retiro", "deposito", "consulta"]
        for _ in range(3):
            tipo = random.choice(operaciones)
            monto = round(random.uniform(10.0, 100.0), 2)

            try:
                cuenta = self.banco.obtener_cuenta(self.usuario.cuenta.numero_cuenta)

                if tipo == "retiro":
                    GestorTransacciones.retirar(cuenta, monto)
                    print("Cajero " + str(self.id_cajero) + " | " + self.usuario.nombre + " | Retiro $" + str(monto) + " -> Éxito")
                elif tipo == "deposito":
                    GestorTransacciones.depositar(cuenta, monto)
                    print("Cajero " + str(self.id_cajero) + " | " + self.usuario.nombre + " | Depósito $" + str(monto) + " -> Éxito")
                elif tipo == "consulta":
                    saldo_actual = GestorTransacciones.consultar(cuenta)
                    print("Cajero " + str(self.id_cajero) + " | " + self.usuario.nombre + " | Consulta -> Saldo: $" + str(saldo_actual))

            except SaldoInsuficienteException as e:
                print("Cajero " + str(self.id_cajero) + " | " + self.usuario.nombre + " | Error: " + str(e))
            except MontoInvalidoException as e:
                print("Cajero " + str(self.id_cajero) + " | " + self.usuario.nombre + " | Error: " + str(e))

            time.sleep(random.uniform(0.1, 0.5))