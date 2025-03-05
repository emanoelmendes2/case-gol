from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Voo
from flask_login import login_required
import matplotlib.pyplot as plt
from io import BytesIO
import base64

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard", methods=["GET", "POST"])
@login_required
def index():
    """ Exibir o dashboard com o gráfico de RPK por Ano-Mês """
    mercados = Voo.query.with_entities(Voo.mercado).distinct().all()
    plot_url = None
    primeiro_voo = Voo.query.order_by(Voo.ano, Voo.mes).first()
    ultimo_voo = Voo.query.order_by(Voo.ano.desc(), Voo.mes.desc()).first()
    mes_ano_inicio = f"{primeiro_voo.mes}/{primeiro_voo.ano}" if primeiro_voo else None
    mes_ano_fim = f"{ultimo_voo.mes}/{ultimo_voo.ano}" if ultimo_voo else None

    if request.method == "POST":
        mercado = request.form["mercado"]
        ano_inicio = int(request.form["ano_inicio"])
        mes_inicio = int(request.form["mes_inicio"])
        ano_fim = int(request.form["ano_fim"])
        mes_fim = int(request.form["mes_fim"])

        #  Validar se os anos e meses estão dentro dos valores disponíveis no banco de dados
        if (ano_inicio < primeiro_voo.ano or (ano_inicio == primeiro_voo.ano and mes_inicio < primeiro_voo.mes) or
            ano_fim > ultimo_voo.ano or (ano_fim == ultimo_voo.ano and mes_fim > ultimo_voo.mes)):
            flash("Os valores de ano e mês devem estar dentro do intervalo disponível.", "danger")
        else:
            # Ajustar a lógica de filtragem para considerar o intervalo de datas corretamente
            voos = Voo.query.filter(
                Voo.mercado == mercado,
                (Voo.ano > ano_inicio) | ((Voo.ano == ano_inicio) & (Voo.mes >= mes_inicio)),
                (Voo.ano < ano_fim) | ((Voo.ano == ano_fim) & (Voo.mes <= mes_fim))
            ).all()

            if voos:
                anos_meses = [f"{voo.ano}-{voo.mes}" for voo in voos]
                rpk = [voo.rpk for voo in voos]

                total_meses = (ano_fim - ano_inicio) * 12 + (mes_fim - mes_inicio + 1)
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
                plt.close() 

                mes_ano_inicio = f"{mes_inicio}/{ano_inicio}"
                mes_ano_fim = f"{mes_fim}/{ano_fim}"
            else:
                flash("Nenhum voo encontrado para o intervalo selecionado.", "danger")

    return render_template("dashboard.html", mercados=mercados, plot_url=plot_url, mes_ano_inicio=mes_ano_inicio, mes_ano_fim=mes_ano_fim)