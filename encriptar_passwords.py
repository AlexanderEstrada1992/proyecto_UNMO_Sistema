from werkzeug.security import generate_password_hash
from Conexion.conexion import obtener_conexion

def migrar_passwords():
    print("Iniciando migración de contraseñas...")
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_usuario, password FROM usuarios")
    usuarios = cursor.fetchall()
    
    modificados = 0
    for u in usuarios:
        # Verifica si ya está encriptada (scrypt o pbkdf2)
        if not u['password'].startswith('scrypt:') and not u['password'].startswith('pbkdf2:'):
            nueva_pass = generate_password_hash(u['password'])
            cursor.execute("UPDATE usuarios SET password = %s WHERE id_usuario = %s", (nueva_pass, u['id_usuario']))
            modificados += 1
            
    conexion.commit()
    conexion.close()
    print(f"Migración completada. Modificados {modificados} usuarios a Hash Seguro.")

if __name__ == '__main__':
    migrar_passwords()
