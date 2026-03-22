import sqlite3

# Clase Modelo (Utilizando POO para encapsular la data)
class EquipoTactico:
    def __init__(self, id_equipo, tipo, estado_operativo, disponibilidad):
        self.id_equipo = id_equipo
        self.tipo = tipo
        self.estado_operativo = estado_operativo
        self.disponibilidad = disponibilidad

# Clase Gestora (POO + Colecciones + SQLite)
class InventarioEquipos:
    def __init__(self, db_name="unmo.db"):
        self.db_name = db_name
        # USO DE COLECCIONES: 'equipos' es un diccionario. 
        # Esto permite una búsqueda eficiente en memoria (O(1)) por id_equipo.
        self.equipos = {} 
        self._inicializar_bd()
        self.cargar_desde_bd()

    def _inicializar_bd(self):
        """Crea la tabla si no existe en la base de datos SQLite"""
        conexion = sqlite3.connect(self.db_name)
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS equipos (
                id_equipo TEXT PRIMARY KEY,
                tipo TEXT NOT NULL,
                estado_operativo TEXT NOT NULL,
                disponibilidad TEXT NOT NULL
            )
        ''')
        conexion.commit()
        conexion.close()

    def cargar_desde_bd(self):
        """Carga datos desde SQLite al diccionario usando tuplas"""
        self.equipos.clear()
        conexion = sqlite3.connect(self.db_name)
        cursor = conexion.cursor()
        cursor.execute('SELECT id_equipo, tipo, estado_operativo, disponibilidad FROM equipos')
        # fetchall devuelve una lista de tuplas
        filas = cursor.fetchall()
        for fila in filas:
            equipo = EquipoTactico(fila[0], fila[1], fila[2], fila[3])
            # Almacena en la colección (diccionario)
            self.equipos[equipo.id_equipo] = equipo
        conexion.close()

    def agregar_equipo(self, equipo):
        """Operación CRUD: CREATE"""
        # 1. Guarda en colección memoria
        self.equipos[equipo.id_equipo] = equipo
        # 2. Guarda en SQLite
        conexion = sqlite3.connect(self.db_name)
        cursor = conexion.cursor()
        cursor.execute(
            'INSERT INTO equipos (id_equipo, tipo, estado_operativo, disponibilidad) VALUES (?, ?, ?, ?)',
            (equipo.id_equipo, equipo.tipo, equipo.estado_operativo, equipo.disponibilidad)
        )
        conexion.commit()
        conexion.close()

    def obtener_todos(self):
        """Operación CRUD: READ ALL"""
        return list(self.equipos.values())
        
    def obtener_equipo(self, id_equipo):
        """Operación CRUD: READ ONE (Búsqueda rápida en diccionario)"""
        return self.equipos.get(id_equipo)

    def actualizar_equipo(self, id_equipo, tipo, estado, disponibilidad):
        """Operación CRUD: UPDATE"""
        if id_equipo in self.equipos:
            # 1. Actualiza en memoria
            self.equipos[id_equipo].tipo = tipo
            self.equipos[id_equipo].estado_operativo = estado
            self.equipos[id_equipo].disponibilidad = disponibilidad
            
            # 2. Actualiza en BD
            conexion = sqlite3.connect(self.db_name)
            cursor = conexion.cursor()
            cursor.execute(
                'UPDATE equipos SET tipo = ?, estado_operativo = ?, disponibilidad = ? WHERE id_equipo = ?',
                (tipo, estado, disponibilidad, id_equipo)
            )
            conexion.commit()
            conexion.close()

    def eliminar_equipo(self, id_equipo):
        """Operación CRUD: DELETE"""
        if id_equipo in self.equipos:
            # 1. Elimina de memoria
            del self.equipos[id_equipo]
            # 2. Elimina de BD
            conexion = sqlite3.connect(self.db_name)
            cursor = conexion.cursor()
            cursor.execute('DELETE FROM equipos WHERE id_equipo = ?', (id_equipo,))
            conexion.commit()
            conexion.close()
