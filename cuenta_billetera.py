import threading

class CuentaBilletera:
    def __init__(self, numero_cuenta: str, saldo_inicial: float, tipo: str):
        numero_cuenta = numero_cuenta.strip()
        tipo = tipo.strip().lower()

        if not numero_cuenta:
            raise ValueError("El número de cuenta no puede estar vacío.")
        if saldo_inicial < 0:
            raise ValueError("El saldo inicial no puede ser negativo.")
        if tipo not in ["ahorros", "corriente"]:
            raise ValueError("El tipo de cuenta debe ser 'ahorros' o 'corriente'.")

        self.numero_cuenta = numero_cuenta
        self.saldo = saldo_inicial
        self.tipo = tipo
        self.mutex = threading.Lock()
        self.historial_transacciones = []

    def __str__(self):
        return "[Cuenta " + self.tipo.capitalize() + ": " + self.numero_cuenta + " | Saldo: $" + str(round(self.saldo, 2)) + "]"