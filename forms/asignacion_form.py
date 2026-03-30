class AsignacionForm:
    def __init__(self, data):
        self.data = data
        self.errores = []

    def validar(self):
        if not self.data.get('id_equipo'): self.errores.append("Debe seleccionar un Equipo.")
        if not self.data.get('id_usuario'): self.errores.append("Debe seleccionar un Usuario.")
        if not self.data.get('fecha_asignacion'): self.errores.append("La Fecha de Asignación es requerida.")
        return len(self.errores) == 0
