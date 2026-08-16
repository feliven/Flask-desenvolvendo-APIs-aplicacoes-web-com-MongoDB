from flask import Blueprint, jsonify, request
from app.models.login_payload import LoginPayload
from app.models.produto import *
from pydantic import ValidationError
from app import db
from bson import ObjectId

main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/")
def index():
    return jsonify({"message": "Bem vindo ao Stylesync!"})


# RF: O sistema deve permitir listagem de todos os produtos
@main_bp.route("/produtos")
def get_produtos():
    produtos_cursor = db.produtos.find({})

    lista_produtos = [
        ProdutoDbModel(**produto).model_dump(by_alias=True, exclude_none=True)
        for produto in produtos_cursor
    ]

    for produtos in produtos_cursor:
        produtos["_id"] = str(produtos["_id"])
        lista_produtos.append(produtos)

    return jsonify(lista_produtos)


# RF: O sistema deve permitir a criacao de um novo produto
@main_bp.route("/produtos", methods=["POST"])
def create_produto():
    return jsonify({"message": "Esta é a rota de criação de produto"})


# RF: O sistema deve permitir a visualizacao dos detalhes de um unico produto
@main_bp.route("/produtos/<string:id_produto>")
def get_produto_by_id(id_produto):
    try:
        oid = ObjectId(id_produto)
    except Exception as e:
        return jsonify({"error": "Erro ao converter ID para ObjectID"}), 500

    produto = db.produtos.find_one({"_id": oid})

    if produto:
        produto_model = ProdutoDbModel(**produto).model_dump(
            by_alias=True, exclude_none=True
        )
        return jsonify(produto_model)
    else:
        return jsonify({"error": f"Produto com id {id_produto} não foi encontrado"})


# RF: O sistema deve permitir a atualizacao de um unico produto e produto existente
@main_bp.route("/produtos/<string:id_produto>", methods=["PUT"])
def update_produto(id_produto):
    return jsonify(
        {"message": f"Esta é a rota de atualizacao do produto com o id {id_produto}"}
    )


# RF: O sistema deve permitir a delecao de um unico produto e produto existente
@main_bp.route("/produtos/<string:id_produto>", methods=["DELETE"])
def delete_produto(id_produto):
    return jsonify(
        {"message": f"Esta é a rota de deleção do produto com o id {id_produto}"}
    )


# RF: O sistema deve permitir que um usuário se autentique para obter um token
@main_bp.route("/login", methods=["POST"])
def login():
    try:
        raw_data = request.get_json()
        user_data = LoginPayload(**raw_data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": "Erro durante a requisição do dado"}), 500

    if user_data.username == "admin" and user_data.password == "123":
        return jsonify({"message": "Login bem-sucedido!"})
    else:
        return jsonify({"message": "Credenciais invalidas!"})

    return jsonify(
        {"message": f"Realizar o login do usuario {user_data.model_dump_json()}"}
    )


# RF: O sistema deve permitir a importacao de vendas através de um arquivo
@main_bp.route("/vendas/upload", methods=["POST"])
def upload_vendas():
    return jsonify({"message": "Esta é a rota de upload do arquivo de vendas"})
