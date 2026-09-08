# routes/usuarios.py

from flask import Blueprint, render_template, request, redirect, url_for, flash

from auth.permissions import permission_required

from database.connection import get_connection

usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")


# =========================================================
# LISTAR USUÁRIOS
# =========================================================


@usuarios_bp.route("/")
@permission_required("GERENCIAR_USUARIOS")
def index():

    conexao = get_connection()

    cursor = conexao.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            id,
            nome,
            email,
            cargo,
            face_id,
            ativo,
            criado_em
        FROM usuarios
        ORDER BY nome
        """)

    usuarios = cursor.fetchall()

    cursor.close()
    conexao.close()

    return render_template("usuarios/index.html", usuarios=usuarios)


# =========================================================
# CRIAR USUÁRIO
# =========================================================


@usuarios_bp.route("/criar", methods=["POST"])
@permission_required("GERENCIAR_USUARIOS")
def criar():

    nome = request.form.get("nome")

    email = request.form.get("email")

    cargo = request.form.get("cargo")

    face_id = request.form.get("face_id")

    if not nome or not email or not cargo:

        flash("Preencha todos os campos obrigatórios.", "warning")

        return redirect(url_for("usuarios.index"))

    conexao = get_connection()

    cursor = conexao.cursor()

    try:

        cursor.execute(
            """
            INSERT INTO usuarios
            (
                nome,
                email,
                cargo,
                face_id
            )
            VALUES (%s, %s, %s, %s)
            """,
            (nome, email, cargo, face_id if face_id else None),
        )

        conexao.commit()

        flash("Usuário cadastrado com sucesso.", "success")

    except Exception as erro:

        conexao.rollback()

        flash(f"Erro ao cadastrar usuário: {erro}", "danger")

    finally:

        cursor.close()
        conexao.close()

    return redirect(url_for("usuarios.index"))


# =========================================================
# DESATIVAR USUÁRIO
# =========================================================


@usuarios_bp.route("/desativar/<int:id>", methods=["POST"])
@permission_required("GERENCIAR_USUARIOS")
def desativar(id):

    conexao = get_connection()

    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE usuarios
        SET ativo = FALSE
        WHERE id = %s
        """,
        (id,),
    )

    conexao.commit()

    cursor.close()
    conexao.close()

    flash("Usuário desativado.", "success")

    return redirect(url_for("usuarios.index"))


# =========================================================
# ATIVAR USUÁRIO
# =========================================================


@usuarios_bp.route("/ativar/<int:id>", methods=["POST"])
@permission_required("GERENCIAR_USUARIOS")
def ativar(id):

    conexao = get_connection()

    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE usuarios
        SET ativo = TRUE
        WHERE id = %s
        """,
        (id,),
    )

    conexao.commit()

    cursor.close()
    conexao.close()

    flash("Usuário ativado.", "success")

    return redirect(url_for("usuarios.index"))
