import time
from excepciones import SaldoInsuficienteException, MontoInvalidoException
from bitacora import logger


def _emitir(mensaje, mostrar=True, nivel="info"):
    if mostrar:
        print(mensaje)

    if nivel == "error":
        logger.error("%s", mensaje)
    elif nivel == "warning":
        logger.warning("%s", mensaje)
    else:
        logger.info("%s", mensaje)


class GestorTransacciones:
    @staticmethod
    def retirar(cuenta, monto, actor="Sistema", demora_critica=1.0, mostrar_mutex=True):
        if monto <= 0:
            mensaje = "Monto de retiro inválido."
            logger.error("%s | %s", actor, mensaje)
            raise MontoInvalidoException(mensaje)

        _emitir(
            f"{actor} | Solicita retiro de ${monto:.2f} en cuenta {cuenta.numero_cuenta}",
            mostrar_mutex,
        )
        _emitir(
            f"{actor} | Intentando adquirir mutex de la cuenta {cuenta.numero_cuenta}...",
            mostrar_mutex,
        )

        cuenta.mutex.acquire()
        try:
            _emitir(f"{actor} | Mutex adquirido.", mostrar_mutex)
            _emitir(f"{actor} | Entra a la sección crítica.", mostrar_mutex)
            _emitir(f"{actor} | Saldo antes del retiro: ${cuenta.saldo:.2f}", mostrar_mutex)

            time.sleep(demora_critica)

            if cuenta.saldo < monto:
                mensaje = f"{actor} | Error: saldo insuficiente para retirar."
                logger.error("%s", mensaje)
                raise SaldoInsuficienteException("Saldo insuficiente para retirar.")

            saldo_anterior = cuenta.saldo
            cuenta.saldo -= monto
            cuenta.historial_transacciones.append(
                f"{actor} | Retiro: -${monto:.2f} | Saldo anterior: ${saldo_anterior:.2f} | Nuevo saldo: ${cuenta.saldo:.2f}"
            )

            _emitir(
                f"{actor} | Saldo actualizado después del retiro: ${cuenta.saldo:.2f}",
                mostrar_mutex,
            )

            return cuenta.saldo
        finally:
            _emitir(f"{actor} | Sale de la sección crítica.", mostrar_mutex)
            _emitir(
                f"{actor} | Libera el mutex de la cuenta {cuenta.numero_cuenta}.\n",
                mostrar_mutex,
            )
            cuenta.mutex.release()

    @staticmethod
    def depositar(cuenta, monto, actor="Sistema", demora_critica=1.0, mostrar_mutex=True):
        if monto <= 0:
            mensaje = "Monto de depósito inválido."
            logger.error("%s | %s", actor, mensaje)
            raise MontoInvalidoException(mensaje)

        _emitir(
            f"{actor} | Solicita depósito de ${monto:.2f} en cuenta {cuenta.numero_cuenta}",
            mostrar_mutex,
        )
        _emitir(
            f"{actor} | Intentando adquirir mutex de la cuenta {cuenta.numero_cuenta}...",
            mostrar_mutex,
        )

        cuenta.mutex.acquire()
        try:
            _emitir(f"{actor} | Mutex adquirido.", mostrar_mutex)
            _emitir(f"{actor} | Entra a la sección crítica.", mostrar_mutex)
            _emitir(f"{actor} | Saldo antes del depósito: ${cuenta.saldo:.2f}", mostrar_mutex)

            time.sleep(demora_critica)

            saldo_anterior = cuenta.saldo
            cuenta.saldo += monto
            cuenta.historial_transacciones.append(
                f"{actor} | Depósito: +${monto:.2f} | Saldo anterior: ${saldo_anterior:.2f} | Nuevo saldo: ${cuenta.saldo:.2f}"
            )

            _emitir(
                f"{actor} | Saldo actualizado después del depósito: ${cuenta.saldo:.2f}",
                mostrar_mutex,
            )

            return cuenta.saldo
        finally:
            _emitir(f"{actor} | Sale de la sección crítica.", mostrar_mutex)
            _emitir(
                f"{actor} | Libera el mutex de la cuenta {cuenta.numero_cuenta}.\n",
                mostrar_mutex,
            )
            cuenta.mutex.release()

    @staticmethod
    def transferir(
        cuenta_origen,
        cuenta_destino,
        monto,
        actor="Sistema",
        demora_critica=1.0,
        mostrar_mutex=True,
    ):
        if monto <= 0:
            mensaje = "Monto de transferencia inválido."
            logger.error("%s | %s", actor, mensaje)
            raise MontoInvalidoException(mensaje)
        if cuenta_origen.numero_cuenta == cuenta_destino.numero_cuenta:
            mensaje = "No se puede transferir a la misma cuenta."
            logger.error("%s | %s", actor, mensaje)
            raise MontoInvalidoException(mensaje)

        cuentas_ordenadas = sorted(
            [cuenta_origen, cuenta_destino], key=lambda cuenta: cuenta.numero_cuenta
        )
        primera_cuenta = cuentas_ordenadas[0]
        segunda_cuenta = cuentas_ordenadas[1]

        _emitir(
            f"{actor} | Solicita transferencia de ${monto:.2f} desde {cuenta_origen.numero_cuenta} hacia {cuenta_destino.numero_cuenta}",
            mostrar_mutex,
        )
        _emitir(
            f"{actor} | Intentando adquirir mutex de {primera_cuenta.numero_cuenta} y luego de {segunda_cuenta.numero_cuenta}...",
            mostrar_mutex,
        )

        primera_cuenta.mutex.acquire()
        try:
            _emitir(
                f"{actor} | Primer mutex adquirido: cuenta {primera_cuenta.numero_cuenta}",
                mostrar_mutex,
            )

            segunda_cuenta.mutex.acquire()
            try:
                _emitir(
                    f"{actor} | Segundo mutex adquirido: cuenta {segunda_cuenta.numero_cuenta}",
                    mostrar_mutex,
                )
                _emitir(
                    f"{actor} | Entra a la sección crítica de transferencia.",
                    mostrar_mutex,
                )
                _emitir(
                    f"{actor} | Saldo origen antes de transferir: ${cuenta_origen.saldo:.2f}",
                    mostrar_mutex,
                )
                _emitir(
                    f"{actor} | Saldo destino antes de transferir: ${cuenta_destino.saldo:.2f}",
                    mostrar_mutex,
                )

                time.sleep(demora_critica)

                if cuenta_origen.saldo < monto:
                    mensaje = f"{actor} | Error: saldo insuficiente para transferir."
                    logger.error("%s", mensaje)
                    raise SaldoInsuficienteException("Saldo insuficiente para transferir.")

                saldo_origen_anterior = cuenta_origen.saldo
                saldo_destino_anterior = cuenta_destino.saldo

                cuenta_origen.saldo -= monto
                cuenta_destino.saldo += monto

                cuenta_origen.historial_transacciones.append(
                    f"{actor} | Transferencia enviada: -${monto:.2f} a {cuenta_destino.numero_cuenta} | Saldo anterior: ${saldo_origen_anterior:.2f} | Nuevo saldo: ${cuenta_origen.saldo:.2f}"
                )
                cuenta_destino.historial_transacciones.append(
                    f"{actor} | Transferencia recibida: +${monto:.2f} de {cuenta_origen.numero_cuenta} | Saldo anterior: ${saldo_destino_anterior:.2f} | Nuevo saldo: ${cuenta_destino.saldo:.2f}"
                )

                _emitir(f"{actor} | Transferencia completada con éxito.", mostrar_mutex)
                _emitir(
                    f"{actor} | Nuevo saldo origen: ${cuenta_origen.saldo:.2f}",
                    mostrar_mutex,
                )
                _emitir(
                    f"{actor} | Nuevo saldo destino: ${cuenta_destino.saldo:.2f}",
                    mostrar_mutex,
                )

                return cuenta_origen.saldo
            finally:
                _emitir(
                    f"{actor} | Libera el segundo mutex: cuenta {segunda_cuenta.numero_cuenta}",
                    mostrar_mutex,
                )
                segunda_cuenta.mutex.release()
        finally:
            _emitir(
                f"{actor} | Libera el primer mutex: cuenta {primera_cuenta.numero_cuenta}\n",
                mostrar_mutex,
            )
            primera_cuenta.mutex.release()

    @staticmethod
    def consultar(cuenta, actor="Sistema", mostrar_mutex=True):
        _emitir(
            f"{actor} | Solicita consulta de saldo en cuenta {cuenta.numero_cuenta}",
            mostrar_mutex,
        )
        _emitir(
            f"{actor} | Intentando adquirir mutex de la cuenta {cuenta.numero_cuenta}...",
            mostrar_mutex,
        )

        cuenta.mutex.acquire()
        try:
            _emitir(f"{actor} | Mutex adquirido para consulta.", mostrar_mutex)
            _emitir(f"{actor} | Saldo consultado: ${cuenta.saldo:.2f}", mostrar_mutex)

            cuenta.historial_transacciones.append(
                f"{actor} | Consulta de saldo: ${cuenta.saldo:.2f}"
            )
            return round(cuenta.saldo, 2)
        finally:
            _emitir(f"{actor} | Libera el mutex después de consultar.\n", mostrar_mutex)
            cuenta.mutex.release()
