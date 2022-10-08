from flask import *
import mysql.connector
import requests

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
        x = request.form.get("login")
        y = request.form.get("senha")
        return render_template("log_user.html", account=x) 
app.run(debug=True)
