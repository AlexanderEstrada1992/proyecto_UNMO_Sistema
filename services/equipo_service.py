from Conexion.conexion import obtener_conexion
from models.equipo import Equipo

class EquipoService:
    @staticmethod
    def obtener_todos():
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM equipos")
        filas = cursor.fetchall()
        conexion.close()
        return [Equipo(**fila) for fila in filas] if filas else []

    @staticmethod
    def obtener_por_id(id_equipo):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM equipos WHERE id_equipo = %s", (id_equipo,))
        fila = cursor.fetchone()
        conexion.close()
        return Equipo(**fila) if fila else None

    @staticmethod
    def agregar(equipo):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO equipos (id_equipo, tipo, estado_operativo, disponibilidad) VALUES (%s, %s, %s, %s)",
            (equipo.id_equipo, equipo.tipo, equipo.estado_operativo, equipo.disponibilidad)
        )
        conexion.commit()
        conexion.close()

    @staticmethod
    def actualizar(id_equipo, equipo):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE equipos SET tipo=%s, estado_operativo=%s, disponibilidad=%s WHERE id_equipo=%s",
            (equipo.tipo, equipo.estado_operativo, equipo.disponibilidad, id_equipo)
        )
        conexion.commit()
        conexion.close()

    @staticmethod
    def eliminar(id_equipo):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM equipos WHERE id_equipo = %s", (id_equipo,))
        conexion.commit()
        conexion.close()
