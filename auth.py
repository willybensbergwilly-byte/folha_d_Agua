
from flask import Blueprint, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash
from repositories.admin_repo import buscar_admin

bp_auth = Blueprint("auth", __name__)


@bp_auth.route("/admin/login", methods=["GET", "POST"])
def login():
    if session.get("admin_id"):
        return redirect(url_for("estoque_admin"))

    erro = None
    if request.method == "POST":
        usuario = request.form.get("usuario", "").strip()
        senha = request.form.get("senha", "")
        admin = buscar_admin(usuario)
        if admin and check_password_hash(admin[2], senha):
            session.clear()
            session["admin_id"] = admin[0]
            session["admin_usuario"] = admin[1]
            return redirect(url_for("estoque_admin"))
        erro = "Usuário ou senha incorretos."
    return render_template("admin/login.html", erro=erro)


@bp_auth.route("/admin/sair", methods=["POST"])
def sair():
    session.clear()
    return redirect(url_for("inicio"))
