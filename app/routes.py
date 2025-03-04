from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import db, Usuario, Voo
from flask_login import login_user, logout_user, login_required
import matplotlib.pyplot as plt
from io import BytesIO
import base64

auth_bp = Blueprint("auth", __name__)
dashboard_bp = Blueprint("dashboard", __name__)

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

@dashboard_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def index():
    mercados = Voo.query.with_entities(Voo.mercado).distinct().all()
    plot_url = None
    if request.method == "POST":
        mercado = request.form["mercado"]
        ano_inicio = int(request.form["ano_inicio"])
        mes_inicio = int(request.form["mes_inicio"])
        ano_fim = int(request.form["ano_fim"])
        mes_fim = int(request.form["mes_fim"])

        # Ajustar a lógica de filtragem para considerar o intervalo de datas corretamente
        voos = Voo.query.filter(
            Voo.mercado == mercado,
            (Voo.ano > ano_inicio) | ((Voo.ano == ano_inicio) & (Voo.mes >= mes_inicio)),
            (Voo.ano < ano_fim) | ((Voo.ano == ano_fim) & (Voo.mes <= mes_fim))
        ).all()

        anos_meses = [f"{voo.ano}-{voo.mes}" for voo in voos]
        rpk = [voo.rpk for voo in voos]

        # Calcular o número total de meses selecionados
        total_meses = (ano_fim - ano_inicio) * 12 + (mes_fim - mes_inicio + 1)
        # Ajustar o tamanho do gráfico dinamicamente
        figsize = (max(12, total_meses * 0.5), 6)

        plt.figure(figsize=figsize)
        plt.plot(anos_meses, rpk, marker="o")
        plt.xlabel("Ano-Mês")
        plt.ylabel("RPK")
        plt.title(f"RPK por Ano-Mês para o Mercado {mercado}")

        img = BytesIO()
        plt.savefig(img, format="png")
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()  # Fechar a figura para liberar memória

    return render_template("dashboard.html", mercados=mercados, plot_url=plot_url)