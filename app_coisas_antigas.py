
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