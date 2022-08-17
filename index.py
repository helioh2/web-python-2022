import datetime
import json
from time import strptime
from typing import List
from flask import (
    Flask,
    session,
    escape,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_sqlalchemy import Pagination, SQLAlchemy
from config import setup_database

from model import Contato, Usuario, db

from flask_migrate import Migrate

from flask_session import Session

from validacao_form import validar_form

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

setup_database(app)

db.init_app(app)
migrate = Migrate(app, db)

PER_PAGE = 10


@app.get("/")
def main():
    return render_template("index.html", data=datetime.datetime.utcnow())


@app.get("/about/")
def about():
    return render_template("about.html")

@app.get("/contatos_json")
def contatos_json():

     ## Pegar usuario logado, se existir:
    usuario = None
    if "user" in session.keys():
        usuario = session["user"]

    if not usuario:
        return {"erro": "Usuário não logado"}

    busca_str = "%" + request.args.get("busca") + "%"
    
    contatos:List[Contato] = (
        Contato.query                                # objeto Query
                .filter_by(id_usuario=usuario.id)    # objeto Query
                .filter(Contato.nome.ilike(busca_str))  # objeto Query
                .all()  # List[Contato]
    )

    return json.dumps([contato.as_dict() for contato in contatos])


@app.get("/contatos")
def contatos():

    ## Pegar usuario logado, se existir:
    usuario = None
    if "user" in session.keys():
        usuario = session["user"]

    if not usuario:
        return "É NECESSÁRIO ESTAR LOGADO PARA VER A LISTA DE CONTATOS"  # TODO: MELHORAR

    try:
        pag = int(request.args.get("page")) ## pode dar erro de conversão de string que não é inteiro
    except:
        pag = 1

    print("Página que veio na URL:", pag)

    contatos:Pagination = (
        Contato.query                                # objeto Query
                .filter_by(id_usuario=usuario.id)    # objeto Query
                .paginate(page=pag, per_page=PER_PAGE)       # objeto Pagination
    )

    print("Quantidade total de páginas:", contatos.pages)
    print("Página atual:", contatos.page)
    print("Tem mais páginas?", contatos.has_next)
    print("Items:", contatos.items)

    return render_template("contatos.html", contatos=contatos)  #mandando dados para View


@app.get("/adicionar_contato_form")
def adicionar_contato_form():
    return render_template("adicionar_contato_form.html")


@app.post("/adicionar_contato_action")
def adicionar_contato_action():

    resultado_validacao = validar_form(request.form)

    if resultado_validacao:  # se ele não for {}
        contato = dict(request.form)
        return render_template(
            "adicionar_contato_form.html",
            contato=contato,
            erros_validacao=resultado_validacao,
        )

    usuario = session["user"]

    if not usuario:
        return "É NECESSÁRIO ESTAR LOGADO PARA ADICIONAR CONTATO"  # TODO: MELHORAR

    #else
    nome = request.form["nome"]
    telefone = request.form["telefone"]
    data_nascimento = request.form["data_nascimento"]
    detalhes = request.form["detalhes"]
   
    contato = Contato(
        nome=nome, 
        telefone=telefone, 
        data_nascimento=data_nascimento,
        detalhes=detalhes,
        id_usuario=usuario.id)

    db.session.merge(contato)  # adiciona ou atualiza
    db.session.commit()
    
    return redirect(url_for("contatos"))


@app.get("/remover_contato_action")
def remover_contato_action():

    id_ = request.args["id"]

    contato = Contato.query.filter_by(id=id_).first()
    db.session.delete(contato)
    db.session.commit()

    return redirect(url_for("contatos"))


@app.get("/alterar_contato_form")
def alterar_contato_form():
    id_ = request.args["id"]

    contato = Contato.query.filter_by(id=id_).first()

    return render_template("adicionar_contato_form.html", contato=contato)


@app.get("/cadastrar_usuario_form")
def cadastrar_usuario_form():
    return render_template("cadastrar.html")


@app.route("/cadastrar_usuario_action", methods=["GET", "POST"])
def cadastrar_usuario_action():

    if request.method == "POST":
        username = request.form.get("username")
        senha = request.form.get("senha")

        usuario = Usuario.query.filter_by(username=username).first()

        if usuario:
            return "USUÁRIO JA EXISTE"  ## TODO: MELHORAR ISSO

        #else
        usuario = Usuario(username=username)

        usuario.set_password(senha)

        db.session.add(usuario) ## INSERT

        db.session.commit() ## COMMIT DA TRANSAÇÃO

        # SETAR A SESSÃO (COOKIE)
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

        # else
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