import datetime
import json
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from model import Contato, db

app = Flask(__name__)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost:5432/agenda'
app.config["SQLALCHEMY_ECHO"] = True
db.init_app(app)
migrate = Migrate(app, db)

@app.get('/')
def main():
    return render_template("index.html", data=datetime.datetime.utcnow())

@app.get('/about/')
def about():
    return render_template('about.html')


@app.get('/contatos')
def contatos():
    
    contatos = Contato.query.filter_by(_deleted=False).all()

    return render_template("contatos.html", contatos=contatos)



@app.get('/adicionar_contato_form')
def adicionar_contato_form():
    return render_template('adicionar_contato_form.html')

@app.post('/adicionar_contato_action')
def adicionar_contato_action():

    nome = request.form["nome"]
    telefone = request.form["telefone"]
    data_nascimento = request.form["data_nascimento"]
    detalhes = request.form["detalhes"]
    id_ = request.form["id"] if request.form["id"] else None

    contato = Contato(id=id_, nome=nome, telefone=telefone, data_nascimento=data_nascimento, detalhes=detalhes)

    db.session.merge(contato)
    db.session.commit()

    return redirect(url_for("contatos"))


@app.get('/remover_contato_action')
def remover_contato_action():
    
    id_ = request.args["id"]

    contato = Contato.query.filter_by(id=int(id_)).first()

    contato._deleted = True
    db.session.merge(contato) #atualiza contato
    db.session.commit()

    return redirect(url_for("contatos"))


@app.get('/alterar_contato_form')
def alterar_contato_form():
    id_ = request.args["id"]
    
    contato = Contato.query.filter_by(id=id_, _deleted=False).first()

    return render_template('adicionar_contato_form.html', contato=contato)