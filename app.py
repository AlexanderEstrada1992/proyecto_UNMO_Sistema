import os
from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from functools import wraps

# Autenticación con Flask-Login
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

# Servicios y Formularios
from services.usuario_service import UsuarioService
from services.equipo_service import EquipoService
from services.asignacion_service import AsignacionService
from forms.usuario_form import UsuarioForm
from forms.equipo_form import EquipoForm
from forms.asignacion_form import AsignacionForm

# Persistencia en archivos (Semana 12)
from inventario.inventario import guardar_persistencia_archivos, leer_txt, leer_json, leer_csv

app = Flask(__name__)
app.secret_key = 'clave_secreta_unmo_super_segura_2026'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Por favor, inicie sesión en su cuenta oficial."
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
    return UsuarioService.obtener_por_id(user_id)

# === RUTAS PÚBLICAS ===
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

# === RUTAS DE AUTENTICACIÓN ===
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('equipos'))
        
    if request.method == 'POST':
        mail = request.form['mail']
        password = request.form['password']
        
        usuario = UsuarioService.obtener_por_mail(mail)
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
        form = UsuarioForm(request.form)
        if form.validar():
            if UsuarioService.obtener_por_mail(form.data['mail']):
                return render_template('registro.html', error="Este correo ya se encuentra registrado.")
            
            from models.usuario import Usuario
            nuevo_usuario = Usuario(None, form.data['nombre'], form.data['mail'], form.data['password'])
            UsuarioService.agregar(nuevo_usuario)
            flash("Se ha creado el perfil policial con éxito.", "success")
            return redirect(url_for('login'))
        else:
            return render_template('registro.html', errores=form.errores, datos=form.data)
            
    return render_template('registro.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# === CRUD EQUIPOS ===
@app.route('/equipos')
@login_required
def equipos():
    lista_equipos = EquipoService.obtener_todos()
    return render_template('equipos/equipos.html', equipos=lista_equipos)

@app.route('/equipos/agregar', methods=['GET', 'POST'])
@login_required
def agregar_equipo():
    if request.method == 'POST':
        form = EquipoForm(request.form)
        if form.validar():
            from models.equipo import Equipo
            # Creamos el objeto Equipo con los datos correctos del formulario
            nuevo_equipo = Equipo(
                id_equipo=form.data['id_equipo'], 
                tipo=form.data['tipo'], 
                estado_operativo=form.data['estado'], 
                disponibilidad=form.data['disponibilidad']
            )
            EquipoService.agregar(nuevo_equipo)
            
            # Persistencia en archivos (semana 12)
            guardar_persistencia_archivos({"id_equipo": nuevo_equipo.id_equipo, "tipo": nuevo_equipo.tipo, "estado_operativo": nuevo_equipo.estado_operativo, "disponibilidad": nuevo_equipo.disponibilidad})
            
            return redirect(url_for('equipos'))
        else:
            return render_template('equipos/formulario_equipo.html', equipo=None, errores=form.errores, form_data=form.data)
            
    return render_template('equipos/formulario_equipo.html', equipo=None)

@app.route('/equipos/editar/<id_equipo>', methods=['GET', 'POST'])
@login_required
def editar_equipo(id_equipo):
    equipo_actual = EquipoService.obtener_por_id(id_equipo)
    if not equipo_actual:
        return redirect(url_for('equipos'))
        
    if request.method == 'POST':
        # Validar la información
        # Inyectamos el id_equipo en la data para que el formulario no falle la validación del campo faltante,
        # O si el id está deshabilitado, lo ponemos manualmente.
        data_to_validate = request.form.to_dict()
        data_to_validate['id_equipo'] = id_equipo 
        
        form = EquipoForm(data_to_validate)
        if form.validar():
            from models.equipo import Equipo
            equipo_modificado = Equipo(
                id_equipo=id_equipo, 
                tipo=form.data['tipo'], 
                estado_operativo=form.data['estado'], 
                disponibilidad=form.data['disponibilidad']
            )
            EquipoService.actualizar(id_equipo, equipo_modificado)
            guardar_persistencia_archivos({"id_equipo": id_equipo, "tipo": form.data['tipo'], "estado_operativo": form.data['estado'], "disponibilidad": form.data['disponibilidad']})
            return redirect(url_for('equipos'))
        else:
            return render_template('equipos/formulario_equipo.html', equipo=equipo_actual, errores=form.errores)
            
    return render_template('equipos/formulario_equipo.html', equipo=equipo_actual)

@app.route('/equipos/eliminar/<id_equipo>')
@login_required
def eliminar_equipo(id_equipo):
    EquipoService.eliminar(id_equipo)
    return redirect(url_for('equipos'))

# === CRUD USUARIOS ===
@app.route('/usuarios')
@login_required
def usuarios():
    lista_usuarios = UsuarioService.obtener_todos()
    return render_template('usuarios/usuarios.html', usuarios=lista_usuarios)

@app.route('/usuarios/agregar', methods=['GET', 'POST'])
@login_required
def agregar_usuario():
    if request.method == 'POST':
        form = UsuarioForm(request.form, es_edicion=False)
        if form.validar():
            from models.usuario import Usuario
            nuevo_usuario = Usuario(None, form.data['nombre'], form.data['mail'], form.data['password'])
            UsuarioService.agregar(nuevo_usuario)
            return redirect(url_for('usuarios'))
        else:
            return render_template('usuarios/formulario_usuario.html', usuario=None, errores=form.errores)
    return render_template('usuarios/formulario_usuario.html', usuario=None)

@app.route('/usuarios/editar/<int:id_usuario>', methods=['GET', 'POST'])
@login_required
def editar_usuario(id_usuario):
    usuario_actual = UsuarioService.obtener_por_id(id_usuario)
    if not usuario_actual:
        return redirect(url_for('usuarios'))
        
    if request.method == 'POST':
        form = UsuarioForm(request.form, es_edicion=True)
        if form.validar():
            from models.usuario import Usuario
            usuario_modificado = Usuario(id_usuario, form.data['nombre'], form.data['mail'], None)
            nueva_password = form.data['password'] if form.data.get('password', '').strip() != '' else None
            
            UsuarioService.actualizar(id_usuario, usuario_modificado, nueva_password)
            return redirect(url_for('usuarios'))
        else:
            return render_template('usuarios/formulario_usuario.html', usuario=usuario_actual, errores=form.errores)
    return render_template('usuarios/formulario_usuario.html', usuario=usuario_actual)

@app.route('/usuarios/eliminar/<int:id_usuario>')
@login_required
def eliminar_usuario(id_usuario):
    UsuarioService.eliminar(id_usuario)
    return redirect(url_for('usuarios'))

# === CRUD ASIGNACIONES (NUEVO) ===
@app.route('/asignaciones')
@login_required
def asignaciones():
    lista_asignaciones = AsignacionService.obtener_todas()
    return render_template('asignaciones/asignaciones.html', asignaciones=lista_asignaciones)

@app.route('/asignaciones/agregar', methods=['GET', 'POST'])
@login_required
def agregar_asignacion():
    equipos = EquipoService.obtener_todos()
    usuarios_list = UsuarioService.obtener_todos()
    
    if request.method == 'POST':
        form = AsignacionForm(request.form)
        if form.validar():
            from models.asignacion import Asignacion
            nueva_asignacion = Asignacion(
                id_asignacion=None,
                id_equipo=form.data['id_equipo'],
                id_usuario=form.data['id_usuario'],
                fecha_asignacion=form.data['fecha_asignacion'],
                observaciones=form.data['observaciones']
            )
            AsignacionService.agregar(nueva_asignacion)
            return redirect(url_for('asignaciones'))
        else:
            return render_template('asignaciones/formulario_asignacion.html', asignacion=None, equipos=equipos, usuarios=usuarios_list, errores=form.errores)
            
    return render_template('asignaciones/formulario_asignacion.html', asignacion=None, equipos=equipos, usuarios=usuarios_list)

@app.route('/asignaciones/editar/<int:id_asignacion>', methods=['GET', 'POST'])
@login_required
def editar_asignacion(id_asignacion):
    asignacion_actual = AsignacionService.obtener_por_id(id_asignacion)
    if not asignacion_actual:
        return redirect(url_for('asignaciones'))
        
    equipos = EquipoService.obtener_todos()
    usuarios_list = UsuarioService.obtener_todos()

    if request.method == 'POST':
        form = AsignacionForm(request.form)
        if form.validar():
            from models.asignacion import Asignacion
            asignacion_modificada = Asignacion(
                id_asignacion=id_asignacion,
                id_equipo=form.data['id_equipo'],
                id_usuario=form.data['id_usuario'],
                fecha_asignacion=form.data['fecha_asignacion'],
                observaciones=form.data['observaciones']
            )
            AsignacionService.actualizar(id_asignacion, asignacion_modificada)
            return redirect(url_for('asignaciones'))
        else:
            return render_template('formulario_asignacion.html', asignacion=asignacion_actual, equipos=equipos, usuarios=usuarios_list, errores=form.errores)
            
    return render_template('formulario_asignacion.html', asignacion=asignacion_actual, equipos=equipos, usuarios=usuarios_list)

@app.route('/asignaciones/eliminar/<int:id_asignacion>')
@login_required
def eliminar_asignacion(id_asignacion):
    AsignacionService.eliminar(id_asignacion)
    return redirect(url_for('asignaciones'))

# === REPORTES PDF ===
@app.route('/reporte_equipos')
@login_required
def reporte_equipos():
    from fpdf import FPDF
    import sys
    
    # Creamos el archivo PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Título
    pdf.cell(200, 10, txt="Reporte General de Equipos Tácticos", ln=True, align="C")
    pdf.ln(10)
    
    # Encabezados de tabla
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(30, 10, "ID", 1)
    pdf.cell(70, 10, "TIPO", 1)
    pdf.cell(40, 10, "ESTADO", 1)
    pdf.cell(40, 10, "DISPONIBILIDAD", 1)
    pdf.ln(10)
    
    # Contenido (Con Service)
    equipos = EquipoService.obtener_todos()
    pdf.set_font("Arial", size=10)
    for eq in equipos:
        pdf.cell(30, 10, str(eq.id_equipo), 1)
        pdf.cell(70, 10, str(eq.tipo), 1)
        pdf.cell(40, 10, str(eq.estado_operativo), 1)
        pdf.cell(40, 10, str(eq.disponibilidad), 1)
        pdf.ln(10)
        
    resultado_pdf = pdf.output(dest="S").encode("latin-1")
    
    # Crear respuesta para el navegador web
    response = make_response(resultado_pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=reporte_equipos.pdf'
    return response

# === OTRAS RUTAS ===
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
