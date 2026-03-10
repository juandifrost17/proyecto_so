class Usuario:
    def __init__(self, nombre, apellido, cedula, email, fecha_nacimiento, telefono, cuenta):
        self.nombre = nombre
        self.apellido = apellido
        self.cedula = cedula
        self.email = email
        self.fecha_nacimiento = fecha_nacimiento
        self.telefono = telefono
        self.cuenta = cuenta

    def __str__(self):
        texto = "[Usuario: " + self.nombre + " " + self.apellido + " | CI: " + self.cedula + " | " + str(self.cuenta) + "]"
        return texto