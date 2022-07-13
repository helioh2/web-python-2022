listaOriginal = document.getElementById("contatos").innerHTML;

function buscaAjax(){
    //document.getElementById("contatos").innerHTML = "BUSCANDO..."
    strBusca = document.getElementById("buscaInput").value

    if (strBusca === "") {
        document.getElementById("contatos").innerHTML = listaOriginal;
        return;
    }
    const timeDelay = 1000;

    // Create an XMLHttpRequest object
    const xhttp = new XMLHttpRequest();

    // Define a callback function
    xhttp.onload = function(){
        if (strBusca === "") {
            document.getElementById("contatos").innerHTML = listaOriginal
            return;
        }
        
        json = JSON.parse(this.responseText);
        console.log(json)
        htmlPart = "<table class='table table-striped'> <thead>  <tr> <th>Nome</th> <th>Telefone</th> <th>Data de Nascimento</th> </tr> </thead> <tbody>";
        json.forEach( function(item, index){
            htmlPart += "<tr>";
            htmlPart += "<td>"+item["nome"]+"</td>";
            htmlPart += "<td>"+item["telefone"]+"</td>";
            htmlPart += "<td>"+item["data_nascimento"]+"</td>";
            htmlPart += "</tr>";
        })
        htmlPart += "</tbody>";
        htmlPart += "</table>";

        document.getElementById("contatos").innerHTML = htmlPart
    }

    sendRequest = function(){
        xhttp.open("GET", "{{url_for('contatos_json')}}?busca="+strBusca);
        xhttp.send();
    }

    sendRequest();

}