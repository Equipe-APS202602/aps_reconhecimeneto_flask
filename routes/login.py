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
from werkzeug.security import generate_password_hash, check_password_hash


login_bp = Blueprint("login", __name__)


# =========================================================
# TELA DE LOGIN
# =========================================================


@login_bp.route("/login")
def login():
    # Se já estiver autenticado, abre o dashboard
    # if session.get("usuario_id"):
    #     return redirect(url_for("dashboard.dashboard"))

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

    # session.clear()

    # session["usuario_id"] = usuario["id"]
    # session["usuario_nome"] = usuario["nome"]
    # session["usuario_email"] = usuario["email"]
    # session["usuario_cargo"] = usuario["cargo"]

    # # =====================================================
    # # REGISTRAR ACESSO
    # # =====================================================

    # registrar_log(
    #     usuario_id=usuario["id"],
    #     acao="LOGIN FACIAL",
    #     recurso="LOGIN",
    #     resultado="PERMITIDO",
    # )

    # return jsonify(
    #     {
    #         "sucesso": True,
    #         "mensagem": "Autenticação realizada com sucesso.",
    #         "nome": usuario["nome"],
    #         "cargo": usuario["cargo"],
    #         "redirect": url_for("dashboard.dashboard"),
    #     }
    # )

    # =====================================================
    # CRIAR SESSÃO TEMPORÁRIA (ETAPA 1)
    # =====================================================

    session.clear()

    # Guarda o ID temporariamente. O usuário AINDA NÃO está logado de verdade.
    session["temp_usuario_id"] = usuario["id"]

    # =====================================================
    # REGISTRAR ACESSO DA ETAPA 1
    # =====================================================

    registrar_log(
        usuario_id=usuario["id"],
        acao="LOGIN FACIAL - ETAPA 1",
        recurso="LOGIN",
        resultado="PERMITIDO",
    )

    # Retorna sucesso, mas avisa o frontend que precisa da senha agora
    return jsonify(
        {
            "sucesso": True,
            "mensagem": "Rosto reconhecido. Por favor, insira sua senha.",
            "exigir_senha": True
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
# =========================================================
# LOGIN POR SENHA (ETAPA 2)
# =========================================================

@login_bp.route("/login/senha", methods=["POST"])
def login_senha():
    # 1. Verifica se o usuário passou pela etapa facial
    usuario_id = session.get("temp_usuario_id")
    if not usuario_id:
        return jsonify({"sucesso": False, "mensagem": "Acesso negado. Faça o reconhecimento facial primeiro."}), 401

    dados = request.get_json(silent=True)
    if not dados:
        return jsonify({"sucesso": False, "mensagem": "Dados não enviados."}), 400

    senha_digitada = dados.get("senha")
    if not senha_digitada:
        return jsonify({"sucesso": False, "mensagem": "Senha não informada."}), 400

    # 2. Buscar o usuário e o hash da senha no banco de dados
    conexao = None
    cursor = None
    usuario = None

    try:
        conexao = get_connection()
        cursor = conexao.cursor(dictionary=True)

        # Lembre-se de garantir que a coluna 'senha_hash' existe na sua tabela
        cursor.execute(
            """
            SELECT id, nome, email, cargo, senha_hash 
            FROM usuarios 
            WHERE id = %s 
            LIMIT 1
            """,
            (usuario_id,)
        )
        usuario = cursor.fetchone()

    except Exception as erro:
        print("Erro ao buscar senha do usuário:", erro)
        return jsonify({"sucesso": False, "mensagem": "Erro ao consultar o banco de dados."}), 500

    finally:
        if cursor is not None:
            cursor.close()
        if conexao is not None and conexao.is_connected():
            conexao.close()

    # 3. Validar a senha comparando o hash
    if not usuario or not check_password_hash(usuario["senha_hash"], senha_digitada):
        registrar_log(
            usuario_id=usuario_id,
            acao="LOGIN SENHA - ETAPA 2",
            recurso="LOGIN",
            resultado="NEGADO",
        )
        return jsonify({"sucesso": False, "mensagem": "Senha incorreta."}), 401

    # 4. Sucesso! Promove a sessão temporária para a sessão real
    session.pop("temp_usuario_id", None) # Remove a variável temporária

    session["usuario_id"] = usuario["id"]
    session["usuario_nome"] = usuario["nome"]
    session["usuario_email"] = usuario["email"]
    session["usuario_cargo"] = usuario["cargo"]

    registrar_log(
        usuario_id=usuario["id"],
        acao="LOGIN COMPLETO",
        recurso="LOGIN",
        resultado="PERMITIDO",
    )

    return jsonify(
        {
            "sucesso": True,
            "mensagem": "Autenticação concluída com sucesso.",
            "nome": usuario["nome"],
            "cargo": usuario["cargo"],
            "redirect": url_for("dashboard.dashboard"),
        }
    )