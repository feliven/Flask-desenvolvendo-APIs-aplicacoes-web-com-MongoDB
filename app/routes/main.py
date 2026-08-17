from flask import (
    Blueprint,
    jsonify,
    request,
    current_app,
    render_template,
    redirect,
    url_for,
    flash,
    session,
)
from app.models.login_payload import LoginPayload
from app.models.produto import Produto, ProdutoDbModel, UpdateProduto
from app.models.venda import Venda
from app.decorators import token_required
from pydantic import ValidationError
from app import db
from bson import ObjectId
from datetime import datetime, timedelta, timezone
import jwt
import csv
import io

main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/")
def index():
    if "jwt_token" not in session:
        return redirect(url_for("main_bp.login"))
    return redirect(url_for("main_bp.dashboard"))


@main_bp.route("/dashboard")
def dashboard():
    if "jwt_token" not in session:
        return redirect(url_for("main_bp.login"))
    return render_template("dashboard.html", title="Dashboard")


# RF: O sistema deve permitir listagem de todos os produtos
@main_bp.route("/produtos")
def get_produtos():
    produtos_cursor = db.produtos.find({})

    return render_template("products.html", products=produtos_cursor, title="Produtos")


# RF: O sistema deve permitir a criacao de um novo produto
@main_bp.route("/produtos/novo", methods=["GET", "POST"])
@token_required
def create_produto(jwt_token):
    if request.method == "POST":
        # Check if the incoming request is JSON (API) or Form Data (HTML Form)
        data = request.get_json() if request.is_json else request.form.to_dict()

        try:
            produto = Produto(**data)
        except ValidationError as e:
            if request.is_json:
                return jsonify({"error": e.errors()}), 400
            flash(f"Erro de validação: {e}", "danger")
            return render_template("add_product.html", title="Adicionar Produto"), 400

        result = db.produtos.insert_one(produto.model_dump())

        if request.is_json:
            return (
                jsonify(
                    {
                        "result": str(result),
                        "id": str(result.inserted_id),
                        "message": "Produto criado com sucesso",
                    }
                ),
                201,
            )
        flash("Produto criado com sucesso!", "success")
        return redirect(url_for("main_bp.get_produtos"))

    return render_template("add_product.html", title="Adicionar Produto")


# RF: O sistema deve permitir a visualizacao dos detalhes de um unico produto
@main_bp.route("/produtos/<string:id_produto>")
def get_produto_by_id(id_produto):
    try:
        oid = ObjectId(id_produto)
    except Exception:
        return jsonify({"error": "Erro ao converter ID para ObjectID"}), 500

    produto = db.produtos.find_one({"_id": oid})

    if produto:
        produto_model = ProdutoDbModel(**produto).model_dump(
            by_alias=True, exclude_none=True
        )
        return jsonify(produto_model), 200
    else:
        return (
            jsonify({"error": f"Produto com id {id_produto} não foi encontrado"}),
            404,
        )


# RF: O sistema deve permitir a atualizacao de um unico produto e produto existente
@main_bp.route("/produtos/<string:id_produto>", methods=["PUT"])
@token_required
def update_produto(jwt_token, id_produto):
    try:
        oid = ObjectId(id_produto)
    except Exception:
        return jsonify({"error": "Erro ao converter ID para ObjectID"}), 500

    try:
        produto_atualizado = UpdateProduto(**request.get_json()).model_dump(
            exclude_unset=True
        )
        result = db.produtos.update_one({"_id": oid}, {"$set": produto_atualizado})
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": f"Erro ao atualizar produto. {e}"}), 500

    if result.matched_count == 0:
        return jsonify({"error": "Produto não encontrado"}), 404

    if result.modified_count == 0:
        return jsonify({"message": "Nenhum produto foi alterado"}), 200

    return (
        jsonify(
            {
                "result": str(result),
                "message": "Produto atualizado com sucesso",
            }
        ),
        200,
    )


# RF: O sistema deve permitir a delecao de um unico produto e produto existente
@main_bp.route("/produtos/<string:id_produto>", methods=["DELETE"])
@token_required
def delete_produto(jwt_token, id_produto):
    try:
        oid = ObjectId(id_produto)
    except Exception:
        return jsonify({"error": "Erro ao converter ID para ObjectID"}), 500

    try:
        result = db.produtos.delete_one({"_id": oid})
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": f"Erro ao deletar produto. {e}"}), 500

    if result.deleted_count == 0:
        return jsonify({"error": "Produto não encontrado"}), 404

    return (
        jsonify(
            {
                "result": str(result.raw_result),
                "message": "Produto removido com sucesso",
            }
        ),
        200,
    )


# RF: O sistema deve permitir que um usuário se autentique para obter um token
@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        user_data = LoginPayload(username=username, password=password)

        if user_data.username == "admin" and user_data.password == "123":
            token = jwt.encode(
                {
                    "user_id": username,
                    "exp": datetime.now(timezone.utc) + timedelta(minutes=30),
                },
                current_app.config["SECRET_KEY"],
                algorithm="HS256",
            )
            session["jwt_token"] = token
            return redirect(url_for("main_bp.dashboard"))
        else:
            flash("Credenciais inválidas!", "danger")
            return redirect(url_for("main_bp.login"))
    else:
        return render_template("login.html", title="Login")


@main_bp.route("/vendas")
@token_required
def get_vendas(jwt_token):
    vendas_cursor = db.vendas.find({})

    lista_vendas = [Venda(**venda).model_dump() for venda in vendas_cursor]

    for vendas in vendas_cursor:
        vendas["_id"] = str(vendas["_id"])
        lista_vendas.append(vendas)

    return jsonify(lista_vendas)


@main_bp.route("/vendas/upload", methods=["GET"])
def upload_vendas_pagina():
    if "jwt_token" not in session:
        return redirect(url_for("main_bp.login"))
    return render_template("upload_sales.html", title="Upload de Vendas")


# RF: O sistema deve permitir a importacao de vendas através de um arquivo
@main_bp.route("/vendas/upload", methods=["POST"])
@token_required
def upload_vendas(jwt_token):
    if "file" not in request.files:
        return jsonify({"error": "Arquivo não foi enviado!"}), 400

    file = request.files["file"]

    # if not file.filename or file.filename == "":
    if not file.filename:
        return jsonify({"error": "Arquivo não foi selecionado"}), 400

    if not file.filename.endswith(".csv"):
        return (
            jsonify({"error": "Formato de arquivo inválido. Apenas .csv é aceito."}),
            400,
        )

    csv_stream = io.StringIO(file.stream.read().decode("UTF-8"), newline=None)
    csv_reader = csv.DictReader(csv_stream)

    vendas_para_inserir = []
    lista_erros = []

    for row_num, row in enumerate(csv_reader, 1):
        try:
            linha = Venda.model_validate(row).model_dump(exclude_unset=True)
            vendas_para_inserir.append(linha)
        except ValidationError:
            lista_erros.append(f"Linha {row_num} com dados inválidos")
        except Exception:
            lista_erros.append(f"Linha {row_num} com erro inesperado nos dados")

    if vendas_para_inserir:
        try:
            db.vendas.insert_many(vendas_para_inserir)
        except Exception as e:
            return jsonify({"error": f"Erro ao inserir dados de vendas. {e}"}), 500

    return (
        jsonify(
            {
                "message": "Upload do arquivo de vendas realizado com sucesso",
                "vendas_importadas": len(vendas_para_inserir),
                "erros_encontrados": lista_erros,
            }
        ),
        200,
    )
