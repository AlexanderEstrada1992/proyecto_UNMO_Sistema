from Conexion.conexion import obtener_conexion
from inventario.inventario import guardar_persistencia_archivos
import os

def poblar():
    equipos_demo = [
        {"id_equipo": "EQ-001", "tipo": "Escudo Antidisturbios Policarbonato", "estado_operativo": "Óptimo", "disponibilidad": "Disponible en Bodega"},
        {"id_equipo": "EQ-002", "tipo": "Casco Táctico con Visor", "estado_operativo": "Bueno", "disponibilidad": "Asignado a Patrulla"},
        {"id_equipo": "EQ-003", "tipo": "Chaleco Antibalas Nivel III", "estado_operativo": "Requiere Mantenimiento", "disponibilidad": "En Taller"},
        {"id_equipo": "EQ-004", "tipo": "Bastón PR-24 (Tolete)", "estado_operativo": "Óptimo", "disponibilidad": "Disponible en Bodega"},
        {"id_equipo": "EQ-005", "tipo": "Máscara Antigás", "estado_operativo": "Bueno", "disponibilidad": "Asignado a Patrulla"},
        {"id_equipo": "EQ-006", "tipo": "Radio de Comunicación Tetra", "estado_operativo": "Óptimo", "disponibilidad": "Disponible en Bodega"}
    ]
    
    print("Conectando a MySQL...")
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    
    # Limpiamos la tabla para que no haya errores de ID duplicado si lo corres dos veces
    cursor.execute("TRUNCATE TABLE equipos")
    
    # Archivos planos: limpiamos los archivos txt, csv y json si existen para reiniciarlos
    for arch in ['datos.txt', 'datos.json', 'datos.csv']:
        ruta = os.path.join('inventario', 'data', arch)
        if os.path.exists(ruta):
            # vaciarlos
            with open(ruta, 'w', encoding='utf-8') as f:
                if arch == 'datos.json':
                    f.write("[]")
                elif arch == 'datos.csv':
                    f.write("id_equipo,tipo,estado_operativo,disponibilidad\n")
                else:
                    pass
    
    # Insertar la información
    for eq in equipos_demo:
        # En MySQL
        cursor.execute(
            "INSERT INTO equipos (id_equipo, tipo, estado_operativo, disponibilidad) VALUES (%s, %s, %s, %s)",
            (eq["id_equipo"], eq["tipo"], eq["estado_operativo"], eq["disponibilidad"])
        )
        # En los Archivos Planos (TXT, JSON, CSV)
        guardar_persistencia_archivos(eq)
        
    conexion.commit()
    conexion.close()
    print("6 equipos tácticos insertados con éxito en la Base de Datos y en los datos Locales.")

if __name__ == '__main__':
    poblar()
