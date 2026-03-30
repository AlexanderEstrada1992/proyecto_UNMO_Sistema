from Conexion.conexion import obtener_conexion
from models.usuario import Usuario
from werkzeug.security import generate_password_hash, check_password_hash

class UsuarioService:
    @staticmethod
    def obtener_todos():
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios")
        filas = cursor.fetchall()
        conexion.close()
        return [Usuario(**fila) for fila in filas] if filas else []

    @staticmethod
    def obtener_por_id(id_usuario):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        fila = cursor.fetchone()
        conexion.close()
        return Usuario(**fila) if fila else None

    @staticmethod
    def obtener_por_mail(mail):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE mail = %s", (mail,))
        fila = cursor.fetchone()
        conexion.close()
        return Usuario(**fila) if fila else None

    @staticmethod
    def agregar(usuario, encriptar=True):
        password = generate_password_hash(usuario.password) if encriptar else usuario.password
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, mail, password) VALUES (%s, %s, %s)",
            (usuario.nombre, usuario.mail, password)
        )
        conexion.commit()
        conexion.close()

    @staticmethod
    def actualizar(id_usuario, usuario, nueva_password=None):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        if nueva_password:
            password = generate_password_hash(nueva_password)
            cursor.execute(
                "UPDATE usuarios SET nombre=%s, mail=%s, password=%s WHERE id_usuario=%s",
                (usuario.nombre, usuario.mail, password, id_usuario)
            )
        else:
            cursor.execute(
                "UPDATE usuarios SET nombre=%s, mail=%s WHERE id_usuario=%s",
                (usuario.nombre, usuario.mail, id_usuario)
            )
        conexion.commit()
        conexion.close()

    @staticmethod
    def eliminar(id_usuario):
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        conexion.commit()
        conexion.close()
