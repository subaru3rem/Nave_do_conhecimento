from distutils.log import error
from fileinput import filename
from nturl2path import pathname2url
from flask import *
import mysql.connector
import re

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database = 'serve_nave'
)
cursor = mydb.cursor()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
@app.route('/')
def home():
    return render_template("home.html")
@app.route('/unidades')
def unidades():
    return render_template("unidades.html")
@app.route('/eventos')
def eventos():
    return render_template("eventos.html")
@app.route("/user")
def user():
    return render_template("area do aluno.html")
def Login(login):
    return render_template("log_user.html", account=login)
@app.route("/user/#")
def Cad(cad, cad_senha):
    return render_template("finalizar_cad.html", login=cad, senha=cad_senha)
def sanitize(dict):
    chave = dict[0]
    string = dict[1]
    if chave == "email":
        string = re.sub("[^\w@.-_]", "", string)
        return string
    elif chave == "cll":
        string = re.sub("[\D ]", "", string)
        if len(string) == 11:
            string = "0"+string
            return string
        elif len(string) == 12:
            return string
    else:
        string = re.sub("[^\w ]", "", string)
        return string
@app.route("/user/#", methods = ["GET", "POST"])
def finalizar_cad():
    login, senha, nome, nome_s = request.form.get("user"),request.form.get("user_senha"),request.form.get("nome"), request.form.get("nome_s")
    sexo, email, data_n, cpf = request.form.get("sexo"), request.form.get("email"), request.form.get("data_n"), request.form.get("cpf")
    cell, uf, cidade, cor = request.form.get("celular"), request.form.get("uf"), request.form.get("cidade"), request.form.get("cor")
    itens = {'login':login, 'senha':senha, 'nome':nome, 'nome_s':nome_s, 'sexo':sexo, 'email':email, 'data_n': data_n, 'cpf':cpf, 'cell': cell, 'uf':uf, 'cidade':cidade, 'cor': cor}
    clean = []
    for i in itens.items():clean.append(sanitize(i))
    cursor.execute(f"""insert into usuarios values('{clean[0]}', '{clean[1]}');""")
    cursor.execute(f'''insert into info_user values('{clean[0]}', '{clean[2]}', '{clean[3]}', '{clean[4]}', '{clean[5]}', '{clean[6]}'
    , '{clean[7]}', '{clean[8]}', '{clean[9]}', '{clean[10]}', '{clean[11]}')''')
    mydb.commit()
    return Login(login)
@app.route('/user', methods =["GET", "POST"])
def validacion():
    if request.method == "POST":
        login = request.form.get("login")
        senha = request.form.get("senha")
        cad = request.form.get("cad")
        cad_senha = request.form.get("senha1")
        confirmação = request.form.get("senha2")
        if login == None:
            if cad == '':
                return user()
            else:
                sql = f"select login from usuarios where login='{cad}'"
                cursor.execute(sql)
                verificação = cursor.fetchone()
                if verificação == None:
                    if cad_senha == confirmação:
                        return Cad(cad, cad_senha)
                    else: 
                        flash("senhas_distintas")
                        return user()
                else:
                    flash('login_cadastrado')
                    return user()
        else:
            sql = f"select senha from usuarios where login='{login}'"
            cursor.execute(sql)
            verificação = cursor.fetchone()
            if verificação == None:
                flash('login_inexistente')
                return user()
            elif verificação[0] == senha:
                return Login(login)
            else:
                flash('senha_incorreta')
                return user()
app.run(debug=True)
