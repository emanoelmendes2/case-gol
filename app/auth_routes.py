from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import db, Usuario
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = Usuario.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for("dashboard.index"))
        else:
            flash("Nome de usuário ou senha incorretos.", "danger")
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        if not username or not email or not password or not confirm_password:
            flash("Todos os campos são obrigatórios.", "danger")
        elif password != confirm_password:
            flash("As senhas não coincidem.", "danger")
        else:
            new_user = Usuario(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash("Cadastro realizado com sucesso!", "success")
            return redirect(url_for("auth.login"))
    return render_template("register.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))