from flask import Blueprint, render_template, session

from auth.permissions import login_required
from database.connection import get_connection

dashboard_bp = Blueprint("dashboard", __name__)


# =========================================================
# DASHBOARD PRINCIPAL
# =========================================================


@dashboard_bp.route("/")
@dashboard_bp.route("/dashboard")
@login_required
def dashboard():

    cargo = session.get("usuario_cargo", "").upper()

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    try:

        # =================================================
        # ATIVIDADE RECENTE
        # =================================================

        cursor.execute("""
            SELECT
                l.id,
                u.nome AS usuario,
                l.acao,
                l.recurso,
                l.resultado,
                l.data_hora
            FROM logs_acesso l
            LEFT JOIN usuarios u
                ON l.usuario_id = u.id
            ORDER BY l.data_hora DESC
            LIMIT 5
        """)

        logs = cursor.fetchall()

        # =================================================
        # ACESSOS PERMITIDOS
        # =================================================

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM logs_acesso
            WHERE resultado = 'PERMITIDO'
        """)

        acessos_permitidos = cursor.fetchone()["total"]

        # =================================================
        # ACESSOS NEGADOS
        # =================================================

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM logs_acesso
            WHERE resultado = 'NEGADO'
        """)

        acessos_negados = cursor.fetchone()["total"]

        # =================================================
        # DADOS ENVIADOS PARA O TEMPLATE
        # =================================================

        dados = {
            "logs": logs,
            "acessos_permitidos": acessos_permitidos,
            "acessos_negados": acessos_negados,
        }

        # =================================================
        # DASHBOARD DE ACORDO COM O CARGO
        # =================================================

        if cargo == "MINISTRO":
            return render_template("dashboard/ministro.html", **dados)

        if cargo == "DIRETOR":
            return render_template("dashboard/diretor.html", **dados)

        return render_template("dashboard/funcionario.html", **dados)

    finally:
        cursor.close()
        connection.close()
