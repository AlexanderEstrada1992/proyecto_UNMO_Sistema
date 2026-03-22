from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Bienvenido al Sistema de Gestión Operativa - UNMO de la Policía Nacional</h1>'

@app.route('/servidor/<nombre>')
def servidor(nombre):
    # Ruta dinámica ajustada al modelo conceptual del sistema UNMO
    return f'<h2>Bienvenido servidor policial {nombre}. Su asignación de servicio está confirmada.</h2>'

if __name__ == '__main__':
    app.run(debug=True)
