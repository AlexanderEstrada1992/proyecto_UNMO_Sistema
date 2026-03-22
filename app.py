from flask import Flask, render_template, request, redirect, url_for
from database import InventarioEquipos, EquipoTactico

app = Flask(__name__)

# Instanciar el gestor del inventario que conecta SQLite y usa colecciones
inventario = InventarioEquipos()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

# === RUTAS CRUD PARA EQUIPOS TÁCTICOS ===

@app.route('/equipos')
def equipos():
    # Leer todos desde el inventario (Colección)
    lista_equipos = inventario.obtener_todos()
    return render_template('equipos.html', equipos=lista_equipos)

@app.route('/equipos/agregar', methods=['GET', 'POST'])
def agregar_equipo():
    if request.method == 'POST':
        id_equipo = request.form['id_equipo']
        tipo = request.form['tipo']
        estado = request.form['estado']
        disponibilidad = request.form['disponibilidad']
        
        nuevo_equipo = EquipoTactico(id_equipo, tipo, estado, disponibilidad)
        inventario.agregar_equipo(nuevo_equipo)
        return redirect(url_for('equipos'))
        
    return render_template('formulario_equipo.html', equipo=None)

@app.route('/equipos/editar/<id_equipo>', methods=['GET', 'POST'])
def editar_equipo(id_equipo):
    equipo_actual = inventario.obtener_equipo(id_equipo)
    if not equipo_actual:
        return redirect(url_for('equipos'))
        
    if request.method == 'POST':
        tipo = request.form['tipo']
        estado = request.form['estado']
        disponibilidad = request.form['disponibilidad']
        
        inventario.actualizar_equipo(id_equipo, tipo, estado, disponibilidad)
        return redirect(url_for('equipos'))
        
    return render_template('formulario_equipo.html', equipo=equipo_actual)

@app.route('/equipos/eliminar/<id_equipo>')
def eliminar_equipo(id_equipo):
    inventario.eliminar_equipo(id_equipo)
    return redirect(url_for('equipos'))

# === FIN RUTAS CRUD ===

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/servidor/<nombre>')
def servidor(nombre):
    return render_template('servidor.html', nombre=nombre)

if __name__ == '__main__':
    app.run(debug=True)
