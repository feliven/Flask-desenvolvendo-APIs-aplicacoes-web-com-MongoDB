from flask import Flask
from pymongo import MongoClient

db = None


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    global db

    try:
        client = MongoClient(app.config["MONGO_URI"])
        db = client.get_default_database()
        # produtos = db["produtos"]

    except Exception as e:
        print("Erro ao se conectar ao MongoDB.", e)

    from .routes.main import main_bp

    app.register_blueprint(main_bp)

    return app
