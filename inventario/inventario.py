import json
import csv
import os

# Establecer la carpeta data dentro de inventario
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

TXT_FILE = os.path.join(DATA_DIR, 'datos.txt')
JSON_FILE = os.path.join(DATA_DIR, 'datos.json')
CSV_FILE = os.path.join(DATA_DIR, 'datos.csv')

def guardar_en_txt(equipo_dict):
    """Guarda un registro en un archivo TXT plano"""
    with open(TXT_FILE, 'a', encoding='utf-8') as f:
        linea = f"{equipo_dict['id_equipo']} | {equipo_dict['tipo']} | {equipo_dict['estado_operativo']} | {equipo_dict['disponibilidad']}\n"
        f.write(linea)

def leer_txt():
    """Lee líneas del archivo TXT"""
    if not os.path.exists(TXT_FILE):
        return []
    with open(TXT_FILE, 'r', encoding='utf-8') as f:
        return f.readlines()

def guardar_en_json(equipo_dict):
    """Guarda un registro en un archivo JSON"""
    datos = []
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        except json.JSONDecodeError:
            datos = []
            
    datos.append(equipo_dict)
    
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def leer_json():
    """Lee el archivo JSON y lo retorna como lista de diccionarios"""
    if not os.path.exists(JSON_FILE):
        return []
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def guardar_en_csv(equipo_dict):
    """Guarda un registro en un archivo CSV"""
    archivo_existe = os.path.exists(CSV_FILE)
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        campos = ['id_equipo', 'tipo', 'estado_operativo', 'disponibilidad']
        writer = csv.DictWriter(f, fieldnames=campos)
        
        # Escribir la cabecera si el archivo es nuevo
        if not archivo_existe:
            writer.writeheader()
            
        writer.writerow(equipo_dict)

def leer_csv():
    """Lee el archivo CSV"""
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def guardar_persistencia_archivos(equipo_dict):
    """Llama a los 3 métodos para persistir en todos los formatos solicitados"""
    guardar_en_txt(equipo_dict)
    guardar_en_json(equipo_dict)
    guardar_en_csv(equipo_dict)
