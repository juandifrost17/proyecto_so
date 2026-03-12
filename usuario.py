class Usuario:
    def __init__(self, nombre, apellido, cedula, email, fecha_nacimiento, telefono):
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula
        self.email = email
        self.fecha_nacimiento = fecha_nacimiento
        self.telefono = telefono
        self.cuentas = []
    
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