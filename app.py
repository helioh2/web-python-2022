import datetime
import json
from flask import (
    Flask,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
    session,
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from model import Contato, Usuario, db
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:root@localhost:5432/agenda"
app.config["SQLALCHEMY_ECHO"] = True

db.init_app(app)
migrate = Migrate(app, db)

PER_PAGE_DEFAULT = 10


@app.get("/")
def main():
    return render_template("index.html", data=datetime.datetime.utcnow())


@app.get("/about/")
def about():
    return render_template("about.html")


@app.get("/contatos_json")
def contatos_json():

    str_busca = "%" + request.args["busca"] + "%"

    usuario = session["user"]

    contatos = Contato.query.filter_by(_deleted=False, id_usuario=usuario)\
                            .filter(Contato.nome.ilike(str_busca))\
                            .all()

    return json.dumps([contato.as_dict() for contato in contatos])


@app.get("/contatos")
def contatos():

    try:
        page = int(request.args["page"])
    except:
        page = 1

    usuario = session["user"]

    paginacao = (
        Contato.query.filter_by(_deleted=False, id_usuario=usuario.id)
                    .order_by(Contato.nome)
                    .paginate(page=page, per_page=PER_PAGE_DEFAULT)
    )

    contatos = paginacao.items
    total_paginas = paginacao.pages

    return render_template(
        "contatos.html", contatos=contatos, total_paginas=total_paginas, pagina=page
    )


@app.get("/adicionar_contato_form")
def adicionar_contato_form():
    return render_template("adicionar_contato_form.html")


@app.post("/adicionar_contato_action")
def adicionar_contato_action():

    nome = request.form["nome"]
    telefone = request.form["telefone"]
    data_nascimento = request.form["data_nascimento"]
    detalhes = request.form["detalhes"]
    id_ = request.form["id"] if request.form["id"] else None
    usuario = session["user"]

    contato = Contato(
        id=id_,
        nome=nome,
        telefone=telefone,
        data_nascimento=data_nascimento,
        detalhes=detalhes,
        id_usuario=usuario.id,
    )

    db.session.merge(contato)
    db.session.commit()

    return redirect(url_for("contatos"))


@app.get("/remover_contato_action")
def remover_contato_action():

    id_ = request.args["id"]

    contato = Contato.query.filter_by(id=int(id_)).first()

    contato._deleted = True
    db.session.merge(contato)  # atualiza contato
    db.session.commit()

    return redirect(url_for("contatos"))


@app.get("/alterar_contato_form")
def alterar_contato_form():
    id_ = request.args["id"]

    contato = Contato.query.filter_by(id=id_, _deleted=False).first()

    return render_template("adicionar_contato_form.html", contato=contato)


@app.get("/cadastrar_usuario_form")
def cadastrar_usuario_form():
    return render_template("cadastrar.html")


@app.route("/cadastrar_usuario_action", methods=["GET", "POST"])
def cadastrar_usuario_action():

    if request.method == "POST":
        username = request.form.get("username")
        senha = request.form.get("senha")

        usuario = Usuario(username=username)
        usuario.set_password(senha)
        db.session.add(usuario)
        db.session.commit()

        session["user"] = usuario

        return render_template("index.html")

    # else
    return render_template("erro.html")


@app.get("/login_form")
def login_form():
    return render_template("login_form.html")


@app.route("/login_action", methods=["POST", "GET"])
def login_action():

    if request.method == "POST":
        username = request.form.get("username")
        senha = request.form.get("senha")

        ## AUTENTICAÇÃO
        usuario: Usuario = Usuario.query.filter_by(username=username).first()
        if not usuario:
            return "Usuário não existe"  ## TODO: MELHORAR ISSO

        if not usuario.check_password(senha):
            return "Senha incorreta"  ## TODO: MELHORAR ISSO

        session["user"] = usuario

        resp = make_response(render_template("index.html"))

        return resp

    # else
    return render_template("erro.html")


@app.get("/logout_action")
def logout_action():
    resp = make_response(render_template("index.html"))
    session["user"] = None

    return resp
