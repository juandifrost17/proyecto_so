import threading

class CuentaBilletera:
    def __init__(self, numero_cuenta: str, saldo_inicial: float):
        self.numero_cuenta = numero_cuenta
        self.saldo = saldo_inicial
        self.mutex = threading.Lock()
        self.historial_transacciones = []

    def __str__(self):
        texto = "[Cuenta: " + self.numero_cuenta + " | Saldo: $" + str(round(self.saldo, 2)) + "]"
        return texto