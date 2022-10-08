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
@app.route('/user/usuario', methods =["GET", "POST"])
def validacion():
    if request.method == "POST":
        login = request.form.get("login")
        senha = request.form.get("senha")
        verificação = f"select senha from usuarios where login='{login}'"
        cursor.execute(verificação)
        verif = cursor.fetchone()
        if verif[0] == senha:
            return render_template("log_user.html", account=login)
        else:
            return 'ERROR'

         
app.run(debug=True)
