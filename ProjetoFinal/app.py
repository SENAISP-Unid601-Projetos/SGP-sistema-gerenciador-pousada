from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from tinydb import TinyDB, Query
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps
import os
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'  # Chave secreta para gerenciamento de sessões

# Configuração do caminho do banco de dados
db_path = os.path.join(os.path.dirname(__file__), 'database.json')

# Inicializa o banco de dados TinyDB
try:
    db = TinyDB(db_path)
except FileNotFoundError:
    raise FileNotFoundError("Banco de dados não encontrado! Por favor, certifique-se de que o arquivo 'database.json' existe no diretório.")

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
                flash('Erro: Este e-mail já está registrado!', 'error')
                return redirect(url_for('login'))

            # Verifica se é o admin
            is_admin = email == ADMIN_EMAIL

            # Adiciona o novo usuário ao banco de dados
            usuarios_db.insert({'nome': nome, 'email': email, 'senha': senha, 'admin': is_admin})
            flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
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
                session['admin'] = usuario[0].get('admin', False)  # Define a sessão de admin
                return redirect(url_for('index'))  # Redireciona sem mensagem de sucesso
            else:
                flash('Erro: E-mail ou senha incorretos!', 'error')
                return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    # Limpa a sessão do usuário ao fazer logout
    session.clear()
    return redirect(url_for('index'))

# Decorator para verificar se o usuário está logado
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'usuario_id' not in session:
            return redirect(url_for('login'))  # Redireciona para a página de login
        return f(*args, **kwargs)
    return decorated_function

@app.route('/meu_perfil')
def meu_perfil():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))  # Redireciona se não estiver logado
    
    usuario_id = session['usuario_id']
    reservas_usuario = reservas_db.search(Usuario.email == session['email'])  # Busca as reservas do usuário

    # Formata as datas antes de passar para o template, se houver reservas
    for reserva in reservas_usuario:
        try:
            if 'checkin' in reserva and 'checkout' in reserva:
                reserva['checkin'] = datetime.strptime(reserva['checkin'], '%Y-%m-%d').strftime('%d/%m/%Y')
                reserva['checkout'] = datetime.strptime(reserva['checkout'], '%Y-%m-%d').strftime('%d/%m/%Y')
                reserva['data_registro'] = datetime.strptime(reserva['data_registro'], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y às %H:%M:%S')
        except (ValueError, KeyError) as e:
            # Trate o erro de formatação, se necessário
            print(f"Erro ao formatar a reserva: {reserva}, erro: {e}")

    return render_template('meu_perfil.html', user=session, reservas=reservas_usuario)

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
@login_required
def submit_data():
    quarto = request.form.get('quarto')
    checkin = request.form.get('checkin')  
    checkout = request.form.get('checkout')  
    email = session['email']

    # Verifique se os dados estão preenchidos
    if email and checkin and checkout and quarto:
        # Converter as datas para objetos datetime
        checkin_date = datetime.strptime(checkin, '%Y-%m-%d')
        checkout_date = datetime.strptime(checkout, '%Y-%m-%d')

        # Verifique se a data de check-out é posterior à data de check-in
        if checkin_date >= checkout_date:
            return jsonify({'error': 'Erro: A data de check-out deve ser posterior à data de check-in!'}), 400

        # Verifique se a data de check-in não é uma data passada
        if checkin_date < datetime.now():
            return jsonify({'error': 'Erro: A data de check-in não pode ser uma data passada!'}), 400

        # Verifique se a reserva tem no mínimo dois dias
        if (checkout_date - checkin_date).days < 2:
            return jsonify({'error': 'Erro: Todos os cômodos devem ter no mínimo dois dias de reserva!'}), 400

        # Verifica se há um conflito de reservas para o mesmo quarto
        if verificar_conflito(quarto, checkin, checkout):
            return jsonify({'error': 'Erro: Já existe uma reserva para este cômodo nas datas selecionadas!'}), 400

        # Salvando os dados no banco TinyDB
        reservas_db.insert({
            'nome': session['nome'],
            'email': email,
            'quarto': quarto,
            'checkin': checkin,
            'checkout': checkout,
            'data_registro': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        return jsonify({'success': 'Reserva efetuada com sucesso!'}), 200

    return jsonify({'error': 'Erro: Todos os campos são obrigatórios!'}), 400

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

@app.route('/excluir_reserva', methods=['POST'])
@login_required
def excluir_reserva():
    reserva_id = request.form.get('reserva_id')

    # Verifica se a reserva existe e se pertence ao usuário logado
    reserva = reservas_db.get(doc_id=int(reserva_id))
    if reserva and reserva['email'] == session['email']:
        reservas_db.remove(doc_ids=[int(reserva_id)])
        return redirect(url_for('meu_perfil'))
    
    return jsonify({'error': 'Erro: Não foi possível excluir a reserva.'}), 400

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

# Decorator para verificar se o usuário é admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('index'))  # Redireciona para a página principal
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin', methods=['GET', 'POST'])
@login_required  # Aplica o decorator
@admin_required
def admin():
    reservas = []
    if request.method == 'POST':
        if 'ver_todas' in request.form:  # Verifica se o botão de "Ver todas" foi clicado
            reservas = reservas_db.all()  # Retorna todas as reservas do banco de dados
        else:
            termo_pesquisa = request.form.get('pesquisa')

            # Busca por quarto, nome ou email
            reservas = reservas_db.search(
                (Usuario.quarto.matches(termo_pesquisa, flags=re.IGNORECASE)) |
                (Usuario.nome.matches(termo_pesquisa, flags=re.IGNORECASE)) |
                (Usuario.email.matches(termo_pesquisa, flags=re.IGNORECASE))
            )

    # Formata as datas antes de passar para o template, se houver reservas
    for reserva in reservas:
        try:
            if 'checkin' in reserva and 'checkout' in reserva:
                reserva['checkin'] = datetime.strptime(reserva['checkin'], '%Y-%m-%d').strftime('%d/%m/%Y')
                reserva['checkout'] = datetime.strptime(reserva['checkout'], '%Y-%m-%d').strftime('%d/%m/%Y')
                reserva['data_registro'] = datetime.strptime(reserva['data_registro'], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y às %H:%M:%S')
        except (ValueError, KeyError) as e:
            # Trate o erro de formatação, se necessário
            print(f"Erro ao formatar a reserva: {reserva}, erro: {e}")

    return render_template('admin.html', reservas=reservas)

if __name__ == '__main__':
    app.run(debug=True)
