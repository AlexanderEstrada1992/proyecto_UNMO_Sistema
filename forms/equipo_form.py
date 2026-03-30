class EquipoForm:
    def __init__(self, data):
        self.data = data
        self.errores = []

    def validar(self):
        if not self.data.get('id_equipo'): self.errores.append("El ID de Equipo es requerido.")
        if not self.data.get('tipo'): self.errores.append("El tipo de Equipo es requerido.")
        if not self.data.get('estado'): self.errores.append("El Estado Operativo es requerido.")
        if not self.data.get('disponibilidad'): self.errores.append("La Disponibilidad es requerida.")
        return len(self.errores) == 0
