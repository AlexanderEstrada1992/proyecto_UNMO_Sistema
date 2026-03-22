import pymysql

def obtener_conexion():
    """
    Establece la conexión con la base de datos MySQL local.
    Ajusta el 'password' si tu servidor MySQL tiene contraseña.
    """
    host = 'localhost'
    usuario = 'root'
    password = ''  # PON TU CONTRASEÑA AQUÍ SI TIENES UNA EN MYSQL WORKBENCH
    base_de_datos = 'unmo_db'
    
    conexion = pymysql.connect(
        host=host,
        user=usuario,
        password=password,
        database=base_de_datos,
        # DictCursor permite que las filas se manejen como diccionarios (igual que sqlalchemy)
        cursorclass=pymysql.cursors.DictCursor
    )
    return conexion
