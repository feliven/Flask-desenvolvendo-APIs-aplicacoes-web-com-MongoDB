from flask import Blueprint, jsonify

main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/")
def index():
    return jsonify({"message": "Bem vindo ao Stylesync!"})


# RF: O sistema deve permitir listagem de todos os produtos
@main_bp.route("/products")
def get_products():
    return jsonify({"message": "Esta é a rota de listagem dos produtos"})


# RF: O sistema deve permitir a criacao de um novo produto
@main_bp.route("/products", methods=["POST"])
def create_product():
    return jsonify({"message": "Esta é a rota de criação de produto"})


# RF: O sistema deve permitir a visualizacao dos detalhes de um unico produto
@main_bp.route("/product/<int:product_id>")
def get_product_by_id(product_id):
    return jsonify(
        {
            "message": f"Esta é a rota de visualizacao do detalhe do id do produto {product_id}"
        }
    )


# RF: O sistema deve permitir a atualizacao de um unico produto e produto existente
@main_bp.route("/product/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    return jsonify(
        {"message": f"Esta é a rota de atualizacao do produto com o id {product_id}"}
    )


# RF: O sistema deve permitir a delecao de um unico produto e produto existente
@main_bp.route("/product/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    return jsonify(
        {"message": f"Esta é a rota de deleção do produto com o id {product_id}"}
    )


# RF: O sistema deve permitir que um usuário se autentique para obter um token
@main_bp.route("/login", methods=["POST"])
def login():
    return jsonify({"message": "Fazer login"})


# RF: O sistema deve permitir a importacao de vendas através de um arquivo
@main_bp.route("/sales/upload", methods=["POST"])
def upload_sales():
    return jsonify({"message": "Esta é a rota de upload do arquivo de vendas"})
