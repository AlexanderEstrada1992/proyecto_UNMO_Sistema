from flask_sqlalchemy import SQLAlchemy

# Inicializamos SQLAlchemy sin pasarle la app todavía
db = SQLAlchemy()

# Definimos el modelo de datos (Reemplaza a la clase POO manual de la semana anterior)
class EquipoTactico(db.Model):
    __tablename__ = 'equipos'
    
    id_equipo = db.Column(db.String(50), primary_key=True)
    tipo = db.Column(db.String(100), nullable=False)
    estado_operativo = db.Column(db.String(50), nullable=False)
    disponibilidad = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        """Convierte el objeto a diccionario para facilitar el guardado en JSON/CSV"""
        return {
            "id_equipo": self.id_equipo,
            "tipo": self.tipo,
            "estado_operativo": self.estado_operativo,
            "disponibilidad": self.disponibilidad
        }
