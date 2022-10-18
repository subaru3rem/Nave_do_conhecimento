from distutils.log import error
from fileinput import filename
from nturl2path import pathname2url
from flask import *
import mysql.connector

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
@app.route("/user/j")
def cad():
    return render_template("finalizar_cad.html")
@app.route("/user/j", methods = ["GET", "POST"])
def finalizar_cad():
    pass
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
                        cursor.execute(f"insert into usuarios values ('{cad}', '{cad_senha}')")
                        mydb.commit()
                        return cad()
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
