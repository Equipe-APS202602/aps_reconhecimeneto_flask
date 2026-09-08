# routes/login.py

from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    session,
    redirect,
    url_for,
)

from auth.facial import reconhecer_rosto
from database.connection import get_connection

login_bp = Blueprint("login", __name__)


# =========================================================
# TELA DE LOGIN
# =========================================================


@login_bp.route("/login")
def login():
    # Se já estiver autenticado, abre o dashboard
    if session.get("usuario_id"):
        return redirect(url_for("dashboard.dashboard"))

    return render_template("login.html")


# =========================================================
# LOGIN FACIAL
# =========================================================


@login_bp.route("/login/facial", methods=["POST"])
def login_facial():
    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({"sucesso": False, "mensagem": "Dados não enviados."}), 400

    imagem = dados.get("imagem")

    if not imagem:
        return jsonify({"sucesso": False, "mensagem": "Imagem não enviada."}), 400

    # Realiza o reconhecimento facial
    resultado = reconhecer_rosto(imagem)

    if not resultado.get("sucesso"):
        registrar_log(
            usuario_id=None,
            acao="TENTATIVA DE LOGIN FACIAL",
            recurso="LOGIN",
            resultado="NEGADO",
        )

        return (
            jsonify(
                {
                    "sucesso": False,
                    "mensagem": resultado.get("mensagem", "Rosto não reconhecido."),
                }
            ),
            401,
        )

    face_id = resultado.get("usuario_id")

    if not face_id:
        return (
            jsonify(
                {
                    "sucesso": False,
                    "mensagem": "O reconhecimento não retornou um identificador.",
                }
            ),
            401,
        )

    # =====================================================
    # BUSCAR USUÁRIO
    # =====================================================

    conexao = None
    cursor = None

    try:
        conexao = get_connection()
        cursor = conexao.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                id,
                nome,
                email,
                cargo,
                ativo
            FROM usuarios
            WHERE face_id = %s
            LIMIT 1
            """,
            (face_id,),
        )

        usuario = cursor.fetchone()

    except Exception as erro:
        print("Erro ao buscar usuário:", erro)

        return (
            jsonify(
                {
                    "sucesso": False,
                    "mensagem": "Erro ao consultar o usuário no banco de dados.",
                }
            ),
            500,
        )

    finally:
        if cursor is not None:
            cursor.close()

        if conexao is not None and conexao.is_connected():
            conexao.close()

    # Usuário não cadastrado
    if not usuario:
        registrar_log(
            usuario_id=None,
            acao="LOGIN FACIAL",
            recurso="LOGIN",
            resultado="NEGADO",
        )

        return jsonify({"sucesso": False, "mensagem": "Usuário não cadastrado."}), 401

    # Usuário desativado
    if not usuario["ativo"]:
        registrar_log(
            usuario_id=usuario["id"],
            acao="LOGIN FACIAL",
            recurso="LOGIN",
            resultado="NEGADO",
        )

        return jsonify({"sucesso": False, "mensagem": "Usuário desativado."}), 403

    # =====================================================
    # CRIAR SESSÃO
    # =====================================================

    session.clear()

    session["usuario_id"] = usuario["id"]
    session["usuario_nome"] = usuario["nome"]
    session["usuario_email"] = usuario["email"]
    session["usuario_cargo"] = usuario["cargo"]

    # =====================================================
    # REGISTRAR ACESSO
    # =====================================================

    registrar_log(
        usuario_id=usuario["id"],
        acao="LOGIN FACIAL",
        recurso="LOGIN",
        resultado="PERMITIDO",
    )

    return jsonify(
        {
            "sucesso": True,
            "mensagem": "Autenticação realizada com sucesso.",
            "nome": usuario["nome"],
            "cargo": usuario["cargo"],
            "redirect": url_for("dashboard.dashboard"),
        }
    )


# =========================================================
# LOGOUT
# =========================================================


@login_bp.route("/logout")
def logout():
    usuario_id = session.get("usuario_id")

    if usuario_id:
        registrar_log(
            usuario_id=usuario_id,
            acao="LOGOUT",
            recurso="LOGIN",
            resultado="PERMITIDO",
        )

    session.clear()

    return redirect(url_for("login.login"))


# =========================================================
# FUNÇÃO PARA REGISTRAR LOG
# =========================================================


def registrar_log(usuario_id, acao, recurso, resultado):
    conexao = None
    cursor = None

    try:
        conexao = get_connection()
        cursor = conexao.cursor()

        cursor.execute(
            """
            INSERT INTO logs_acesso
                (usuario_id, acao, recurso, resultado)
            VALUES
                (%s, %s, %s, %s)
            """,
            (usuario_id, acao, recurso, resultado),
        )

        conexao.commit()

    except Exception as erro:
        print("Erro ao registrar log:", erro)

    finally:
        if cursor is not None:
            cursor.close()

        if conexao is not None and conexao.is_connected():
            conexao.close()
