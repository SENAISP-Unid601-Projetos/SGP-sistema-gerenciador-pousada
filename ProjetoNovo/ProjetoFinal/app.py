from flask import Flask, render_template, request, redirect, url_for
from tinydb import TinyDB
from datetime import datetime

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

@app.route('/domo')
def domo():
    return render_template('domo.html')

@app.route('/suite')
def suite():
    return render_template('suite.html')

@app.route('/estacionamento')
def estacionamento():
    return render_template('estacionamento.html')

@app.route('/charrua')
def charrua():
    return render_template('charrua.html')

@app.route('/chale')
def chale():
    return render_template('chale.html')

@app.route('/cabana')
def cabana():
    return render_template('cabana.html')

@app.route('/addData', methods=['POST'])
def submit_data():
    # Coletando os dados do formulário
    nome = request.form.get('nome')
    email = request.form.get('email')
    checkin = request.form.get('checkin')
    checkout = request.form.get('checkout')

# Verificando se os dados estão preenchidos
    if nome and email and checkin and checkout:
        # Salvando os dados no banco TinyDB
        db.insert({
            'nome': nome,
            'email': email,
            'checkin': checkin,
            'checkout': checkout,
            'data_registro': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        return redirect(url_for('index'))  # Redireciona de volta para a página inicial

    return 'Erro: Todos os campos são obrigatórios!', 400

# Inicia o servidor
if __name__ == '__main__':
    app.run(debug=True)
