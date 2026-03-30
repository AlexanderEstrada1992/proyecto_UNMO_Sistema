class UsuarioForm:
    def __init__(self, data, es_edicion=False):
        self.data = data
        self.es_edicion = es_edicion
        self.errores = []

    def validar(self):
        if not self.data.get('nombre'): self.errores.append("El Nombre es requerido.")
        if not self.data.get('mail'): self.errores.append("El Correo es requerido.")
        if not self.es_edicion and not self.data.get('password'): 
            self.errores.append("La Contraseña es requerida.")
        return len(self.errores) == 0
