from flask import Flask, render_template

app = Flask(__name__)

# Criar a primeira pagina
#route -> link 
#funçao -> oq será exibido na página
# template para o html

@app.route("/") # decorator -> uma linha de codigo que atribui uma funcionalidade pra função
def homepage():
    return render_template("index.html")

@app.route("/usuarios/<nome_usuario>")
def usuario(nome_usuario):
    return render_template("usuarios.html", nome_usuario=nome_usuario)

# Coloca o site no ar
if __name__ == "__main__":
    app.run(debug=True)