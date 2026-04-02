class Equipo:
    def __init__(self, id_equipo, tipo, estado_operativo, disponibilidad, activo=True):
        self.id_equipo = id_equipo
        self.tipo = tipo
        self.estado_operativo = estado_operativo
        self.disponibilidad = disponibilidad
        self.activo = activo
