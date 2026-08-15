from wsgiref.simple_server import make_server


def app(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])

    with open("index.html", "r", encoding="utf-8") as pagina:
        html = pagina.read()

    return [html.encode("utf-8")]


make_server("", 5001, app).serve_forever()
