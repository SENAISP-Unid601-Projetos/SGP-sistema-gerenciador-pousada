from flask import Flask, render_template, request, redirect, url_for
from tinydb import TinyDB, Query
from datetime import datetime

app = Flask(__name__)

# Inicializa o banco de dados TinyDB
db = TinyDB('database.json')

# Rota para a página principal (index)
@app.route('/')
def index():
    return render_template('index.html')

# Rota para visualizar o calendário de check-ins
@app.route('/calendario')
def calendario():
    # Buscar todas as reservas no banco de dados
    reservas = db.all()
    return render_template('calendario.html', reservas=reservas)

# Rota para adicionar uma nova reserva
@app.route('/add_checkin', methods=['POST'])
def add_checkin():
    # Obtém os dados do formulário (nome, data de check-in e check-out)
    nome = request.form.get('nome')
    checkin = request.form.get('checkin')
    checkout = request.form.get('checkout')

    # Verifica se os dados estão completos
    if nome and checkin and checkout:
        # Salva a nova reserva no TinyDB
        db.insert({
            'nome': nome,
            'checkin': checkin,
            'checkout': checkout,
            'data_registro': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    return redirect(url_for('calendario'))

# Rota para deletar uma reserva
@app.route('/delete/<int:id>')
def delete_reserva(id):
    db.remove(doc_ids=[id])
    return redirect(url_for('calendario'))

# Inicia o servidor
if __name__ == '__main__':
    app.run(debug=True)
