from Conexion.conexion import obtener_conexion
from models.equipo import Equipo

class EquipoService:
    @staticmethod
    def obtener_todos(search_query=None):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        if search_query:
            query = "SELECT * FROM equipos WHERE activo = 1 AND (id_equipo LIKE %s OR tipo LIKE %s)"
            like_term = f"%{search_query}%"
            cursor.execute(query, (like_term, like_term))
        else:
            cursor.execute("SELECT * FROM equipos WHERE activo = 1")
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
        
        # Validar si tiene asignaciones
        cursor.execute("SELECT COUNT(*) as count FROM asignaciones WHERE id_equipo = %s", (id_equipo,))
        resultado = cursor.fetchone()
        
        if resultado and resultado['count'] > 0:
            conexion.close()
            return False # No se puede eliminar por integridad referencial
            
        cursor.execute("UPDATE equipos SET activo = 0 WHERE id_equipo = %s", (id_equipo,))
        conexion.commit()
        conexion.close()
        return True
