import os
from flask import Flask, render_template, request, redirect, url_for
from Conexion.conexion import obtener_conexion

# Mantenemos la persistencia en archivos (Semana 12)
from inventario.inventario import guardar_persistencia_archivos, leer_txt, leer_json, leer_csv

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

# === RUTAS CRUD MYSQL: EQUIPOS TÁCTICOS ===
@app.route('/equipos')
def equipos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM equipos")
    lista_equipos = cursor.fetchall()
    conexion.close()
    return render_template('equipos.html', equipos=lista_equipos)

@app.route('/equipos/agregar', methods=['GET', 'POST'])
def agregar_equipo():
    if request.method == 'POST':
        id_equipo = request.form['id_equipo']
        tipo = request.form['tipo']
        estado = request.form['estado']
        disponibilidad = request.form['disponibilidad']
        
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO equipos (id_equipo, tipo, estado_operativo, disponibilidad) VALUES (%s, %s, %s, %s)",
            (id_equipo, tipo, estado, disponibilidad)
        )
        conexion.commit()
        conexion.close()
        
        # Persistencia en archivos simultánea
        equipo_dict = {"id_equipo": id_equipo, "tipo": tipo, "estado_operativo": estado, "disponibilidad": disponibilidad}
        guardar_persistencia_archivos(equipo_dict)
        
        return redirect(url_for('equipos'))
    return render_template('formulario_equipo.html', equipo=None)

@app.route('/equipos/editar/<id_equipo>', methods=['GET', 'POST'])
def editar_equipo(id_equipo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM equipos WHERE id_equipo = %s", (id_equipo,))
    equipo_actual = cursor.fetchone()
    
    if not equipo_actual:
        conexion.close()
        return redirect(url_for('equipos'))
        
    if request.method == 'POST':
        tipo = request.form['tipo']
        estado = request.form['estado']
        disponibilidad = request.form['disponibilidad']
        
        cursor.execute(
            "UPDATE equipos SET tipo=%s, estado_operativo=%s, disponibilidad=%s WHERE id_equipo=%s",
            (tipo, estado, disponibilidad, id_equipo)
        )
        conexion.commit()
        conexion.close()
        
        # Guardar historial simple en archivos
        equipo_dict = {"id_equipo": id_equipo, "tipo": tipo, "estado_operativo": estado, "disponibilidad": disponibilidad}
        guardar_persistencia_archivos(equipo_dict)
        
        return redirect(url_for('equipos'))
        
    conexion.close()
    return render_template('formulario_equipo.html', equipo=equipo_actual)

@app.route('/equipos/eliminar/<id_equipo>')
def eliminar_equipo(id_equipo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM equipos WHERE id_equipo = %s", (id_equipo,))
    conexion.commit()
    conexion.close()
    return redirect(url_for('equipos'))

# === RUTAS CRUD MYSQL: USUARIOS (NUEVO SEMANA 13) ===
@app.route('/usuarios')
def usuarios():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios")
    lista_usuarios = cursor.fetchall()
    conexion.close()
    return render_template('usuarios.html', usuarios=lista_usuarios)

@app.route('/usuarios/agregar', methods=['GET', 'POST'])
def agregar_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        mail = request.form['mail']
        password = request.form['password']
        
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, mail, password) VALUES (%s, %s, %s)",
            (nombre, mail, password)
        )
        conexion.commit()
        conexion.close()
        return redirect(url_for('usuarios'))
    return render_template('formulario_usuario.html', usuario=None)

@app.route('/usuarios/editar/<int:id_usuario>', methods=['GET', 'POST'])
def editar_usuario(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    usuario_actual = cursor.fetchone()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        mail = request.form['mail']
        password = request.form['password']
        
        cursor.execute(
            "UPDATE usuarios SET nombre=%s, mail=%s, password=%s WHERE id_usuario=%s",
            (nombre, mail, password, id_usuario)
        )
        conexion.commit()
        conexion.close()
        return redirect(url_for('usuarios'))
        
    conexion.close()
    return render_template('formulario_usuario.html', usuario=usuario_actual)

@app.route('/usuarios/eliminar/<int:id_usuario>')
def eliminar_usuario(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    conexion.commit()
    conexion.close()
    return redirect(url_for('usuarios'))

# === RUTAS SECUNDARIAS ===
@app.route('/datos')
def datos():
    datos_txt = leer_txt()
    datos_json = leer_json()
    datos_csv = leer_csv()
    return render_template('datos.html', datos_txt=datos_txt, datos_json=datos_json, datos_csv=datos_csv)

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/servidor/<nombre>')
def servidor(nombre):
    return render_template('servidor.html', nombre=nombre)

if __name__ == '__main__':
    app.run(debug=True)
