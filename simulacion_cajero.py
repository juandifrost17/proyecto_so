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
        operaciones = ["retiro", "deposito", "consulta", "transferencia"]
        for _ in range(3):
            tipo = random.choice(operaciones)
            monto = round(random.uniform(10.0, 100.0), 2)
            cuenta_seleccionada = random.choice(self.usuario.cuentas)
            try:
                cuenta = self.banco.obtener_cuenta(cuenta_seleccionada.numero_cuenta)

                if tipo == "retiro":
                    saldo_actual = GestorTransacciones.retirar(cuenta, monto)
                    print("Cajero " + str(self.id_cajero) + " | " + self.usuario.nombre + " (" + cuenta.tipo + ") | Retiro $" + format(monto, '.2f') + " -> Éxito | Saldo restante: $" + format(saldo_actual, '.2f'))
                
                elif tipo == "deposito":
                    GestorTransacciones.depositar(cuenta, monto)
                    print("Cajero " + str(self.id_cajero) + " | " + self.usuario.nombre + " (" + cuenta.tipo + ") | Depósito $" + format(monto, '.2f') + " -> Éxito")
                elif tipo == "consulta":
                    saldo_actual = GestorTransacciones.consultar(cuenta)
                    print("Cajero " + str(self.id_cajero) + " | " + self.usuario.nombre + " (" + cuenta.tipo + ") | Consulta -> Saldo: $" + format(saldo_actual, '.2f'))
                elif tipo == "transferencia":
                    todas_las_cuentas = self.banco.listar_cuentas()
                    cuentas_destino_posibles = [c for c in todas_las_cuentas if c.numero_cuenta != cuenta.numero_cuenta]
                    if cuentas_destino_posibles:
                        cuenta_destino = random.choice(cuentas_destino_posibles)
                        saldo_actual = GestorTransacciones.transferir(cuenta, cuenta_destino, monto)
                        print("Cajero " + str(self.id_cajero) + " | " + self.usuario.nombre + " (" + cuenta.tipo + ") | Transferencia de $" + format(monto, '.2f') + " a cuenta " + cuenta_destino.numero_cuenta + " -> Éxito | Tu saldo restante: $" + format(saldo_actual, '.2f'))
                    else:
                        print("Cajero " + str(self.id_cajero) + " | " + self.usuario.nombre + " (" + cuenta.tipo + ") | Transferencia cancelada: No hay cuentas destino disponibles.")
            except SaldoInsuficienteException as e:
                print("Cajero " + str(self.id_cajero) + " | " + self.usuario.nombre + " (" + cuenta_seleccionada.tipo + ") | Error: " + str(e))
            except MontoInvalidoException as e:
                print("Cajero " + str(self.id_cajero) + " | " + self.usuario.nombre + " (" + cuenta_seleccionada.tipo + ") | Error: " + str(e))
            time.sleep(random.uniform(0.1, 0.5))
