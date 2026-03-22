from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/equipos')
def equipos():
    return render_template('equipos.html')

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/servidor/<nombre>')
def servidor(nombre):
    return render_template('servidor.html', nombre=nombre)

if __name__ == '__main__':
    app.run(debug=True)
