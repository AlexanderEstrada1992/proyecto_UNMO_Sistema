from flask_login import UserMixin

class Usuario(UserMixin):
    def __init__(self, id_usuario, nombre, mail, password):
        self.id = str(id_usuario)  # Necesario para Flask-Login
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.mail = mail
        self.password = password
