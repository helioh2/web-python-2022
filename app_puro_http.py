from http.server import BaseHTTPRequestHandler, HTTPServer
# BaseHTTPRequestHandler = classe responsável por tratar requisições HTTP

class MeuHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # CRIANDO CABEÇALHO DA RESPOSTA
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        print(self.requestline())

        # CRIAR O CORPO DA RESPOSTA
        file_ = open("index.html", "r")
        mensagem = file_.read()
        mensagem += str(self.requestline)
        self.wfile.write(bytes(mensagem, "utf8"))

   
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        message = "Hello, World! Here is a POST response"
        self.wfile.write(bytes(message, "utf8"))



with HTTPServer(('', 8000), MeuHandler) as server:
    server.serve_forever()