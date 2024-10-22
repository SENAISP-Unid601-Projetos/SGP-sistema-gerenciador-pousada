from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from tinydb import TinyDB, Query
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'  # Chave secreta para gerenciamento de sessões

# Inicializa o banco de dados TinyDB
db = TinyDB('database.json')
usuarios_db = db.table('usuarios')  # Tabela para usuários
reservas_db = db.table('reservas')  # Tabela para reservas
Usuario = Query()

# Página principal
@app.route('/')
def index():
    datas_reservadas = obter_datas_reservadas()  # Obtém todas as datas reservadas
    return render_template('index.html', datas_reservadas=datas_reservadas)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if 'signup' in request.form:  # Verifica se é um cadastro
            nome = request.form['nome']
            email = request.form['email']
            senha = generate_password_hash(request.form['senha'])

            # Verifica se o email já está registrado
            usuario_existente = usuarios_db.search(Usuario.email == email)
            if usuario_existente:
                return redirect(url_for('login'))

            # Adiciona o novo usuário ao banco de dados
            usuarios_db.insert({'nome': nome, 'email': email, 'senha': senha})
            return redirect(url_for('login'))

        elif 'signin' in request.form:  # Verifica se é um login
            email = request.form['email']
            senha = request.form['senha']

            # Busca o usuário no banco de dados
            usuario = usuarios_db.search(Usuario.email == email)

            if usuario and check_password_hash(usuario[0]['senha'], senha):
                # Login bem-sucedido, armazena informações do usuário na sessão
                session['usuario_id'] = usuario[0].doc_id
                session['nome'] = usuario[0]['nome']
                session['email'] = usuario[0]['email']
                return redirect(url_for('index'))
            else:
                return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    # Limpa a sessão do usuário ao fazer logout
    session.clear()
    return redirect(url_for('index'))

@app.route('/addData', methods=['POST'])
def submit_data():
    # Coletando os dados do formulário
    nome = request.form.get('nome')
    email = request.form.get('email')
    quarto = request.form.get('quarto')
    checkin = request.form.get('checkin')  # Ex: 25/01/2005
    checkout = request.form.get('checkout')  # Ex: 30/01/2005

    # Convertendo as datas para o formato esperado
    try:
        checkin_formatado = datetime.strptime(checkin, '%d/%m/%Y').strftime('%Y-%m-%d')
        checkout_formatado = datetime.strptime(checkout, '%d/%m/%Y').strftime('%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'Erro: Formato de data inválido. Utilize dia/mês/ano!'}), 400

    # Verificando se os dados estão preenchidos
    if nome and email and checkin_formatado and checkout_formatado and quarto:
        
        # Verifica se há um conflito de reservas para o mesmo quarto
        if verificar_conflito(quarto, checkin_formatado, checkout_formatado):
            return jsonify({'error': 'Erro: Já existe uma reserva para este cômodo nas datas selecionadas!'}), 400

        # Salvando os dados no banco TinyDB
        reservas_db.insert({
            'nome': nome,
            'email': email,
            'quarto': quarto,
            'checkin': checkin_formatado,
            'checkout': checkout_formatado,
            'data_registro': datetime.now().strftime('%d/%m/%Y às %H:%M:%S')  # Formato DD/MM/AAAA
        })
        return jsonify({'success': 'Reserva efetuada com sucesso!'}), 200  # Redireciona de volta para a página inicial

    return jsonify({'error': 'Erro: Todos os campos são obrigatórios!'}), 400

@app.route('/reserva')
def reserva():
    return render_template('reserva.html')

@app.route('/meu_perfil')
def meu_perfil():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))  # Redireciona se não estiver logado
    
    usuario_id = session['usuario_id']
    reservas_usuario = reservas_db.search(Usuario.email == session['email'])  # Busca as reservas do usuário

    return render_template('meu_perfil.html', user=session, reservas=reservas_usuario)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    reservas = []
    if request.method == 'POST':
        if 'ver_todas' in request.form:  # Verifica se o botão de "Ver todas" foi clicado
            reservas = reservas_db.all()  # Retorna todas as reservas do banco de dados
        else:
            termo_pesquisa = request.form.get('termo').lower()  # Convertendo o termo pesquisado para minúsculas
            Quarto = Query()
            # Busca insensível a maiúsculas/minúsculas usando regex
            reservas = reservas_db.search(
                (Quarto.quarto.matches(termo_pesquisa, flags=re.IGNORECASE)) |
                (Quarto.nome.matches(termo_pesquisa, flags=re.IGNORECASE)) |
                (Quarto.email.matches(termo_pesquisa, flags=re.IGNORECASE)) |
                (Quarto.checkin.matches(termo_pesquisa, flags=re.IGNORECASE)) |
                (Quarto.checkout.matches(termo_pesquisa, flags=re.IGNORECASE)) 
            )

    # Formata as datas antes de passar para o template
    for reserva in reservas:
        reserva['checkin'] = datetime.strptime(reserva['checkin'], '%Y-%m-%d').strftime('%d/%m/%Y')
        reserva['checkout'] = datetime.strptime(reserva['checkout'], '%Y-%m-%d').strftime('%d/%m/%Y')

    return render_template('admin.html', reservas=reservas)

# Função para obter todas as datas reservadas
def obter_datas_reservadas():
    reservas = reservas_db.all()
    datas_reservadas = []
    
    for reserva in reservas:
        checkin = datetime.strptime(reserva['checkin'], '%Y-%m-%d')
        checkout = datetime.strptime(reserva['checkout'], '%Y-%m-%d')

        while checkin <= checkout:
            datas_reservadas.append(checkin.strftime('%d/%m/%Y'))  # Formato DD/MM/AAAA
            checkin += timedelta(days=1)

    return datas_reservadas

# Função para verificar conflitos de reserva
def verificar_conflito(quarto, checkin, checkout):
    # Converter as datas para objetos datetime
    checkin = datetime.strptime(checkin, '%Y-%m-%d')
    checkout = datetime.strptime(checkout, '%Y-%m-%d')

    # Buscar todas as reservas do mesmo quarto
    Quarto = Query()
    reservas = reservas_db.search(Quarto.quarto == quarto)

    # Verificar se alguma reserva existente tem sobreposição de datas
    for reserva in reservas:
        checkin_existente = datetime.strptime(reserva['checkin'], '%Y-%m-%d')
        checkout_existente = datetime.strptime(reserva['checkout'], '%Y-%m-%d')

        # Verifica se as datas se sobrepõem
        if checkin <= checkout_existente and checkout >= checkin_existente:
            return True  # Conflito encontrado

    return False  # Sem conflitos

# Inicia o servidor
if __name__ == '__main__':
    app.run(debug=True)
