import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Conexion.conexion import obtener_conexion

def main():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    try:
        cursor.execute("ALTER TABLE equipos ADD COLUMN activo BOOLEAN DEFAULT TRUE")
        print("Column 'activo' added to 'equipos'.")
    except Exception as e:
        print("Error altering 'equipos' (might already exist):", e)
        
    try:
        cursor.execute("ALTER TABLE usuarios ADD COLUMN activo BOOLEAN DEFAULT TRUE")
        print("Column 'activo' added to 'usuarios'.")
    except Exception as e:
        print("Error altering 'usuarios' (might already exist):", e)
        
    conexion.commit()
    conexion.close()

if __name__ == "__main__":
    main()
