import os
from flask import Flask, render_template, request, redirect, url_for, flash
from Conexion.conexion import obtener_conexion

# Módulos de Semana 14: Seguridad y Autenticación con Flask-Login
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import Usuario

# Mantenemos la persistencia en archivos (Semana 12)
from inventario.inventario import guardar_persistencia_archivos, leer_txt, leer_json, leer_csv

app = Flask(__name__)

# LLAVE SECRETA (Obligatoria para la gestión de sesiones en Flask-Login)
app.secret_key = 'clave_secreta_unmo_super_segura_2026'

# 1. Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Redirección si un usuario sin sesión intenta entrar
login_manager.login_message = "Por favor, inicie sesión en su cuenta oficial para acceder a esta página."
login_manager.login_message_category = "warning"

# 2. Cargar Usuario en la Sesión mediante el ID de Base de Datos
@login_manager.user_loader
def load_user(user_id):
    return Usuario.get(user_id)

# === RUTAS PÚBLICAS ===
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

# === RUTAS DE AUTENTICACIÓN (NUEVAS - SEMANA 14) ===
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('equipos'))  # Si ya está logueado, lo manda al panel
        
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']
        
        # Validar en base de datos usando check_password_hash
        usuario = Usuario.get_by_mail(mail)
        if usuario and check_password_hash(usuario.password, password):
            login_user(usuario)
            return redirect(url_for('equipos'))
        else:
            return render_template('login.html', error="Correo o contraseña incorrectos.")
            
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if current_user.is_authenticated:
        return redirect(url_for('equipos'))
        
    if request.method == 'POST':
        nombre = request.form['nombre']
        mail = request.form['mail']
        password = request.form['password']
        
        # Evitar correos duplicados
        if Usuario.get_by_mail(mail):
            return render_template('registro.html', error="Este correo ya se encuentra registrado. Intente Iniciar Sesión.")
            
        # Encriptar clave antes de guardar
        hashed_password = generate_password_hash(password)
        
        # Crear en base de datos MySQL 
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO usuarios (nombre, mail, password) VALUES (%s, %s, %s)",
            (nombre, mail, hashed_password)
        )
        conexion.commit()
        conexion.close()
        
        flash("Se ha creado el perfil policial con éxito. Ya puede iniciar sesión.", "success")
        return redirect(url_for('login'))
        
    return render_template('registro.html')

@app.route('/logout')
@login_required # Ruta Protegida
def logout():
    logout_user() # Terminar sesión
    return redirect(url_for('login'))

# === RUTAS PROTEGIDAS CON @login_required (Requerimiento de la Semana) ===
@app.route('/equipos')
@login_required
def equipos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM equipos")
    lista_equipos = cursor.fetchall()
    conexion.close()
    return render_template('equipos.html', equipos=lista_equipos)

@app.route('/equipos/agregar', methods=['GET', 'POST'])
@login_required
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
        
        # Persistencia simultánea
        equipo_dict = {"id_equipo": id_equipo, "tipo": tipo, "estado_operativo": estado, "disponibilidad": disponibilidad}
        guardar_persistencia_archivos(equipo_dict)
        return redirect(url_for('equipos'))
    return render_template('formulario_equipo.html', equipo=None)

@app.route('/equipos/editar/<id_equipo>', methods=['GET', 'POST'])
@login_required
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
        
        equipo_dict = {"id_equipo": id_equipo, "tipo": tipo, "estado_operativo": estado, "disponibilidad": disponibilidad}
        guardar_persistencia_archivos(equipo_dict)
        return redirect(url_for('equipos'))
    conexion.close()
    return render_template('formulario_equipo.html', equipo=equipo_actual)

@app.route('/equipos/eliminar/<id_equipo>')
@login_required
def eliminar_equipo(id_equipo):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM equipos WHERE id_equipo = %s", (id_equipo,))
    conexion.commit()
    conexion.close()
    return redirect(url_for('equipos'))

@app.route('/usuarios')
@login_required
def usuarios():
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios")
    lista_usuarios = cursor.fetchall()
    conexion.close()
    return render_template('usuarios.html', usuarios=lista_usuarios)

@app.route('/usuarios/agregar', methods=['GET', 'POST'])
@login_required
def agregar_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        mail = request.form['mail']
        password = request.form['password']
        
        hashed_password = generate_password_hash(password)
        
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO usuarios (nombre, mail, password) VALUES (%s, %s, %s)", (nombre, mail, hashed_password))
        conexion.commit()
        conexion.close()
        return redirect(url_for('usuarios'))
    return render_template('formulario_usuario.html', usuario=None)

@app.route('/usuarios/editar/<int:id_usuario>', methods=['GET', 'POST'])
@login_required
def editar_usuario(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    usuario_actual = cursor.fetchone()
    if request.method == 'POST':
        nombre = request.form['nombre']
        mail = request.form['mail']
        password = request.form['password']
        
        if password.strip() == "":
            cursor.execute("UPDATE usuarios SET nombre=%s, mail=%s WHERE id_usuario=%s", (nombre, mail, id_usuario))
        else:
            hashed_password = generate_password_hash(password)
            cursor.execute("UPDATE usuarios SET nombre=%s, mail=%s, password=%s WHERE id_usuario=%s", (nombre, mail, hashed_password, id_usuario))
            
        conexion.commit()
        conexion.close()
        return redirect(url_for('usuarios'))
    conexion.close()
    return render_template('formulario_usuario.html', usuario=usuario_actual)

@app.route('/usuarios/eliminar/<int:id_usuario>')
@login_required
def eliminar_usuario(id_usuario):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
    conexion.commit()
    conexion.close()
    return redirect(url_for('usuarios'))

@app.route('/datos')
@login_required
def datos():
    datos_txt = leer_txt()
    datos_json = leer_json()
    datos_csv = leer_csv()
    return render_template('datos.html', datos_txt=datos_txt, datos_json=datos_json, datos_csv=datos_csv)

@app.route('/servicios')
@login_required
def servicios():
    return render_template('servicios.html')

@app.route('/servidor/<nombre>')
@login_required
def servidor(nombre):
    return render_template('servidor.html', nombre=nombre)

if __name__ == '__main__':
    app.run(debug=True)
