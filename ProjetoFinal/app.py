from flask import Flask, render_template, request, redirect, url_for
from tinydb import TinyDB, Query

app = Flask(__name__)

# Inicializa o banco de dados TinyDB
db = TinyDB('database.json')

# Rota para a página principal (index)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/reserva')
def reserva():
    return render_template('reserva.html')

# Inicia o servidor
if __name__ == '__main__':
    app.run(debug=True)
