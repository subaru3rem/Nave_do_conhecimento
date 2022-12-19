from distutils.log import error
from fileinput import filename
from nturl2path import pathname2url
from flask import *
import mysql.connector
import re
import os

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database = 'serve_nave'
)
cursor = mydb.cursor(buffered=True)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
@app.route('/')
def home():
    return render_template("index.html")
@app.route('/unidades')
def unidades():
    return render_template("unidades.html")
@app.route('/eventos')
def eventos():
    return render_template("eventos.html")
@app.route("/user")
def user():
    cookie = request.cookies.get('login')
    cursor.execute(f"select login, img from info_user where login='{cookie}'")
    login = cursor.fetchone()
    if login:
        return redirect(f"/user/{login[0]}")
    else:
        return render_template("area do aluno.html")
@app.route("/user/<login>")
def user_login(login):
    cookie = request.cookies.get('login')
    cursor.execute(f"select login, img from info_user where login='{cookie}'")
    login = cursor.fetchone()
    if login:
        return render_template("log_user.html", account=login[0], img=login[1])
    else:
        return redirect("/user")
@app.route("/user/img", methods= ['GET', 'POST'])
def img():
    if request.method == "POST":
        login = request.cookies.get('login')
        arquivos = request.files['input_img']
        arquivos.save(f'static/uploads/img_perfil_{login}.jpg')
        cursor.execute(f"update info_user set img = 'img_perfil_{login}' where login = '{login}'")
        mydb.commit()
        return ['imagem salva']
    else:
        login = request.cookies.get('login')
        cursor.execute(f"select * from info_user where login='{login}'")
        requisição = cursor.fetchone()
        json = {'login':requisição[0], 'nome':requisição[1], 'nome_s':requisição[2], 'sexo':requisição[3], 'email':requisição[4], 'data_n': requisição[5].strftime("%Y-%m-%d"), 'cpf':requisição[6], 'cell': requisição[7], 'uf':requisição[8], 'municipio':requisição[9], 'cor': requisição[10]}
        return json
@app.route("/user")
def Login(login):
    res = make_response(redirect(f"/user/{login}"))
    res.set_cookie("login",login)
    return res
def Cad(cad, cad_senha):
    return {'template':render_template("finalizar_cad.html", login=cad, senha=cad_senha)}
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
@app.route("/user/end", methods = ["POST"])
def finalizar_cad():
    login, senha, nome, nome_s = request.form.get("user"),request.form.get("user_senha"),request.form.get("nome"), request.form.get("nome_s")
    sexo, email, data_n, cpf = request.form.get("sexo"), request.form.get("email"), request.form.get("data_n"), request.form.get("cpf")
    cell, uf, municipio, cor = request.form.get("celular"), request.form.get("uf"), request.form.get("municipio"), request.form.get("cor")
    itens = {'login':login, 'senha':senha, 'nome':nome, 'nome_s':nome_s, 'sexo':sexo, 'email':email, 'data_n': data_n, 'cpf':cpf, 'cell': cell, 'uf':uf, 'municipio':municipio, 'cor': cor}
    clean = []
    for i in itens.items():clean.append(sanitize(i))
    cursor.execute(f"""insert into usuarios values('{clean[0]}', '{clean[1]}');""")
    cursor.execute(f'''insert into info_user values('{clean[0]}', '{clean[2]}', '{clean[3]}', '{clean[4]}', '{clean[5]}', '{clean[6]}'
    , '{clean[7]}', '{clean[8]}', '{clean[9]}', '{clean[10]}', '{clean[11]}', 'defaut_user')''')
    mydb.commit()
    return Login(login)
@app.route("/edit", methods = ["POST"])
def editar_cad():
    login = request.form.get('login')
    if login:
        senha = request.form.get("senha_antiga")
        cursor.execute(f"select senha from usuarios where login = '{login}'")
        requisicao = cursor.fetchone()
        if senha == requisicao:
            nova_senha = request.form.get("senha_nova")
    else:
        login = request.cookies.get("login")
        nome, nome_s = request.form.get("nome"), request.form.get("nome_s")
        sexo, email, data_n, cpf = request.form.get("sexo"), request.form.get("email"), request.form.get("data_n"), request.form.get("cpf")
        cell, uf, municipio, cor = request.form.get("celular"), request.form.get("uf"), request.form.get("municipio"), request.form.get("cor")
        itens = {'nome':nome, 'nome_s':nome_s, 'sexo':sexo, 'email':email, 'data_n': data_n, 'cpf':cpf, 'cell': cell, 'uf':uf, 'municipio':municipio, 'cor': cor}
        clean = []
        for i in itens.items():clean.append(sanitize(i))
        sql = f'''update info_user set nome ='{clean[0]}', nome_s='{clean[1]}', sexo='{clean[2]}', email='{clean[3]}', data_nascimento ='{clean[4]}', cpf='{clean[5]}'
        , cell='{clean[6]}', uf='{clean[7]}', cidade='{clean[8]}', cor='{clean[9]}' where login='{login}' '''
        cursor.execute(sql)
        mydb.commit()
        return 'Dados alterados com sucesso'
@app.route('/user/val', methods =["POST"])
def validacion():
    validar = request.form.get('validar')
    if validar == 'cad':
        cad = request.form.get("cad")
        cad_senha = request.form.get("senha1")
        confirmação = request.form.get("senha2")
        sql = f"select login from usuarios where login='{cad}'"
        cursor.execute(sql)
        verificação = cursor.fetchone()
        if verificação == None:
            if cad_senha == confirmação:
                return Cad(cad, cad_senha)
            else: 
                return {'alerta':"Senhas distintas"}
        else:
            return {'alerta':'Login já cadastrado'}
    else:
        login = request.form.get("login")
        senha = request.form.get("senha")
        sql = f"select senha from usuarios where login='{login}'"
        cursor.execute(sql)
        verificação = cursor.fetchone()
        print(cursor.rowcount)
        if verificação == None:
            return 'Login inexistente'
        elif verificação[0] == senha:
            return Login(login)
        else:
            return 'Senha incorreta'
app.run(host = '0.0.0.0', debug=True)
