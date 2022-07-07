import datetime
import json
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main():
    return render_template("index.html", data=datetime.datetime.utcnow())

@app.route('/about/')
def about():
    return render_template('about.html')


@app.get('/contatos_direto_codigo')
def contatos_direto_codigo():
    f = open("dados/contatos.json", "r")
    contatos_json = json.load(f)
    print(contatos_json["contatos"][1]["nome"])

    html_output = "<table>"
    html_output += "<tr> <th>Nome</th> <th>Telefone</th> <th>Data de Nascimento</th> </tr>"
    for contato in contatos_json["contatos"]:
        html_output += "<tr>"
        html_output += "<td>" + contato["nome"] + "</td>"
        html_output += "<td>" + contato["telefone"] + "</td>"
        html_output += "<td>" + contato["data_nascimento"] + "</td>"
        html_output += "</tr>"
        
    html_output += "</table>"

    return html_output

@app.get('/contatos')
def contatos():
    # CARREGA DADOS DE UM ARQUIVO
    f = open("dados/contatos.json", "r", encoding="utf8")
    contatos_json = json.load(f)

    from pprint import pprint
    pprint(contatos_json["contatos"])

    # RENDERIZA A PÁGINA COM OS DADOS DE CONTATOS
    return render_template("contatos.html", contatos=contatos_json["contatos"])
