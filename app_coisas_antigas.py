
import json


# @app.get('/contatos_direto_codigo')
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


@app.get('/contatos_com_objetos')
def contatos_com_objetos():
    
    conn = psycopg2.connect("dbname=agenda user=postgres password=root")
    cursor_ = conn.cursor()

    cursor_.execute("SELECT * FROM contatos WHERE deletado='false'")

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



##Login e logout com cookies:

@app.route("/login_action", methods = ['POST', 'GET'])
def login_action():

    if request.method == "POST":
        username = request.form.get("username")

        ## TODO: AUTENTICAÇÃO

        resp = make_response(render_template("index.html"))
        resp.set_cookie('userId', username) # exemplo: cookie userId='fulano'
        resp.set_cookie('zuera', 'never ends')

        return resp

    #else
    return render_template("erro.html")
    

@app.get("/logout_action")
def logout_action():
    resp = make_response(render_template("index.html"))
    resp.delete_cookie("userId")

    return resp