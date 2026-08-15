from wsgiref.simple_server import make_server


def app(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
    html = b"""
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>WSGI</title>
    </head>
    <body>
        WSGI
    </body>
    </html>
    """

    return [html]


make_server("", 5001, app).serve_forever()
