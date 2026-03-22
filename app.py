import os
from flask import Flask, render_template, request, redirect, url_for

# Nuevas importaciones para Persistencia Avanzada (Semana 12)
from inventario.bd import db, EquipoTactico
from inventario.inventario import guardar_persistencia_archivos, leer_txt, leer_json, leer_csv

app = Flask(__name__)

# Configuración de SQLite con SQLAlchemy (ORM)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'unmo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Crear tablas en SQLite si no existen
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

# === RUTAS CRUD PARA EQUIPOS (PERSISTENCIA DUAL: ORM + ARCHIVOS) ===

@app.route('/equipos')
def equipos():
    # Lectura usando SQLAlchemy ORM
    lista_equipos = EquipoTactico.query.all()
    return render_template('equipos.html', equipos=lista_equipos)

@app.route('/equipos/agregar', methods=['GET', 'POST'])
def agregar_equipo():
    if request.method == 'POST':
        id_equipo = request.form['id_equipo']
        tipo = request.form['tipo']
        estado = request.form['estado']
        disponibilidad = request.form['disponibilidad']
        
        # 1. Guardar en SQLite vía SQLAlchemy ORM
        nuevo_equipo = EquipoTactico(
            id_equipo=id_equipo, 
            tipo=tipo, 
            estado_operativo=estado, 
            disponibilidad=disponibilidad
        )
        db.session.add(nuevo_equipo)
        db.session.commit()
        
        # 2. Guardar en TXT, JSON, CSV
        guardar_persistencia_archivos(nuevo_equipo.to_dict())
        
        return redirect(url_for('equipos'))
        
    return render_template('formulario_equipo.html', equipo=None)

@app.route('/equipos/editar/<id_equipo>', methods=['GET', 'POST'])
def editar_equipo(id_equipo):
    equipo_actual = EquipoTactico.query.get(id_equipo)
    if not equipo_actual:
        return redirect(url_for('equipos'))
        
    if request.method == 'POST':
        equipo_actual.tipo = request.form['tipo']
        equipo_actual.estado_operativo = request.form['estado']
        equipo_actual.disponibilidad = request.form['disponibilidad']
        
        db.session.commit()
        # Se guarda el log de actualización en los archivos planos secuenciales
        guardar_persistencia_archivos(equipo_actual.to_dict())
        
        return redirect(url_for('equipos'))
        
    return render_template('formulario_equipo.html', equipo=equipo_actual)

@app.route('/equipos/eliminar/<id_equipo>')
def eliminar_equipo(id_equipo):
    equipo = EquipoTactico.query.get(id_equipo)
    if equipo:
        db.session.delete(equipo)
        db.session.commit()
    return redirect(url_for('equipos'))

# === NUEVA RUTA SEMANA 12: LEER DATA DE ARCHIVOS PLANOS ===
@app.route('/datos')
def datos():
    datos_txt = leer_txt()
    datos_json = leer_json()
    datos_csv = leer_csv()
    return render_template('datos.html', datos_txt=datos_txt, datos_json=datos_json, datos_csv=datos_csv)

# === RUTAS SECUNDARIAS ===
@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/servidor/<nombre>')
def servidor(nombre):
    return render_template('servidor.html', nombre=nombre)

if __name__ == '__main__':
    app.run(debug=True)
