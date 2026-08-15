from wsgiref.simple_server import make_server


def app(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])

    with open("index.html", "r", encoding="utf-8") as pagina:
        html = pagina.read()

    produtos = [
        {"nome": "Notebook", "valor": 7499.99},
        {"nome": "Mouse", "valor": 125.99},
        {"nome": "Teclado", "valor": 450.99},
        {"nome": "Monitor", "valor": 2100.99},
    ]

    linhas_html = ""
    for produto in produtos:
        linhas_html += f"<li>{produto['nome']} - R$ {produto['valor']}</li>"

    html_final = html.replace("{{PRODUTOS}}", linhas_html)

    return [html_final.encode("utf-8")]


make_server("", 5001, app).serve_forever()
