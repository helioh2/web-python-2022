import datetime
import json
from time import strptime
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import psycopg2.extras

class Contato:
    """
    DTO = Data Transfer Object
    """

    def __init__(self, id, nome, telefone, data_nascimento, detalhes):
        self.id = id
        self.nome = nome
        self.telefone = telefone
        self.data_nascimento = data_nascimento
        self.detalhes = detalhes



@app.get('/')
def main():
    return render_template("index.html", data=datetime.datetime.utcnow())

@app.get('/about/')
def about():
    return render_template('about.html')

@app.get('/contatos_json')
def contatos_json():
    # CARREGA DADOS DE UM ARQUIVO
    f = open("dados/contatos.json", "r", encoding="utf8")
    contatos_json = json.load(f)

    from pprint import pprint
    pprint(contatos_json["contatos"])

    # RENDERIZA A PÁGINA COM OS DADOS DE CONTATOS
    return render_template("contatos.html", contatos=contatos_json["contatos"])



@app.get('/contatos')
def contatos():
    
    conn = psycopg2.connect("dbname=agenda user=postgres password=root")
    cursor_ = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor_.execute("SELECT * FROM contatos WHERE deletado='false'")

    resultados = cursor_.fetchall()

    conn.close()

    from pprint import pprint
    pprint(resultados)
    
    return render_template("contatos.html", contatos=resultados)



@app.get('/adicionar_contato_form')
def adicionar_contato_form():
    return render_template('adicionar_contato_form.html')

@app.post('/adicionar_contato_action')
def adicionar_contato_action():

    conn = psycopg2.connect("dbname=agenda user=postgres password=root")
    cursor_ = conn.cursor()

    nome = request.form["nome"]
    telefone = request.form["telefone"]
    data_nascimento = request.form["data_nascimento"]
    # data_nascimento = datetime.datetime.strptime(data_nascimento_origem, "%d/%m/%Y")
    detalhes = request.form["detalhes"]

    id_ = request.form["id"]

    if id_: # se id não é vazio
        sql = """UPDATE contatos SET nome=%s, telefone=%s, data_nascimento=%s,
                                    detalhes=%s WHERE id=%s"""
        val = (nome, telefone, data_nascimento, detalhes, id_)
    else:
        sql = """INSERT INTO contatos (nome, telefone, data_nascimento, detalhes) 
                                VALUES (%s, %s, %s, %s)"""
        val = (nome, telefone, data_nascimento, detalhes)
    
    cursor_.execute(sql, val)

    conn.commit()
    conn.close()

    return redirect(url_for("contatos"))


@app.get('/remover_contato_action')
def remover_contato_action():
    
    id_ = request.args["id"]

    conn = psycopg2.connect("dbname=agenda user=postgres password=root")
    cursor_ = conn.cursor()

    sql_ = "UPDATE contatos SET deletado='true' WHERE id={}".format(id_)

    cursor_.execute(sql_)

    conn.commit()
    conn.close()

    return redirect(url_for("contatos"))


@app.get('/alterar_contato_form')
def alterar_contato_form():
    id_ = request.args["id"]
    
    conn = psycopg2.connect("dbname=agenda user=postgres password=root")
    cursor_ = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    sql_ = "SELECT * FROM contatos WHERE deletado='false' AND id={}".format(id_)

    cursor_.execute(sql_)
    resultado = cursor_.fetchone()

    from pprint import pprint
    pprint(resultado)

    return render_template('adicionar_contato_form.html', contato=resultado)