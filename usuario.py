from datetime import date
import re

class Usuario:
    def __init__(self, nombre, apellido, cedula, email, fecha_nacimiento, telefono):
        nombre = nombre.strip()
        apellido = apellido.strip()
        cedula = cedula.strip()
        email = email.strip().lower()
        telefono = telefono.strip()

        if not self._nombre_valido(nombre):
            raise ValueError("El nombre no puede estar vacío y no debe contener números.")
        if not self._nombre_valido(apellido):
            raise ValueError("El apellido no puede estar vacío y no debe contener números.")
        if not cedula.isdigit() or len(cedula) != 10:
            raise ValueError("La cédula debe contener exactamente 10 dígitos numéricos.")
        if not self._email_valido(email):
            raise ValueError("El email ingresado no es válido.")
        if not telefono.isdigit():
            raise ValueError("El teléfono debe contener solo números.")
        if not isinstance(fecha_nacimiento, date):
            raise ValueError("La fecha de nacimiento no es válida.")
        if fecha_nacimiento > date.today():
            raise ValueError("La fecha de nacimiento no puede ser futura.")

        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula
        self.email = email
        self.fecha_nacimiento = fecha_nacimiento
        self.telefono = telefono
        self.cuentas = []

    @staticmethod
    def _nombre_valido(texto):
        if not texto:
            return False
        return bool(re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", texto))

    @staticmethod
    def _email_valido(email):
        return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email))
    
    def tiene_cuenta_tipo(self, tipo):
        for cuenta in self.cuentas:
            if cuenta.tipo == tipo:
                return True
        return False

    def __str__(self):
        if not self.cuentas:
            cuentas_str = "Sin cuentas asignadas"
        else:
            cuentas_str = ", ".join(str(c) for c in self.cuentas)
        texto = "[Usuario: " + self.nombre + " " + self.apellido + " | CI: " + self.cedula + " | " + cuentas_str + "]"
        return texto