import os
import secrets
from decimal import Decimal, InvalidOperation
from flask import Flask, abort, redirect, render_template, request, url_for

from repositories.catalogo_repo import (
    atualizar_estoque,
    buscar_produto,
    cadastrar_produto,
    deletar_produto,
    editar_produto,
    listar_produtos,
)
from utils.imagens import salvar_imagem
from flask import session
from auth import bp_auth

app = Flask(__name__)
app.config["SECRET_KEY"] = (
    os.environ.get("FLASK_SECRET_KEY")
    or secrets.token_hex(32)
)

app.register_blueprint(bp_auth)


@app.before_request
def proteger_admin():
    if (
        request.path.startswith("/admin")
        and request.endpoint not in ("auth.login", "auth.sair")
        and not session.get("admin_id")
    ):
        return redirect(url_for("auth.login"))
    
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # Upload de até 5 MB.

TIPOS_PRODUTO = {"Buquê", "Arranjo", "Flor individual"}


def validar_dados_produto(formulario):
    """Converte e valida os campos enviados pelo formulário HTML."""
    tipo = formulario.get("tipo_produto", "").strip()
    nome = formulario.get("nome_flor", "").strip()
    try:
        preco = Decimal(formulario.get("preco", ""))
        estoque = int(formulario.get("estoque", ""))
    except (ValueError, TypeError, InvalidOperation):
        raise ValueError("Informe preço e estoque válidos.")
    if tipo not in TIPOS_PRODUTO:
        raise ValueError("Selecione um tipo de produto válido.")
    if not nome or len(nome) > 150 or not preco.is_finite() or preco <= 0:
        raise ValueError("Nome ou preço inválido.")
    if estoque < 0 or preco > Decimal("99999999.99") or preco.as_tuple().exponent < -2:
        raise ValueError("Estoque ou preço inválido.")
    return tipo, nome, preco, estoque


@app.route("/")
def inicio():
    produtos = listar_produtos()
    categoria = request.args.get("categoria", "Todos")

    categorias_validas = ["Buquê", "Arranjo", "Flor individual"]

    if categoria in categorias_validas:
        produtos = [
            produto for produto in produtos
            if produto[1] == categoria
        ]
    else:
        categoria = "Todos"

    return render_template(
        "index.html",
        produtos=produtos,
        categoria=categoria
    )


@app.route("/admin/")
def admin():
    return redirect(url_for("estoque_admin"))


@app.route("/admin/produtos/cadastrar", methods=["GET", "POST"])
def cadastrar_produto_admin():
    if request.method == "POST":
        try:
            dados = validar_dados_produto(request.form)
            nome_imagem = salvar_imagem(request.files.get("imagem"), app.static_folder)
        except ValueError as erro:
            return str(erro), 400
        try:
            cadastrar_produto(*dados, nome_imagem)
        except Exception:
            # Em caso de falha no banco, não deixar uma foto órfã.
            from utils.imagens import apagar_imagem
            apagar_imagem(nome_imagem, app.static_folder)
            raise
        return redirect(url_for("estoque_admin"))
    return render_template("admin/cadastrar_produto.html", pagina_ativa="cadastro")


@app.route("/admin/estoque")
def estoque_admin():
    produtos = listar_produtos()
    return render_template("admin/estoque.html", produtos=produtos, pagina_ativa="estoque")


@app.route("/admin/estoque/atualizar/<int:id>", methods=["POST"])
def atualizar_estoque_admin(id):
    estoque = request.form.get("estoque", type=int)
    if estoque is None or estoque < 0:
        return "Informe uma quantidade válida.", 400
    if not atualizar_estoque(id, estoque):
        abort(404, description="Produto não encontrado.")
    return redirect(url_for("estoque_admin"))


@app.route("/admin/estoque/editar/<int:id>", methods=["GET", "POST"])
def editar_produto_admin(id):
    produto = buscar_produto(id)
    if produto is None:
        abort(404, description="Produto não encontrado.")

    if request.method == "POST":
        try:
            dados = validar_dados_produto(request.form)
            nome_imagem = salvar_imagem(request.files.get("imagem"), app.static_folder)
        except ValueError as erro:
            return str(erro), 400

        try:
            editar_produto(id, *dados, nome_imagem)
        except Exception:
            from utils.imagens import apagar_imagem
            apagar_imagem(nome_imagem, app.static_folder)
            raise
        # Remover imagem anterior somente após a atualização bem-sucedida.
        if nome_imagem and produto[5]:
            from utils.imagens import apagar_imagem
            apagar_imagem(produto[5], app.static_folder)
        return redirect(url_for("estoque_admin"))

    return render_template("admin/editar_produto.html", produto=produto, pagina_ativa="estoque")


@app.route("/admin/estoque/deletar/<int:id>", methods=["POST"])
def deletar_produto_admin(id):
    produto = buscar_produto(id)
    if produto is None or not deletar_produto(id):
        abort(404, description="Produto não encontrado.")
    from utils.imagens import apagar_imagem
    apagar_imagem(produto[5], app.static_folder)
    return redirect(url_for("estoque_admin"))


if __name__ == "__main__":
    app.run(debug=True)  # Somente desenvolvimento local; desative em produção.
    app.run(host="0.0.0.0", port=5000, debug=True)

