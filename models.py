from flask_login import UserMixin
from Conexion.conexion import obtener_conexion

class Usuario(UserMixin):
    def __init__(self, id_usuario, nombre, mail, password):
        # Flask-Login requiere que el ID sea string accesible via property 'id'
        self.id = str(id_usuario)  
        self.nombre = nombre
        self.mail = mail
        self.password = password

    @staticmethod
    def get(user_id):
        """Busca al usuario por su ID interno en la base de datos MySQL"""
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (user_id,))
        dato = cursor.fetchone()
        conexion.close()
        
        if dato:
            return Usuario(dato['id_usuario'], dato['nombre'], dato['mail'], dato['password'])
        return None

    @staticmethod
    def get_by_mail(mail):
        """Busca al usuario por su correo para el Login"""
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE mail = %s", (mail,))
        dato = cursor.fetchone()
        conexion.close()
        
        if dato:
            return Usuario(dato['id_usuario'], dato['nombre'], dato['mail'], dato['password'])
        return None
