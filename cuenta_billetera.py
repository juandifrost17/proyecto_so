import threading

class CuentaBilletera:
    def __init__(self, numero_cuenta: str, saldo_inicial: float, tipo: str):
        self.numero_cuenta = numero_cuenta
        self.saldo = saldo_inicial
        self.tipo = tipo
        self.mutex = threading.Lock()
        self.historial_transacciones = []

    def __str__(self):
        return "[Cuenta " + self.tipo.capitalize() + ": " + self.numero_cuenta + " | Saldo: $" + str(round(self.saldo, 2)) + "]"