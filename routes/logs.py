# routes/logs.py

from flask import Blueprint, render_template, request

from auth.permissions import permission_required
from database.connection import get_connection

logs_bp = Blueprint("logs", __name__, url_prefix="/logs")


# =========================================================
# VISUALIZAR LOGS
# =========================================================


@logs_bp.route("/")
@permission_required("VISUALIZAR_LOGS")
def index():
    # Recebe o filtro pela URL:
    # /logs/?resultado=PERMITIDO
    resultado = request.args.get("resultado", "").upper()

    filtro_sql = ""
    parametros = []

    # Permite somente filtros conhecidos
    if resultado in ["PERMITIDO", "NEGADO"]:
        filtro_sql = """
            WHERE logs_acesso.resultado = %s
        """

        parametros.append(resultado)

    else:
        resultado = ""

    consulta = f"""
        SELECT
            logs_acesso.id,
            logs_acesso.acao,
            logs_acesso.recurso,
            logs_acesso.resultado,
            logs_acesso.data_hora,
            usuarios.nome,
            usuarios.cargo
        FROM logs_acesso
        LEFT JOIN usuarios
            ON logs_acesso.usuario_id = usuarios.id
        {filtro_sql}
        ORDER BY logs_acesso.data_hora DESC
    """

    conexao = None
    cursor = None
    logs = []

    try:
        conexao = get_connection()
        cursor = conexao.cursor(dictionary=True)

        if parametros:
            cursor.execute(consulta, tuple(parametros))
        else:
            cursor.execute(consulta)

        logs = cursor.fetchall()

    except Exception as erro:
        print("Erro ao consultar logs:", erro)

    finally:
        if cursor is not None:
            cursor.close()

        if conexao is not None and conexao.is_connected():
            conexao.close()

    return render_template("logs/index.html", logs=logs, filtro_resultado=resultado)
