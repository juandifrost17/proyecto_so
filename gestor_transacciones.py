from excepciones import SaldoInsuficienteException, MontoInvalidoException

class GestorTransacciones:
    @staticmethod
    def retirar(cuenta, monto):
        if monto <= 0:
            raise MontoInvalidoException("Monto de retiro inválido.")
        with cuenta.mutex:
            if cuenta.saldo < monto:
                raise SaldoInsuficienteException("Saldo insuficiente para retirar.")
            cuenta.saldo -= monto
            cuenta.historial_transacciones.append("Retiro: -$" + str(monto))
            print("Retiro exitoso de: $" + str(monto))
            return cuenta.saldo

    @staticmethod
    def depositar(cuenta, monto):
        if monto <= 0:
            raise MontoInvalidoException("Monto de depósito inválido.")
        with cuenta.mutex:
            cuenta.saldo += monto
            cuenta.historial_transacciones.append("Depósito: +$" + str(monto))
            print("Depósito de $" + str(monto) + " recibido con éxito.")
            return "Éxito"
        
    @staticmethod
    def transferir(cuenta_origen, cuenta_destino, monto):
        if monto <= 0:
            raise MontoInvalidoException("Monto de transferencia inválido.")
        cuentas = sorted([cuenta_origen, cuenta_destino], key=lambda c: c.numero_cuenta)
        primer_lock = cuentas[0].mutex
        segundo_lock = cuentas[1].mutex
        with primer_lock:
            with segundo_lock:
                if cuenta_origen.saldo < monto:
                    raise SaldoInsuficienteException("Saldo insuficiente para transferir.")
                cuenta_origen.saldo -= monto
                cuenta_destino.saldo += monto
                cuenta_origen.historial_transacciones.append("Transferencia enviada: -$" + str(monto) + " a " + cuenta_destino.numero_cuenta)
                cuenta_destino.historial_transacciones.append("Transferencia recibida: +$" + str(monto) + " de " + cuenta_origen.numero_cuenta)
                print("Transferencia de $" + str(monto) + " exitosa.")
                return cuenta_origen.saldo

    @staticmethod
    def consultar(cuenta):
        with cuenta.mutex:
            cuenta.historial_transacciones.append("Consulta de saldo: $" + str(round(cuenta.saldo, 2)))
            print("Tu saldo actual es: $" + str(round(cuenta.saldo, 2)))
            return round(cuenta.saldo, 2)
