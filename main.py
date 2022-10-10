from distutils.log import error
from fileinput import filename
from flask import *
import mysql.connector
import requests

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
@app.route('/user', methods =["GET", "POST"])
def validacion():
    if request.method == "POST":
        login = request.form.get("login")
        senha = request.form.get("senha")
        verificação = f"select senha from usuarios where login='{login}'"
        cursor.execute(verificação)
        verif = cursor.fetchone()
        print(verif)
        if verif == None:
            flash('Login não encontrado')
            return user()
        else:
         if verif[0] == senha:
            return Login(login)
         else: 
            flash('Senha incorreta')
            return user()    
app.run(debug=True)
