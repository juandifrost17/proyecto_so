import threading


class CuentaBilletera:
    def __init__(self, numero_cuenta: str, saldo_inicial: float, tipo: str, titular: str = "No asignado"):
        numero_cuenta = numero_cuenta.strip()
        tipo = tipo.strip().lower()
        titular = titular.strip()

        if not numero_cuenta:
            raise ValueError("El número de cuenta no puede estar vacío.")
        if saldo_inicial < 0:
            raise ValueError("El saldo inicial no puede ser negativo.")
        if tipo not in ["ahorros", "corriente"]:
            raise ValueError("El tipo de cuenta debe ser 'ahorros' o 'corriente'.")

        self.numero_cuenta = numero_cuenta
        self.saldo = saldo_inicial
        self.tipo = tipo
        self.titular = titular or "No asignado"
        self.mutex = threading.Lock()
        self.historial_transacciones = []

    def descripcion_corta(self):
        return (
            f"Titular: {self.titular} | Cuenta {self.tipo.capitalize()} | "
            f"Número: {self.numero_cuenta} | Saldo: ${self.saldo:.2f}"
        )

    def __str__(self):
        return (
            f"[Titular: {self.titular} | Cuenta {self.tipo.capitalize()}: {self.numero_cuenta} | "
            f"Saldo: ${self.saldo:.2f}]"
        )
