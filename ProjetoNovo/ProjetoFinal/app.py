from flask import Flask, render_template, request, redirect, url_for, jsonify
from tinydb import TinyDB, Query
from datetime import datetime, timedelta

app = Flask(__name__)

# Inicializa o banco de dados TinyDB
db = TinyDB('database.json')

# Rota para a página principal (index)
@app.route('/')
def index():
    datas_reservadas = obter_datas_reservadas()  # Obtém todas as datas reservadas
    return render_template('index.html', datas_reservadas=datas_reservadas)

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
    quarto = request.form.get('quarto')
    checkin = request.form.get('checkin')
    checkout = request.form.get('checkout')

    # Verificando se os dados estão preenchidos
    if nome and email and checkin and checkout and quarto:
        
        # Verifica se há um conflito de reservas para o mesmo quarto
        if verificar_conflito(quarto, checkin, checkout):
            return jsonify({'error': 'Erro: Já existe uma reserva para este cômodo nas datas selecionadas!'}), 400

        # Salvando os dados no banco TinyDB
        db.insert({
            'nome': nome,
            'email': email,
            'quarto': quarto,
            'checkin': checkin,
            'checkout': checkout,
            'data_registro': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        return jsonify({'success': 'Reserva efetuada com sucesso!'}), 200  # Redireciona de volta para a página inicial

    return jsonify({'error': 'Erro: Todos os campos são obrigatórios!'}), 400

# Função para verificar conflitos de reserva
def verificar_conflito(quarto, checkin, checkout):
    # Converter as datas para objetos datetime
    checkin = datetime.strptime(checkin, '%Y-%m-%d')
    checkout = datetime.strptime(checkout, '%Y-%m-%d')

    # Buscar todas as reservas do mesmo quarto
    Quarto = Query()
    reservas = db.search(Quarto.quarto == quarto)

    # Verificar se alguma reserva existente tem sobreposição de datas
    for reserva in reservas:
        checkin_existente = datetime.strptime(reserva['checkin'], '%Y-%m-%d')
        checkout_existente = datetime.strptime(reserva['checkout'], '%Y-%m-%d')

        # Verifica se as datas se sobrepõem
        if checkin <= checkout_existente and checkout >= checkin_existente:
            return True  # Conflito encontrado

    return False  # Sem conflitos

    # Função para obter todas as datas reservadas
def obter_datas_reservadas():
    reservas = db.all()
    datas_reservadas = []
    
    # Itera sobre todas as reservas e gera um intervalo de datas entre check-in e check-out
    for reserva in reservas:
        checkin = datetime.strptime(reserva['checkin'], '%Y-%m-%d')
        checkout = datetime.strptime(reserva['checkout'], '%Y-%m-%d')

        # Gera as datas entre check-in e check-out
        while checkin <= checkout:
            datas_reservadas.append(checkin.strftime('%Y-%m-%d'))
            checkin += timedelta(days=1)

    return datas_reservadas
    
# Inicia o servidor
if __name__ == '__main__':
    app.run(debug=True)
