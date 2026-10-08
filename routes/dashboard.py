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
        # REGISTROS DISPONÍVEIS
        # =================================================

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM registros_cofre
            WHERE nivel_acesso IN ('FUNCIONARIO', 'DIRETOR')
        """)

        registros_disponiveis = cursor.fetchone()["total"]

        # =================================================
        # ACESSOS REALIZADOS HOJE
        # =================================================

        usuario_id = session.get("usuario_id")

        cursor.execute(
            """
            SELECT COUNT(*) AS total
            FROM logs_acesso
            WHERE usuario_id = %s
              AND DATE(data_hora) = CURDATE()
        """,
            (usuario_id,),
        )

        acessos_hoje = cursor.fetchone()["total"]

        # =================================================
        # ÚLTIMO ACESSO
        # =================================================

        cursor.execute(
            """
            SELECT data_hora
            FROM logs_acesso
            WHERE usuario_id = %s
              AND resultado = 'PERMITIDO'
            ORDER BY data_hora DESC
            LIMIT 1
        """,
            (usuario_id,),
        )

        ultimo_acesso = cursor.fetchone()

        if ultimo_acesso:
            ultimo_acesso = ultimo_acesso["data_hora"]
        else:
            ultimo_acesso = None

        # =================================================
        # DADOS ENVIADOS PARA OS TEMPLATES
        # =================================================

        dados = {
            "logs": logs,
            "acessos_permitidos": acessos_permitidos,
            "acessos_negados": acessos_negados,
            "registros_disponiveis": registros_disponiveis,
            "acessos_hoje": acessos_hoje,
            "ultimo_acesso": ultimo_acesso,
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
