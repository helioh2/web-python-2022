import datetime
import json
from time import strptime
from flask import Flask, redirect, render_template, request, url_for
import psycopg2
import psycopg2.extras

app = Flask(__name__)



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

@app.get('/contatos_com_objetos')
def contatos_com_objetos():
    
    conn = psycopg2.connect("dbname=agenda user=postgres password=root")
    cursor_ = conn.cursor()

    cursor_.execute("SELECT * FROM contatos")

    resultados = cursor_.fetchall()

    from pprint import pprint
    pprint(resultados)

    conn.close()

    """
    resultados:
    [
        (1, 'Fulano da Silva', '636236363', datetime.date(1998, 10, 1), 'BLANBLANBLAJLSKAJALKDJSLKSAJDKLJ'), 
        (2, 'Beltrano de Souza', '23232323', datetime.date(2001, 5, 10), 'blublublublublublu'), 
        (3, 'Ciclana Ferreira', '2431424234', datetime.date(1991, 1, 28), 'nsjksndakjsndkjnsdkjand')
        ]
    """

    contato1 = Contato(resultados[0][0], resultados[0][1], resultados[0][2], resultados[0][3])

    contatos = []  #lista vazia de contatos
    for resultado in resultados:
        id_ = resultado[0]
        nome = resultado[1]
        telefone = resultado[2]
        data_nascimento_date = resultado[3] #datetime
        data_nascimento_str = data_nascimento_date.strftime("%d/%m/%Y")
        detalhes = resultado[4]

        contato = Contato(id_, nome, telefone, data_nascimento_str, detalhes) # criando objeto contato a partir da linha da tabela
        contatos.append(contato)
    
    return render_template("contatos.html", contatos=contatos)


@app.get('/contatos')
def contatos():
    
    conn = psycopg2.connect("dbname=agenda user=postgres password=root")
    cursor_ = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cursor_.execute("SELECT * FROM contatos")

    resultados = cursor_.fetchall()

    conn.close()
    
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

    sql = """INSERT INTO contatos (nome, telefone, data_nascimento, detalhes) 
                            VALUES (%s, %s, %s, %s)"""
    val = (nome, telefone, data_nascimento, detalhes)
    cursor_.execute(sql, val)

    conn.commit()
    conn.close()

    return redirect(url_for("contatos"))
