from Conexion.conexion import obtener_conexion
from models.asignacion import Asignacion

class AsignacionService:
    @staticmethod
    def obtener_todas(search_query=None):
        """Obtiene todas las asignaciones con los nombres de equipos y usuarios (JOIN)"""
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        query = '''
            SELECT a.id_asignacion, a.id_equipo, a.id_usuario, a.fecha_asignacion, a.observaciones,
                   e.tipo as equipo_tipo, u.nombre as usuario_nombre
            FROM asignaciones a
            JOIN equipos e ON a.id_equipo = e.id_equipo
            JOIN usuarios u ON a.id_usuario = u.id_usuario
        '''
        
        if search_query:
            query += " WHERE a.id_equipo LIKE %s OR u.nombre LIKE %s OR e.tipo LIKE %s"
            like_term = f"%{search_query}%"
            cursor.execute(query, (like_term, like_term, like_term))
        else:
            cursor.execute(query)
            
        filas = cursor.fetchall()
        conexion.close()
        return filas

    @staticmethod
    def obtener_por_id(id_asignacion):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM asignaciones WHERE id_asignacion = %s", (id_asignacion,))
        fila = cursor.fetchone()
        conexion.close()
        return Asignacion(**fila) if fila else None

    @staticmethod
    def agregar(asignacion):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO asignaciones (id_equipo, id_usuario, fecha_asignacion, observaciones) VALUES (%s, %s, %s, %s)",
            (asignacion.id_equipo, asignacion.id_usuario, asignacion.fecha_asignacion, asignacion.observaciones)
        )
        conexion.commit()
        conexion.close()

    @staticmethod
    def actualizar(id_asignacion, asignacion):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "UPDATE asignaciones SET id_equipo=%s, id_usuario=%s, fecha_asignacion=%s, observaciones=%s WHERE id_asignacion=%s",
            (asignacion.id_equipo, asignacion.id_usuario, asignacion.fecha_asignacion, asignacion.observaciones, id_asignacion)
        )
        conexion.commit()
        conexion.close()

    @staticmethod
    def eliminar(id_asignacion):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM asignaciones WHERE id_asignacion = %s", (id_asignacion,))
        conexion.commit()
        conexion.close()
