import random
import threading
import time
from gestor_transacciones import GestorTransacciones
from excepciones import SaldoInsuficienteException, MontoInvalidoException
from bitacora import logger


class SimulacionCajero(threading.Thread):
    def __init__(
        self,
        id_cajero,
        banco,
        usuario=None,
        modo="aleatorio",
        cuenta=None,
        operacion=None,
        monto=None,
        iteraciones=3,
        operaciones_disponibles=None,
        demora_critica=1.0,
    ):
        super().__init__(name=f"Cajero-{id_cajero}")
        self.id_cajero = id_cajero
        self.banco = banco
        self.usuario = usuario
        self.modo = modo
        self.cuenta = cuenta
        self.operacion = operacion
        self.monto = monto
        self.iteraciones = iteraciones
        self.operaciones_disponibles = operaciones_disponibles or [
            "retiro",
            "deposito",
            "consulta",
            "transferencia",
        ]
        self.demora_critica = demora_critica
        self.actor = "Cajero " + str(self.id_cajero)

    def run(self):
        if self.modo == "predefinido":
            self._ejecutar_operacion_predefinida()
        else:
            self._ejecutar_simulacion_general()

    def _ejecutar_operacion_predefinida(self):
        if self.cuenta is None or self.operacion is None:
            mensaje = self.actor + " | Configuración inválida para simulación predefinida."
            print(mensaje)
            logger.error("%s", mensaje)
            return

        if self.operacion != "consulta" and self.monto is None:
            mensaje = self.actor + " | Falta el monto para la operación predefinida."
            print(mensaje)
            logger.error("%s", mensaje)
            return

        try:
            self._ejecutar_operacion(self.cuenta, self.operacion, self.monto)
        except (SaldoInsuficienteException, MontoInvalidoException) as error:
            mensaje = self.actor + " | Error: " + str(error)
            print(mensaje)
            logger.error("%s", mensaje)

    def _ejecutar_simulacion_general(self):
        cuentas_disponibles = self.banco.listar_cuentas()
        if not cuentas_disponibles:
            mensaje = self.actor + " | No hay cuentas registradas para simular."
            print(mensaje)
            logger.warning("%s", mensaje)
            return

        for _ in range(self.iteraciones):
            operacion = random.choice(self.operaciones_disponibles)
            cuenta = random.choice(cuentas_disponibles)

            try:
                if operacion == "transferencia":
                    monto = round(random.uniform(10.0, 100.0), 2)
                    cuentas_destino = [
                        cuenta_destino
                        for cuenta_destino in cuentas_disponibles
                        if cuenta_destino.numero_cuenta != cuenta.numero_cuenta
                    ]

                    if not cuentas_destino:
                        mensaje = self.actor + " | Transferencia omitida: no hay otra cuenta destino."
                        print(mensaje)
                        logger.info("%s", mensaje)
                    else:
                        cuenta_destino = random.choice(cuentas_destino)
                        GestorTransacciones.transferir(
                            cuenta,
                            cuenta_destino,
                            monto,
                            actor=self.actor,
                            demora_critica=self.demora_critica,
                            mostrar_mutex=True,
                        )
                elif operacion == "consulta":
                    self._ejecutar_operacion(cuenta, operacion, None)
                else:
                    monto = round(random.uniform(10.0, 100.0), 2)
                    self._ejecutar_operacion(cuenta, operacion, monto)

            except (SaldoInsuficienteException, MontoInvalidoException) as error:
                mensaje = self.actor + " | Error: " + str(error)
                print(mensaje)
                logger.error("%s", mensaje)

            time.sleep(random.uniform(0.2, 0.6))

    def _ejecutar_operacion(self, cuenta, operacion, monto=None):
        if operacion == "retiro":
            GestorTransacciones.retirar(
                cuenta,
                monto,
                actor=self.actor,
                demora_critica=self.demora_critica,
                mostrar_mutex=True,
            )
        elif operacion == "deposito":
            GestorTransacciones.depositar(
                cuenta,
                monto,
                actor=self.actor,
                demora_critica=self.demora_critica,
                mostrar_mutex=True,
            )
        elif operacion == "consulta":
            GestorTransacciones.consultar(
                cuenta,
                actor=self.actor,
                mostrar_mutex=True,
            )
        else:
            mensaje = self.actor + " | Operación no reconocida: " + str(operacion)
            print(mensaje)
            logger.error("%s", mensaje)