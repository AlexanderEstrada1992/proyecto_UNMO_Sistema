from flask import Flask

app = Flask(__name__)

# Ruta principal solicitada en la tarea
@app.route('/')
def inicio():
    return "Bienvenido al Sistema Operativo UNMO"

# Ruta dinámica solicitada en la tarea
@app.route('/usuario/<nombre>')
def usuario(nombre):
    return f"Bienvenido, {nombre}. Tu usuario en el Sistema UNMO está activo."

if __name__ == '__main__':
    app.run(debug=True)
